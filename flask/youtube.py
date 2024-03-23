# This file handles using YouTube's API and authentication

import os

from googleapiclient.discovery import build
from pytube import YouTube
from pytube.exceptions import VideoUnavailable

from moviepy.editor import *


api_key = os.environ["YOUTUBE_API_KEY"]
youtube = build("youtube", "v3", developerKey=api_key)


def getVideoInfo(url):
    vid = ""
    substr = "https://www.youtube.com/watch?v="
    vid = url.replace(substr, "")
    request = youtube.videos().list(
        part='contentDetails',
        id=vid,
        maxResults=1
    )
    return request.execute()
# Returns a list of video IDs from NPR's YouTube channel
def getNPRIds():
    request = youtube.channels().list(
        part='contentDetails',
        forUsername="nprmusic"
    )
    response = request.execute()
    # You have to do this ugliness to get the id from the json dump
    new_playlistId = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=new_playlistId,
        maxResults=50
    )
    response = request.execute()
    ids = []
    items = response['items']
    for item in items:
        title = item['snippet']['title']
        if 'Tiny Desk Concert' in title or 'Tiny Desk (Home) Concert' in title:
            ids.append(item['contentDetails']['videoId'])

    new_nextPageToken = response['nextPageToken']

    while True:  #Always a good sign
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=new_playlistId,
            maxResults=50,
            pageToken=new_nextPageToken
        )

        response = request.execute()
        items = response['items']
        for item in items:
            title = item['snippet']['title']
            if 'Tiny Desk Concert' in title or 'Tiny Desk (Home) Concert' in title:
                ids.append(item['contentDetails']['videoId'])
        try:
            new_nextPageToken = response['nextPageToken']
        except KeyError:
            break

    return ids

# Checks video IDs to see if any have already been downloaded, downloads them if not
def checkVids(ids):
    toDownload = []
    file = open('../videos/npr.txt', 'r')
    old_ids = file.readlines()
    for item in ids:
        if item not in old_ids:
            toDownload.append(item)
    file.close()
    return toDownload

# Downloads and converts videos from youtube given a list of watch IDs
# Adds all converted videos' IDs to the text file to ensure they are not downloaded
# again
def downloadandConvertVideos(videos):
    file = open('../videos/npr.txt', 'w+')
    for video in videos:
        link = "https://www.youtube.com/watch?v=" + video
        yt = YouTube(link)
        try:
            mp4path = yt.streams.filter(only_audio=True).first().download("../videos")
        except VideoUnavailable:
            continue
        mp3path = mp4path.replace('mp4', 'mp3')
        convert(mp4path, mp3path)
        file.write(video + '\n')
    file.close()

# Downloads one video from YouTube and converts it to an mp3
# File is saved in a directory outside of the current one, labeled as "videos"
def downloadandConvert(url):
    yt = YouTube(url)
    try:
        mp4path = yt.streams.filter(only_audio=True).first().download("../videos")
    except VideoUnavailable:
        return
    else:
        mp3path = mp4path.replace('mp4', 'mp3')
        convert(mp4path, mp3path)

# Converts an mp4 given its path to an mp3
# Creates an mp3 file in the process, deletes old mp4 file
def convert(pathTomp4, pathTomp3):
    toConvert = AudioFileClip(pathTomp4)
    toConvert.write_audiofile(pathTomp3)
    toConvert.close()
    os.remove(pathTomp4)

#TODO: put all mp3s into a zip file
#TODO: given list of mp3s upload to spotify and create playlist from local files
#TODO: have process daemonized and check for updates on NPR's channel

if __name__ == "__main__":
    pass