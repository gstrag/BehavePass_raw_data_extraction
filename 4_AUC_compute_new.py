import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import copy, json
import random, string, sys
from itertools import chain


set_type = 'test'
if set_type == 'test':
    n_users = 20
if set_type == 'val':
    n_users = 10

new_folder = 'extracted_data/'

# task = sys.argv[1]
#
# here I create the list of enrolment sessions, their pseudonyms and a dictionary containing the relation between the two
# NOT SHUFFLED
enrolment_sessions = []
pseu_enrolment_sessions = []
enrolment_sessions_dict = {}
for user in range(1, n_users + 1):
    enrolment_sessions.append('u' + str(user) + 'e1')
    enrolment_sessions.append('u' + str(user) + 'e2')
    all_chars = list(string.digits + string.ascii_letters)
    random.shuffle(all_chars)
    pseu_enrolment_sessions.append('enrolment_' + ''.join(all_chars[:4]))
    enrolment_sessions_dict['enrolment_' + ''.join(all_chars[:4])] = 'u' + str(user) + 'e1'
    random.shuffle(all_chars)
    pseu_enrolment_sessions.append('enrolment_' + ''.join(all_chars[:4]))
    enrolment_sessions_dict['enrolment_' + ''.join(all_chars[:4])] = 'u' + str(user) + 'e2'

# # checking that we have enough different sessions
# # NOT SHUFFLED
# pseu_enrolment_sessions = list(set(pseu_enrolment_sessions))
#
#
# here I create the list of verification sessions, their pseudonyms and a dictionary containing the relation between the two
# NOT SHUFFLED
verification_sessions = []
pseu_verification_sessions = []
for user in range(1, n_users + 1):
    verification_sessions.append(['v' + str(user) + 'a', 'v' + str(user) + 'b', 'v' + str(user) + 'c',
                                  'v' + str(user) + 'd', 'v' + str(user) + 'e', 'v' + str(user) + 'f'])
    verification_sessions.append(['v' + str(user) + 'a', 'v' + str(user) + 'b', 'v' + str(user) + 'c',
                                  'v' + str(user) + 'd', 'v' + str(user) + 'e', 'v' + str(user) + 'f'])
    for i in range(6):
        all_chars = list(string.digits + string.ascii_letters)
        random.shuffle(all_chars)
        pseu_verification_sessions.append('verification_' + ''.join(all_chars[:4]))
pseu_verification_sessions_set = list(set(pseu_verification_sessions))
pseu_verification_sessions_set = [pseu_verification_sessions_set[i:i+6] for i in range(0, len(pseu_verification_sessions_set), 6)]
pseu_verification_sessions = [pseu_verification_sessions[i:i+6] for i in range(0, len(pseu_verification_sessions), 6)]
pseu_verification_sessions = list(chain(*[[i]*2 for i in pseu_verification_sessions]))


verification_sessions_dict = {}

for user in range(len(pseu_verification_sessions_set)):
    verification_sessions_dict[pseu_verification_sessions_set[user][0]] = 'v' + str(user+1) + 'a'
    verification_sessions_dict[pseu_verification_sessions_set[user][1]] = 'v' + str(user+1) + 'b'
    verification_sessions_dict[pseu_verification_sessions_set[user][2]] = 'v' + str(user+1) + 'c'
    verification_sessions_dict[pseu_verification_sessions_set[user][3]] = 'v' + str(user+1) + 'd'
    verification_sessions_dict[pseu_verification_sessions_set[user][4]] = 'v' + str(user+1) + 'e'
    verification_sessions_dict[pseu_verification_sessions_set[user][5]] = 'v' + str(user+1) + 'f'


c = list(zip(pseu_enrolment_sessions, pseu_verification_sessions))
random.shuffle(c)
pseu_enrolment_sessions, pseu_verification_sessions = zip(*c)

comparisons_list = []
comparisons_list_type = []
for i in range(n_users*2):
    for j in range(6):
        comparisons_list.append(pseu_enrolment_sessions[i] + ' ' + pseu_verification_sessions[i][j])
        if verification_sessions_dict[pseu_verification_sessions[i][j]][-1] == 'a' or verification_sessions_dict[pseu_verification_sessions[i][j]][-1] == 'b':
            comparisons_list_type.append('genuine')
        if verification_sessions_dict[pseu_verification_sessions[i][j]][-1] == 'c' or verification_sessions_dict[pseu_verification_sessions[i][j]][-1] == 'd':
            comparisons_list_type.append('skilled')
        if verification_sessions_dict[pseu_verification_sessions[i][j]][-1] == 'e' or verification_sessions_dict[pseu_verification_sessions[i][j]][-1] == 'f':
            comparisons_list_type.append('random')

