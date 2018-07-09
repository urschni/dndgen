from random_dungeon_name import gen_random_dungeon_name
import pdfkit

#Prints the HTML page for the client

def createResponse(debug, name, attributes, encounters,img_name):
    #Create the HTML file
    file_path = "saved_dungeons/"+img_name+".html"
    file = open(file_path,"w")
    file.write("<!DOCTYPE HTML>")
    file.write("<html>")
    file.write("<meta charset=\"utf-8\">")
    file.write("<head> <title>Dungeon Generator</title> ")
    file.write("<link rel=\"shortcut icon\" href=\"../graphics/icon.ico\" type=\"image/vnd.microsoft.icon\" />")
    file.write("<style>")
    file.write("body{background-image: url(../graphics/bg.png);}")
    file.write(".content {max-width: 500px;margin: auto;padding: 10px;background-color: rgba(255,255,255,0.85);line-height: 2;font-size: 20px;}")
    file.write(".gitlink {max-width: 525px;margin: auto;left: 0;bottom: 0;text-align: right;}")
    file.write("input{font-size: 18px;}")
    file.write("select{font-size: 18px;}")
    file.write(".center {display: block;margin: auto}")
    file.write("</style>")
    file.write("</head>")
    file.write("<body>")
    file.write("<img class=\"center\" src=\"../graphics/DungeonGen.png\" alt=\"Dungeon Logo\" style=\"width:500px\">")
    file.write("<div class=\"content\">")
    if name is not None:
        file.write("<h1>" + name + "</h1>")
    else:
        file.write("<h1>" + gen_random_dungeon_name() + "</h1>")
    if debug:
        file.write("<h2>Values:</h2>")
        file.write(attributes)
    file.write("<br><img src=\"../saved_dungeons/"+img_name+".png\" alt=\"Dungeon Map\" style=\"width:500px\"><br>")
    file.write("<a href=\"../saved_dungeons/"+img_name+".pdf\" download=\"Dungeon\"><button type=\"button\">Download as Pdf</button></a> &nbsp;")
    file.write("<a href=\"../saved_dungeons/"+img_name+".png\" download=\"Dungeon\"><button type=\"button\">Download Dungeon Image</button></a><br>")
    file.write(encounters)
    file.write("</div>")
    file.write("<div class=\"gitlink\"><br><a href=\"https://github.com/urschni/dndgen\"><img src=\"../graphics/GithubLogo.png\" alt=\"Github Link\" style=\"width:150px\"></a></div>")
    file.write("</body>")
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