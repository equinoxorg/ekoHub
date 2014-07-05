from google.appengine.ext import db
from datetime import date, datetime
from dataFile import remoteSettings
from timeUtilities import GMT1, GMT2, UTC
from utility_functions import active_user
from google.appengine.api import users
import os, time
import cgi
import webapp2
import jinja2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class kioskHandler(webapp2.RequestHandler):
    def get(self):

        user_name = active_user()
        active = False if (user_name == '') else True
        login = users.create_login_url(self.request.uri)

        template_values = {
            'user_name': user_name,
            'active_user': active,
            'login_url': login,
        }

        template = JINJA_ENVIRONMENT.get_template('/pages/kiosks.html')
        self.response.write(template.render(template_values))


