from flask import redirect, url_for, session
import json
import google.oauth2.credentials
from googleapiclient.discovery import build
import requests
from assignment import spotify


def loggedin():
    if ('credentials' in session and 'spotify_login' in session):
        return True
    return False

def give_songslist(yt_pl):
    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])
    # print(session["credentials"])
    youtube = build('youtube', 'v3', credentials=credentials)
    titles = []
    if(yt_pl != "like"):
        response = youtube.playlists().list(
            mine=True, part='snippet,contentDetails').execute()
        playlist_id = "notset"
        # print(response)
        for item in response["items"]:
            if item["snippet"]["title"] == yt_pl:
                playlist_id = item["id"]

        response = youtube.playlistItems().list(part="snippet,contentDetails",
                                                playlistId=playlist_id, maxResults=50).execute()
        for item in response["items"]:
            video_title = item["snippet"]["title"]
            titles.append(video_title)
    else:
        response = youtube.videos().list(part="snippet,contentDetails,statistics",
                                         myRating="like", maxResults=50).execute()
        for item in response["items"]:
            video_title = item["snippet"]["title"]
            titles.append(video_title)
    return titles


def get_uris(titles):
    ans = []
    for i in titles:
        name = i.split("ft")[0]
        artist, songname = name.split("-")
        url = "search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=2".format(
            songname, artist)
        resp = spotify.get(url, token=session["spotify_login"])
        songs = resp.json()
        # print("artist : {},song: {}".format(artist,songname))
        # print(songs)
        try:
            uri = songs["tracks"]["items"][0]["uri"]
            ans.append(uri)
        except:
            print(i,"is not available")
    return ans


def create_playlist(name):
    request_body = json.dumps({
        "name": name,
        "description": "All Liked Youtube Videos",
        "public": True
    })

    query = "https://api.spotify.com/v1/users/{}/playlists".format(
        get_currentuser_id())
    response = requests.post(
        query,
        data=request_body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(session["spotify_login"]["access_token"])
        }
    )
    response_json = response.json()
    print("playlist created")
    # playlist id
    return response_json["id"]


def get_currentuser_id():

    resp = spotify.get('me', token=session["spotify_login"])
    user_info = resp.json()
    return(user_info["id"])


def addsongs(name, uri):
    playlist_id = create_playlist(name)

    # add all songs into new playlist
    request_data = json.dumps(uri)

    query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
        playlist_id)

    response = requests.post(
        query,
        data=request_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(session["spotify_login"]["access_token"])
        }
    )

    response_json = response.json()
    return response_json
