import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import requests
import json
from dotenv import load_dotenv
import os
from numpy import NaN
import time
import logging

# Create a logger for the status
status_logger = logging.getLogger('status')
status_logger.setLevel(logging.INFO)

status_handler = logging.FileHandler('transfer/status.log')
status_handler.setLevel(logging.INFO)

status_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
status_handler.setFormatter(status_formatter)

status_logger.addHandler(status_handler)


# Create a logger for errors
error_logger = logging.getLogger('errors')
error_logger.setLevel(logging.ERROR)

error_handler = logging.FileHandler('transfer/errors.log')
error_handler.setLevel(logging.ERROR)

error_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
error_handler.setFormatter(error_formatter)

error_logger.addHandler(error_handler)

status_logger.info('Application is starting..')

status_logger.info('Loading env variables..')
load_dotenv()
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
LAST_FM_API_KEY = os.environ.get("LAST_FM_API")

status_logger.info('Env variables loaded')
status_logger.info('Connecting to spotify API...')

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

status_logger.info('Successfully connected to the API')
status_logger.info('Loading chart power scores..')

# Load the chart power df
chart_power_df = pd.read_excel('chart-power-scores_80s.xlsx')
chart_power_df = chart_power_df.applymap(lambda s: s.lower() if type(s) == str else s)
chart_power_df = chart_power_df[['Song', 'Artist', 'Points']].groupby(['Song', 'Artist']).sum()
chart_power_df.reset_index(inplace=True)

status_logger.info('Successfully loaded chart power scores')
status_logger.info('Ready to go')

def filter_track_features(track, genre):
    '''
    Filters the relevant features of a track in returns them in JSON object.

    Parameter
    ---------
    track: Object
        Track returend by the spotify API

    genre: string
        Genre that should be used

    Return
    ------
    relevant_features: Object
        JSON Object that contains the relevant featues
    '''
    
    features = sp.audio_features(track['id'])[0]

    external_ids = track['external_ids'] if 'external_ids' in track else {}
    isrc = external_ids['isrc'] if 'isrc' in external_ids else NaN
    artist_names = []

    if 'artists' in track and type(track['artists']) == list:
        for artist in track['artists']:
            if 'name' in artist:
                artist_names.append(artist['name'])

    artist_names = ','.join(artist_names)
    
    if 'album' in track:
        album = track['album']['name'] if 'name' in track['album'] else NaN
        release_date = track['album']['release_date'] if 'release_date' in track['album'] else NaN
        release_date_precision = track['album']['release_date_precision'] if 'release_date_precision' in track['album'] else NaN
    else:
         album = NaN
         release_date = NaN
         release_date_precision = NaN


    track_name = track['name'] if 'name' in track else NaN
    if track_name != NaN:
        points = chart_power_df.loc[(chart_power_df.Song == track_name.lower()) & (chart_power_df.Artist == artist_names.lower())]['Points']
        if points.empty:
             points = NaN
        else:
            points = int(points)
    else:
         points = NaN


    return {
        'name': track_name,
        'artists': artist_names,
        'album': album,
        'release_date': release_date,
        'release_date_precision': release_date_precision,
        'spotify_id': track['id'] if 'id' in track else NaN,
        'chart_power': points,
        'uri': track['uri'] if 'uri' in track else NaN,
        'popularity': track['popularity'] if 'popularity' in track else NaN,
        'genres': genre,
        'danceability': features['danceability'] if 'danceability' in features else NaN,
        'energy': features['energy'] if 'energy' in features else NaN,
        'key': features['key'] if 'key' in features else NaN,
        'loudness': features['loudness'] if 'loudness' in features else NaN,
        'mode': features['mode'] if 'mode' in features else NaN,
        'speechiness': features['speechiness'] if 'speechiness' in features else NaN,
        'acousticness': features['acousticness'] if 'acousticness' in features else NaN,
        'instrumentalness': features['instrumentalness'] if 'instrumentalness' in features else NaN,
        'liveness': features['liveness'] if 'liveness' in features else NaN,
        'valence': features['valence'] if 'valence' in features else NaN,
        'tempo': features['tempo'] if 'tempo' in features else NaN,
        'duration_ms': features['duration_ms'] if 'duration_ms' in features else NaN,
        'time_signature': features['time_signature'] if 'time_signature' in features else NaN,
        'isrc': isrc,
    }


def get_number_of_tracks(release_year, start_letters, genre):
    '''
    Retrieves the number of tracks the spotfiy API returns for a specific query.

    Parameter
    ---------
    release_year: int
        Year the tracks were released

    start_letters: string
        Letters the songs start with

    genre: string
        Genre that should be used

    Return
    ------
    num: int
        Number of tracks that spotify has data for. The max number is 1000. If 1000 is returned, it is possible that the number is higher.
    '''
    try:
        result = sp.search(q=f'year:{release_year} track:{start_letters}* genre:{genre}', type='track', limit=1, offset=0, market='DE')
        tracks = result['tracks'] if 'tracks' in result else ''
        return tracks['total'] if 'total' in tracks else 0
    except Exception as e:
        # print(e)
        error_logger.error(e)
    return 0

def req_query_tracks(release_year, genres, start_letters = '', limit=50):
    '''
    Recursivley queries all tracks spotify returns for a specific query.

    Parameter
    ---------
    release_year: int
        Year the tracks were released

    genres: list
        Genres that should be queried

    start_letters: string, default=''
        Letters the songs start with
    
    limit: int; default=50
        Number of tracks that should be queried at once. Max number is 50
    '''
    global df
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if type(genres) == str:
        genres = [genres]
    for genre in genres:
        for letter in alphabet:
            letters = start_letters + letter
            status_logger.info(f'Getting number of tracks for: {release_year}, {letters}, {genre}...')
            total_results = get_number_of_tracks(release_year, letters, genre)
            status_logger.info('Number of tracks received!')
            if total_results < 1000:
                status_logger.info(f'{release_year}-{letters}-{genre}-{total_results}')
                # Loop through results and retrieve tracks
                offset = 0

                while offset < total_results:
                    try:
                        track_features = []
                        result = sp.search(q=f'year:{release_year} track:{letters}* genre:{genre}', type='track', limit=limit, offset=offset, market='DE')
                        tracks = result['tracks'] if 'tracks' in result else ''
                        if 'items' in tracks:
                            for track in tracks['items']:
                                features = filter_track_features(track, genre)
                                track_features.append(features)
                            offset += limit
                            df = pd.concat([df, pd.DataFrame(track_features)], ignore_index=True)
                        else:
                            continue
                    except Exception as e:
                        # print(e)
                        error_logger.error(e)
            else:
                req_query_tracks(release_year, genre, letters)
        df.to_csv('transfer/data.csv', index=False)

columns = ['name', 'artists', 'album', 'release_date', 'release_date_precision', 'chart_power', 'spotify_id', 'uri', 'popularity', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature', 'isrc', 'genres']
df = pd.DataFrame(columns=columns)


genres = sp.recommendation_genre_seeds()['genres']
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
for year in range(1980, 1990):
    req_query_tracks(year, genres, '')