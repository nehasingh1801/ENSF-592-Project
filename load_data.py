'''
@author(s) Neha Singh, Sanyam, Taruneesh Sachdeva

'''
import pymongo
import csv


def load_data(filename,col_name):
    '''function load_data() is used to parse csv to dictionary
    '''
    with open(filename,'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            col_name.insert_one(line)

# create DB
def create_db(db_name, db_var_name):
    db_var_name = client[db_name]

# Removes the specified collection from the database.
def drop_collection(collection_name):
    db[collection_name].drop() 
# 	Deletes documents from a collection.
    #db.traffic_volume.remove()

# create collection
# def create_collect(db_name, collection_name):
#     db_name.createCollection(collection_name)


if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb+srv://db_user1:lX7UMVmXXoypDNPK@cluster0.wzbtd.mongodb.net/admin?retryWrites=true&w=majority")
    
    f1 = (r'C:\Users\nehas\OneDrive\Documents\ENSF-592\Project\Traffic_Volumes_for_2018.csv')
    f2 = (r'C:\Users\nehas\OneDrive\Documents\ENSF-592\Project\2017_Traffic_Volume_Flow.csv')
    f3 = (r'C:\Users\nehas\OneDrive\Documents\ENSF-592\Project\TrafficFlow2016_OpenData.csv')

    f4 = (r'C:\Users\nehas\OneDrive\Documents\ENSF-592\Project\Traffic_Incidents_Archive_2017.csv')
    f5 = (r'C:\Users\nehas\OneDrive\Documents\ENSF-592\Project\Traffic_Incidents_Archive_2016.csv')
    f6 = (r'C:\Users\nehas\OneDrive\Documents\ENSF-592\Project\Traffic_Incidents.csv')

    vol_file_list = [f1,f2, f3]
    incidents_file_list = [f4, f5, f6]
    
    # for file in vol_file_list:
    #     load_data(file,db.traffic_volume)
        

    # for file in incidents_file_list:
    #     load_data(file,db.traffic_incidents)
        
    #craete DB
    print("Creating DB....")
    #create_db("calgary_traffic", "db" )
    db = client["calgary_traffic"]
    print(client.list_database_names())

    # create collections
    print("Creating Collection....")
    my_coll = db["my_collection"]
   
    # load data
    print("loading data....")
    load_data(f5,db.my_collection)

    # drop collection
    print("dropping collection: my_collection")
    #drop_collection("my_collection")





