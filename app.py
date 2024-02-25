from flask import Flask, render_template, request, send_from_directory, flash
import os
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip


app = Flask(__name__)

ALLOWED_EXTENSIONS = [".mp4"]

app.config["SECRET_KEY"] = os.urandom(32)


os.makedirs("videos", exist_ok=True)
os.makedirs("thumbnails", exist_ok=True)

@app.route("/")
def home():
    videos = os.listdir("videos")
    return render_template("index.html", videos=videos, splitext=os.path.splitext)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["video"]
        if os.path.splitext(file.filename)[1] not in ALLOWED_EXTENSIONS:
            flash(f"Invalid file type. Please upload a video in one of the following formats: {ALLOWED_EXTENSIONS}.")
            return render_template("upload.html")
        filename = secure_filename(f"{request.form['author']}.{request.form['title']}{os.path.splitext(file.filename)[1]}")
        file.save(os.path.join("videos", filename))
        clip = VideoFileClip(os.path.join("videos", filename))
        clip.save_frame(os.path.join("thumbnails", f"{os.path.splitext(filename)[0]}.png"), t=1)
        flash("Upload Successful")
        return render_template("upload.html")
    else:
        return render_template("upload.html")
    
@app.route("/getvideo/<video>")
def getvideo(video):
    return send_from_directory("videos", video)

@app.route("/getthumbnail/<thumbnail>")
def getthumbnail(thumbnail):
    return send_from_directory("thumbnails", thumbnail)
    
@app.route("/play/<video>")
def play(video):
    return render_template("play.html", video=video, splitext=os.path.splitext)

if __name__ == "__main__":
    app.run(debug=True)