import folium
from streamlit_folium import st_folium
import pandas as pd
import requests 
import streamlit as st
from streamlit_lottie import st_lottie
import random


# Load the CSV file
df = pd.read_csv('./Carpool2School_Full_Updated_Dummy_Data_Corrected.csv')
carpool_df = df[df['carpool'] == 'N'].head(10)
# Set page configuration
st.set_page_config(page_title="User Dashboard", page_icon="📊", layout="wide")

# Hide the Streamlit default menu and footer
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Lottie animation
lottie_welcome = load_lottieurl("https://lottie.host/2aa73612-1291-4340-9f33-d15379e1b5ea/b7lKQ8huU9.json")



# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login(username, password):
    if username in df['username'].values and password in df[df['username'] == username]['password'].values:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.school_name = df[df['username' == username]]['school_name']
    else:
        st.error("❌ Invalid username or password")


# Define the about page content
def about_page():
    # Main header
    st.title("About Us 🌟")

    # Mission
    st.header("Our Mission 🌍")
    st.write("""
    At **CoRide**, our mission is to provide a streamlined and efficient solution for organizing carpooling, 
    thereby reducing the carbon footprint of daily commutes in schools, institutions, and organizations. 
    We aim to foster a community of eco-friendly commuters who contribute to a sustainable future.
    """)

    # Problem
    st.header("The Problem 🚗🌎")
    st.write("""
    Transportation is a significant contributor to global carbon emissions, exacerbating climate change. 
    In many institutions, a large percentage of individuals travel by private cars without carpooling. 
    This not only increases fuel consumption and traffic congestion but also has a considerable environmental impact. 
    A survey of 746 students showed that 62.3% of those who travel by car do not carpool, 
    mainly because they are unaware of others living nearby with similar schedules.
    """)

    # Solution
    st.header("Our Solution 💡")
    st.write("""
    **CoRide** is a web application designed to facilitate carpooling by connecting members of institutions who travel similar routes. 
    By minimizing the number of vehicles on the road, **CoRide** helps lower carbon emissions and promotes eco-friendly commuting habits.
    """)

    # Functionality
    st.header("Functionality 🔧")
    st.write("""
    **CoRide** collects user data, including addresses and commuting preferences, to match individuals for optimal carpooling. 
    The app uses the Google Maps API to map user addresses and calculate distances between homes and destinations. 
    An algorithm, based on the vehicle routing problem, finds the best carpool pairs, optimizing routes to reduce carbon emissions. 
    The front end is built using Streamlit, and data management is handled via CSV files.
    """)

    # Vision
    st.header("Our Vision 🌱")
    st.write("""
    Our vision is to expand the user base of **CoRide** by adding features such as real-time GPS tracking for enhanced safety and convenience, 
    dynamic carpooling based on car availability, and support for a broader range of users including office workers and airport travelers. 
    We aspire to create a more sustainable and eco-friendly transportation ecosystem across various sectors.
    """)

    # Team
    st.header("Our Team 👥")
    st.write("We are a group of passionate students from Vasant Valley School, dedicated to making a difference.")

    st.subheader("Kabir Bahl 📚")
    st.write("Co-founder: Student in class 12 at Vasant Valley School.")

    st.subheader("Savya Meattle 📚")
    st.write("Co-founder: Student in class 12 at Vasant Valley School.")

    st.subheader("Vedant Saini 📚")
    st.write("Co-founder: Student in class 12 at Vasant Valley School.")

    st.subheader("Vivaan Garg 📚")
    st.write("Co-founder: Student in class 12 at Vasant Valley School.")

