import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import AzureChatOpenAI
from openai import AzureOpenAI

azure_image_api = os.getenv('IMAGE_API_KEY')
if not azure_image_api:
    raise EnvironmentError("Azure API key (azure_image_api) not found in environment variables.")

azure_image_endpoint= os.getenv('IMAGE_AZURE_ENDPOINT')
if not azure_image_endpoint:
    raise EnvironmentError("Azure endpoint (image_azure_endpoint) not found in environment variables.")

# Load API keys and endpoints from environment variables, ensuring they exist.
AZURE_API_KEY = os.getenv('API_KEY')
if not AZURE_API_KEY:
    raise EnvironmentError("Azure API key (AZURE_API_KEY128) not found in environment variables.")

AZURE_ENDPOINT = os.getenv('END_POINT')
if not AZURE_ENDPOINT:
    raise EnvironmentError("Azure endpoint (AZURE_ENDPOINT128) not found in environment variables.")

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise EnvironmentError("Google API key (GOOGLE_API_KEY) not found in environment variables.")

# Configure the Google Generative AI with the API key.
# This configuration is critical for enabling interactions with Google's generative AI services.
try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    raise RuntimeError(f"Failed to configure Google Generative AI: {e}")

# Initialize instances for interacting with AI models.
# These instances allow for the use of generative AI in processing tasks, such as text summarization and generation.
try:
    client = AzureOpenAI(
        api_version="2023-12-01-preview",
        azure_endpoint=azure_image_endpoint,
        api_key= azure_image_api,
    )
except Exception as e:
    raise RuntimeError(f"Failed to initialize Azure Image OpenAI instance: {e}")

try:
    google_llm = ChatGoogleGenerativeAI(google_api_key=GOOGLE_API_KEY, model="gemini-pro")
except Exception as e:
    raise RuntimeError(f"Failed to initialize Google Generative AI instance: {e}")

try:
    azure_llm = AzureChatOpenAI(api_key=AZURE_API_KEY, model="gpt-4",
                                openai_api_version="2023-07-01-preview",
                                azure_endpoint=AZURE_ENDPOINT, temperature=0.55)
except Exception as e:
    raise RuntimeError(f"Failed to initialize Azure Chat OpenAI instance: {e}")
