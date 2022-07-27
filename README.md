Analyzing Tweets about Ukraine using MRJOB and GCP
to Flag Potential Russian Bot Accounts

Data from https://www.kaggle.com/datasets/bwandowando/ukraine-russian-crisis-twitter-dataset-1-2-m-rows?resource=download
Main dataset for Google Cloud Platform's Dataproc API is 30M + tweets (~9 GB)

APIs to Install:
pip install nltk — used for stopwords in analyzing tweet language
pip install urllib — read file from GCS
pip install codecs - decode file form url
pip install contextlib - get url in less time-intensive way
pip install requests - request the data at a URL location

Files Used:
lines_removed.py — preprocessing file used to clean "0502_UkraineCombinedDeduped.csv"
    - outputs the csv used for the full day's tweets: "output.csv"
sample_generator.py - preprocessing a 1000-tweet randomly generated sample csv for file_reader.py for quick testing
analyze_tweets.py - runner file to carry out the MRJob
file_reader.py - called to do inner comparison of one tweet to every other tweet in a 1000-tweet sample
clean_tweet.py - used in file_reader.py to remove hashtags, @'s, and turn each tweet into set of relevant words

Files Tested in Running:
0502_UkraineCombinedDeduped.csv - 500,000 tweets from one day, found on Kaggle
output.csv - cleaned version of above csv
reduced_data.csv - 250 tweet small dataset used to test MRJob
sample_1000.csv - 1000 tweet dataseet
sample_1500.csv - 1500 tweet dataset
sample_2000.csv - 2000 tweet dataset
comparison_sample.csv - 1000 tweet dataset for comparison in file_reader.py
