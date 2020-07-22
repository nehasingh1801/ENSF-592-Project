'''
@author(s) Neha Singh, Sanyam, Taruneesh Sachdeva

This .py file has a class draw_map and imports the db_manager_new class.
'''

import webbrowser
import tkinter as tk
from db_manager_new import DbManagerNew

import folium

'''
draw_map class saves the map in .html file and displays it on the web browser
'''
class draw_map():

    def draw(self, year, type, text, win, obj):
        '''method receives the coordinates as arguments and displays it on the map.
        '''

        text.delete('1.0', tk.END)
        if((year == 0) or (type == "")):
            text.insert(tk.END, "OOOps!! Please select valid type and year.")
        else:
            
            # creating a base map
            # tileset represents the way data is displayed in the map
            # zoom_start tells the zoom_in size
            output_file = 'map.html'

            # displays the map of Calgary city
            m = folium.Map(location = [51.049999, -114.066666], zoom_start=10)

            # calls the find_coordinates method from db_manager class
            # returns the corresponding coordinates
            final_list = obj.find_coordinates(type,year)

            lat_lst = final_list[0]
            lng_lst = final_list[1]

            name = []
            for i in range(len(lat_lst)):
                name.append("Location: "+str(i+1))
                
            feature_group = folium.FeatureGroup("Locations")

            # adds all the coordinates to the map
            for lat, lng, name in zip(lat_lst, lng_lst, name):
                feature_group.add_child(folium.Marker(location=[lat,lng],popup=name))

            m.add_child(feature_group)

            # folium.marker() plots the marker on the map at the given Location
            # saving the map in HTML file
            m.save(output_file)

            # display map on browser
            webbrowser.open(output_file, new=2)

            # displays in the checkbox if map is written successfully
            text.insert(tk.END, "Successfully written map")

