import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))