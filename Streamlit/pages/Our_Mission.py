import streamlit as st

st.set_page_config(page_title="Our Mission", page_icon="📈")

st.markdown("# Our Mission")
st.sidebar.header("Our Mission")
st.write(
    """If you are an advertising agency, online marketing strategist, or a business owner,
    you know how hard it can be to find the right audience for your product or service. Trying
    to identify members of your target audience can be a time-consuming and expensive process.
    Our mission is to make this process easier and more affordable for you. We are proud to
    demonstrate our work on social profiling with transformers. Our application allows you to
    upload a list of names that exemplify your target audience, then based on the parameters you
    want to identify in your potential customers, we will return a list of names that match your
    query within a specified degree of similarity."""
)

st.markdown("## How is this different?")
st.write("""Compared to other social profiling tools, our application is unique in that it uses
    sentence transformers to embed text data sourced from social media profiles. Then, we use the
    Pinecone vector database to create an index of the embeddings and perform similarity searches.
    Compared to other social profiling tools, our application is highlt effective at scale, as our
    embeddings have been trained on a wide variety of social media attributes along with a swathe of
    relevant social profile information like salary, location, and job titles. This means that your
    options for identifying your target audience are virtually limitless. """)

# Apply custom styles
# st.markdown("""
# <style>
#     body {
#         font-family: 'IBM Plex Sans', sans-serif;
#         color: #333;
#     }
#     h1, h2, h3, h4, h5, h6 {
#         color: #333;
#     }
#     a {
#         color: #333;
#         text-decoration: underline;
#     }
# </style>
# """, unsafe_allow_html=True)