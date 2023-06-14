import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.environ.get('YouTube_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.video_count = int(self.channel['items'][0]['statistics']['videoCount'])
        self.url = f"https://www.youtube.com/channel/{channel_id}"
        self.description = self.channel['items'][0]['snippet']['description']
        self.subscribers_count = int(self.channel['items'][0]['statistics']['subscriberCount'])
        self.view_count = int(self.channel['items'][0]['statistics']['viewCount'])

    def print_info(self):
        """Выводит в консоль информацию о канале."""
        data = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(data)

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return cls.youtube

    def to_json(self, filename):
        """сохраняет в файл значения атрибутов экземпляра `Channel`"""
        data = {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscribers_count": self.subscribers_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }

        with open(filename, 'w', encoding='UTF-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return self.subscribers_count + other.subscribers_count

    def __sub__(self, other):
        return self.subscribers_count - other.subscribers_count

    def __sub__(self, other):
        return other.subscribers_count - self.subscribers_count

    def __gt__(self, other):
        return self.subscribers_count > other.subscribers_count

    def __ge__(self, other):
        return self.subscribers_count >= other.subscribers_count

    def __lt__(self, other):
        return self.subscribers_count < other.subscribers_count

    def __le__(self, other):
        return self.subscribers_count <= other.subscribers_count

    def __eq__(self, other):
        return self.subscribers_count == other.subscribers_count
