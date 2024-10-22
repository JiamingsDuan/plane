from itertools import chain, combinations

import pandas as pd

label_sets = ['BRT_0401', 'BRT_0404', 'BRT_040B', 'BRT_040C',
              'BRT_040D', 'BRT_040E', 'BRT_040F', 'BRT_040G',
              'BRT_040H', 'BRT_040K', 'BRT_040T']

# business_label = []
KC_ID_sets = pd.read_csv('data/KC_ID.csv')['KC_ID'].to_list()


# eliminate only business_id
def eliminate_KC_ID(ls, elements):
    return [x for x in ls if x not in elements]


# calculate all in bool
def all_in(list1, list2):
    return all(i in list2 for i in list1)


# calculate all out bool
def all_out(list1, list2):
    for item in list1:
        if item in list2:
            return False
    return True


def obtain_combination(need_combination):
    combination_list = []
    for r in range(1, len(need_combination) + 1):
        for combination in combinations(need_combination, r):
            combination_list.append(list(combination))
    return combination_list


def str_in_list(s, l3):
    return s in l3


def generate_id(only, rst):
    if (all_in(only, rst)) and (all_out(eliminate_KC_ID(KC_ID_sets, only), rst)):
        return True


def determine_KC_ID(business_id_list, rst_label):
    rt = business_id_list
    sec_label = 'KC_None'
    fir_label = 'KC_None'
    # KC_0401
    if generate_id(['040O0204'], rst=rt):
        fir_label = 'KC_0401'
    else:
        combination1 = obtain_combination(['042E0106', '040O0270', '042E0150', '040O0293'])
        for comb in combination1:
            comb = list(chain(['040O0204'], comb))
            if generate_id(only=comb, rst=rt):
                fir_label = 'KC_0401'

    # KC_0402
    if generate_id(['040O0212', '040O0204'], rst=rt):
        fir_label = 'KC_0402'
    else:
        combination2 = obtain_combination(['042E0106', '040O0270', '042E0150', '040O0293'])
        for comb in combination2:
            comb = list(chain(['040O0212', '040O0204'], comb))
            if generate_id(only=comb, rst=rt):
                fir_label = 'KC_0402'

    # KC_0403
    combination31 = obtain_combination(['042F0801', '042F0802'])
    combination32 = obtain_combination(['042E0106', '040O0270', '042E0150', '040O0293'])
    for comb1 in combination31:
        comb1 = list(chain(comb1, ['040O0204']))
        if generate_id(only=comb1, rst=rt):
            fir_label = 'KC_0403'
        for comb2 in combination32:
            comb2 = list(chain(comb1, comb2))
            if generate_id(only=comb2, rst=rt):
                fir_label = 'KC_0403'

    # KC_0404
    combination41 = obtain_combination(['042F0801', '042F0802'])
    combination42 = obtain_combination(['042E0106', '040O0270', '042E0150', '040O0293'])
    for comb1 in combination41:
        comb1 = list(chain(comb1, ['040O0212', '040O0204']))
        if generate_id(only=comb1, rst=rt):
            fir_label = 'KC_0404'
        for comb2 in combination42:
            comb2 = list(chain(comb1, comb2))
            if generate_id(only=comb2, rst=rt):
                fir_label = 'KC_0404'

    # KC_0405
    combination51 = obtain_combination(['042E0146', '040O0238'])
    combination52 = obtain_combination(['042E0106', '040O0270', '042E0150', '040O0293'])
    for comb1 in combination51:
        if generate_id(only=comb1, rst=rt):
            fir_label = 'KC_0405'
        for comb2 in combination52:
            comb2 = list(chain(comb1, comb2))
            if generate_id(only=comb2, rst=rt):
                fir_label = 'KC_0405'

    # KC_0406
    combination61 = obtain_combination(['042E0146', '040O0238'])
    combination62 = obtain_combination(['042E0106', '040O0270', '042E0150', '040O0293'])
    for comb1 in combination61:
        comb1 = list(chain(comb1, ['040O0204']))
        if generate_id(only=comb1, rst=rt):
            fir_label = 'KC_0406'
        for comb2 in combination62:
            comb2 = list(chain(comb1, comb2))
            if generate_id(only=comb2, rst=rt):
                fir_label = 'KC_0406'

    # KC_0407
    combination7 = obtain_combination(['042E0106', '040O0270'])
    for comb1 in combination7:
        if generate_id(only=comb1, rst=rt):
            fir_label = 'KC_0407'

    # # KC_0408
    if generate_id(only=[], rst=rt) and str_in_list(s=rst_label, l3=label_sets):
        fir_label = 'KC_0408'

    # KC_0409
    combination9 = obtain_combination(['042E0150', '040O0293'])
    for comb1 in combination9:
        if generate_id(only=comb1, rst=rt):
            fir_label = 'KC_0409'

    return fir_label
