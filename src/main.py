import os
from model import chat_model
from dotenv import load_dotenv

# Reads key value pairs from .env file and adds them to environment variables
load_dotenv()

out = chat_model(
    system_content='You are a nice chat model',
    user_content='Who invented the wheel?',
)

print(out.choices[0].message)


