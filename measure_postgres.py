import os
import json
import glob
import time
import psutil
import threading
import numpy as np
import psycopg2
from pymongo import MongoClient

conn = psycopg2.connect(
    "dbname=measure user=postgres password=mysecretpassword host=localhost port=5431")
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
    order_wh.append(c)

class Measure():
    def __init__(self, start_cpu, start_memory):
        self.start_cpu = start_cpu
        self.start_memory = start_memory
        self.total_time = None
        self.cpu = []
        self.memory = []
        self.is_stop = True

    def measure(self):
        self.is_stop = False
        while not self.is_stop:
            self.memory.append(psutil.virtual_memory().percent)
            self.cpu.append(psutil.cpu_percent(interval=0.1))
        return



time.sleep(10)
print('''
START MEASURE
===============
''')
start_cpu = psutil.cpu_percent()
start_memory = psutil.virtual_memory().percent
measure = Measure(start_cpu=start_cpu, start_memory=start_memory)
start_time = time.time()
t1 = threading.Thread(target=measure.measure)
t1.start()

# ======================
# Add your data function

# ======================

end_time = time.time()
measure.total_time = end_time - start_time
measure.is_stop = True

import matplotlib.pyplot as plt

# Turn interactive plotting off
plt.ioff()

measure.cpu = np.clip(np.array(measure.cpu) - measure.start_cpu, 0, 100)
measure.memory = np.clip(np.array(measure.memory) - measure.start_memory, 0,
                         100)
# Create a new figure, plot into it, then close it so it never gets displayed
fig = plt.figure()
plt.plot(measure.cpu)
plt.savefig('/home/thai0125nt/Desktop/rudder-sdk-python/mongo/cpu_insert.png')
plt.close(fig)

plt.figure()
plt.plot(measure.memory)
plt.savefig(
    '/home/thai0125nt/Desktop/rudder-sdk-python/mongo/memory_insert.png')
plt.close(fig)

output = {
    'cpu_average': np.average(measure.cpu),
    'memory_average': np.average(measure.memory),
    'total_time': measure.total_time
}

with open('/home/thai0125nt/Desktop/rudder-sdk-python/mongo/summary_insert.json', 'w') as json_file:
    json.dump(output, json_file)




time.sleep(10)
print('''
START MEASURE
===============
''')
start_cpu = psutil.cpu_percent()
start_memory = psutil.virtual_memory().percent
measure = Measure(start_cpu=start_cpu, start_memory=start_memory)
start_time = time.time()
t1 = threading.Thread(target=measure.measure)
t1.start()

# ======================
# Add your data function

# ======================

end_time = time.time()
measure.total_time = end_time - start_time
measure.is_stop = True

import matplotlib.pyplot as plt

# Turn interactive plotting off
plt.ioff()

measure.cpu = np.clip(np.array(measure.cpu) - measure.start_cpu, 0, 200)
measure.memory = np.clip(np.array(measure.memory) - measure.start_memory, 0,
                         200)
# Create a new figure, plot into it, then close it so it never gets displayed
fig = plt.figure()
plt.plot(measure.cpu)
plt.savefig('/home/thai0125nt/Desktop/rudder-sdk-python/mongo/cpu_join.png')
plt.close(fig)

plt.figure()
plt.plot(measure.memory)
plt.savefig(
    '/home/thai0125nt/Desktop/rudder-sdk-python/mongo/memory_join.png')
plt.close(fig)

output = {
    'cpu_average': np.average(measure.cpu),
    'memory_average': np.average(measure.memory),
    'total_time': measure.total_time
}

with open('/home/thai0125nt/Desktop/rudder-sdk-python/mongo/summary_join.json', 'w') as json_file:
    json.dump(output, json_file)

