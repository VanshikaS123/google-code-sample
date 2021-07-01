"""A video playlist class."""

class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, playlist_title: str):
        self._title = playlist_title
        self._videos = list()

    @property
    def title(self) -> str:
        """Returns the title of playlist."""
        return self._title

    @property
    def videos(self):
        return self._videos

    def add_video(self, video_id):
        self._videos.append(video_id)

    def remove_video(self, video_id):
        self._videos.remove(video_id)
    
    def clear(self):
        self._videos.clear()