import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import base64

# Input dict for categorical label
# Brand dict
brand_dict = {
    'Ambassador': 0,
    'Ashok': 1,
    'Audi': 2,
    'BMW': 3,
    'Bajaj': 4,
    'Chevrolet': 5,
    'Datsun': 6,
    'Fiat': 7,
    'Force Motors': 8,
    'Ford': 9,
    'Honda': 10,
    'Hyundai': 11,
    'Isuzu': 12,
    'Jaguar': 13,
    'Jeep': 14,
    'Kia': 15,
    'Land': 16,
    'Land Rover': 17,
    'Lexus': 18,
    'MG': 19,
    'Mahindra': 20,
    'Maruti Suzuki': 21,
    'Mercedes-Benz': 22,
    'Mini': 23,
    'Mitsubishi': 24,
    'Nissan': 25,
    'Opel': 26,
    'Porsche': 27,
    'Renault': 28,
    'Rolls-Royce': 29,
    'Skoda': 30,
    'Smart': 31,
    'Ssangyong': 32,
    'Tata': 33,
    'Toyota': 34,
    'Volkswagen': 35,
    'Volvo': 36
}
# Model Dict
model_dict = {
    '1 Series': 0,
    '1000': 1,
    '3 Series': 2,
    '5 Series': 3,
    '7 Series': 4,
    '800': 5,
    'A-Class': 6,
    'A-Star': 7,
    'A3': 8,
    'A4': 9,
    'A5': 10,
    'A6': 11,
    'A8': 12,
    'Accent': 13,
    'Accord': 14,
    'Alcazar': 15,
    'Alto': 16,
    'Altroz': 17,
    'Alturas G4': 18,
    'Amaze': 19,
    'Ambassador': 20,
    'Ameo': 21,
    'Aspire': 22,
    'Astor': 23,
    'Aura': 24,
    'Aveo': 25,
    'Avventura': 26,
    'B-Class': 27,
    'BRV': 28,
    'Baleno': 29,
    'Beat': 30,
    'Beetle': 31,
    'Bolero': 32,
    'Bolt': 33,
    'Brio': 34,
    'C-Class': 35,
    'CLA': 36,
    'CLS': 37,
    'CRV': 38,
    'Camry': 39,
    'Captiva': 40,
    'Captur': 41,
    'Carens': 42,
    'Cayenne': 43,
    'Cedia': 44,
    'Celerio': 45,
    'Cerato': 46,
    'Ciaz': 47,
    'City': 48,
    'Civic': 49,
    'Classic': 50,
    'Compass': 51,
    'Cooper': 52,
    'Cooper 3': 53,
    'Cooper 5': 54,
    'Cooper Convertible': 55,
    'Cooper Countryman': 56,
    'Cooper S': 57,
    'Corolla': 58,
    'Corsa': 59,
    'Creta': 60,
    'Cruze': 61,
    'D-Max': 62,
    'Discovery': 63,
    'Duster': 64,
    'E-20': 65,
    'E-Class': 66,
    'Ecosport': 67,
    'Eeco': 68,
    'Elantra': 69,
    'Elevate': 70,
    'Endeavour': 71,
    'Enjoy': 72,
    'Eon': 73,
    'Ertiga': 74,
    'Esteem': 75,
    'Etios': 76,
    'Etios Cross': 77,
    'Etios Liva': 78,
    'Exter': 79,
    'Fabia': 80,
    'Fiesta': 81,
    'Figo': 82,
    'Fluence': 83,
    'Force One': 84,
    'Fortuner': 85,
    'Fortwo': 86,
    'Freelander 2': 87,
    'Freestyle': 88,
    'Fronx': 89,
    'Fronx ': 90,
    'Fusion': 91,
    'GL-Class': 92,
    'GLA': 93,
    'GLE': 94,
    'GLS': 95,
    'GO': 96,
    'GO Plus': 97,
    'Getz': 98,
    'Glanza': 99,
    'Grand Vitara': 100,
    'Gurkha': 101,
    'Gypsy': 102,
    'Harrier': 103,
    'Hector': 104,
    'Hexa': 105,
    'Hi-Lander': 106,
    'Ignis': 107,
    'Ikon': 108,
    'Indica': 109,
    'Indigo': 110,
    'Innova': 111,
    'Jazz': 112,
    'Jeep': 113,
    'Jetta': 114,
    'Jimny': 115,
    'KUV100': 116,
    'Kicks': 117,
    'Kiger': 118,
    'Kodiaq': 119,
    'Koleos': 120,
    'Kushaq': 121,
    'Kwid': 122,
    'LS': 123,
    'LX': 124,
    'Lancer': 125,
    'Laura': 126,
    'Leyland Stile': 127,
    'Linea': 128,
    'Lodgy': 129,
    'Logan': 130,
    'M-Class': 131,
    'MUX': 132,
    'Magnite': 133,
    'Manza': 134,
    'Marazzo': 135,
    'Marshal': 136,
    'Meridian': 137,
    'Micra': 138,
    'Mobilio': 139,
    'NX': 140,
    'Nano': 141,
    'Nexon': 142,
    'Nuvosport': 143,
    'Octavia': 144,
    'Omni': 145,
    'Optra': 146,
    'Outlander': 147,
    'Pajero': 148,
    'Pajero Sport': 149,
    'Passat': 150,
    'Patrol': 151,
    'Petra': 152,
    'Phantom': 153,
    'Polo': 154,
    'Pulse': 155,
    'Punch': 156,
    'Punch ': 157,
    'Punto': 158,
    'Q3': 159,
    'Q5': 160,
    'Q7': 161,
    'Qualis': 162,
    'Quanto': 163,
    'R-Class': 164,
    'RE60': 165,
    'RX': 166,
    'Range Rover': 167,
    'Range Rover Evoque': 168,
    'Rapid': 169,
    'Redi GO': 170,
    'Rexton': 171,
    'Ritz': 172,
    'S-Class': 173,
    'S-Cross': 174,
    'S-Presso': 175,
    'S60': 176,
    'S80': 177,
    'SX4': 178,
    'Safari': 179,
    'Sail': 180,
    'Sail U-VA': 181,
    'Santa Fe': 182,
    'Santro': 183,
    'Scala': 184,
    'Scorpio': 185,
    'Seltos': 186,
    'Siena': 187,
    'Slavia': 188,
    'Sonata': 189,
    'Sonet': 190,
    'Spark': 191,
    'Sumo': 192,
    'Sunny': 193,
    'Superb': 194,
    'Swift': 195,
    'Swift Dzire': 196,
    'TUV300': 197,
    'Taigun': 198,
    'Tavera': 199,
    'Teana': 200,
    'Terrano': 201,
    'Thar': 202,
    'Tiago': 203,
    'Tigor': 204,
    'Tiguan': 205,
    'Trailblazer': 206,
    'Trax Cruiser': 207,
    'Triber': 208,
    'Tucson': 209,
    'Urban Cross': 210,
    'Urban Cruiser Hyryder': 211,
    'V40': 212,
    'Vento': 213,
    'Venture': 214,
    'Venue': 215,
    'Verito': 216,
    'Verna': 217,
    'Virtus': 218,
    'Vitara-Brezza': 219,
    'WRV': 220,
    'WagonR': 221,
    'X-Trail': 222,
    'X1': 223,
    'X3': 224,
    'X4': 225,
    'X5': 226,
    'XC60': 227,
    'XC90': 228,
    'XE': 229,
    'XF': 230,
    'XJ': 231,
    'XL6': 232,
    'XUV300': 233,
    'XUV500': 234,
    'XUV700': 235,
    'Xcent': 236,
    'Xenon': 237,
    'Xylo': 238,
    'Yaris': 239,
    'Yeti': 240,
    'Z4': 241,
    'Zen': 242,
    'Zen-Estilo': 243,
    'Zest': 244,
    'i10': 245,
    'i20': 246
}
# Transmission Dict
transmission_dict = {
    'Automatic': 0,
    'Manual': 1
}
# Owner Dictionary
owner_dict = {
    'first': 0,
    'fourth & above': 1,
    'second': 2,
    'third': 3
}
# Fuel Type Dictionary
fuel_type_dictionary = {
    'Diesel': 0,
    'Electric': 1,
    'Hybrid/CNG': 2,
    'LPG': 3,
    'Petrol': 4
}

