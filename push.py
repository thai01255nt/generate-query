from pymongo import MongoClient
from load_data import load_data


raw_order,order_wh,profile_wh = load_data()

cloud = MongoClient("mongodb+srv://root:root_password@mongothai.mcbsw.mongodb.net/measure?retryWrites=true&w=majority")
cloud_measure = cloud.dbMeasure

try:
    cloud_measure.rawOrder.insert_many(raw_order)
except:
    pass
try:
    cloud_measure.orderWH.insert_many(order_wh)
except:
    pass
try:
    cloud_measure.profileWH.insert_many(profile_wh)
except:
    pass