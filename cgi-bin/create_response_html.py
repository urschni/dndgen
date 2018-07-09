from random_dungeon_name import gen_random_dungeon_name
import pdfkit

#Prints the HTML page for the client

def createResponse(debug, name, attributes, encounters,img_name):
    #Create the HTML file
    file_path = "saved_dungeons/"+img_name+".html"
    if name is None:
        name = gen_random_dungeon_name()
    file = open(file_path,"w")
    file.write("<html>\n")
    file.write("<meta charset=\"utf-8\">\n")
    file.write("<head> <title>" + name + "</title> \n")
    file.write("<link rel=\"shortcut icon\" href=\"../graphics/icon.ico\" type=\"image/vnd.microsoft.icon\" />\n")
    file.write("<style>\n")
    file.write("body{background-image: url(../graphics/bg.png);}\n")
    file.write(".content {max-width: 500px;margin: auto;padding: 10px;background-color: rgba(255,255,255,0.85);line-height: 2;font-size: 20px;}\n")
    file.write(".gitlink {max-width: 525px;margin: auto;left: 0;bottom: 0;text-align: right;}\n")
    file.write("input{font-size: 18px;}\n")
    file.write("select{font-size: 18px;}\n")
    file.write(".center {display: block;margin: auto}\n")
    file.write("</style>\n")
    file.write("</head>\n")
    file.write("<body>\n")
    file.write("<img class=\"center\" src=\"../graphics/DungeonGen.png\" alt=\"Dungeon Logo\" style=\"width:500px\">\n")
    file.write("<div class=\"content\">\n")
    file.write("<h1>" + name + "</h1>\n")
    if debug:
        file.write("<h2>Values:</h2>\n")
        file.write(attributes)
    file.write("<br><img src=\"../saved_dungeons/"+img_name+".png\" alt=\"Dungeon Map\" style=\"width:500px\"><br>\n")
    file.write("<a href=\"../saved_dungeons/"+img_name+".pdf\" download=\"Dungeon\"><button type=\"button\">Download as Pdf</button></a> &nbsp;\n")
    file.write("<a href=\"../saved_dungeons/"+img_name+".png\" download=\"Dungeon\"><button type=\"button\">Download Dungeon Image</button></a><br>\n")
    file.write(encounters)
    file.write("</div>\n")
    file.write("<div class=\"gitlink\"><br><a href=\"https://github.com/urschni/dndgen\"><img src=\"../graphics/GithubLogo.png\" alt=\"Github Link\" style=\"width:150px\"></a></div>\n")
    file.write("</body>\n")
    file.write("</html>")
    
    file.close()
    #Create downlaodable pdf file
    
    output_path = "saved_dungeons/"+img_name+".pdf"
    options = {
        'margin-top': '0cm',
        'margin-right': '0cm',
        'margin-bottom': '0cm',
        'margin-left': '0cm'
    }
    pdfkit.from_file(file_path, output_path, options)

    
    
    #Create Redirect
    print("Content-Type: text/html; charset=utf-8\n")
    print("<html>")
    print("<head>")
    print("<script type=\"text/javascript\">")
    print("window.location.href = \"../saved_dungeons/"+img_name+".html\"")
    print("</script>")
    print("<title>Page Redirection</title>")
    print("</head>")
    print("<body>")
    #print("<!-- Note: don't tell people to `click` the link, just tell them that it is a link. -->")
    print("If you are not redirected automatically, follow this <a href=\"../saved_dungeons/"+img_name+".html\">link to example</a>.")
    print("</body>")
    print("</html>")