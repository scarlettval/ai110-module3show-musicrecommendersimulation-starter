import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Scoring weights from the Algorithm Recipe in README.md (max total = 5.0).
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.5
ACOUSTIC_WEIGHT = 0.5

# Best possible score: the sum of the weights used in score_song.
MAX_SCORE = GENRE_WEIGHT + MOOD_WEIGHT + ENERGY_WEIGHT + ACOUSTIC_WEIGHT

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

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py

    Returns one dict per row. Numeric columns are converted so they can be
    used in math: `id` becomes an int, the audio features become floats.
    Text columns (title, artist, genre, mood) stay as strings.
    """
    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            song: Dict = {}
            for key, value in row.items():
                value = value.strip()
                if key in int_fields:
                    song[key] = int(value)
                elif key in float_fields:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)

    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Algorithm recipe (max 5.0 points):
      - Genre match:      +2.0
      - Mood match:       +1.0
      - Energy closeness: 1.5 * (1 - |song energy - target energy|)
      - Acoustic fit:     0.5 * acousticness       if the user likes acoustic
                          0.5 * (1 - acousticness) otherwise

    Returns (score, reasons), where reasons lists every part that added points.
    """
    score = 0.0
    reasons: List[str] = []

    # Categorical features: all-or-nothing exact match (case-insensitive).
    if song["genre"].strip().lower() == user_prefs["favorite_genre"].strip().lower():
        score += GENRE_WEIGHT
        reasons.append(f"genre match: {song['genre']} (+{GENRE_WEIGHT:.1f})")

    if song["mood"].strip().lower() == user_prefs["favorite_mood"].strip().lower():
        score += MOOD_WEIGHT
        reasons.append(f"mood match: {song['mood']} (+{MOOD_WEIGHT:.1f})")

    # Numeric feature: reward closeness to the target, not a higher or lower value.
    # Energy is on a 0-1 scale, so the distance is also 0-1 and similarity = 1 - distance.
    target_energy = user_prefs["target_energy"]
    energy_similarity = 1.0 - abs(song["energy"] - target_energy)
    energy_points = ENERGY_WEIGHT * energy_similarity
    score += energy_points
    reasons.append(
        f"energy {song['energy']:.2f} vs target {target_energy:.2f} (+{energy_points:.2f})"
    )

    # Acoustic preference is yes/no, so it rewards one direction of the scale.
    if user_prefs.get("likes_acoustic", False):
        acoustic_fit = song["acousticness"]
        label = "acoustic sound"
    else:
        acoustic_fit = 1.0 - song["acousticness"]
        label = "non-acoustic sound"
    acoustic_points = ACOUSTIC_WEIGHT * acoustic_fit
    score += acoustic_points
    reasons.append(
        f"{label}, acousticness {song['acousticness']:.2f} (+{acoustic_points:.2f})"
    )

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # 1. Judge: score every song in the catalog with score_song.
    #    Each item becomes (song, score, reasons); the * unpacks score_song's tuple.
    scored = [(song, *score_song(user_prefs, song)) for song in songs]

    # 2. Rank: highest score first. Ties are broken by lower song id so the
    #    order is always the same. sorted() returns a new list and leaves
    #    `songs` untouched.
    ranked = sorted(scored, key=lambda item: (-item[1], item[0]["id"]))

    # 3. Keep the top k and turn each reasons list into one explanation string.
    return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked[:k]]
