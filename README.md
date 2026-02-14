# YouTube Mashup Creator

A Python application that creates mashups from YouTube videos. Available as both a command-line tool and a web service.

## Features

### Program 1: Command Line Interface
- Download N videos from YouTube for any singer
- Convert videos to audio (MP3)
- Cut first Y seconds from each audio
- Merge all clips into a single mashup file
- Comprehensive error handling and validation

### Program 2: Web Service
- User-friendly web interface
- Email delivery of mashup files
- Background processing
- Real-time validation
- Beautiful, responsive design

## Installation

### Prerequisites
- Python 3.8 or higher
- FFmpeg (required for audio processing)

### Install FFmpeg

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**On macOS:**
```bash
brew install ffmpeg
```

**On Windows:**
Download from [FFmpeg official website](https://ffmpeg.org/download.html) and add to PATH.

### Install Python Dependencies

```bash
pip install -r requirements.txt --break-system-packages
```

Or install individually:
```bash
pip install yt-dlp pydub flask flask-mail --break-system-packages
```

## usage

### Program 1: Command Line

**Basic Usage:**
```bash
python 102317026.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>
```

**Example:**
```bash
python 102317026.py "Sharry Maan" 20 20 101556-output.mp3
```

**Parameters:**
- `SingerName`: Name of the singer/artist (use quotes for multi-word names)
- `NumberOfVideos`: Number of videos to download (must be > 10)
- `AudioDuration`: Duration in seconds to cut from each video (must be > 20)
- `OutputFileName`: Name of the output mashup file

**Examples:**
```bash
# Create a 20-video mashup with 30-second clips
python 102317026.py "Arijit Singh" 20 30 arijit-mashup.mp3

```

### Program 2: Web Service

**Start the Server:**
```bash
python app.py
```

**Access the Web Interface:**
Open your browser and navigate to:
```
http://localhost:5000
```

**Configure Email Settings:**

Before running the web service, update the email configuration in `app.py`:

```python
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'your-app-password'      # Your app password
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'
```

**For Gmail:**
1. Enable 2-factor authentication
2. Generate an App Password (Google Account Settings → Security → App Passwords)
3. Use the app password in the configuration

##  File Structure

```
.
├── 102317026.py              # Commandline program
├── app.py                 # Web service 
├── templates/
│   └── index.html        # Web int template
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## How It Works

### Command Line Program Flow:
1. **Validation**: Checks all input parameters
2. **Download**: Searches YouTube and downloads N videos
3. **Convert**: Extracts audio and converts to MP3
4. **Cut**: Trims each audio to Y seconds
5. **Merge**: Combines all clips into one file
6. **Cleanup**: Removes temporary files

### Web Service Flow:
1. **User Input**: Web form with validation
2. **Background Processing**: Runs mashup creation in separate thread
3. **Email**: Sends completed mashup to user's email
4. **Auto-cleanup**: Removes files after sending

## Error Handling

Both programs include comprehensive error handling for:
- Invalid parameters (wrong types, out of range values)
- Network errors during download
- Audio processing errors
- File system errors
- Email sending failures (web service)

