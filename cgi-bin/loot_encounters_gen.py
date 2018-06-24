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
Function to split an integer value into pp, gp, sp and cp to print it out
output format: str with W pp X gp Y sp Z cp if W,X,Y,Z is bigger than 0
'''
def currency_split(value, currency):
    if isinstance(value, str):
        value = int(value)
    value = get_cp(value, currency)
    value_str = ''
    if value >= 1000:
        value_str += str(int(value / 1000)) + ' pp'
        value -= int(value / 1000)
    elif value >= 100:
        value_str += str(int(value / 100)) + ' gp'
        value -= int(value / 100)
    elif value >= 10:
        value_str += str(int(value / 10)) + ' sp'
        value -= int(value / 10)
    elif value >= 1:
        value_str += str(int(value)) + ' cp'
        value -= int(value)
    return value_str

'''
Generate one loot, dependend on the CR and the progression_speed
progression_speed correspons: 0-slow, 1-medium, 2-fast
'''
def gen_loot(cr, progression_speed=1):
    assert cr in cr_table
    assert progression_speed in [0, 1, 2]

    budget = treasure_per_encounter[cr][progression_speed]
    budget = get_cp(budget, 'gp')
    #print('start budget', budget)

    #loot contains elements with the structure (number of object, object, value)
    loot = []
    gem_values = sorted(gems.keys())
    if budget < min(gem_values):
        loot.append((budget, 'cp', budget))
        return print_loot(loot)
    while budget > min(gem_values):
        smallest_fitting_gem = gem_values[bisect(gem_values, budget) - 1]
        #print(smallest_fitting_gem)
        number = int(budget / smallest_fitting_gem)
        #print(number)
        budget = budget - number * smallest_fitting_gem
        #print('budget', budget)
        loot.append((number, gems[smallest_fitting_gem][randint(0, len(gems[smallest_fitting_gem]) - 1)], number * smallest_fitting_gem))
    if budget > 0:
        loot.append((budget, 'cp', budget))
    #print(loot)
    return print_loot(loot)
    

    
#Formatted output for loot generation
def print_loot(loot):
    output = ""
    for item in loot:
        number, kind, value = item
        value = currency_split(value, 'gp')
        output += str(number) + 'x ' + kind + ', ' + str(value) + '<br>\n'
    return output


'''
if __name__ == '__main__':
    for a in range(28, 30):
        print('------------------------\n', str(a))
        for b in range(0, 1000):
            print(gen_encounter(a))
    #print(gen_loot(5))
'''
