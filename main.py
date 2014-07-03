import os
import bqclient
import webapp2
import logging
from oauth2client.appengine import oauth2decorator_from_clientsecrets
# [START cached-decor]
from google.appengine.api import memcache

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
SCOPES = [
    'https://www.googleapis.com/auth/bigquery'
]
decorator = oauth2decorator_from_clientsecrets(
    filename=CLIENT_SECRETS,
    scope=SCOPES,
    cache=memcache)
# [STOP cached-decor]

# Project ID for a project where you and your users
#   are viewing members.  This is where the bill will be sent.
#   During the limited availability preview, there is no bill.
# Replace this value with the Client ID value from your project,
#   the same numeric value you used in client_secrets.json
DATA_PROJECT_ID = "publicdata"
DATASET = "samples"
TABLE = "natality"


class MainPage(webapp2.RequestHandler):
    @decorator.oauth_required
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        bq = bqclient.BigQueryClient(decorator)
        modTime = bq.getLastModTime(DATA_PROJECT_ID, DATASET, TABLE)
        if modTime:
            msg = 'Last mod time = ' + modTime
        else:
            msg = "Could not find last modification time.\n"
        self.response.write('Hello, Dashboard! %s' % msg)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    (decorator.callback_path, decorator.callback_handler())
], debug=True)
