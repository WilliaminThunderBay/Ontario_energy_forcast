import streamlit as st
import os
from PIL import Image

# 配置页面基本信息
st.set_page_config(page_title="Ontario Energy Forecasting", layout="wide")

# CSS样式
custom_css = """
<style>
.top-bar {
    background-color: #000000;
    padding: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.green-bar {
    background-color: #006A4D;
    padding: 15px;
    color: white;
    font-size: 20px;
    font-weight: bold;
}
.footer {
    background-color: #000000;
    color: white;
    text-align: center;
    padding: 10px;
    font-size: 14px;
    position: fixed;
    bottom: 0;
    width: 100%;
}
.content {
    padding-top: 50px;
    padding-bottom: 60px;
    text-align: center;
    background-color: #f5f5f5;
}
.menu {
    background-color: white;
    border: 1px solid black;
    width: 200px;
    position: absolute;
    top: 100px;
    right: 10px;
    z-index: 999;
}
.menu-item {
    padding: 10px;
    cursor: pointer;
    font-size: 16px;
}
.menu-item:hover {
    background-color: #f0f0f0;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Session State
if 'menu_visible' not in st.session_state:
    st.session_state.menu_visible = False
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# 菜单函数
def toggle_menu():
    st.session_state.menu_visible = not st.session_state.menu_visible

def set_page(page_name):
    st.session_state.page = page_name
    st.session_state.menu_visible = False

# 顶部黑色栏
with st.container():
    cols = st.columns([10, 1])
    with cols[0]:
        try:
            icon = Image.open("1.png")
            st.image(icon, width=160)
        except Exception:
            st.warning("Logo image not found.")

    with cols[1]:
        menu_icon = "3.png" if st.session_state.menu_visible else "2.png"
        if st.button("", key="menu_button"):
            toggle_menu()
        try:
            icon_image = Image.open(menu_icon)
            st.image(icon_image, width=100)
        except Exception:
            st.error("Menu icon not found.")

# 下拉菜单
if st.session_state.menu_visible:
    menu_options = ["Home", "Visualization", "Prediction", "Evaluation"]
    for option in menu_options:
        if st.button(option, key=f"menu_{option}"):
            set_page(option)

# 顶部绿色栏
st.markdown('<div class="green-bar">Ontario Energy Forecasting</div>', unsafe_allow_html=True)

# 主内容区域
if st.session_state.page == "Home":
    with st.container():
        st.markdown('<div class="content">', unsafe_allow_html=True)
        try:
            main_image = Image.open("main.png")
            st.image(main_image, use_column_width=True)
        except Exception:
            st.error("(No main.png found)")

        st.markdown("<h1 style='font-size:30px;font-weight:bold;color:black;'>Welcome to Ontario Energy Forecasting System!</h1>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "Visualization":
    st.header("Data Visualization (Images)")
    vis_path = "./Visulation"
    descriptions = {
        "Average Monthly Temperature.png": "Monthly average temperature variations throughout the year.",
        "Energy Demand over time.png": "Energy demand fluctuations over different periods.",
        "Energy Price Over time.png": "Energy prices fluctuation trends over time."
        # Add other descriptions here...
    }

    if os.path.exists(vis_path):
        images = [img for img in os.listdir(vis_path) if img.lower().endswith('.png')]
        cols = st.columns(2)
        for idx, img_name in enumerate(images):
            with cols[idx % 2]:
                st.subheader(img_name)
                img = Image.open(os.path.join(vis_path, img_name))
                st.image(img, use_column_width=True)
                st.write(descriptions.get(img_name, "No description available."))
    else:
        st.error("Visualization folder not found.")

elif st.session_state.page == "Prediction":
    st.header("Prediction Configuration")
    model = st.selectbox("Select Model", ["ARIMA", "LightGBM", "XGboost", "RandomForest"])
    target = st.selectbox("Prediction Target", ["Electricity Demand", "Electricity Price", "Electricity Demand & Electricity Price"])

    if st.button("Run Prediction"):
        prediction_map = {
            ("ARIMA", "Electricity Price"): "Arima forcast for electricity price.png",
            ("ARIMA", "Electricity Demand"): "Arima Forecast for electricity demand.png"
            # Complete the mapping as needed
        }
        filename = prediction_map.get((model, target))
        if filename:
            img_path = os.path.join("./predict", filename)
            if os.path.exists(img_path):
                st.image(Image.open(img_path), caption=f"{model} prediction for {target}")
            else:
                st.error("Prediction image not found.")
        else:
            st.error("No matching prediction available.")

elif st.session_state.page == "Evaluation":
    st.header("Model Evaluation")
    eval_path = "./Evaluation"

    if os.path.exists(eval_path):
        images = [img for img in os.listdir(eval_path) if img.lower().endswith('.png')]
        cols = st.columns(2)
        for idx, img_name in enumerate(images):
            with cols[idx % 2]:
                st.subheader(img_name)
                img = Image.open(os.path.join(eval_path, img_name))
                st.image(img, use_column_width=True)
                st.write(f"Description for {img_name}: Evaluation results and performance indicators.")
    else:
        st.error("Evaluation folder not found.")

# 底部版权栏
st.markdown('<div class="footer">© Data Science Project, 2025-3-26</div>', unsafe_allow_html=True)