# Define the profile page content
def profile_page():
    # Load the existing data
    csv_path = "Carpool2School_Full_Updated_Dummy_Data_Corrected.csv"
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=[
            "name", "student email", "username", "password", "school name", "class",
            "parent 1 name", "parent 1 phone", "parent 1 email",
            "parent 2 name", "parent 2 phone", "parent 2 email",
            "address", "pin code", "mode of transport", "carpool", "car details", "fuel type"
        ])

    # Function to preload data
    def preload_data(username):
        if username in df['username'].values:
            user_data = df[df['username'] == username].iloc[0]
            return user_data
        else:
            return None

    # Preload data if username exists
    username_input = st.session_state.username
    user_data = preload_data(username_input)

    # Page title and subtitle
    st.title("🚗 CoRide Profile 🌍")
    st.subheader("Update Your Profile")
    st.write("Please fill out the form below to keep your information up-to-date!")

    # Create a form for collecting student information
    with st.form(key='student_profile_form'):
        st.markdown("<h3 style='text-align: center;'>📋 Student Profile Form</h3>", unsafe_allow_html=True)

        name = st.text_input("👤 Full Name", user_data['name'] if user_data is not None else "")
        student_email = st.text_input("📧 Student Email", user_data['student_email'] if user_data is not None else "")
        school_name = st.selectbox("🏫 School Name", [
            "Delhi Public School", "Springdales School", "The Mother's International School", 
            "Vasant Valley School", "Sanskriti School"
        ], index=list(df['school_name']).index(user_data['school_name']) if user_data is not None else 0)
        student_class = st.selectbox("🎓 Class", [str(i) for i in range(1, 13)], index=int(user_data['class'])-1 if user_data is not None else 0)
        parent1_name = st.text_input("👨‍👩‍👦 Parent 1 Name", user_data['parent_1_name'] if user_data is not None else "")
        parent1_phone = st.text_input("📞 Parent 1 Phone", user_data['parent_1_phone'] if user_data is not None else "")
        parent1_email = st.text_input("✉️ Parent 1 Email", user_data['parent_1_email'] if user_data is not None else "")
        parent2_name = st.text_input("👨‍👩‍👦 Parent 2 Name", user_data['parent_2_name'] if user_data is not None else "")
        parent2_phone = st.text_input("📞 Parent 2 Phone", user_data['parent_2_phone'] if user_data is not None else "")
        parent2_email = st.text_input("✉️ Parent 2 Email", user_data['parent_2_email'] if user_data is not None else "")
        address = st.text_input("🏠 Address", user_data['address'] if user_data is not None else "")
        pin_code = st.text_input("📮 Pin Code", user_data['pin_code'] if user_data is not None else "")
        mode_of_transport = st.selectbox("🚘 Mode of Transport", ["Car", "Bus"], index=["Car", "Bus"].index(user_data['mode_of_transport']) if user_data is not None else 0)

        car_companies = ["Maruti", "Hyundai", "Honda", "Toyota", "Ford", "Tata", "Mahindra", "Volkswagen"]
        car_models = {
            "Maruti": ["Alto", "Swift", "Baleno"],
            "Hyundai": ["i20", "Verna", "Creta"],
            "Honda": ["City", "Civic", "Jazz"],
            "Toyota": ["Innova", "Corolla", "Fortuner"],
            "Ford": ["EcoSport", "Endeavour", "Figo"],
            "Tata": ["Nexon", "Harrier", "Tiago"],
            "Mahindra": ["Scorpio", "XUV500", "Bolero"],
            "Volkswagen": ["Polo", "Vento", "Passat"]
        }

        if mode_of_transport == "Car":
            carpool = st.radio("Carpool", ["Y", "N"], index=["Y", "N"].index(user_data['carpool']) if user_data is not None else 1)
            car_company = st.selectbox("Car Company", car_companies, index=car_companies.index(user_data['car_details'].split()[0]) if user_data is not None and user_data['car_details'] else 0)
            car_model = st.selectbox("Car Model", car_models[car_company], index=car_models[car_company].index(user_data['car_details'].split()[1]) if user_data is not None and user_data['car_details'] else 0)
            fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel"], index=["Petrol", "Diesel"].index(user_data['fuel_type']) if user_data is not None else 0)
        else:
            carpool = ""
            car_company = ""
            car_model = ""
            fuel_type = "Diesel"

        # Save button
        save_button = st.form_submit_button(label="Save 💾")

    # Save data to CSV if form is submitted
    if save_button:
        new_data = {
            "name": name,
            "student email": student_email,
            "username": username_input,
            "password": user_data['password'] if user_data is not None else f"Pass{random.randint(1000, 9999)}",
            "school name": school_name,
            "class": student_class,
            "parent 1 name": parent1_name,
            "parent 1 phone": parent1_phone,
            "parent 1 email": parent1_email,
            "parent 2 name": parent2_name,
            "parent 2 phone": parent2_phone,
            "parent 2 email": parent2_email,
            "address": address,
            "pin code": pin_code,
            "mode of transport": mode_of_transport,
            "carpool": carpool,
            "car details": f"{car_company} {car_model}" if car_model else "",
            "fuel type": fuel_type
        }

        if user_data is not None:
            df.update(pd.DataFrame([new_data]))
        else:
            df = df.append(new_data, ignore_index=True)

        print(df['school_name'])
        df.to_csv(csv_path, index=False)
        st.success("Your information has been saved successfully! 🎉")

    # Footer
    st.markdown("<footer style='text-align: center; color: #9E9E9E;'>© 2024 CoRide. All rights reserved.</footer>", unsafe_allow_html=True)

    
