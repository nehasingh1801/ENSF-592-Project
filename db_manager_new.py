import pymongo
import csv

class DbManagerNew():
    
    def __init__(self):
        # if db_client is None:
        #     client = pymongo.MongoClient("mongodb+srv://db_user1:lX7UMVmXXoypDNPK@cluster0.wzbtd.mongodb.net/admin?retryWrites=true&w=majority")
        #     self.db_client = client["calgary_traffic"]
        # else:
        #     self.db_client = db_client
        #self.db = db
        client = pymongo.MongoClient("mongodb+srv://db_user1:lX7UMVmXXoypDNPK@cluster0.wzbtd.mongodb.net/admin?retryWrites=true&w=majority")
        global db
        db = client["calgary_traffic"]


    def ret_data(self,collection_type,year):
        response = []
        if(collection_type == "traffic_volume"):
            if(year == "2016"):
                print("2016")
                for x in db.traffic_volume.find( { "year_vol": "2016" } ):
                    response.append(x)

            elif(year == "2017"):
                print("2017")
                for x in db.traffic_volume.find( { "year": "2017" } ):
                    response.append(x)

            elif(year == "2018"):
                print("2018")
                for x in db.traffic_volume.find( { "YEAR": "2018" } ):
                    response.append(x)

        elif(collection_type == "traffic_incidents"):
            print("inside trff inc")
            for x in db.traffic_incidents.find( { "MODIFIED_DT": {'$regex': year}} ):
                response.append(x)
                print("inside trff inc find")
        
        return response[0:10]

    def sort_data(self,collection_type,year):
        response = []
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

        if(collection_type == "traffic_incidents"):
            res = []
            new_res = []

            for x in db.traffic_incidents.aggregate( [ {'$match': {"START_DT": {'$regex': str(year)}}},{ '$group' : { '_id' : "$INCIDENT INFO", "count": { '$sum': 1 }} } ] ):
                #res.append(list(x.values())[1])
                res.append(x)

            new_res = sorted(res, key = lambda i: i['count'], reverse=True)
            num = 0
            #print(new_res)
            for i in new_res:
                if(num == 10):
                    break
                key = list(i.values())[0]
                num +=1
                #print("in new_res for")
                #print(key)
                for x in db.traffic_incidents.find({"INCIDENT INFO": key ,"MODIFIED_DT": {'$regex': str(year)} }):
                    response.append(x)

        return response[0:15]


    def data_analysis(self,collection_type):
        print("level1")
        analysis_dict = {}
        if(collection_type == "traffic_volume"):
            
            # running for year 2016
            #for x in db.traffic_volume.aggregate( [ {'$match': {"year_vol": "2016"}},{ '$group' : { '_id' : "$year_vol","max_vol": { '$max' : "$volume" } } } ] ):
                #analysis_list.append((list(x.values())[1]))
            max_val = 0
            for x in db.traffic_volume.aggregate([{ '$match': {"year_vol": "2016"}},{'$group' : {'_id': "$volume"}}]):
                #print(list(x.values())[0])
                if ((int)(list(x.values())[0])) > max_val:
                    max_val = ((int)(list(x.values())[0]))   
            analysis_dict["2016"] = max_val

            # running for year 2017
            max_val = 0
            for x in db.traffic_volume.aggregate([{ '$match': {"year": "2017"}},{'$group' : {'_id': "$volume"}}]):
                #print(list(x.values())[0])
                if ((int)(list(x.values())[0])) > max_val:
                    max_val = ((int)(list(x.values())[0]))   
            analysis_dict["2017"] = max_val

            # running for year 2018
            max_val = 0
            for x in db.traffic_volume.aggregate([{ '$match': {"YEAR": "2018"}},{'$group' : {'_id': "$VOLUME"}}]):
                #print(list(x.values())[0])
                if ((int)(list(x.values())[0])) > max_val:
                    max_val = ((int)(list(x.values())[0]))   
            analysis_dict["2018"] = max_val

        elif(collection_type == "traffic_incidents"):
            for year in range (2016, 2019, 1):
                res = []
                for x in db.traffic_incidents.find({ "START_DT": {'$regex': str(year)} } ):
                    res.append(x)
                analysis_dict[year] = (len(res))
            print(analysis_dict)

            # # code for max incidents in a year
            # for year in range (2016, 2019, 1):
            #     res = []
            #     print("llevel3")
            #     for x in db.traffic_incidents.aggregate( [ {'$match': {"START_DT": {'$regex': str(year)}}},{ '$group' : { '_id' : "$INCIDENT INFO", "count": { '$sum': 1 }} } ] ):
            #         res.append(list(x.values())[1])
            #         #analysis_list.append(list(x.values())[1])
            #     analysis_dict[year] = (max(res))
            # print(analysis_dict)
            #         #max_value.append(x)
            # 


        return analysis_dict

    def find_coordinates(self, collection_type, year):
        analysis_dict = self.data_analysis(collection_type)
        ls_loc = []
        loc_param = []
        latitude_list= []
        longitude_list= []
        final_list=[]
        max_value = 0
        
        if(collection_type == "traffic_volume"):
            if(year == "2016"):
                max_value = list(analysis_dict.values())[0]
                
                for x in db.traffic_volume.find({ "volume": str(max_value), "year_vol": "2016" } ):
                    print("I am here")
                    ls_loc.append(x)
                #print(ls_loc)
                for ls in ls_loc:
                    loc_param.append(ls['the_geom'])
                #print(loc_param)
                for i in range(len(loc_param)):
                    loc1 = (loc_param[i].replace("MULTILINESTRING ((","").split(',')[0]).split()
                    #loc2 = (loc_param[1].replace("MULTILINESTRING ((","").split(',')[0]).split()
                    longitude_list.append(loc1[0]) #longitude
                    latitude_list.append(loc1[1]) #latitude
                    #print("i: ",i)

            if(year == "2017"):
                max_value = list(analysis_dict.values())[1]
                
                for x in db.traffic_volume.find({ "volume": str(max_value), "year": "2017" } ):
                    print("I am here")
                    ls_loc.append(x)
                #print(ls_loc)
                for ls in ls_loc:
                    loc_param.append(ls['the_geom'])
                #print(loc_param)
                for i in range(len(loc_param)):
                    loc1 = (loc_param[i].replace("MULTILINESTRING ((","").split(',')[0]).split()
                    #loc2 = (loc_param[1].replace("MULTILINESTRING ((","").split(',')[0]).split()
                    longitude_list.append(loc1[0]) #longitude
                    latitude_list.append(loc1[1]) #latitude
                    
            if(year == "2018"):
                max_value = list(analysis_dict.values())[2]
                #print(max_value)
                for x in db.traffic_volume.find({ "VOLUME": str(max_value), "YEAR": "2018" } ):
                    print("I am here")
                    ls_loc.append(x)
                #print(ls_loc)
                for ls in ls_loc:
                    loc_param.append(ls['multilinestring'])
                #print(loc_param)
                for i in range(len(loc_param)):
                    loc1 = (loc_param[i].replace("MULTILINESTRING ((","").split(',')[0]).split()
                    longitude_list.append(loc1[0]) #longitude
                    latitude_list.append(loc1[1]) #latitude

        if(collection_type == "traffic_incidents"):
            print("inside traffic_incidents analysis part")

            for yr in range (2016, 2019, 1):
                response = []
                print("llevel3")
                for x in db.traffic_incidents.aggregate( [ {'$match': {"START_DT": {'$regex': str(yr)}}},{ '$group' : { '_id' : "$INCIDENT INFO", "count": { '$sum': 1 }} } ] ):
                    response.append(list(x.values())[1])
                analysis_dict[yr] = (max(response))
            print("analysis_dict for incidents",analysis_dict)
            # analysis_dict for incidents {2016: 8, 2017: 32, 2018: 40}

            if(str(year) == "2016"):
                max_value = list(analysis_dict.values())[0]
                print("max_value 2016:",max_value)

            elif(str(year) == "2017"):
                max_value = list(analysis_dict.values())[1]
                print("max_value",max_value)

            elif(str(year) == "2018"):
                max_value = list(analysis_dict.values())[2]
                print("max_value",max_value)

            res = []
            loc_param = set()
            loc_identity = ""
            
            

            for x in db.traffic_incidents.aggregate( [ {'$match': {"START_DT": {'$regex': str(year)}}},{ '$group' : { '_id' : "$INCIDENT INFO", "count": { '$sum': 1 }} } ] ):
                #res.append(list(x.values())[1])
                res.append(x)

            #print(res)
            for i in res:
                if((list(i.values())[1]) == max_value):
                    loc_identity = (list(i.values()))[0]
            #print(loc_identity)
            for x in db.traffic_incidents.find({ "INCIDENT INFO": loc_identity,"START_DT": {'$regex': str(year)} } ):
                ls_loc.append(x)
                #print(x)
            #print(ls_loc)
            for ls in ls_loc:
                #loc_param.append(ls['location'])
                #loc_param.add(ls['location'])
                loc_param.add((ls['location']).replace("(", "").replace(")", ""))
            #print(loc_param)
            list_new = list(loc_param)
            #print(list_new)
            for i in range(len(list_new)):
                loc1 = (list_new[i].split(','))
                print(loc1)
                longitude_list.append(loc1[1]) #longitude
                latitude_list.append(loc1[0]) #latitude
                #print("i: ",i)    

        final_list.append(latitude_list)
        final_list.append(longitude_list)
        print("final_list from db manager: ",final_list)
        return final_list



   






