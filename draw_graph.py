'''
@author(s) Neha Singh, Sanyam, Taruneesh Sachdeva

This .py file has a class draw_graph and uses the db_manager_new class .
'''

import matplotlib 

# Specifying the backend "TkAgg" to be used with Matplotlib
matplotlib.use("TKAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from db_manager_new import DbManagerNew

import tkinter as tk


class draw_graph():
    '''draw_graph displays the data as line graph for specified type for years 2016-2017-2018.
    '''
    def draw(self,  win, text,  type,obj):

        # clears the displayed status text
        text.delete('1.0', tk.END)

        #if year or collection type is invalid
        if(type == ""):
            text.insert(tk.END, "Please select valid type.")
        else:
            canvas = tk.Canvas(win)
            canvas.grid(row=0, column=1, sticky="nsew")

            # creating an instance of Figure and setting its size
            # dpi - dots per inches (determines pixels)
            f = Figure(figsize=(5, 5), dpi=100)

            # These are subplot grid parameters encoded as a single integer.
            # For example, "221" means two wide and two tall grid
            a = f.add_subplot(221)

            # labeling x,y axis
            if(type == "traffic_volume"):
                a.set_ylabel('Max Volume')
                a.set_title("Graph displaying maximum traffic volume for each year")
            elif(type == "traffic_incidents"):
                a.set_ylabel('Number of accidents')
                a.set_title("Graph displaying maximum incidents for each year")

            a.set_xlabel('Year')


            # calling data_analysis method
            # returns the max volume and incidents for 2018, 2017, 2016
            analysis_dict = obj.data_analysis(type)
            year_list = list(analysis_dict.keys())
            data_list = list(analysis_dict.values())

            a.plot(year_list, data_list)

            # creating a canvas for the display
            canvas1 = FigureCanvasTkAgg(f, master= canvas)
            canvas1.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

            #updates the status text
            text.insert(tk.END, "Graph is displayed successfully.")

