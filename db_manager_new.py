from db_manager import DbManager
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

    def data_analysis(self,collection_type):
        print("level1")
        analysis_dict = {}
        if(collection_type == "traffic_volume"):
            
            # running for year 2016
            #for x in db.traffic_volume.aggregate( [ {'$match': {"year_vol": "2016"}},{ '$group' : { '_id' : "$year_vol","max_vol": { '$max' : "$volume" } } } ] ):
                #analysis_list.append((list(x.values())[1]))
            max = 0
            for x in db.traffic_volume.aggregate([{ '$match': {"year_vol": "2016"}},{'$group' : {'_id': "$volume"}}]):
                #print(list(x.values())[0])
                if ((int)(list(x.values())[0])) > max:
                    max = ((int)(list(x.values())[0]))   
            analysis_dict["2016"] = max

            # running for year 2017
            max = 0
            for x in db.traffic_volume.aggregate([{ '$match': {"year": "2017"}},{'$group' : {'_id': "$volume"}}]):
                #print(list(x.values())[0])
                if ((int)(list(x.values())[0])) > max:
                    max = ((int)(list(x.values())[0]))   
            analysis_dict["2017"] = max

            # running for year 2018
            max = 0
            for x in db.traffic_volume.aggregate([{ '$match': {"YEAR": "2018"}},{'$group' : {'_id': "$VOLUME"}}]):
                #print(list(x.values())[0])
                if ((int)(list(x.values())[0])) > max:
                    max = ((int)(list(x.values())[0]))   
            analysis_dict["2018"] = max

        elif(collection_type == "traffic_incidents"):
            print("llevel2")
            
            for year in range (2016, 2019, 1):
                res = []
                print("llevel3")
                for x in db.traffic_incidents.aggregate( [ {'$match': {"START_DT": {'$regex': str(year)}}},{ '$group' : { '_id' : "$INCIDENT INFO", "count": { '$sum': 1 }} } ] ):
                    res.append(list(x.values())[1])
                    #analysis_list.append(list(x.values())[1])
                analysis_dict[year] = (max(res))
            print(analysis_dict)
                    #max_value.append(x)  

        return analysis_dict 

   






