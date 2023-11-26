import pandas as pd


with open('songs.json', encoding='utf-8') as f:
    df = pd.read_json(f)

df.to_csv('songs.csv', encoding='utf-8', index=False)

