from isodate import parse_duration
from fastapi import HTTPException
from googleapiclient.errors import HttpError
from app.schemas import Video
from app.youtube_services import initialize_youtube_service


def retrieve_youtube_search_results(youtube_service, topic: str, max_results: int) -> list:
    """
    Retrieves a list of YouTube search results for a given topic.
    
    Parameters:
    - youtube_service (object): The initialized YouTube service client.
    - topic (str): The search query or topic.
    - max_results (int): The maximum number of search results to return.

    Returns:
    - list: A list of search results from YouTube.

    Raises:
    - HTTPException: If the search request fails.
    """
    try:
        search_request = youtube_service.search().list(
            q=topic,
            part='snippet',
            type='video',
            order='relevance',
            maxResults=max_results,
            safeSearch='strict',
            relevanceLanguage='en'
        )
        search_response = search_request.execute()
        
        if 'items' not in search_response:
            raise KeyError("The 'items' key is missing from the search response.")
        
        return search_response
    except HttpError as http_err:
        raise HTTPException(status_code=500, detail=f"YouTube search API request failed: {http_err}")
    except KeyError as key_err:
        raise HTTPException(status_code=500, detail=f"Invalid response format: {key_err}")



def extract_ids_from_search_results(search_results: dict) -> list:
    """
    Extracts video IDs from YouTube search results.

    Parameters:
    - search_results (dict): The search results returned from the YouTube API.

    Returns:
    - list: A list of video IDs extracted from the search results.

    Raises:
    - HTTPException: If video IDs cannot be extracted.
    """
    try:
        return [item['id']['videoId'] for item in search_results['items']]
    except KeyError as exc:
        raise HTTPException(status_code=500, detail="Extracting video IDs failed: " + str(exc))



def retrieve_youtube_video_details(youtube_service, video_ids: list) -> dict:
    """
    Fetches details for a list of YouTube video IDs.

    Parameters:
    - youtube_service (object): The initialized YouTube service client.
    - video_ids (list): A list of YouTube video IDs.

    Returns:
    - dict: A dictionary with video IDs as keys and video durations in seconds as values.

    Raises:
    - HTTPException: If fetching video details fails.
    """
    try:
        video_details_request = youtube_service.videos().list(
            part="contentDetails",
            id=",".join(video_ids)
        )
        video_details_response = video_details_request.execute()
        return {item['id']: parse_duration(item['contentDetails']['duration']).total_seconds()
                for item in video_details_response['items']}
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Fetching video details failed: " + str(exc))



def filter_videos_by_duration(video_details: dict, min_duration: int = 60, max_duration: int = 3600) -> list:
    """
    Filters videos by duration.

    Parameters:
    - video_details (dict): A dictionary mapping video IDs to their durations in seconds.
    - min_duration (int): The minimum duration of videos to include.
    - max_duration (int): The maximum duration of videos to include.

    Returns:
    - list: A list of video IDs that meet the duration criteria.

    Raises:
    - HTTPException: If the filtering process fails.
    """
    try:
        filtered_video_ids = [video_id for video_id, duration in video_details.items()
                                if min_duration < duration < max_duration]
        return filtered_video_ids
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Filtering videos by duration failed: " + str(exc))



def format_video_data_for_display(video_ids: list, search_results: dict, video_details: dict) -> list:
    """
    Formats video data for display based on video IDs, including video durations.

    Parameters:
    - video_ids (list): A list of video IDs to format.
    - search_results (dict): The original search results from the YouTube API.
    - video_details (dict): A dictionary with video IDs as keys and video durations in seconds as values.

    Returns:
    - list: A list of dictionaries, each containing formatted video information including duration.

    Raises:
    - HTTPException: If formatting the video data fails.
    """
    try:
        formatted_video_data = []
        for item in search_results['items']:
            video_id = item['id']['videoId']
            if video_id in video_ids:
                # Include duration in the formatted data
                duration = video_details.get(video_id, 0)  # Default to 0 if not found
                formatted_video_data.append({
                    'title': item['snippet']['title'],
                    'link': f"https://www.youtube.com/watch?v={video_id}",
                    'thumbnail': item['snippet']['thumbnails']['high']['url'],
                    'video_id': video_id,
                    'duration': duration,  # Include duration here
                })
        return formatted_video_data
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Formatting video data failed: " + str(exc))




def return_filtered_and_formatted_videos(video: Video, max_results: int = 10) -> list:
    """
    Orchestrates the process of filtering and formatting video previews based on a search topic.

    Parameters:
    - video (Video): An instance of Video schema containing the search topic.
    - max_results (int): The maximum number of videos to return after filtering.

    Returns:
    - list: A list of filtered and formatted video data for previews.

    Raises:
    - HTTPException: If any step in the process fails.
    """
    try:
        youtube_service = initialize_youtube_service()
        search_response = retrieve_youtube_search_results(youtube_service, video.video.lower(), max_results)
        
        if not isinstance(search_response, dict) or 'items' not in search_response:
            raise ValueError("Invalid search response format.")
        
        video_ids = extract_ids_from_search_results(search_response)
        video_details = retrieve_youtube_video_details(youtube_service, video_ids)
        
        filtered_video_ids = filter_videos_by_duration(video_details)
        videos_data = format_video_data_for_display(filtered_video_ids, search_response, video_details) 
        
        return videos_data[:max_results]
    except (HTTPException, ValueError) as exc:
        raise HTTPException(status_code=500, detail=f"Failed to return video previews: {exc}")
