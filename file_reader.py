#!/usr/bin/env python3
'''
this function iterates over a file, treating entries as strings, and isolates
the text column, comparing it to an outer body of text. 

Inputs:
filename (string): name of the file to iterate over
outer_string: string to compare text to

Returns (int): number of text bodies that are similar over .75 ratio
'''
import pandas as pd
import urllib
import codecs
from contextlib import closing
import csv
import requests
import clean_tweet
from clean_tweet import clean_tweet

# adjustable sim threshold parameter
SIMILARITY_THRESHOLD = 0.50

HEADERS = ["","userid","username","acctdesc","location","following","followers",
"totaltweets","usercreatedts","tweetid","tweetcreatedts","retweetcount","text",
"hashtags","language","coordinates","favorite_count","is_retweet",
"original_tweet_id","original_tweet_userid","original_tweet_username",
"in_reply_to_status_id","in_reply_to_user_id","in_reply_to_screen_name",
"is_quote_status","quoted_status_id","quoted_status_userid",
"quoted_status_username","extractedts"]

COLS = {}
for i in range(0, len(HEADERS)):
    COLS[HEADERS[i]] = i

url = "https://storage.googleapis.com/jt_tweets/sample_2000.csv"

def file_reader(outer_string):

    outer_wordset = clean_tweet(outer_string)
    sim_count = 0

    with closing(requests.get(url, stream=True)) as r:
        
        reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
        
        for row in reader:

            # non-corrupted parsing check
            if len(row) == len(COLS):
                
                # a second row corruption check for castability as bool
                try:
                    is_retweet = bool(row[COLS["is_retweet"]])
                except Exception:
                    pass
                else:
                    
                    #processing
                    if not is_retweet:
                        current_text = row[COLS["text"]]
                        inner_wordset = clean_tweet(current_text)
                        sim_wordset = inner_wordset.intersection(outer_wordset)
                        total_wordset = inner_wordset.union(outer_wordset)

                        if len(sim_wordset) / len(total_wordset) >= SIMILARITY_THRESHOLD:
                            sim_count += 1
        
                        else:
                            pass
            
            else:
                pass
        
    return sim_count

    '''
    OLD - INEFFICIENT VERSION
    
    #df = pd.read_csv("https://storage.googleapis.com/jt_tweets/reduced_data.csv", lineterminator = '\n').reset_index(drop = True)
    #df = df.drop("Unnamed: 0", axis =1)

    data = urllib.request.urlopen("https://storage.googleapis.com/jt_tweets/reduced_data.csv")

    outer_wordset = set(outer_string.split(" "))
    sim_count = 0

    for line in data.readlines():

        current_row = line.split(",")

        if len(current_row) == len(COLS) and current_row[COLS["is_retweet"]] in set(["False", "false"]):

            current_text = current_row[COLS["text"]]
            inner_wordset = set(current_text.split(" "))
            sim_wordset = inner_wordset.intersection(outer_wordset)
            total_wordset = inner_wordset.union(outer_wordset)

            if len(sim_wordset) / len(total_wordset) >= SIMILARITY_THRESHOLD:
                sim_count += 1
            
            else:
                pass

    return sim_count
    '''
    '''
    for index, row in df.iterrows():

        if not row["is_retweet"]:
            current_text = row["text"]
            inner_wordset = set(current_text.split(" "))
            sim_wordset = inner_wordset.intersection(outer_wordset)
            total_wordset = inner_wordset.union(outer_wordset)

            if len(sim_wordset) / len(total_wordset) >= SIMILARITY_THRESHOLD:
                sim_count += 1
    
        else:
            pass
    
    return sim_count

    '''

    '''
    OLD - Worked locally, but in GCS.

    with open(filename) as f:
        for line in f:

            current_row = line.split(",")

            # ensure the row is parsed properly
            if len(current_row) == len(COLS):

                current_text = current_row[COLS["text"]]
                inner_wordset = set(current_text.split(" "))
                sim_wordset = inner_wordset.intersection(outer_wordset)
                total_wordset = inner_wordset.union(outer_wordset)

                if len(sim_wordset) / len(total_wordset) >= SIMILARITY_THRESHOLD and current_row[COLS["is_retweet"]] in set(["False", "false"]):
                    sim_count += 1
            
            else:
                pass
    
    return sim_count
    '''

