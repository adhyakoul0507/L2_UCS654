#!/usr/bin/env python3
"""
Mashup Program - Web Service Version
Web interface for creating YouTube mashups and sending via email.

Usage: python app.py
Then visit http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_mail import Mail, Message
import os
import sys
import shutil
from threading import Thread
from yt_dlp import YoutubeDL
from pydub import AudioSegment
import re


app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = ''  # Update this
app.config['MAIL_PASSWORD'] = ''      # Update this
app.config['MAIL_DEFAULT_SENDER'] = ''  # Update this

mail = Mail(app)


def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def download_videos(singer_name, num_videos, task_id):
    """Download videos from YouTube."""
    download_dir = f"temp_{task_id}"
    if os.path.exists(download_dir):
        shutil.rmtree(download_dir)
    os.makedirs(download_dir)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(download_dir, '%(autonumber)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'default_search': 'ytsearch',
        'ignoreerrors': True,
        'playlistend': num_videos,
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            # Search for videos and download
            search_query = f"ytsearch{num_videos}:{singer_name}"
            ydl.download([search_query])
    except Exception as e:
      
        if "Maximum number of downloads reached" not in str(e):
            print(f"Download error: {e}")
            # anyhow(personal notes)
    
    audio_files = [os.path.join(download_dir, f) for f in os.listdir(download_dir)
                  if f.endswith('.mp3')]
    audio_files.sort()
    
    return audio_files, download_dir


def cut_audio(audio_files, duration):
    """Cut first Y seconds from all audio files."""
    cut_files = []
    
    for audio_file in audio_files:
        try:
            audio = AudioSegment.from_mp3(audio_file)
            cut_duration_ms = duration * 1000
            
            if len(audio) < cut_duration_ms:
                cut_audio = audio
            else:
                cut_audio = audio[:cut_duration_ms]
            
            cut_file = audio_file.replace('.mp3', '_cut.mp3')
            cut_audio.export(cut_file, format='mp3')
            cut_files.append(cut_file)
        except Exception as e:
            print(f"Error processing {audio_file}: {e}")
            continue
    
    return cut_files


def merge_audio(cut_files, output_file):
    """Merge all audio files into a single output file."""
    merged_audio = AudioSegment.empty()
    
    for cut_file in cut_files:
        audio = AudioSegment.from_mp3(cut_file)
        merged_audio += audio
    
    merged_audio.export(output_file, format='mp3')


def create_mashup(singer_name, num_videos, duration, output_file, task_id):
    """Create the mashup - main processing function."""
    download_dir = f"temp_{task_id}"
    try:
        # Download videos
        audio_files, download_dir = download_videos(singer_name, num_videos, task_id)
        
        if len(audio_files) == 0:
            raise Exception("No videos were downloaded successfully")
        
        # Cut audio
        cut_files = cut_audio(audio_files, duration)
        
        if len(cut_files) == 0:
            raise Exception("No audio files were processed successfully")
        
        # Merge audio
        merge_audio(cut_files, output_file)
        
        # Cleanup
        if os.path.exists(download_dir):
            shutil.rmtree(download_dir)
        
        return True
    except Exception as e:
        print(f"Error in create_mashup: {e}")
        
        if os.path.exists(download_dir):
            shutil.rmtree(download_dir)
        raise


def send_email_with_attachment(recipient_email, singer_name, output_file):
    """Send email with the mashup file attached."""
    try:
        with app.app_context():
            msg = Message(
                subject=f"Your {singer_name} Mashup is Ready!",
                recipients=[recipient_email]
            )
            
            msg.body = f"""
Hello!

Your mashup for "{singer_name}" has been created successfully!

Please find the mashup file attached to this email.

Enjoy your music!

Best regards,
Mashup Service
            """
            
            # Read file directly instead of using app.open_resource
            with open(output_file, 'rb') as fp:
                msg.attach(
                    filename=os.path.basename(output_file),
                    content_type="audio/mpeg",
                    data=fp.read()
                )
            
            mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def process_mashup_task(singer_name, num_videos, duration, email, task_id):
    """Background task to process mashup and send email."""
    output_file = f"mashups/mashup_{task_id}.mp3"
    
    os.makedirs("mashups", exist_ok=True)
    
    try:
     
        create_mashup(singer_name, num_videos, duration, output_file, task_id)
        
        # Send email
        send_email_with_attachment(email, singer_name, output_file)
        
       #yeh final cleanup
        if os.path.exists(output_file):
            os.remove(output_file)
            
        print(f"Task {task_id} completed successfully")
    except Exception as e:
        print(f"Task {task_id} failed: {e}")


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/create-mashup', methods=['POST'])
def create_mashup_endpoint():
    """API endpoint to create mashup."""
    try:
        
        singer_name = request.form.get('singer_name', '').strip()
        num_videos = request.form.get('num_videos', '').strip()
        duration = request.form.get('duration', '').strip()
        email = request.form.get('email', '').strip()
    
        if not singer_name:
            return jsonify({'success': False, 'error': 'Singer name is required'})
        
        if not email:
            return jsonify({'success': False, 'error': 'Email is required'})
        
        if not validate_email(email):
            return jsonify({'success': False, 'error': 'Invalid email format'})
        
        try:
            num_videos = int(num_videos)
            if num_videos <= 10:
                return jsonify({'success': False, 'error': 'Number of videos must be greater than 10'})
        except ValueError:
            return jsonify({'success': False, 'error': 'Number of videos must be a valid integer'})
        
        try:
            duration = int(duration)
            if duration <= 20:
                return jsonify({'success': False, 'error': 'Duration must be greater than 20 seconds'})
        except ValueError:
            return jsonify({'success': False, 'error': 'Duration must be a valid integer'})
        
        
        import time
        task_id = str(int(time.time() * 1000))
        
        
        thread = Thread(
            target=process_mashup_task,
            args=(singer_name, num_videos, duration, email, task_id)
        )
        thread.start()
        
        return jsonify({
            'success': True,
            'message': f'Your mashup is being created! You will receive an email at {email} when it\'s ready.',
            'task_id': task_id
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    print("\n" + "="*60)
    print(" "*15 + "YOUTUBE MASHUP WEB SERVICE")
    print("="*60)
    print("\nStarting server...")
    print("Visit http://localhost:5000 to use the application")
    print("\nNote: Make sure to update email configuration in app.py")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
