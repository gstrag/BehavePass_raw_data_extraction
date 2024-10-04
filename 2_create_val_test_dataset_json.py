import numpy as np
import json
import copy

new_folder = 'extracted_data/'


data_random = np.load(new_folder + 'random_test_dataset.npy', allow_pickle=True).item()
data_skilled = np.load(new_folder + 'skilled_test_dataset.npy', allow_pickle=True).item()

user_list = [str(x) for x in range(30)]
session_list = [x for x in range(4)]
session_skilled_list = [x for x in range(2)]
task_list = ['keystroke', 'readtext', 'gallery', 'tap']
sensor_list = ['sensor_acc', 'sensor_grav', 'sensor_gyro', 'sensor_accl', 'sensor_magn']

ul = ['ES218746', 'ES7L6690', 'ESDH7853', 'ESBV3311', 'ES6R4770', 'EN7I2687', 'ES8S1161', 'ES4C9910', 'ESBV5283', 'ES9M6548', 'ESER9915', 'ES5M9443', 'ES6M6836', 'ES3S9501', 'ES0M3657', 'ESCM6922', 'ES7F7550', 'ESDC5518', 'ES0A7163', 'ES4R2777', 'ES8F5434', 'EN3E6278', 'ES216147', 'ES9S2091', 'ESAR7223', 'ESCC4592', 'ESEC9025', 'ES3M3004', 'ESFS3784', 'ES7A7962', 'EN4R1904', 'ESDP6151', 'ES3M4251', 'ES1R5876', 'ES7M9981', 'ES6C2035', 'ESFE9276', 'ES5R3480', 'ES212398', 'ES8M5647', 'ES8S1484', 'ES212904', 'ES5M8006', 'ESFM9022', 'ES6S9186', 'ES6S2469', 'ESCI9755', 'ES217599', 'ESAC4722', 'ESDS7415', 'ES8P1666', 'ES5M4201']


genuine_list_names = {
    0: 'g1',
    1: 'g2',
    2: 'g3',
    3: 'g4',
}

impostor_list_names = {
    0: 's1',
    1: 's2',
}

datae = {}
for user in user_list:
    datae[user] = {}
    for session in session_list:
        datae[user][genuine_list_names[session]] = {}
        for task in task_list:
            datae[user][genuine_list_names[session]][task] = {}
            for sensor in sensor_list:
                print(user, session, task, sensor, 'random')
                raw = data_random[sensor][task]['final_data'][user][session].tolist()
                for element in raw:
                    element[0] = int(element[0])
                    for i in range(1,len(element)):
                        element[i] = np.around(element[i], 4)
                datae[user][genuine_list_names[session]][task][sensor] = raw
            raw = data_random[task][task]['final_data'][user][session].tolist()
            if task != 'keystroke':
                for element in raw:
                    element[0] = int(element[0])
                    for i in range(1,len(element)):
                        element[i] = np.around(element[i], 4)
                    element[-1] = int(element[-1])
            if task == 'keystroke':
                for element in raw:
                    element[0] = int(element[0])
                    for i in range(1,len(element)):
                        element[i] = np.around(element[i], 5)
            datae[user][genuine_list_names[session]][task]['touch'] = raw

del data_random

for user in user_list:
    for session in session_skilled_list:
        datae[user][impostor_list_names[session]] = {}
        for task in task_list:
            datae[user][impostor_list_names[session]][task] = {}
            for sensor in sensor_list:
                print(user, session, task, sensor, 'skilled')
                raw = data_skilled[sensor][task]['final_data'][user][session].tolist()
                for element in raw:
                    element[0] = int(element[0])
                    for i in range(1,len(element)):
                        element[i] = np.around(element[i], 4)
                datae[user][impostor_list_names[session]][task][sensor] = raw
            raw = data_skilled[task][task]['final_data'][user][session].tolist()
            if task != 'keystroke':
                for element in raw:
                    element[0] = int(element[0])
                    for i in range(1,len(element)):
                        element[i] = np.around(element[i], 4)
                    element[-1] = int(element[-1])
            if task == 'keystroke':
                for element in raw:
                    element[0] = int(element[0])
                    for i in range(1,len(element)):
                        element[i] = np.around(element[i], 5)
            datae[user][impostor_list_names[session]][task]['touch'] = raw

del data_skilled

data_val = {user: datae[user] for user in [str(x) for x in range(10)]}

for user in [str(x) for x in range(10)]:
    del datae[user]


with open(new_folder + 'data_val.json', 'w') as f:
    json.dump(data_val, f)

with open(new_folder + 'datae.json', 'w') as f:
    json.dump(datae, f)

