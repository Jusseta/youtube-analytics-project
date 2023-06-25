import os
from googleapiclient.discovery import build
import isodate
import datetime


class PlayList:
    api_key: str = os.environ.get('YouTube_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_info = self.youtube.playlists().list(id=playlist_id, part='contentDetails,snippet',
                                                                maxResults=50, ).execute()

        self.playlist_id = playlist_id
        self.title = self.playlist_info['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        total_duration = datetime.timedelta()

        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)).execute()

        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self):
        best_video = ''

        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)).execute()

        for video in video_response['items']:
            if int(video['statistics']['likeCount']) > 0:
                best_video = video['id']

        return f'https://youtu.be/{best_video}'
