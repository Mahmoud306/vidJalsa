import time
import threading
from fastapi import HTTPException
from .utils import (directory_generator, render_blog, parse_json_like_string, 
                    generate_deployment_url, extract_video_ids)
from .llm_chains_classes import TranscriptProcessor, ArticleGenerator, image_generator
from app.database import database_connection
from app.database.database import AbstractDatabase
from app.database.cruds.blog_crud import BlogCRUD
from app.database.cruds.deployment_crud import DeploymentCRUD
from app.database_services.custom_query import check_deployment_video_exists
import datetime
import time
from typing import List

transcript_processor = TranscriptProcessor()
article_generator = ArticleGenerator()


def fetch_summarize_process(url, idx):
    """
    Fetches, chunks, summarizes a transcript, prints the time taken, and returns a summarized string.
    """
    start_thread_time = time.time()
    try:
        fetched_transcript = transcript_processor.fetch(url)
        if fetched_transcript is None:
            return ""
        chunked_transcripts = transcript_processor.chunk(fetched_transcript)
        summarized_transcript = transcript_processor.summarize(chunked_transcripts)
        end_thread_time = time.time()
        print(f"Thread {idx} processing time: {end_thread_time - start_thread_time} seconds")
        return summarized_transcript
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video URL {url}: {str(e)}")


def generate_deployment_name(base_username="hamza"):
    """Generates a unique deployment name based on the username and current timestamp."""
    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    return f"{base_username}_{formatted_time}"


def handle_existing_blog(blog, blogCrud):
    """
    Handles the processing for an existing blog by generating its deployment URL.

    Parameters:
    - blog: The blog object retrieved from the database.
    - blogCrud: The CRUD object for blog operations.

    Returns:
    - dict: A dictionary containing a message and the deployment URL.
    """
    exited_blog = blogCrud.get(blog.blog_id)
    html_content = render_blog(title=exited_blog.title, question=exited_blog.question, author=exited_blog.user_id,
                               paragraphs=exited_blog.paragraphs,image_url=exited_blog.image_url)
    directory_name = directory_generator(html_content, "app/user", generate_deployment_name())
    deployment_url = generate_deployment_url(directory_name)
    time.sleep(0.5)  # Pause for 1 second
    return {"message": "The Processing Is Finished!", "deployment_url": deployment_url}


def generate_video_image_task(results, topic):
    results['generate_video_image'] = generate_video_image(topic)


def fetch_summarize_process_task(url, idx, results):
    results[idx] = fetch_summarize_process(url, idx)


def process_new_blog(video_urls, sorted_ids_string, blogCrud, deploymentCrud, topic):
    """
    Processes new blogs from video URLs, saves them, and generates a deployment URL. Also records the deployment
    in the database using DeploymentCRUD.

    Parameters:
    - video_urls (list): A list of video URLs to process.
    - sorted_ids_string (str): A string of sorted video IDs used for deployment tracking.
    - blogCrud: The CRUD object for blog operations.
    - deploymentCrud: The CRUD object for deployment operations.

    Returns:
    - dict: A dictionary containing a message and the deployment URL.
    """

    results = {}
    threads = []

    all_threads_time = time.time()

    thread = threading.Thread(target=generate_video_image_task, args=(results, topic))
    threads.append(thread)
    thread.start()

    for i, url in enumerate(video_urls):
        thread = threading.Thread(target=fetch_summarize_process_task, args=(url, i, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


    print(f"all_threads_time {time.time() - all_threads_time}")

    image_result = results.get('generate_video_image')

    summarized_transcripts = [results[i] for i in range(len(video_urls)) if i in results]
    combined_summarized_transcript = "\n\n\n\n".join(summarized_transcripts)

    json_output = article_generator.generate(combined_summarized_transcript)
    json_output = parse_json_like_string(json_output)

    after_second_propmt_time = time.time()

    # Add new blog entry to the database
    current_blog = blogCrud.add(1, json_output["Title"], json_output["Question"], json_output["Paragraphs"], image_result)

    # Deployment name generation and deployment record creation
    deployment_name = generate_deployment_name()
    deploymentCrud.add(deployment_name=deployment_name, deployment_video=sorted_ids_string, user_id=1,
                       blog_id=int(current_blog.id))

    # Generate HTML content and deployment URL
    html_content = render_blog(title=json_output["Title"], question=json_output["Question"],
                               author=json_output["Author"], paragraphs=json_output["Paragraphs"],
                               image_url=image_result)
    directory_name = directory_generator(html_content, "app/user", deployment_name)
    deployment_url = generate_deployment_url(directory_name)

    print(f"after second propmt time {time.time() - after_second_propmt_time}")

    return {"message": "The Processing Is Finished!", "deployment_url": deployment_url}


def generate_video_image(video_title: str) -> str:
    image_url = image_generator.Generate_image(video_title)
    return image_url


async def process_videos(video_urls: List[str], topic: str):
    """
    Asynchronously processes a list of video URLs to generate and deploy an article.

    Parameters:
    - video_urls (VideoUrls): A data model containing a list of video URLs.

    Returns:
    - dict: A dictionary containing a message and a deployment URL of the generated article.

    Raises:
    - HTTPException: If video processing fails.
    """

    full_time_start = time.time()
    print(video_urls, topic)
    # try:
    start_time = time.time()
    print("Checking for existing blog")
    video_ids = extract_video_ids(video_urls)
    sorted_ids_string = ' '.join(sorted(video_ids))
    blog = check_deployment_video_exists(sorted_ids_string)
    blogCrud = BlogCRUD(database_connection)
    deploymentCrud = DeploymentCRUD(database_connection)
    if blog:

        return handle_existing_blog(blog, blogCrud)
    else:
        print("Processing Started")
        response = process_new_blog(video_urls, sorted_ids_string, blogCrud, deploymentCrud, topic)
        full_time_end = time.time()
        print(f"  full_time:  {full_time_end - full_time_start}")
        return response
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"An error occurred during video processing: {str(e)}")
    # finally:
    # print(f"Processing Finished in {time.time() - start_time} seconds")