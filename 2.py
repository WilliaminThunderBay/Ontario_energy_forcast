import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ------------------loading data function------------------
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"data loading failed: {e}")
        return None
    return df

class EnergyPredictionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ontario Energy Demand System")
        self.root.state('zoomed')

        # 加载示例数据
        self.df = load_data('data.csv')

        # ===================== 顶部黑色栏 =====================
        self.top_frame = tk.Frame(root, bg="#000000", height=200)
        self.top_frame.pack(fill="x", side="top")

        # 左侧logo
        try:
            self.icon_image = Image.open("1.png").resize((160, 60))
            self.icon = ImageTk.PhotoImage(self.icon_image)
            self.icon_label = tk.Label(self.top_frame, image=self.icon, bg="#000000")
            self.icon_label.pack(side="left", padx=20)
        except Exception:
            print("Warning: icon image not found.")

        # 菜单与关闭图标
        self.menu_icon = None
        self.close_icon = None
        try:
            menu_img = Image.open("2.png").resize((160, 60))
            self.menu_icon = ImageTk.PhotoImage(menu_img)
            close_img = Image.open("3.png").resize((160, 60))
            self.close_icon = ImageTk.PhotoImage(close_img)
        except Exception as e:
            print(f"Warning: menu/close icon not found: {e}")
        
        # 右侧菜单按钮
        self.right_icon_label = tk.Label(self.top_frame, bg="#000000", cursor="hand2")
        self.right_icon_label.pack(side="right", padx=20)
        if self.menu_icon:
            self.right_icon_label.config(image=self.menu_icon)
        self.right_icon_label.bind("<Button-1>", self.toggle_dropdown_menu)
        self.menu_visible = False

        # ===================== 顶部绿色栏 =====================
        self.green_bar = tk.Frame(root, bg="#006A4D", height=100)
        self.green_bar.pack(fill="x", side="top")
        self.green_label = tk.Label(self.green_bar, text="Ontario Energy Forecasting",
                                    fg="white", bg="#006A4D", font=("Arial", 14, "bold"))
        self.green_label.pack(side="left", padx=30, pady=5)

        # ===================== 下拉菜单框架 =====================
        self.dropdown_frame = tk.Frame(self.root, bg="white", relief="solid", borderwidth=2)
        self.dropdown_buttons = []
        options = ["Home", "Visualization", "Prediction", "Evaluation"]
        for option in options:
            btn = tk.Button(self.dropdown_frame, text=option, anchor="w", relief="flat", 
                            bg="white", fg="black", width=20, height=2, font=("Arial", 10),
                            command=lambda opt=option: self.handle_menu_selection(opt))
            btn.pack(fill="x", padx=10, pady=5)
            self.dropdown_buttons.append(btn)
        self.root.bind("<Button-1>", self.close_menu_if_outside)

        # ===================== 主内容框架 =====================
        self.content_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.content_frame.pack(fill="both", expand=True)

        # 创建各个页面
        self.create_home_page()
        self.create_visualization_page()
        self.create_predict_page()   # 使用新的预测页面逻辑
        self.create_evaluation_page()

        # 默认显示首页
        self.show_page("Home")
        self.current_page = None

    # ------------------顶部菜单相关------------------
    def toggle_dropdown_menu(self, event):
        if self.menu_visible:
            self.hide_dropdown_menu()
        else:
            self.show_dropdown_menu()

    def show_dropdown_menu(self):
        if not self.menu_visible:
            x = self.right_icon_label.winfo_rootx() - self.root.winfo_rootx()
            y = self.top_frame.winfo_height() + self.green_bar.winfo_height()
            dropdown_width = 200
            self.dropdown_frame.place(x=x, y=y, width=dropdown_width)
            self.dropdown_frame.lift()
            self.menu_visible = True
            if self.close_icon:
                self.right_icon_label.config(image=self.close_icon)

    def hide_dropdown_menu(self):
        if self.menu_visible:
            self.dropdown_frame.place_forget()
            if self.menu_icon:
                self.right_icon_label.config(image=self.menu_icon)
            self.menu_visible = False

    def close_menu_if_outside(self, event):
        if self.menu_visible:
            widget_under_mouse = self.root.winfo_containing(event.x_root, event.y_root)
            if widget_under_mouse not in [self.dropdown_frame, self.right_icon_label] and \
               widget_under_mouse not in self.dropdown_buttons:
                self.hide_dropdown_menu()

    def handle_menu_selection(self, option):
        self.hide_dropdown_menu()
        self.show_page(option)

    # ------------------Home Page------------------
    def create_home_page(self):
        self.home_frame = tk.Frame(self.content_frame, bg="#f5f5f5")
        top_spacer = tk.Label(self.home_frame, bg="#f5f5f5")
        top_spacer.pack(pady=50)
        try:
            img = Image.open("main.png")
            self.home_img = ImageTk.PhotoImage(img)
            self.home_img_label = tk.Label(self.home_frame, image=self.home_img, bg="#f5f5f5")
            self.home_img_label.pack(pady=10)
        except Exception as e:
            print(f"Warning: main.png not found: {e}")
            self.home_img_label = tk.Label(self.home_frame, text="(No main.png found)",
                                           bg="#f5f5f5", font=("Arial", 18, "bold"))
            self.home_img_label.pack(pady=10)
        self.home_text_label = tk.Label(
            self.home_frame,
            text="Welcome to Ontario Energy Forecasting System!",
            bg="#f5f5f5",
            font=("Arial", 30, "bold")
        )
        self.home_text_label.pack(pady=5)
        # 底部黑色版权栏
        footer_frame = tk.Frame(self.home_frame, bg="#000000", height=30)
        footer_frame.pack(side="bottom", fill="x")
        
        footer_label = tk.Label(
            footer_frame,
            text="© Data Science Project, 2025-3-25",
            fg="white",
            bg="#000000",
            font=("Arial", 10)
        )
        footer_label.pack(pady=5)


    # ------------------Visualization Page------------------
    def create_visualization_page(self):
        self.visualization_frame = tk.Frame(self.content_frame, bg="#ffffff")
        vis_label = tk.Label(self.visualization_frame, text="Data Visualization (Images)",
                             font=("Arial", 18, "bold"), bg="#ffffff")
        vis_label.pack(pady=10)

        self.vis_canvas = tk.Canvas(self.visualization_frame, bg="#ffffff", highlightthickness=0)
        self.vis_canvas.pack(side="left", fill="both", expand=True)
        self.vis_scrollbar = tk.Scrollbar(self.visualization_frame, orient="vertical", command=self.vis_canvas.yview)
        self.vis_scrollbar.pack(side="right", fill="y")
        self.vis_canvas.configure(yscrollcommand=self.vis_scrollbar.set)

        self.images_frame = tk.Frame(self.vis_canvas, bg="#ffffff")
        self.vis_canvas.create_window((0, 0), window=self.images_frame, anchor="nw")

        def on_images_frame_configure(event):
            self.vis_canvas.configure(scrollregion=self.vis_canvas.bbox("all"))
        self.images_frame.bind("<Configure>", on_images_frame_configure)

        self.visualization_frame.bind("<Enter>", lambda e: self.visualization_frame.focus_set())
        self.visualization_frame.bind("<MouseWheel>", 
                                      lambda event: self.vis_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

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

        folder_path = "./Visulation"
        self.loaded_images_vis = []

        if not os.path.exists(folder_path):
            tk.Label(self.images_frame, text="Visualization folder not found.", fg="red", bg="#ffffff").pack()
            return

        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".png")]
        if not image_files:
            tk.Label(self.images_frame, text="No images found.", fg="red", bg="#ffffff").pack()
            return

        for idx, img_file in enumerate(image_files):
            file_path = os.path.join(folder_path, img_file)
            title_text = os.path.splitext(img_file)[0]

            column_frame = tk.Frame(self.images_frame, bg="#ffffff")
            column_frame.grid(row=idx // 2, column=idx % 2, padx=10, pady=10, sticky="n")

            tk.Label(column_frame, text=title_text, font=("Times New Roman", 16, "bold"), bg="#ffffff").pack(pady=(10, 2))

            try:
                pil_img = Image.open(file_path)
                pil_img.thumbnail((600, 450))
                img_obj = ImageTk.PhotoImage(pil_img)
                self.loaded_images_vis.append(img_obj)

                tk.Label(column_frame, image=img_obj, bg="#ffffff").pack(pady=5)

                description = descriptions.get(img_file, "No description available.")
                tk.Label(column_frame, text=description, font=("Arial", 12), bg="#ffffff",
                         wraplength=550, justify="left").pack(pady=(0, 15))
            except Exception as e:
                tk.Label(column_frame, text=f"Error loading {img_file}: {e}", fg="red", bg="#ffffff").pack()

        self.visualization_frame.pack(fill="both", expand=True)

    # ------------------Predict Page (新)------------------
    def create_predict_page(self):
        """
        创建预测页面：
        1. 下拉选择模型（ARIMA, LightGBM, XGboost, RandomForest）
        2. 下拉选择预测目标（Electricity Demand, Electricity Price, Electricity Demand & Electricity Price）
        3. 点击按钮后先显示 "Running {model} for {target} (5 Years)...",
           再延迟几秒后显示对应的单张图片作为预测结果
        """
        self.predict_frame = tk.Frame(self.content_frame, bg="#f5f5f5")

        # 标题
        predict_label = tk.Label(self.predict_frame, text="Prediction Configuration",
                                 font=("Arial", 18, "bold"), bg="#f5f5f5")
        predict_label.pack(pady=10)

        # 配置框
        config_frame = ttk.Frame(self.predict_frame, padding=20, relief="ridge")
        config_frame.pack(pady=10)

        # Select Model
        ttk.Label(config_frame, text="Select Model:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.model_var = tk.StringVar()
        model_combo = ttk.Combobox(config_frame, textvariable=self.model_var,
                                   values=["ARIMA", "LightGBM", "XGboost", "RandomForest"],
                                   state='readonly', width=30)
        model_combo.grid(row=0, column=1, padx=10, pady=5)

        # Select Target
        ttk.Label(config_frame, text="Prediction Target:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.target_var = tk.StringVar()
        target_combo = ttk.Combobox(config_frame, textvariable=self.target_var,
                                    values=["Electricity Demand", "Electricity Price", 
                                            "Electricity Demand & Electricity Price"],
                                    state='readonly', width=30)
        target_combo.grid(row=1, column=1, padx=10, pady=5)

        # Run Prediction 按钮
        run_button = ttk.Button(config_frame, text="Run Prediction", command=self.run_prediction)
        run_button.grid(row=2, column=0, columnspan=2, pady=10)

        # 输出结果文本框（显示 "Running ..." 等提示信息）
        self.output_text = tk.Text(self.predict_frame, height=5, width=80, state="disabled")
        self.output_text.pack(pady=10)
        # ========== 2. 图片显示区域（仅显示一张预测结果图） ==========

        self.predict_canvas = tk.Canvas(self.predict_frame, bg="#ffffff", highlightthickness=0)
        self.predict_canvas.pack(side="left", fill="both", expand=True)

        self.predict_scrollbar = tk.Scrollbar(self.predict_frame, orient="vertical", command=self.predict_canvas.yview)
        self.predict_scrollbar.pack(side="right", fill="y")
        self.predict_canvas.configure(yscrollcommand=self.predict_scrollbar.set)

        # 创建Frame并放置在Canvas的中央
        self.predict_images_frame = tk.Frame(self.predict_canvas, bg="#ffffff")
        self.canvas_window = self.predict_canvas.create_window((0, 0), window=self.predict_images_frame, anchor="center")

        # 动态更新滚动区域并保持居中
        def on_predict_images_frame_configure(event):
            canvas_width = event.width
            frame_width = self.predict_images_frame.winfo_reqwidth()
            x_position = max((canvas_width - frame_width) // 2, 0)
            self.predict_canvas.coords(self.canvas_window, x_position, 0)
            self.predict_canvas.configure(scrollregion=self.predict_canvas.bbox("all"))

        def on_canvas_configure(event):
            canvas_width = event.width
            frame_width = self.predict_images_frame.winfo_reqwidth()
            x_position = max((canvas_width - frame_width) // 2, 0)
            self.predict_canvas.coords(self.canvas_window, x_position, 0)

        self.predict_images_frame.bind("<Configure>", on_predict_images_frame_configure)
        self.predict_canvas.bind("<Configure>", on_canvas_configure)



        # 鼠标滚轮事件绑定
        self.predict_canvas.bind_all("<MouseWheel>", self._on_mousewheel_predict)

        # ========== 模型-目标 与 文件名的映射表 ==========
        # 请确保与 ./predict 文件夹下的图片名匹配
        self.model_target_map = {
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

        self.predict_frame.pack(fill="both", expand=True)

    def _on_mousewheel_predict(self, event):
        """
        鼠标滚轮事件,用于Predict页面的Canvas滚动
        """
        self.predict_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def run_prediction(self):
        """
        点击 'Run Prediction' 后的逻辑：
        1. 显示 "Running ..." 提示
        2. 延迟若干秒后加载并显示对应图片
        """
        selected_model = self.model_var.get()
        selected_target = self.target_var.get()

        if not selected_model or not selected_target:
            messagebox.showerror("Error", "Please select Model and Target before running prediction.")
            return

        # 显示运行提示
        result_text = f"Running {selected_model} for {selected_target} (5 Years)...\nPrediction results will be displayed here."
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, result_text)
        self.output_text.config(state="disabled")

        # 延迟 2 秒后显示结果（模拟预测耗时）
        self.root.after(2000, lambda: self._show_single_prediction_image(selected_model, selected_target))

    def _show_single_prediction_image(self, model, target):
        """
        延迟后，加载并显示对应的单张图片，覆盖面板
        """
        # 清空预测图片区域
        for child in self.predict_images_frame.winfo_children():
            child.destroy()

        # 获取文件名
        filename = self.model_target_map.get((model, target), None)
        if not filename:
            tk.Label(self.predict_images_frame, text="No matching image found for this selection.",
                     fg="red", bg="#ffffff").pack(pady=10)
            return

        file_path = os.path.join("./predict", filename)
        if not os.path.exists(file_path):
            tk.Label(self.predict_images_frame, text=f"Image not found: {filename}",
                     fg="red", bg="#ffffff").pack(pady=10)
            return

        try:
            pil_img = Image.open(file_path)
            pil_img.thumbnail((900, 600))
            img_obj = ImageTk.PhotoImage(pil_img)

            # 保存引用以防被回收
            if not hasattr(self, 'single_prediction_image'):
                self.single_prediction_image = []
            self.single_prediction_image.clear()
            self.single_prediction_image.append(img_obj)

            tk.Label(self.predict_images_frame, image=img_obj, bg="#ffffff").pack(pady=10)
            desc = f"This is the predicted result of {model} for {target}."
            tk.Label(self.predict_images_frame, text=desc, font=("Arial", 12), bg="#ffffff").pack(pady=(0, 10))
        except Exception as e:
            tk.Label(self.predict_images_frame, text=f"Error loading image: {e}",
                     fg="red", bg="#ffffff").pack(pady=10)

    # ------------------Evaluation Page------------------
    def create_evaluation_page(self):
        """
        仅保留 "Model Evaluation" 标题，
        并在 /Evaluation 文件夹下以 2 列多行方式显示所有 .png 图片，可滚动查看。
        """
        self.evaluation_frame = tk.Frame(self.content_frame, bg="#f5f5f5")
    
        evaluation_label = tk.Label(self.evaluation_frame, text="Model Evaluation",
                                    font=("Arial", 16, "bold"), bg="#f5f5f5")
        evaluation_label.pack(pady=10)
    
        eval_images_canvas = tk.Canvas(self.evaluation_frame, bg="#ffffff", highlightthickness=0)
        eval_images_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        eval_scrollbar = tk.Scrollbar(self.evaluation_frame, orient="vertical", command=eval_images_canvas.yview)
        eval_scrollbar.pack(side="right", fill="y")
        eval_images_canvas.configure(yscrollcommand=eval_scrollbar.set)
    
        self.eval_images_frame = tk.Frame(eval_images_canvas, bg="#ffffff")
        eval_images_canvas.create_window((0, 0), window=self.eval_images_frame, anchor="nw")
    
        def on_eval_images_frame_configure(event):
            eval_images_canvas.configure(scrollregion=eval_images_canvas.bbox("all"))
        self.eval_images_frame.bind("<Configure>", on_eval_images_frame_configure)
    
        self.evaluation_frame.bind("<Enter>", lambda e: self.evaluation_frame.focus_set())
        self.evaluation_frame.bind("<MouseWheel>",
                                   lambda event: eval_images_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
    
        folder_path = "./Evaluation"
        self.loaded_images_eval = []
    
        if not os.path.exists(folder_path):
            tk.Label(self.eval_images_frame, text="Evaluation folder not found.", fg="red", bg="#ffffff").pack()
            return
    
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".png")]
        if not image_files:
            tk.Label(self.eval_images_frame, text="No images found.", fg="red", bg="#ffffff").pack()
            return
    
        for idx, img_file in enumerate(image_files):
            file_path = os.path.join(folder_path, img_file)
            title_text = os.path.splitext(img_file)[0]
    
            row = idx // 2
            col = idx % 2
    
            column_frame = tk.Frame(self.eval_images_frame, bg="#ffffff")
            column_frame.grid(row=row, column=col, padx=10, pady=10, sticky="n")
    
            tk.Label(column_frame, text=title_text, font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=(10, 2))
    
            try:
                pil_img = Image.open(file_path)
                pil_img.thumbnail((600, 450))
                img_obj = ImageTk.PhotoImage(pil_img)
                self.loaded_images_eval.append(img_obj)
    
                tk.Label(column_frame, image=img_obj, bg="#ffffff").pack(pady=5)
            except Exception as e:
                tk.Label(column_frame, text=f"Error loading {img_file}: {e}", fg="red", bg="#ffffff").pack()
    
            description_text = f"Description for {title_text}: This image illustrates the evaluation results and key performance indicators for the model."
            tk.Label(column_frame, text=description_text, font=("Arial", 12), bg="#ffffff",
                     wraplength=600, justify="left").pack(pady=(5, 10))
        
        self.evaluation_frame.pack(fill="both", expand=True)
    
    # ------------------页面切换------------------
    def show_page(self, page_name):
        if hasattr(self, 'home_frame'):
            self.home_frame.pack_forget()
        if hasattr(self, 'visualization_frame'):
            self.visualization_frame.pack_forget()
        if hasattr(self, 'predict_frame'):
            self.predict_frame.pack_forget()
        if hasattr(self, 'evaluation_frame'):
            self.evaluation_frame.pack_forget()
    
        if page_name == "Home":
            self.home_frame.pack(fill="both", expand=True)
        elif page_name == "Visualization":
            self.visualization_frame.pack(fill="both", expand=True)
        elif page_name == "Prediction":
            self.predict_frame.pack(fill="both", expand=True)
        elif page_name == "Evaluation":
            self.evaluation_frame.pack(fill="both", expand=True)
    
        self.current_page = page_name

# ------------------主程序入口------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = EnergyPredictionGUI(root)
    root.mainloop()
