import re
import os
from fastapi import HTTPException
from .blog_template import header_template, styling_template, content_template

def generate_deployment_url(directory_name: str) -> str:
    """Generates a URL for the deployed blog based on the directory name."""
    return f"http://127.0.0.1:7000/{directory_name}/index.html"


def parse_json_like_string(json_string: str) -> dict:
    """
    Parses a string that resembles JSON format into a Python dictionary.

    Parameters:
    - json_string (str): A string formatted similarly to JSON.

    Returns:
    - dict: Parsed data as a dictionary.

    Raises:
    - HTTPException: If parsing fails.
    """
    try:
        lines = json_string.strip().split('\n')
        parsed_data = {}
        inside_array = False
        array_key = ''
        array_values = []

        for line in lines:
            if '[' in line:
                colon_index = line.find(':')
                array_key = line[:colon_index].strip().strip('"{} ')
                inside_array = True
                continue
            if ']' in line:
                inside_array = False
                parsed_data[array_key] = array_values
                array_values = []
                continue
            if inside_array:
                array_value = line.strip().strip('"{}[], ')
                if array_value:
                    array_values.append(array_value)
                continue

            colon_index = line.find(':')
            if colon_index != -1:
                key = line[:colon_index].strip().strip('"{} ')
                value = line[colon_index + 1:].strip().strip('"{}[], ')
                parsed_data[key] = value

        return parsed_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during parsing: {str(e)}")


def parse_article(content: str) -> dict:
    """
    Extracts key-value pairs from a string using regular expressions and returns them as a dictionary.

    Parameters:
    - content (str): The content string to be parsed.

    Returns:
    - dict: Extracted data as a dictionary.

    Raises:
    - HTTPException: If parsing fails.
    """
    try:
        pattern = r'\*\*(.+?)\*\*:\s*"(.+?)"'
        matches = re.findall(pattern, content, re.DOTALL)

        article_json = {'Paragraphs': []}
        for key, value in matches:
            if "Paragraph" in key:
                article_json['Paragraphs'].append(value)
            else:
                article_json[key] = value

        return article_json
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during article parsing: {str(e)}")
    

def directory_generator(html_content: str, deployment_directory: str, deployment_name: str) -> str:
    """
    Generates a directory for storing HTML content and writes the content to an index.html file.

    Parameters:
    - html_content (str): The HTML content to write.
    - deployment_directory (str): The root directory for deployment.
    - deployment_name (str): The name of the deployment.

    Returns:
    - str: The path to the generated directory.

    Raises:
    - HTTPException: If directory generation fails.
    """
    try:
        user_output_dir = os.path.join(deployment_directory, deployment_name)
        os.makedirs(user_output_dir, exist_ok=True)
        with open(os.path.join(user_output_dir, "index.html"), "w") as html_file:
            html_file.write(html_content)

        return user_output_dir
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during directory generation: {str(e)}")


def extract_video_id(url: str) -> str:
    """
    Extracts the video ID from a YouTube URL using regular expressions.

    Parameters:
    - url (str): The YouTube URL.

    Returns:
    - str: The extracted video ID, or an empty string if no ID is found.

    Raises:
    - HTTPException: If extraction fails.
    """
    try:
        regex_patterns = [
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&\s]+)',
            r'(?:https?:\/\/)?youtu\.be\/([^&\s]+)',  
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^&\s]+)', 
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([^&\s]+)'
        ]

        for pattern in regex_patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return ""
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during video ID extraction: {str(e)}")


def render_blog(title: str, question: str, author: str, paragraphs: list,image_url) -> str:
    """
    Renders an HTML blog post using templates for the header, styling, and content.

    Parameters:
    - title (str): The blog post title.
    - question (str): The blog post question.
    - author (str): The author of the blog post.
    - paragraphs (list): A list of paragraphs in the blog post.

    Returns:
    - str: The complete HTML content of the blog post.
    """
    try:
        paragraphs_html_content = ""
        for paragraph in paragraphs:
                paragraphs_html_content += f'<p>{paragraph}</p>\n'

        header = header_template.format(title=title)    
        content = content_template.format(author=author, title=title, question=question, paragraphs_html_content=paragraphs_html_content,image_url=image_url)
        
        return header + styling_template + content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during blog rendering: {str(e)}")


def extract_video_ids(youtube_links):
    """
    Extracts video IDs from a list of YouTube links.

    Args:
        youtube_links (list): A list of YouTube links.

    Returns:
        list: A list of video IDs extracted from the YouTube links.
    """
    video_ids = []
    for link in youtube_links:
        print(f"Type of link: {type(link)}")  # Add this line to debug
        match = re.search(r"watch\?v=([^\s&]+)", link)
        if match:
            video_ids.append(match.group(1))
    return video_ids