import streamlit as st

st.set_page_config(page_title="Documentation", page_icon="📈")

st.markdown("# Documentation")
st.sidebar.header("Documentation")
st.write(
    """As our project is a product for eCairn, we are restricting access to the documentation for the time being.\n
    If you are interested in learning more about our project, please contact eCairn directly."""
)


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