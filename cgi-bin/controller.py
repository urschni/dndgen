import cgi, cgitb
import time
from DnD import *
from loot_encounters_gen import *
import json
from random import randint
from PIL import Image
import numpy as np
import sqlite3
import os
cgitb.enable()

#Timestamp to create unique filenames
current_milli_time = lambda: int(round(time.time() * 1000.000))


'''
dungeon_size = (30,30)
site_offset = 1
inner_dungeon_size = (dungeon_size[0] - 2*site_offset, dungeon_size[1] - 2*site_offset)

w, h = dungeon_size[0], dungeon_size[1]
data = np.zeros((h, w, 3), dtype=np.uint8)

#Lay out inner quadratic rooms
number_of_tries = 10
max_min_roomsize = (2, 5)
for a in range(number_of_tries):
    actual_roomsize = randint(max_min_roomsize[0], max_min_roomsize[1])
    print(actual_roomsize)
    actual_position = (randint(site_offset, inner_dungeon_size[0] - actual_roomsize), randint(site_offset, inner_dungeon_size[1] -  actual_roomsize))
    print(actual_position)
    is_free = True
    for x in range(actual_position[0] - 1, actual_position[0] + actual_roomsize + 1):
        for y in range(actual_position[1] - 1, actual_position[1] + actual_roomsize + 1):
            """if x > inner_dungeon_size[0] or y > inner_dungeon_size[1] or x < :
                is_working = False
                break
            """
            if np.array_equal(data[x][y], [255,255,255]):
                is_free = False
                break
    if is_free:
        data[actual_position[0]:actual_position[0] + actual_roomsize, actual_position[1]:actual_position[1] + actual_roomsize] = [255,255,255]

#Markings for axis
#Pink
data[3:20,3] = [255,0,255]
#Blue
data[4,4:20] = [0,255,255]

#Generate entrances
number_of_entrances = 2
entrances = []
#0 - north, 1 - east, 2 - south, 3 - west
while(len(entrances) < number_of_entrances):
    direction = randint(0, 3)
    if direction == 0 or direction == 2:
        pos = randint(0, dungeon_size[0] - 1)
        if direction == 0:
            entrances.append((pos, 0))
        else:
            entrances.append((pos, dungeon_size[1] - 1))
    else:
        pos = randint(0, dungeon_size[1] - 1)
        if direction == 3:
            entrances.append((0, pos))
        else: 
            entrances.append((dungeon_size[1] - 1, pos))
print("Entrance positions:")
for entrance_pos in entrances:
    print(entrance_pos)
    data[entrance_pos[0],entrance_pos[1]] = [255,255,255]

'''


#Get the values from the form
form = cgi.FieldStorage()
dungeon_name = form.getvalue('dungeon_name')
dungeon_size = form.getvalue('dungeon_size')
dungeon_lvl = form.getvalue('dungeon_lvl')
party_size = form.getvalue('party_size')
monster_allow = form.getvalue('monster_allow')
monster_type = form.getvalue('monster_type')
trap_allow = form.getvalue('trap_allow')
trap_freq = form.getvalue('trap_freq')
deadend_allow = form.getvalue('deadend_allow')
loot_allow = form.getvalue('loot_allow')

#Debug message with all attribtes from the HTML-form
all_attributes = ""
for x in form:
    all_attributes = all_attributes + str(form[x])[16:] + "<br>"

yes_no_to_bool = {'yes': True, 'no': False, None: None}
#Process HTML form data
#Process dungeon_size
if 'small' == dungeon_size:
    dungeon_size = (10, 10)
    max_room_size = (3, 3)
elif 'medium' == dungeon_size:
    dungeon_size = (20, 20)
    max_room_size = (5, 5)
else:
    dungeon_size = (30, 30)
    max_room_size = (7, 7)
#Process dungeon_lvl
dungeon_lvl = int(dungeon_lvl)
#Process party_size
party_size = int(party_size)
#Process monster_allow
monster_allow = yes_no_to_bool[monster_allow]
#Process monster_type
#monster_type comes right from the html-form
#Process trap_allow
trap_allow = yes_no_to_bool[trap_allow]
#Process trap_freq
if trap_freq == 'low':
    trap_freq = 0.1
elif trap_freq == 'medium':
    trap_freq = 0.3
else:
    trap_freq = 0.5
#Process deadend_allow
deadend_allow = yes_no_to_bool[deadend_allow]
#Process loot_allow
loot_allow = yes_no_to_bool[loot_allow]

#Create Dungeon
dungeon = Dungeon(dungeon_size[0], dungeon_size[1], 50)
dungeon.multiRoom(5, max_room_size[0], max_room_size[1], 1)
map = dungeon.returnArray()

#Generate encounter
number_of_encounter = np.amax(map) - 1
encounter = ''
if monster_allow or loot_allow:
    encounter = '<h2>Encounter</h2>\n'
    for room_number in range(1, number_of_encounter):
        encounter += '<h3>Room ' + str(room_number) + '</h3>\n'
        if monster_allow:
            encounter += '<h4>Monster:</h4>\n'
            encounter += gen_encounter(dungeon_lvl) + '\n'
        if loot_allow:
            encounter += '<h4>Loot:</h4>\n'
            encounter += gen_loot(dungeon_lvl)

def black_white(x):
    return 0 if x == 0 else 1
black_white = np.vectorize(black_white)
#Generate Image from numpyArray and resize it
normalize = int(255/np.amax(map)) if np.amax(map) > 0 else 1
img = Image.fromarray(black_white(map), mode='1')
img = img.resize((500,500))
img = img.rotate(90)
img.save('./my.png')

include_debug = True
#Print the HTML page for the client
print("Content-Type: text/html; charset=utf-8\n")
print("<html>")
print("<meta charset=\"utf-8\">")
print("<head> <title>Dungeon Generator</title> ")
print("<link rel=\"shortcut icon\" href=\"http://localhost:8000/graphics/icon.ico\" type=\"image/vnd.microsoft.icon\" />")
print("<style>")
print("body{background-image: url(http://localhost:8000/graphics/bg.png);}")
print(".content {max-width: 500px;margin: auto;padding: 10px;background-color: rgba(255,255,255,0.85);line-height: 2;font-size: 20px;}")
print("input{font-size: 18px;}")
print("select{font-size: 18px;}")
print(".center {display: block;margin-left: auto;margin-right: auto;}")
print("</style>")
print("</head>")
print("<body>")
print("<img class=\"center\" src=\"http://localhost:8000/graphics/DungeonGen.png\" alt=\"Dungeon Logo\" style=\"width:500px\">")
print("<div class=\"content\">")
if dungeon_name is not None:
    print("<h1>" + dungeon_name + "</h1>")
else:
    print("<h1>Dungeon is generated!</h1>")
if include_debug:
    print("<h2>Values:</h2>")
    print(all_attributes)
print("<br><img src=\"/my.png\" alt=\"Dungeon Map\"><br>")
print(encounter)
print("</div>")
print("</body>")
print("</html>")
