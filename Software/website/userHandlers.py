import webapp2
import os
from google.appengine.api import users

#google accounts
accounts = ['fofanadave']

# This logs out the user from the application only, not 
# from other google services. Found at 
# http://ptspts.blogspot.ca/2011/12/how-to-log-out-from-appengine-app-only.html
class LogoutPage(webapp2.RequestHandler):
  def get(self):
    target_url = self.request.referer or '/'
    if os.environ.get('SERVER_SOFTWARE', '').startswith('Development/'):
      self.redirect(users.create_logout_url(target_url))
      return

    # On the production instance, we just remove the session cookie, because
    # redirecting users.create_logout_url(...) would log out of all Google
    # (e.g. Gmail, Google Calendar).
    #
    # It seems that AppEngine is setting the ACSID cookie for http:// ,
    # and the SACSID cookie for https:// . We just unset both below.
    cookie = Cookie.SimpleCookie()
    cookie['ACSID'] = ''
    cookie['ACSID']['expires'] = -86400  # In the past, a day ago.
    self.response.headers.add_header(*cookie.output().split(': ', 1))
    cookie = Cookie.SimpleCookie()
    cookie['SACSID'] = ''
    cookie['SACSID']['expires'] = -86400
    self.response.headers.add_header(*cookie.output().split(': ', 1))
    self.redirect(target_url) 

class userLoginHandler(webapp2.RequestHandler):

    def get(self):
        
        user_name = active_user()

        template_values = {
            'user_name': json.dumps(user_name)
        }

        template = JINJA_ENVIRONMENT.get_template('htmlTest.html')
        self.response.write(template.render(template_values))

# Go to the application settings to give administrative rights to users
# Then check if user is an administrator for the corresponding
# tasks that he/she wishes to perform, using the code below
#https://developers.google.com/appengine/docs/python/users/adminusers

