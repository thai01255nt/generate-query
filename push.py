from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
# cloud = MongoClient("mongodb+srv://root:root_password@mongothai.mcbsw.mongodb.net/measure?retryWrites=true&w=majority")

db_measure = client.dbMeasure
# cloud_measure = cloud.dbMeasure
cursor = db_measure.rawProfile.find({})
data = []
for c in cursor:
    data.append(c)