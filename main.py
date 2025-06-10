import requests
import json
import nltk
import re
import pandas as pd
import os
from dotenv import load_dotenv
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

# API endpoint from the newly deployed service

API_URL = "https://zfgp45ih7i.execute-api.eu-west-1.amazonaws.com/sandbox/api/search"
load_dotenv()
API_KEY = os.getenv('API_KEY')

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}


query = "vaccine"

# Edit the below to get different data
payload = {
  "query_text": query,
  "result_size": 3,
  "include_highlights": True,
  "ai_answer": "basic",
}

response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
json_response = response.json()

print(json_response)