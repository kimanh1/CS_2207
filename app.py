# Sidebar for user input
import streamlit as st
from prediction import predict
import numpy as np
from datetime import datetime
import joblib
import pandas as pd
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
st.set_page_config(layout="wide")

province_districts = {
    'Ha Noi': [
        'Ba Dinh', 'Hoan Kiem', 'Tay Ho', 'Long Bien', 'Cau Giay', 'Dong Da',
        'Hai Ba Trung', 'Hoang Mai', 'Thanh Xuan', 'Nam Tu Liem', 'Bac Tu Liem',
        'Dong Anh', 'Gia Lam', 'Thanh Tri', 'Soc Son', 'Me Linh', 'Dan Phuong',
        'Hoai Duc', 'Thanh Oai', 'Quoc Oai', 'Chuong My', 'Thuong Tin',
        'Phu Xuyen', 'Ung Hoa', 'My Duc', 'Son Tay'
    ],
    'Ho Chi Minh City': [
        'District 1', 'District 2', 'District 3', 'District 4', 'District 5',
        'District 6', 'District 7', 'District 8', 'District 9', 'District 10',
        'District 11', 'District 12', 'Binh Thanh', 'Go Vap', 'Phu Nhuan',
        'Tan Binh', 'Tan Phu', 'Thu Duc', 'Nha Be', 'Hoc Mon', 'Cu Chi',
        'Binh Chanh'
    ],
    'Da Nang': [
        'Hai Chau', 'Thanh Khe', 'Lien Chieu', 'Son Tra', 'Ngu Hanh Son',
        'Cam Le', 'Hoa Vang'
    ],
    'Hai Phong': [
        'Hong Bang', 'Le Chan', 'Ngo Quyen', 'Kien An', 'Duong Kinh',
        'Hai An', 'Do Son', 'Tien Lang', 'Vinh Bao', 'An Duong', 'An Lao',
        'Kien Thuy', 'Thuy Nguyen', 'Cat Hai'
    ],
    'Can Tho': [
        'Ninh Kieu', 'Binh Thuy', 'O Mon', 'Thot Not', 'Phong Dien'
    ],
    'An Giang': [
        'Long Xuyen', 'Chau Doc', 'An Phu', 'Tan Chau', 'Chau Phu',
        'Thot Not', 'Phu Tan', 'Tri Ton', 'Tinh Bien', 'Cho Moi', 'Chau Thanh'
    ],
    'Ba Ria - Vung Tau': [
        'Vung Tau', 'Ba Ria', 'Long Dien', 'Dat Do', 'Xuyen Moc', 
        'Tan Thanh', 'Vinh Phuc'
    ],
    'Bac Giang': [
        'Bac Giang', 'Lang Giang', 'Yen The', 'Tan Yen', 'Viet Yen',
        'Hiep Hoa', 'Son Dong', 'Luc Ngan', 'Dinh Lap'
    ],
    'Bac Kan': [
        'Bac Kan', 'Ba Be', 'Bach Thong', 'Cho Don', 'Cho Moi',
        'Na Ri', 'Ngan Son', 'Pac Nam'
    ],
    'Ben Tre': [
        'Ben Tre', 'Chau Thanh', 'Binh Dai', 'Thanh Phu', 'Giong Trom',
        'Mo Cay Bac', 'Mo Cay Nam', 'Ba Tri'
    ],
    'Binh Duong': [
        'Thu Dau Mot', 'Di An', 'Thuan An', 'Ben Cat', 'Tan Uyen',
        'Phu Giao', 'Bac Tan Uyen'
    ],
    'Binh Dinh': [
        'Qui Nhon', 'An Nhon', 'Hoai Nhon', 'Phu My', 'Vinh Thanh',
        'Tay Son', 'Phu Cat', 'Tam Quan', 'Hoai An', 'Duc Phong', 'Nhan Hoa'
    ],
    'Binh Phuoc': [
        'Dong Xoai', 'Phuoc Long', 'Bu Dang', 'Bu Gia Map', 'Chon Thanh',
        'Hon Quan', 'Phu Rieng', 'Loc Ninh', 'Dong Phu', 'Bu Dop'
    ],
    'Ca Mau': [
        'Ca Mau', 'Dam Doi', 'Nam Can', 'Cai Nuoc', 'Tran Van Thoi',
        'Ngoc Hien', 'U Minh', 'Thoi Binh', 'Ke Sach'
    ],
    'Dak Lak': [
        'Buon Ma Thuot', 'Buon Ho', 'Ea Hleo', 'Cu Kuin', 'Krong Ana',
        'Krong Buk', 'Krong Nang', 'M Drak', 'Lak', 'Dak Mil', 'Dak R Lap'
    ],
    'Dak Nong': [
        'Gia Nghia', 'Dak Mil', 'Dak Song', 'Cu Jut', 'Krong No',
        'Tuy Duc', 'Dak R Lap'
    ],
    'Dien Bien': [
        'Dien Bien Phu', 'Muong Lay', 'Dien Bien', 'Muong Nhe',
        'Muong Cha', 'Tua Chua', 'Nam Po'
    ],
    'Ha Giang': [
        'Ha Giang', 'Dong Van', 'Vi Xuyen', 'Quan Ba', 'Yen Minh',
        'Bac Me', 'Gia Chau', 'Hoang Su Phi', 'Meo Vac', 'Xin Man'
    ],
    'Ha Nam': [
        'Phu Ly', 'Duy Tien', 'Kim Bang', 'Binh Luc', 'Ly Nhan'
    ],
    'Ha Tinh': [
        'Ha Tinh', 'Hong Linh', 'Ky Anh', 'Cam Xuyen', 'Can Loc',
        'Duc Tho', 'Huong Khe', 'Huong Son', 'Nghi Xuan', 'Thach Ha', 'Vu Quang', 'Loc Ha'
    ],
    'Khanh Hoa': [
        'Nha Trang', 'Cam Ranh', 'Ninh Hoa', 'Van Ninh', 'Khanh Vinh',
        'Dien Khanh', 'Truong Sa', 'Cam Lam'
    ],
    'Kien Giang': [
        'Rach Gia', 'Ha Tien', 'Phu Quoc', 'Kien Luong', 'Chau Thanh',
        'Giong Rieng', 'Go Quao', 'Tan Hiep', 'Vinh Thuan', 'An Bien',
        'An Minh', 'Hon Dat', 'Tay Yen', 'Binh Giang', 'U Minh Thuong'
    ],
    'Kon Tum': [
        'Kon Tum', 'Dak Glei', 'Ngoc Hoi', 'Dak To', 'Sa Thay', 
        'Kon Plong', 'Tu Mo Rong', 'Dak Ha', 'Ia H Drai', 'Dak To'
    ],
    'Lang Son': [
        'Lang Son', 'Chi Lang', 'Huu Lung', 'Van Lang', 'Dinh Lap',
        'Loc Binh', 'Cao Loc', 'Binh Gia', 'Bac Son', 'Vo Nhai'
    ],
    'Lao Cai': [
        'Lao Cai', 'Sa Pa', 'Bac Ha', 'Bat Xat', 'Muong Khuong',
        'Van Ban', 'Dong Van'
    ],
    'Nam Dinh': [
        'Nam Dinh', 'My Loc', 'Xuan Truong', 'Truc Ninh', 'Nam Truc',
        'Nghia Hung', 'Hai Hau', 'Vu Ban', 'Y Yen', 'Dong Hung', 'Giao Thuy'
    ],
    'Nghe An': [
        'Vinh', 'Thai Hoa', 'Cua Lo', 'Nghe An', 'Que Phong', 
        'Tuong Duong', 'Ky Son', 'Con Cuong', 'Dien Chau', 'Yen Thanh',
        'Do Luong', 'Thanh Chuong', 'Nam Dan', 'Hung Nguyen', 'Nghi Loc', 
        'Can Loc', 'Tan Ky', 'Thai Hoa', 'Phu Quy'
    ],
    'Ninh Binh': [
        'Ninh Binh', 'Tam Diep', 'Yen Khanh', 'Hoa Lu', 'Gia Vien', 
        'Nho Quan', 'Kim Son', 'Tam Diep'
    ],
    'Phu Tho': [
        'Viet Tri', 'Phu Tho', 'Doan Hung', 'Ha Hoa', 'Phu Ninh', 
        'Tam Nong', 'Thanh Ba', 'Cam Khe', 'Tan Son', 'Yen Lap'
    ],
    'Quang Binh': [
        'Dong Hoi', 'Ba Don', 'Quang Trach', 'Tuyen Hoa', 'Le Thuy', 
        'Minh Hoa', 'Bo Trach', 'Quang Ninh'
    ],
    'Quang Nam': [
        'Tam Ky', 'Hoi An', 'Dien Ban', 'Duy Xuyen', 'Hiep Duc', 
        'Que Son', 'Phu Ninh', 'Nam Giang', 'Phuoc Son', 'Nong Son', 
        'Dai Loc', 'Thang Binh', 'Hien', 'Tay Giang', 'Dong Giang', 
        'Phuoc Son'
    ],
    'Quang Ngai': [
        'Quang Ngai', 'Ba To', 'Binh Son', 'Hanh Thien', 'Tu Nghia', 
        'Son Tinh', 'Tra Bong', 'Mo Duc', 'Nghia Hanh', 'Dong Nghia', 
        'Ly Son'
    ],
    'Quang Ninh': [
        'Ha Long', 'Cam Pha', 'Uong Bi', 'Mong Cai', 'Dong Trieu', 
        'Hoanh Bo', 'Yen Hung', 'Tien Yen', 'Bai Tu Long', 'Cai Rong', 
        'Ba Che', 'Hai Ha', 'Quang Yen', 'Vang Danh'
    ],
    'Soc Trang': [
        'Soc Trang', 'Ngai Tu', 'Ke Sach', 'My Tu', 'My Xuyen', 
        'Long Phu', 'Tran De', 'Vinh Chau', 'Dai Loc', 'Chau Thanh'
    ],
    'Son La': [
        'Son La', 'Mai Son', 'Thuan Chau', 'Moc Chau', 'Yen Chau', 
        'Van Ho', 'Song Ma', 'Phu Yen', 'Muong La', 'Quynh Nhai', 
        'Thuan Chau', 'Thang Loi', 'Thuan Chau'
    ],
    'Tay Ninh': [
        'Tay Ninh', 'Hoa Thanh', 'Tan Chau', 'Duong Minh Chau', 
        'Ben Cau', 'Chau Thanh', 'Gio Linh', 'Trang Bang'
    ],
    'Thai Binh': [
        'Thai Binh', 'Kien Xuong', 'Thai Thuy', 'Quynh Phu', 'Tien Hai', 
        'Vu Thu', 'Dong Hung', 'Hai Hau', 'Thanh Ly', 'Thai Tan'
    ],
    'Thai Nguyen': [
        'Thai Nguyen', 'Song Cong', 'Dai Tu', 'Phu Binh', 'Vo Nhai', 
        'Dong Hy', 'Phu Luong', 'Phu Luong', 'Tan Cuong', 'Dinh Hoa'
    ],
    'Thanh Hoa': [
        'Thanh Hoa', 'Sam Son', 'Nhu Xuan', 'Thach Thanh', 'Lang Chanh', 
        'Ba Thuoc', 'Cam Thuy', 'Hoang Hoa', 'Hau Loc', 'Vinh Loc', 
        'Quoc Thanh', 'Thieu Hoa', 'Dong Son'
    ],
    'Thua Thien - Hue': [
        'Hue', 'Hue City', 'Phu Vang', 'Huong Tra', 'Huong Thuy', 
        'A Luoi', 'Nam Dong', 'Phong Dien', 'Quang Dien'
    ],
    'Tien Giang': [
        'My Tho', 'Gò Cong', 'Cai Lay', 'Tan Phuoc', 'Cho Gao', 
        'Chau Thanh', 'Thu Thua', 'Tan Phuoc', 'Vinh Kim', 'Dai Loc'
    ],
    'Vinh Long': [
        'Vinh Long', 'Binh Minh', 'Tra On', 'Vung Liem', 'Long Ho', 
        'Mang Thit', 'Tam Binh'
    ],
    'Yen Bai': [
        'Yen Bai', 'Luc Yen', 'Van Chan', 'Mu Cang Chai', 'Tran Yen', 
        'Yen Binh', 'Nga Ba'
    ]
}

