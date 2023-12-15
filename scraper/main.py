from yandex import search_playlists
from tunebat import search_tracks


def scrap_playlist_data(keyword):
    tracks = search_playlists(keyword)
    results = []
    for track in tracks:
        data = search_tracks(f"{track['title']} - {track['artists']}", 1)
        print(data)
        results.append(data)

    return results
