# app.py
import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Playlist')
client = MongoClient(host=f'{host}?retryWrites=False')
db = client.get_default_database()
playlist= db.playlist

#Local db version
#client = MongoClient()
#db = client.Playlist
#playlist = db.playlist

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
    return render_template('playlist_new.html', playlist = {}, title = 'New Playlist')

@app.route('/playlist', methods=['POST'])
def playlist_submit():
    """Submit a new playlist"""
    p_list= { 
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    #Youtube doesn't like to display in this way, replace this component of the URL to embed/ and it'll work fine.
    for index in range(len(p_list['videos'])):
        p_list['videos'][index] = p_list['videos'][index].replace("watch?v=", "embed/")

    playlist_id = playlist.insert_one(p_list).inserted_id
    #print(request.form.to_dict())
    #return redirect(url_for('playlist_index'))
    return redirect(url_for('playlist_show', playlist_id = playlist_id))

@app.route('/playlist/<playlist_id>')
def playlist_show(playlist_id):
    """Show a single playlist"""
    p_list = playlist.find_one({'_id': ObjectId(playlist_id)})
    #Double check URL's that may have been saved without /embed/ and check that they even have links.
    if p_list.get('videos'):
        for index in range(len(p_list['videos'])):
            p_list['videos'][index] = p_list['videos'][index].replace("watch?v=", "embed/")
    return render_template('playlist_show.html',playlist=p_list)

@app.route('/playlist/<playlist_id>/edit')
def playlist_edit(playlist_id):
    """Show the edit form for a playlist"""
    p_list = playlist.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlist_edit.html',playlist=p_list, title='Edit Playlist')

@app.route('/playlist/<playlist_id>', methods=['POST'])
def playlist_update(playlist_id):
    """Submit and edited playlist"""
    updated_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    #Youtube doesn't like to display with watch?, replace this component of the URL to embed/ and it'll work fine.
    for index in range(len(updated_playlist['videos'])):
        updated_playlist['videos'][index] = updated_playlist['videos'][index].replace("watch?v=", "embed/")
    playlist.update_one(
        {'_id':ObjectId(playlist_id)},
        {'$set':updated_playlist})
    return redirect(url_for('playlist_show', playlist_id = playlist_id))

@app.route('/playlist/<playlist_id>/delete', methods=["POST"])
def playlist_delete(playlist_id):
    """Delete specified playlist"""
    playlist.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('playlist_index'))

if app.name == '__main__':
    #app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))