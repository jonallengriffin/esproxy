# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1 
# 
# The contents of this file are subject to the Mozilla Public License Version 
# 1.1 (the "License"); you may not use this file except in compliance with 
# the License. You may obtain a copy of the License at 
# http://www.mozilla.org/MPL/ # 
# Software distributed under the License is distributed on an "AS IS" basis, 
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License 
# for the specific language governing rights and limitations under the 
# License. 
# 
# The Original Code is ESProxy.
# 
# The Initial Developer of the Original Code is 
#   Mozilla Foundation. 
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
# 
# Contributor(s):
#  Jonathan Griffin <jgriffin@mozilla.com>
# 
# Alternatively, the contents of this file may be used under the terms of 
# either the GNU General Public License Version 2 or later (the "GPL"), or 
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"), 
# in which case the provisions of the GPL or the LGPL are applicable instead 
# of those above. If you wish to allow use of your version of this file only 
# under the terms of either the GPL or the LGPL, and not to allow others to 
# use your version of this file under the terms of the MPL, indicate your 
# decision by deleting the provisions above and replace them with the notice 
# and other provisions required by the GPL or the LGPL. If you do not delete 
# the provisions above, a recipient may use your version of this file under 
# the terms of any one of the MPL, the GPL or the LGPL. 
# 
# ***** END LICENSE BLOCK *****

import BaseHTTPServer
import httplib
from optparse import OptionParser
from SocketServer import ThreadingMixIn
import traceback

from config import allowed_paths

EShost = '127.0.0.1:9200'

class ESRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def server_error(self, error):
        self.send_response(500)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(error)

    def file_not_found(self):
        self.send_response(404)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write('%s not found' % self.path)

    def do_request(self, method):
        try:
            allowed = False
            allowed_regexes = allowed_paths.get(method, [])
            for regex in allowed_regexes:
                m = regex.match(self.path)
                if m:
                    allowed = True
                    break

            if not allowed:
                self.file_not_found()
                return

            body = None
            content_len = self.headers.getheader('content-length')
            if content_len:
                body = self.rfile.read(int(content_len))

            (host, port) = EShost.split(':')
            conn = httplib.HTTPConnection(host, port=port)
            conn.request(method, self.path, body=body)
            response = conn.getresponse()
            self.send_response(response.status)
            self.send_header("Content-type", response.getheader('Content-type', "application/json"))
            self.end_headers()
            self.wfile.write(response.read())
            conn.close()
        except:
            self.server_error(traceback.format_exc())

    def do_DELETE(self):
        self.do_request('DELETE')

    def do_GET(self):
        self.do_request('GET')

    def do_HEAD(self):
        self.do_request('HEAD')

    def do_POST(self):
        self.do_request('POST')

    def do_PUT(self):
        self.do_request('PUT')


class ThreadedHTTPServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    """ Subclass of HTTPServer which handles each request in a separate
        thread.
    """


class ESProxy(object):

    def __init__(self, proxy_port=9210):
        self.proxy_port = proxy_port

    def start(self):
        httpd = ThreadedHTTPServer(('127.0.0.1', self.proxy_port),
                                   ESRequestHandler)
        httpd.serve_forever()


if __name__ == "__main__":
    parser = OptionParser(usage='%prog [options] elasaticsearch_address')
    parser.add_option('-p', '--port', dest='port',
                      default=9210, type='int',
                      help="port to run proxy on")
    options, args = parser.parse_args()

    if not args:
        parser.print_usage()
        parser.exit()

    EShost = args[0]
    proxy = ESProxy(proxy_port=options.port)
    proxy.start()
