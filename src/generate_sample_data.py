"""
generate_sample_data.py
Creates a small synthetic tracks.csv so you can test the recommender
without a Spotify account.
"""

import os
import random
import pandas as pd

SONGS = [
    ("Blinding Lights",      "The Weeknd"),
    ("Shape of You",         "Ed Sheeran"),
    ("Levitating",           "Dua Lipa"),
    ("Stay",                 "The Kid LAROI"),
    ("Peaches",              "Justin Bieber"),
    ("Good 4 U",             "Olivia Rodrigo"),
    ("Montero",              "Lil Nas X"),
    ("Butter",               "BTS"),
    ("Permission to Dance",  "BTS"),
    ("Bad Guy",              "Billie Eilish"),
    ("Happier Than Ever",    "Billie Eilish"),
    ("drivers license",      "Olivia Rodrigo"),
    ("Dynamite",             "BTS"),
    ("Watermelon Sugar",     "Harry Styles"),
    ("As It Was",            "Harry Styles"),
    ("Anti-Hero",            "Taylor Swift"),
    ("Shake It Off",         "Taylor Swift"),
    ("Flowers",              "Miley Cyrus"),
    ("Cruel Summer",         "Taylor Swift"),
    ("Espresso",             "Sabrina Carpenter"),
]

random.seed(42)

rows = []
for name, artist in SONGS:
    rows.append({
        "name":             name,
        "artists":          artist,
        "danceability":     round(random.uniform(0.3, 0.95), 3),
        "energy":           round(random.uniform(0.3, 0.95), 3),
        "loudness":         round(random.uniform(-12, -2), 2),
        "speechiness":      round(random.uniform(0.02, 0.25), 3),
        "acousticness":     round(random.uniform(0.01, 0.80), 3),
        "instrumentalness": round(random.uniform(0.0,  0.10), 4),
        "liveness":         round(random.uniform(0.05, 0.40), 3),
        "valence":          round(random.uniform(0.2,  0.90), 3),
        "tempo":            round(random.uniform(80,   180),  1),
    })

os.makedirs("data", exist_ok=True)
df = pd.DataFrame(rows)
df.to_csv("data/tracks.csv", index=False)
print(f"Generated {len(df)} sample tracks → data/tracks.csv")
