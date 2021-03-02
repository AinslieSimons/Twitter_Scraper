import requests
import os
import json
import pandas as pd
from io import StringIO
from pandas.io.json import json_normalize
from datetime import datetime

import time
from timeloop import Timeloop
from datetime import timedelta

incident_name = 'tacoma'
loop_time = 15

def current_time():
    now = datetime.now()
    time = now.strftime("%d/%m/%Y %H:%M:%S")
    return time

def auth():
    bearer_token = //api_token_here
    return bearer_token


def create_url(tweet_id):
    query = "ids="+tweet_id
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    tweet_fields = "tweet.fields=author_id,conversation_id,public_metrics,created_at&user.fields=created_at&expansions=referenced_tweets.id,attachments.media_keys&media.fields=public_metrics"
    url = "https://api.twitter.com/2/tweets?{}&{}".format(
        query, tweet_fields
    )
    print (url)
    return url

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def open_text(file_to_read):

    text_test = open(file_to_read)
    text_test = text_test.read().split('\n')
    return (text_test)

# def create_dataframe():
#     df = pd.DataFrame()
#     return df

# test_data_frame = create_dataframe()

# test_data_frame

# Get and Dump Individual Tweet Data

def main(tweet_id):
    bearer_token = auth()
    url = create_url(tweet_id)
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    tweet_dump = json.dumps(json_response, indent=4, sort_keys=True)
    #print(tweet_dump)
    return tweet_dump

# Iterate Over Tweets

def iterate_tweets(save_name):
    test_data_frame = pd.DataFrame()
#   create temp dataframe for this scrape cycle
    
    tweet_list = open_text(incident_name + '.txt')
    print ("scraping " + str(len(tweet_list)) + ' tweets')
    #open the tweet list
    
    for tweet in tweet_list:
        dump = main(tweet)
        tweet_test = json.loads(dump)
            
        if "errors" in tweet_test:
            print ('Error: ' + str(tweet_test['errors'][0]['detail']))
        else:   
            json_response = json.loads(dump)["data"]
            json_normalized = pd.json_normalize(json_response)
            json_normalized['date_time'] = current_time()
            test_data_frame = test_data_frame.append(json_normalized)
            print (str(tweet) + ' added to dataframe at ' + current_time())
    
    print(test_data_frame[['created_at', 'id', 'public_metrics.like_count', 'public_metrics.reply_count', 'public_metrics.retweet_count']])     
    test_data_frame.to_csv(save_name + '.csv', mode='a', header=False,index=False)
    print(str(save_name) + '.csv saved')

# Timeloop Script

tl = Timeloop()

print('initial data scrape...')
iterate_tweets(incident_name)
print('commencing time loop')

minutes_loop_time = loop_time
loop_seconds = minutes_loop_time*60

@tl.job(interval=timedelta(seconds=loop_seconds))
def test_job():   
    print (incident_name + " tweets Scraping Started At: " + current_time() + " loop set every " + str(minutes_loop_time) + " minutes")
    iterate_tweets(incident_name)
    print (incident_name + " scraping Concluded At: " + current_time())
        
tl.start(block=True)
