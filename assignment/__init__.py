from flask import Flask
import os
from authlib.integrations.flask_client import OAuth
from assignment.my_secrets import client_id,client_secret

app = Flask(__name__)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app.secret_key = "some string"
app.config['SESSION_TYPE'] = "filesystem"
# print(client_id,client_secret)
oauth = OAuth(app)
spotify = oauth.register(
    name='spotify',
    client_id=client_id,
    client_secret=client_secret,
    access_token_url='https://accounts.spotify.com/api/token',
    access_token_params=None,
    authorize_url='https://accounts.spotify.com/authorize',
    authorize_params=None,
    api_base_url='https://api.spotify.com/v1/',
    userinfo_endpoint='me',
    client_kwargs={'scope': 'playlist-modify-public,playlist-modify-private'},
)
from assignment import routes