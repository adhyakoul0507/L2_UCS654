# YouTube Mashup Generator

This project is developed as part of the UCS654 Lab Assignment.

It consists of:

- Program 1 – Command Line Mashup Generator
- Program 2 – Web-Based Mashup Service (Deployed on Render)

---

# 📁 Project Structure
L2_UCS654/
│
├── 102317026.py # Program 1 (Command Line)
├── app.py # Program 2 (Web App)
├── templates/
│ └── index.html # Web UI
├── requirements.txt
├── render.yaml
├── .python-version
└── README.md
---

# Program 1 – Command Line Mashup

## Description

This program:

1. Downloads N videos of a singer from YouTube  
2. Converts them to audio  
3. Cuts first Y seconds from each  
4. Merges all audio clips into one mashup file  

Uses Python packages from PyPI:
- yt-dlp
- pydub

---

## How to Run

python 102317026.py "Singer Name" NumberOfVideos Duration OutputFileName.mp3

### Example:

python 102317026.py "Sharry Maan" 20 30 output.mp3


---

## 🔹 Conditions Checked

- Number of parameters
- Number of videos must be > 10
- Duration must be > 20 seconds
- Handles invalid input and exceptions

---

# Program 2 – Web Application

## Description

The web app allows user to:

- Enter Singer Name
- Enter Number of Videos (>10)
- Enter Duration (>20 seconds)
- Enter Email ID

The system:

- Generates mashup
- Compresses output file
- Sends result via email (ZIP format)

---

##  Live Deployment

Web App Link:
https://l2-ucs654.onrender.com

---

# Technologies Used

- Python 3.11
- Flask
- yt-dlp
- pydub
- gunicorn
- Render (Deployment)





