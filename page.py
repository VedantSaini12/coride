import streamlit as st
import pandas as pd
import random

# Load the existing data
csv_path = "carpool2school_full_updated_dummy_data.csv"
try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    df = pd.DataFrame(columns=[
        "name", "student email", "username", "password", "school name", "class",
        "parent 1 name", "parent 1 phone", "parent 1 email",
        "parent 2 name", "parent 2 phone", "parent 2 email",
        "address", "pin code", "mode of transport", "carpool", "car details", "fuel type"
    ])

# Set page title and layout
st.set_page_config(page_title="Carpool2School - Student Profile", layout="wide")

# Page title and subtitle
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🚗 Carpool2School 🌍</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #6A1B9A;'>Update Your Profile</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6A1B9A;'>Please fill out the form below to keep your information up-to-date!</p>", unsafe_allow_html=True)

# Input field for username to preload data
username_input = st.text_input("Enter your username to preload data", "")

# Function to preload data
def preload_data(username):
    if username in df['username'].values:
        user_data = df[df['username'] == username].iloc[0]
        return user_data
    else:
        return None

# Preload data if username exists
user_data = preload_data(username_input)

# Create a form for collecting student information
with st.form(key='student_profile_form'):
    st.markdown("<h3 style='text-align: center;'>📋 Student Profile Form</h3>", unsafe_allow_html=True)

    name = st.text_input("👤 Full Name", user_data['name'] if user_data is not None else "")
    student_email = st.text_input("📧 Student Email", user_data['student email'] if user_data is not None else "")
    school_name = st.selectbox("🏫 School Name", [
        "Delhi Public School", "Springdales School", "The Mother's International School", 
        "Vasant Valley School", "Sanskriti School"
    ], index=list(df['school name']).index(user_data['school name']) if user_data is not None else 0)
    student_class = st.selectbox("🎓 Class", [str(i) for i in range(1, 13)], index=int(user_data['class'])-1 if user_data is not None else 0)
    parent1_name = st.text_input("👨‍👩‍👦 Parent 1 Name", user_data['parent 1 name'] if user_data is not None else "")
    parent1_phone = st.text_input("📞 Parent 1 Phone", user_data['parent 1 phone'] if user_data is not None else "")
    parent1_email = st.text_input("✉️ Parent 1 Email", user_data['parent 1 email'] if user_data is not None else "")
    parent2_name = st.text_input("👨‍👩‍👦 Parent 2 Name", user_data['parent 2 name'] if user_data is not None else "")
    parent2_phone = st.text_input("📞 Parent 2 Phone", user_data['parent 2 phone'] if user_data is not None else "")
    parent2_email = st.text_input("✉️ Parent 2 Email", user_data['parent 2 email'] if user_data is not None else "")
    address = st.text_input("🏠 Address", user_data['address'] if user_data is not None else "")
    pin_code = st.text_input("📮 Pin Code", user_data['pin code'] if user_data is not None else "")
    mode_of_transport = st.selectbox("🚘 Mode of Transport", ["Car", "Bus"], index=["Car", "Bus"].index(user_data['mode of transport']) if user_data is not None else 0)

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
        car_company, car_model = (user_data['car details'].split() if user_data is not None and user_data['car details'] else ("", ""))
        car_company = st.selectbox("Car Company", car_companies, index=car_companies.index(car_company) if car_company else 0)
        car_model = st.selectbox("Car Model", car_models[car_company], index=car_models[car_company].index(car_model) if car_model else 0)
        fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel"], index=["Petrol", "Diesel"].index(user_data['fuel type']) if user_data is not None else 0)
    else:
        carpool = ""
        car_company = ""
        car_model = ""
        fuel_type = "Diesel"

    # Save button
    save_button = st.form_submit_button(label="Save 💾", help="Click to save your information")

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

        df.to_csv(csv_path, index=False)
        st.success("Your information has been saved successfully! 🎉")

# Footer
st.markdown("<footer style='text-align: center; color: #9E9E9E;'>© 2024 Carpool2School. All rights reserved.</footer>", unsafe_allow_html=True)