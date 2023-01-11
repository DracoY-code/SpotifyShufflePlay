import sys

from modules.alias import *
from modules.exceptions import *
from modules.shuffler import Shuffler


# Variable definitions
shuffler: Shuffler
username: StringOrNone
playlist_id: StringOrNone

if sys.argv[1:]:
    username = sys.argv[1]
    shuffler = Shuffler(username=username)
    if sys.argv[2:]:
        playlist_id = sys.argv[2]
        shuffler.start(playlist_id=playlist_id)

        while True:
            if input('Change track (q to quit)? ') == 'q':
                print('Quitting...')
                break
            else:
                shuffler.next()
    else:
        raise MissingPlaylistIdError
else:
    raise MissingSpotifyUserIdError
