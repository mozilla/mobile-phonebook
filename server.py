#! /usr/bin/python

import os
import BaseHTTPServer
import SimpleHTTPServer

import fetch

PORT = 8001

types = {
    '.manifest': 'text/cache-manifest'
}

SimpleHTTPServer.SimpleHTTPRequestHandler.extensions_map.update(types)

def run(server_class=BaseHTTPServer.HTTPServer,
        handler_class=SimpleHTTPServer.SimpleHTTPRequestHandler,
        port=PORT):
    os.chdir(fetch.STATIC_FILES_DIR)
    server_address = ('', port)
    print "Serving files in '%s' on port %d." % (os.getcwd(), port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
