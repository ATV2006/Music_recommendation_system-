"""
spotify_fetch.py
Fetches tracks from a Spotify playlist and saves audio features to CSV.
Requires: spotipy, pandas
Install : pip install spotipy pandas
"""

import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# ── credentials (set as environment variables) ──────────────────────────────
CLIENT_ID     = os.getenv("SPOTIFY_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "YOUR_CLIENT_SECRET")
# ────────────────────────────────────────────────────────────────────────────


def get_client():
    auth = SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    return spotipy.Spotify(auth_manager=auth)


def fetch_playlist_tracks(sp, playlist_id):
    """Return a list of (track_id, name, artists) from a playlist."""
    results = sp.playlist_tracks(playlist_id)
    tracks = []

    while results:
        for item in results["items"]:
            track = item.get("track")
            if track and track.get("id"):
                artists = ", ".join(a["name"] for a in track["artists"])
                tracks.append({
                    "id":      track["id"],
                    "name":    track["name"],
                    "artists": artists,
                })
        results = sp.next(results) if results["next"] else None

    return tracks


def fetch_audio_features(sp, track_ids):
    """Fetch audio features in batches of 100."""
    all_features = []
    for i in range(0, len(track_ids), 100):
        batch = sp.audio_features(track_ids[i:i + 100])
        all_features.extend([f for f in batch if f])
    return all_features


def build_dataset(playlist_id, output_path="data/tracks.csv"):
    sp = get_client()
    print(f"Fetching tracks from playlist: {playlist_id}")
    tracks = fetch_playlist_tracks(sp, playlist_id)

    if not tracks:
        print("No tracks found.")
        return

    track_ids = [t["id"] for t in tracks]
    print(f"Fetched {len(track_ids)} tracks. Getting audio features…")
    features = fetch_audio_features(sp, track_ids)

    meta_df    = pd.DataFrame(tracks).set_index("id")
    feature_df = pd.DataFrame(features).set_index("id")
    df         = meta_df.join(feature_df, how="inner").reset_index(drop=True)

    os.makedirs("data", exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} tracks to {output_path}")


if __name__ == "__main__":
    playlist_id = input("Enter Spotify Playlist ID: ").strip()
    build_dataset(playlist_id)
