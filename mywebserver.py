from http.server import HTTPServer, CGIHTTPRequestHandler
import cgitb;
cgitb.enable()  ## This line enables CGI error reporting
 
server = HTTPServer
handler = CGIHTTPRequestHandler
server_address = ("", 8000)
 
httpd = server(server_address, handler)
httpd.serve_forever()
