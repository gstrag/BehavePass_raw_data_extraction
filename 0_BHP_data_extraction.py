import os

from BHP_data_extraction_utils import *
import time
import matplotlib.pyplot as plt
from collections import OrderedDict
from operator import itemgetter
import math

# a = np.load('extracted_data/skilled_test_dataset.npy', allow_pickle=True).item()
# b = np.load('extracted_data/copied/skilled_test_dataset.npy', allow_pickle=True).item()

start = time.time()

acceptable_limit = 5000
avg = False
NF = 3
noise = False
if noise:
    noise_add = '_noise'
else:
    noise_add = ''
impostor_dict = {
    'random_dev': 'without_skilled',
    'random_test': 'with_skilled_30',
    'skilled': 'with_skilled_30',
}

saved_set_dict = {
    'random_dev': 'development_dataset',
    'random_test': 'random_test_dataset',
    'skilled': 'skilled_test_dataset',
}


base_dir = 'D:/DBs/BHP_release_perfect/'
impostor = 'random_test'  # 'skilled'

db = base_dir + impostor_dict[impostor] + '/'
new_folder = 'extracted_data/'
DESTINATION_FOLDER = new_folder + impostor_dict[impostor] + '_preprocessed{}/'.format(noise_add)

task_codes = {
    'keystroke': '3',
    'readtext': '4',
    'gallery': '5',
    'tap': '6',
}

save_extracted_data = False
use_empty_session_flag = True  # when finds empty data in any user session, removes user completely
use_impossible_value_flag = True  # when finds empty data in any user session, removes user completely
files = ["general"]
background_sensor_list = ['sensor_acc', 'sensor_grav', 'sensor_gyro', 'sensor_accl', 'sensor_magn'] #
touch_task_list = ['keystroke', 'readtext', 'gallery', 'tap']
# We divide the users into training and validation according to the following proportion
val_prop = 0.0
stats = {}
data = {}
keys = {}

