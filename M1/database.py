import pymongo

class Database:
    def __init__(self,name,collection):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.database = self.client[name]
        self.collection = self.database[collection]


    def storeData(self,data):
        # collection = self.database[collection]
        print("Start storing")
        for d in data:
            result = self.collection.insert_one({"_id":d,"data":data[d] })
            print(result)        
        print("Finish storing")

    def findById(self,id):
        result = self.collection.find_one({"_id":id})
        return result

    def replaceById(self,id,document):
        self.collection.replace_one({"_id":id},{"_id":id,"data":document})
    
    def insertOne(self,id,document):
        result = self.collection.insert_one({"_id":id, "data":document})

    def updateOne(self,id,doc):
        update = {"$push": {"data.docs": doc}}
        collection.update_one({"_id":id}, update)
    

        
