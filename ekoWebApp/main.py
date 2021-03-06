import webapp2

from webapp2_extras import jinja2, sessions
from google.appengine.api import users
from data import Kiosk, SyncSession
from google.appengine.ext import db
import logging

from handlers.BaseHandler import BaseHandler, FlushCacheHandler
from handlers.KioskHandlers import RegKiosksHandler, EditKioskHandler, ListKiosksHandler, SendMsgKioskHandler
from handlers.RPCHandlers import JSONRPCHandler
from handlers.FileUploadHandlers import FileUploadHandler, FileUploadRequestHandler
from handlers.SyncSessionHandler import ListSyncSessionHandler
from handlers.DownloadHandler import DownloadSyncHandler
class HomePageHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        ctx = self.get_ctx(user)
        self.render_response('main.html', **ctx)

config = {}
# secret key for testing
config['webapp2_extras.sessions'] = {
    'secret_key': 'le9c3jc0dkiwidocsiameses',
}

app = webapp2.WSGIApplication([
    ('/', HomePageHandler),
    ('/kiosks', ListKiosksHandler),
    ('/kiosks/register', RegKiosksHandler),
    ('/kiosks/send_message', SendMsgKioskHandler),
    (r'/kiosks/edit/([a-zA-Z0-9_]+)', EditKioskHandler),
    ('/api/json', JSONRPCHandler),
    ('/api/upload', FileUploadHandler),
    ('/api/upload_request', FileUploadRequestHandler),
    ('/sys/flush', FlushCacheHandler),
    (r'/kiosks/syncs/([a-zA-Z0-9_]+)', ListSyncSessionHandler),
    (r'/download/([a-zA-Z0-9_-]+)', DownloadSyncHandler),
], config=config, debug=True)

def main():
    app.run()
    
if __name__ == '__main__':
    main()
    
