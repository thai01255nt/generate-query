import json
import time
import psutil
import threading
import numpy as np
import psycopg2
from load_data import load_data
from postgres import generate_insert_query, generate_join_query

TYPE_DB = 'postgres'
conn = psycopg2.connect(
    "dbname=measure user=postgres password=mysecretpassword host=localhost port=5431")
cur = conn.cursor()
raw_profile, raw_order, profile_wh, order_wh = load_data()

insert_raw_order_query, insert_order_wh_query, insert_profile_wh_query = \
    generate_insert_query(raw_order=raw_order, order_wh=order_wh,
                          profile_wh=profile_wh)
join_query = generate_join_query()


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
cur.execute(insert_raw_order_query)
conn.commit()
cur.execute(insert_order_wh_query)
conn.commit()
cur.execute(insert_profile_wh_query)
conn.commit()
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
plt.savefig(f'/home/thai0125nt/Desktop/rudder-sdk-python/{TYPE_DB}/cpu_insert.png')
plt.close(fig)

plt.figure()
plt.plot(measure.memory)
plt.savefig(
    f'/home/thai0125nt/Desktop/rudder-sdk-python/{TYPE_DB}/memory_insert.png')
plt.close(fig)

output = {
    'cpu_average': np.average(measure.cpu),
    'memory_average': np.average(measure.memory),
    'total_time': measure.total_time
}

with open(
        f'/home/thai0125nt/Desktop/rudder-sdk-python/{TYPE_DB}/summary_insert.json',
        'w') as json_file:
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
cur.execute(join_query)
conn.commit()
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
plt.savefig(f'/home/thai0125nt/Desktop/rudder-sdk-python/{TYPE_DB}/cpu_join.png')
plt.close(fig)

plt.figure()
plt.plot(measure.memory)
plt.savefig(
    f'/home/thai0125nt/Desktop/rudder-sdk-python/{TYPE_DB}/memory_join.png')
plt.close(fig)

output = {
    'cpu_average': np.average(measure.cpu),
    'memory_average': np.average(measure.memory),
    'total_time': measure.total_time
}

with open(f'/home/thai0125nt/Desktop/rudder-sdk-python/{TYPE_DB}/summary_join.json',
          'w') as json_file:
    json.dump(output, json_file)
