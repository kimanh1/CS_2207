# Sidebar for user input
import streamlit as st
import streamlit as st
import joblib
# original_title = '<h1 style="font-family: san-serif; color:white; font-size: 20px;">Streamlit CSS Styling✨ </h1>'
# st.markdown(original_title, unsafe_allow_html=True)
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns([1,1])

with col1:
    background_image = """
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background-image: url("https://content.jdmagicbox.com/comp/allahabad/b4/0532px532.x532.190510161607.y8b4/catalogue/n-i-real-estate-civil-lines-allahabad-estate-agents-yw16py6790.jpg");
        background-size: auto 100vh;  # This sets the size to cover 100% of the viewport width and height
        background-position: center;  
        background-repeat: no-repeat;
    }
    </style>
    """

    st.markdown(background_image, unsafe_allow_html=True)


with col2:

    
    input_style= """
    <style>
    input[type="text"] {
        background-color: transparent;
        color: #cc5500;  // This changes the text color inside the input box
        border: 2px solid #4CAF50;  /* Change this color to your desired border color */
        border-radius: 5px;  /* Optional: Adds rounded corners */
        padding: 10px;
    }
    div[data-baseweb="base-input"] {
        background-color: transparent !important;
    }
    [data-testid="stAppViewContainer"] {
        background-color: transparent !important;
    }
    </style>
    """
    
    col3, col4 = st.columns([1,1])
    with col3:
        name = st.text_input("Name")
    with col4:
        email = st.text_input("Email")
    
    col5, col6 = st.columns([1, 1])
    with col5:
        phone = st.text_input("Phone", key="phone", placeholder="Enter your phone number")
    with col6:
        address = st.text_input("Address", key="address", placeholder="Enter your address")

    # Row 3
    col7, col8 = st.columns([1, 1])
    with col7:
        city = st.text_input("City", key="city", placeholder="Enter your city")
    with col8:
        country = st.text_input("Country", key="country", placeholder="Enter your country")
    # predict_button = st.button(label='Predict')
    st.markdown(input_style, unsafe_allow_html=True)
    if st.button("Predict"):
        cb = joblib.load("cb_model.sav")
        st.text(cb.predict([[-0.964187343,-0.095079871,	113,	4,	1856.904762,	0,	29,	28,	0,	2]]))
