"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


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

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
