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
Table Treasure Values per Encounter
Column one for slow, two for medium, three for fast
Numbers are in GP
'''
treasure_per_encounter = {
    1.8: [20, 35, 50],
    1.6: [30, 45, 65],
    1.4: [40, 65, 100],
    1.3: [55, 85, 135],
    1.2: [85, 130, 200],
    1: [170, 260, 400],
    2: [350, 550, 800],
    3: [550, 800, 1200],
    4: [750, 1150, 1700],
    5: [1000, 1550, 2300],
    6: [1350, 2000, 3000],
    7: [1750, 2600, 3900],
    8: [2200, 3350, 5000],
    9: [2850, 4250, 6400],
    10: [3650, 5450, 8200],
    11: [4650, 7000, 10500],
    12: [6000, 9000, 13500],
    13: [7750, 11600, 17500],
    14: [10000, 15000, 22000],
    15: [13000, 19500, 29000],
    16: [16500, 25000, 38000],
    17: [22000, 32000, 48000],
    18: [28000, 41000, 62000],
    19: [35000, 53000, 79000],
    20: [44000, 67000, 100000],
    21: [55000, 84000, 125000],
    22: [69000, 104000, 155000],
    23: [85000, 127000, 190000],
    24: [102000, 155000, 230000],
    25: [125000, 185000, 275000],
    26: [150000, 220000, 330000],
    27: [175000, 260000, 390000],
    28: [205000, 305000, 460000],
    29: [240000, 360000, 540000],
    30: [280000, 420000, 630000]
}

gems = {
    1000: ['agates', 'azurite', 'blue quartz', 'hematite', 'lapis lazuli', 'malachite', 'obsidian', 'rhodochrosite', 'tigereye', 'turquoise', 'freshwater (irregular) pearl'],
    5000: ['bloodstone', 'carnelian', 'chalcedony', 'chrysoprase', 'citrine', 'jasper', 'moonstone', 'onyx', 'peridot', 'rock crystal (clear quartz)', 'sard', 'sardonyx', 'rose quartz', 'smoky quartz', 'star rose quartz', 'zircon'],
    10000: ['amber', 'amethyst', 'chrysoberyl', 'coral', 'red garnet', 'brown-green garnet', 'jade', 'jet', 'white pearl', 'golden pearl', 'pink pearl', 'silver pearl', 'red spinel', 'red-brown spinel', 'deep green spinel', 'tourmaline'],
    50000: ['alexandrite', 'aquamarine', 'violet garnet', 'black pearl', 'deep blue spinel', 'golden yellow topaz'],
    100000: ['emerald', 'white opal', 'black opal', 'fire opal', 'blue sapphire', 'fiery yellow corundum', 'rich purple corundum', 'blue star sapphire', 'black star sapphire'],
    500000: ['clearest bright green emerald', 'diamond', 'jacinth', 'ruby']
}

#Connect to the databases
def openDB():

    #ABSOLUTE filepaths are important or the databases are not found!
    path = os.path.abspath(__file__)

    path = path[:path.rfind(os.sep) + 1]
    print(path)

    monsterdb = sqlite3.connect(path + '../data/monsters.db')
    itemdb = sqlite3.connect(path + '../data/items.db')

    cursorMonsters = monsterdb.cursor()
    cursorItems = itemdb.cursor()
    return monsterdb, itemdb

'''
Function to get a random monster based on cr and type from the monster database
'''
#These are the columns returned by the function getOneRandomMonster
monster_columns = ['name', 'cr', 'url', 'xp']
def getOneRandomMonster(monsterDB, cr, types):
    monster_columns_sql = ', '.join(monster_columns)
    assert cr in cr_table
    if isinstance(cr, float):
        cr = str(cr).replace('.', '/')
    cursor = monsterDB.cursor()
    if types is None:
        cursor.execute('SELECT ' + monster_columns_sql + ' FROM monsters WHERE cr = ' + str(cr) + ' ORDER BY random() LIMIT 1;')
        randomMonster = cursor.fetchall()
        return randomMonster
    else:
        if not isinstance(types, list):
            types = [types]
        type_sql = "("
        for type in types:
            type_sql += "\'" + type + "\',"
        type_sql = type_sql[:-1] + ")"
        cursor.execute('SELECT ' + monster_columns_sql + ' FROM monsters WHERE creature_type in ' + type_sql + ' LIMIT 1;')
        randomMonster = cursor.fetchall()
        return randomMonster

def print_monster(monster):
    name = str(monster[monster_columns.index('name')])
    #cr = str(monster[monster_columns.index('cr')])
    url = str(monster[monster_columns.index('url')])
    xp = str(monster[monster_columns.index('xp')])
    return '<a href=\"' + url + '\" target=\"_blank\">' + name + '</a>, ' + xp

def print_encounter(encounter):
    return '<br>\n'.join([print_monster(m) for m in encounter])


'''
Function to get smaller or bigger CR
cr is the actual CR and "change_by" gives the number of steps to make cr bigger (positive number) or smaller (negative number)
'''
def get_next_cr(cr, change_by):
    assert (isinstance(change_by, int))
    assert (isinstance(cr, (int, float)))
    assert cr in cr_table
    temp_cr = cr_table.index(cr) + change_by
    if (temp_cr < 0):
        print("CR is lower than 1/8")
        return None
    elif (temp_cr > 34):
        print("CR is bigger than 30, ")
        return None
    return cr_table[temp_cr]


'''
Function to get a value in cp dependent on the currency
currency can have the following currencys: cp, sp, gp, pp
'''
def get_cp(number, currency):
    assert isinstance(number, int)
    assert isinstance(currency, str)
    assert currency.lower() in ['cp', 'sp', 'gp', 'pp']

    currency = currency.lower()
    if currency == "cp":
        return number
    elif currency == 'sp':
        return number * 10
    elif currency == 'gp':
        return number * 100
    elif currency == 'pp':
        return number * 1000
    else:
        return None


'''
Generate one loot, dependend on the CR and the progression_speed
progression_speed correspons: 0-slow, 1-medium, 2-fast
'''
def gen_loot(cr, progression_speed=1):
    assert cr in cr_table
    assert progression_speed in [0, 1, 2]

    budget = treasure_per_encounter[cr][progression_speed]
    budget = get_cp(budget, 'gp')
    print('start budget', budget)

    #loot contains elements with the structure (number of object, object, value)
    loot = []
    gem_values = sorted(gems.keys())
    if budget < min(gem_values):
        loot.append((budget, 'cp', budget))
    while budget > min(gem_values):
        smallest_fitting_gem = gem_values[bisect(gem_values, budget) - 1]
        print(smallest_fitting_gem)
        number = int(budget / smallest_fitting_gem)
        print(number)
        budget = budget - number * smallest_fitting_gem
        print('budget', budget)
        loot.append((number, gems[smallest_fitting_gem][randint(0, len(gems[smallest_fitting_gem]) - 1)], number * smallest_fitting_gem))
    if budget > 0:
        loot.append((budget, 'cp', budget))
    return loot


'''
Possible arguments:
group_size - Number of groupmembers
group_lvl - Number of mean level in the group (rounded to the nearest whole number)
difficulty - Number to change the APL by
OR
cr - Challenge rating of the encounter
'''
def gen_encounter(*args):
    if len(args) == 3:
        group_size = args[0]
        group_lvl = args[1]
        difficulty = args[2]
        if (isinstance(group_size, str)):
            if (group_size.isDigit()):
                group_size = int(group_size)
        if (isinstance(group_lvl, str)):
            if (group_lvl.isDigit()):
                group_lvl = int(group_lvl)
        assert isinstance(group_size, int)
        assert isinstance(group_lvl, int)
        assert isinstance(difficulty, int)
        apl = group_lvl
        if group_size <= 3:
            apl -= 1
        elif group_size >= 6:
            apl += 1
        cr = apl + difficulty
    elif len(args) == 1:
        cr = args[0]
    else:
        print("Wrong number of arguments! Either 1 for only CR or 3 for group_size, group_lvl and difficulty")
        return None

    #Randomly decide if this encounter is easy, average, challenging, hard or epic
    encounter_design = int(nprandom.choice([-1, 0, 1, 2, 3], p=[0.28, 0.55, 0.10, 0.05, 0.02]))
    cr = get_next_cr(cr, encounter_design)

    #open the monster database
    monsterDB = openDB()[0]

    xp_available = cr_to_xp[cr][0]
    min_number_of_monsters = 3
    max_number_of_monsters = 5
    actual_number_of_monsters = randint(min_number_of_monsters, max_number_of_monsters)

    encounter = []
    monsters = cr_splits(cr, actual_number_of_monsters)
    for monster in monsters:
        number_of_monsters = monster[0]
        if number_of_monsters == 1:
            encounter += getOneRandomMonster(monsterDB, monster[1], None)
        else:
            #Decide if all Monster witht he same CR are of the same type
            #All the same
            if randint(1,3) == 1:
                encounter += getOneRandomMonster(monsterDB, monster[1], None)
            else:
                number_of_next_monster = randint(1, number_of_monsters - 1)
                number_of_monsters = number_of_monsters - number_of_next_monster
                encounter += getOneRandomMonster(monsterDB, monster[1], None)
                while number_of_monsters > 0:
                    print("number_of_monsters", number_of_monsters)
                    number_of_next_monster = randint(1, number_of_monsters)
                    number_of_monsters = number_of_monsters - number_of_next_monster
                    encounter += getOneRandomMonster(monsterDB, monster[1], None)
    return print_encounter(encounter)


#Splits the CR to the given number of monster
def cr_splits(cr, number_of_monsters):
    assert cr in cr_table
    assert isinstance(number_of_monsters, int)
    assert number_of_monsters <= 16 and number_of_monsters > 0
    # Table High CR Equivalencies
    number_of_creatures = [2, 3, 4, 6, 8, 12, 16]
    splits = [[(1, cr)]]
    for a in range(2, len(number_of_creatures) + 1):
        if get_next_cr(cr, -a) is not None:
            splits.append([(number_of_creatures[a - 2], get_next_cr(cr, -a))])
        else:
            break
    for a in range(0,len(splits) - 1):
        enc = splits[a]
        if enc[0][0] > 1 and get_next_cr(enc[0][1], -2) is not None:
            splits.append([enc[0], (2, get_next_cr(enc[0][1], - 2))])
    # rand_index = random.randint(0,len(splits) - 1)
    if number_of_monsters == 1:
        return [(1, cr)]
    elif number_of_monsters in number_of_creatures:
        next_cr = get_next_cr(cr, - number_of_creatures.index(number_of_monsters) - 2)
        if next_cr is not None:
            return [(number_of_monsters, next_cr)]
        else:
            return None
    else:
        monster_fitting = number_of_creatures[bisect(number_of_creatures, number_of_monsters) - 1]
        cr_fitting = get_next_cr(cr, -(number_of_creatures.index(monster_fitting) + 2))
        if cr_fitting is None:
            return None
        elif(number_of_monsters - monster_fitting) == 1:
            rest_monster = cr_splits(cr_fitting, number_of_monsters - monster_fitting + 1)
            if rest_monster is not None:
                return [(monster_fitting - 1, cr_fitting)] + rest_monster
            else:
                print("Number of monsters can't be fit to given CR!")
                return None
        else:
            rest_monster = cr_splits(cr_fitting, number_of_monsters - monster_fitting)
            print("rest_monster,",rest_monster)
            if rest_monster is not None:
                return [(monster_fitting, cr_fitting)] + rest_monster
            else:
                print("Number of monsters can't be fit to given CR!")
                return None
    return splits

if __name__ == '__main__':
    gen_encounter(5)