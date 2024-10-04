import os, csv
import numpy as np
import copy
import json
import codecs

probs = {'sensor_acc' : ['EN3M2418', 'EN5M8625','EN6P5297','EN9M1951','ENAM5229','ES1C9400','ES1O8150','ES211904','ES218558','ES2C6583','ES2M6438',
'ES2R5074','ES2R6470','ES3S5192','ES3S6848','ES4C9616','ES4R1418','ES5K3240','ES5R2089',
'ES6C8429','ES6S3851','ES7R3577','ES7R8882','ES8C6513','ES8R9196','ES9M1165','ES9M6474',
'ES9M8371','ESAM9016','ESAR2869','ESAR9807','ESBH6521','ESBS5463','ESDO4027','ESER1720',
'ESFP4005','FR2G1047','ES0R4909','ES0R9953','ES0S3858','ES1R6859','ES216205','ES2R8694',
'ES3M3817','ES4M5580','ES6R4616','ES7M3003','ES7R2838','ES7R5791','ES7R8188','ES9C6590',
'ESAM5111','ESAP1304','ESAR5141','ESBA4420','ESBR1435','ESBR2908','ESBR3202','ESER1571',
'ESER6809','ESFM9111','ESFR5179','ES0V7055','ES1R2495','ES9R5993','ESAM6016','ES0S7126',
'ES7M3069','ES7R9990'],
         'sensor_grav' : ['EN0O9998','EN2R6581','EN3M2418','EN3M5488','EN3S8308','EN5M8625','EN6P5297','EN6S2692','EN8S9978','EN9M1951','EN9R2896','ENAM5229','ENAM7544','ES0A3487','ES0M3286','ES0M6665',
'ES0R4909','ES0R9953','ES0S3858','ES0S5249','ES0S7126','ES0S9367','ES0S9487','ES1C8734','ES1C9400','ES1M5391','ES1M5984','ES1O6973','ES1O8150','ES1R2495','ES1R6859','ES1R7711',
'ES1R9361','ES1S4002','ES1S5169','ES1S6412','ES1S8205','ES211904','ES212117','ES212536','ES213742','ES215325','ES216205','ES216638','ES217509','ES218558','ES2C6583','ES2M2452',
'ES2M4623','ES2M6438','ES2R5074','ES2R6470','ES2R8694','ES2S2905','ES2X5783','ES3I7658','ES3M3817','ES3O8335','ES3S2563','ES3S4325','ES3S4915','ES3S5192','ES3S5461','ES3S5662',
'ES3S6848','ES4C9616','ES4M5580','ES4M6404','ES4M8914','ES4M9574','ES4P9671','ES4R1418','ES4R6057','ES4R6256','ES4R7483','ES4S1296','ES4S7966','ES4S9590','ES5I3672','ES5K3240',
'ES5M6957','ES5R2089','ES6C8429','ES6J7316','ES6M1099','ES6M4163','ES6M6964','ES6M7806','ES6S3123','ES6S3851','ES6S5045','ES6S7011','ES6S8724','ES7I9258','ES7M3003','ES7M3069',
'ES7M8035','ES7R2838','ES7R3577','ES7R5791','ES7R8188','ES7R8882','ES7R9990','ES8C1399','ES8C6513','ES8M4673','ES8M5482','ES8M6000','ES8M7210','ES8M9156','ES8R9196','ES9C5552',
'ES9C6590','ES9I9568','ES9M1165','ES9M2047','ES9M3284','ES9M5675','ES9M6474','ES9M6793','ES9M8371','ES9P1545','ES9P2876','ES9R5993','ES9S4597','ESAM1363','ESAM2791','ESAM5111',
'ESAM6016','ESAM7365','ESAM9016','ESAM9834','ESAP1304','ESAP9418','ESAR1564','ESAR5141','ESAR9807','ESAS1554','ESAS5695','ESBA4420','ESBC2144','ESBH6521','ESBL6999','ESBM3199',
'ESBM4667','ESBR1435','ESBR2908','ESBR3202','ESBS5463','ESCM3076','ESCO6424','ESCR3265','ESDG9106','ESDO4027','ESDR7867','ESDS3072','ESDS6408','ESDS7496','ESDS8018','ESDS9520',
'ESEM2205','ESEM7075','ESEM9990','ESER1571','ESER1720','ESER3731','ESER6108','ESER6584','ESER6809','ESER8971','ESES3738','ESES6926','ESES7209','ESFC9458','ESFG1266','ESFI3584',
'ESFM9111','ESFP4005','ESFR5179','ESFR8483','ESFS2957','FR2G1047'],
         'sensor_gyro' : ['EN0O9998','EN2R6581','EN3M2418','EN3M5488','EN3S8308','EN5M8625','EN6P5297','EN6S2692','EN8S9978','EN9M1951','EN9R2896','ENAM5229','ENAM7544','ES0A3487','ES0M3286','ES0M6665',
'ES0R4909','ES0R9953','ES0S3858','ES0S7126','ES0S9367','ES0S9487','ES0V7055','ES1C8734','ES1C9400','ES1M5391','ES1M5984','ES1O6973','ES1O8150','ES1R2495','ES1R6859','ES1R7711',
'ES1R9361','ES1S4002','ES1S5169','ES1S6412','ES1S8205','ES211904','ES212117','ES212536','ES213742','ES215325','ES216205','ES216638','ES217509','ES218558','ES2C6583','ES2M2452',
'ES2M4623','ES2M6438','ES2R5074','ES2R6470','ES2R8694','ES2S2905','ES2X5783','ES3I7658','ES3M3817','ES3O8335','ES3S2563','ES3S4325','ES3S4915','ES3S5192','ES3S5461','ES3S5662',
'ES4C9616','ES4M5580','ES4M6404','ES4M8914','ES4M9574','ES4P9671','ES4R1418','ES4R6057','ES4R6256','ES4R7483','ES4S1296','ES4S7966','ES4S9590','ES5I3672','ES5K3240','ES5M6957',
'ES5R2089','ES5V7262','ES6J7316','ES6M1099','ES6M4163','ES6M6964','ES6M7806','ES6S3123','ES6S3851','ES6S5045','ES6S7011','ES6S8724','ES7I9258','ES7M3003','ES7M3069','ES7M8035',
'ES7R2838','ES7R3577','ES7R5791','ES7R8188','ES7R8882','ES7R9990','ES8C1399','ES8C6513','ES8M4673','ES8M5482','ES8M6000','ES8M7210','ES8M9156','ES8R9196','ES8S9891','ES9C5552',
'ES9C6590','ES9I9568','ES9M1165','ES9M2047','ES9M3284','ES9M5675','ES9M6474','ES9M6793','ES9M8371','ES9P1545','ES9P2876','ES9R5993','ES9S4597','ESAM1363','ESAM2791','ESAM5111',
'ESAM6016','ESAM7365','ESAM9016','ESAM9834','ESAP1304','ESAP9418','ESAR1564','ESAR2869','ESAR5141','ESAR9807','ESBA4420','ESBC2144','ESBH6521','ESBL6999','ESBM3199','ESBM4667',
'ESBR1435','ESBR2908','ESBR3202','ESBS5463','ESCM3076','ESCO6424','ESCR3265','ESDG9106','ESDO4027','ESDR7867','ESDS3072','ESDS8018','ESDS9520','ESEM2205','ESEM7075','ESEM9990',
'ESER1571','ESER1720','ESER3731','ESER6584','ESER6809','ESER8971','ESES3738','ESES7209','ESFC9458','ESFG1266','ESFI3584','ESFM9111','ESFP4005','ESFR5179','ESFR8483','ESFS2957',
'ESFS5018','FR2G1047','ES6R4616','ES8S4163','ESER6108','ESES6926'],
         'sensor_accl' : ['EN0O9998','EN2R6581','EN3M2418','EN3M5488','EN3S8308','EN5M8625','EN6P5297','EN6S2692','EN8S9978','EN9M1951','EN9R2896','ENAM5229','ENAM7544','ES0A3487','ES0M3286','ES0M6665',
'ES0R4909','ES0R9953','ES0S3858','ES0S5249','ES0S7126','ES0S9367','ES0S9487','ES1C8734','ES1C9400','ES1M5391','ES1M5984','ES1O6973','ES1O8150','ES1R2495','ES1R6859','ES1R7711',
'ES1R9361','ES1S4002','ES1S5169','ES1S6412','ES1S8205','ES211904','ES212117','ES212536','ES213742','ES215325','ES216205','ES216638','ES217509','ES218558','ES2C6583','ES2M2452',
'ES2M4623','ES2M6438','ES2R5074','ES2R6470','ES2R8694','ES2S2905','ES2X5783','ES3I7658','ES3M3817','ES3O8335','ES3S2563','ES3S4325','ES3S4915','ES3S5192','ES3S5461','ES3S5662',
'ES3S6848','ES4C9616','ES4M5580','ES4M6404','ES4M8914','ES4M9574','ES4P9671','ES4R1418','ES4R6057','ES4R6256','ES4R7483','ES4S1296','ES4S7966','ES4S9590','ES5I3672','ES5K3240',
'ES5M6957','ES5R2089','ES6C8429','ES6J7316','ES6M1099','ES6M4163','ES6M6964','ES6M7806','ES6S3123','ES6S3851','ES6S5045','ES6S7011','ES6S8724','ES7I9258','ES7M3003','ES7M3069',
'ES7M8035','ES7R2838','ES7R3577','ES7R5791','ES7R8188','ES7R8882','ES7R9990','ES8C1399','ES8C6513','ES8M4673','ES8M5482','ES8M6000','ES8M7210','ES8M9156','ES8R9196','ES9C5552',
'ES9C6590','ES9I9568','ES9M1165','ES9M2047','ES9M3284','ES9M5675','ES9M6474','ES9M6793','ES9M8371','ES9P1545','ES9P2876','ES9R5993','ES9S4597','ESAM1363','ESAM2791','ESAM5111',
'ESAM6016','ESAM7365','ESAM9016','ESAM9834','ESAP1304','ESAP9418','ESAR1564','ESAR5141','ESAR9807','ESAS1554','ESAS5695','ESBA4420','ESBC2144','ESBH6521','ESBL6999','ESBM3199',
'ESBM4667','ESBR1435','ESBR2908','ESBR3202','ESBS5463','ESCM3076','ESCO6424','ESCR3265','ESDG9106','ESDO4027','ESDR7867','ESDS3072','ESDS6408','ESDS7496','ESDS8018','ESDS9520',
'ESEM2205','ESEM7075','ESEM9990','ESER1571','ESER1720','ESER3731','ESER6108','ESER6584','ESER6809','ESER8971','ESES3738','ESES6926','ESES7209','ESFC9458','ESFG1266','ESFI3584',
'ESFM9111','ESFP4005','ESFR5179','ESFR8483','ESFS2957','FR2G1047'],
         'sensor_magn': ['EN2S9781','EN3M2418','EN3S8308','EN5M8625','EN6P5297','EN7S2957','EN9M1951','ENAM5229','ES0R4909','ES0S3702','ES0S5249','ES0V7055','ES1C9400','ES1M5984','ES1O8150','ES1R2495',
'ES1S2178','ES1S4419','ES211904','ES212094','ES212536','ES216205','ES218558','ES2C6583','ES2M6438','ES2R5074','ES2R6470','ES2R8694','ES3S4325','ES3S5192','ES3S5810','ES3S6639',
'ES3S6848','ES3S7838','ES4C9616','ES4M5580','ES4M9574','ES4R1418','ES4R6057','ES4R6256','ES5I3672','ES5K3240','ES5R2089','ES6C8429','ES6S3851','ES7M3003','ES7R2838','ES7R3577',
'ES7R5791','ES7R8188','ES7R8882','ES7R9990','ES8C6513','ES8M6000','ES8M9156','ES8R9196','ES9M1165','ES9M5675','ES9M6474','ES9M8371','ES9R5993','ESAC6991','ESAM5111','ESAM6016',
'ESAM9016','ESAP1304','ESAR5141','ESAR9807','ESBA4420','ESBC2144','ESBH6521','ESBM3199','ESBR2908','ESBR3202','ESBS2409','ESBS5463','ESCC1160','ESCR3265','ESCS2659','ESDG9106',
'ESDO4027','ESDS3072','ESER1571','ESER1720','ESER3731','ESER6108','ESER6809','ESER8971','ESFM9111','ESFP4005','FR2G1047','FRFS5556','ES0R9953','ES0S3858','ES1R6859','ES2M2452',
'ES3M3817','ES3S5461','ES4P9671','ES7S6477','ES9C6590','ES9M2047','ESAS1554','ESBR1435','ESCS3269','ESES6926','ESFG1266','ESFI3584','ESFR5179','ES1O6973','ES4R7483','ES6J7316',
'ES6M4163','ES6S7011','ES8M4673','ES8S9891','ESER6584','ES0S7126','ESCO6424','ESES3738','ES0M3286','ES3I7658','ES6S3123','ES7M3069','ES8C1399','ES9P1545','ES9P2876'],
         '': []
         }

