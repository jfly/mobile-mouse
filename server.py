#!/usr/bin/env python

import SimpleHTTPServer
import SocketServer

import json
import traceback

import gtk

display = gtk.gdk.display_get_default()

class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def __init__(self, *argv, **argw):
        SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, *argv, **argw)
        
    def do_GET(self):
        path = self.path
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        if path == "/move":
            error = None
            try:
                screen, x, y, modifiers = display.get_pointer()
                display.warp_pointer(screen, x, y+1)
                display.flush()
            except:
                error = traceback.format_exc()

            self.send_response(200 if error is None else 500)
            response = { "error": error }
            self.wfile.write(json.dumps(response) + "\r\n")
            return

        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

def main():
    PORT = 8000

    SocketServer.TCPServer.allow_reuse_address = True
    httpd = SocketServer.TCPServer(("", PORT), CustomHandler)

    print "serving at port", PORT
    httpd.serve_forever()

if __name__ == "__main__":
    main()
