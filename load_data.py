import pymongo
import csv

# Function to parse csv to dictionary
def load_data(filename,col_name):
    with open(filename,'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            #print(line)
            col_name.insert_one(line)

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb+srv://db_user1:lX7UMVmXXoypDNPK@cluster0.wzbtd.mongodb.net/admin?retryWrites=true&w=majority")
    db = client["calgary_traffic"]
    f1 = (r'C:\Users\nehas\OneDrive\Documents\ENSF-592\Project\Traffic_Volumes_for_2018.csv')
    f2 = (r'C:\Users\nehas\OneDrive\Documents\ENSF-592\Project\2017_Traffic_Volume_Flow.csv')
    f3 = (r'C:\Users\nehas\OneDrive\Documents\ENSF-592\Project\TrafficFlow2016_OpenData.csv')

    f4 = (r'C:\Users\nehas\OneDrive\Documents\ENSF-592\Project\Traffic_Incidents_Archive_2017.csv')
    f5 = (r'C:\Users\nehas\OneDrive\Documents\ENSF-592\Project\Traffic_Incidents_Archive_2016.csv')
    f6 = (r'C:\Users\nehas\OneDrive\Documents\ENSF-592\Project\Traffic_Incidents.csv')

    vol_file_list = [f1,f2, f3]
    incidents_file_list = [f4, f5, f6]
    
    #collection_name  = db["traffic_incidents", { collation: { locale: 'en_US', strength: 2 } }]
    
    print(client.list_database_names())
    print(db.list_collection_names())

    for file in vol_file_list:
        #load_data(file,db.traffic_volume)
        print("hello")

    for file in incidents_file_list:
        load_data(file,db.traffic_incidents)
        print("nice")

    # Removes the specified collection from the database.
    #db.col_name.drop()    
    # 	Deletes documents from a collection.
    #db.traffic_volume.remove()