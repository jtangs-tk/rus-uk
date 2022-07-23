import pandas as pd

df = pd.read_csv("output.csv", lineterminator="\n")
df = df[df["is_retweet"] == False]

def generate_sample(size, name):
    '''
    Generates a random sample from non-retweets for comparison 
    and analysis of performance and reliability of the algo

    Inputs:
    size (int): desired size of sample
    name (string): file to use, .csv will be appended
    '''

    sample = df.sample(size)
    title = name + ".csv"
    try:
        sample.to_csv(title, index=False)
    except Exception:
        return "failed to convert to CSV"
    else:
        return "successfully generated sample"