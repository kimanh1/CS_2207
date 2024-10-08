# Sidebar for user input
import streamlit as st
from prediction import predictForSale
from prediction import predictForLease
import numpy as np
from datetime import datetime
import joblib
import pandas as pd
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
st.set_page_config(layout="wide")



day_mapping = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6
}
land_type_options = [
    "Alley house",
    "Apartment",
    "Room for rent",
    "Adjacent townhouses",
    "Office, Business premises",
    "Streetfront house",
    "Service apartment, mini",
    "Duplex"
]
type_options = [
    "LEASE",
    "SALE"
]
col2,col3 = st.columns([1,1])

# with col1:
#     # col13, col14 = st.columns([1,1])
#     # with col13:
#     province = st.selectbox('Provice:', list(province_districts.keys()))
# # with col14:
#     # selected_district = 
#     if province:
#         districts = st.selectbox('District:',province_districts[province])
# col15, col16 = st.columns([1,1])
# with col15:
    # STREET = st.text_input("Street")
STREET = st.sidebar.text_input("Street", "3 Thang 2")

if STREET:
    geolocator = Nominatim(user_agent="GTA Lookup")
    # Geocode the street name to get the location
    location = geolocator.geocode(STREET + ", Viet Nam")
    
    if location:
        lat = location.latitude
        lon = location.longitude

        # Get the full address to extract ward, district, and province
        full_address = location.address.split(", ")
        if len(full_address) >= 4:
            ward = full_address[-5]  # Ward is usually the fourth last element
            districts = full_address[-4]  # District is the third last element
            province = full_address[-3]  # Province is the second last element

            # Display selected ward, district, and province
            # st.success(f"Location found: {ward}, {district}, {province}")
        else:
            st.warning("Unable to retrieve full address details.")
    else:
        st.error("Location not found. Please check your input.")

# Display dropdowns for wards, districts, and provinces
    # st.sidebar.subheader("Select Ward, District, and Province")
    selected_ward = st.sidebar.write( ward)
    selected_district = st.sidebar.write( districts)
    selected_province = st.sidebar.write( province)

#     WARD = st.text_input("Ward")
with col2:
    # geolocator = Nominatim(user_agent="GTA Lookup")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    # location = geolocator.geocode(STREET+", "+WARD+", "+districts+", "+province+", "+"Viet Nam")

    # lat = location.latitude
    # lon = location.longitude

    map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})

    if lat is not None and lon is not None:
        
    # Optionally display the map
        st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}),use_container_width=True)
        st.success(f"Latitude: {lat}, Longitude: {lon}")
    else:
        st.error("Location not found. Please check your input.")

#     image_path = 'real.png'
#     st.markdown(
#     """
#     <style>
#     .center-image {
#         # display: block;
#         # margin-left: auto;
#         # margin-right: auto;
#         display: flex;
#         justify-content: center;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
#     st.markdown('<div class="center-image">', unsafe_allow_html=True)
#     st.image(image_path, use_column_width=True)
#     st.markdown('</div>', unsafe_allow_html=True)
#     st.image("VIETNAM.png", use_column_width=True)


