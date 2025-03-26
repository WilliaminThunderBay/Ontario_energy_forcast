import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from PIL import Image

# ------------------loading data function------------------
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"Data loading failed: {e}")
        return None

# ------------------Main Streamlit App------------------
def main():
    st.set_page_config(page_title="Ontario Energy Forecasting System", layout="wide")

    # Sidebar Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", 
        ["Home", "Visualization", "Prediction", "Evaluation"])

    # File uploader (optional - for custom CSV upload)
    st.sidebar.markdown("### Upload your data")
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type="csv")
    
    # Load data
    if uploaded_file:
        df = load_data(uploaded_file)
    else:
        df = load_data('data.csv')

    # Home Page
    if page == "Home":
        st.title("Ontario Energy Forecasting System")
        
        # Try to display main image
        try:
            img = Image.open("main.png")
            st.image(img, use_column_width=True)
        except Exception as e:
            st.warning(f"Could not load main image: {e}")
        
        st.write("Welcome to the Ontario Energy Forecasting System!")
        
        # Footer-like information
        st.markdown("---")
        st.markdown("© Data Science Project, 2025-3-25")

    # Visualization Page
    elif page == "Visualization":
        st.header("Data Visualization")
        
        visualization_folder = "./Visulation"
        if os.path.exists(visualization_folder):
            image_files = [f for f in os.listdir(visualization_folder) if f.lower().endswith(".png")]
            
            descriptions = {
                "Average Monthly Temperature.png": "Monthly average temperature variations",
                "Distribution of Temp-population-hourly demand.png": "Temperature, population, and hourly demand distribution",
                "Energy Demand Cluster Based on Climate change.png": "Energy demand clusters based on climate conditions",
                "Energy Demand over time.png": "Energy demand fluctuations over time",
                "Energy Demand Vs Wind Speed.png": "Energy demand vs wind speed",
                "Energy Price Over time.png": "Energy price trends",
                "Feature Correlation.png": "Feature correlations",
                "impact of extreme weather on energy demand.png": "Extreme weather impact on energy demand",
                "Mutual information scores for predictiong hourly_demand.png": "Feature predictive power",
                "Ontario Population over time.png": "Ontario population growth",
                "Population Vs. Energy Demand.png": "Population vs energy demand",
                "Scatter Matrix of Electricity Demand Price and Weather Factors.png": "Multivariate relationships",
                "Temperature Trends Over Time.png": "Temperature trends",
                "Vs01-Averege Hourly Demand by Season in Ontario.png": "Hourly demand by season"
            }
            
            for i in range(0, len(image_files), 2):
                cols = st.columns(2)
                with cols[0]:
                    img_path = os.path.join(visualization_folder, image_files[i])
                    img = Image.open(img_path)
                    st.image(img, use_column_width=True)
                    st.caption(descriptions.get(image_files[i], "No description"))
                
                if i + 1 < len(image_files):
                    with cols[1]:
                        img_path = os.path.join(visualization_folder, image_files[i+1])
                        img = Image.open(img_path)
                        st.image(img, use_column_width=True)
                        st.caption(descriptions.get(image_files[i+1], "No description"))

        else:
            st.error("Visualization folder not found.")

    # Prediction Page
    elif page == "Prediction":
        st.header("Prediction Configuration")
        
        model = st.selectbox("Select Model", 
            ["ARIMA", "LightGBM", "XGboost", "RandomForest"])
        
        target = st.selectbox("Prediction Target", 
            ["Electricity Demand", "Electricity Price", 
             "Electricity Demand & Electricity Price"])
        
        if st.button("Run Prediction"):
            st.info(f"Running {model} for {target} prediction (5 Years)...")
            
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
                    st.image(img, use_column_width=True)
                    st.caption(f"Prediction result for {model} - {target}")
                except Exception as e:
                    st.error(f"Could not load prediction image: {e}")
            else:
                st.warning("No matching prediction image found.")

    # Evaluation Page
    elif page == "Evaluation":
        st.header("Model Evaluation")
        
        evaluation_folder = "./Evaluation"
        if os.path.exists(evaluation_folder):
            image_files = [f for f in os.listdir(evaluation_folder) if f.lower().endswith(".png")]
            
            for i in range(0, len(image_files), 2):
                cols = st.columns(2)
                with cols[0]:
                    img_path = os.path.join(evaluation_folder, image_files[i])
                    img = Image.open(img_path)
                    st.image(img, use_column_width=True)
                    st.caption(f"Evaluation: {os.path.splitext(image_files[i])[0]}")
                
                if i + 1 < len(image_files):
                    with cols[1]:
                        img_path = os.path.join(evaluation_folder, image_files[i+1])
                        img = Image.open(img_path)
                        st.image(img, use_column_width=True)
                        st.caption(f"Evaluation: {os.path.splitext(image_files[i+1])[0]}")
        else:
            st.error("Evaluation folder not found.")

# Run the app
if __name__ == "__main__":
    main()
