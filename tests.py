# tests.py

from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app #throws error when reading pymongo unless pymongo is installed in the (env)

sample_playlist_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_playlist = {
    'title': 'Cat Videos',
    'description': 'Cats acting Wierd',
    'videos': [
        'https://youtube.com/embed/hY7m5jjJ9mM',
        'https://youtube.com/embed/CQ85sUNBK7w'
    ]
}
sample_form_data = {
    'title': sample_playlist['title'],
    'description': sample_playlist['description'],
    'videos': '\n'.join(sample_playlist['videos'])
}

class PlaylistTests(TestCase):
    """Flask tests."""

    def Setup(self):
        """Stuff to do before every test"""
        #Get the Flask test client
        self.client = app.test_client()

        #Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Tests the playlist homepage"""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Playlist', result.data)

    def test_new(self):
        """Test the new playlist creation page"""
        result = self.client.get('/playlist/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New Playlist', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_playlist(self, mock_find):
        """Test showing a single playlist"""
        mock_find.return_value = sample_playlist

        result = self.client.get(f'/playlist/{sample_playlist_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Cat Videos', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_playlist(self, mock_find):
        """Test showing a single playlist"""
        mock_find.return_value = sample_playlist

        result = self.client.get(f'/playlist/{sample_playlist_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Cat Videos', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_submit_playlist(self, mock_insert):
        """Test submitting a new playlist"""
        result = self.client.post('/playlist', data=sample_form_data)

        #After submitting, should redirect to that playlists' page
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_playlist)

    #@mock.patch('pymongo.collection.Collection.update_one')
    #def test_update_playlist(self, mock_update):


    if __name__ == '__main__':
        unittest_main()