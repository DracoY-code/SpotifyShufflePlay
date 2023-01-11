# This file defines all the custom exceptions.

class UserAccessError(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        super().add_note('User access unsuccessful!')


class PlaylistAccessError(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        super().add_note('Playlist access unsuccessful!')


class MissingSpotifyUserIdError(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        super().add_note('1 positional argument missing: SPOTIFY_USER_ID')


class MissingPlaylistIdError(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        super().add_note('1 positional argument missing: PLAYLIST_ID')


class SpotifyAPIError(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        super().add_note(f'{args}: an API error has occured!')
