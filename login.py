import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import pandas as pd

# Load the CSV file
df = pd.read_csv('./Carpool2School_Full_Corrected_Dummy_Data.csv')
carpool_df = df[df['carpool'] == 'N'].head(10)

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

def get_distance_matrix(origins, destinations):
    url = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={origins}&destinations={destinations}&key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        return data['rows'][0]['elements'][0]['distance']['value'], data['rows'][0]['elements'][0]['duration']['text']
    else:
        raise Exception(f'Error fetching distance data: {data["status"]}')

def create_map(user_location, carpool_data, destination_location):
    map = folium.Map(location=user_location, zoom_start=13)
    
    # Add a marker for the user's current location
    folium.Marker(user_location, popup='Your Location', icon=folium.Icon(color='green')).add_to(map)
    
    # Add markers for carpool locations
    for _, row in carpool_data.iterrows():
        address = row['address']
        name = row['name']
        contact = row['parent_1_phone']
        transport_type = row['mode_of_transport']
        fuel_type = row['fuel_type']
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
    
    return map

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
st.title('Geolocation Map')

address_input = st.text_input('Enter your current address:')

if address_input:
    try:
        user_location = get_geolocation(address_input)
        
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
                username = 'Sai Reddy'
                pairings = get_best_pairings(carpool_df,user_location,destination_location)
                user_pairing = [i[0] for i in pairings if i[0] == username or i[1] == username]
                carbon_emissions = calculateCarbonEmissions(transport_type, fuel_type, person_to_school_distance     / 1000) + calculateCarbonEmissions(transport_type, fuel_type, user_to_school_distance / 1000) - calculateCarbonEmissions(transport_type, fuel_type, combined_distance / 1000) # distance in km
                st.write(f'Your Star Carpooler is {user_pairing}')
                st.write(f'### If you Carpool2School with {name}:')
                st.write(f"Distance from your location to the selected person: **{user_to_person_distance / 1000:.2f} km**")
                st.write(f"Distance from the selected person to the school: **{person_to_school_distance / 1000:.2f} km**")
                st.write(f"Combined distance if they pick you up and then go to school: **{combined_distance / 1000:.2f} km**")
                st.write(f"Total emissions saved: **{carbon_emissions:.2f} kg CO2**")
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
