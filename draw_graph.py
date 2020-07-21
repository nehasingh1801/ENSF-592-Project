import matplotlib 

# Specifying the backend "TkAgg" to be used with Matplotlib
matplotlib.use("TKAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from db_manager_new import DbManagerNew


import tkinter as tk

class draw_graph():
    def draw(self,  win, text,  type,obj):
        text.delete('1.0', tk.END)
        if(type == ""):
            text.insert(tk.END, "OOOps!! Please select valid type.")
        else:
            canvas = tk.Canvas(win)
            canvas.grid(row=0, column=1, sticky="nsew")
            # creating an instance of Figure and setting its size
            # dpi - dots per inches (determines pixels)
            f = Figure(figsize=(5, 5), dpi=100)

            # These are subplot grid parameters encoded as a single integer.
            # For example, "221" means two wide and two tall grid
            a = f.add_subplot(221)
            if(type == "traffic_volume"):
                a.set_ylabel('Max Volume')
            elif(type == "traffic_incidents"):
                a.set_ylabel('Number of accidents')

            a.set_xlabel('Year')


            # calling data_analysis method
            print("type: ", type)
            analysis_dict = obj.data_analysis(type)
            print("analysis_dict: ",analysis_dict)
            year_list = list(analysis_dict.keys())
            print("year_list: ",year_list)
            data_list = list(analysis_dict.values())
            print("data_list: ",data_list)
            a.plot(year_list, data_list)

            # creating a canvas for the display
            canvas1 = FigureCanvasTkAgg(f, master= canvas)
            canvas1.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
            text.insert(tk.END, "Graph is displayed successfully.")

