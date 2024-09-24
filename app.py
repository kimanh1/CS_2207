# Sidebar for user input
import streamlit as st

st.sidebar.write("### Predict House Price")
sqft = st.sidebar.number_input('Square Footage', min_value=500, max_value=5000, value=1500)
bedrooms = st.sidebar.slider('Number of Bedrooms', min_value=1, max_value=10, value=3)
bathrooms = st.sidebar.slider('Number of Bathrooms', min_value=1, max_value=5, value=2)

# Make a prediction based on the user input
# user_input = np.array([[sqft, bedrooms, bathrooms]])
# predicted_price = model.predict(user_input)

# Display the predicted price
st.sidebar.write(f"Predicted Price: 2")
