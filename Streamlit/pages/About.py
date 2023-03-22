import streamlit as st

st.set_page_config(page_title="About the Contributors", page_icon="📈")



st.markdown("# About the Contributors")
# st.sidebar.header("About the Contributors")
st.write(
    """Our project was developed by a team of six Oregon State University students, in collaboration with eCairn.
    If you'd like to ask any questions about the development, functionality, or usage of our application, please
    contact any of the contributors or the eCairn team directly."""
)

# Add your developers' information as a list of dictionaries
developers = [
    {"name": "Alexander Jones", "email": "joneale2@oregonstate.edu", "image": "image1.png",
     "description": "Alex is a 4th-year Computer Science student on the Artificial Intelligence track at Oregon State University."
                    "In this project, he was responsible for backend development, database design, transformer model research, and API integration."},
    {"name": "Ethan Nechanicky", "email": "nechanie@oregonstate.edu", "image": "image2.png",
     "description": "Developer 2 description"},
    {"name": "Mishary Alotaibi", "email": "lotaimi@oregonstate.edu", "image": "image1.png",
     "description": "Developer 1 description"},
    {"name": "Phillip Dinh", "email": "email1@example.com", "image": "image1.png",
     "description": "Developer 1 description"},
    {"name": "Haofan Wang", "email": "wanghaof@oregonstate.edu", "image": "image1.png",
     "description": "Developer 1 description"},
    {"name": "Julian Gilmour", "email": "gilmouju@oregonstate.edu", "image": "image1.png",
     "description": "Developer 1 description"},

    # Add more developers as needed
]

for dev in developers:
    st.subheader(dev["name"])
    st.write(dev["email"])
    #st.image(dev["image"], width=100)
    #st.write(dev["description"])

st.markdown("# About the Project Author")
dom = {"name": "Dominique Lahaix", "email": "dominique.lahaix@ecairn.com", "image": "image1.png",
         "description": "eCairn founder and CEO Dominique Lahaix has successfully led the development and deployment"
                        " of AI/ML solutions at F100 companies such as HP and eBay. He later "
                        "moved to the US to launch his own startup, eCairn, building ML powered"
                        " solutions for Social Marketing and Social Selling. In that position"
                        " he helped companies like Converse, Hershey’s, 3M, and large private "
                        "banks in the US and in Europe leverage social data to transform their"
                        " marketing and sales processes. He owns a patent on tribe mapping with"
                        " linguistic signals."}

st.subheader(dom["name"])
st.write(dom["email"])
#st.image(dev["image"], width=100)
st.write(dom["description"])

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
