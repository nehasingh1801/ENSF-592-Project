import webbrowser
import tkinter as tk

import folium


class draw_map():

    def draw(self, year, type, text, win):

        text.delete('1.0', tk.END)

        cord = [51.049999, -114.066666]
        run = 0

        # creating a base map
        # tileset represents the way data is displayed in the map
        # zoom_start tells the zoom_in size
        output_file = 'map.html'
        m = folium.Map(location = [51.049999, -114.066666], zoom_start=12)

        # folium.marker() plots the marker on the map at the given Location
        folium.Marker(location = cord, popup = 'Heavily Crowded', color = 'crimson', tooltip = "Click for more", fill = False).add_to(m)
        # saving the map in HTML file
        m.save(output_file)

        # display map on browser
        webbrowser.open(output_file, new=2)
        text.insert(tk.END, "Successfully written map")

