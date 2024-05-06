import os
from model import chat_model
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

out = chat_model(
    system_content='You are a nice chat model',
    user_content='Who invented the wheel?',
    api_key=api_key
)

print(out.choices[0].message)


