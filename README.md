# Music Recommendation System

A content-based music recommender that suggests similar songs from a playlist.  
Built with **Spotify API · Pandas · PCA · Scikit-Learn**.

---

## How It Works

1. **Fetch** – Pull tracks and audio features from a Spotify playlist via the Spotify API.  
2. **Preprocess** – Clean the data with Pandas (drop nulls, select audio features).  
3. **PCA** – Reduce the 9 audio features to 5 principal components, capturing maximum variance.  
4. **Recommend** – Compute cosine similarity between songs in PCA space and return the top-N matches.

---

## Project Structure

```
music-recommender/
├── data/
│   └── tracks.csv            # Generated dataset (git-ignored)
├── src/
│   ├── spotify_fetch.py      # Pull data from Spotify API → tracks.csv
│   ├── generate_sample_data.py  # Create sample data (no Spotify needed)
│   └── recommender.py        # PCA + cosine similarity recommender
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2a. Use sample data (no Spotify account needed)

```bash
cd music-recommender
python src/generate_sample_data.py   # creates data/tracks.csv
python src/recommender.py
```

### 2b. Use real Spotify data

1. Create an app at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2. Copy your **Client ID** and **Client Secret**.
3. Export them as environment variables:

```bash
export SPOTIFY_CLIENT_ID="your_client_id"
export SPOTIFY_CLIENT_SECRET="your_client_secret"
```

4. Fetch a playlist (grab the playlist ID from its Spotify URL):

```bash
python src/spotify_fetch.py        # enter playlist ID when prompted
```

5. Run the recommender:

```bash
python src/recommender.py
```

---

## Example

```
Enter a song name to get recommendations: Blinding Lights

Top Recommendations:
          name          artists  similarity
     Levitating         Dua Lipa       0.987
   Watermelon Sugar  Harry Styles       0.974
      Butter              BTS       0.961
      Dynamite            BTS       0.955
    Shape of You     Ed Sheeran       0.943
```

---

## Audio Features Used

| Feature          | Description                          |
|------------------|--------------------------------------|
| danceability     | How suitable for dancing (0–1)       |
| energy           | Intensity and activity level (0–1)   |
| loudness         | Overall loudness in dB               |
| speechiness      | Presence of spoken words (0–1)       |
| acousticness     | Confidence of being acoustic (0–1)   |
| instrumentalness | Predicts no vocals (0–1)             |
| liveness         | Presence of live audience (0–1)      |
| valence          | Musical positiveness (0–1)           |
| tempo            | Estimated BPM                        |

---

## Tech Stack

| Tool         | Purpose                              |
|--------------|--------------------------------------|
| Spotify API  | Source of playlist tracks & features |
| Pandas       | Data loading and preprocessing       |
| Scikit-Learn | PCA + cosine similarity              |
| NumPy        | Numerical operations                 |

---

## Notes

- The `data/` folder is not committed to Git. Add `data/` to your `.gitignore`.
- PCA components (`n_components`) and recommendations count (`top_n`) can be adjusted in `recommender.py`.
