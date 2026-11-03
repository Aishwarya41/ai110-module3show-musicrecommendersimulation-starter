"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


# Numeric values are targets to be close to, not minimums.
PROFILES = {
    # --- Distinct, well-behaved profiles ---
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.90,
        "target_valence": 0.85,
        "target_acousticness": 0.15,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
        "target_valence": 0.60,
        "target_acousticness": 0.75,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.92,
        "target_valence": 0.40,
        "target_acousticness": 0.08,
    },

    # --- Adversarial / edge-case profiles ---
    # Conflicting: "sad" usually means low energy, but asks for 0.9 energy.
    # Also, no song in the catalog has mood "sad".
    "Sad but Hyper": {
        "favorite_genre": "pop",
        "favorite_mood": "sad",
        "target_energy": 0.90,
        "target_valence": 0.15,
        "target_acousticness": 0.50,
    },
    # Genre says calm, but everything else says loud and aggressive.
    "Lofi Genre, Metal Everything Else": {
        "favorite_genre": "lofi",
        "favorite_mood": "angry",
        "target_energy": 0.95,
        "target_valence": 0.30,
        "target_acousticness": 0.05,
    },
    # Physically implausible: very high energy AND very high acousticness.
    "Loud Unplugged": {
        "favorite_genre": "folk",
        "favorite_mood": "wistful",
        "target_energy": 0.95,
        "target_valence": 0.50,
        "target_acousticness": 0.95,
    },
    # Genre and mood that don't exist in the data: only numbers can score.
    "Unknown Genre/Mood": {
        "favorite_genre": "k-pop",
        "favorite_mood": "nostalgic-but-hype",
        "target_energy": 0.50,
        "target_valence": 0.50,
        "target_acousticness": 0.50,
    },
    # Targets outside the 0-1 range: every similarity collapses toward 0.
    "Out-of-Range Targets": {
        "favorite_genre": "edm",
        "favorite_mood": "euphoric",
        "target_energy": 1.5,
        "target_valence": -0.3,
        "target_acousticness": 2.0,
    },
    # No preferences at all: every score is 0.0, so ranking is just CSV order.
    "Empty Profile": {},
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\n=== {name} ===")
        for song, score, explanation in recommendations:
            print(f"{song['title']} ({song['genre']}/{song['mood']}) - Score: {score:.2f}")
            print(f"  Because: {explanation}")


if __name__ == "__main__":
    main()
