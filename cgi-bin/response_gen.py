

#Prints the HTML page for the client

def printResponse(debug, name, attributes, encounters):

	print("Content-Type: text/html; charset=utf-8\n")
	print("<html>")
	print("<meta charset=\"utf-8\">")
	print("<head> <title>Dungeon Generator</title> ")
	print("<link rel=\"shortcut icon\" href=\"http://localhost:8000/graphics/icon.ico\" type=\"image/vnd.microsoft.icon\" />")
	print("<style>")
	print("body{background-image: url(http://localhost:8000/graphics/bg.png);}")
	print(".content {max-width: 500px;margin: auto;padding: 10px;background-color: rgba(255,255,255,0.85);line-height: 2;font-size: 20px;}")
	print(".gitlink {max-width: 525px;margin: auto;left: 0;bottom: 0;text-align: right;}")
	print("input{font-size: 18px;}")
	print("select{font-size: 18px;}")
	print(".center {display: block;margin: auto}")
	print("</style>")
	print("</head>")
	print("<body>")
	print("<img class=\"center\" src=\"http://localhost:8000/graphics/DungeonGen.png\" alt=\"Dungeon Logo\" style=\"width:500px\">")
	print("<div class=\"content\">")
	if name is not None:
		print("<h1>" + name + "</h1>")
	else:
		print("<h1>Dungeon is generated!</h1>")
	if debug:
		print("<h2>Values:</h2>")
		print(attributes)
	print("<br><img src=\"/my.png\" alt=\"Dungeon Map\" style=\"width:500px\"><br>")
	print(encounters)
	print("</div>")
	print("<div class=\"gitlink\"><br><a href=\"https://github.com/urschni/dndgen\"><img src=\"http://localhost:8000/graphics/GithubLogo.png\" alt=\"Github Link\" style=\"width:150px\"></a></div>")
	print("</body>")
	print("</html>")
