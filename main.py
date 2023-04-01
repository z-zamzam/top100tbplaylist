import requests
from bs4 import BeautifulSoup
import lxml
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os


# # Retrieving the desired billboard page and calling the bs class on the data
user_choice = input("Enter the year you would like to be taken back to. (YYYY-MM-DD)\n")
response = requests.get(f'https://www.billboard.com/charts/hot-100/{user_choice}/')
soup = BeautifulSoup(response.text, 'lxml')

# Cleaning up the data and selecting specific elements we need from the list
songs = [song.getText().replace("\t", "").replace("\n", "") for song in soup.select(".o-chart-results-list-row-container #title-of-a-story")][::4]

# Calling the spotify API using spotipy library
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        show_dialog=True,
        cache_path="token.txt"
    )
)
# Creating a list to store the songs in the correct format and a playlist to add the retrieved songs to
playlist_id = sp.user_playlist_create(os.environ['USER_ID'], f'{user_choice} Throwback', public=False)
song_list = []

# Adding the songs to the song_list and then passing the song_list as an argument to add to the playlist
for i in range(0, len(songs)):
    song_uri = sp.search(q=songs[i], type='track')
    song = song_uri['tracks']['items'][0]['uri'].split(":")[2]
    song_list.append(song)
sp.playlist_add_items(playlist_id['id'], song_list)

