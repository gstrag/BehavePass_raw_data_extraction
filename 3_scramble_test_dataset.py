import json
import numpy as np

new_folder = 'extracted_data/'

with open(new_folder + 'datae.json') as f:
# with open(new_folder + 'data_val.json') as f:
    data = json.load(f)

enrolment_sessions_names = ['g1', 'g2']
verification_sessions_names = ['g3', 'g4', 's1', 's2']

enrolment = {}
keee = 1
for user in list(data.keys()):
    enrolment[str(keee)] = data[user][enrolment_sessions_names[0]]
    keee = keee + 1
    enrolment[str(keee)] = data[user][enrolment_sessions_names[1]]
    keee = keee + 1
    del data[user][enrolment_sessions_names[0]]
    del data[user][enrolment_sessions_names[1]]

verification = {}
keev = 1
for user in list(data.keys()):
    verification[str(keev)] = data[user][verification_sessions_names[0]]
    keev = keev + 1
    verification[str(keev)] = data[user][verification_sessions_names[1]]
    keev = keev + 1
    verification[str(keev)] = data[user][verification_sessions_names[2]]
    keev = keev + 1
    verification[str(keev)] = data[user][verification_sessions_names[3]]
    keev = keev + 1
    del data[user][verification_sessions_names[0]]
    del data[user][verification_sessions_names[1]]
    del data[user][verification_sessions_names[2]]
    del data[user][verification_sessions_names[3]]

del data

with open(new_folder + 'enrolment_test.json', 'w') as f:
    json.dump(enrolment, f)
with open(new_folder + 'verification_test.json', 'w') as f:
    json.dump(verification, f)

# with open(new_folder + 'enrolment.json') as f:
#     enrolment = json.load(f)
#
# with open(new_folder + 'verification.json') as f:
#     verification = json.load(f)

# keys_enrolment = np.loadtxt(new_folder + "keys_enrolment.txt", dtype=int)
# keys_verification = np.loadtxt(new_folder + "keys.txt", dtype=int)
#
# enrolment_scrambled = {}
# for session in list(enrolment.keys()):
#     enrolment_scrambled[session] = enrolment[str(keys_enrolment[int(session)-1])]
#
# with open(new_folder + 'enrolment_scrambled.json', 'w') as f:
#     json.dump(enrolment_scrambled, f)

