from data import *
from random import randint
from bisect import bisect
import os
import sqlite3
from numpy import random as nprandom

'''
Table Experience Point Awards
1.8 equal to 1/8, 1.6 to 1/6, 1.4 to 1/4, 1.3 to 1/3 and 1.2 to 1/2
'''
cr_table = [1.8, 1.6, 1.4, 1.3, 1.2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
            24, 25, 26, 27, 28, 29, 30]
'''
Table Experience Point Awards
Gives XP per encounter with CR as key
Column one is total XP, column two to four are individual XP for 1-3, 4-5 and 6+ players
1.8 equal to 1/8, 1.6 to 1/6, 1.4 to 1/4, 1.3 to 1/3 and 1.2 to 1/2
'''
cr_to_xp = {
    1.8: [50, 15, 15, 10],
    1.6: [65, 20, 15, 10],
    1.4: [100, 35, 25, 15],
    1.3: [135, 45, 35, 25],
    1.2: [200, 65, 50, 35],
    1: [400, 135, 100, 65],
    2: [600, 200, 150, 100],
    3: [800, 265, 200, 135],
    4: [1200, 400, 300, 200],
    5: [1600, 535, 400, 265],
    6: [2400, 800, 600, 400],
    7: [3200, 1070, 800, 535],
    8: [4800, 1600, 1200, 800],
    9: [6400, 2130, 1600, 1070],
    10: [9600, 3200, 2400, 1600],
    11: [12800, 4270, 3200, 2130],
    12: [19200, 6400, 4800, 3200],
    13: [25600, 8530, 6400, 4270],
    14: [38400, 12800, 9600, 6400],
    15: [51200, 17100, 12800, 8530],
    16: [76800, 25600, 19200, 12800],
    17: [102400, 34100, 25600, 17100],
    18: [153600, 51200, 38400, 25600],
    19: [204800, 68300, 51200, 34100],
    20: [307200, 102000, 76800, 51200],
    21: [409600, 137000, 102400, 68300],
    22: [614400, 205000, 153600, 102400],
    23: [819200, 273000, 204800, 137000],
    24: [1228800, 410000, 307200, 204800],
    25: [1638400, 546000, 409600, 273000],
    26: [2457600, 820000, 614400, 409600],
    27: [3276800, 1092000, 819200, 546000],
    28: [4915200, 1640000, 1228800, 819200],
    29: [6553600, 2184000, 1638400, 1092000],
    30: [9830400, 3280000, 2457600, 1638400]
}

'''
Possible arguments:
group_size - Number of groupmembers
group_lvl - Number of mean level in the group (rounded to the nearest whole number)
difficulty - Number to change the APL by
OR
cr - Challenge rating of the encounter
'''


def gen_monster_encounter(*args):
    if len(args) == 3:
        group_size = args[0]
        group_lvl = args[1]
        difficulty = args[2]
        if isinstance(group_size, str):
            if group_size.isDigit():
                group_size = int(group_size)
        if isinstance(group_lvl, str):
            if group_lvl.isDigit():
                group_lvl = int(group_lvl)
        assert isinstance(group_size, int)
        assert isinstance(group_lvl, int)
        assert isinstance(difficulty, int)
        apl = group_lvl
        if group_size <= 3:
            apl -= 1
        elif group_size >= 6:
            apl += 1
        cr = get_next_cr(apl, difficulty)
    elif len(args) == 1:
        cr = args[0]
    else:
        print("Wrong number of arguments! Either 1 for only CR or 3 for group_size, group_lvl and difficulty")
        return None

    # Randomly decide if this encounter is easy, average, challenging, hard or epic
    encounter_design = int(nprandom.choice([-1, 0, 1, 2, 3], p=[0.28, 0.55, 0.10, 0.05, 0.02]))
    cr = get_next_cr(cr, encounter_design)

    # open the monster database
    monsterDB = openDB()[0]

    xp_available = cr_to_xp[cr][0]
    min_number_of_monsters = 3
    max_number_of_monsters = 5
    actual_number_of_monsters = randint(min_number_of_monsters, max_number_of_monsters)

    # encounter contains tuples as elements with the structure (amount, name of monster, xp)
    encounter = []
    monsters = cr_splits(cr, actual_number_of_monsters)
    # rint('what it should be:', actual_number_of_monsters, '; what it is', sum([m[0] for m in monsters]))
    for monster in monsters:
        # print(monster)
        number_of_monsters = monster[0]
        if number_of_monsters == 1:
            encounter.append((1, getOneRandomMonster(monsterDB, monster[1], None)))
        else:
            # Decide if all Monster with the same CR are of the same type
            # All the same
            if randint(1, 3) == 1:
                encounter.append((number_of_monsters, getOneRandomMonster(monsterDB, monster[1], None)))
            else:
                number_of_next_monster = randint(1, number_of_monsters - 1)
                number_of_monsters = number_of_monsters - number_of_next_monster
                encounter.append((number_of_next_monster, getOneRandomMonster(monsterDB, monster[1], None)))
                while number_of_monsters > 0:
                    # print("number_of_monsters", number_of_monsters)
                    number_of_next_monster = randint(1, number_of_monsters)
                    number_of_monsters -= number_of_next_monster
                    encounter.append((number_of_next_monster, getOneRandomMonster(monsterDB, monster[1], None)))
    # print(encounter)
    closeDB(monsterDB)

    # Add same monsters together:
    # Keys are the monster types, values are the amount of this monster type
    encounter_set = {}
    for monster in encounter:
        monster = list(monster)
        amount, monster_type = monster
        if monster_type in encounter_set.keys():
            encounter_set[monster_type] += amount
        else:
            encounter_set[monster_type] = amount
    encounter = [(encounter_set[mons], mons) for mons in encounter_set.keys()]

    return print_encounter(encounter)


