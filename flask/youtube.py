# This file handles using YouTube's API and authentication

import os

from googleapiclient.discovery import build
from pytube import YouTube

from moviepy.editor import *

# Returns a list of video IDs from NPR's YouTube channel
def getNPRIds():
    api_key = os.environ["YOUTUBE_API_KEY"]
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.channels().list(
        part='contentDetails',
        forUsername="nprmusic"
    )
    response = request.execute()
    # You have to do this ugliness to get the id from the json dump
    new_playlistId = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=new_playlistId,
        maxResults=50
    )

    response = request.execute()
    new_nextPageToken = response['nextPageToken']

    ids = []

    while True:  #Always a good sign
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=new_playlistId,
            maxResults=50,
            pageToken=new_nextPageToken
        )

        response = request.execute()
        items = response['items']

        for item in items:
            ids.append(item['contentDetails']['videoId'])

        try:
            new_nextPageToken = response['nextPageToken']
        except KeyError:
            break
    return ids

# Checks video IDs to see if any have already been downloaded, downloads them if not
def checkVids(ids):
    toDownload = []
    file = open('../videos/npr.txt', 'w+')
    old_ids = file.readlines()
    for item in ids:
        if item not in old_ids:
            file.write(item + '\n')
            toDownload.append(item)
    return toDownload

# Downloads and converts videos from youtube given a list of watch IDs
def downloadandConvertVideos(videos):
    link = "https://www.youtube.com/watch?v=" + vid
    yt = YouTube(link)
    for video in videos:
        yt.streams.filter(only_audio=True).first().download("../videos")

# Downloads one video from YouTube, used for testing
def testDownloadandConvert(url):
    yt = YouTube(url)
    yt.streams.filter(only_audio=True).first().download("../videos")

#TODO: given videos from youtube convert to mp3s
#TODO: put all mp3s into a zip file
#TODO: given list of mp3s upload to spotify and create playlist from local files
#TODO: have process daemonized and check for updates on NPR's channel



if __name__ == "__main__":
    #videoIds = getNPRIds()
    #toDownload = checkVids(videoIds)
    #downloadandConvertVideos(toDownload)
    testDownloadandConvert('https://www.youtube.com/watch?v=_pxMTXadCqI')