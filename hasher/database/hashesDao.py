from hasher.database.MongoConnection import MongoConnection

class hashesDao(MongoConnection):

    def __init__(self):
        super(hashesDao, self).__init__()
        self.get_collection("hashes")
    
    def getHashValue(self, hashValue):
        result = self.collection.find_one({"hash" : hashValue})
        return result
    
    def addUrlId(self, urlData , urlId):
        result = self.collection.update_one(
                {
                    "urlId" : urlId
                },
                {
                    "$set" : urlData
                },
                upsert = True)
        
        return result.acknowledged
    
    def getOriginalUrl(self, urlId):
        result = self.collection.find_one({"urlId" : urlId})
        return result
    
   
  