def get_data(SOURCE_FILE_PATH, use_empty_session_flag = True, touch_flag = False, db = 'D:\\Giuseppe\\DBs\\BHP_complete\\test_set\\', sensor = ''):
    users = os.listdir(db)
    dict_raw = {}
    complete_user_counter = 0
    empty_session_user_counter = 0
    users_considered = len(users)
    for i in range(users_considered):
        if users[i] not in probs[sensor]:
            print("user considered:", i, users[i])
            user_folder = db + "/" + users[i] + "/"
            user_sessions = [x[1] for x in os.walk(user_folder)]
            session_data = []
            if len(user_sessions[0]) == 4:  # considering fixed number of sessions = maximum number of sessions
                complete_user_counter = complete_user_counter + 1
                empty_session_flag = False
                ###### HERE ######
                for session in user_sessions[0]:
                    if touch_flag:
                        filename = '{}_g_touch.csv'.format(session)
                    else:
                        filename = sensor + '.csv'
                    print("session", session)
                    try:
                        with open(user_folder + session + SOURCE_FILE_PATH + filename, newline='') as csv_file: # + filename, newline='') as csv_file:  #, newline='') as csv_file: #
                            reader = csv.reader(csv_file)
                            list_item = list(reader)
                            list_item = [item[0].split("\t\t") for item in list_item]
                            session_data.append(list_item)
                    except Exception as e:
                        print(e)
                        print(user_folder + session + SOURCE_FILE_PATH)
                        if len(list_item) == 0:
                            if use_empty_session_flag == True:
                                empty_session_flag = True
                                empty_session_user_counter += empty_session_user_counter
                if empty_session_flag == False:
                    dict_raw[str(i)] = session_data #
    return dict_raw, users


