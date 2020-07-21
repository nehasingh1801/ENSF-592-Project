import webbrowser
import tkinter as tk
from db_manager_new import DbManagerNew

import folium


class draw_map():

    def draw(self, year, type, text, win, obj):

        text.delete('1.0', tk.END)
        if((year == 0) or (type == "")):
            text.insert(tk.END, "OOOps!! Please select valid type and year.")
        else:

            # cord = [51.049999, -114.066666]
            # run = 0

            # creating a base map
            # tileset represents the way data is displayed in the map
            # zoom_start tells the zoom_in size
            output_file = 'map.html'
            m = folium.Map(location = [51.049999, -114.066666], zoom_start=10)
            final_list = obj.find_coordinates(type,year)
            # lat_lst = [50.9007203471, 51.0485664617, 51.0485461436]
            # lng_lst = [-114.0701479559,  -114.0691867156,  -114.0683208229]
            lat_lst = final_list[0]
            print("lat list: ", lat_lst)
            lng_lst = final_list[1]
            print("long list: ", lng_lst)
            name = []
            for i in range(len(lat_lst)):
                name.append("Location: "+str(i+1))
                
            print("name: ", name)
            print("final_list in draw graph: ", final_list)
            #name = ["first", "Second", "third"]
            feature_group = folium.FeatureGroup("Locations")

            for lat, lng, name in zip(lat_lst, lng_lst, name):
                feature_group.add_child(folium.Marker(location=[lat,lng],popup=name))

            m .add_child(feature_group)


            # folium.marker() plots the marker on the map at the given Location
            # folium.Marker(location = cord, popup = 'Heavily Crowded', color = 'crimson', tooltip = "Click for more", fill = False).add_to(m)
            # saving the map in HTML file
            m.save(output_file)

            # display map on browser
            webbrowser.open(output_file, new=2)
            text.insert(tk.END, "Successfully written map")

