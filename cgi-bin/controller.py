import cgi, cgitb
import time
import json
from random import randint
from PIL import Image
import numpy as np
cgitb.enable()

#Timestamp to create unique filenames
current_milli_time = lambda: int(round(time.time() * 1000.000))

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
            '''if x > inner_dungeon_size[0] or y > inner_dungeon_size[1] or x < :
                is_working = False
                break
            '''
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

#Generate Image from numpyArray and resize it
img = Image.fromarray(data, 'RGB')
img = img.resize((500,500))
img = img.rotate(90)
img.save('../my.png')



#Get the values from the form
form = cgi.FieldStorage()
trap_allow =  form.getvalue('trap_allow')
monster_cr = form.getvalue('monster_cr')
group_size = form.getvalue('group_size')
trap_freq = form.getvalue('trap_freq')
dungeon_size = form.getvalue('dungeon_size')
deadends_allow = form.getvalue('deadends_allow')
all_attributes = ""
for x in form:
    all_attributes = all_attributes + str(form[x])[16:] + "<br>"


print("Content-Type: text/html; charset=utf-8\n\n")
print("<html>")
print("<body>")
print("<h1>Dungeon is generated!</h1>")
print("<h2>Values:</h2>")
print(all_attributes)
print("<br><img src=\"/my.png\" alt=\"Red Point\">")
print("</body>")
print("</html>")
