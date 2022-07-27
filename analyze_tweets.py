# Imports
import sys
from mrjob.job import MRJob
from datetime import date
from datetime import datetime
from dateutil import parser
from file_reader import file_reader

# from clean_tweet import clean_tweet
# WARNING: the above import does not recognize google translate library,
# this may need to be resolved by my version of Python

# global variable containing headers. IMPORTANT: this only applies to headers
# that align with the May 05 dataset. If the April 20 update was the most
# recent update to the tracked columns, this only works until april 20
HEADERS = ["","userid","username","acctdesc","location","following","followers",
"totaltweets","usercreatedts","tweetid","tweetcreatedts","retweetcount","text",
"hashtags","language","coordinates","favorite_count","is_retweet",
"original_tweet_id","original_tweet_userid","original_tweet_username",
"in_reply_to_status_id","in_reply_to_user_id","in_reply_to_screen_name",
"is_quote_status","quoted_status_id","quoted_status_userid",
"quoted_status_username","extractedts"]

# generation of a global dictionary that will be called to get table-like
# behavior for text rows of MRJob
COLS = {}
for i in range(0, len(HEADERS)):
    COLS[HEADERS[i]] = i

# global variables
SUS_FOLLOWER_RATIO = 20
SUS_NUM_SIMILAR = 2
SUS_NUM_FLAGS = 2

class MRTweetFlags(MRJob):

    def mapper(self, _, line):

        flag_count = 0

        # construct row from text
        current_row = line.split(',')
        current_user = current_row[COLS["userid"]]

        if len(current_row) == len(COLS):
        
            # follow ratio check
            follower_string = current_row[COLS["followers"]]
            following_string = current_row[COLS["followers"]]

            # handle the edge case of the CSV header line, which breaks typecast
            try:
                followers = int(follower_string)
                following = int(following_string)
            except ValueError:
                pass
            else:
                if followers == 0:
                    flag_count += 1
                else:
                    ratio = following / followers
                    if ratio == 1 or ratio >= SUS_FOLLOWER_RATIO:
                        flag_count += 1

            # username check
            current_username = current_row[COLS["username"]]
            try:
                int(current_username)
            except ValueError:
                pass
            else:
                flag_count += 1

            # no bio check
            current_bio = current_row[COLS["acctdesc"]]
            if current_bio == "":
                flag_count += 1

            # recent creation check
            created_date_str = current_row[COLS["usercreatedts"]]
            try:
                created_date = parser.parse(created_date_str)
            except parser._parser.ParserError:
                days_active = None
            else:
                today = datetime.now()
                days_active = (today - created_date).days
                if days_active <= 31:
                    flag_count += 1

            # irrgular freq check
            try:
                total_tweets = int(current_row[COLS["totaltweets"]])
            except ValueError:
                pass
            else:
                if days_active != None:
                    tweets_per_day = total_tweets / days_active
                    if tweets_per_day >= 75:
                        flag_count += 1

            # low originality check NESTED MRJob need to solve
            '''
            current_text = current_row[COLS["text"]]
            if file_reader(current_text) >= SUS_NUM_SIMILAR:
                flags["low originality"] = True
            '''
            yield (current_user, flag_count)
                    

    #def combiner(self, user, counts):
        #if counts
        #yield (user, max(counts))
    
    def reducer(self, user, counts):
        num = 0
        den = 0
        for count in counts:
            num += count
            den += 1
        if (num/den) >= SUS_NUM_FLAGS:
            yield (user, num/den)

if __name__ == '__main__':
    '''
    FILENAME = str(sys.argv[1])
    print(FILENAME)
    print(type(FILENAME))
    FILEPATH += FILENAME
    '''
    MRTweetFlags.run()

