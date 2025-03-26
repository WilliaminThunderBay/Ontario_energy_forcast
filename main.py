import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ------------------数据加载函数------------------
def load_data(file_path):
    """根据需要读取CSV并返回DataFrame，这里仅作示例。"""
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"读取数据失败: {e}")
        return None
    return df

class EnergyPredictionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ontario Energy Demand System")
        self.root.state('zoomed')
        self.df = load_data('data.csv')
        self.top_frame = tk.Frame(root, bg="#000000", height=200)
        self.top_frame.pack(fill="x", side="top")

        try:
            self.icon_image = Image.open("1.png").resize((160, 60))
            self.icon = ImageTk.PhotoImage(self.icon_image)
            self.icon_label = tk.Label(self.top_frame, image=self.icon, bg="#000000")
            self.icon_label.pack(side="left", padx=20)
        except Exception:
            print("Warning: icon image not found.")

        self.menu_icon = None
        self.close_icon = None
        try:
            menu_img = Image.open("2.png").resize((160, 60))
            self.menu_icon = ImageTk.PhotoImage(menu_img)
            close_img = Image.open("3.png").resize((160, 60))
            self.close_icon = ImageTk.PhotoImage(close_img)
        except Exception as e:
            print(f"Warning: menu/close icon not found: {e}")
        
        self.right_icon_label = tk.Label(self.top_frame, bg="#000000", cursor="hand2")
        self.right_icon_label.pack(side="right", padx=20)
        if self.menu_icon:
            self.right_icon_label.config(image=self.menu_icon)
        
        self.right_icon_label.bind("<Button-1>", self.toggle_dropdown_menu)
        self.menu_visible = False
        self.green_bar = tk.Frame(root, bg="#006A4D", height=100)
        self.green_bar.pack(fill="x", side="top")
        self.green_label = tk.Label(self.green_bar, text="Ontario Energy Forecasting",
                                    fg="white", bg="#006A4D", font=("Arial", 14, "bold"))
        self.green_label.pack(side="left", padx=20, pady=5)

        self.dropdown_frame = tk.Frame(self.root, bg="white", relief="solid", borderwidth=2)
        self.dropdown_buttons = []
        options = ["Home", "Visualization", "Predict", "Evaluation"]
        for option in options:
            btn = tk.Button(self.dropdown_frame, text=option, anchor="w", relief="flat", 
                            bg="white", fg="black", width=20, height=2, font=("Arial", 10),
                            command=lambda opt=option: self.handle_menu_selection(opt))
            btn.pack(fill="x", padx=10, pady=5)
            self.dropdown_buttons.append(btn)
        self.root.bind("<Button-1>", self.close_menu_if_outside)

        self.content_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.content_frame.pack(fill="both", expand=True)
        
        self.create_home_page()
        self.create_visualization_page()
        self.create_predict_page()
        self.create_evaluation_page()
        
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
##Home page
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

    def create_visualization_page(self):
        import os
        from PIL import Image, ImageTk
        import tkinter as tk

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

        self.loaded_images = []

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

            tk.Label(column_frame, text=title_text, font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=(10, 2))

            try:
                pil_img = Image.open(file_path)
                pil_img.thumbnail((600, 450))
                img_obj = ImageTk.PhotoImage(pil_img)
                self.loaded_images.append(img_obj)

                tk.Label(column_frame, image=img_obj, bg="#ffffff").pack(pady=5)

                description = descriptions.get(img_file, "No description available.")
                tk.Label(column_frame, text=description, font=("Arial", 12), bg="#ffffff", wraplength=550, justify="left").pack(pady=(0, 15))

            except Exception as e:
                tk.Label(column_frame, text=f"Error loading {img_file}: {e}", fg="red", bg="#ffffff").pack()

    def create_evaluation_page(self):
        self.evaluation_frame = tk.Frame(self.content_frame, bg="#f5f5f5")
        evaluation_label = tk.Label(self.evaluation_frame, text="Model Evaluation",
                                    font=("Arial", 16, "bold"), bg="#f5f5f5")
        evaluation_label.pack(pady=10)

        eval_config_frame = ttk.Frame(self.evaluation_frame, padding=20, relief="ridge")
        eval_config_frame.pack(pady=10)
        
        ttk.Label(eval_config_frame, text="Select Model:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        eval_model_var = tk.StringVar()
        eval_model_combo = ttk.Combobox(eval_config_frame, textvariable=eval_model_var,
                                        values=["ARIMA", "XGBoost", "LSTM", "Ensemble"],
                                        state='readonly', width=30)
        eval_model_combo.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(eval_config_frame, text="Evaluation Metric:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        metric_var = tk.StringVar()
        metric_combo = ttk.Combobox(eval_config_frame, textvariable=metric_var,
                                    values=["RMSE", "MAE", "MAPE", "All Metrics"],
                                    state='readonly', width=30)
        metric_combo.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(eval_config_frame, text="Test Period:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        test_period_var = tk.StringVar()
        test_period_combo = ttk.Combobox(eval_config_frame, textvariable=test_period_var,
                                         values=["Last 3 Months", "Last 6 Months", "Last Year"],
                                         state='readonly', width=30)
        test_period_combo.grid(row=2, column=1, padx=10, pady=5)

        evaluate_button = ttk.Button(eval_config_frame, text="Run Evaluation",
                                     command=lambda: messagebox.showinfo("Info", "Evaluation logic not implemented."))
        evaluate_button.grid(row=3, column=0, columnspan=2, pady=10)

        eval_result_frame = ttk.Frame(self.evaluation_frame, padding=10)
        eval_result_frame.pack(pady=10, fill="both", expand=True)
        eval_result_label = ttk.Label(eval_result_frame, text="Evaluation Results:")
        eval_result_label.pack(anchor="w")
        eval_output = tk.Text(eval_result_frame, height=10, width=80, state="disabled")
        eval_output.pack(pady=5, fill="both", expand=True)

    # ------------------页面切换------------------
    def show_page(self, page_name):
        # 隐藏所有页面
        if hasattr(self, 'home_frame'):
            self.home_frame.pack_forget()
        if hasattr(self, 'visualization_frame'):
            self.visualization_frame.pack_forget()
        if hasattr(self, 'predict_frame'):
            self.predict_frame.pack_forget()
        if hasattr(self, 'evaluation_frame'):
            self.evaluation_frame.pack_forget()
        
        # 根据页面名称展示对应frame
        if page_name == "Home":
            self.home_frame.pack(fill="both", expand=True)
        elif page_name == "Visualization":
            self.visualization_frame.pack(fill="both", expand=True)
        elif page_name == "Predict":
            self.predict_frame.pack(fill="both", expand=True)
        elif page_name == "Evaluation":
            self.evaluation_frame.pack(fill="both", expand=True)

        self.current_page = page_name

    # ------------------Predict逻辑------------------
    def run_prediction(self):
        selected_model = self.model_var.get()
        selected_target = self.target_var.get()
        selected_duration = self.duration_var.get()
        if not selected_model or not selected_target or not selected_duration:
            messagebox.showerror("Error", "Please select all options before running prediction.")
            return
        result_text = (f"Running {selected_model} for {selected_target} ({selected_duration})...\n"
                       "Prediction logic not implemented in this demo.")
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, result_text)
        self.output_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = EnergyPredictionGUI(root)
    root.mainloop()
