import csv
import math
from typing import List, Dict, Tuple, Optional
from dataclasses import asdict, dataclass

# How much each feature counts toward the final score
WEIGHTS = {
    "energy": 2.0,
    "mood": 1.5,
    "genre": 1.0,
    "valence": 1.0,
    "acousticness": 0.5,
}

# Tolerance (sigma) for each numeric feature: the distance at which a song's
# similarity drops to about 0.61
SIGMAS = {
    "energy": 0.15,
    "valence": 0.20,
    "acousticness": 0.25,
}

# Maps each numeric feature to the user_prefs key holding its target value
NUMERIC_TARGETS = {
    "energy": "target_energy",
    "valence": "target_valence",
    "acousticness": "target_acousticness",
}

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    @staticmethod
    def _prefs(user: UserProfile) -> Dict:
        """Convert a UserProfile into the prefs dict that score_song expects."""
        return {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "target_acousticness": 0.8 if user.likes_acoustic else 0.2,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the k songs with the highest score for this user."""
        prefs = self._prefs(user)
        ranked = sorted(
            self.songs,
            key=lambda song: score_song(prefs, asdict(song))[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a semicolon-separated list of why this song fits the user."""
        _, reasons = score_song(self._prefs(user), asdict(song))
        return "; ".join(reasons) if reasons else "No matching preferences"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    numeric = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")
    songs = []
    with open(csv_path, newline="", encoding="utf8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for key in numeric:
                row[key] = float(row[key])
            songs.append(row)
    return songs

def numeric_similarity(value: float, target: float, sigma: float) -> float:
    """Gaussian similarity: 1.0 at the target, falling off with distance."""
    return math.exp(-((value - target) ** 2) / (2 * sigma ** 2))

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Returns a weighted average of per-feature similarities (0 to 1) and a
    list of reasons, each showing the points that feature contributed. Features the user gave no preference for are skipped.
    """
    total = 0.0
    weight_sum = 0.0
    reasons = []

    for feature, pref_key in (("genre", "favorite_genre"), ("mood", "favorite_mood")):
        wanted = user_prefs.get(pref_key)
        if wanted is None:
            continue
        weight_sum += WEIGHTS[feature]
        if song[feature] == wanted:
            total += WEIGHTS[feature]
            reasons.append(f"{feature} match ({wanted}) (+{WEIGHTS[feature]:.1f})")

    for feature, pref_key in NUMERIC_TARGETS.items():
        target = user_prefs.get(pref_key)
        if target is None:
            continue
        sim = numeric_similarity(song[feature], target, SIGMAS[feature])
        points = WEIGHTS[feature] * sim
        total += points
        weight_sum += WEIGHTS[feature]
        if sim >= 0.6:
            reasons.append(
                f"{feature} {song[feature]:.2f} is close to target {target:.2f} "
                f"(+{points:.1f} of {WEIGHTS[feature]:.1f})"
            )

    score = total / weight_sum if weight_sum else 0.0
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "No close matches"
        scored.append((song, score, explanation))
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
