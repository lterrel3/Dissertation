import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import re
from time import sleep

#Before requesting from Spotify API, must pass area variables "SPOTIPY_CLIENT_ID" and "SPOTIPY_CLIENT_SECRET" 
#export SPOTIPY_CLIENT_ID='***'
#export SPOTIPY_CLIENT_SECRET='***'
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

'''
In playlist URL, URI is the numbers between "playlist/" and "?"
Example: https://open.spotify.com/playlist/31j4SWqROfsFS2jT44Td1i?si=932da44f329d4822
URI = 31j4SWqROfsFS2jT44Td1i
'''
pl1 = 'URI'
pl2 = 'URI'
pl3 = 'URI'

#input playlist URI and title
#access playlist metadata
#return a csv file with track name, artist name, and artist's genres for each track on a playlist
def getgenres(playlist, title):
    offset = 0
    while True:
        #sort through PL data to track data
        response = sp.playlist_items(playlist, offset=offset, 
                                    additional_types=['track'])
        #breaks while loop when there are no more tracks
        if len(response['items']) == 0:
                    break
        #create dataframe with specified columns
        df = pd.DataFrame(columns=['Track Name', 'Artist(s)', 'Genres'])
        #for each track, retrieve track name, artist name(s), and artist genres)
        for track in response['items']:
            artist_names = []
            genres = []
            if track['track'] is not None:
                for artist in track['track']['artists']:
                    artist_names.append(artist['name'])
                    genres.append(artist[genres])
                track = {'Track Name': track['track']['name'], 'Artist(s)': artist_names, 'Genres': genres}
            df = pd.concat([df, pd.DataFrame(track)], ignore_index=True)
            df = df.drop_duplicates(subset='Track Name')
        offset = offset + len(response['items'])
        #convert dataframe to csv file
        df.to_csv('%s,%d.csv'%(title, offset))
        #prevents overloading server, adjust time as needed
        sleep(5)
     
#input playlist URI and title
#accesses playlist metadata
#return a csv file with track name, artist name, and popularity scores for each track on a playlist
def getpopularity(playlist, title):
    offset = 0
    while True:
        #sort through PL data to track data
        response = sp.playlist_items(playlist, offset=offset, 
                                    additional_types=['track'])
        #breaks while loop when there are no more tracks
        if len(response['items']) == 0:
                    break
        #create dataframe with specified columns
        df = pd.DataFrame(columns=['Track Name', 'Artist(s)', 'Popularity'])
        #for each track, retrieve track name, artist name(s), and popularity scores)
        for track in response['items']:
            artist_names = []
            if track['track'] is not None:
                for artist in track['track']['artists']:
                    artist_names.append(artist['name'])
                track = {'Track Name': track['track']['name'], 'Artist(s)': artist_names, 'Popularity': track['track']['popularity']}
            df = pd.concat([df, pd.DataFrame(track)], ignore_index=True)
            df = df.drop_duplicates(subset='Track Name')
        offset = offset + len(response['items'])
        #convert dataframe to csv file
        df.to_csv('%s,%d.csv'%(title, offset))
        #prevents overloading server, adjust time as needed
        sleep(5)

#input playlist URI and title
#access playlist metadata
#return a csv file with Spotify's encoded audio features for each track on a playlist
def getaudiofeatures(URI, title):
    #create file with chosen title (likely the playlist title)
    with open (title, 'w') as f:
        #create columns in file
        f.write('Track, danceability, energy, key, loudness, mode, speechiness, acousticness,instrumentalness, liveness, valence, tempo, duration_ms, time_signature\n')
        for pl in URI:
            offset = 0
            while True:
                #sort through PL data to track data
                response = sp.playlist_items(pl, offset=offset, 
                                            additional_types=['track'])
                #break while loop when there are no more tracks
                if len(response['items']) == 0:
                            break
                trackuri = []
                names = {}
                for track in response['items']:
                    #access track URI, assign track URI to trackuri list
                    track_uri = track['track']['uri']
                    trackuri.append(track_uri)
                    #access track name, clean (remove emojis), replace old name with clean name in names dict
                    name = track['track']['name']
                    clean_name = re.sub(r',', '&#44', name)
                    names[track_uri] = clean_name
                #access spotify audio features using track URI
                features = sp.audio_features(trackuri)
                #assign track name and audio features to their respective columns. Ensure same ordering as column names above.
                for feature in features:
                    f.write('%s, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f\n'%(names[feature['uri']], feature['danceability'], feature['energy'], feature['key'], 
                                                            feature['loudness'], feature['mode'], feature['speechiness'], feature['acousticness'], feature['instrumentalness'], 
                                                            feature['liveness'], feature['valence'], feature['tempo'], feature['duration_ms'], feature['time_signature']))
                offset = offset + len(response['items'])
                #show # tracks processed and total # tracks in PL
                print(offset, '/', response['total'])
    return 

#assign sets of playlists and their titles to ordered lists 
pls = [pl1, pl2, pl3]
titles = ['1.csv', '2.csv', '3.csv']

#for each dataset (set), using its comparison title (title)
for pl, title in pls, titles:
    #create csv with track, artist, genres
    getgenres(pl, title)
    #create csv with track, artist, popularity
    getpopularity(pl, title)
    #create csv with track, audio features
    getaudiofeatures(pl, title)