def get_data_s(SOURCE_FILE_PATH, use_empty_session_flag = True, touch_flag = False, db = 'D:\\Giuseppe\\DBs\\BHP_complete\\test_set\\', sensor = ''):
    users = os.listdir(db)
    dict_raw = {}
    complete_user_counter = 0
    empty_session_user_counter = 0
    users_considered = len(users)
    for i in range(users_considered):
        if users[i] not in probs[sensor]:
            print("user considered:", i, users[i])
            user_folder = db + "/" + users[i] + "/"
            user_sessions = [x[1] for x in os.walk(user_folder)]
            session_data = []
            if len(user_sessions[0]) == 4:  # considering fixed number of sessions = maximum number of sessions
                complete_user_counter = complete_user_counter + 1
                empty_session_flag = False
                ###### HERE ######
                for session in user_sessions[0][2:]:
                    if touch_flag:
                        filename = '{}_s_touch.csv'.format(session)
                    else:
                        filename = sensor + '.csv'
                    print("session", session)
                    try:
                        with open(user_folder + session + SOURCE_FILE_PATH + filename, newline='') as csv_file:  #, newline='') as csv_file: #
                            reader = csv.reader(csv_file)
                            list_item = list(reader)
                            list_item = [item[0].split("\t\t") for item in list_item]
                            session_data.append(list_item)
                    except Exception as e:
                        print(e)
                        print(user_folder + session + SOURCE_FILE_PATH)
                        if len(list_item) == 0:
                            if use_empty_session_flag == True:
                                empty_session_flag = True
                                empty_session_user_counter += empty_session_user_counter
                if empty_session_flag == False:
                    dict_raw[str(i)] = session_data #str(i)
    return dict_raw, users


