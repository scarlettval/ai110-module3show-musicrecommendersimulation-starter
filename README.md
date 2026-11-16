# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world platforms like Spotify and TikTok combine two approaches. **Collaborative filtering** recommends what similar users liked, learned from behavior such as plays, skips, likes and playlist adds. **Content-based filtering** recommends songs whose attributes (genre, mood, energy, tempo, and so on) match what a user already enjoys. Most production systems are hybrids: they score many candidate songs, then rank and re-rank them into a feed. My simulation is a **content-based** recommender, since it has song attributes but no data from other users. It puts the user's **genre** first, as a stable long-term taste; **mood** second, as what they want right now; and closeness to their preferred **energy** level third. The goal is for songs that *match* the user's taste to rank highest, rather than songs that are simply louder or calmer. I left out tempo and danceability because in this dataset they closely follow energy (correlations of 0.96 and 0.86), so they would mostly count the same signal again.

**`Song` features used in scoring**

- `genre`: categorical, exact match with the user's favorite
- `mood`: categorical, exact match with the user's favorite
- `energy`: 0–1, scored by closeness to the user's target
- `acousticness`: 0–1, scored according to whether the user likes acoustic music

(`id`, `title` and `artist` identify the song; `tempo_bpm`, `valence` and `danceability` are loaded but not scored.)

**`UserProfile` features**

- `favorite_genre`: e.g. `"lofi"`
- `favorite_mood`: e.g. `"chill"`
- `target_energy`: preferred energy level from 0 to 1, e.g. `0.40`
- `likes_acoustic`: `True` / `False`

**Scoring rule (one song, max 5.0 points)**

| Part | Points |
|---|---|
| Genre match | +2.0 |
| Mood match | +1.0 |
| Energy closeness | 1.5 × (1 − \|song.energy − target_energy\|) |
| Acoustic fit | 0.5 × acousticness if `likes_acoustic`, else 0.5 × (1 − acousticness) |

**Ranking rule (whole catalog)**: score every song, sort from highest to lowest score, break ties consistently, and return the top *k*.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