for file in files:
    data[file] = {}
    stats[file] = {}
    for sensor in background_sensor_list:
        if impostor == 'skilled':
            SOURCE_FILE_PATH = "/s/" + file + "/sensors/"  # key_data.csv"  #
            list_raw, users = get_data_s(SOURCE_FILE_PATH, use_empty_session_flag=True, touch_flag=False, db=db, sensor=sensor)
        else:
            SOURCE_FILE_PATH = "/g/" + file + "/sensors/"  # key_data.csv"  #
            list_raw, users = get_data(SOURCE_FILE_PATH, use_empty_session_flag=True, touch_flag=False, db=db, sensor=sensor)
        if file == 'general':
            stats[file][sensor] = {}
            data[file][sensor] = {}
            for code in touch_task_list:
                data[file][sensor][code] = {}
                print("Task:", file + ", sensor:", sensor, ", code:", code)
                # data[file][sensor][code]["lista_problemi"] = extrat(code, sensor, task_codes, list_raw, acceptable_limit, use_impossible_value_flag, touch_flag=False)
                if noise:
                    data[file][sensor][code]["nn_extracted_data"], impossible_user_value_counter, _ = extract_general(code, sensor, task_codes, list_raw, acceptable_limit, use_impossible_value_flag, touch_flag=False, db = db)
                    data[file][sensor][code]["extracted_data"] = add_mult_noise(data[file][sensor][code]["nn_extracted_data"], (0.98, 1.02))
                else:
                    data[file][sensor][code]["extracted_data"], impossible_user_value_counter, _ = extract_general(code, sensor, task_codes, list_raw, acceptable_limit, use_impossible_value_flag, touch_flag=False, db = db)
                # data[file][sensor][code]["d_extracted_data"] = derive(data[file][sensor][code]["extracted_data"])
                # data[file][sensor][code]["dd_extracted_data"] = derive(data[file][sensor][code]["d_extracted_data"])

                # # we now check timestamp for equalizing frequency
                # data[file][sensor][code]['diff'], data[file][sensor][code]['all_cases'], data[file][sensor][code]['diff_ts'] = get_diff(data[file][sensor][code]["extracted_data"])

                # data[file][sensor][code]['freq'] = get_freq(data[file][sensor][code]['diff'])
                # data[file][sensor][code]['lista_user_mean'], data[file][sensor][code]['lista_user_std'], data[file][sensor][code]['lista_user_freq'] = get_freq_stats(data[file][sensor][code]['freq'])
                #
                # data[file][sensor][code]["ds_extracted_data"] = downsample(data[file][sensor][code]["extracted_data"], data[file][sensor][code]['freq'], avg=avg)
                # data[file][sensor][code]["ds_d_extracted_data"] = downsample(data[file][sensor][code]["d_extracted_data"], data[file][sensor][code]['freq'], avg=avg)
                # data[file][sensor][code]["ds_dd_extracted_data"] = downsample(data[file][sensor][code]["dd_extracted_data"], data[file][sensor][code]['freq'], avg=avg)
                #
                # data[file][sensor][code]['diff_post_ds'], data[file][sensor][code]['all_cases_post_ds'], data[file][sensor][code]['diff_ts_post_ds'] = get_diff(data[file][sensor][code]["ds_extracted_data"])
                # data[file][sensor][code]['freq_post_ds'] = get_freq(data[file][sensor][code]['diff_post_ds'])
                # data[file][sensor][code]['lista_user_mean_post_ds'], data[file][sensor][code]['lista_user_std_post_ds'], data[file][sensor][code]['lista_user_freq_post_ds'] = get_freq_stats(data[file][sensor][code]['freq_post_ds'])
                #
                #
                # data[file][sensor][code]["ds_extracted_data_nrm"] = normalize_no_sub(data[file][sensor][code]["ds_extracted_data"])
                # data[file][sensor][code]["ds_d_extracted_data_nrm"] = normalize_no_sub(data[file][sensor][code]["ds_d_extracted_data"])
                # data[file][sensor][code]["ds_dd_extracted_data_nrm"] = normalize_no_sub(data[file][sensor][code]["ds_dd_extracted_data"])

                data[file][sensor][code]["data_list"] = [data[file][sensor][code]["extracted_data"]]

                data[file][sensor][code]["final_data"] = stack(data[file][sensor][code]["data_list"], [3, 5, 6])
                # data[file][sensor][code]["final_data"] = keep_k_sessions(data[file][sensor][code]["final_data"], [1,2])
                # del data[file][sensor][code]["final_data"]['11']
                # del data[file][sensor][code]["final_data"]['24']
                # del data[file][sensor][code]["final_data"]['31']

                # total_user_number = len(data[file][sensor][code]['final_data'])
                #
                # validation_set_size = int(total_user_number * val_prop)
                # training_set_size = total_user_number - validation_set_size
                #
                # total_user_idxs = [x for x in range(total_user_number)]
                #
                # training_set_idxs = list(data[file][sensor][code]['final_data'].keys())[:training_set_size]
                # validation_set_idxs = list(data[file][sensor][code]['final_data'].keys())[training_set_size:]
                #
                # train_dict = {key: data[file][sensor][code]["final_data"][key] for key in
                #               data[file][sensor][code]["final_data"].keys() & training_set_idxs}
                # validation_dict = {key: data[file][sensor][code]["final_data"][key] for key in
                #                    data[file][sensor][code]["final_data"].keys() & validation_set_idxs}
                #
                # keys = natsort.natsorted(train_dict.keys())
                # train_dict = OrderedDict((k, train_dict[k]) for k in keys)
                #
                # keys = natsort.natsorted(validation_dict.keys())
                # validation_dict = OrderedDict((k, validation_dict[k]) for k in keys)

                if save_extracted_data:
                    np.save(DESTINATION_FOLDER + file + '_' + sensor + '_' + code + '.npy', data[file][sensor][code]["final_data"])