def extract_general(code, sensor, task_codes, list_raw, acceptable_limit, use_impossible_value_flag, touch_flag = False, db = 'D:\\Giuseppe\\DBs\\BHP_complete\\test_set\\'):
    hw = []
    impossible_value_user_counter = 0
    if touch_flag:
        index = 6
    else:
        index = 4
    data = {}
    for user_key in list_raw:  # user
        data_user = []
        for j in range(len(list_raw[user_key])):  # session
            data_session = []
            impossible_value_flag = False
            print("Code", code, "sensor", sensor)
            print("User", user_key, "Session", j)
            for k in range(len(list_raw[user_key][j])):  # sample
                # print("list_raw[user_key][j][k][index] == task_codes[code]",
                #       list_raw[user_key][j][k][index] == task_codes[code])
                if list_raw[user_key][j][k][index] == task_codes[code]:
                    # print("list_raw[user_key][j][k][index]", list_raw[user_key][j][k][index])
                    # print("task_codes[code]", task_codes[code])
                    temp_list = [int(float(list_raw[user_key][j][k][0])), float(list_raw[user_key][j][k][1]), float(list_raw[user_key][j][k][2]), float(list_raw[user_key][j][k][4]), float(list_raw[user_key][j][k][3]), list_raw[user_key][j][k][index], list_raw[user_key][j][k][-2]]
                    # print("type(temp_list[0])", type(temp_list[0]))
                    if any(abs(t) > acceptable_limit for t in temp_list[1:-2]):
                        impossible_value_flag = True
                        print("been here. user #:", user_key)
                    data_session.append(temp_list)
            data_user.append(data_session)
            print("data_user", data_session[0])
        if use_impossible_value_flag:
            if not impossible_value_flag:
                data[user_key] = data_user
            else:
                impossible_value_user_counter = impossible_value_user_counter + 1
        else:
            data[user_key] = data_user
    for user in data.keys():
        for session in range(len(data[user])):
            for sample in range(len(data[user][session])):
                for number in range(len(data[user][session][sample])):
                    data[user][session][sample][number] = float(data[user][session][sample][number])
            data[user][session] = np.array(data[user][session])
    if touch_flag:
        users = os.listdir(db)
        users_considered = len(users)
        for user in range(users_considered):
            user_folder = db + "/" + users[user] + "/"
            with codecs.open(user_folder + "config.json", 'r', 'utf-8') as json_data:  # , newline='') as csv_file: #
                dictio = json.load(json_data)
                height = dictio['height']
                width = dictio['width']
                hw.append([height, width])
            for session in range(len(data[str(user)])):
                for sample in range(len(data[str(user)][session])):
                    data[str(user)][session][sample][1] = data[str(user)][session][sample][1] / width
                    data[str(user)][session][sample][2] = data[str(user)][session][sample][2] / height
    return copy.deepcopy(data), impossible_value_user_counter, hw