# Title
st.set_page_config(page_title='Used Car price Prediction')

# Creating df by the cleaned dataset we saved
df = pd.read_csv('../Dataset/Used_Car_Final.csv')

# Loading Model
@st.cache_resource
def model_loader(path):
    model = joblib.load(path)
    return model

# Show a spinner while the model is loading
with st.spinner('Hold on, the app is loading!'):
    model_pred = model_loader("../Dataset/Used_Car_Price_Prediction.pkl")

# Header
st.markdown("<h1 style='text-align: center;'>Used Car Price Prediction</h1>", unsafe_allow_html=True)


# Inputs from user -> Brand | Model | Age | KmDriven | Transmission | Owner | FuelType

# Brand
# Get unique brands
brands = df['Brand'].unique()

# Dropdown for brand selection
selected_brand = st.selectbox("Select a Brand", brands)


# Model
# Filter models based on selected brand
filtered_models = df[df['Brand'] == selected_brand]['Model'].unique()

# Dropdown for model selection
selected_model = st.selectbox("Select a Model", filtered_models)


# Age
# Create two columns for year and month selection
col1, col2 = st.columns(2)

# Slider for selecting the year of manufacture in the first column
with col1:
    year = st.slider('Select the year when the car was manufactured', 1980, 2024, 2014, help='The year the car was manufactured')