#
#                 for user in range(len(data[file][sensor][code]['final_data'])):  # len(data[file][touch_task]['final_data'])):
#                     for session in range(len(data[file][sensor][code]['final_data'][str(user)])):
#                         mx = np.mean(data[file][sensor][code]['final_data'][str(user)][session][:, 1])
#                         if abs(mx) > 0.0: mx = str(math.floor(math.log(abs(mx), 10)))
#                         else: mx = "-inf"
#                         my = np.mean(data[file][sensor][code]['final_data'][str(user)][session][:, 2])
#                         if abs(my) > 0.0: my = str(math.floor(math.log(abs(my), 10)))
#                         else: my = "-inf"
#                         mz = np.mean(data[file][sensor][code]['final_data'][str(user)][session][:, 3])
#                         if abs(mz) > 0.0: mz = str(math.floor(math.log(abs(mz), 10)))
#                         else: mz = "-inf"
#                         sx = np.std(data[file][sensor][code]['final_data'][str(user)][session][:, 1])
#                         if abs(1-sx) > 0.0: sx = str(math.floor(math.log(abs(1-sx), 10)))
#                         else: sx = "-inf"
#                         sy = np.std(data[file][sensor][code]['final_data'][str(user)][session][:, 2])
#                         if abs(1-sy) > 0.0: sy = str(math.floor(math.log(abs(1-sy), 10)))
#                         else: sy = "-inf"
#                         sz = np.std(data[file][sensor][code]['final_data'][str(user)][session][:, 3])
#                         if abs(1-sz) > 0.0: sz = str(math.floor(math.log(abs(1-sz), 10)))
#                         else: sz = "-inf"
#                         print("User: " + str(user) + ", Session: " + str(session) + ', Mean (x, y, z): (' + mx + ', ' + my + ', ' + mz + ')')
#                         plt.plot(data[file][sensor][code]['final_data'][str(user)][session][:, 1:4], label = 'Mean (x, y, z): (' + mx + ', ' + my + ', ' + mz + ') - ' +
#                                  '1-Std (x, y, z): (' + sx + ', ' + sy + ', ' + sz + ')')
#                         plt.legend(loc='lower left')
#                         plt.ylim(-25,25)
#                         plt.title(sensor + ' ' + code + ' ' + str(user) + ' ' + str(session) + '\norig. sess. frequency: ' +
#                                   str(data[file][sensor][code]['lista_user_freq'][str(user)][session])[:6] + '\npost downsample: ' +
#                                   str(data[file][sensor][code]['lista_user_freq_post_ds'][str(user)][session])[:6], fontsize = 10)
#                         plt.savefig("session_plots/sensor_{}_code_{}_user_{}_session_{}.jpg".format(sensor, code, str(user),
#                                                                                                     session))
#                         plt.close()

# good_users_i = {}
# for sensor in background_sensor_list:
#     good_users_i[sensor] = {}
#     for code in touch_task_list:
#         good_user_indexes = []
#         for user in data['general'][sensor][code]['lista_user_freq'].keys():
#             if np.sum(np.array(data['general'][sensor][code]['lista_user_freq'][user]) > 30) == 4:
#                 good_user_indexes.append(user)
#         good_users_i[sensor][code] = good_user_indexes