day_mapping = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6
}
col1, col2,col3 = st.columns([0.5,1,1.5])

with col1:
    # col13, col14 = st.columns([1,1])
    # with col13:
    province = st.selectbox('Provice:', list(province_districts.keys()))
# with col14:
    # selected_district = 
    if province:
        districts = st.selectbox('District:',province_districts[province])
# col15, col16 = st.columns([1,1])
# with col15:
    STREET = st.text_input("Street")

    WARD = st.text_input("Ward")
with col2:
    geolocator = Nominatim(user_agent="GTA Lookup")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    location = geolocator.geocode(STREET+", "+WARD+", "+districts+", "+province+", "+"Viet Nam")

    lat = location.latitude
    lon = location.longitude

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
    # st.image("VIETNAM.png", use_column_width=True)


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
    col7, col8 = st.columns([1, 1])
    with col7:
        NB_FLOORS =st.number_input(label="Number of floors",step=1.,format="%.0f")
       
    with col8:
        NB_ROOMS = st.number_input(label="Number of rooms",step=1.,format="%.0f")

    # col9, col10= st.columns([1, 1])
    # with col9:
    #    NB_ROOMS = st.slider('Select number of ROOMS', min_value=0, max_value=20, value=5)
    # with col10:
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

        result = predict(
           [[0.969802452722392, 130,	-0.005,	14,	1856.904762,	-0.155,	8,	10,	0,	2]])
        st.text(result) 
        # cb = joblib.load("cb_model.sav")
        # st.write(cb.predict([[0.969802452722392, surface,	used_surface,	width,	1856.904762,	NB_FLOORS,	LENGTH,	selected_day,	NB_ROOMS,	day_of_week]]))