# Dropdown for selecting the month of manufacture in the second column
with col2:
    month = st.selectbox('Select the month when the car was manufactured', 
                    ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                    help='The month the car was manufactured')

# Get the current month and year
current_month = datetime.today().month
current_year = datetime.today().year

# Convert month name to month number
month_number = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'].\
                index(month) + 1

# Calculate the age of the car in months
selected_age = (current_year - year) * 12 + (current_month - month_number)

# Display the car age in months
st.write(f"The age of the car is: **{selected_age} months**")


# KmDriven
selected_KmDriven = st.number_input(
    label='Enter how many kilometers the car has driven',
    help='Enter in km',
    min_value=0,  # Minimum value for kilometers
    step=100      # Step size of 500 km
)


# Transmission
transmission = df['Transmission'].unique()

# Dropdown for brand selection
selected_transmission = st.selectbox("Select a transmission", transmission)


# Owner
owner = df['Owner'].unique()

# Dropdown for brand selection
selected_owner = st.selectbox("Select a owner type", owner)


# FuelType
fuel_type = df['FuelType'].unique()

# Dropdown for brand selection
selected_fuel_type = st.selectbox("Select a fuel type", fuel_type)


# Convert selected values to numerical values
selected_brand_value = brand_dict[selected_brand]
selected_model_value = model_dict[selected_model]
selected_transmission_value = transmission_dict[selected_transmission]
selected_owner_value = owner_dict[selected_owner]
selected_fuel_type_value = fuel_type_dictionary[selected_fuel_type]

# Creating an input array for prediction using numerical values
inp_array = np.array([[selected_brand_value, selected_model_value, selected_age, selected_KmDriven, selected_transmission_value, selected_owner_value, selected_fuel_type_value]])

predict = st.button('Predict') # creating a predict button

if predict: 
        pred = model_pred.predict(inp_array)
        if pred < 0: # handeling negative outputs
            st.error('The input values must be irrelevant, try again by giving relevent information.')
        pred = round(float(np.exp(pred)))
        formatted_pred = f"{pred:,}"
        write = 'The predicted price of the car is ₹'+ str(formatted_pred) # showing the price prediction

        col3, col4 = st.columns(2)
        with col3:
            st.success(write)


        # Showing gif
        with col4:
            file_ = open("../Code/cars-success.gif", "rb")
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")
            file_.close()

            st.markdown(
                f'<img src="data:image/gif;base64,{data_url}" alt="There was supposed to be Lightning McQueen waving you Hi :(" width="auto" height="auto">',
                unsafe_allow_html=True,
            )


# writing some information about the projects.
st.header('Info About the Project')
project_info = """
            Here you can predict the price of your used car giving some information (Don't worry, we don't save data, or do we? 😈)
            Click on predict button, and see what happens\n
"""
st.write(project_info)
st.header("""Until then 🫡""")