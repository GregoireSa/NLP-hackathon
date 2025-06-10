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


def get_articles(query, result_size=100):
    # Edit the below to get different data
    payload = {
        "query_text": query,
        "result_size": result_size,
        'timerange': '180d'
        }

    response = requests.post(API_URL, headers=headers,
                             data=json.dumps(payload))
    json_response = response.json()

    return json_response


def get_sentiment(summaries):

    sia = SentimentIntensityAnalyzer()

    most_pos = ''
    most_neg = ''
    pos_score = -1
    neg_score = 1


    if not summaries:
        return 0.0
    
    score_sum = 0.0
    score_count = 0
    for summary in summaries:
        if summary:
            score_count += 1
            score = sia.polarity_scores(summary)['compound']
            score_sum += score

            if score > pos_score:
                most_pos = summary
                pos_score = score
                
            if score < neg_score:
                most_neg = summary
                neg_score = score
    
    response = {
        "score": round(score_sum / score_count, 3),
        "pos": most_pos,
        "neg": most_neg
    }

    return response


countries = ["France", "UK", "USA", "India", "China", "South Africa",
             "Germany", "Mexico", "Japan", "Australia", "Brazil"]
query = "vaccines"

for country in countries:

    articles = get_articles(f"{country} {query}")
    if 'message' not in articles:
        summaries = []

        for article in articles['results']:
            summaries.append(article['summary'])
        
        sentiment_response = get_sentiment(summaries)
        sentiment_score = sentiment_response["score"]

        if sentiment_score >= .1:
            sentiment = 'positive'
        elif sentiment_score <= -.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        print("-"*25 + '\n')
        print(f'{country.upper()}: {sentiment} sentiment ({sentiment_score})\n')
        print(f"most positive article: {sentiment_response["pos"]}")
        print(f"most negative article: {sentiment_response["neg"]}\n")
        
        print(f"[{len(summaries)} summaries found]\n")

    else:
        print(articles)
