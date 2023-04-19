from pytube import YouTube
from pytube import Playlist
from pytube.cli import on_progress
import os

playlist_file = 'youtube_downloader_playlist.txt'
report_file = 'youtube_downloader_report.txt'


def get_playlist(playlist_file):
    with open(playlist_file, 'r') as f:
        playlists_url = f.readlines()
        all_path = []
        all_folder = []
        for playlist in playlists_url:
            if 'playlist?' in playlist:
                temp_pl = Playlist(playlist.split(' ')[0])
                all_path += temp_pl
                for i in range(len(temp_pl)):
                    all_folder.append('Youtube_video/' + temp_pl.title +'/')
            if 'watch?' in playlist:
                all_path.append(playlist.split(' ')[0])
                all_folder.append('Youtube_video/')
    return all_path, all_folder
 
def get_videos(all_path, all_folder):
    all_file_names = []
    count = 0
    for i in range(len(all_path)):
        video = YouTube(all_path[i])
        video.register_on_progress_callback(on_progress)

        d_stream = video.streams.get_highest_resolution()
        d_stream.download(output_path=f'{all_folder[count]}')

        v_title = d_stream.default_filename

        file = f'{all_folder[count]}/{v_title}'
        os.rename(file, f'{all_folder[count]}/{video.title}.mp4')
        print(f'[{count+1}] Download video: "{video.title}.mp4"')
        all_file_names.append(f'{video.title}.mp4')
        count += 1
    return all_path, all_folder, all_file_names


def save_playlist(all_path, all_folder, all_file_names):
    with open(report_file, 'w') as f:
        for i in range(len(all_path)):
            f.write(all_path[i] + '  ->   "' + all_folder[i] + all_file_names[i] + '"\n')


download_list = get_playlist(playlist_file)
report_list = get_videos(*download_list)
save_playlist(*report_list)
print("Все видео из плейлиста загруженны! Всё ОК.")