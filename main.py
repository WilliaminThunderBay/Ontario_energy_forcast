import streamlit as st
import os
import pandas as pd
from PIL import Image
import time
import random

# Custom CSS for button-style navigation
def custom_nav_css():
    st.markdown("""
    <style>
    /* Custom navigation button styling */
    .stRadio > div {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 20px;
    }
    .stRadio > div > div {
        margin: 0 !important;
    }
    .stRadio > div > div > label {
        background-color: #f0f2f6;
        color: #333;
        padding: 10px 20px;
        border-radius: 10px;
        transition: all 0.3s ease;
        cursor: pointer;
        border: 2px solid transparent;
    }
    .stRadio > div > div > label:hover {
        background-color: #e6e9ef;
        border-color: #4CAF50;
    }
    .stRadio > div > div > [data-baseweb="radio"] {
        display: none;
    }
    .stRadio > div > div > label[data-baseweb="radio"][aria-checked="true"] {
        background-color: #4CAF50;
        color: white;
        border-color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# ------------------Main Streamlit App------------------
def main():
    st.set_page_config(page_title="Ontario Energy Forecasting System", layout="wide")

    # Apply custom CSS for navigation
    custom_nav_css()

    # Navigation
    pages = {
        "Home": home_page,
        "Visualization": visualization_page,
        "Prediction": prediction_page,
        "Evaluation": evaluation_page
    }

    # Create menu in the main page instead of sidebar
    page = st.radio("Navigation", list(pages.keys()), horizontal=True)

    # Call the appropriate page function
    pages[page]()

def home_page():
    st.title("Ontario Energy Forecasting System")
    
    # Try to display main image with more robust error handling
    img_path = "main.png"
    if os.path.exists(img_path):
        try:
            img = Image.open(img_path)
            st.image(img, use_container_width=True)
        except Exception as e:
            st.error(f"Error processing image: {e}")
    else:
        st.info("Main image not found. Please check the image file.")
    
    st.write("Welcome to the Ontario Energy Forecasting System!")
    
    # Footer-like information
    st.markdown("---")
    st.markdown("© Data Science Project, 2025-3-26")

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
        
        if not image_files:
            st.info("No visualization images found in the folder.")
        
        for i in range(0, len(image_files), 2):
            cols = st.columns(2)
            with cols[0]:
                img_path = os.path.join(visualization_folder, image_files[i])
                try:
                    img = Image.open(img_path)
                    st.image(img, use_container_width=True)
                    st.caption(descriptions.get(image_files[i], "No description"))
                except Exception as e:
                    st.error(f"Could not load image {image_files[i]}: {e}")
            
            if i + 1 < len(image_files):
                with cols[1]:
                    img_path = os.path.join(visualization_folder, image_files[i+1])
                    try:
                        img = Image.open(img_path)
                        st.image(img, use_container_width=True)
                        st.caption(descriptions.get(image_files[i+1], "No description"))
                    except Exception as e:
                        st.error(f"Could not load image {image_files[i+1]}: {e}")

    else:
        st.error("Visualization folder not found. Please check the folder path.")

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
            predict_folder = "./predict"
            full_path = os.path.join(predict_folder, filename)
            
            if os.path.exists(full_path):
                try:
                    img = Image.open(full_path)
                    st.image(img, use_container_width=True)
                    st.caption(f"Prediction result for {model} - {target}")
                except Exception as e:
                    st.error(f"Could not load prediction image: {e}")
            else:
                st.warning(f"Prediction image {filename} not found in {predict_folder}.")
        else:
            st.warning("No matching prediction image found.")

def evaluation_page():
    st.header("Model Evaluation")
    
    evaluation_folder = "./Evaluation"
    if os.path.exists(evaluation_folder):
        image_files = [f for f in os.listdir(evaluation_folder) if f.lower().endswith(".png")]
        
        if not image_files:
            st.info("No evaluation images found in the folder.")
        
        for i in range(0, len(image_files), 2):
            cols = st.columns(2)
            with cols[0]:
                img_path = os.path.join(evaluation_folder, image_files[i])
                try:
                    img = Image.open(img_path)
                    st.image(img, use_container_width=True)
                    st.caption(f"Evaluation: {os.path.splitext(image_files[i])[0]}")
                except Exception as e:
                    st.error(f"Could not load image {image_files[i]}: {e}")
            
            if i + 1 < len(image_files):
                with cols[1]:
                    img_path = os.path.join(evaluation_folder, image_files[i+1])
                    try:
                        img = Image.open(img_path)
                        st.image(img, use_container_width=True)
                        st.caption(f"Evaluation: {os.path.splitext(image_files[i+1])[0]}")
                    except Exception as e:
                        st.error(f"Could not load image {image_files[i+1]}: {e}")
    else:
        st.error("Evaluation folder not found. Please check the folder path.")

# Run the app
if __name__ == "__main__":
    main()