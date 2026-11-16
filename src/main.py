"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from src.recommender import load_songs, recommend_songs   # python -m src.main
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs       # python src/main.py


MAX_SCORE = 5.0   # genre 2.0 + mood 1.0 + energy 1.5 + acoustic 0.5
WIDTH = 64        # width of the printed report
BAR_LENGTH = 20   # number of characters in the score bar


def score_bar(score: float) -> str:
    """Draw the score as a bar, e.g. [###############-----]."""
    filled = round(score / MAX_SCORE * BAR_LENGTH)
    return "[" + "#" * filled + "-" * (BAR_LENGTH - filled) + "]"


def print_profile(user_prefs: dict) -> None:
    """Print the taste profile the recommendations are based on."""
    print("=" * WIDTH)
    print("  MUSIC RECOMMENDER - Top Picks".center(WIDTH))
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


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Taste profile: a "late-night study" listener who wants calm, acoustic lofi.
    # Keys match the UserProfile dataclass fields in recommender.py.
    user_prefs = {
        "favorite_genre": "lofi",   # +2.0 points on exact match
        "favorite_mood": "chill",   # +1.0 point on exact match
        "target_energy": 0.40,      # up to +1.5 points, by closeness to this value
        "likes_acoustic": True,     # up to +0.5 points, favors high acousticness
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_profile(user_prefs)
    print_recommendations(recommendations)


if __name__ == "__main__":
    main()
