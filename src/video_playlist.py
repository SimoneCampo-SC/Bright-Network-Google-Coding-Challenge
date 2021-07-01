"""A video playlist class."""

from src.video import Video


class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, playlist_name: str):
        """Playlist constructor."""
        self._name = playlist_name
        self._video = []

    @property
    def name(self) -> str:
        """Returns the name of the playlist."""
        return self._name
    
    @property
    def video(self) -> Video:
        """Returns the list of videos."""
        return self._video