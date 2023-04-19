from pytube import Playlist
from pytube.cli import on_progress
import os

url = 'https://youtube.com/playlist?list=PLKRzh9MUs_5oyHvYT5wWBZgE0qoFTWNst'

playlist = Playlist(url)
title = playlist.title

count = 0

for video in playlist.videos:
    video.register_on_progress_callback(on_progress)

    d_stream = video.streams.get_highest_resolution()
    d_stream.download(output_path=f'{title}')

    v_title = d_stream.default_filename

    file = f'{title}/{v_title}'
    os.rename(file, f'{title}/{video.title}.mp4')
    print(f'Downloaded {video.title}.mp4')

    count += 1
    