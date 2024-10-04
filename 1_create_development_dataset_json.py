import numpy as np
import json

new_folder = 'extracted_data/'
data = np.load(new_folder + 'development_dataset.npy', allow_pickle=True).item()

user_list = [str(x) for x in range(51)]
session_list = [x for x in range(4)]
task_list = ['keystroke', 'readtext', 'gallery', 'tap']
sensor_list = ['sensor_acc', 'sensor_grav', 'sensor_gyro', 'sensor_accl', 'sensor_magn']

genuine_list_names = {
    0: 'g1',
    1: 'g2',
    2: 'g3',
    3: 'g4',
}

datae = {}
for user in user_list:
    datae[user] = {}
    for session in session_list:
        datae[user][genuine_list_names[session]] = {}
        for task in task_list:
            datae[user][genuine_list_names[session]][task] = {}
            for sensor in sensor_list:
                print(user, session, task, sensor)
                raw = data[sensor][task]['final_data'][user][session].tolist()
                for element in raw:
                    element[0] = int(element[0])
                    for i in range(1,len(element)):
                        element[i] = float(np.around(element[i], 4))
                datae[user][genuine_list_names[session]][task][sensor] = raw
            raw = data[task][task]['final_data'][user][session].tolist()
            if task != 'keystroke':
                for element in raw:
                    element[0] = int(element[0])
                    for i in range(1,len(element)):
                        element[i] = float(np.around(element[i], 4))
                    element[-1] = int(element[-1])
            if task == 'keystroke':
                for element in raw:
                    element[0] = int(element[0])
                    for i in range(1,len(element)):
                        element[i] = float(np.around(element[i], 5))
            datae[user][genuine_list_names[session]][task]['touch'] = raw

with open(new_folder + 'development_dataset.json', 'w') as f:
    json.dump(datae, f)
