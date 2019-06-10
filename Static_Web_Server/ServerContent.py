#Code for webserver based on code from the following git link
#https://gist.github.com/HaiyangXu/ec88cbdce3cdbac7b8d5

import http.server
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import os

PORT = 8080

#Displays the contents from the content folder and not the
#current directory with the run.batch and ServerContent.py file
#https://stackoverflow.com/questions/39801718/how-to-run-a-http-server-which-serve-a-specific-path
serverdir = os.path.join(os.path.dirname(__file__), 'Web Server Content')
os.chdir(serverdir)

handler = http.server.SimpleHTTPRequestHandler

#Accepted mime types that HTTP web server handlees
handler.extensions_map={
	'.html': 'text/html',
	'.jpg': 'image/jpeg',
    '.mp3': 'audio/mpeg',
    '.mp4': 'video/mp4',
}

httpd = socketserver.TCPServer(("", PORT), handler)

print("Serving at port", PORT)
httpd.serve_forever()
