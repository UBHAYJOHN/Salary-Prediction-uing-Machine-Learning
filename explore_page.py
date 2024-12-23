import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to load and clean data
@st.cache_data
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    df = df[df["ConvertedCompYearly"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)

    # Clean the 'Country' column to group less frequent countries
    country_map = shorten_categories(df.Country.value_counts(), 200)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedCompYearly"] <= 250000]
    df = df[df["ConvertedCompYearly"] >= 15000]
    df = df[df["Country"] != "Other"]

    # Clean the 'YearsCodePro' and 'EdLevel' columns
    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    return df

# Functions for cleaning data
def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

# Function to render the Explore page
def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    # Load data
    df = load_data()

    st.write("### Stack Overflow Developer Survey 2022")

    # Pie Chart: Data distribution by country
    st.write("#### Number of Data from Different Countries")
    country_data = df["Country"].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(country_data, labels=country_data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)

    # Filter by country
    selected_country = st.selectbox('Select a Country', df['Country'].unique())
    country_df = df[df['Country'] == selected_country]

    # Bar Chart: Mean salary by country
    st.write(f"#### Mean Salary in {selected_country}")
    country_salary_data = country_df.groupby(["Country"])["Salary"].mean()
    st.bar_chart(country_salary_data)

    # Line Chart: Salary by Experience
    st.write("#### Mean Salary Based on Experience Level")
    experience_salary_data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(experience_salary_data)

# Run the app
if __name__ == "__main__":
    show_explore_page()
