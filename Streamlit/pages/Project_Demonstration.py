# Demonstration Page
from types import SimpleNamespace
import json
import streamlit as st
import datetime
import torch
import pinecone
import pandas as pd

from database_class import DB
from model_class import Model
from system_logging import SystemLogging
from pinecone_helper import *
from eCairn_connector import eCairnConnector
from connection_type import Types

databaseConfig: SimpleNamespace
pineconeConfig: SimpleNamespace
with open("config.json", "r") as f:
    config = json.load(f, object_hook=lambda x: SimpleNamespace(**x))
    databaseConfig = config.oregonstate.data
    loggingConfig = config.oregonstate.logging
    pineconeConfig = config.pinecone


# Home Page
def set_model(test_model, logger):
    # Name
    name = st.text_input('Name', value="Test", help='Name for database entry')
    test_model.name = name

    # Tokenizer
    tokenizer_name = st.selectbox('Tokenizer', ('sentence-transformers/all-MiniLM-L6-v2', 'Option 2'),
                                  index=0, help='Sentence Transformer Tokenizer')
    test_model.tokenizer_name = tokenizer_name

    # Model
    model_name = st.selectbox('Model', ('sentence-transformers/all-MiniLM-L6-v2', 'Option 2'),
                              index=0, help='Sentence Transformer Model')
    test_model.model_name = model_name

    # TODO Make conditional with other models
    # Dimensions
    if model_name == 'sentence-transformers/all-MiniLM-L6-v2':
        test_model.dimensions = 384
    else:
        test_model.dimensions = 0

    # Namespace
    name_space = st.text_input('Pinecone Namespace',
                               value="Streamlit_Test", help='Pinecone namespace to store embeddings.')
    logger.pinecone_namespace = name_space

    # Rows
    rows = st.number_input('Rows (Maximum)', help='Number of database entries to embed.', step=1)
    test_model.rows = rows

    # Top N
    top_n = st.number_input('Similar Results', help='Number of results from embeddings.', step=1)
    logger.top_n = top_n

    if torch.cuda.is_available():
        test_model.device = "cuda:0"
    else:
        test_model.device = "cpu"


def setLogger(logger, tokenizer_name, model_name, dimensions, device, name, index):
    logger.system_start = datetime.datetime.now()
    logger.tokenizer = tokenizer_name
    logger.model = model_name
    logger.model_dim = dimensions
    logger.input = [i for i in range(20)]
    logger.device = device
    logger.name = name
    logger.pinecone_index = index
    
    
# ------------------------------------------------------------------------
# Set Page Base UI
st.set_page_config(page_title="Project Demonstration")
st.sidebar.success("Project Demonstration")
st.subheader('Model Embedding')
col1, col2 = st.columns(2)

# Create a model class
test_model = Model

# Connect to Database
db = DB(databaseConfig)

# Create a logger class
logger = SystemLogging(loggingConfig)

# Get Model Inputs
with col1:
    set_model(test_model, logger)

run_btn = st.button("Embed Data")

if run_btn:
    setLogger(logger,
              test_model.tokenizer_name,
              test_model.model_name,
              test_model.dimensions,
              test_model.device,
              test_model.name,
              pineconeConfig.index)

    # if test_model.rows != 0:
    # 	new_data = eCairnConnector(Types.Connection.FROM_TYPE_DB, db_config=databaseConfig, limit=test_model.rows)
    # else:
    # 	new_data = eCairnConnector(Types.Connection.FROM_TYPE_DB, db_config=databaseConfig)

    # test_list = new_data.get_dataframe()
    # test_list = test_list.to_numpy()

    # Old db method
    test_list = db.get_test_list(test_model.rows)

    # Render rows selected
    with col2:
        st.write(test_list)

    # Embed data and set progress bar
    progress_bar = st.progress(0, text="Please wait")
    embeddings_dataset = test_model().get_embeddings(logger, test_list, progress_bar)

    st.success('Done!')

    # Render embeddings
    st.write(embeddings_dataset)

# PINECONE
# pinecone.init(api_key=pineconeConfig.key, environment=pineconeConfig.env)
# index = pinecone.Index(pineconeConfig.index)

# Works uncomment when we want to upload
# uploadToPineCone(logger, index, embeddings_dataset)

# TODO Change database_class to eCairnConnector and this might Work
# uploadLog(logger, index, embeddings_dataset)


col1_1, col2_1 = st.columns(2, gap="large")

# Connect to Database
databaseConfig: SimpleNamespace
with open("config.json", "r") as f:
    config = json.load(f, object_hook=lambda x: SimpleNamespace(**x))
    databaseConfig = config.oregonstate.data
db = DB(databaseConfig)

query_df = pd.DataFrame()

# SQL input
with col1_1:
    st.subheader("Manual SQL Query")
    with st.form(key='query_form'):
        raw_code = st.text_area("Enter SQL Query")
        submit_code = st.form_submit_button("Execute")

    # Show DB table names
    with st.expander("DB Tables"):
        tables_df = db.sql_executor("SHOW TABLES;")
        st.dataframe(tables_df)

    # Run query
    if submit_code:
        st.info("Query Submitted")
        st.code(raw_code)
        query_df = db.sql_executor(raw_code)

    # Table

# Results Layouts
with col2_1:
    st.subheader("Search Twitter Profiles")
    search_attribute = st.selectbox(
        'Attribute to query',
        ('id', 'person_id', 'twitter_id', 'screen_name', 'name', 'location'))

    # Query by ID
    if search_attribute == 'id' or search_attribute == 'person_id' or search_attribute == 'twitter_id':
        search_id = st.number_input(('Please input: ' + search_attribute), step=1)

        error_message = st.empty()

        id_btn = st.button("Run Query")
        if id_btn:
            submit_info = st.info("Query Submitted")
            query_df = db.query_by_id(search_id)
            if query_df.empty:
                submit_info.empty()
                error_message = st.error('No entries found', icon="🚨")

    # Other queries
    if search_attribute == 'name' or search_attribute == 'screen_name' or search_attribute == 'location':
        search_txt = st.text_input('Search by: ' + search_attribute)

        txt_btn = st.button("execute")

        if search_attribute == 'location':
            location_warning = st.warning(
                'Same location may be formatted differently in database for different entries', icon="⚠️")

        if txt_btn:
            st.info("Query Submitted")
            location_warning.empty()
            query_df = db.query_by_text(search_attribute, search_txt)
            if query_df.empty:
                submit_info.empty()
                error_message = st.error('No entries found', icon="🚨")

# Render query results
if not query_df.empty:
    st.dataframe(query_df)
    submit_info.empty()