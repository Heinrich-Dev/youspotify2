# This file handles using YouTube's API and authentication

import os

from googleapiclient.discovery import build

def main():
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
        part="snippet,contentDetails,status",
        playlistId=new_playlistId
    )
    #TODO: extract video ids from list of videos gathered
    #TODO: check if any video ids are not already downloaded
    #TODO: given video ids build urls
    #TODO: given urls download videos from youtube
    #TODO: given videos from youtube convert to mp3s
    #TODO: given list of mp3s upload to spotify and create playlist from local files
    response = request.execute()
    print(response)

if __name__ == "__main__":
    main()