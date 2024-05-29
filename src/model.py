import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_model(system_content: str, user_content: str):
  """
  Generates a chat response using the OpenAI GPT-3.5 Turbo model.

  Args:
    system_content (str): The content of the system message.
    user_content (str): The content of the user message.

  Returns:
    str: The generated chat response.

  Raises:
    OpenAIError: If there is an error in generating the chat response.

  """
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": system_content},
      {"role": "user", "content": user_content}
    ]
  )

  return completion