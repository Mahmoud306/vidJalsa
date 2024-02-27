from pytrends.request import TrendReq
from fastapi import HTTPException

def get_trending_topics() -> list:
    """
    Fetches the current trending search topics from Google Trends for the United States.

    Returns:
        list: A list of the top trending search topics.

    Raises:
        HTTPException: If an error occurs during the request to Google Trends.
    """
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        trending = pytrends.trending_searches(pn='united_states')
        topics = trending[0].head(8).tolist()
        return topics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching trending topics: {e}")
