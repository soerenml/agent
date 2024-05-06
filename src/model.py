import os
import openai

def chat_model(
    system_content: str,
    user_content: str,
    api_key: str):
  """
  Calls OpenAI model

  Parameters
  ----------
  system_content: str
    How the bot behaves

  user_content: str
    Message to the bot

  api_key: str
    OpenAI API key

  Returns
  -------
  completion: str
    Response from the bot
  """
  openai.api_key = api_key

  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": system_content},
      {"role": "user", "content": user_content}
    ]
  )

  return completion