def settings_page():
    st.title("Settings ⚙️")
    st.write("Here you can adjust your settings to personalize your experience.")

# Define the logout functionality
def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()
# Emission factors and fuel consumption mapping
fuelConsumptionMapping = {
    'Bus': 0.35,  # Average value for diesel buses
    'Hyundai i20': 0.06,
    'Mahindra Scorpio': 0.11,
    'Volkswagen Polo': 0.055,
    'Maruti Alto': 0.045,
    'Ford EcoSport': 0.075,
    'Toyota Innova': 0.12,
    'Honda City': 0.06,
    'Tata Nexon': 0.07,
    'Car': 0.09  # Default value for unspecified cars
}

emissionFactors = {
    'Diesel': 2.68,
    'Petrol': 2.31
}

def calculateCarbonEmissions(transportType, fuelType, distance):
    fuelConsumption = fuelConsumptionMapping.get(transportType, fuelConsumptionMapping['Car'])
    emissionFactor = emissionFactors.get(fuelType, emissionFactors['Petrol'])
    totalFuelUsed = fuelConsumption * distance
    carbonEmissions = totalFuelUsed * emissionFactor
    return carbonEmissions

def home_page():
    # Load the existing data
    csv_path = "carpool2school_full_updated_dummy_data_corrected.csv"
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        st.error("CSV file not found. Please make sure the file is in the correct location.")
        df = pd.DataFrame(columns=[
            "name", "student email", "username", "password", "school name", "class",
            "parent 1 name", "parent 1 phone", "parent 1 email",
            "parent 2 name", "parent 2 phone", "parent 2 email",
            "address", "pin code", "mode of transport", "carpool", "car details", "fuel type"
        ])

    # Get the username from session state
    username = st.session_state.username

    # Function to preload data
    def preload_data(username):
        if username in df['username'].values:
            user_data = df[df['username'] == username].iloc[0]
            return user_data
        else:
            return None

    # Preload data if username exists
    user_data = preload_data(username)


        # Page title and subtitle
    st.markdown("<h1 style='text-align: center;'>CoRide Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Your Eco-Friendly Commute Partner</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Join us in reducing carbon emissions and making our planet greener, one carpool at a time!</p>", unsafe_allow_html=True)

    st.markdown("---")

    # Emissions Overview
    st.markdown("## Emissions Overview")
    with st.container():
        col1,col2 = st.columns(2)
        with col1:
            st.markdown("#### 👤 Your Own Emissions")
            own_emissions = f"{random.randint(9,14)}.{random.randint(1,9)}kg CO₂e"  # Replace with actual calculation if available
            st.metric(label="Your Emissions", value=own_emissions, help="Your personal emissions")
        with col2:
            st.markdown("#### 🌱 Potential Emissions Saved")
            saved_emissions = f"{random.randint(1,2)}.{random.randint(1,9)}kg CO₂e"  # Replace with actual calculation if available
            st.metric(label="Saved Emissions", value=saved_emissions, help="Potential emissions saved")

    st.markdown("---")

 # Your Google Maps API key
    API_KEY = 'AIzaSyC1P58VbgiSoiOj5e00ERPHyvQcSQSwYjw'

    def get_geolocation(address):
        url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}'
        response = requests.get(url)
        data = response.json()
        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            raise Exception('Error fetching geolocation data')

    def get_full_name(username, csv_path="carpool2school_full_updated_dummy_data_corrected.csv"):
        # Load the existing data
        try:
            df = pd.read_csv(csv_path)
        except FileNotFoundError:
            print("CSV file not found. Please make sure the file is in the correct location.")
            return None

        # Search for the username
        user_row = df[df['username'] == username]
        if not user_row.empty:
            full_name = user_row.iloc[0]['name']
            return full_name
        else:
            return "Username not found. Please check the username and try again."

    # Example usage
    username_to_search = "sai733"

    def get_distance_matrix(origins, destinations): 
        url = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={origins}&destinations={destinations}&key={API_KEY}'
        response = requests.get(url)
        data = response.json()
        if data['status'] == 'OK':
            return data['rows'][0]['elements'][0]['distance']['value'], data['rows'][0]['elements'][0]['duration']['text']
        else:
            raise Exception(f'Error fetching distance data: {data["status"]}')

    def create_map(user_location, carpool_data, destination_location):
        map = folium.Map(location=user_location, zoom_start=12,tiles='OpenStreetMap')
        # Add markers for carpool locations
        for _, row in carpool_data.iterrows():
            address = row['address']
            name = row['name']
            contact = row['parent_1_phone']
            location = get_geolocation(address)
                    
            # Get distances
            user_to_person_distance, user_to_person_duration = get_distance_matrix(f"{user_location[0]},{user_location[1]}", f"{location[0]},{location[1]}")
            person_to_school_distance, person_to_school_duration = get_distance_matrix(f"{location[0]},{location[1]}", f"{destination_location[0]},{destination_location[1]}")
            
            popup_text = (
                f"{name}<br>Contact: {contact}<br>Address: {address}<br><br>"
                f"Distance to you: {user_to_person_distance/1000:.2f} km<br>"
            )
            
            folium.Marker(location, popup=popup_text, icon=folium.Icon(color='blue')).add_to(map)
        
        # Add a marker for the final destination
        folium.Marker(destination_location, popup='Vasant Valley School', icon=folium.Icon(color='red')).add_to(map)
        folium.Marker(user_location, popup='Your Location', icon=folium.Icon(color='green')).add_to(map)
        
        return map

    # Conversion factors
    co2ToIceArea = 3  # square meters of ice per metric ton of CO2
    iceDensity = 917  # kg/m³

    def get_best_pairings(carpool_data, user_location, destination_location):
        pairings = []
        user_to_school_distance, _ = get_distance_matrix(f"{user_location[0]},{user_location[1]}", f"{destination_location[0]},{destination_location[1]}")

        for _, user_row in carpool_data.iterrows():
            for _, partner_row in carpool_data.iterrows():
                if user_row['name'] != partner_row['name']:
                    partner_location = get_geolocation(partner_row['address'])

                    # Calculate distances
                    user_to_partner_distance, _ = get_distance_matrix(f"{user_location[0]},{user_location[1]}", f"{partner_location[0]},{partner_location[1]}")
                    partner_to_school_distance, _ = get_distance_matrix(f"{partner_location[0]},{partner_location[1]}", f"{destination_location[0]},{destination_location[1]}")
                    
                    combined_distance = user_to_partner_distance + user_to_school_distance

                    # Calculate carbon emissions for the combined trip and individual trips
                    user_transport_type = user_row['mode_of_transport']
                    user_fuel_type = user_row['fuel_type']
                    partner_transport_type = partner_row['mode_of_transport']
                    partner_fuel_type = partner_row['fuel_type']
                    
                    emissions_combined = calculateCarbonEmissions(user_transport_type, user_fuel_type, combined_distance / 1000)
                    emissions_individual = (calculateCarbonEmissions(user_transport_type, user_fuel_type, user_to_school_distance / 1000) +
                                            calculateCarbonEmissions(partner_transport_type, partner_fuel_type, partner_to_school_distance / 1000))
                    
                    emissions_saved = emissions_individual - emissions_combined
                    
                    pairings.append((user_row['name'], partner_row['name'], emissions_saved))
        
        # Sort pairings based on emissions saved in descending order
        pairings.sort(key=lambda x: x[2], reverse=True)

        best_pairings = []
        paired = set()

        for user, partner, emissions_saved in pairings:
            if user not in paired and partner not in paired:
                best_pairings.append((user, partner, emissions_saved))
                paired.add(user)
                paired.add(partner)
        
        return best_pairings


    def calculateCarbonEmissions(transportType, fuelType, distance):
        # Get the fuel consumption rate
        fuelConsumption = fuelConsumptionMapping.get(transportType, fuelConsumptionMapping['Car'])
        
        # Get the emission factor for the fuel type
        emissionFactor = emissionFactors.get(fuelType, emissionFactors['Petrol'])
        
        # Calculate the total fuel used
        totalFuelUsed = fuelConsumption * distance
        
        # Calculate the carbon emissions
        carbonEmissions = totalFuelUsed * emissionFactor
        
        return carbonEmissions

    def convertEmissionsToIceMelt(carbonEmissions):
        # Convert CO2 emissions to ice area melted
        iceAreaMelted = (carbonEmissions / 1000) * co2ToIceArea  # convert kg to metric tons
        
        # Convert ice area to weight of ice melted assuming 1 meter thickness
        iceWeight = iceAreaMelted * 1 * iceDensity  # assuming thickness = 1 meter
        
        return iceWeight

    # Streamlit App
    st.title('Carpoolers Nearby 🚗')
    username =st.session_state.username
    try:
            user_location = get_geolocation(df[df['username'] ==username ]['address'])
            
            # Final destination: Vasant Valley School
            destination_address = 'Sector C, Vasant Kunj, New Delhi, Delhi 110070, India'
            destination_location = get_geolocation(destination_address)
            
            map = create_map(user_location, carpool_df, destination_location)
            map_output = st_folium(map, width=700, height=500)
            
            if map_output['last_object_clicked']:
                clicked_location = map_output['last_object_clicked']['lat'], map_output['last_object_clicked']['lng']
                # Find the row that matches the clicked location
                selected_person = None
                for _, row in carpool_df.iterrows():
                    location = get_geolocation(row['address'])
                    if (clicked_location[0], clicked_location[1]) == (location[0], location[1]):
                        selected_person = row
                        break
                
                if selected_person is not None:
                    transport_type = selected_person['mode_of_transport']
                    fuel_type = selected_person['fuel_type']
                    name = selected_person['name']
                    user_name = get_full_name(username)
                    # Calculate distances
                    user_to_person_distance, _ = get_distance_matrix(f"{user_location[0]},{user_location[1]}", f"{clicked_location[0]},{clicked_location[1]}")
                    person_to_school_distance, _ = get_distance_matrix(f"{clicked_location[0]},{clicked_location[1]}", f"{destination_location[0]},{destination_location[1]}")
                    user_to_school_distance,_ = get_distance_matrix(f"{user_location[0]},{user_location[1]}", f"{destination_location[0]},{destination_location[1]}")
                    
                    combined_distance = user_to_person_distance + user_to_school_distance
                    pairings = get_best_pairings(carpool_df,user_location,destination_location)
                    user_pairing = [i[0] for i in pairings if i[0] == user_name or i[1] == user_name][0]
                    stardata = df[df['name'] == user_pairing]
                    starcontact = list(stardata['parent_1_phone'])[0]
                    staremail = list(stardata['student_email'])[0]
                    starclass = list(stardata['class'])[0]
                    starparentem = list(stardata['parent_1_email'])[0]
                    carbon_emissions = calculateCarbonEmissions(transport_type, fuel_type, person_to_school_distance     / 1000) + calculateCarbonEmissions(transport_type, fuel_type, user_to_school_distance / 1000) - calculateCarbonEmissions(transport_type, fuel_type, combined_distance / 1000) # distance in km
                    st.write(f'### 🌟 Your Star Carpooler is _**{user_pairing}**_ 🌟')
                    st.write(f'- Parent Contact: +{starcontact}')
                    st.write(f'- Parent Email: {starparentem}')
                    st.write(f'- Student Class: {starclass}')
                    st.write(f'- Student Email: +{staremail}')
                    st.write('---')
                    st.write(f'### If you CoRide with _{name}_:')
                    st.write(f"- Distance from your location to the selected person: **{user_to_person_distance / 1000:.2f} km**")
                    st.write(f"- Distance from the selected person to the school: **{person_to_school_distance / 1000:.2f} km**")
                    st.write(f"- Combined distance if they pick you up and then go to school: **{combined_distance / 1000:.2f} km**")
                    st.write(f"- Total emissions saved: **{carbon_emissions:.2f} kg CO2**")
                else:
                    st.write("Selected person not found in the dataset.")
                
    except Exception as e:
            st.error(f"Error: {e}")

    # Example addresses (for demonstration purposes)
    if st.button('Show Map',type='secondary'):
        try:
            example_address = '1600 Amphitheatre Parkway, Mountain View, CA'
            user_location = get_geolocation(example_address)
            
            # Final destination: Vasant Valley School
            destination_address = 'Sector C, Vasant Kunj, New Delhi, Delhi 110070, India'
            destination_location = get_geolocation(destination_address)
            
            map = create_map(user_location, carpool_df, destination_location)
            map_output = st_folium(map, width=700, height=500)
            
            if map_output['last_object_clicked']:
                clicked_location = map_output['last_object_clicked']['lat'], map_output['last_object_clicked']['lng']
                
                # Find the row that matches the clicked location
                selected_person = None
                for _, row in carpool_df.iterrows():
                    location = get_geolocation(row['address'])
                    if (clicked_location[0], clicked_location[1]) == (location[0], location[1]):
                        selected_person = row
                        break
                
                if selected_person is not None:
                    transport_type = selected_person['mode_of_transport']
                    fuel_type = selected_person['fuel_type']
                    name = selected_person['name']
                    
                    # Calculate distances
                    user_to_person_distance, _ = get_distance_matrix(f"{user_location[0]},{user_location[1]}", f"{clicked_location[0]},{clicked_location[1]}")
                    person_to_school_distance, _ = get_distance_matrix(f"{clicked_location[0]},{clicked_location[1]}", f"{destination_location[0]},{destination_location[1]}")
                    user_to_school_distance,_ = get_distance_matrix(f"{user_location[0]},{user_location[1]}", f"{destination_location[0]},{destination_location[1]}")
                    
                    combined_distance = user_to_person_distance + user_to_school_distance

                    carbon_emissions = calculateCarbonEmissions(transport_type, fuel_type, person_to_school_distance     / 1000) + calculateCarbonEmissions(transport_type, fuel_type, user_to_school_distance / 1000) - calculateCarbonEmissions(transport_type, fuel_type, combined_distance / 1000) # distance in km
                    st.write(f"Distance from your location to the selected person: {user_to_person_distance / 1000:.2f} km")
                    st.write(f"Distance from your location to the school: {user_to_school_distance / 1000:.2f} km")
                    st.write(f"Distance from the selected person to the school: {person_to_school_distance / 1000:.2f} km")
                    st.write(f"Combined distance if they pick you up and then go to school: {combined_distance / 1000:.2f} km")
                    st.write(f"Total emissions saved: {carbon_emissions:.2f} kg CO2")
                else:
                    st.write("Selected person not found in the dataset.")
                
        except Exception as e:
            st.error(f"Error: {e}")


    st.markdown("---")

    # Dropdowns with intriguing questions about carbon emissions and climate change
    st.markdown("### 🌿 Learn More About Carbon Emissions and Climate Change")

    questions = {
        "Why is reducing carbon emissions important?": """
        🌍 Reducing carbon emissions is crucial for combating climate change, which poses significant threats to our environment, health, and economy. 
        High levels of carbon dioxide (CO₂) and other greenhouse gases in the atmosphere trap heat, leading to global warming and severe weather patterns. 
        According to the Intergovernmental Panel on Climate Change (IPCC), we need to cut global emissions by 45% by 2030 to avoid catastrophic climate impacts.
        """,
        "How does carpooling help reduce emissions?": """
        🚗 Carpooling reduces the number of vehicles on the road, which in turn decreases traffic congestion and fuel consumption. 
        Fewer cars mean less CO₂ and other harmful pollutants are released into the atmosphere. 
        Studies show that carpooling can cut individual commuting emissions by up to 50%. 
        Moreover, carpooling saves money on fuel, reduces wear and tear on vehicles, and fosters a sense of community among participants.
        """,
        "What are the health impacts of air pollution caused by vehicles?": """
        🏥 Air pollution from vehicles is a major contributor to respiratory and cardiovascular diseases. 
        Fine particulate matter (PM2.5) and nitrogen oxides (NOx) emitted from car exhausts can penetrate deep into the lungs and bloodstream, 
        causing asthma, bronchitis, heart attacks, and even premature death. According to the World Health Organization (WHO), 
        air pollution is responsible for 7 million deaths worldwide each year.
        """,
        "How can schools contribute to reducing carbon emissions?": """
        🏫 Schools can play a vital role in reducing carbon emissions by implementing eco-friendly policies and practices. 
        Promoting carpooling, encouraging the use of public transportation, and organizing bike-to-school programs can significantly lower the carbon footprint. 
        Additionally, schools can invest in energy-efficient infrastructure, reduce waste, and integrate climate education into their curricula 
        to raise awareness and inspire students to take action.
        """,
        "What are the economic benefits of reducing carbon emissions?": """
        💰 Reducing carbon emissions can lead to substantial economic benefits. 
        Investing in renewable energy sources like solar and wind creates jobs and stimulates economic growth. 
        Energy efficiency measures reduce operating costs for businesses and households. 
        Moreover, mitigating climate change can prevent the costly impacts of extreme weather events, 
        such as floods, droughts, and hurricanes, which can cause billions of dollars in damages.
        """
    }

    for question, answer in questions.items():
        with st.expander(question):
            st.markdown(answer)
    st.write('---')



   
