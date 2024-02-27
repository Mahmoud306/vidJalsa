import time

from fastapi import HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_core.output_parsers import StrOutputParser
from .utils import extract_video_id
from .prompts_templates import summarize_prompt_text, blog_gen_prompt_text , image_generation_prompt
from . import google_llm, azure_llm , client
import json
from .prompts_templates import summarize_prompt_text, blog_gen_prompt_text, blog_quality_template
from . import google_llm, azure_llm

class TranscriptProcessor:
    """
    Handles the fetching, chunking, and summarizing of YouTube video transcripts.
    """
    
    def fetch(self, url: str) -> list:
        """
        Retrieves the transcript for a given YouTube video URL.
        
        Parameters:
        - url (str): The YouTube video URL.
        
        Returns:
        - list: The fetched transcript as a list of dictionaries.
        
        Raises:
        - HTTPException: If fetching the transcript fails.
        """
        try:
            video_id = extract_video_id(url)
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return transcript
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred during fetching: {str(e)}")

    def chunk(self, transcript: list) -> list:
        """
        Chunks a transcript into smaller parts if necessary.
        
        Parameters:
        - transcript (list): The transcript to be chunked.
        
        Returns:
        - list: A list of chunked transcripts.
        
        Raises:
        - HTTPException: If chunking the transcript fails.
        """
        try:
            transcript_splitter = RecursiveCharacterTextSplitter(chunk_size=32000, chunk_overlap=3200)
            doc = [Document(page_content=str(transcript), metadata={"source": "local"})]
            return transcript_splitter.split_documents(doc)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred during chunking: {str(e)}")

    def summarize(self, chunked_transcripts: list) -> str:
        """
        Summarizes chunked transcripts.
        
        Parameters:
        - chunked_transcripts (list): The transcripts to be summarized.
        
        Returns:
        - str: The summarized transcript.
        
        Raises:
        - HTTPException: If summarization fails.
        """
        try:
            summarize_prompt = PromptTemplate(template=summarize_prompt_text, input_variables=["text"])
            blog_quality_prompt = PromptTemplate(template=blog_quality_template, input_variables=["text"])
            summarize_chain = load_summarize_chain(llm=google_llm, chain_type="map_reduce", map_prompt=summarize_prompt, combine_prompt = blog_quality_prompt)
            summarized_transcript = summarize_chain.run({'input_documents': chunked_transcripts})
            return summarized_transcript
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred during summarization: {str(e)}")



class ArticleGenerator:
    """
    Generates an article based on a combined summarized transcript.
    """
    def __init__(self):
        self.output_parser = StrOutputParser()

    def generate(self, combined_summarized_transcript: str) -> dict:
        """
        Generates the final article from the combined summarized transcript.
        
        Parameters:
        - combined_summarized_transcript (str): The summarized transcript to generate the article from.
        
        Returns:
        - dict: The generated article.
        
        Raises:
        - HTTPException: If article generation fails.
        """
        try:
            second_prompt_start_time = time.time()
            blog_gen_prompt = PromptTemplate(template=blog_gen_prompt_text, input_variables=["combined_summarized_transcript"])
            blog_gen_chain = blog_gen_prompt | azure_llm | self.output_parser
            response = blog_gen_chain.invoke({'combined_summarized_transcript': combined_summarized_transcript})
            second_prompt_end_time = time.time()
            print(f" second_prompt_time  {second_prompt_end_time - second_prompt_start_time}")
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred in article generation: {str(e)}")
        
class image_generator:
    """Generate an image based on the video title"""
    def Generate_image(video_title: str):
        try:
            generated_image = client.images.generate(
                model="dalle_images_lookup",
                prompt=image_generation_prompt.format(video_title=video_title),
                n=1,
            )

            image_url = json.loads(generated_image.json())['data'][0]['url']
            return image_url
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred in image generation: {str(e)}")

