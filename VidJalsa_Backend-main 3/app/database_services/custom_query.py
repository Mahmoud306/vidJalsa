from app.database import database_connection
from app.database.models.models import User, Blog, Deployments


def get_blogs_by_username(username):
    """
    Retrieve blogs written by a user with the given username.

    Args:
        username (str): The username of the user.

    Returns:
        list: A list of Blog objects written by the user, or None if the user does not exist.
    """
    session = database_connection.get_session()
    # Retrieve the user by the username
    user = session.query(User).filter(User.username == username).first()

    if user is not None:
        # Retrieve blogs written by the user
        blogs = session.query(Blog).filter(Blog.user_id == user.id).all()
        return blogs
    else:
        return None


def check_deployment_video_exists(video_name):
    """
    Check if a deployment video with the given name exists.

    Args:
    session (Session): The database session to use for the query.
    video_name (str): The name of the video to check.

    Returns:
    bool: True if the video exists, False otherwise.
    """
    session = database_connection.get_session()
    return session.query(Deployments).filter(Deployments.deployment_video == video_name).first()