import spotipy
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
        return artists

    def get_recent_played_tracks(self):
        results = self.sp.current_user_recently_played()
        tracks = results["items"]
        return tracks

    def get_top_tracks(self):
        results = self.sp.current_user_top_tracks(time_range="long_term", limit=25)


    def track_trimmer(self, results):
        tracks = results["items"]
        trimmed_tracks = []
        for track in tracks:
            track_info = {}
            track_info["album"] = track["album"]
            track_info["artist"] = track["artists"][0]
            track_info["id"] = track["id"]
            track_info["name"] = track["name"]
            trimmed_tracks.append(track_info)
        return trimmed_tracks

    def get_top_genres(self):
        pass

    def get_audio_features(self, tracks):

        track_ids = [track["track"]["id"] for track in tracks]
        audio_features = self.sp.audio_features(track_ids)

        valence_mapping = ['Depressing', 'Sad', 'Melancholic', 'Mellow', 'Calm',
                        'Neutral', 'Upbeat', 'Peppy', 'Excited', 'Euphoric', 'Ecstatic']

        danceability_mapping = ['Stationary', 'Little Movement', 'Light Footed', 'Grooving',
                                'Moving', 'Bouncy', 'Bopping', 'Jiving', 'Raving', 'Going Crazy',
                                'You\'re a MANIAC, MANIAC on the floor!']

        key_mapping = ['C', 'C♯/D♭', 'D', 'D♯/E♭', 'E', 'F', 'F♯/G♭', 'G', 'G♯/A♭', 'A', 'A♯/B♭', 'B']

        for i, track in enumerate(tracks):
            song = track['track']['name']
            artist = track['track']['artists'][0]['name']
            valence_rating = int(audio_features[i]['valence'] * 10)
            valence = valence_mapping[min(valence_rating, len(valence_mapping) - 1)]
            danceability_rating = int(audio_features[i]['danceability'] * 10)
            danceability = danceability_mapping[min(danceability_rating, len(danceability_mapping) - 1)]
            key = audio_features[i]['key']
            musical_key = key_mapping[min(key, len(key_mapping) - 1)]
            tempo = int(audio_features[i]['tempo'])
            print(f"{song} by {artist}"
                f"- BPM: {tempo}, Danceability: {danceability}, Key: {musical_key}, Valence: {valence}")

