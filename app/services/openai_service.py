from sentence_transformers import SentenceTransformer
import os
import json
import requests

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

#openai_client = OpenAI(api_key=OPENAI_API_KEY)
MODEL = SentenceTransformer("thenlper/gte-base")
CHATGPT_MODEL = "gpt-4-turbo-preview"

messages = [{"role": "system", "content": "You are a helpful online bookstore assistant (you can provide book recommendations/availability, add selected items to a user's shopping cart, and answer general inquiries about store policies, shipping, and returns.)"}]

def get_embedding(text):
  embedding = MODEL.encode(text).tolist()
  return embedding



def get_llm_answer(prompt):
  #messages = [{"role": "system", "content": "You are a helpful online bookstore assistant (you can provide book recommendations, add selected items to a user's shopping cart, and answer general inquiries about store policies, shipping, and returns.)"}]
  messages.append({"role": "user", "content": prompt})
  print(messages)
  # Send the payload to the LLM to retrieve an answer
  url = 'https://api.openai.com/v1/chat/completions'
  headers = {
      'content-type': 'application/json; charset=utf-8',
      'Authorization': f"Bearer {OPENAI_API_KEY}"            
  }
  data = {
      'model': CHATGPT_MODEL,
      'messages': messages,
      'temperature': 1, 
      'max_tokens': 1000
  }
  response = requests.post(url, headers=headers, data=json.dumps(data))
  
  # return the final answer
  try:
      response = requests.post(url, headers=headers, data=json.dumps(data))
      response.raise_for_status()  # Raise exception for 4xx or 5xx status codes
      response_json = response.json()
      completion = response_json["choices"][0]["message"]["content"]
      completion = completion.replace("\n", "")  # Replace newlines with empty string
      messages.append({"role": "system", "content": completion})
      return completion
  except requests.exceptions.RequestException as e:
      print("Error:", e)
      return None 

def construct_llm_payload(question, context_chunks, chat_history):
  
  # Build the prompt with the context chunks and user's query
  prompt = build_prompt(question, context_chunks)
  print("\n==== PROMPT ====\n")
  print(prompt)

  # Construct messages array to send to OpenAI
  messages = construct_messages_list(chat_history, prompt)

  # Construct headers including the API key
  headers = {
      'content-type': 'application/json; charset=utf-8',
      'Authorization': f"Bearer {OPENAI_API_KEY}"            
  }  

  # Construct data payload
  data = {
      'model': CHATGPT_MODEL,
      'messages': messages,
      'temperature': 1, 
      'max_tokens': 1000,
      'stream': True
  }

  return headers, data

