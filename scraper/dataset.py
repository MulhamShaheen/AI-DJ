import pandas as pd
from yandex import search_playlists
from tunebat import search_tracks, props_dict
import csv
import yaml


def scrap_playlist_data(keyword, count=200):
    tracks = search_playlists(keyword)
    results = []
    for i, track in enumerate(tracks):
        if i == count:
            break
        data = search_tracks(f"{track['title']} - {track['artists']}", 1)
        if i % 10 == 0:
            print(data)
        results.append(data)

    return results


def create_subset(query: list, label: str):
    cols = list(props_dict.values())
    rows = []
    f = open(f"{label}_temp.csv", "a+", newline="", encoding="utf-8")
    writer = csv.writer(f)

    for q in query:
        data = scrap_playlist_data(q)
        for track in data:
            rows.append(list(track.values()))
            writer.writerow(list(track.values()))

    df = pd.DataFrame(data=rows, columns=cols)
    df.to_csv(f"{label}.csv")

    return df

def csv_to_yaml(csv_file: str, yaml_path:str = "data.yaml"):
    f = open(csv_file, "r", encoding="utf8")
    reader = csv.reader(f)
    to_yaml = []
    for i, raw in enumerate(reader):
        to_yaml.append({})
        for j, prop in enumerate(raw):
            if j == 14:
                to_yaml[i]["label"] = prop
                break
            to_yaml[i][list(props_dict.values())[j]] = prop

    with open(yaml_path, 'w') as f:
        yaml.dump(to_yaml, f)

    f.close()


csv_to_yaml("songs_database.csv")

# create_subset(["Workout energetic music", "Music for sport"], "sport")