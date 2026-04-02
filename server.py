from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

    def log_message(self, format, *args):
        pass

def run():
    server = HTTPServer(('0.0.0.0', 8080), Handler)
    server.serve_forever()

def stay_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()
