import os
from flask import Flask, render_template, request
from .models import DB, Song
from .spotify_client import *

from .spotify_client import SPOTIPY_API, SPOTIFY_API, retrieve_spotify_ids, retrieve_spotify_song_id, retrieve_audio_features
from .functions import song_recommender


   
app = Flask(__name__)



# configure app
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialize database
DB.init_app(app)

#initialize Spotify API
spotify = SPOTIFY_API
spotify.perform_auth()
access_token = spotify.access_token

# create table(s)
with app.app_context():
    DB.create_all()

   # ROOT ROUTE
    @app.route('/', methods=["GET", "POST"])
    def root():     
        """Base view"""
        resp = None
        # When visitor types song and artist then hits a button...
        if request.method == "POST":
            # THIS IS WHERE WE GET THE SONG NAME FROM THE HTML
            song_name = request.form["song_name"]
            # THIS IS WHERE WE GET THE ARTIST NAME FROM THE HTML
            artist_name = request.form["artist_name"]
           # REPLACE SPOTIFY.SEARCH WITH *GENERATE_OUTPUT*
            #search_results = spotify.search(query=song_name, search_type="track")
            song_id = retrieve_spotify_song_id(song_name=song_name, artist_name=artist_name)
            features = retrieve_audio_features(spotify_id=song_id)
            recomended_ids = song_recommender(features=features)
            import pdb; pdb.set_trace()
            tracks = ['https://open.spotify.com/embed/track/' + track_id for track_id in recomended_ids]
            # SET UP ITEMS TO EQUAL A LIST OF TRACK ID'S
            #items = search_results['tracks']['items']
            return render_template('predict.html', len=len(tracks), song_urls=tracks)
        
        return render_template('predict.html', title = 'home', len=None, song_urls=None)
if __name__ == "__main__":
    app.run()
           