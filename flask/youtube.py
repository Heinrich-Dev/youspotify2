# This file handles using YouTube's API and authentication

import os

from googleapiclient.discovery import build

def main():
    api_key = os.environ["YOUTUBE_API_KEY"]
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.channels().list(
        part='statistics',
        forUsername="nprmusic"
    )
    response = request.execute()
    print(response)

if __name__ == "__main__":
    main()