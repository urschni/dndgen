from http.server import HTTPServer, CGIHTTPRequestHandler
from threading import Thread
import cgitb
import sys
from img_cleaner import *

sys.path.insert(0, './cgi-bin')

cgitb.enable()  ## This line enables CGI error reporting

server = HTTPServer
handler = CGIHTTPRequestHandler
server_address = ("", 8000)
cleaner_thread = Thread(target=img_cleaner.thread)
print("server started")
try:
    cleaner_thread.start()
except (KeyboardInterrupt, SystemExit):
    cleanup_stop_thread()
    sys.exit

httpd = server(server_address, handler)
httpd.serve_forever()
