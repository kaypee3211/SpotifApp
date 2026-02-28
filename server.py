from flask import Flask, render_template, request

import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

CLIENT_ID = "Your client id"
CLIENT_SECRET = "Your client secret"
REDIRECT_URI = "http://127.0.0.1:5000"
SCOPE = "user-read-private user-top-read user-read-currently-playing user-library-read"

sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
)



@app.route("/")
def hello_world():
    
    code = request.args.get("code")
    if code:
        token_info = sp_oauth.get_access_token(code, as_dict=True)
        sp = spotipy.Spotify(auth=token_info["access_token"])
        user = sp.current_user()

        display_name = user["display_name"]
        country = user["country"]
        followers = user["followers"]
        image = user["images"]

        top_artist = sp.current_user_top_artists(time_range='medium_term',limit=5)
        top_tracks = sp.current_user_top_tracks(time_range='medium_term',limit=5)

        return render_template(
            "index.html", 
            spotify_name=display_name,
            cou = country, 
            f = followers, 
            n = image,
            topA=top_artist['items'],
            topT=top_tracks['items']
            )
    else:
        auth_url = sp_oauth.get_authorize_url()
        return f'<a href="{auth_url}">Zaloguj się przez Spotify</a>'
    
if __name__ == "__main__":
    app.run(debug=True)