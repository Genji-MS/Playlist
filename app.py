from flask import Flask, render_template

app = Flask(__name__)

playlist = [
    {'title': 'Twitch Fails', 'description': 'Live streaming video-game funny moments'},
    {'title': 'New Retro Music', 'description': 'Technology, Metal, Chiptune fusion'}
]

#@app.route('/')
def index():
    """Return homepage"""
    return render_template('home.html', msg='flask flask baby~')

@app.route('/')
def playlist_index():
    """Show All playlists"""
    return render_template('playlist_index.html', playlist= playlist)

if app.name == '__main__':
    app.run(debug=True)