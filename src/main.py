"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from src.recommender import load_songs, recommend_songs, MAX_SCORE   # python -m src.main
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs, MAX_SCORE       # python src/main.py


WIDTH = 64        # width of the printed report
BAR_LENGTH = 20   # number of characters in the score bar


def score_bar(score: float) -> str:
    """Draw the score as a bar, e.g. [###############-----]."""
    filled = round(score / MAX_SCORE * BAR_LENGTH)
    filled = max(0, min(BAR_LENGTH, filled))  # keep the bar in range even for odd scores
    return "[" + "#" * filled + "-" * (BAR_LENGTH - filled) + "]"


def print_profile(name: str, user_prefs: dict) -> None:
    """Print the taste profile the recommendations are based on."""
    print("=" * WIDTH)
    print(f"  MUSIC RECOMMENDER - {name}".center(WIDTH))
    print("=" * WIDTH)
    print("  Listener profile:")
    print(f"    Genre ........ {user_prefs['favorite_genre']}")
    print(f"    Mood ......... {user_prefs['favorite_mood']}")
    print(f"    Energy ....... {user_prefs['target_energy']:.2f}")
    print(f"    Acoustic ..... {'yes' if user_prefs['likes_acoustic'] else 'no'}")
    print("=" * WIDTH)


def print_recommendations(recommendations: list) -> None:
    """Print each recommendation with its score bar and the reasons behind it."""
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print()
        print(f"  #{rank}  {song['title']}  -  {song['artist']}")
        print(f"      {song['genre']} / {song['mood']}")
        print(f"      Score: {score:.2f} / {MAX_SCORE:.2f}  {score_bar(score)}")
        print("      Why:")
        for reason in explanation.split("; "):
            print(f"        + {reason}")
        print("  " + "-" * (WIDTH - 2))
    print()


# Taste profiles. Keys match the UserProfile dataclass fields in recommender.py.
# Scoring: genre +2.0, mood +1.0, energy up to +1.5, acoustic up to +0.5.
PROFILES = {
    # --- Standard profiles: clear, consistent tastes --------------------
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "likes_acoustic": False,
    },

    # --- Adversarial / edge-case profiles: try to trick the scorer -------
    # Conflicting signals: high energy but a sad mood. The only "sad" song
    # (Rainy Window) is low energy, so mood and energy pull opposite ways.
    "EDGE: Energetic but Sad": {
        "favorite_genre": "blues",
        "favorite_mood": "sad",
        "target_energy": 0.90,
        "likes_acoustic": False,
    },
    # Genre and mood that do not exist in the catalog: no categorical
    # match is possible, so ranking falls back to energy + acoustic only.
    "EDGE: Unknown Genre/Mood": {
        "favorite_genre": "opera",
        "favorite_mood": "triumphant",
        "target_energy": 0.50,
        "likes_acoustic": True,
    },
    # Contradictory texture: loud, angry metal fan who "likes acoustic".
    # Metal songs have near-zero acousticness.
    "EDGE: Acoustic Metalhead": {
        "favorite_genre": "metal",
        "favorite_mood": "angry",
        "target_energy": 0.95,
        "likes_acoustic": True,
    },
    # Out-of-range energy (scale is 0-1). Energy similarity can go
    # negative, so every song may LOSE points on energy.
    "EDGE: Energy Out of Range (1.5)": {
        "favorite_genre": "edm",
        "favorite_mood": "euphoric",
        "target_energy": 1.5,
        "likes_acoustic": False,
    },
    # Near-miss genre: "indie pop" vs "pop" and messy casing/whitespace.
    # Exact match is required, so "indie pop" songs get no genre credit.
    "EDGE: Messy Casing / Near-Miss": {
        "favorite_genre": "  Indie POP ",
        "favorite_mood": "HAPPY",
        "target_energy": 0.80,
        "likes_acoustic": False,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_profile(name, user_prefs)
        print_recommendations(recommendations)


if __name__ == "__main__":
    main()
