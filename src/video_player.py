"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist
from .video import Video
import random


class VideoPlayer:
    """A class used to represent a Video Player."""

    currently_playing = None
    is_playing = False
    playlists = []

    def __init__(self):
        self._video_library = VideoLibrary()

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        all_videos = self._video_library.get_all_videos()
        all_videos.sort(key=lambda x: x.title)
        print("Here's a list of all available videos:")
        for video in all_videos:
            if video.flag.get('status') == 1:
                print(f"{video.title} ({video.video_id}) [{' '.join(str(x) for x in video.tags)}] - FLAGGED (reason: {video.flag.get('reason')})")
            else:
                print(f"{video.title} ({video.video_id}) [{' '.join(str(x) for x in video.tags)}]")

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        user_video = self._video_library.get_video(video_id)
        if user_video == None:
            print("Cannot play video: Video does not exist")
        elif user_video.flag.get('status') == 1:
            print(f"Cannot play video: Video is currently flagged (reason: {user_video.flag.get('reason')})")
        else:
            if VideoPlayer.currently_playing != None:
                print(f"Stopping video: {VideoPlayer.currently_playing.title}")
            VideoPlayer.currently_playing = user_video
            VideoPlayer.is_playing = True
            print(f"Playing video: {VideoPlayer.currently_playing.title}")

    def stop_video(self):
        """Stops the current video."""
        if VideoPlayer.currently_playing != None:
            print(f"Stopping video: {VideoPlayer.currently_playing.title}")
            VideoPlayer.currently_playing = None
            VideoPlayer.is_playing = False
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        video_list = []
        for video in self._video_library.get_all_videos():
            if video.flag.get('status') == 0:
                video_list.append(video)
        if len(video_list) == 0:
            print("No videos available")
        else:
            random_number = random.randint(0, len(video_list) - 1)
            video = video_list[random_number]
            self.play_video(video.video_id)

    def pause_video(self):
        """Pauses the current video."""
        if VideoPlayer.is_playing == True:
            print(f"Pausing video: {VideoPlayer.currently_playing.title}")
            VideoPlayer.is_playing = False
        elif VideoPlayer.currently_playing != None:
            print(
                f"Video already paused: {VideoPlayer.currently_playing.title}")
        else:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        """Resumes playing the current video."""
        if VideoPlayer.is_playing == True:
            print("Cannot continue video: Video is not paused")
        elif VideoPlayer.currently_playing != None:
            print(f"Continuing video: {VideoPlayer.currently_playing.title}")
            VideoPlayer.is_playing = True
        else:
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        """Displays video currently playing."""
        video = VideoPlayer.currently_playing
        if video != None:
            if VideoPlayer.is_playing:
                print(
                    f"Currently playing: {video.title} ({video.video_id}) [{' '.join(str(x) for x in video.tags)}]")
            else:
                print(
                    f"Currently playing: {video.title} ({video.video_id}) [{' '.join(str(x) for x in video.tags)}] - PAUSED")
        else:
            print("No video is currently playing")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if VideoPlayer.playlists.count != 0:
            allOk = True
            for playlist in VideoPlayer.playlists:
                if playlist.name.lower() == playlist_name.lower():
                    allOk = False
                    break
            if allOk:
                new = Playlist(playlist_name)
                VideoPlayer.playlists.append(new)
                print(f"Successfully created new playlist: {new.name}")
            else:
                print(
                    "Cannot create playlist: A playlist with the same name already exists")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        user_video = self._video_library.get_video(video_id)
        user_playlist = None
        for playlist in VideoPlayer.playlists:
            if playlist.name.lower() == playlist_name.lower():
                user_playlist = playlist
                break
        if user_playlist == None:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
        elif user_video == None:
            print(f"Cannot add video to {playlist_name}: Video does not exist")
        elif user_video.flag.get('status') == 1:
            print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {user_video.flag.get('reason')})")
        else:
            AllOk = True
            if len(user_playlist.video) != 0:
                for video in user_playlist.video:
                    if video.video_id == video_id:
                        AllOk = False
                        break
            if AllOk:
                user_playlist.video.append(user_video)
                print(f"Added video to {playlist_name}: {user_video.title}")
            else:
                print(
                    f"Cannot add video to {playlist_name}: Video already added")

    def show_all_playlists(self):
        """Display all playlists."""

        if len(VideoPlayer.playlists) == 0:
            print("No playlists exist yet")
        else:
            sorted_list = sorted(VideoPlayer.playlists, key=lambda playlist: playlist.name)
            print("Showing all playlists:")
            for playlist in sorted_list:
                print(playlist.name)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        user_playlist = None
        for playlist in VideoPlayer.playlists:
            if playlist.name.lower() == playlist_name.lower():
                user_playlist = playlist
                break
        if user_playlist == None:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
            userChoice = input(f"Do you want to create a playlist called: {playlist_name}?[Y/N]: ")
            if userChoice.lower() == 'y':
                self.create_playlist(playlist_name)
        else:
            if len(user_playlist.video) == 0:
                print(f"Showing playlist: {playlist_name}")
                print("No videos here yet")
            else:
                if len(user_playlist.video) == 1:
                    num_video = "video"
                else:
                    num_video = "videos"
                print(f"Showing playlist: {playlist_name} ({len(user_playlist.video)} {num_video})")
                for video in user_playlist.video:
                    if video.flag.get('status') == 1:
                        print(f"{video.title} ({video.video_id}) [{' '.join(str(x) for x in video.tags)}] - FLAGGED (reason: {video.flag.get('reason')})")
                    else:
                        print(f"{video.title} ({video.video_id}) [{' '.join(str(x) for x in video.tags)}]")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        user_playlist = None
        for playlist in VideoPlayer.playlists:
            if playlist.name.lower() == playlist_name.lower():
                user_playlist = playlist
                break
        if user_playlist == None:
            print(
                f"Cannot remove video from {playlist_name}: Playlist does not exist")
        else:
            delete_video = None
            for video in user_playlist.video:
                if video.video_id == video_id:
                    delete_video = video
            if delete_video != None:
                print(
                    f"Removed video from {playlist_name}: {delete_video.title}")
                user_playlist.video.remove(delete_video)
            else:
                print(
                    f"Cannot remove video from {playlist_name}: Video does not exist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        user_playlist = None
        for playlist in VideoPlayer.playlists:
            if playlist.name.lower() == playlist_name.lower():
                user_playlist = playlist
                break
        if user_playlist == None:
            print(
                f"Cannot clear playlist {playlist_name}: Playlist does not exist")
        else:
            user_playlist.video.clear()
            print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        user_playlist = None
        for playlist in VideoPlayer.playlists:
            if playlist.name.lower() == playlist_name.lower():
                user_playlist = playlist
                break
        if user_playlist == None:
            print(
                f"Cannot delete playlist {playlist_name}: Playlist does not exist")
        else:
            VideoPlayer.playlists.remove(user_playlist)
            print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        list_result = []
        for video in self._video_library.get_all_videos():
            if video.flag.get('status') == 0:
                if search_term.lower() in video.title.lower():
                    list_result.append(video)
        self.display_results(list_result, search_term)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        list_videos = []
        for video in self._video_library.get_all_videos():
            if video.flag.get('status') == 0:
                for tag in video.tags:
                    if video_tag.lower() in tag.lower():
                        list_videos.append(video)
                        break
        self.display_results(list_videos, video_tag)

    def display_results(self, list_result, search_term):
        if len(list_result) == 0:
            print(f"No search results for {search_term}")
        else:
            print(f"Here are the results for {search_term}:")
            for i in range(0, len(list_result)):
                print(
                    f"{i+1}) {list_result[i].title} ({list_result[i].video_id}) [{' '.join(str(tag) for tag in list_result[i].tags)}]")
            print("would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            userChoice = input()
            try:
                userInt = int(userChoice)
                if (int(userChoice) > 0 and int(userChoice) <= len(list_result)):
                    self.play_video(list_result[int(userChoice)-1].video_id)
            except ValueError:
                print()

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        user_video = self._video_library.get_video(video_id)

        if user_video != None:
            if user_video.flag.get("status") == 1:
                print("Cannot flag video: Video is already flagged")
            else:
                user_video.flag.update({"status": 1})
                if flag_reason == "":
                    flag_reason = "Not supplied"
                user_video.flag.update({"reason": flag_reason})
                if VideoPlayer.currently_playing == user_video:
                    self.stop_video()
                print(f"Successfully flagged video: {user_video.title} ({user_video.flag.get('reason')})")
        else:
            print("Cannot flag video: Video does not exist")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        user_video = self._video_library.get_video(video_id)

        if user_video == None:
            print("Cannot remove flag from video: Video does not exist")
        elif user_video.flag.get('status') == 0:
            print("Cannot remove flag from video: Video is not flagged")
        else:
            user_video.flag.update({"status": 0})
            user_video.flag.update({"reason": ""})
            if user_video.flag.get('status') == 0 and user_video.flag.get('reason') == "":
                print(f"Successfully removed flag from video: {user_video.title}")
            else:
                print("An error occurred")

