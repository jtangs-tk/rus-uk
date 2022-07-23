#!/usr/bin/env python3
import re
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords
import pandas as pd
import string

stopwords_en = stopwords.words("english")

def clean_tweet(tweet_text):

    #Remove references to other users. 
    new_text = re.sub(r'@\S+', "", tweet_text) 
    #Remove hashtag symbol, but keep hashtag as text.
    new_text = re.sub(r'#',"", new_text)
    #Remove links.
    new_text = re.sub(r'http[s]?://\S+', "", new_text)

    lst_text = []
    
    new_text = new_text.replace(".", " ")
    new_text = re.sub(r'[^\w\s]', "", new_text)

    lst_text = new_text.split()
    #Remove stopwords from tweet; harmed effectiveness by not being able to translate.
    lst_text = [word.lower() for word in lst_text if word not in stopwords_en]
    
    #Cast list as a set to get unique non-stopwords in the tweet.
    set_text = set(lst_text)
    return set_text

'''
Code used for Google Translate 
- Had to discard because only allows for free translating of 100 strings per hour.

import googletrans
from googletrans import Translator

translator = Translator()
languages = googletrans.LANGUAGES

Within the clean_tweet function:
    lang = translator.detect(new_text).lang
    
    if lang != "en":
        if lang in languages:
            new_text = translator.translate(new_text, src=lang, dest="en").text
            print("Translated tweet from {}".format(lang))
        else:
            print("Could not translate")
            return None
'''
