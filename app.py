from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import logging
import requests
from datetime import datetime

# --- Logtail Logging Setup ---
class LogtailHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        logtail_url = os.getenv('LOGTAIL_TOKEN')
        if logtail_url:
            try:
                requests.post(logtail_url, json={
                    "dt": datetime.utcnow().isoformat(),
                    "message": log_entry
                })
            except Exception as e:
                print(f"Logtail error: {e}")

# --- Flask App Setup ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///songs.db'
db = SQLAlchemy(app)

# --- Attach Logtail Logger ---
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(LogtailHandler())

# --- Database Model ---
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    album = db.Column(db.String(100))
    genre = db.Column(db.String(50))

# --- Routes ---
@app.route('/')
def index():
    app.logger.info("Homepage accessed")
    songs = Song.query.all()
    return render_template('index.html', songs=songs)

@app.route('/add', methods=['POST'])
def add_song():
    song = Song(
        title=request.form['title'],
        artist=request.form['artist'],
        album=request.form['album'],
        genre=request.form['genre']
    )
    db.session.add(song)
    db.session.commit()
    app.logger.info(f"Added song: {song.title} by {song.artist}")
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_song(id):
    song = Song.query.get(id)
    db.session.delete(song)
    db.session.commit()
    app.logger.info(f"Deleted song: {song.title}")
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update_song(id):
    song = Song.query.get(id)
    song.title = request.form['title']
    song.artist = request.form['artist']
    song.album = request.form['album']
    song.genre = request.form['genre']
    db.session.commit()
    app.logger.info(f"Updated song: {song.title}")
    return redirect('/')

# --- Run App ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
     port = int(os.environ.get("PORT", 5000))
    app.run(debug=True)
