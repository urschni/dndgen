import cgi, cgitb
import time
from PIL import Image
import numpy as np
cgitb.enable()

#Timestamp to create unique filenames
current_milli_time = lambda: int(round(time.time() * 1000.000))

dungeon_size = (30,30)

w, h = dungeon_size[0], dungeon_size[1]
data = np.zeros((h, w, 3), dtype=np.uint8)
data[int(w/2), int(h/2)] = [255, 0, 0]
img = Image.fromarray(data, 'RGB')
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
