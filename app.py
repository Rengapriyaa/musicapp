from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///songs.db'
db = SQLAlchemy(app)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    album = db.Column(db.String(100))
    genre = db.Column(db.String(50))

@app.route('/')
def index():
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
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_song(id):
    song = Song.query.get(id)
    db.session.delete(song)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update_song(id):
    song = Song.query.get(id)
    song.title = request.form['title']
    song.artist = request.form['artist']
    song.album = request.form['album']
    song.genre = request.form['genre']
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This will create the table(s) if not exist
    app.run(host='0.0.0.0', port=5000, debug=True)

