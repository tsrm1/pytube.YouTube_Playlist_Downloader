from pytube import YouTube
from pytube import Playlist
from pytube.cli import on_progress
import os

playlist_file = 'youtube_downloader_playlist.txt'
report_file = 'youtube_downloader_report.txt'


def get_playlist(playlist_file):
    all_path = []
    all_folder = []

    with open(playlist_file, 'r') as f:
        playlists_url = f.readlines()
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

def normalize_filename(f_name):
    return '_'.join(i for i in f_name.split(" ") if i.isalnum())


def save_report(path, folder, video_title):
    string = path + '  ->   "' + folder + video_title + '"\n'
    with open(file=report_file, mode='a', encoding='utf-8') as file:
        file.write(string)


def get_video(path, folder):
    status = False  
    video = YouTube(path)
    video.register_on_progress_callback(on_progress)
    d_stream = video.streams.get_highest_resolution()
    d_stream.download(output_path=f'{folder}')
    v_title = d_stream.default_filename
    status = v_title
    return status


def main():
    all_path, all_folder = get_playlist(playlist_file)
    saved_path, _ = get_playlist(report_file)
    print('__________________________________________')

    flag = 0
    list_begin = 0

    if len(saved_path) > 0:
        for i in range(len(saved_path)):
            if all_path[i] == saved_path[i]:
                flag += 1

    if (flag == len(saved_path)) and (flag > 0):
        print('Файл отчёта частично дублируется!',flag, 'файлов из', len(all_path),'уже загружено.')
        list_begin = flag
    else:
        print('Список загруженных файлов отличаеться от списка необходимых файлов.')
        with open(report_file, 'w') as file:
            file.write('')
            print("Создан новый файл отчёта!")
 
    for i in range(list_begin, len(all_path)):
        file_name = get_video(all_path[i], all_folder[i])
        if file_name:
            print(f'[{i+1}] File: "{file_name}" - OK. ({ round((i+1)*100/len(all_path), 1)}%)') 
            save_report(all_path[i], all_folder[i], file_name)
    
    saved_path, _ = get_playlist(report_file)
    if len(all_path) == len(saved_path):
        print('__________________________________________')
        print("Все видео из плейлиста загруженны! Всё ОК.")
        print('__________________________________________')


if __name__ == "__main__":
    main()
