from flask import render_template, redirect, url_for, request, session
import google_auth_oauthlib.flow
import google.oauth2.credentials
import requests
from assignment import app, oauth,CLIENT_CONFIG
from assignment.helper import *


@app.route("/authorize")
def getauth():
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        client_config=CLIENT_CONFIG, scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])
    flow.redirect_uri = url_for('outhcallback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true')
    session['state'] = state
    # print("print", state, session['state'])
    return redirect(authorization_url)


@app.route("/outhcallback")
def outhcallback():
    # print("hiii")
    state = session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        client_config=CLIENT_CONFIG,
        scopes=['https://www.googleapis.com/auth/youtube.force-ssl'],
        state=state)
    flow.redirect_uri = url_for('outhcallback', _external=True)
    # print(request.url)
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes}

    return redirect(url_for('login'))


@app.route("/login")
def login():
    # print("inside login")
    if 'credentials' not in session:
        return redirect(url_for('getauth'))
    if 'spotify_login' not in session:
        authorize_spotify()
        return redirect(url_for('authorize_spotify'))
    return redirect(url_for('home'))


@app.route("/do")
def do():
    if(not loggedin()):
        return redirect(url_for('home'))
    sp_pl = request.args.get("spotify")
    yt_pl = request.args.get("youtube")
    try:
        titles = give_songslist(yt_pl)
        uri = get_uris(titles)
        addsongs(sp_pl, uri)
    except:
        print("error")
    return redirect(url_for("home"))


@app.route("/authorize_spotify")
def authorize_spotify():
    spotify = oauth.create_client('spotify')  # create the google oauth client
    redirect_uri = url_for('oauth2callback', _external=True)
    return spotify.authorize_redirect(redirect_uri)


@app.route("/oauth2callback")
def oauth2callback():
    spotify = oauth.create_client('spotify')  # create the spotify oauth client
    # Access token from spotify (needed to get user info)
    token = spotify.authorize_access_token()
    session["spotify_login"] = token
    # user = oauth.spotify.userinfo()  # uses openid endpoint to fetch user info
    # session['profile'] = user_info
    return redirect(url_for('login'))


@app.route('/revoke')
def revoke():
    if 'credentials' not in session:
        return ('You need to <a href="/authorize">authorize</a> before ' +
                'testing the code to revoke credentials.')

    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])

    revoke = requests.post('https://oauth2.googleapis.com/revoke', params={
                           'token': credentials.token}, headers={'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        return('Credentials successfully revoked.')
    else:
        return('An error occurred.')


@app.route('/logout')
def logout():
    # print("logout")
    if(not loggedin()):
        return redirect(url_for('home'))
    del session['credentials']
    del session['spotify_login']
    return redirect(url_for('home'))


@app.route("/")
def home():
    print("in home dirtory")
    return render_template("index.html", login=loggedin())
