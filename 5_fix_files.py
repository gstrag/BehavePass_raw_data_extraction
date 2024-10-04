import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import copy, json
import random, string, sys
from itertools import chain

task = 'gallery'
num_users = 20
new_folder = 'extracted_data/'
with open(new_folder + 'enrolment_sessions_dict_test_{}.json'.format(task)) as f:
    enrolment_sessions_test_dict = json.load(f)

with open(new_folder + 'verification_sessions_dict_test_{}.json'.format(task)) as f:
    verification_sessions_test_dict = json.load(f)

pseu_enrolment_sessions = list(enrolment_sessions_test_dict.keys())
pseu_verification_sessions = list(verification_sessions_test_dict.keys())
enrolment_sessions = [enrolment_sessions_test_dict[x] for x in pseu_enrolment_sessions]
verification_sessions = [verification_sessions_test_dict[x] for x in pseu_verification_sessions]

plain_comparison_list_0 = []
for i in range(num_users):
    plain_comparison_list_0.append([enrolment_sessions[0+i*2],
                                  [verification_sessions[0+i*6], verification_sessions[1+i*6], verification_sessions[2+i*6],
                                   verification_sessions[3+i*6], verification_sessions[4+i*6], verification_sessions[5+i*6]]])
    plain_comparison_list_0.append([enrolment_sessions[1+i*2],
                                  [verification_sessions[0+i*6], verification_sessions[1+i*6], verification_sessions[2+i*6],
                                   verification_sessions[3+i*6], verification_sessions[4+i*6], verification_sessions[5+i*6]]])

plain_comparison_list = []
for comparisons in plain_comparison_list_0:
    for verification_session in comparisons[1]:
        plain_comparison_list.append([comparisons[0], verification_session])


reversed_enrolment_sessions_test_dict = {v: k for k, v in enrolment_sessions_test_dict.items()}
reversed_verification_sessions_test_dict = {v: k for k, v in verification_sessions_test_dict.items()}
comparisons_list = []
for plain_comparison in plain_comparison_list:
    comparisons_list.append(reversed_enrolment_sessions_test_dict[plain_comparison[0]] + ' ' + reversed_verification_sessions_test_dict[plain_comparison[1]])

comparisons_type = []
for element in plain_comparison_list:
    if element[1][-1] == 'a' or element[1][-1] == 'b':
        comparisons_type.append('genuine')
    if element[1][-1] == 'c' or element[1][-1] == 'd':
        comparisons_type.append('skilled')
    if element[1][-1] == 'e' or element[1][-1] == 'f':
        comparisons_type.append('random')

c = list(zip(comparisons_list, comparisons_type))
random.shuffle(c)
comparisons_list, comparisons_type = zip(*c)

to_save_comparisons_list = [str(x) + '\n' for x in comparisons_list]
with open(new_folder + 'comparisons_list_test_{}_NEW.txt'.format(task), mode='w') as out_file:
    out_file.write(''.join(to_save_comparisons_list))

to_save_comparisons_list_type = [str(x) + '\n' for x in comparisons_type]
with open(new_folder + 'comparisons_list_type_test_{}_NEW.txt'.format(task), mode='w') as out_file:
    out_file.write(''.join(to_save_comparisons_list_type))


t = 0