import streamlit as st 
import pickle 
import numpy as np 

def load_model():  # Corrected function name
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()  # Corrected function name

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")
    
    st.write("""### We need some information to predict the salary""")
    
    countries = [  # Converted to list
        "Germany",
        "United Kingdom of Great Britain",
        "Northern Ireland",
        "India",
        "Canada",
        "France",
        "Brazil",
        "Spain",
        "Netherlands",
        "Australia",
        "Italy",
        "Poland",
        "Sweden",
        "Russian Federation",
        "Switzerland",
    ]

    education = [  # Converted to list
        "Master’s degree",
        "Bachelor’s degree",
        "Less than a Bachelors",
        "Post grad",
    ]

    country = st.selectbox("Country", countries)
    education_level = st.selectbox("Education level", education)  # Renamed to avoid shadowing

    experience = st.slider("Years of experience", 0, 50, 3) 

    ok = st.button("Calculate Salary")
    if ok:
        X = np.array([[country, education_level, experience]])
        X[:, 0] = le_country.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])
        X = X.astype(float)
        
        salary = regressor.predict(X)
        st.subheader(f"The estimated Salary is INR {20 * salary[0]:,.2f}")