def check_sessions(code, sensor, task_codes, list_raw, acceptable_limit, use_impossible_value_flag, touch_flag = False):
    impossible_value_user_counter = 0
    lista_problemi = []
    if touch_flag:
        index = 6
    else:
        index = 4
    data = {}
    for user_key in list_raw:  # user
        data_user = []
        for j in range(len(list_raw[user_key])):  # session
            data_session = []
            impossible_value_flag = False
            print("Code", code, "sensor", sensor)
            print("User", user_key, "Session", j)
            for k in range(len(list_raw[user_key][j])):  # sample
                # print("list_raw[user_key][j][k][index] == task_codes[code]",
                #       list_raw[user_key][j][k][index] == task_codes[code])
                if list_raw[user_key][j][k][index] == task_codes[code]:
                    # print("list_raw[user_key][j][k][index]", list_raw[user_key][j][k][index])
                    # print("task_codes[code]", task_codes[code])
                    temp_list = [int(float(list_raw[user_key][j][k][0])), float(list_raw[user_key][j][k][1]), float(list_raw[user_key][j][k][2]), float(list_raw[user_key][j][k][3]), list_raw[user_key][j][k][index], list_raw[user_key][j][k][-1]]
                    # print("type(temp_list[0])", type(temp_list[0]))
                    if any(abs(t) > acceptable_limit for t in temp_list[1:-2]):
                        impossible_value_flag = True
                        print("been here. user #:", user_key)
                    data_session.append(temp_list)
            data_user.append(data_session)
            try:
                print("data_user", data_session[0])
            except:
                lista_problemi.append([code, sensor, user_key, j])
    if lista_problemi != []:
        print("lista_problemi", lista_problemi)
    return lista_problemi


