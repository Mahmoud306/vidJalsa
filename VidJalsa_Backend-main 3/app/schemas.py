from pydantic import BaseModel
from typing import List

class Video(BaseModel):
    """Represents a video."""
    video: str  

class VideoUrlsAndTopic(BaseModel):
    """Represents a request with a list of video URLs and a topic."""
    urls: List[str]
    topic: str
