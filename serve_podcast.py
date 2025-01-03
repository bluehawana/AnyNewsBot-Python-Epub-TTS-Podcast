from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

# Change to the podcast directory
os.chdir("./podcast_output")

# Start the server
httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
print("Serving podcast at http://localhost:8000")
httpd.serve_forever() 