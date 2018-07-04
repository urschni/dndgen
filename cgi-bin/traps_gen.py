from random import random
from data import *

'''
Table Experience Point Awards
1.8 equal to 1/8, 1.6 to 1/6, 1.4 to 1/4, 1.3 to 1/3 and 1.2 to 1/2
'''
cr_table = [1.8, 1.6, 1.4, 1.3, 1.2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
            24, 25, 26, 27, 28, 29, 30]
trap_columns = ['name', 'url', 'disable_device', 'perception', 'cr']


# Formatted output for trap generation
def print_trap(traps):
    output = ""
    for trap in traps:
        number = trap[0]
        cur_trap = trap[1]
        url = cur_trap[trap_columns.index('url')]
        name = cur_trap[trap_columns.index('name')]
        output += str(number) + 'x <a href=\"' + url + '\" target=\"_blank\">' + name + '</a><br>\n'
    return output


'''
Function to get smaller or bigger CR
cr is the actual CR and "change_by" gives the number of steps to make cr bigger (positive number) or smaller (negative number)
'''


def get_next_cr(cr, change_by):
    assert (isinstance(change_by, int))
    assert (isinstance(cr, (int, float)))
    assert cr in cr_table
    temp_cr = cr_table.index(cr) + change_by
    if temp_cr < 0:
        # print("CR is lower than 1/8")
        return 1.8
    elif temp_cr > 34:
        # print("CR is bigger than 30, ")
        return 30
    return cr_table[temp_cr]


'''
Gives one random trap from the trap_db dependend on the cr and the difficulty range
difficulty[0] gives the maximal CR of the returned trap dependent on the given CR with CR + difficulty[0]
difficulty[1] gives the minimal CR of the returned trap dependent on the given CR with CR - difficulty[1]
'''


def get_random_trap(trap_db, cr, difficulty=(1, 2)):
    trap_columns_sql = ', '.join(trap_columns)
    cursor = get_Cursor(trap_db)
    cursor.execute('SELECT ' + trap_columns_sql + ' FROM traps WHERE cr <= ' + str(cr + difficulty[0]) + ' AND cr >= ' + str(cr - difficulty[1]) + ' ORDER BY random() LIMIT 1;')
    random_trap = cursor.fetchone()
    return random_trap


'''
Generate traps, e. g. for one room, dependent on the CR and the difficulty
difficulty[0] gives the maximal CR of the returned traps dependend on the given CR with CR + difficulty[0]
difficulty[1] gives the minimal CR of the returned traps dependend on the given CR with CR - difficulty[1]
chance is a floatvalue between 0 and 1 that gives the chance of getting a trap
'''


def gen_traps(cr, chance, difficulty=(1, 2), chance_to_get_multiple_traps=0.05):
    assert cr in cr_table
    assert isinstance(chance, (float, int))
    assert 0 <= chance <= 1

    trap_db = openDB()[2]

    # traps contains elements with the structure described in trap_columns
    traps = []
    if random() <= chance:
        next_trap = get_random_trap(trap_db, cr, difficulty)
        if next_trap in [tra[1] for tra in traps]:
            traps[[tra[1] for tra in traps].index(next_trap)][0] += 1
        else:
            traps.append([1, next_trap])

        # 5 % chance to get another trap
        while random() <= chance_to_get_multiple_traps:
            next_trap = get_random_trap(trap_db, cr, difficulty)
            if next_trap in [tra[1] for tra in traps]:
                traps[[tra[1] for tra in traps].index(next_trap)][0] += 1
            else:
                traps.append([1, next_trap])

    if len(traps) == 0:
        return None
    else:
        return print_trap(traps)


if __name__ == '__main__':
    for a in range(1, 21):
        print(gen_traps(1, 1.0))
