import os
import json
from yandex_music import Client
from yandex_music.exceptions import NotFoundError

import csv
import datetime

with open('token.json', 'r') as fp:
    TOKEN = json.load(fp)["yt_token"]

client = Client(TOKEN).init()

type_to_name = {
    'track': 'трек',
    'artist': 'исполнитель',
    'album': 'альбом',
    'playlist': 'плейлист',
    'video': 'видео',
    'user': 'пользователь',
    'podcast': 'подкаст',
    'podcast_episode': 'эпизод подкаста',
}


def search_playlists(query):
    search_result = client.search(query).playlists
    results = []
    writer = csv.writer(open("yandex.csv", "a+", newline="", encoding="utf-8"))

    for result in search_result.results:
        playlist = result.fetch_tracks()

        for track_short in playlist:
            track = track_short.track
            artists = track.artists
            album = track.albums[0]
            info = {
                "id": track.id,
                "title": track.title,
                "artists": ', '.join(artist.name for artist in artists),
                "album": album.title,
                "album_id": album.id,
                "time": datetime.datetime.now(),
            }

            writer.writerow(list(info.values()))
            results.append(info)

    return results


def send_search_request_and_print_result(query):
    search_result = client.search(query)

    text = [f'Результаты по запросу "{query}":', '']

    best_result_text = ''
    if search_result.best:
        type_ = search_result.best.type
        best = search_result.best.result

        text.append(f'❗️Лучший результат: {type_to_name.get(type_)}')

        if type_ in ['track', 'podcast_episode']:
            artists = ''
            if best.artists:
                artists = ' - ' + ', '.join(artist.name for artist in best.artists)
            best_result_text = best.title + artists
        elif type_ == 'artist':
            best_result_text = best.name
        elif type_ in ['album', 'podcast']:
            best_result_text = best.title
        elif type_ == 'playlist':
            best_result_text = best.title
        elif type_ == 'video':
            best_result_text = f'{best.title} {best.text}'

        text.append(f'Содержимое лучшего результата: {best_result_text}\n')

    if search_result.artists:
        text.append(f'Исполнителей: {search_result.artists.total}')
    if search_result.albums:
        text.append(f'Альбомов: {search_result.albums.total}')
    if search_result.tracks:
        text.append(f'Треков: {search_result.tracks.total}')
    if search_result.playlists:
        text.append(f'Плейлистов: {search_result.playlists.total}')
    if search_result.videos:
        text.append(f'Видео: {search_result.videos.total}')

    text.append('')
    print('\n'.join(text))


def get_album(id):
    album = client.albums_with_tracks(id)
    tracks = []
    for i, volume in enumerate(album.volumes):
        if len(album.volumes) > 1:
            tracks.append(f'💿 Диск {i + 1}')
        tracks += volume

    text = 'АЛЬБОМ\n\n'
    text += f'{album.title}\n'
    text += f"Исполнитель: {', '.join([artist.name for artist in album.artists])}\n"
    text += f'{album.year} · {album.genre}\n'

    cover = album.cover_uri
    if cover:
        text += f'Обложка: {cover.replace("%%", "400x400")}\n\n'

    text += 'Список треков:'

    print(text)

    for track in tracks:
        if isinstance(track, str):
            print(track)
        else:
            artists = ''
            if track.artists:
                artists = ' - ' + ', '.join(artist.name for artist in track.artists)
            print(track.title + artists)

    return album, tracks


def get_lyrics(song_id: int) -> str:
    track = client.tracks(song_id)[0]
    try:
        lyrics = track.get_lyrics()
        text = lyrics.fetch_lyrics()
        return text

    except NotFoundError:
        print('Текст песни отсутствует')


if __name__ == '__main__':
    while True:
        input_query = input('Введите поисковой запрос: ')
        get_lyrics(int(input_query))
