#!/usr/bin/env python
# http-server
# GEsquivel 2010.05.24 V0.1
#
# Run a simple webserver at the given root

import string
import cgi
import time
import os
import sys
import thread
import getopt
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


__author__ = "Gus Esquivel (gesquive@gmail.com)"
__version__ = "0.1"
__app__ = os.path.basename(sys.argv[0])

def usage():
    usage = \
"""Usage: %s [options] root_dir
    Run a local http server with the given root directory.
Options and arguments:
  root_dir                          The directory path for the hosted files.
  -p --http-port <port>             The port for the server to listen on.
                                        (default: 8080)
  -n --no-dir-list                  Turn off directory listing.
  -h --help                         Prints this message.
  -u --update                       Checks server for an update, replaces
                                        the current version if there is a
                                        newer version available.
  -v --verbose                      Writes all messages to console.

    version %s
""" % (__app__, __version__)

    print usage

def main():
    server_port = 8080
    root_dir = None
    list_dir = True

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvunp:", \
        ["help", "verbose", "update", "no-dir-list", "http-port="])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)

    if len(args) is 1:
        if os.path.exists(args[0]):
            if os.path.isdir(args[0]):
                root_dir = args[0]
            else:
                print "root directory is not a valid directory."
                sys.exit(2)
        else:
            print "root directory does not exist."
            sys.exit(2)
    else:
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            # Print out help and exit
            usage()
            sys.exit()
        elif o in ("-u", "--update"):
            update(info_file_path)
            sys.exit(0)
        elif o in ("-v", "--verbose"):
            verbose = True
        elif o in ("-n", "--no-dir-list"):
            list_dir = False
        elif o in ("-p", "--http-port"):
            if not a.isdigit():
                print "http port: \'%s\' must be a valid integer." % a
                sys.exit(2)
            server_port = int(a)

    try:
        server = QuickServer(('', server_port), root_dir, list_dir)
        print 'Started HTTPServer...'
        thread.start_new_thread(server.serve_forever, ())
        raw_input("Press any key to stop server")
    except KeyboardInterrupt:
        print ''
    print 'Shutting down server'
    server.socket.close()


class QuickServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            file_path = os.path.join(self.server.root_dir, self.path[1:])
            print file_path
            if file_path.endswith(".html"):
                print file_path
                f = open(file_path) #self.path has /test.html

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            elif file_path.endswith(".esp"):   #our dynamic content
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("Today is the " + str(time.localtime()[7]))
                self.wfile.write(" day in the year " + str(time.localtime()[0]))
                return
            elif self.server.list_dir and os.path.isdir(file_path):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                dir_list = self.server.dir_generator.generate_listing(file_path)
                self.wfile.write(dir_list)
            elif os.path.isdir(file_path):
                #TODO: Double check this error code
                self.send_error(403,'Directory listing not allowed: %s' % self.path)
                return
            else:
                 self.send_error(404,'File Not Found: %s' % self.path)

            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)


    def do_POST(self):
        global rootnode
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                query=cgi.parse_multipart(self.rfile, pdict)
            self.send_response(301)

            self.end_headers()
            upfilecontent = query.get('upfile')
            print "filecontent", upfilecontent[0]
            #TODO: Write this file to disk somewhere
            self.send_error(403,'No permissions: %s' % self.path)
            #self.wfile.write("<HTML>POST OK.<BR><BR>");
            #self.wfile.write(upfilecontent[0]);

        except :
            pass


class QuickServer(HTTPServer):
    root_dir = '.'
    list_dir = False

    def __init__(self, server_address, root_dir, list_dir=True):
        HTTPServer.__init__(self, server_address, QuickServerHandler)
        self.root_dir = root_dir
        self.list_dir = list_dir
        self.dir_generator = DirectoryListGenerator()


class DirectoryListGenerator:
    def __init__(self):
        pass

    def generate_listing(self, dir_path, title=None):
        #TODO: Write directory listing generation
        #return "If this script was finished, " \
        #       "a directory listing would appear here."
        if not title:
            title = "Index of %s" % dir_path.strip(os.sep).split(os.sep)[-1:][0]
        file_list = "<h1>%s</h1>\n<hr>" % title
        for file in os.listdir(dir_path):
            file_list = "%s<br>\n%s" % (file_list, file)

        return file_list


if __name__ == '__main__':
    main()
