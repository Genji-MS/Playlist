from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

client = MongoClient()
db = client.Playlist
playlist = db.playlist

app = Flask(__name__)

'''playlist = [
    {'title': 'Twitch Fails', 'description': 'Live streaming video-game funny moments'},
    {'title': 'New Retro Music', 'description': 'Technology, Metal, Chiptune fusion'}
]'''

#@app.route('/')
def index():
    """Return homepage"""
    return render_template('home.html', msg='flask flask baby~')

@app.route('/')
def playlist_index():
    """Show All playlists"""
    return render_template('playlist_index.html', playlist= playlist.find())

@app.route('/playlist/new')
def playlist_new():
    """Create New playlist"""
    return render_template('playlist_new.html')

@app.route('/playlist', methods=['POST'])
def playlist_submit():
    """Submit a new playlist"""
    p_list= { 
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    playlist.insert_one(p_list)
    #print(request.form.to_dict())
    return redirect(url_for('playlist_index'))

if app.name == '__main__':
    app.run(debug=True)