# lenslist = []
# senslens = {}
# for sensor in background_sensor_list:
#     senslens[sensor] = {}
#     for code in touch_task_list:
#         senslens[sensor][code] = {}
#         for user in data['general'][sensor][code]['lista_user_freq'].keys():
#             senslens[sensor][code][user] = {}
#             for session in range(4):
#                 senslens[sensor][code][user][session] = len(data['general'][sensor][code]['final_data'][user][session])
#                 lenslist.append([[sensor, code, user, session], len(data['general'][sensor][code]['final_data'][user][session])])
# # t = 0
for file in files:
    # data[file] = {}
    # stats[file] = {}
    if file == 'general':
        # for touch_task in [x for x in touch_task_list if x != 'keystroke']:
        for touch_task in touch_task_list:
            code = touch_task
            if impostor == 'skilled':
                SOURCE_FILE_PATH = "/s/" + file + "/touches/"  # key_data.csv"  #
                list_raw_touch, users = get_data_s(SOURCE_FILE_PATH, use_empty_session_flag=True, touch_flag=True, db=db)
            else:
                SOURCE_FILE_PATH = "/g/" + file + "/touches/"  # key_data.csv"  #
                list_raw_touch, users = get_data(SOURCE_FILE_PATH, use_empty_session_flag=True, touch_flag=True, db = db)
            stats[file][touch_task] = {}
            data[file][touch_task] = {}
            stats[file][touch_task][code] = {}
            data[file][touch_task][code] = {}

            print("Task:", file + ", touch file:", touch_task, ", code:", task_codes[touch_task])
            if touch_task != 'keystroke':
                data[file][touch_task][code]["extracted_data"], impossible_user_value_counter, a = extract_general(touch_task, '', task_codes, list_raw_touch, acceptable_limit, use_impossible_value_flag, touch_flag=True, db = db)
                # data[file][keyword]["n_extracted_data"] = add_mult_noise(data[file][keyword]["extracted_data"], (0.98, 1.02))
                # data[file][touch_task][code]["d_extracted_data"] = derive(data[file][touch_task][code]["extracted_data"], dims = 2)
                # data[file][touch_task][code]["dd_extracted_data"] = derive(data[file][touch_task][code]["d_extracted_data"], dims = 2)


                # data[file][touch_task][code]["extracted_data_nrm"] = normalize_no_sub(data[file][touch_task][code]["extracted_data"])
                # data[file][touch_task][code]["d_extracted_data_nrm"] = normalize_no_sub(data[file][touch_task][code]["d_extracted_data"])
                # data[file][touch_task][code]["dd_extracted_data_nrm"] = normalize_no_sub(data[file][touch_task][code]["dd_extracted_data"])

                data[file][touch_task][code]["data_list"] = [data[file][touch_task][code]["extracted_data"]]

                data[file][touch_task][code]["final_data"] = stack(data[file][touch_task][code]["data_list"], todel = [4, 5, 6])

            if touch_task == 'keystroke':
                data[file][touch_task][code] = {}
                if impostor == 'skilled':
                    data[file][touch_task][code]['final_data'], impossible_user_value_counter, user_phrases = keystroke_extract(list_raw_touch, acceptable_limit, use_impossible_value_flag, [0, 0])
                else:
                    data[file][touch_task][code][
                        'final_data'], impossible_user_value_counter, user_phrases = keystroke_extract(list_raw_touch,
                                                                                                       acceptable_limit,
                                                                                                       use_impossible_value_flag,
                                                                                                       [1, 2])

            # total_user_number = len(data[file][touch_task][code]['final_data'])
            #
            # validation_set_size = int(total_user_number * val_prop)
            # training_set_size = total_user_number - validation_set_size
            #
            # total_user_idxs = [x for x in range(total_user_number)]
            #
            # training_set_idxs = list(data[file][touch_task][code]['final_data'].keys())[:training_set_size]
            # validation_set_idxs = list(data[file][touch_task][code]['final_data'].keys())[training_set_size:]
            #
            # train_dict = {key: data[file][touch_task][code]["final_data"][key] for key in
            #               data[file][touch_task][code]["final_data"].keys() & training_set_idxs}
            # validation_dict = {key: data[file][touch_task][code]["final_data"][key] for key in
            #                    data[file][touch_task][code]["final_data"].keys() & validation_set_idxs}
            #
            # keys = natsort.natsorted(train_dict.keys())
            # train_dict = OrderedDict((k, train_dict[k]) for k in keys)
            #
            # keys = natsort.natsorted(validation_dict.keys())
            # validation_dict = OrderedDict((k, validation_dict[k]) for k in keys)
            if save_extracted_data:
                np.save(DESTINATION_FOLDER + file + '_' + code + '_' + code + '.npy', data[file][touch_task][code]["final_data"])

data1 = copy.deepcopy(data['general'])
for keyz in list(data1.keys()):
    if keyz in touch_task_list[1:]:
        del data1[keyz][keyz]['extracted_data']
        del data1[keyz][keyz]['data_list']
    if keyz in background_sensor_list:
        for task in touch_task_list:
            del data1[keyz][task]['extracted_data']
            del data1[keyz][task]['data_list']
t = 0
np.save(new_folder + '{}.npy'.format(saved_set_dict[impostor]), data1)

val_set_users = users[:10]
test_set_users = users[10:]

with open(new_folder + 'val_set_users.txt', 'w') as f:
    for line in val_set_users:
        f.write(f"{line}\n")

with open(new_folder + 'test_set_users.txt', 'w') as f:
    for line in test_set_users:
        f.write(f"{line}\n")


# phrases = {}
# for user in list(data['general']['keystroke']['keystroke']['final_data'].keys()):
#     phrases[user] = {}
#     for session in range(len(data['general']['keystroke']['keystroke']['final_data'][user])):
#         chrs = []
#         for line in list_raw_touch[user][session]:
#             if line[9] == '7' and line[4] != '1':
#                 if line[8] != '-1' and int(line[8]) < 256:
#                     chrs.append(chr(int(line[8])))
#         chrs = ''.join(chrs)
#         phrases[user][session] = chrs
# a_file = open("phrases_52.json", "w")
# a_file = json.dump(phrases, a_file, indent=4)