import os
from googleapiclient.discovery import build


class Video:
    """Класс для видео"""
    api_key: str = os.environ.get('YouTube_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        try:
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                             id=video_id).execute()
            self.video_id = video_id
            self.video_title = video_response['items'][0]['snippet']['title']
            self.video_url = f"https://youtu.be/{video_response['items'][0]['id']}"
            self.view_count = video_response['items'][0]['statistics']['viewCount']
            self.like_count = video_response['items'][0]['statistics']['likeCount']

        except:
            self.id = video_id
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    """Класс для плейлиста"""
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return self.video_title
