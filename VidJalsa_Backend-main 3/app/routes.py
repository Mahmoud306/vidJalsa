from typing import List
from fastapi import APIRouter
from app.youtube_services.youtube_api_interaction import return_filtered_and_formatted_videos
from app.google_trends_services.trends_api_interaction import get_trending_topics
from app.main_processing_services.llm_chains_interactions import process_videos

from app.schemas import VideoUrlsAndTopic, Video

router = APIRouter()

@router.get("/api/v1/trending", response_model=List[str])
def trending_topics():
    """
    Get the list of trending topics from the Google Trends API.

    Returns:
        List[str]: The list of trending topics.
    """
    return get_trending_topics()

@router.post("/api/v1/videos_preview")
def videos_preview(video: Video):
    """
    Return filtered and formatted videos based on the given video information.

    Args:
        video (Video): The video information.

    Returns:
        The filtered and formatted videos.
    """
    return return_filtered_and_formatted_videos(video)

@router.post("/api/v1/process_videos")
async def api_process_videos(request_data: VideoUrlsAndTopic):
    """
    Process the videos based on the given video URLs.

    Args:
        video_urls (VideoUrls): The video URLs.

    Returns:
        The processed videos.
    """
    return await process_videos(request_data.urls, request_data.topic)
