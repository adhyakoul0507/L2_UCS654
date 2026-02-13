import sys
import os
import shutil
from yt_dlp import YoutubeDL
from pydub import AudioSegment


def check_inputs(args):
    if len(args) != 5:
        print("Usage: python <file.py> <SingerName> <NumberOfVideos> <Duration> <OutputFile>")
        sys.exit(1)

    singer = args[1]

    # number of videos
    try:
        num_videos = int(args[2])
    except:
        print("no of videos need to be integer value")
        sys.exit(1)

    if num_videos <= 10:
        print("Number of videos > 10 is imp")
        sys.exit(1)

    # duration
    try:
        duration = int(args[3])
    except:
        print("Duration must be an integer")
        sys.exit(1)

    if duration <= 20:
        print("the duration should must be higher than 20 sec")
        sys.exit(1)

    output_file = args[4]
    if not output_file.endswith(".mp3"):
        output_file += ".mp3"

    return singer, num_videos, duration, output_file


def download(singer, num_videos):
    print("\nenjoy while i search and download music")

    folder = "temp_files"

    if os.path.exists(folder):
        shutil.rmtree(folder)

    os.makedirs(folder)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3'
        }],
        'outtmpl': os.path.join(folder, '%(autonumber)s.%(ext)s'),
        'default_search': 'ytsearch',
        'ignoreerrors': True
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            query = f"ytsearch{num_videos}:{singer}"
            ydl.download([query])
    except Exception as e:
        print("error while i was unfortunately downloading:", e)
        sys.exit(1)

    files = []
    for file in os.listdir(folder):
        if file.endswith(".mp3"):
            files.append(os.path.join(folder, file))

    if len(files) == 0:
        print("No files downloaded")
        sys.exit(1)

    print(f"{len(files)} files have been now downloaded yayyy")
    return files


def cut(files, duration):
    print("\nCutting audio filess.")

    cut_files = []

    for file in files:
        try:
            audio = AudioSegment.from_mp3(file)
            part = audio[:duration * 1000]

            new_file = file.replace(".mp3", "_cut.mp3")
            part.export(new_file, format="mp3")
            cut_files.append(new_file)

        except Exception as e:
            print("Error processing file:", e)

    if len(cut_files) == 0:
        print("No files processed properly.")
        sys.exit(1)

    return cut_files


def merge(files, output):
    print("\nMerging files...")

    final_audio = AudioSegment.empty()

    for file in files:
        audio = AudioSegment.from_mp3(file)
        final_audio += audio

    try:
        final_audio.export(output, format="mp3")
        print("\nMashup created successfully.")
        print("Output file:", output)
    except Exception as e:
        print("Error while exporting:", e)
        sys.exit(1)


def clean():
    folder = "temp_files"
    if os.path.exists(folder):
        shutil.rmtree(folder)


def main():
    singer, num_videos, duration, output = check_inputs(sys.argv)

    try:
        files = download(singer, num_videos)
        cut_files = cut(files, duration)
        merge(cut_files, output)
        clean()

    except KeyboardInterrupt:
        print("\nProcess stopped.")
        clean()
        sys.exit(1)

    except Exception as e:
        print("Unexpected error:", e)
        clean()
        sys.exit(1)


if __name__ == "__main__":
    main()

