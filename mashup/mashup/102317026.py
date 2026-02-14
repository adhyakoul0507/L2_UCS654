#!/usr/bin/env python3
"""
Mashup Program - Command Line Version
Downloads YouTube videos, converts to audio, cuts and merges them.

Usage: python 101556.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>
Example: python 101556.py "Sharry Maan" 20 20 101556-output.mp3
"""

import sys
import os
import re
from yt_dlp import YoutubeDL
from pydub import AudioSegment
import shutil


def validate_arguments(args):
    """Validate command line arguments."""
    if len(args) != 5:
        print("Error: Incorrect number of parameters!")
        print("\nUsage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        print('Example: python 101556.py "Sharry Maan" 20 20 101556-output.mp3')
        sys.exit(1)
    
    singer_name = args[1]
    
    # Validate number of videos
    try:
        num_videos = int(args[2])
        if num_videos <= 10:
            print("Error: Number of videos must be greater than 10!")
            sys.exit(1)
    except ValueError:
        print("Error: Number of videos must be a valid integer!")
        sys.exit(1)
    
    # Validate audio duration
    try:
        duration = int(args[3])
        if duration <= 20:
            print("Error: Audio duration must be greater than 20 seconds!")
            sys.exit(1)
    except ValueError:
        print("Error: Audio duration must be a valid integer!")
        sys.exit(1)
    
    output_file = args[4]
    if not output_file.endswith('.mp3'):
        print("Warning: Output file should have .mp3 extension. Adding .mp3")
        output_file += '.mp3'
    
    return singer_name, num_videos, duration, output_file


def download_videos(singer_name, num_videos):
    """Download videos from YouTube for the given singer."""
    print(f"\n{'='*60}")
    print(f"Searching for '{singer_name}' videos on YouTube...")
    print(f"{'='*60}\n")
    
    # Create a temporary directory for downloads
    download_dir = "temp_downloads"
    if os.path.exists(download_dir):
        shutil.rmtree(download_dir)
    os.makedirs(download_dir)
    
    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(download_dir, '%(autonumber)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
        'default_search': 'ytsearch',
        'playlistend': num_videos,
        'ignoreerrors': True,
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            # Search for videos and download
            search_query = f"ytsearch{num_videos}:{singer_name}"
            print(f"Downloading {num_videos} videos...")
            ydl.download([search_query])
    except Exception as e:
        # Check if it's just the "max downloads reached" message
        # This happens after successful downloads, so we continue
        if "Maximum number of downloads reached" not in str(e):
            print(f"\nError during download: {str(e)}")
            sys.exit(1)
    
    # Get list of downloaded files
    audio_files = [os.path.join(download_dir, f) for f in os.listdir(download_dir)
                  if f.endswith('.mp3')]
    audio_files.sort()
    
    if len(audio_files) < num_videos:
        print(f"\nWarning: Only {len(audio_files)} videos were successfully downloaded.")
    
    if len(audio_files) == 0:
        print("Error: No videos were downloaded successfully!")
        sys.exit(1)
    
    print(f"\n✓ Successfully downloaded {len(audio_files)} audio files!")
    return audio_files


def cut_audio(audio_files, duration):
    """Cut first Y seconds from all audio files."""
    print(f"\n{'='*60}")
    print(f"Cutting first {duration} seconds from each audio file...")
    print(f"{'='*60}\n")
    
    cut_files = []
    
    for i, audio_file in enumerate(audio_files, 1):
        try:
            print(f"Processing file {i}/{len(audio_files)}: {os.path.basename(audio_file)}")
            
            # Load audio file
            audio = AudioSegment.from_mp3(audio_file)
            
            # Cut first Y seconds (duration is in seconds, pydub uses milliseconds)
            cut_duration_ms = duration * 1000
            
            if len(audio) < cut_duration_ms:
                print(f"  Warning: Audio is only {len(audio)//1000}s long. Using full audio.")
                cut_audio = audio
            else:
                cut_audio = audio[:cut_duration_ms]
            
            # Save cut audio
            cut_file = audio_file.replace('.mp3', '_cut.mp3')
            cut_audio.export(cut_file, format='mp3')
            cut_files.append(cut_file)
            
        except Exception as e:
            print(f"  Error processing {audio_file}: {str(e)}")
            continue
    
    if len(cut_files) == 0:
        print("\nError: No audio files were successfully processed!")
        sys.exit(1)
    
    print(f"\n✓ Successfully cut {len(cut_files)} audio files!")
    return cut_files


def merge_audio(cut_files, output_file):
    """Merge all audio files into a single output file."""
    print(f"\n{'='*60}")
    print(f"Merging all audio files into '{output_file}'...")
    print(f"{'='*60}\n")
    
    try:
        # Start with an empty audio segment
        merged_audio = AudioSegment.empty()
        
        # Merge all cut audio files
        for i, cut_file in enumerate(cut_files, 1):
            print(f"Adding file {i}/{len(cut_files)} to mashup...")
            audio = AudioSegment.from_mp3(cut_file)
            merged_audio += audio
        
        # Export the merged audio
        print(f"\nExporting final mashup...")
        merged_audio.export(output_file, format='mp3')
        
        # Get file size
        file_size = os.path.getsize(output_file) / (1024 * 1024)  # Convert to MB
        duration_seconds = len(merged_audio) / 1000
        
        print(f"\n{'='*60}")
        print(f"✓ MASHUP CREATED SUCCESSFULLY!")
        print(f"{'='*60}")
        print(f"Output file: {output_file}")
        print(f"File size: {file_size:.2f} MB")
        print(f"Duration: {duration_seconds:.0f} seconds ({duration_seconds/60:.1f} minutes)")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"\nError during merging: {str(e)}")
        sys.exit(1)


def cleanup(download_dir="temp_downloads"):
    """Clean up temporary files."""
    print("Cleaning up temporary files...")
    try:
        if os.path.exists(download_dir):
            shutil.rmtree(download_dir)
        print("✓ Cleanup completed!")
    except Exception as e:
        print(f"Warning: Could not clean up temporary files: {str(e)}")


def main():
    """Main function to orchestrate the mashup creation."""
    print("\n" + "="*60)
    print(" "*15 + "YOUTUBE MASHUP CREATOR")
    print("="*60)
    
    # Validate arguments
    singer_name, num_videos, duration, output_file = validate_arguments(sys.argv)
    
    print(f"\nConfiguration:")
    print(f"  Singer: {singer_name}")
    print(f"  Number of videos: {num_videos}")
    print(f"  Audio duration: {duration} seconds")
    print(f"  Output file: {output_file}")
    
    try:
        # Step 1: Download videos
        audio_files = download_videos(singer_name, num_videos)
        
        # Step 2: Cut audio to specified duration
        cut_files = cut_audio(audio_files, duration)
        
        # Step 3: Merge all audio files
        merge_audio(cut_files, output_file)
        
        # Step 4: Cleanup
        cleanup()
        
        print("\n🎵 All done! Enjoy your mashup! 🎵\n")
        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user. Cleaning up...")
        cleanup()
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {str(e)}")
        cleanup()
        sys.exit(1)


if __name__ == "__main__":
    main()