def keystroke_extract(keystroke_list_raw, acceptable_limit, use_impossible_value_flag, imp_sessions):
    impossible_value_user_counter = 0
    key_data = {}
    user_phrases = {}
    for user_key in keystroke_list_raw:  # user
        user_phrases[user_key] = {}
        key_data_user = []
        for j in range(len(keystroke_list_raw[user_key])):  # session
            key_data_session = []
            user_phrases[user_key][j] = {}
            phrases = []
            asciis = []
            impossible_value_flag = False
            for k in range(len(keystroke_list_raw[user_key][j])-1):  # sample
                if keystroke_list_raw[user_key][j][k][9] == '7' and float(keystroke_list_raw[user_key][j][k+1][8]) < 256 and keystroke_list_raw[user_key][j][k+1][8] != '-1' and \
                        ((j != imp_sessions[0] and j != imp_sessions[1]) or keystroke_list_raw[user_key][j][k][7] == '0'):
                    try:
                        phrases.append(keystroke_list_raw[user_key][j][k][8].encode('utf-8').decode())
                        # if chr(int(keystroke_list_raw[user_key][j][k][8])) == '\u007f':
                        #     print("int(keystroke_list_raw[user_key][j][k][8])", int(keystroke_list_raw[user_key][j][k][8]))
                        asciis.append(int(keystroke_list_raw[user_key][j][k][8]))
                    except:
                        pass # print(user_key, j, int(keystroke_list_raw[user_key][j][k][8]))
                # len-1 is needed because we are calculating inter_press time
                #     if keystroke_list_raw[user_key][j][k+1][0] != '0':  # MADE A DUMMY LINE FOR BHP CHANGING THE INDEX 2 TO 0 # considering only characters not suppressed
                    inter_press = (int(keystroke_list_raw[user_key][j][k+1][0]) - int(keystroke_list_raw[user_key][j][k][0]))/1000000000  # inter_press time [s]
                    temp_list = [float(keystroke_list_raw[user_key][j][k+1][0]), inter_press, float(keystroke_list_raw[user_key][j][k+1][8])/255]  # , chr(int(keystroke_list_raw[i][j][k+1][2]))], dtype=float)
                    if any(abs(t) > acceptable_limit for t in temp_list[1:3]):
                        impossible_value_flag = True
                        print("Problematic user:", user_key, j, k)
                        impossible_value_user_counter += impossible_value_user_counter
                    key_data_session.append(temp_list)
                    user_phrases[user_key][j] = ''.join(phrases)
                    # user_phrases[user_key][j]['phrases'] = ''.join(phrases)
                    # user_phrases[user_key][j]['asciis'] = asciis
            key_data_user.append(np.asarray(key_data_session))
        if use_impossible_value_flag:
            if not impossible_value_flag:
                key_data[user_key] = key_data_user
        else:
            key_data[user_key] = key_data_user
    return copy.deepcopy(key_data), impossible_value_user_counter, user_phrases

def derive(data, dims = 3):
    # this is before reshaping
    data_1 = copy.deepcopy(data)
    for user in data_1:
        for session in range(len(data_1[user])):
            b = np.zeros((np.shape(data_1[user][session])[0], dims))#np.shape(data_1[user][session])[1]-3))
            # print("np.shape(b)", np.shape(b))
            # print("np.shape()", np.shape(np.reshape(data_1[user][session][:, 0], (np.shape(data_1[user][session][:, 0])[0], 1))))
            # b = np.concatenate((np.reshape(data_1[user][session][:, 0], (np.shape(data_1[user][session][:, 0])[0], 1)), b), axis=1)
            for axis in range(1, dims+1):
                try:
                    # b[:, axis] = np.gradient([x[axis] for x in data_1[user][session]])
                    b[:, axis-1] = np.gradient(data_1[user][session][:, axis])
                except Exception as e:
                    print(e)
            data_1[user][session][:, 1:dims+1] = b
    return data_1

def get_diff(data, remove_duplicates=True):
    data_0 = copy.deepcopy(data)
    data_1 = {}
    all_cases = 0
    same_ts = 0
    for user in list(data_0.keys()):
        data_1[user] = {}
        for session in range(len(data_0[user])):
            temp_list = []
            for i in range(len(data_0[user][session])-1):
                diff = int(data_0[user][session][i+1][0]) - int(data_0[user][session][i][0])
                all_cases = all_cases + 1
                if remove_duplicates:
                    if diff > 0:
                        temp_list.append(diff)
                        same_ts = same_ts + 1
                else:
                    temp_list.append(diff)
            data_1[user][session] = temp_list
    return data_1, all_cases, same_ts


def get_freq(data):
    data_0 = copy.deepcopy(data)
    data_1 = {}
    for user in list(data_0.keys()):
        data_1[user] = {}
        for session in range(len(data_0[user])):
            data_1[user][session] = [1E9 * 1 / np.mean(data_0[user][session]), 1E9 * 1 / np.std(data_0[user][session])]

    return data_1


