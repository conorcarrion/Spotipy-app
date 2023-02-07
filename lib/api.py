import spotipy
import tabpy
import yaml
import spotipy.util as util

class API:
    def __init__(self):

        # Load client ID and secret from a YAML file
        with open("credentials.yaml", "r") as outfile:
            credentials = yaml.safe_load(outfile)
        client_id = credentials["CLIENT_ID"]
        client_secret = credentials["CLIENT_SECRET"]
        redirect_uri = credentials["uri"]

        # Your Spotify username
        username = credentials["juno"]

        # Scopes for the Spotify API
        scopes = "user-top-read"

        # Get an authorization token
        token = util.prompt_for_user_token(username, scopes, client_id, client_secret, redirect_uri)

        # Initialize the Spotify API client
        self.sp = spotipy.Spotify(auth=token)
        return self.sp

    def get_alltime_most_played_artists(self):
        # Get your all-time most played artists
        results = self.sp.current_user_top_artists(time_range="long_term", limit=15)
        artists = results["items"]
        for artist in artists:
            print(f"{artist['name']} ({artist['popularity']})")


