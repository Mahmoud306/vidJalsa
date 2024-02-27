import os
from googleapiclient.discovery import build

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
if not YOUTUBE_API_KEY:
    raise EnvironmentError("YouTube API key not found in environment variables.")

def initialize_youtube_service() -> object:
    """
    Initializes the YouTube Data API client using the developer API key.

    The API key is read from the environment variables and should be set before
    the application starts. It's recommended to use a secure way to set environment
    variables, such as through a .env file or a cloud service's environment management.

    Returns:
        object: An instance of the YouTube Data API client, which can be used to make
                requests to the YouTube Data API.

    Raises:
        EnvironmentError: If the YOUTUBE_API_KEY environment variable is not found.
    """
    return build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
