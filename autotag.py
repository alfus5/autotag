#!/usr/bin/env python
# coding: utf-8
#this script have been made by alfu5 on python 3.9.13

import os
import sys
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import eyed3
import requests
import time



print("""\n\n\n\n\nAUTOTAG is a handy tool coded in Python by alfu5. It allows you to easily add music audio file metadata such as title, artist, release date, album name and track number. With AUTOTAG, you can organize your music library in no time and fully enjoy your favorite music.""")
folder = input(str("please enter the path of the folder where the music is located:"))
input("\n\n\033[31mPress Enter to continue...🎶🎵\033[0m")


for file in os.listdir(folder):

    if file == 'desktop.ini' or file == '.thumbnails' or file == 'musique':
        continue

    print('\033[32m fichier: \033[0m', file)
    filename = file
    pattern = r'^(.+?) - (.+?)(?: \(clip officiel\))?\.mp3$'
    match = re.search(pattern, filename)

    if match:
        artists = match.group(1).split(' feat. ')
        artist1 = artists[0]
        artist2 = artists[1] if len(artists) > 1 else None
        title = match.group(2)
        print(f"Artist 1: {artist1}")
        if artist2:
            print(f"Artist 2: {artist2}")
        print(f"Titre: {title}")
    else:
        print("The file name does not match the expected format. Check the file extension or make sure it is not corrupted.")


    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="a4acf43b65614f14b20bb03a57918f14", client_secret="1257ab065e6d451f85ede31c3c5884bc"))

    artist = artists

    results = sp.search(q=f"artist:{artist} track:{title}", type="track")
    tracks = results["tracks"]["items"]

    if tracks:
        track = tracks[0]
        print("\t\t\n\n a corresponding sound seems to have been found. here is its information:")
        print(f"\t\tTitle: {track['name']}")
        print(f"\t\tArtist(s): {', '.join([artist['name'] for artist in track['artists']])}")
        print(f"\t\tAlbum: {track['album']['name']}")
        print(f"\t\tRelease date: {track['album']['release_date']}")

        image_url = track["album"]["images"][0]["url"]
        image_data = requests.get(image_url).content

        audiofile = eyed3.load(folder + '/' + file)
        audiofile.tag.images.set(3, image_data, "image/jpeg", "cover")

        audiofile.tag.artist = track['artists'][0]['name']
        audiofile.tag.album = track['album']['name']
        audiofile.tag.album_artist = track['artists'][0]['name']
        audiofile.tag.title = track['name']
        audiofile.tag.track_num = (track['track_number'], track['disc_number']) # numéro de piste 1 sur 10
        audiofile.tag.release_date = "2022-01-01"
        audiofile.tag.save()
        print("The file located in", audiofile, "has been successfully modified✅")
    else:
        print("No songs were found.❌")

print("\n\n\nAll .mp3 files have been tagged")