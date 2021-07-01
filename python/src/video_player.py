"""A video player class."""

import random
from .video_library import VideoLibrary
from .video_playlist import Playlist


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._video_currently_playing = None 
        self._playlists = {}
        self._is_paused = False

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")
    
    def describe_video(self, video):
        id = "(" + video.video_id + ")"

        tags = "[" 
        tags_list = video._tags
        for i in range(len(tags_list)):
            tags += tags_list[i]
            if i < len(tags_list) - 1:
                tags += " "
        tags += "]"

        description = video.title + " " + id + " " + tags 
        return description

    def show_all_videos(self):
        """Returns all videos."""

        videos_sorted = sorted(self._video_library.get_all_videos(), key=lambda vid: vid.title)

        print("Here's a list of all available videos:")
        for video in videos_sorted:
            print("  " +  self.describe_video(video) + " - FLAGGED (reason: " + str(video.flag) + ")")

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """

        video = self._video_library.get_video(video_id)
        if video != None:

            if not video.flag:

                if (self._video_currently_playing != None): 
                    self.stop_video()
                self._video_currently_playing = video
                self._is_paused = False
                print("Playing video: " + video.title)
            else:
                print("Cannot play video: Video is currently flagged (reason: " + video.flag + ")")
        else:
            print("Cannot play video: Video does not exist")

    def stop_video(self):
        """Stops the current video."""

        if self._video_currently_playing != None:
            print("Stopping video: " + self._video_currently_playing.title)
            self._video_currently_playing = None
        else:  
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""

        if not self._video_library.get_all_playable_videos():
            print("No videos available")
        else:
            rand_video = random.choice(self._video_library.get_all_playable_videos())

            if self._video_currently_playing != None:
                self.stop_video()

            self.play_video(rand_video.video_id)

    def pause_video(self):
        """Pauses the current video."""

        if self._video_currently_playing != None:

            if self._is_paused == False:
                self._is_paused = True
                print("Pausing video: " + self._video_currently_playing.title)
            else:
                print("Video already paused: " + self._video_currently_playing.title)
        else:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        """Resumes playing the current video."""

        if self._video_currently_playing != None:

            if self._is_paused == True:
                self._is_paused = False
                print("Continuing video: " + self._video_currently_playing.title)
            else:
                print("Cannot continue video: Video is not paused")
        else:
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        """Displays video currently playing."""

        if self._video_currently_playing != None:

            if self._is_paused == True:
                print("Currently playing: " + self.describe_video(self._video_currently_playing) + " - PAUSED")
            else:
                print("Currently playing: " + self.describe_video(self._video_currently_playing))  
        else:
            print("No video is currently playing")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() not in self._playlists:
            self._playlists[playlist_name.upper()] = Playlist(playlist_name)
            print("Successfully created new playlist: " + playlist_name)
        else:
            print("Cannot create playlist: A playlist with the same name already exists")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        if playlist_name.upper() in self._playlists:
            playlist = self._playlists.get(playlist_name.upper())
            video = self._video_library.get_video(video_id)

            if video != None:

                if not video.flag:

                    if video_id not in playlist.videos:
                        playlist.add_video(video_id)
                        print("Added video to " + playlist_name + ": " + video.title)
                    else:
                        print("Cannot add video to " + playlist_name + ": Video already added")
                else:
                    print("Cannot add video to " + playlist_name + ": Video is currently flagged (reason: " + video.flag + ")")
            else:
                print("Cannot add video to " + playlist_name + ": Video does not exist")

        else:
            print("Cannot add video to " + playlist_name + ": Playlist does not exist")

    def show_all_playlists(self):
        """Display all playlists."""

        if self._playlists:
            print("Showing all playlists:")
            playlists_sorted = sorted(self._playlists.values(), key=lambda playlist: playlist.title)
            for playlist in playlists_sorted:
                print("  " + playlist.title)
        else:
            print("No playlists exist yet")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() in self._playlists:
            playlist = self._playlists.get(playlist_name.upper())
            print("Showing playlist: " + playlist_name)

            if len(playlist.videos) != 0:
                for video_id in playlist.videos:
                    video = self._video_library.get_video(video_id)
                    print("  " + self.describe_video(video) + " - FLAGGED (reason: " + str(video.flag) + ")")
            else:
                print("  No videos here yet")
        else:
            print("Cannot show playlist " + playlist_name + ": Playlist does not exist")
        
    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        if playlist_name.upper() in self._playlists:
            playlist = self._playlists.get(playlist_name.upper())
            video = self._video_library.get_video(video_id)

            if video != None:

                if video_id in playlist.videos:
                    playlist.remove_video(video_id)
                    print("Removed video from " + playlist_name + ": " + video.title)
                else:
                    print("Cannot remove video from " + playlist_name + ": Video is not in playlist")
            else:
                print("Cannot remove video from " + playlist_name + ": Video does not exist")

        else:
            print("Cannot remove video from " + playlist_name + ": Playlist does not exist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if playlist_name.upper() in self._playlists:
            playlist = self._playlists.get(playlist_name.upper())
            playlist.clear()
            print("Successfully removed all videos from " + playlist_name)          
        else:
            print("Cannot clear playlist " + playlist_name + ": Playlist does not exist")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() in self._playlists:
            del self._playlists[playlist_name.upper()]
            print("Deleted playlist: " + playlist_name)          
        else:
            print("Cannot delete playlist " + playlist_name + ": Playlist does not exist")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """

        videos_sorted = sorted(self._video_library.get_all_playable_videos(), key=lambda vid: vid.title)
        videos_found = list()
            
        for video in videos_sorted:
            if search_term.lower() in video.title.lower():
                videos_found.append(video)

        if videos_found:
            print("Here are the results for " + search_term + ":")

            for i in range(len(videos_found)):
                print("  " + str(i + 1) + ") " + self.describe_video(videos_found[i]))
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            answer = input()

            if answer.isdigit():
                answer = int(answer)

                if answer > 0 and answer <= len(videos_found):
                    self.play_video(videos_found[answer-1].video_id)

        else:
            print("No search results for " + search_term)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        videos_sorted = sorted(self._video_library.get_all_playable_videos(), key=lambda vid: vid.title)
        videos_found = list()

        for video in videos_sorted:
            tags = [tag.lower() for tag in video.tags]
            if video_tag.lower() in tags:
                videos_found.append(video)

        if videos_found:
            print("Here are the results for " + video_tag + ":")

            for i in range(len(videos_found)):
                print("  " + str(i + 1) + ") " + self.describe_video(videos_found[i]))
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            answer = input()

            if answer.isdigit():
                answer = int(answer)

                if answer > 0 and answer <= len(videos_found):
                    self.play_video(videos_found[answer-1].video_id)

        else:
            print("No search results for " + video_tag)

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video = self._video_library.get_video(video_id)
        if video != None:

            if video.flag == None: 
                video.add_flag(flag_reason)

                if video == self._video_currently_playing:
                    self.stop_video()
                print("Successfully flagged video: " + video.title + " (reason: " + video.flag + ")")
            else:
                print("Cannot flag video: Video is already flagged")
        else:
            print("Cannot flag video: Video does not exist")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)
        if video != None:

            if video.flag != None: 
                video.remove_flag()
                print("Successfully removed flag from video: " + video.title)
            else:
                print("Cannot remove flag from video: Video is not flagged")
        else:
            print("Cannot remove flag from video: Video does not exist")
