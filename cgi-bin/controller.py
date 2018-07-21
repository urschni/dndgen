import cgi
import cgitb
import time
from DnD import *
from loot_encounters_gen import *
from monster_encounters_gen import *
from traps_gen import *
from response_gen import *
from create_response_html import *
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from random import randint
import numpy as np
import uuid

cgitb.enable()

# Timestamp to create unique filenames
current_milli_time = lambda: int(round(time.time() * 1000.000))

# Get the values from the form
form = cgi.FieldStorage()
dungeon_name = form.getvalue('dungeon_name')
dungeon_size_allow = form.getvalue('tapset')
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

# Debug message with all attribtes from the HTML-form
all_attributes = ""
for x in form:
    all_attributes = all_attributes + str(form[x])[16:] + "<br>"

yes_no_to_bool = {'yes': True, 'no': False, None: None}
# Process HTML form data
# Process dungeon_size

if 'small' == dungeon_size:
    dungeon_size = (20, 20)
    max_room_size = (5, 5)
elif 'medium' == dungeon_size:
    dungeon_size = (40, 40)
    max_room_size = (8, 8)
else:
    dungeon_size = (60, 60)
    max_room_size = (12, 12)
# Process room_density
if room_density == 'low':
    room_num = randint(4,10)
    room_density = [int(room_num/2), room_num]
elif room_density == 'medium':
    room_num = randint(8,14)
    room_density = [int(room_num/2), room_num]
else:
    room_num = randint(12,18)
    room_density = [int(room_num/2), room_num]
# Process dungeon_lvl
dungeon_lvl = int(dungeon_lvl)
# Process party_size
party_size = int(party_size)
# Process monster_allow
monster_allow = yes_no_to_bool[monster_allow]
# Process monster_type
# monster_type comes right from the html-form
# Process trap_allow
trap_allow = yes_no_to_bool[trap_allow]
# Process trap_freq
if trap_freq == 'low':
    trap_freq = 0.2
elif trap_freq == 'medium':
    trap_freq = 0.4
else:
    trap_freq = 0.6
# Process dead end_allow
deadend_allow = yes_no_to_bool[deadend_allow]
# Process loot_allow
loot_allow = yes_no_to_bool[loot_allow]
# Process img_res

img_len_diff = 2000 % dungeon_size[0]
img_len = 2000 - img_len_diff
img_height = int(img_len / dungeon_size[0]) * dungeon_size[1]
img_res = (img_len, img_height)

# Create Dungeon
dungeon = Dungeon(dungeon_size[0], dungeon_size[1])
dungeon.multiRoom(room_density[0], room_density[1])
dungeon.roadCreating()
map = dungeon.returnArray()

# Generate encounter
number_of_encounter = len(dungeon.rooms)
encounter = ''
if monster_allow or loot_allow or trap_allow:
    encounter = '<h2>Encounter</h2>\n'
    encounter += "<div class=\"container\">\n"
    for room_number in range(0, number_of_encounter):
        encounter += "<div class=\"item\">\n"
        encounter += '<h3 id=\"room' + str(room_number+1) + '\">Room ' + str(room_number+1) + '</h3>\n'
        if monster_allow:
            encounter += '<h4>Monster:</h4>\n'
            encounter += gen_monster_encounter(dungeon_lvl) + '\n'
        if loot_allow:
            encounter += '<h4>Loot:</h4>\n'
            encounter += gen_loot(dungeon_lvl)
        if trap_allow:
            traps = gen_traps(dungeon_lvl, trap_freq, chance_to_get_multiple_traps=trap_freq / 2)
            if traps is not None:
                encounter += '<h4>Traps:</h4>\n'
                encounter += traps
        encounter += "</div>\n"

# create unique name
img_name = str(uuid.uuid4().hex)
img_path = "./saved_dungeons/" + img_name + ".png"

# print Dungeon
bw_map = np.zeros((dungeon_size[0], dungeon_size[1], 3), np.uint8)
bw_map[map == 10] = [255, 255, 255]
bw_map[map == 3] = [128, 128, 128]
bw_map[map == 6] = [128, 0, 0]
img = Image.fromarray(bw_map, mode='RGB')
img = img.resize(img_res)

# Print GRID
draw = ImageDraw.Draw(img)
y_start = 0
y_end = img.height
step_size = int(img.height / dungeon_size[0])

for x in range(0, img.width, step_size):
    line = ((x, y_start), (x, y_end))
    draw.line(line, fill=0)

x_start = 0
x_end = img.width
step_size = int(img.width / dungeon_size[1])

for y in range(0, img.height, step_size):
    line = ((x_start, y), (x_end, y))
    draw.line(line, fill=0)

# Print RoomNumbers
font = ImageFont.truetype('arialbd.ttf', 25)
for k, v in dungeon.getCorner().items():
    draw.text((v[0][1]*img.height/dungeon.shape[0] + img.height/dungeon.shape[0]/2 - font.getsize(str(k))[0]/2, v[0][0]*img.height/dungeon.shape[1] + img.width/dungeon.shape[1]/2 - font.getsize(str(k))[1]/2), str(k), fill=128, font=font)

img.save(img_path)

include_debug = True

# Send attributes to the HTML page- printer

createResponse(include_debug, dungeon_name, all_attributes, encounter, img_name)