def get_freq_stats(data):
    data_0 = copy.deepcopy(data)
    # print(list(data_0.keys()))
    lista_user_mean = {}
    lista_user_std = {}
    lista_user = {}
    for user in list(data_0.keys()):
        # lista_user_mean[user] = np.mean(list(data_0[user].values()))
        # lista_user_std[user] = np.std(list(data_0[user].values()))
        lista_user_mean[user] = np.mean([x[0] for x in list(data_0[user].values())])
        lista_user_std[user] = np.std([x[0] for x in list(data_0[user].values())])
        lista_user[user] = [x[0] for x in list(data_0[user].values())]
    return lista_user_mean, lista_user_std, lista_user


def downsample(data, freq, avg=False, post_reshape=False):
    data_1 = copy.deepcopy(data)
    if post_reshape == False:
        # this is before reshaping
        if avg == False:
            for user in data_1:
                for session in range(len(data_1[user])):
                   # print("freq[user][session]:", freq[user][session])
                   if freq[user][session][0] < 75.0:
                       ratio = 1
                   if freq[user][session][0] >= 75.0 and freq[user][session][0] < 150:
                       ratio = 2
                   if freq[user][session][0] >= 150.0:
                       ratio = 4
                   # print("Ratio:", ratio)
                   data_1[user][session] = data_1[user][session][::ratio]
        if avg == True:
            for user in data_1:
                for session in range(len(data_1[user])):
                    for session in range(len(data_1[user])):
                        # print("freq[user][session]:", freq[user][session])
                        if freq[user][session][0] < 75.0:
                            ratio = 1
                        if freq[user][session][0] >= 75.0 and freq[user][session][0] < 150:
                            ratio = 2
                        if freq[user][session][0] >= 150.0:
                            ratio = 4
                        # print("Ratio:", ratio)
                        end = ratio * int(len(data_1[user][session]) / ratio)
                    data_1[user][session] = data_1[user][session][:end]
                    b = np.zeros((int(end / ratio), np.shape(data_1[user][session])[1]))
                    for i in range(int(end / ratio)):
                        b[i] = np.mean(data_1[user][session][i * ratio:(i + 1) * ratio], 0)
                    data_1[user][session] = b
    if post_reshape == True:
        original_length_of_subsession = len(list(data_1['0'][0][0]))
        new_length_of_subsession = int(original_length_of_subsession / ratio)
        num_dim = np.shape(data_1['0'][0][0])[-1]
        data_2 = {}
        if avg == False:
            for user in data_1:
                data_2[user] = {}
                for session in range(len(data_1[user])):
                    for session in range(len(data_1[user])):
                        # print("freq[user][session]:", freq[user][session])
                        if freq[user][session][0] < 75.0:
                            ratio = 1
                        if freq[user][session][0] >= 75.0 and freq[user][session][0] < 150:
                            ratio = 2
                        if freq[user][session][0] >= 150.0:
                            ratio = 4
                        # print("Ratio:", ratio)
                    for subsession in range(len(data_1[user][session])):
                        data_1[user][session][subsession] = data_1[user][session][subsession][:, ::ratio]
        if avg == True:
            for user in data_1:
                data_2[user] = {}
                for session in range(len(data_1[user])):
                    for session in range(len(data_1[user])):
                        # print("freq[user][session]:", freq[user][session])
                        if freq[user][session][0] < 75.0:
                            ratio = 1
                        if freq[user][session][0] >= 75.0 and freq[user][session] < 150:
                            ratio = 2
                        if freq[user][session][0] >= 150.0:
                            ratio = 4
                        # print("Ratio:", ratio)
                    num_subsessions = len(list(data_1[user][session]))
                    data_2[user][session] = np.zeros((num_subsessions, new_length_of_subsession, num_dim))
                    for subsession in range(len(data_1[user][session])):
                        end = ratio * int(len(data_1[user][session][subsession]) / ratio)
                        data_1[user][session][subsession] = data_1[user][session][subsession][:end]
                        b = np.zeros((int(end / ratio), np.shape(data_1[user][session][subsession])[1]))
                        for i in range(int(end / ratio)):
                            b[i] = np.mean(data_1[user][session][subsession][i * ratio:(i + 1) * ratio], 0)
                        data_2[user][session][subsession] = b
    if avg and post_reshape:
        return data_2
    else:
        return data_1


