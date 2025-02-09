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
    'Aston Martin': 2,
    'Audi': 3,
    'BMW': 4,
    'Bajaj': 5,
    'Bentley': 6,
    'Chevrolet': 7,
    'Datsun': 8,
    'Fiat': 9,
    'Force': 10,
    'Ford': 11,
    'Honda': 12,
    'Hyundai': 13,
    'Isuzu': 14,
    'Jaguar': 15,
    'Jeep': 16,
    'Kia': 17,
    'Land Rover': 18,
    'Lexus': 19,
    'MG': 20,
    'Mahindra': 21,
    'Maruti Suzuki': 22,
    'Maserati': 23,
    'Mercedes-Benz': 24,
    'Mini': 25,
    'Mitsubishi': 26,
    'Nissan': 27,
    'Opel': 28,
    'Porsche': 29,
    'Renault': 30,
    'Rolls-Royce': 31,
    'Skoda': 32,
    'Ssangyong': 33,
    'Tata': 34,
    'Toyota': 35,
    'Volkswagen': 36,
    'Volvo': 37
}
# Model Dict
model_dict = {
    'Wagon R': 0,
    '1 Series': 1,
    '1000': 2,
    '2 Series': 3,
    '2.8 Legender 4X2': 4,
    '2.9 Sportback': 5,
    '3 DOOR': 6,
    '3 Series': 7,
    '3 Series GT': 8,
    '3 Series Gran Limousine': 9,
    '5 DOOR': 10,
    '5 Series': 11,
    '5 Series Gt': 12,
    '6 Series': 13,
    '6 Series GT': 14,
    '7 Series': 15,
    '718': 16,
    '800': 17,
    'A Class': 18,
    'A-Class Limousine': 19,
    'A-Star': 20,
    'A-class Limousine': 21,
    'A3': 22,
    'A3 Cabriolet': 23,
    'A4': 24,
    'A5': 25,
    'A6': 26,
    'A8 L': 27,
    'AMG': 28,
    'AMG A35': 29,
    'AMG C 43': 30,
    'AMG GLE Coupe': 31,
    'ASTOR': 32,
    'Accent': 33,
    'Accent Hatchback': 34,
    'Accord': 35,
    'Alcazar': 36,
    'Alto': 37,
    'Alto 800': 38,
    'Alto K10': 39,
    'Alto-800': 40,
    'Alto-K10': 41,
    'Altroz': 42,
    'Alturas G4': 43,
    'Amaze': 44,
    'Ambassador': 45,
    'Ameo': 46,
    'Aspire': 47,
    'Aura': 48,
    'Avventura': 49,
    'B Class': 50,
    'BRV': 51,
    'Baleno': 52,
    'Baleno-RS': 53,
    'Beat': 54,
    'Beetle': 55,
    'Bolero': 56,
    'Bolero Neo': 57,
    'Bolero Neo Plus': 58,
    'Bolero Power Plus': 59,
    'Bolt': 60,
    'Boxster': 61,
    'Brezza': 62,
    'Brio': 63,
    'C Class': 64,
    'C-Class': 65,
    'CERATO': 66,
    'CLA': 67,
    'CLS-Class': 68,
    'CR-V': 69,
    'CRV': 70,
    'Camry': 71,
    'Captiva': 72,
    'Captur': 73,
    'Carens': 74,
    'Carnival': 75,
    'Cayenne': 76,
    'Cayenne Coupe': 77,
    'Cayman': 78,
    'Cedia': 79,
    'Celerio': 80,
    'Celerio X': 81,
    'Celerio-X': 82,
    'Ciaz': 83,
    'City': 84,
    'City Hybrid eHEV': 85,
    'City ZX': 86,
    'Civic': 87,
    'Compass': 88,
    'Cooper': 89,
    'Cooper 3 DOOR': 90,
    'Cooper 5 DOOR': 91,
    'Cooper Clubman': 92,
    'Cooper Convertible': 93,
    'Cooper Countryman': 94,
    'Cooper S': 95,
    'Corolla': 96,
    'Corolla Altis': 97,
    'Corsa': 98,
    'Countryman': 99,
    'Creta': 100,
    'Creta Facelift': 101,
    'CrossPolo': 102,
    'Cruze': 103,
    'Curvv': 104,
    'D-Max V-Cross': 105,
    'Defender': 106,
    'Discovery': 107,
    'Discovery Sport': 108,
    'Duster': 109,
    'Dzire': 110,
    'E-20': 111,
    'E-Class': 112,
    'EON': 113,
    'ES': 114,
    'Ecosport': 115,
    'Eeco': 116,
    'Elantra': 117,
    'Elevate': 118,
    'Elite i20': 119,
    'Endeavour': 120,
    'Enjoy': 121,
    'Eon': 122,
    'Ertiga': 123,
    'Esteem': 124,
    'Estilo': 125,
    'Estima': 126,
    'Etios': 127,
    'Etios Cross': 128,
    'Etios Liva': 129,
    'Exter': 130,
    'F-Pace': 131,
    'Fabia': 132,
    'Fiesta': 133,
    'Fiesta Classic': 134,
    'Figo': 135,
    'Figo Aspire': 136,
    'Fluence': 137,
    'Fluidic Verna': 138,
    'Flying Spur': 139,
    'Fortuner': 140,
    'Free Style': 141,
    'Freelander 2': 142,
    'Fronx': 143,
    'Fronx ': 144,
    'G': 145,
    'G Class': 146,
    'G-Class': 147,
    'GL-Class': 148,
    'GLA': 149,
    'GLA Class': 150,
    'GLC': 151,
    'GLC Class': 152,
    'GLC Coupe': 153,
    'GLE': 154,
    'GLE COUPE': 155,
    'GLE Class': 156,
    'GLS': 157,
    'GO': 158,
    'GO Plus': 159,
    'GTI': 160,
    'Getz': 161,
    'Getz Prime': 162,
    'Glanza': 163,
    'Gloster': 164,
    'Gran Turismo': 165,
    'Grand Punto': 166,
    'Grand Vitara': 167,
    'Grand i10': 168,
    'Grand i10 Nios': 169,
    'Grand i10 Prime': 170,
    'Gypsy': 171,
    'H5x': 172,
    'Harrier': 173,
    'Hector': 174,
    'Hector Plus': 175,
    'Hexa': 176,
    'Isuzu Hi-Lander': 177,
    'Ignis': 178,
    'Ikon': 179,
    'Indica': 180,
    'Indica Ev2': 181,
    'Indica V2': 182,
    'Indica Vista': 183,
    'Indigo Cs': 184,
    'Indigo Ecs': 185,
    'Indigo Marina': 186,
    'Innova': 187,
    'Innova Crysta': 188,
    'Innova Hycross': 189,
    'Invicto': 190,
    'Jazz': 191,
    'Jeep': 192,
    'Jetta': 193,
    'Jimny': 194,
    'KUV 100': 195,
    'KUV100 NXT': 196,
    'KWID': 197,
    'Kicks': 198,
    'Kiger': 199,
    'Kodiaq': 200,
    'Kushaq': 201,
    'LS': 202,
    'LX': 203,
    'Lancer': 204,
    'Land Cruiser': 205,
    'Land Cruiser Prado': 206,
    'Laura': 207,
    'Leyland Stile': 208,
    'Linea': 209,
    'Lodgy': 210,
    'M-Class': 211,
    'M340i': 212,
    'MAX': 213,
    'MICRA PRIMO': 214,
    'MUX': 215,
    'Macan': 216,
    'Magnite': 217,
    'Manza': 218,
    'Marazzo': 219,
    'Marshal': 220,
    'Meridian': 221,
    'Micra': 222,
    'Micra Active': 223,
    'Mobilio': 224,
    'Motors FM Force One Test': 225,
    'Motors FM Gurkha': 226,
    'Motors FM Trax Cruiser': 227,
    'Mustang': 228,
    'NX': 229,
    'Nano': 230,
    'Nano Genx': 231,
    'New Accord': 232,
    'New Duster': 233,
    'New Elantra': 234,
    'New Santro': 235,
    'New i20': 236,
    'New-gen Swift': 237,
    'Nexon': 238,
    'Nuvosport': 239,
    'Octavia': 240,
    'Omni': 241,
    'Optra': 242,
    'Optra Magnum': 243,
    'OptraSRV': 244,
    'Others': 245,
    'Outlander': 246,
    'PATROL': 247,
    'Pajero Sport': 248,
    'Panamera': 249,
    'Passat': 250,
    'Phantom Drop HeadCoupe': 251,
    'Phantom Series II': 252,
    'Polo': 253,
    'Polo GTI': 254,
    'Pulse': 255,
    'Punch': 256,
    'Punch ': 257,
    'Punto': 258,
    'Punto EVO': 259,
    'Punto Pure': 260,
    'Q3': 261,
    'Q5': 262,
    'Q7': 263,
    'Quanto': 264,
    'RE60': 265,
    'RX': 266,
    'Range Rover': 267,
    'Range Rover Evoque': 268,
    'Range Rover Sport': 269,
    'Range Rover Velar': 270,
    'Rapid': 271,
    'Redi Go': 272,
    'RediGO': 273,
    'Renault Logan': 274,
    'Rexton': 275,
    'Ritz': 276,
    'S 80': 277,
    'S-Class': 278,
    'S-Cross': 279,
    'S-Cross1': 280,
    'S-Presso': 281,
    'S60': 282,
    'S60 Cross Country': 283,
    'S80': 284,
    'S90': 285,
    'SL-Class': 286,
    'SLK-Class': 287,
    'SX4': 288,
    'Safari': 289,
    'Safari Storme': 290,
    'Sail': 291,
    'Sail U-VA': 292,
    'Santa Fe': 293,
    'Santro': 294,
    'Santro Xing': 295,
    'Scala': 296,
    'Scorpio': 297,
    'Scorpio Classic': 298,
    'Scorpio N': 299,
    'Scorpio-N': 300,
    'Seltos': 301,
    'Slavia': 302,
    'Sonata': 303,
    'Sonata Embera': 304,
    'Sonet': 305,
    'Spark': 306,
    'Ssangyong Rexton': 307,
    'Ssangyong-Rexton': 308,
    'Stingray': 309,
    'Sumo': 310,
    'Sumo Gold': 311,
    'Sumo Grande MK II': 312,
    'Sumo Victa': 313,
    'Sunny': 314,
    'Superb': 315,
    'Swift': 316,
    'Swift Dzire': 317,
    'Swift-Dzire': 318,
    'Swift-Dzire-Tour': 319,
    'Sx4': 320,
    'TUV': 321,
    'TUV 300': 322,
    'TUV 300-plus': 323,
    'Taigun': 324,
    'Tavera': 325,
    'Teana': 326,
    'Terrano': 327,
    'Thar': 328,
    'Tiago': 329,
    'Tigor': 330,
    'Tiguan': 331,
    'Tiguan All Space': 332,
    'Trailblazer': 333,
    'Triber': 334,
    'Tucson': 335,
    'Urban Cross': 336,
    'Urban Cruiser': 337,
    'Urban Cruiser Hyryder': 338,
    'Urvan': 339,
    'V-Class': 340,
    'V40 Cross Country': 341,
    'VELLFIRE': 342,
    'Vantage': 343,
    'Vento': 344,
    'VentoTest': 345,
    'Venture': 346,
    'Venue': 347,
    'Venue N Line': 348,
    'Verito': 349,
    'Verna': 350,
    'Virtus': 351,
    'Vista Tech': 352,
    'Vitara-Brezza': 354,
    'WR-V': 355,
    'WRV': 356,
    'Wagon R': 357,
    'Wagon R 1.0': 358,
    'Wagon-R': 359,
    'Wagon-R-1-0': 360,
    'Wagon-R-Stingray': 361,
    'Wrangler': 362,
    'X1': 363,
    'X3': 364,
    'X4': 365,
    'X5': 366,
    'X5 M': 367,
    'X6': 368,
    'X7': 369,
    'XC 90': 370,
    'XC40': 371,
    'XC60': 372,
    'XC90': 373,
    'XE': 374,
    'XF': 375,
    'XJ': 376,
    'XL6': 377,
    'XUV300': 379,
    'XUV500': 380,
    'XUV700': 381,
    'Xcent': 382,
    'Xcent Prime': 383,
    'Xenon XT': 384,
    'Xylo': 385,
    'Yaris': 386,
    'Z4': 387,
    'Zen-Estilo': 389,
    'Zest': 390,
    'i10': 391,
    'i20': 392,
    'i20 Active': 393,
    'i20 N Line': 394,
    'Brezza': 395,
    'Dzire': 396,
    'Punch': 397
}
# Transmission Dict
transmission_dict = {
    'Automatic': 0,
    'Manual': 1
}
# Owner Dictionary
owner_dict = {
    'first': 0,
    'second': 1
}
# Fuel Type Dictionary
fuel_type_dictionary = {
    'Diesel': 0,
    'Hybrid/CNG': 1,
    'Petrol': 2
}

# Title
st.set_page_config(page_title='Used Car price Prediction')

# Creating cars brands and models df by the cleaned dataset we saved
df = pd.read_csv('../Dataset/Used_Car_Final.csv')

# Creating a function for filtering the model name correspond to it brand
# Return the models of the selected Brand only
def find_model(brand):
    model = car[car['Brand'] == brand]['Model']
    return list(model)

# Loading Model
@st.cache_resource
def model_loader(path):
    model = joblib.load(path)
    return model

# Show a spinner while the model is loading
with st.spinner('Hold on, the app is loading!'):
    model_pred = model_loader("../Code/Used_Car_Price_Prediction.pkl")

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