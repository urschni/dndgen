import cgi, cgitb
cgitb.enable()
form = cgi.FieldStorage()
trap_allow =  form.getvalue('trap_allow')
monster_cr = form.getvalue('monster_cr')
group_size = form.getvalue('group_size')
trap_freq = form.getvalue('trap_freq')
dungeon_size = form.getvalue('dungeon_size')
deadends_allow = form.getvalue('deadends_allow')


print("Content-Type: text/html; charset=utf-8\n\n")
print("<html>")
print("<body>")
print("<h1>Dungeon is generated!</h1>")
print(deadends_allow)
print("</body>")
print("</html>")
