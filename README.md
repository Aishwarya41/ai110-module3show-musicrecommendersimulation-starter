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

Real-world recommenders like Spotify and YouTube combine two signals: collaborative filtering, which suggests what similar listeners played, and content-based filtering, which matches the attributes of songs you already like. They learn from huge amounts of behavior such as skips, replays, and playlists. This version is a small content-based recommender with no listening history. It prioritizes closeness to a user's stated taste: genre and mood matches, plus how near a song's energy and valence are to the user's targets, so a song is rewarded for fitting the preference, not for having a higher or lower value.

### Features

- **`Song`**: `genre`, `mood`, `energy`, `valence`, and `acousticness` are used in scoring. `tempo_bpm` and `danceability` are loaded but not scored yet.
- **`UserProfile`**: `favorite_genre`, `favorite_mood`, `target_energy`, and `likes_acoustic`. Acoustic preference becomes a target of 0.8 (likes acoustic) or 0.2 (doesn't). Target valence is optional.

### Algorithm Recipe

Every song is scored against the user's profile, then the songs are ranked by score and the top `k` are returned.

| Feature | Weight | How it scores |
|---|---|---|
| Energy | 2.0 | Closeness to the target, from 0 to 1 |
| Mood | 1.5 | Exact match is 1, otherwise 0 |
| Genre | 1.0 | Exact match is 1, otherwise 0 |
| Valence | 1.0 | Closeness to the target, from 0 to 1 |
| Acousticness | 0.5 | Closeness to the target, from 0 to 1 |

- **Closeness** uses a Gaussian curve: `exp(-(song - target)^2 / (2 * sigma^2))`. A perfect match scores 1.0, and the score falls smoothly as the song moves away from the target. A song that is too high scores as badly as one that is too low. Sigma is 0.15 for energy, 0.20 for valence, and 0.25 for acousticness.
- **Final score** = `sum(weight * similarity) / sum(weights)`, so it falls between 0 and 1. Features the user gave no preference for are left out of both sums.
- **Why these weights:** mood and energy describe how a song feels, and genre is a coarse label. With only 28 songs and mostly one or two per genre, a heavy genre weight (such as +2.0) would act as a filter and bury good cross-genre matches. So mood counts 1.5x genre, and energy counts 2x genre.
- **Each recommendation** comes with the reasons it scored well, such as "mood matches (chill)" or "energy 0.38 is close to target 0.40".

### Expected Biases

- **Exact-match labels are all-or-nothing.** "Chill" earns nothing for a "relaxed" song, even though the two are close. The system can miss good songs because of word choice.
- **Energy can outvote mood.** Energy is the largest weight, so a song with the right energy but the wrong mood can outrank one with the right mood and slightly different energy. For example, an "angry" song could rank above a "peaceful" one for a user who wants low energy and peaceful music.
- **Genre is weighted lowest of the label features, so a loyal genre fan may see off-genre songs.** The system might undervalue genre for users who care about it strongly.
- **No history or discovery.** The system recommends only what matches stated taste, so it can't surprise the user and tends to repeat the same kind of song.

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



