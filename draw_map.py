'''
@author(s) Neha Singh, Sanyam, Taruneesh Sachdeva

This .py file has a class draw_map and uses the db_manager_new class.
'''

#importing webbrowser for opening the map as .html file in any online browser
import webbrowser
#importing tkinter for GUI
import tkinter as tk
#importing the DbManagerNew class
from db_manager_new import DbManagerNew

#importing folium for drawing map
import folium

'''
draw_map class has a draw method() which accepts five parameters. The required map will
open in a web browser
'''
class draw_map():

    def draw(self, year, type, text, win, obj):

        text.delete('1.0', tk.END)
        if((year == 0) or (type == "")):
            text.insert(tk.END, "OOOps!! Please select valid type and year.")
        else:
            
            # creating a base map
            # tileset represents the way data is displayed in the map
            # zoom_start tells the zoom_in size
            output_file = 'map.html'
            m = folium.Map(location = [51.049999, -114.066666], zoom_start=10)
            final_list = obj.find_coordinates(type,year)
            lat_lst = final_list[0]
            print("lat list: ", lat_lst)
            lng_lst = final_list[1]
            print("long list: ", lng_lst)
            name = []
            for i in range(len(lat_lst)):
                name.append("Location: "+str(i+1))
                
            print("name: ", name)
            print("final_list in draw graph: ", final_list)
            feature_group = folium.FeatureGroup("Locations")

            for lat, lng, name in zip(lat_lst, lng_lst, name):
                feature_group.add_child(folium.Marker(location=[lat,lng],popup=name))

            m .add_child(feature_group)

            # folium.marker() plots the marker on the map at the given Location
            # saving the map in HTML file
            m.save(output_file)

            # display map on browser
            webbrowser.open(output_file, new=2)
            #displays in the checkbox if map is written successfully
            text.insert(tk.END, "Successfully written map")