def normalize_no_sub(data, epsilon=0.00000001, less_right_columns=2):
    Std_cnt = 0
    Std_no_zero = 0
    data_1 = copy.deepcopy(data)
    for user in data_1:
        for session in range(len(list(data_1[user]))):
                for axis in range(1, np.shape(data_1[user][session])[1]-less_right_columns):
                    Mean = np.mean([x[axis] for x in data_1[user][session]])
                    Std = np.std([x[axis] for x in data_1[user][session]])
                    data_1[user][session][:, axis] = data_1[user][session][:,axis]-Mean
                    data_1[user][session][:, axis] = data_1[user][session][:,axis]/(Std+epsilon)
                    if Std > 0:
                        Std_no_zero = Std_no_zero + 1
                    Std_cnt = Std_cnt + 1
    # print("Std_no_zero/Std_cnt", Std_no_zero / Std_cnt)
    # print("Std_cnt", Std_cnt)
    return data_1


def stack(data_list, todel):
    data_1 = copy.deepcopy(data_list[0])
    for i in range(1, len(data_list)):
        for user in data_list[i]:
            for session in range(len(data_list[i][user])):
                # print("user", user)
                # print("session", session)
                data_1[user][session] = np.concatenate((data_1[user][session], data_list[i][user][session]), axis=-1)
    for user in list(data_1.keys()):
        for session in range(len(data_1[user])):
            print(user, session)
            data_1[user][session] = np.delete(data_1[user][session], todel, axis=1)
            print(data_1[user][session][0])
    return data_1

def timestamp_alignment(tdictio, bdictio):
    initial_task_ts = []
    final_task_ts = []
    bdictio['Test_db_msk'] = copy.deepcopy(bdictio)
    for user in tdictio.keys():
        initial_task_sess_ts = []
        final_task_sess_ts = []
        for session in range(len(tdictio[user])):
            initial_task_sess_ts.append(int(tdictio[user][session][0][0]))
            final_task_sess_ts.append(int(tdictio[user][session][-1][0]))
        initial_task_ts.append(initial_task_sess_ts)
        final_task_ts.append(final_task_sess_ts)
    for user in bdictio.keys():
        for session in range(len(bdictio[user])):
            mask = []
            for sample in range(len(bdictio[user][session])):
                mask.append(int((bdictio[user][session][sample][0] >= initial_task_ts[int(user)][session] and bdictio[user][session][sample][0] <= final_task_ts[int(user)][session])))
            for sample in range(len(bdictio[user][session])):
                bdictio['Test_db_msk'][user][session][sample][0] = np.multiply(mask[sample], bdictio[user][session][sample][0])
    for user in bdictio.keys():
        for session in range(len(bdictio[user])):
            bdictio['Test_db_msk'][user][session] = np.asarray([x for x in bdictio['Test_db_msk'][user][session] if x[0]!=0])
            bdictio['mask'] = mask
    tdictio["initial_task_ts"] = initial_task_ts
    tdictio["final_task_ts"] = final_task_ts
    return 0


def keep_k_sessions(data, tobekept_list):
    findat = {}
    for user in list(data.keys()):
        findat[user] = {}
        for kept_ses in tobekept_list:
            findat[user][tobekept_list.index(kept_ses)] = data[user][kept_ses]
    return findat

def add_mult_noise(data, tuple_interval):
    rang = tuple_interval[1]-tuple_interval[0]
    minim = tuple_interval[0]
    data_1 = copy.deepcopy(data)
    for user in data_1:
        for session in range(len(data_1[user])):
            shape = np.shape(data_1[user][session])
            multiplicative = np.random.rand(shape[0], shape[1]-3)*rang+minim
            # print("np.shape(multiplicative)", np.shape(multiplicative))
            # print("data_1[user][session][:, 1:]", np.shape(data_1[user][session][:, 1:]))
            multiplicative = np.concatenate((np.ones((shape[0], 1)), multiplicative), axis=1)
            multiplicative = np.concatenate((multiplicative,np.ones((shape[0], 1))), axis=1)
            multiplicative = np.concatenate((multiplicative,np.ones((shape[0], 1))), axis=1)
            data_1[user][session] = np.multiply(data_1[user][session], multiplicative) #+ additive
    return data_1