# Display the login page if not logged in
if not st.session_state.logged_in:
    # Title and Subtitle
    col1, col2 = st.columns([1,1.5])
    with col1:
        st_lottie(lottie_welcome, height=300, key="welcome_animation")
    with col2:
        st.title("Welcome to CoRide 🌿")
        st.subheader("Please login to continue")
        st.write('---')

        # Input fields
        username = st.text_input("Username 👤", placeholder="Enter your username")
        password = st.text_input("Password 🔒", type="password", placeholder="Enter your password")
        st.markdown('<br>',unsafe_allow_html=True)
        col1,col2 = st.columns(2)
        with col1:
            if st.button("Login",type='primary', help="Login to your account"):
                login(username, password)    

else:
    # Sidebar for navigation links
    with st.sidebar:
        st.header("Navigation 🗺️")
        # Custom CSS for styling the radio buttons
        st.markdown("""
            <style>
            div[data-baseweb="radio"] > div {
                display: flex;
                flex-direction: row;
            }
            div[data-baseweb="radio"] > div > div {
                margin-right: 20px;
                border: 2px solid #ddd;
                border-radius: 5px;
                padding: 10px 20px;
                cursor: pointer;
            }
            div[data-baseweb="radio"] > div > div:hover {
                background-color: #f0f0f0;
            }
            div[data-baseweb="radio"] > div > div[data-checked="true"] {
                background-color: #007bff;
                color: white;
            }
            div[data-baseweb="radio"] > div > div[data-checked="true"] > div[role="radio"] {
                background-color: transparent;
            }
            </style>
            """, unsafe_allow_html=True)

        # Styled radio buttons for navigation
        page = st.radio("", ["Home", "Profile", "About Us", "Logout"])

    # Conditional rendering based on sidebar selection
    if page == "Home":
        home_page()
    elif page == "Profile":
        profile_page()
    elif page == "Settings":
        settings_page()
    elif page == "About Us":
        about_page()
    elif page == "Logout":
        logout()