with col3:

    
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
    # Dictionary mapping provinces to their districts
    
    
    col13, col14 = st.columns([1,1])
    with col13:
        land_type = st.selectbox("Choose the type of land:", land_type_options)
    with col14: 
        real_estate_type = st.selectbox("Choose the type of real estate:", type_options)
    col3, col4 = st.columns([1,1])
    with col3:
        surface = st.number_input(label="Surface",step=1.,format="%.1f")
        # Price_m2 = st.text_input("Price m2")
    with col4:      
        used_surface =st.number_input(label="Used surface",step=1.,format="%.1f")
    
    col5, col6 = st.columns([1, 1])
    with col5:
        LENGTH = st.number_input(label="Length",step=1.,format="%.0f")
      
    with col6:
        width = st.number_input(label="Width",step=1.,format="%.0f")

    # Row 3
    col7, col8,col9 = st.columns([1, 1,1])
    with col7:
        NB_FLOORS =st.number_input(label="Number of floors",step=1.,format="%.0f")
       
    with col8:
        NB_ROOMS = st.number_input(label="Number of rooms",step=1.,format="%.0f")

    with col9:
       NB_TOLETS = st. number_input(label="Number of toilets",step=1.,format="%.0f")
   
    selected_date = st.date_input("Date", datetime.now())
    selected_day = selected_date.day
    # st.write("day:", selected_day)
    
    day_of_week = selected_date.strftime("%A")
    day_of_week = day_mapping[day_of_week]
    # st.write("day of week:", day_of_week)
    st.markdown(input_style, unsafe_allow_html=True)
    if st.button("Predict"):
        standard_scaler = joblib.load('standard_scaler.joblib')
        min_max_scaler = joblib.load('min_max_scaler.joblib')    

        surface_reshaped = np.array([surface]) 
        # surface_reshape=surface_reshaped.reshape(1, -1)
        # st.write("Scaled surface:", surface_reshaped.shape)
        # Transform using the scaler
        surface= standard_scaler.transform([surface_reshaped])
        # st.write("Scaled surface:", surface)

        # st.write("Scaled surface:", surface_scaled)
        # surface=standard_scaler.transform(surface_reshaped)
        NB_FLOORS_reshaped = np.array([NB_FLOORS]) 
        # NB_FLOORS_reshape=NB_FLOORS_reshaped.reshape(1, -1)
        # st.write("Scaled surface:", surface_reshaped.shape)
        NB_FLOORS=min_max_scaler.transform([NB_FLOORS_reshaped])
        # st.write("rooms:", NB_FLOORS)
        if real_estate_type=="SALE":
           
            # if land_type=="Streetfront house":
            #     land_type_is=TRUE
            # else:
            #     land_type_is='FALSE'
            if land_type == 'Alley house':
                land_type_is = True
            else:
                land_type_is = False
            # if province=="HOCHIMINH CITY":
            #     city=TRUE
            # else:
            #     city=FALSE
            if province == 'Thành phố Hồ Chí Minh':
                city = True
            else:
                city = False
            #st.write( ([[NB_ROOMS,lat,used_surface,surface[0, 0],lon,	width,	NB_FLOORS[0, 0],	LENGTH,	city,land_type_is]]))
            a=([[NB_ROOMS,lat,used_surface,surface[0, 0],lon,	width,	NB_FLOORS[0, 0],	LENGTH,	city,land_type_is]])
            result = predictForSale(
            np.array(a, dtype="object") )
            # st.text(result[0])
            st.text(f"{float(result[0]) * 1000000:,.0f} VND ≈ {round(float(result[0])/1000)} billion VND")
            
            #st.write( ([[NB_ROOMS,lat,used_surface,surface[0, 0],lon,	width,	NB_FLOORS[0, 0],	LENGTH,	city,land_type_is]]))
        #cb = joblib.load("cb_model.sav")
        #st.write(cb.predict([[0.969802452722392, surface[0, 0],	used_surface,	width,	1856.904762,	NB_FLOORS[0, 0],	LENGTH,	selected_day,	NB_ROOMS,	day_of_week]]))
        else:
            
            # if land_type=="Office, Business premises":
            #     land_type_is='TRUE'
            # else:
            #     land_type_is='FALSE'
            if land_type == 'Office, Business premises':
                land_type_is = True
            else:
                land_type_is = False
            #st.write( [[surface[0, 0],used_surface,lat,lon,NB_TOLETS,NB_ROOMS,LENGTH,	width, land_type_is	,	day_of_week]])
            a=( [[ surface[0, 0],used_surface,lat,lon,NB_TOLETS,NB_ROOMS,LENGTH,	width, land_type_is	,	day_of_week]])
            # print(a.shape)
            result = predictForLease(
            np.array(a, dtype="object") ) 
            st.text(f"{float(result[0]) * 1000000:,.0f} VND/Month ≈ {round(float(result[0]))} million VND/Month ")
            
            #st.write( [[ surface[0, 0],used_surface,lat,lon,NB_TOLETS,NB_ROOMS,LENGTH,	width, land_type_is	,	day_of_week]])