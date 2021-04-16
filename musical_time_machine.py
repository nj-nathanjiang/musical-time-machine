from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = "My Client ID"
client_secret = "My Client Secret"

date = input("What year do you want to travel to? Enter in YYYY-MM-DD format: ")

hot_100_url = f"https://www.billboard.com/charts/hot-100/{date}"
response = requests.get(hot_100_url)
html_code = response.text

soup = BeautifulSoup(html_code, "html.parser")
list_of_song_titles = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
list_of_song_titles = [tag.getText() for tag in list_of_song_titles]

redirect_uri = "http://example.com"
scope = "playlist-modify-private"

authorization = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private",
                                                          redirect_uri=redirect_uri,
                                                          client_id=client_id,
                                                          client_secret=client_secret,
                                                          show_dialog=True,
                                                          cache_path="token.txt"))

user_id = authorization.current_user()["id"]
song_uris = []
for song in list_of_song_titles:
    result = authorization.search(q=f"track:{song} year:{date.split('-')[0]}", type="track")

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"Sorry. The song {song} does not exist in Spotify's servers.")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
