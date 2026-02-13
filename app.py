import importlib.util
from flask import Flask, request, render_template
import os
import smtplib
from email.message import EmailMessage
import zipfile

path = os.path.join(os.path.dirname(__file__), "102317026.py")

spec = importlib.util.spec_from_file_location("mod", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

download = mod.download
cut = mod.cut
merge = mod.merge
clean = mod.clean

app = Flask(__name__)
def send_mail(email_id, file_name):

    sender = os.getenv("EMAIL")      # set in Render
    password = os.getenv("PASSWORD")  # set in Render

    msg = EmailMessage()
    msg["Subject"] = "Your Mashup is Ready"
    msg["From"] = sender
    msg["To"] = email_id
    msg.set_content("Mashup file is attached in ZIP format.")

    with open(file_name, "rb") as f:
        data = f.read()
        name = os.path.basename(file_name)

    msg.add_attachment(
        data,
        maintype="application",
        subtype="zip",
        filename=name
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)


# -------- Routes --------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        singer = request.form["singer"]
        videos = int(request.form["videos"])
        duration = int(request.form["duration"])
        email_id = request.form["email"]

        try:
            output = "web_output.mp3"

            # Step 1: Generate mashup
            files = download(singer, videos)
            parts = cut(files, duration)
            merge(parts, output)

            # Step 2: Create ZIP file
            zip_name = "mashup.zip"
            with zipfile.ZipFile(zip_name, "w") as zipf:
                zipf.write(output)

            # Step 3: Send ZIP
            send_mail(email_id, zip_name)

            # Step 4: Cleanup
            clean()

            if os.path.exists(output):
                os.remove(output)

            if os.path.exists(zip_name):
                os.remove(zip_name)

            return "<h3>Mashup created and sent to email in ZIP format!</h3>"

        except Exception as e:
            return f"<h3>Error: {str(e)}</h3>"

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

