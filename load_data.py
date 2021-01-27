import os
import json
import glob
import time
import psutil
import threading
import numpy as np
from pymongo import MongoClient


def load_data():
    client = MongoClient("mongodb://127.0.0.1:27017")

    db_measure = client.dbMeasure
    # Load data
    cursor = db_measure.rawProfile.find({})
    raw_profile = []
    for c in cursor:
        c.pop('_id')
        raw_profile.append(c)

    raw_order = []
    cursor = db_measure.rawOrder.find({})
    for c in cursor:
        c.pop('_id')
        raw_order.append(c)

    profile_wh = []
    cursor = db_measure.profileWH.find({})
    for c in cursor:
        c.pop('_id')
        profile_wh.append(c)

    order_wh = []
    cursor = db_measure.orderWH.find({})
    for c in cursor:
        c.pop('_id')
        if 'cdpId' not in c.keys():
            c['cdpId'] = 1
        order_wh.append(c)
    return raw_profile, raw_order, profile_wh, order_wh
