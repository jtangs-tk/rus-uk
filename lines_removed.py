import re
import io
import pandas as pd
import numpy as np

def change_csv(csv = "0502_UkraineCombinedTweetsDeduped.csv"):
    df = pd.read_csv(csv)
    
    for col in df.columns:
        if df[col].dtype == np.object_:
            df[col] = df[col].str.replace('\n', " ")
            df[col] = df[col].str.replace(',', '')

    df.to_csv('./output.csv', index = False)