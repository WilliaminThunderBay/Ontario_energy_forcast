import streamlit as st
import os
import pandas as pd
from PIL import Image
import time
import random

def custom_navigation():
    """
    Creates a custom navigation bar using HTML and CSS
    """
    st.markdown("""
    <style>
    /* Custom Navigation Container */
    .nav-container {
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #f0f2f6;
        border-radius: 50px;
        padding: 10px 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Navigation Links */
    .nav-link {
        text-decoration: none;
        color: #333;
        padding: 10px 20px;
        margin: 0 10px;
        border-radius: 25px;
        transition: all 0.3s ease;
        font-weight: 500;
        position: relative;
        overflow: hidden;
    }
    
    /* Active Navigation Link */
    .nav-link.active {
        background-color: #007bff;
        color: white !important;
        box-shadow: 0 4px 6px rgba(0,123,255,0.2);
    }
    
    /* Hover Effect */
    .nav-link:hover {
        background-color: rgba(0,123,255,0.1);
        color: #007bff;
    }
    
    /* Hide default Streamlit radio button */
    .stRadio > div > div > label > div > div > div {
        display: none !important;
    }
    </style>
    
    <div class="nav-container">
        <script>
        // JavaScript to handle active state
        document.addEventListener('DOMContentLoaded', (event) => {
            const links = document.querySelectorAll('.nav-link');
            const currentPath = window.location.pathname;
            
            links.forEach(link => {
                link.addEventListener('click', function() {
                    links.forEach(l => l.classList.remove('active'));
                    this.classList.add('active');
                });
            });
        });
        </script>
    """, unsafe_allow_html=True)

    # Create custom navigation using HTML
    nav_html = """
    <div class="nav-links">
        <a href="#Home" class="nav-link" onclick="window.location.reload()">Home</a>
        <a href="#Visualization" class="nav-link" onclick="window.location.reload()">Visualization</a>
        <a href="#Prediction" class="nav-link" onclick="window.location.reload()">Prediction</a>
        <a href="#Evaluation" class="nav-link" onclick="window.location.reload()">Evaluation</a>
    </div>
    """
    st.markdown(nav_html, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Ontario Energy Forecasting System", layout="wide")

    # Replace the standard radio button with custom navigation
    custom_navigation()

    # Navigation
    pages = {
        "Home": home_page,
        "Visualization": visualization_page,
        "Prediction": prediction_page,
        "Evaluation": evaluation_page
    }

    # Determine current page based on hash in URL
    current_page = "Home"
    page_hash = st.experimental_get_query_params().get("page", ["Home"])[0]
    
    if page_hash in pages:
        current_page = page_hash

    # Call the appropriate page function
    pages[current_page]()

# Rest of the functions remain the same as in the original script
def home_page():
    st.title("Ontario Energy Forecasting System")
    
    # Try to display main image
    try:
        img = Image.open("main.png")
        st.image(img, use_container_width=True)
    except Exception as e:
        st.warning(f"Could not load main image: {e}")
    
    st.write("Welcome to the Ontario Energy Forecasting System!")
    
    # Footer-like information
    st.markdown("---")
    st.markdown("© Data Science Project_Group02, 2025-3-26--")

def visualization_page():
    st.header("Data Visualization")
    
    descriptions = {
        "Average Monthly Temperature.png": "This chart represents the monthly average temperature variations throughout the year, clearly showing the seasonal temperature differences and their impact on energy demand.",
        "Distribution of Temp-population-hourly demand.png": "This visualization illustrates the distributions and relationships among temperature, population density, and hourly energy demand.",
        "Energy Demand Cluster Based on Climate change.png": "A clustering visualization that categorizes energy demand patterns based on different climatic conditions, highlighting how climate change may affect future energy usage.",
        "Energy Demand over time.png": "A time series graph depicting how energy demand fluctuates over different periods, helping identify peak usage times and seasonal variations.",
        "Energy Demand Vs Wind Speed.png": "A scatter plot showing the relationship between wind speed and energy demand, illustrating potential correlations or influences of wind conditions on electricity consumption.",
        "Energy Price Over time.png": "This line chart tracks the fluctuations in energy prices over time, offering insights into pricing trends and their relation to energy market dynamics.",
        "Feature Correlation.png": "A heatmap displaying correlations among various features, such as temperature, humidity, population, and other factors that might influence energy consumption.",
        "impact of extreme weather on energy demand.png": "This visualization shows how extreme weather events, such as heatwaves or cold snaps, significantly affect energy demand peaks and overall consumption.",
        "Mutual information scores for predictiong hourly_demand.png": "Bar chart depicting mutual information scores of various features, assessing their predictive power for forecasting hourly energy demand.",
        "Ontario Population over time.png": "A line graph illustrating the population growth trend in Ontario, providing context for understanding the changing scale of energy demands over time.",
        "Population Vs. Energy Demand.png": "A scatter plot analyzing the relationship between population size and energy demand, highlighting the direct impact of population growth on energy consumption.",
        "Scatter Matrix of Electricity Demand Price and Weather Factors.png": "Scatter matrix exploring relationships between electricity demand, pricing, and weather variables, showing detailed interactions between multiple variables.",
        "Temperature Trends Over Time.png": "A detailed time series illustrating temperature trends over an extended period, indicating possible long-term climatic shifts affecting energy usage.",
        "Vs01-Averege Hourly Demand by Season in Ontario.png": "Bar graph showing average hourly energy demand segmented by season in Ontario, emphasizing seasonal variations in energy consumption."
    }
    
    visualization_folder = "./Visulation"
    if os.path.exists(visualization_folder):
        image_files = [f for f in os.listdir(visualization_folder) if f.lower().endswith(".png")]
        
        for i in range(0, len(image_files), 2):
            cols = st.columns(2)
            with cols[0]:
                img_path = os.path.join(visualization_folder, image_files[i])
                img = Image.open(img_path)
                st.image(img, use_container_width=True)
                st.caption(descriptions.get(image_files[i], "No description"))
            
            if i + 1 < len(image_files):
                with cols[1]:
                    img_path = os.path.join(visualization_folder, image_files[i+1])
                    img = Image.open(img_path)
                    st.image(img, use_container_width=True)
                    st.caption(descriptions.get(image_files[i+1], "No description"))

    else:
        st.error("Visualization folder not found.")

def prediction_page():
    st.header("Prediction Configuration")
    
    model = st.selectbox("Select Model", 
        ["ARIMA", "LightGBM", "XGboost", "RandomForest"])
    
    target = st.selectbox("Prediction Target", 
        ["Electricity Demand", "Electricity Price", 
         "Electricity Demand & Electricity Price"])
    
    if st.button("Run Prediction"):
        st.info(f"Running {model} for {target} prediction (5 Years)...")
        time.sleep(2 + random.randint(1, 3))
        model_target_map = {
            ("ARIMA", "Electricity Price"): "Arima forcast for electricity price.png",
            ("ARIMA", "Electricity Demand"): "Arima Forecast for electricity demand.png",
            ("ARIMA", "Electricity Demand & Electricity Price"): "Arima-prediction.png",
            ("LightGBM", "Electricity Price"): "prediction-price-lightgbm.png",
            ("LightGBM", "Electricity Demand"): "prediction-demand-lightgbm.png",
            ("LightGBM", "Electricity Demand & Electricity Price"): "prediciton-lightgbm.png",
            ("XGboost", "Electricity Price"): "prediction-price-xgboost.png",
            ("XGboost", "Electricity Demand"): "prediction-demand-xgboost.png",
            ("XGboost", "Electricity Demand & Electricity Price"): "prediction-xgboost.png",
            ("RandomForest", "Electricity Price"): "prediction-price-randomforest.png",
            ("RandomForest", "Electricity Demand"): "prediction-demand-RandomForest.png",
            ("RandomForest", "Electricity Demand & Electricity Price"): "prediction-randomforest.png",
        }
        
        filename = model_target_map.get((model, target))
        if filename:
            try:
                img_path = os.path.join("./predict", filename)
                img = Image.open(img_path)
                st.image(img, use_container_width=True)
                st.caption(f"Prediction result for {model} - {target}")
            except Exception as e:
                st.error(f"Could not load prediction image: {e}")
        else:
            st.warning("No matching prediction image found.")

def evaluation_page():
    st.header("Model Evaluation")
    
    evaluation_folder = "./Evaluation"
    if os.path.exists(evaluation_folder):
        image_files = [f for f in os.listdir(evaluation_folder) if f.lower().endswith(".png")]
        
        for i in range(0, len(image_files), 2):
            cols = st.columns(2)
            with cols[0]:
                img_path = os.path.join(evaluation_folder, image_files[i])
                img = Image.open(img_path)
                st.image(img, use_container_width=True)
                st.caption(f"Evaluation: {os.path.splitext(image_files[i])[0]}")
            
            if i + 1 < len(image_files):
                with cols[1]:
                    img_path = os.path.join(evaluation_folder, image_files[i+1])
                    img = Image.open(img_path)
                    st.image(img, use_container_width=True)
                    st.caption(f"Evaluation: {os.path.splitext(image_files[i+1])[0]}")
    else:
        st.error("Evaluation folder not found.")

# Run the app
if __name__ == "__main__":
    main()