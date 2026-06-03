"""
Music Recommendation System
Uses Spotify API + Pandas + PCA + Content-Based Filtering (Scikit-Learn)
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity


def load_data(filepath):
    """Load music dataset from CSV."""
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} tracks.")
    return df


def preprocess(df):
    """Clean and select audio features."""
    features = [
        "danceability", "energy", "loudness", "speechiness",
        "acousticness", "instrumentalness", "liveness",
        "valence", "tempo"
    ]
    df = df.dropna(subset=features)
    return df, features


def apply_pca(df, features, n_components=5):
    """Standardize features and apply PCA."""
    scaler = StandardScaler()
    X = scaler.fit_transform(df[features])

    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X)

    explained = pca.explained_variance_ratio_.sum() * 100
    print(f"PCA variance captured: {explained:.1f}% with {n_components} components")
    return X_pca


def recommend(df, X_pca, song_name, top_n=5):
    """Find top_n similar songs using cosine similarity."""
    df = df.reset_index(drop=True)

    # Find the song index (case-insensitive)
    matches = df[df["name"].str.lower() == song_name.lower()]
    if matches.empty:
        print(f"Song '{song_name}' not found in dataset.")
        return None

    idx = matches.index[0]
    sim = cosine_similarity([X_pca[idx]], X_pca)[0]
    sim[idx] = -1  # exclude the song itself

    top_indices = sim.argsort()[::-1][:top_n]
    results = df.iloc[top_indices][["name", "artists"]].copy()
    results["similarity"] = sim[top_indices].round(3)
    return results


if __name__ == "__main__":
    # Example run with sample data
    df = load_data("data/tracks.csv")
    df, features = preprocess(df)
    X_pca = apply_pca(df, features, n_components=5)

    song = input("Enter a song name to get recommendations: ").strip()
    recs = recommend(df, X_pca, song, top_n=5)

    if recs is not None:
        print("\nTop Recommendations:")
        print(recs.to_string(index=False))
