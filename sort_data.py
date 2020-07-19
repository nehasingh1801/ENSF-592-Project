import tkinter as tk

class sort_data():
    def sort(self, win,year, type):
        print("I am sorting", year, type)
        canvas = tk.Text(win)
        canvas.grid(row=0, column=1, sticky="nsew")
