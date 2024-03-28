# This file handles everything related to running the flask server and dealing with Spotify's authentication
import spotipy
import os
from datetime import datetime, timedelta
import requests
import base64
import re
import hashlib
import urllib
from flask import Flask, session, url_for, redirect, request, json, jsonify
from youtube import getVideoInfo

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']

CLIENT_ID = os.environ['SPOTIPY_CLIENT_ID']
CLIENT_SECRET = os.environ['SPOTIPY_CLIENT_SECRET']
REDIRECT_URI = os.environ['REDIRECT_URI']

@app.route("/")
def start():
    return "<a href='/login'>Login</a>"

@app.route("/login")
def login():

    scope = 'playlist-modify-public playlist-modify-private'

    url = 'https://accounts.spotify.com/authorize'

    dataObj = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True
    }

    authUrl = f"{url}?{urllib.parse.urlencode(dataObj)}"

    return redirect(authUrl)

@app.route("/redirect")
def redirectPage():
    url = 'https://accounts.spotify.com/api/token'
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})
    
    if 'code' in request.args:
        headerObj = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        dataObj = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        }

        response = requests.post(url, headers=headerObj, data=dataObj)
        token = response.json()

        session['accessToken'] = token['access_token']
        session['refreshToken'] = token['refresh_token']
        session['expiresAt'] = datetime.now().timestamp() + token['expires_in']

        return "<a href='/getTest'> Get Local File Hopefully</a>"

@app.route('/getTest')
def getTest():
    token = session['accessToken']
    playlist = getPlaylistItems(token)
    uris = geturis(playlist)
    result = addToPlaylist(token, '1W4qGpgPZ9OA5yiCZp9DQJ', uris)
    return "<h1>{result}</h1>"

@app.route("/youtubeget", methods=["POST"])
def youtubeget():
    json = request.get_json()
    query = json["search"]
    return getVideoInfo(query)

def getPlaylistItems(accessToken):
    url = 'https://api.spotify.com/v1/playlists/0OzEgmNhb9SRFbDXTddWma?si=12c5203d76734844/tracks' # Henry's playlist ID
    headerObj = {
        'Authorization': 'Bearer ' + accessToken 
    }
    result = requests.get(url, headers=headerObj)
    return result.json()

def geturis(playlistItems):
    items = playlistItems['tracks']['items']
    uris = []
    for item in items:
        uris.append(item['track']['uri'])
    return uris

def addToPlaylist(accessToken, playlistId, uris):
    url = 'https://api.spotify.com/v1/playlists/' + playlistId + '/tracks'
    headerObj = {
        'Authorization': 'Bearer ' + accessToken,
        'Content-type': 'application/json'
    }
    dataObj = {
        'uris': uris,
        'position': 0
    }
    result = requests.post(url, headers=headerObj, json=dataObj)
    print(result.json())
    return result

if __name__ == "__main__":
    app.run(debug=True)