import pymongo

import pymongo

class Database:
    def __init__(self,client,database_name):
        self.client = pymongo.MongoClient(client)
        self.database = self.client[database_name]


    def storeData(self,collection_name,data):
        collection = self.database[collection_name]
        for d in data:
            result = collection.insert_one({"_id":d,"data":data[d] })

    def findById(self,collection_name,id):
        collection = self.database[collection_name]
        result = collection.find_one({"_id":id})
        return result

    def replaceById(self,collection_name,id,document):
        collection = self.database[collection_name]
        collection.replace_one({"_id":id},document)
    
    def insertOne(self,collection_name,document):
        collection = self.database[collection_name]
        result = collection.insert_one(document)