import cgi, cgitb
import time
from DnD import *
from loot_encounters_gen import *
from monster_encounters_gen import *
from response_gen import *
from random import randint
from PIL import Image
import numpy as np

cgitb.enable()

#Timestamp to create unique filenames
current_milli_time = lambda: int(round(time.time() * 1000.000))

#Get the values from the form
form = cgi.FieldStorage()
dungeon_name = form.getvalue('dungeon_name')
dungeon_size_box = form.getvalue('dungeon_size_box')
dungeon_height = form.getvalue('dungeon_size_height')
dungeon_length = form.getvalue('dungeon_size_length')
dungeon_size = form.getvalue('dungeon_size')
room_density = form.getvalue('room_density')
dungeon_lvl = form.getvalue('dungeon_lvl')
party_size = form.getvalue('party_size')
monster_allow = form.getvalue('monster_allow')
monster_type = form.getvalue('monster_type')
trap_allow = form.getvalue('trap_allow')
trap_freq = form.getvalue('trap_freq')
deadend_allow = form.getvalue('deadend_allow')
loot_allow = form.getvalue('loot_allow')
img_res = form.getvalue('img_res')

#Debug message with all attribtes from the HTML-form
all_attributes = ""
for x in form:
    all_attributes = all_attributes + str(form[x])[16:] + "<br>"

yes_no_to_bool = {'yes': True, 'no': False, None: None}
#Process HTML form data
#Process dungeon_size
dungeon_size_box = yes_no_to_bool[dungeon_size_box]
if dungeon_size_box:
	if (dungeon_height and dungeon_length) != None:
		height = int(dungeon_height)
		length = int(dungeon_length)
		dungeon_size = (length,height)
		max_room_size = (int(length/4),int(height/4))
	else:
		dungeon_size = (20, 20)
		max_room_size = (5, 5)
else:
	if 'small' == dungeon_size:
		dungeon_size = (10, 10)
		max_room_size = (3, 3)
	elif 'medium' == dungeon_size:
		dungeon_size = (20, 20)
		max_room_size = (5, 5)
	else:
		dungeon_size = (30, 30)
		max_room_size = (7, 7)
#Process room_density
if room_density == 'low':
	room_density = 0.5
elif room_density == 'medium':
	room_density = 1
else:
	room_density = 1.5
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
#Process img_res
if img_res == 'low':
	img_len = 250
elif img_res == 'medium':
	img_len = 500
elif img_res == 'high':
	img_len = 1000
elif img_res == 'very_high':
	img_len = 2000
else:
	img_len = 4000
img_height = int(img_len/dungeon_size[0])*dungeon_size[1]
img_res = (img_len,img_height)

#Create Dungeon
dungeon = Dungeon(dungeon_size[0], dungeon_size[1], 50)
dungeon.multiRoom(5, 2)
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
            encounter += gen_monster_encounter(dungeon_lvl) + '\n'
        if loot_allow:
            encounter += '<h4>Loot:</h4>\n'
            encounter += gen_loot(dungeon_lvl)

bw_map = np.zeros((dungeon_size[0], dungeon_size[1], 3), np.uint8)
bw_map[map > 0] = [255, 255, 255]
bw_map[map < -1] = [255, 255, 255]
bw_map[map == 0] = [0, 0, 0]
bw_map[map == -1] = [128, 128, 128]
img = Image.fromarray(bw_map, mode='RGB')
img = img.resize((500, 500))
img = img.rotate(90)
img.save('./my.png')

include_debug = True


#Send attributes to the HTML page- printer

printResponse(include_debug, dungeon_name, all_attributes, encounter) 