c = list(zip(comparisons_list, comparisons_list_type))
random.shuffle(c)
comparisons_list, comparisons_list_type = zip(*c)


task_list = ['keystroke', 'gallery', 'readtext', 'tap']

for task in task_list:


    comparisons_list_results = []
    for i in range(6*2*n_users):
        if comparisons_list_type[i] == 'genuine':
            comparisons_list_results.append(np.clip(np.random.normal(0.45, 0.22), 0,1))
        if comparisons_list_type[i] == 'skilled':
            comparisons_list_results.append(np.clip(np.random.normal(0.55, 0.22), 0,1))
        if comparisons_list_type[i] == 'random':
            comparisons_list_results.append(np.clip(np.random.normal(0.6, 0.22), 0,1))

    to_save_comparisons_list = [str(x) + '\n' for x in comparisons_list]
    with open(new_folder + 'comparisons_list_{}_{}.txt'.format(set_type, task), mode='w') as out_file:
        out_file.write(''.join(to_save_comparisons_list))

    to_save_comparisons_list_type = [str(x) + '\n' for x in comparisons_list_type]
    with open(new_folder + 'comparisons_list_type_{}_{}.txt'.format(set_type, task), mode='w') as out_file:
        out_file.write(''.join(to_save_comparisons_list_type))
    to_save_comparisons_list_results = [str(x) + '\n' for x in comparisons_list_results]
    with open(new_folder + 'comparisons_list_results_{}_{}.txt'.format(set_type, task), mode='w') as out_file:
        out_file.write(''.join(to_save_comparisons_list_results))

    with open(new_folder + 'enrolment_sessions_dict_{}_{}.json'.format(set_type, task), 'w') as outfile:
        json.dump(enrolment_sessions_dict, outfile)

    with open(new_folder + 'verification_sessions_dict_{}_{}.json'.format(set_type, task), 'w') as outfile:
        json.dump(verification_sessions_dict, outfile)

    t = 0

    with open(new_folder + 'comparisons_list_{}_{}.txt'.format(set_type, task)) as f:
        comparisons_list = f.readlines()
    for i in range(len(comparisons_list)):
        comparisons_list[i] = comparisons_list[i][:-1]

    with open(new_folder + 'comparisons_list_type_{}_{}.txt'.format(set_type, task)) as f:
        comparisons_list_type = f.readlines()
    for i in range(len(comparisons_list_type)):
        comparisons_list_type[i] = comparisons_list_type[i][:-1]

    results = np.loadtxt(new_folder + 'comparisons_list_results_{}_{}.txt'.format(set_type, task), dtype=float)

    with open(new_folder + 'enrolment_sessions_dict_{}_{}.json'.format(set_type, task)) as f:
        enrolment_sessions_dict = json.load(f)

    with open(new_folder + 'verification_sessions_dict_{}_{}.json'.format(set_type, task)) as f:
        verification_sessions_dict = json.load(f)


    t = 0

    with open(new_folder + 'enrolment_{}.json'.format(set_type)) as f:
        enrolment = json.load(f)

    enrolment_session_keys = {}
    for i in range(0,n_users*2,2):
        string1 = 'u' + str(int(np.ceil((i+1)/2))) + 'e' + str(1)
        string2 = 'u' + str(int(np.ceil((i+1)/2))) + 'e' + str(2)
        enrolment_session_keys[string1] = str(i+1)
        enrolment_session_keys[string2] = str(i+2)

    for session in list(enrolment_session_keys.keys()):
        enrolment[session] = copy.deepcopy(enrolment[enrolment_session_keys[session]])
        del enrolment[enrolment_session_keys[session]]

    for session in list(enrolment_sessions_dict.keys()):
        enrolment[session] = copy.deepcopy(enrolment[enrolment_sessions_dict[session]])
        del enrolment[enrolment_sessions_dict[session]]

    enrolment_sessions_list_shuffled = sorted(list(enrolment_sessions_dict.keys()), key=lambda k: random.random())

    enrolment_shuffled = {}
    for session in enrolment_sessions_list_shuffled:
        enrolment_shuffled[session] = enrolment[session]
    del enrolment

    for session in list(enrolment_shuffled.keys()):
        for task_here in list(enrolment_shuffled[session].keys()):
            if task_here != task:
                del enrolment_shuffled[session][task_here]

    with open(new_folder + 'enrolment_shuffled_{}_{}.json'.format(set_type, task), 'w') as outfile:
        json.dump(enrolment_shuffled, outfile)

    with open(new_folder + 'verification_{}.json'.format(set_type)) as f:
        verification = json.load(f)

    verification_session_keys = {}
    index = 1
    for i in range(0,n_users*6,6):
        if i != (n_users-1)*6:
            string1 = 'v' + str(int(np.ceil((i+1)/6))) + 'a'
            string2 = 'v' + str(int(np.ceil((i+1)/6))) + 'b'
            string3 = 'v' + str(int(np.ceil((i+1)/6))) + 'c'
            string4 = 'v' + str(int(np.ceil((i+1)/6))) + 'd'
            string5 = 'v' + str(int(np.ceil((i+1)/6))) + 'e'
            string6 = 'v' + str(int(np.ceil((i+1)/6))) + 'f'
            verification_session_keys[string1] = str(index)
            verification_session_keys[string2] = str(index+1)
            verification_session_keys[string3] = str(index+2)
            verification_session_keys[string4] = str(index+3)
            verification_session_keys[string5] = str(index+4)
            verification_session_keys[string6] = str(index+5)
            index = index + 4
        else:
            string1 = 'v' + str(int(np.ceil((i+1)/6))) + 'a'
            string2 = 'v' + str(int(np.ceil((i+1)/6))) + 'b'
            string3 = 'v' + str(int(np.ceil((i+1)/6))) + 'c'
            string4 = 'v' + str(int(np.ceil((i+1)/6))) + 'd'
            string5 = 'v' + str(int(np.ceil((i+1)/6))) + 'e'
            string6 = 'v' + str(int(np.ceil((i+1)/6))) + 'f'
            verification_session_keys[string1] = str(index)
            verification_session_keys[string2] = str(index+1)
            verification_session_keys[string3] = str(index+2)
            verification_session_keys[string4] = str(index+3)
            verification_session_keys[string5] = '1'
            verification_session_keys[string6] = '2'
            index = index + 4


    for session in list(verification_session_keys.keys()):
        verification[session] = copy.deepcopy(verification[verification_session_keys[session]])
    for i in [str(x) for x in range(1,n_users*4+1)]:
        del verification[i]
    for session in list(verification_sessions_dict.keys()):
        verification[session] = copy.deepcopy(verification[verification_sessions_dict[session]])
        del verification[verification_sessions_dict[session]]

    verification_sessions_list_shuffled = sorted(list(verification_sessions_dict.keys()), key=lambda k: random.random())

    verification_shuffled = {}
    for session in verification_sessions_list_shuffled:
        verification_shuffled[session] = verification[session]
    del verification

    for session in list(verification_shuffled.keys()):
        for task_here in list(verification_shuffled[session].keys()):
            if task_here != task:
                del verification_shuffled[session][task_here]

    with open(new_folder + 'verification_shuffled_{}_{}.json'.format(set_type, task), 'w') as outfile:
        json.dump(verification_shuffled, outfile)


# task = 'gallery'
# results = np.loadtxt(new_folder + 'comparisons_list_results_{}_{}.txt'.format(task), dtype=float)
# labels_raw = open(new_folder + "comparisons_list_type_{}_{}.txt".format(task), "r").read().split('\n')[:-1]
# labels = [0 if x == 'genuine' else 1 for x in labels_raw]
#
# temp = list(zip(labels_raw, results))
# temp = [x for x in temp if x[0] != 'skilled']
# labels_raw_random, results_random = zip(*temp)
# labels_random = [0 if x == 'genuine' else 1 for x in labels_raw_random]
#
# temp = list(zip(labels_raw, results))
# temp = [x for x in temp if x[0] != 'random']
# labels_raw_skilled, results_skilled = zip(*temp)
# labels_skilled = [0 if x == 'genuine' else 1 for x in labels_raw_skilled]
#
#
# auc = AUC_compute(labels, results)
# auc_random = AUC_compute(labels_random, results_random)
# auc_skilled = AUC_compute(labels_skilled, results_skilled)

print("finished")
# t = 0