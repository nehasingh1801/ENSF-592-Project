'''
@author(s) Neha Singh, Sanyam, Taruneesh Sachdeva

This .py file has a class DbManagerNew which has a constructor for establishing the connection to 
the MongoDB database. The class has several functions which we'll use to read,sort,analyse and map the 
required data.
'''

#Importing the required packages
import pymongo
import csv

class DbManagerNew():
    
    #Constructor
    def __init__(self):
        client = pymongo.MongoClient("mongodb+srv://db_user1:lX7UMVmXXoypDNPK@cluster0.wzbtd.mongodb.net/admin?retryWrites=true&w=majority")
        global db
        db = client["calgary_traffic"]
        
    
    def ret_data(self,collection_type,year):
        '''ret_data() method takes in two parameters: collection_type and year. An empty list response is
        appended as the if-elif conditions are checked for three years 2016,2017 and 2018.
        It reads the data from the database and displays n rows pertaining to it. It returns the 
        response[] list.
        '''
        response = []
        #If the collection type selected by the user in the GUI is traffic volume.
        if(collection_type == "traffic_volume"):
            if(year == "2016"):
                for x in db.traffic_volume.find( { "year_vol": "2016" } ):
                    response.append(x)

            elif(year == "2017"):
                for x in db.traffic_volume.find( { "year": "2017" } ):
                    response.append(x)

            elif(year == "2018"):
                for x in db.traffic_volume.find( { "YEAR": "2018" } ):
                    response.append(x)

        #If the collection type selected by the user in the GUI is traffic incidents.
        elif(collection_type == "traffic_incidents"):
            for x in db.traffic_incidents.find( { "MODIFIED_DT": {'$regex': year}} ):
                response.append(x)
        
        #returns 41 rows
        return response[0:40]

    
    def sort_data(self,collection_type,year):
        '''sort_data() method is defined for sorting the data after reading it from the database.
        Depending on which year and collection type user selected, it'll return the response list 
        with n rows and sorting the data in descending order i.e. highest -> lowest
        '''
        response = []
        #If the collection type selected by the user in the GUI is traffic volume.
        if(collection_type == "traffic_volume"):
            if(year == "2016"):
                for x in db.traffic_volume.find({"year_vol": "2016" }).sort([("volume", -1)]).collation({"locale": "en_US", "numericOrdering": True}):
                    response.append(x)

            if(year == "2017"):
                for x in db.traffic_volume.find({"year": "2017" }).sort([("volume", -1)]).collation({"locale": "en_US", "numericOrdering": True}):
                    response.append(x)

            if(year == "2018"):
                for x in db.traffic_volume.find({"YEAR": "2018" }).sort([("VOLUME", -1)]).collation({"locale": "en_US", "numericOrdering": True}):
                    response.append(x)

        #If the collection type selected by the user in the GUI is traffic incidents.
        if(collection_type == "traffic_incidents"):
            res = []
            # stores sorted list
            new_res = [] 

            for x in db.traffic_incidents.aggregate( [ {'$match': {"START_DT": {'$regex': str(year)}}},{ '$group' : { '_id' : "$INCIDENT INFO", "count": { '$sum': 1 }} } ] ):
                #res.append(list(x.values())[1])
                res.append(x)

            #sorts the data in descending order
            new_res = sorted(res, key = lambda i: i['count'], reverse=True)
            num = 0
            for i in new_res:
                if(num == 10):
                    break
                key = list(i.values())[0]
                num +=1
                for x in db.traffic_incidents.find({"INCIDENT INFO": key ,"MODIFIED_DT": {'$regex': str(year)} }):
                    response.append(x)

        #returns the response list sliced to 43 rows
        return response[0:42]

    
    def data_analysis(self,collection_type):
        '''data_analysis() method accepts collection_type as a parameter. The purpose of this method is 
        to plot a line graph based on the year and collection type selected by the user in the Graphical
        User Interface. It returns an analysis_dict dictionary
        '''
        analysis_dict = {}
        #If the collection type selected by the user in GUI is traffic volume
        if(collection_type == "traffic_volume"):
            
            # running for year 2016
            max_val = 0
            for x in db.traffic_volume.aggregate([{ '$match': {"year_vol": "2016"}},{'$group' : {'_id': "$volume"}}]):
                #Type-casting to integer
                if ((int)(list(x.values())[0])) > max_val:
                    max_val = ((int)(list(x.values())[0]))   
            analysis_dict["2016"] = max_val

            # running for year 2017
            max_val = 0
            for x in db.traffic_volume.aggregate([{ '$match': {"year": "2017"}},{'$group' : {'_id': "$volume"}}]):
                if ((int)(list(x.values())[0])) > max_val:
                    max_val = ((int)(list(x.values())[0]))   
            analysis_dict["2017"] = max_val

            # running for year 2018
            max_val = 0
            for x in db.traffic_volume.aggregate([{ '$match': {"YEAR": "2018"}},{'$group' : {'_id': "$VOLUME"}}]):
                if ((int)(list(x.values())[0])) > max_val:
                    max_val = ((int)(list(x.values())[0]))   
            analysis_dict["2018"] = max_val

        #If the collection type selected by the user in GUI is traffic incidents
        elif(collection_type == "traffic_incidents"):
            for yr in range (2016, 2019, 1):
                res = []
                for x in db.traffic_incidents.aggregate( [ {'$match': {"START_DT": {'$regex': str(yr)}}},{ '$group' : { '_id' : "$INCIDENT INFO", "count": { '$sum': 1 }} } ] ):
                    res.append(list(x.values())[1])
                analysis_dict[yr] = (max(res))
                                      
        return analysis_dict
    
    
    def find_coordinates(self, collection_type, year):
        '''find_coordinates() method is used for displaying the map as an HTML file. It takes in 
        collection_type and year as parameters. This method calls the data_analysis method
        '''
        analysis_dict = self.data_analysis(collection_type)
        ls_loc = []
        loc_param = []
        latitude_list= []
        longitude_list= []
        final_list=[]
        max_value = 0
        
        #If the collection type selected by the user in the GUI is traffic volume
        if(collection_type == "traffic_volume"):
            if(year == "2016"):
                max_value = list(analysis_dict.values())[0]
                
                # finds data based on max volume from analysis_dict
                for x in db.traffic_volume.find({ "volume": str(max_value), "year_vol": "2016" } ):
                    ls_loc.append(x)

                # appends the location of sections based on max volume
                for ls in ls_loc:
                    loc_param.append(ls['the_geom'])

                # for locations in the loc_param list, creates the latitude and longitude list
                for i in range(len(loc_param)):
                    loc1 = (loc_param[i].replace("MULTILINESTRING ((","").split(',')[0]).split()
                    longitude_list.append(loc1[0]) 
                    latitude_list.append(loc1[1]) 

            if(year == "2017"):
                max_value = list(analysis_dict.values())[1]
                
                # finds data based on max volume from analysis_dict
                for x in db.traffic_volume.find({ "volume": str(max_value), "year": "2017" } ):
                    ls_loc.append(x)
                
                # appends the location of sections based on max volume
                for ls in ls_loc:
                    loc_param.append(ls['the_geom'])

                # for locations in the loc_param list, creates the latitude and longitude list
                for i in range(len(loc_param)):
                    loc1 = (loc_param[i].replace("MULTILINESTRING ((","").split(',')[0]).split()
                    longitude_list.append(loc1[0]) 
                    latitude_list.append(loc1[1]) 
                    
            if(year == "2018"):
                max_value = list(analysis_dict.values())[2]
                for x in db.traffic_volume.find({ "VOLUME": str(max_value), "YEAR": "2018" } ):
                    ls_loc.append(x)

                for ls in ls_loc:
                    loc_param.append(ls['multilinestring'])

                for i in range(len(loc_param)):
                    loc1 = (loc_param[i].replace("MULTILINESTRING ((","").split(',')[0]).split()
                    longitude_list.append(loc1[0]) 
                    latitude_list.append(loc1[1]) 

        #If the collection type selected by the user in the GUI is traffic incidents.
        if(collection_type == "traffic_incidents"):
            
            # gets the max values from analysis_dict based on year
            if(year == "2016"):
                max_value = list(analysis_dict.values())[0]

            elif(year == "2017"):
                max_value = list(analysis_dict.values())[1]

            elif(year == "2018"):
                max_value = list(analysis_dict.values())[2]

            
            #loc_param is defined a set for unique values
            res = []
            loc_param = set()
            loc_identity = ""

            # gets the count of sections 
            for x in db.traffic_incidents.aggregate( [ {'$match': {"START_DT": {'$regex': str(year)}}},{ '$group' : { '_id' : "$INCIDENT INFO", "count": { '$sum': 1 }} } ] ):
                res.append(x)
            
            # gets the location identity for max count
            for i in res:
                if((list(i.values())[1]) == max_value):
                    loc_identity = (list(i.values()))[0]

            # gets all the sections based on loc_identity from previous search 
            for x in db.traffic_incidents.find({ "INCIDENT INFO": loc_identity,"START_DT": {'$regex': str(year)} } ):
                ls_loc.append(x)

            for ls in ls_loc:
                loc_param.add((ls['location']).replace("(", "").replace(")", ""))
                
            list_new = list(loc_param)
            for i in range(len(list_new)):
                loc1 = (list_new[i].split(','))
                longitude_list.append(loc1[1]) 
                latitude_list.append(loc1[0])     

        #final list is appended with latitude_list and longitude list
        final_list.append(latitude_list)
        final_list.append(longitude_list)
        #returns the final list with appended latitude and longitude coordinates
        return final_list



   






