import spotipy
from spotipy.oauth2 import SpotifyOAuth
from  dotenv import load_dotenv
import os
import pandas as pd
import pprint

load_dotenv(r"C:\Users\f2013\Downloads\Spotify\.env")

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
scope = 'playlist-read-private'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://localhost:3000",
                                               scope=scope))

results = sp.current_user_playlists(limit=50)

def show_tracks(results):
    for i, item in enumerate(results['items']):
        track = item['track']
        print(
            "   %d %32.32s %s" %
            (i, track['artists'][0]['name'], track['name']))

playlists = sp.current_user_playlists()
user_id = sp.me()['id']

for playlist in playlists['items']:
    if playlist['owner']['id'] == user_id:
        print()
        name = playlist['name'].replace("/","-")
        print(name)
        print('  total tracks', playlist['tracks']['total'])

        results = sp.playlist(playlist['id'], fields="tracks")["tracks"]["items"]
        df = pd.DataFrame(columns=["Artist","Track"])

        for i, result in enumerate(results):
            df.loc[i,"Artist"] = results[i]["track"]["artists"][0]["name"]
            df.loc[i,"Track"] = results[i]["track"]["name"]
        print(df)
        df.to_csv(fr"C:\Users\f2013\Downloads\Spotify\Playlists\{str(name)}.csv", index=False)



# df = pd.DataFrame(columns=["Artist", "Track"])

# for i in range(0,478,50):
#     results = sp.current_user_saved_tracks(limit=50,offset=i)
#     for idx, item in enumerate(results['items']):
#         track = item['track']
#         print(idx+1+i, track['artists'][0]['name'], " – ", track['name'])
#         new_row = {"Artist": track['artists'][0]['name'], "Track": track['name']}
#         df = pd.concat([df,pd.DataFrame([new_row])], names=["Artist","Track"], ignore_index=True)

# df.to_csv("Liked Songs.csv", index=False)