# Formatting for only one monster of an encounter
def print_monster(monster):
    # print(monster)
    number = monster[0]
    monster = monster[1]
    name = str(monster[monster_columns.index('name')])
    # cr = str(monster[monster_columns.index('cr')])
    url = str(monster[monster_columns.index('url')])
    xp = str(number * int(''.join(c for c in monster[monster_columns.index('xp')] if c.isdigit())))
    return str(number) + 'x <a href=\"' + url + '\" target=\"_blank\">' + name + '</a>, ' + xp


# Formatting for an entire encounter
def print_encounter(encounter):
    return '<br>\n'.join([print_monster(m) for m in encounter])


'''
Function to get a random monster based on cr and type from the monster database
'''
# These are the columns returned by the function getOneRandomMonster
monster_columns = ['name', 'cr', 'url', 'xp']


def getOneRandomMonster(monster_db, cr, types):
    monster_columns_sql = ', '.join(monster_columns)
    assert cr in cr_table
    if isinstance(cr, float):
        cr = str(cr).replace('.', '/')
    cursor = get_Cursor(monster_db)
    # print('CR:\t', cr)
    if types is None:
        cursor.execute('SELECT ' + monster_columns_sql + ' FROM monsters WHERE cr = \'' + str(cr) + '\' ORDER BY random() LIMIT 1;')
        monster_db.commit()
        random_monster = cursor.fetchone()
        # print('cr', cr, ';random_monster', random_monster)
        if random_monster[monster_columns.index('xp')] is None:
            random_monster = list(random_monster)
            random_monster[monster_columns.index('xp')] = '0'
            return tuple(random_monster)
        return random_monster
    else:
        if not isinstance(types, list):
            types = [types]
        type_sql = "("
        for act_type in types:
            type_sql += "\'" + act_type + "\',"
        type_sql = type_sql[:-1] + ")"
        cursor.execute('SELECT ' + monster_columns_sql + ' FROM monsters WHERE creature_type in ' + type_sql + ' LIMIT 1;')
        random_monster = cursor.fetchone()
        if isinstance(random_monster, list):
            return random_monster[0]
        else:
            return random_monster


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
Splits the CR to the given number of monster
'''


def cr_splits(cr, number_of_monsters):
    assert cr in cr_table
    assert isinstance(number_of_monsters, int)
    assert 0 < number_of_monsters <= 16
    # Table High CR Equivalencies
    number_of_creatures = [2, 3, 4, 6, 8, 12, 16]
    splits = [[(1, cr)]]
    for a in range(2, len(number_of_creatures) + 1):
        if get_next_cr(cr, -a) is not None:
            splits.append([(number_of_creatures[a - 2], get_next_cr(cr, -a))])
        else:
            break
    for a in range(0, len(splits) - 1):
        enc = splits[a]
        if enc[0][0] > 1 and get_next_cr(enc[0][1], -2) is not None:
            splits.append([enc[0], (2, get_next_cr(enc[0][1], - 2))])
    # rand_index = random.randint(0,len(splits) - 1)
    if number_of_monsters == 1:
        # print('It is only one monster!')
        return [(1, cr)]
    elif number_of_monsters in number_of_creatures:
        next_cr = get_next_cr(cr, - number_of_creatures.index(number_of_monsters) - 2)
        if next_cr is not None:
            return [(number_of_monsters, next_cr)]
        else:
            print('CR did not fit!')
            return None
    else:
        monster_fitting = number_of_creatures[bisect(number_of_creatures, number_of_monsters) - 1]
        cr_fitting = get_next_cr(cr, -(number_of_creatures.index(monster_fitting) + 2))
        if cr_fitting is None:
            return None
        elif (number_of_monsters - monster_fitting) == 1:
            rest_monster = cr_splits(cr_fitting, number_of_monsters - monster_fitting + 1)
            if rest_monster is not None:
                return [(monster_fitting - 1, cr_fitting)] + rest_monster
            else:
                print("Number of monsters (", number_of_monsters - monster_fitting + 1, ") with CR=", cr_fitting, " can't be fit to given CR!", sep='')
                return [(monster_fitting - 1, cr_fitting)]
        else:
            rest_monster = cr_splits(cr_fitting, number_of_monsters - monster_fitting)
            # print("rest_monster,",rest_monster)
            if rest_monster is not None:
                return [(monster_fitting, cr_fitting)] + rest_monster
            else:
                print("Number of monsters can't be fit to given CR!")
                return [(monster_fitting, cr_fitting)]
    return splits

if __name__ == '__main__':
    for a in range(1, 5):
        print(gen_monster_encounter(1))
