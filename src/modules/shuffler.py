import json
import os
import random

from modules.alias import *
from modules.exceptions import *

from spotipy import Spotify, SpotifyException
from spotipy.oauth2 import SpotifyOAuth

from dotenv import load_dotenv
load_dotenv(dotenv_path='src/resources/.env')


class Shuffler:
    """This class
        1. loads the spotipy object,
        2. randomises the playlist into a queue,
        3. and plays the shuffled playlist.
    """
    def __init__(self, username: StringOrNone = None) -> None:
        self.client_id: StringOrNone 
        self.client_secret: StringOrNone
        self.redirect_uri: StringOrNone

        self.client_id = os.getenv('SPOTIPY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
        
        self.scope: StringOrNone
        self._load_scope()

        self.sp: Spotify
        try:
            self._setup(username=username)
        except:
            print('Removing cache...')
            os.remove(f'cache/.cache-{username}')
            self._setup(username=username)

    def _load_scope(self) -> None:
        """This loads the scope.json file and sets the scope variable.
        """
        with open('src/resources/scope.json') as fp:
            self.scope = ' '.join(json.load(fp)['scope'])

    def _setup(self, username: StringOrNone = None) -> None:
        """This sets up the spotipy object and manages the cache.
        """
        self.sp = Spotify(auth_manager=SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
            cache_path=f'cache/{username}'
        ))

    def next(self) -> None:
        """This plays the next track from the randomised queue.
        """
        try:
            self.sp.next_track()
        except SpotifyException as e:
            raise SpotifyAPIError(e.http_status)

    def start(self, playlist_id: StringOrNone = None) -> None:
        """This executes the shuffling process.
            1. GET User Details
            2. GET Playlist Details
            3. Randomise the playlist
            4. Play it
        """
        user: JSON
        name: StringOrNone
        playlist: JSON
        playlist_title: StringOrNone
        follow_count: IntOrNone
        queue: list[JSON]
        
        try:
            user = self.sp.current_user()
            if user is None:
                raise UserAccessError
            name = user['display_name']
            print(f'Logged in as "{name}" successfully!\n')

            playlist = self.sp.playlist(playlist_id=playlist_id)
            if playlist is None:
                raise PlaylistAccessError
            playlist_title = playlist['name']
            follow_count = playlist['followers']['total']
            print(f'Playlist    : {playlist_title}')
            print(f'Followers   : {follow_count}\n')

            queue = playlist['tracks']['items']
            random.shuffle(queue)
            for track in queue:
                if track is not None:
                    self.sp.add_to_queue(uri=track['track']['uri'])
        except SpotifyException as e:
            raise SpotifyAPIError(e.http_status)
