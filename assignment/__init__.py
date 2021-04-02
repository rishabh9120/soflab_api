from flask import Flask
import os
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app.secret_key = "some string"
app.config['SESSION_TYPE'] = "filesystem"
# print(os.getenv("client_id"),os.getenv("client_secret"))
oauth = OAuth(app)
spotify = oauth.register(
    name='spotify',
    client_id=os.getenv("client_id"),
    client_secret=os.getenv("client_secret"),
    access_token_url='https://accounts.spotify.com/api/token',
    access_token_params=None,
    authorize_url='https://accounts.spotify.com/authorize',
    authorize_params=None,
    api_base_url='https://api.spotify.com/v1/',
    userinfo_endpoint='me',
    client_kwargs={'scope': 'playlist-modify-public,playlist-modify-private'},
)


CLIENT_CONFIG = {'web': {
    'client_id': os.getenv("GOOGLE_CLIENT_ID"),
    'project_id': os.getenv("GOOGLE_PROJECT_ID"),
    'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
    'token_uri': 'https://www.googleapis.com/oauth2/v3/token',
    'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
    'client_secret': os.getenv("GOOGLE_CLIENT_SECRET"),
    'redirect_uris': os.getenv("GOOGLE_REDIRECT_URIS"),
    'javascript_origins': os.getenv("GOOGLE_JAVASCRIPT_ORIGINS")}}

# This scope will allow the application to manage your calendars
SCOPES = ['https://www.googleapis.com/auth/calendar']
from assignment import routes