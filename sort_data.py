from tkinter import *
import tkinter as tk
from db_manager_new import DbManagerNew


class sort_data():
    def sort(self, win,text, year, type, obj):
        text.delete('1.0', tk.END)
        if((year == 0) or (type == "")):
            text.insert(tk.END, "OOOps!! Please select valid type and year.")
        else:
            print("I am reading, year, type")
            list1 = obj.sort_data(type, year)


            total_rows = len(list1)
            header = list(list1[0].keys())
            total_columns = len(list1[0])

            canvas = tk.Canvas(win)
            canvas.grid(row=0, column=1, sticky="nsew")

            # printing header
            for i in range(1,len(header)):
                self.e = Entry(canvas, width=25, fg='blue', font=('Arial', 10))
                self.e.grid(row=0, column=i-1)
                self.e.insert(END, header[i])

            # code for creating table
            for i in range(total_rows):
                for j in range(1, total_columns):
                    self.e = Entry(canvas, width=25, fg='blue',font=('Arial', 10))
                    self.e.grid(row=i+1, column=j-1)
                    self.e.insert(END, list(list1[i].values())[j])

            text.insert(tk.END, "Data is sorted successfully.")

