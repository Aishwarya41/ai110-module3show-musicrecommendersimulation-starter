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
| Energy | 4.0 | Closeness to the target, from 0 to 1 |
| Mood | 1.5 | Exact match is 1, otherwise 0 |
| Genre | 0.5 | Exact match is 1, otherwise 0 |
| Valence | 1.0 | Closeness to the target, from 0 to 1 |
| Acousticness | 0.5 | Closeness to the target, from 0 to 1 |

- **Closeness** uses a Gaussian curve: `exp(-(song - target)^2 / (2 * sigma^2))`. A perfect match scores 1.0, and the score falls smoothly as the song moves away from the target. A song that is too high scores as badly as one that is too low. Sigma is 0.15 for energy, 0.20 for valence, and 0.25 for acousticness.
- **Final score** = `sum(weight * similarity) / sum(weights)`, so it falls between 0 and 1. Features the user gave no preference for are left out of both sums.
- **Why these weights:** mood and energy describe how a song feels, and genre is a coarse label. With only 28 songs and mostly one or two per genre, a heavy genre weight (such as +2.0) would act as a filter and bury good cross-genre matches. So mood counts 3x genre, and energy counts 8x genre.
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
python3 -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python3 -m src.main`, which runs the recommender once per profile in `PROFILES` ([src/main.py](src/main.py)) and prints the top 5. The first three are standard profiles; the rest are adversarial edge cases. Weights: energy 4.0, mood 1.5, genre 0.5, valence 1.0, acousticness 0.5.

### High-Energy Pop

```text
Sunrise City (pop/happy) - Score: 0.93
  Because: genre match (pop) (+0.5); mood match (happy) (+1.5); energy 0.82 is close to target 0.90 (+3.5 of 4.0); valence 0.84 is close to target 0.85 (+1.0 of 1.0); acousticness 0.18 is close to target 0.15 (+0.5 of 0.5)
Gloss Pop Heart (pop/happy) - Score: 0.89
  Because: genre match (pop) (+0.5); mood match (happy) (+1.5); energy 0.80 is close to target 0.90 (+3.2 of 4.0); valence 0.86 is close to target 0.85 (+1.0 of 1.0); acousticness 0.20 is close to target 0.15 (+0.5 of 0.5)
Gym Hero (pop/intense) - Score: 0.77
  Because: genre match (pop) (+0.5); energy 0.93 is close to target 0.90 (+3.9 of 4.0); valence 0.77 is close to target 0.85 (+0.9 of 1.0); acousticness 0.05 is close to target 0.15 (+0.5 of 0.5)
Rooftop Lights (indie pop/happy) - Score: 0.72
  Because: mood match (happy) (+1.5); energy 0.76 is close to target 0.90 (+2.6 of 4.0); valence 0.81 is close to target 0.85 (+1.0 of 1.0); acousticness 0.35 is close to target 0.15 (+0.4 of 0.5)
Neon Pulse Festival (edm/euphoric) - Score: 0.70
  Because: energy 0.95 is close to target 0.90 (+3.8 of 4.0); valence 0.88 is close to target 0.85 (+1.0 of 1.0); acousticness 0.04 is close to target 0.15 (+0.5 of 0.5)
```

### Chill Lofi

```text
Rainy Window Beats (lofi/chill) - Score: 0.99
  Because: genre match (lofi) (+0.5); mood match (chill) (+1.5); energy 0.38 is close to target 0.40 (+4.0 of 4.0); valence 0.58 is close to target 0.60 (+1.0 of 1.0); acousticness 0.82 is close to target 0.75 (+0.5 of 0.5)
Midnight Coding (lofi/chill) - Score: 0.99
  Because: genre match (lofi) (+0.5); mood match (chill) (+1.5); energy 0.42 is close to target 0.40 (+4.0 of 4.0); valence 0.56 is close to target 0.60 (+1.0 of 1.0); acousticness 0.71 is close to target 0.75 (+0.5 of 0.5)
Library Rain (lofi/chill) - Score: 0.97
  Because: genre match (lofi) (+0.5); mood match (chill) (+1.5); energy 0.35 is close to target 0.40 (+3.8 of 4.0); valence 0.60 is close to target 0.60 (+1.0 of 1.0); acousticness 0.86 is close to target 0.75 (+0.5 of 0.5)
Focus Flow (lofi/focused) - Score: 0.80
  Because: genre match (lofi) (+0.5); energy 0.40 is close to target 0.40 (+4.0 of 4.0); valence 0.59 is close to target 0.60 (+1.0 of 1.0); acousticness 0.78 is close to target 0.75 (+0.5 of 0.5)
Late Night Notes (lofi/focused) - Score: 0.79
  Because: genre match (lofi) (+0.5); energy 0.43 is close to target 0.40 (+3.9 of 4.0); valence 0.55 is close to target 0.60 (+1.0 of 1.0); acousticness 0.74 is close to target 0.75 (+0.5 of 0.5)
```

### Deep Intense Rock

```text
Storm Runner (rock/intense) - Score: 0.99
  Because: genre match (rock) (+0.5); mood match (intense) (+1.5); energy 0.91 is close to target 0.92 (+4.0 of 4.0); valence 0.48 is close to target 0.40 (+0.9 of 1.0); acousticness 0.10 is close to target 0.08 (+0.5 of 0.5)
Thunder Road Burnout (rock/intense) - Score: 0.97
  Because: genre match (rock) (+0.5); mood match (intense) (+1.5); energy 0.89 is close to target 0.92 (+3.9 of 4.0); valence 0.52 is close to target 0.40 (+0.8 of 1.0); acousticness 0.12 is close to target 0.08 (+0.5 of 0.5)
Gym Hero (pop/intense) - Score: 0.82
  Because: mood match (intense) (+1.5); energy 0.93 is close to target 0.92 (+4.0 of 4.0); acousticness 0.05 is close to target 0.08 (+0.5 of 0.5)
Broken Amp (rock/angry) - Score: 0.78
  Because: genre match (rock) (+0.5); energy 0.94 is close to target 0.92 (+4.0 of 4.0); valence 0.30 is close to target 0.40 (+0.9 of 1.0); acousticness 0.07 is close to target 0.08 (+0.5 of 0.5)
Iron Tide (metal/angry) - Score: 0.67
  Because: energy 0.97 is close to target 0.92 (+3.8 of 4.0); valence 0.25 is close to target 0.40 (+0.8 of 1.0); acousticness 0.03 is close to target 0.08 (+0.5 of 0.5)
```

### Sad but Hyper

```text
Broken Amp (rock/angry) - Score: 0.63
  Because: energy 0.94 is close to target 0.90 (+3.9 of 4.0); valence 0.30 is close to target 0.15 (+0.8 of 1.0)
Iron Tide (metal/angry) - Score: 0.61
  Because: energy 0.97 is close to target 0.90 (+3.6 of 4.0); valence 0.25 is close to target 0.15 (+0.9 of 1.0)
Gym Hero (pop/intense) - Score: 0.60
  Because: genre match (pop) (+0.5); energy 0.93 is close to target 0.90 (+3.9 of 4.0)
Storm Runner (rock/intense) - Score: 0.58
  Because: energy 0.91 is close to target 0.90 (+4.0 of 4.0)
Thunder Road Burnout (rock/intense) - Score: 0.58
  Because: energy 0.89 is close to target 0.90 (+4.0 of 4.0)
```

### Lofi Genre, Metal Everything Else

```text
Broken Amp (rock/angry) - Score: 0.93
  Because: mood match (angry) (+1.5); energy 0.94 is close to target 0.95 (+4.0 of 4.0); valence 0.30 is close to target 0.30 (+1.0 of 1.0); acousticness 0.07 is close to target 0.05 (+0.5 of 0.5)
Iron Tide (metal/angry) - Score: 0.92
  Because: mood match (angry) (+1.5); energy 0.97 is close to target 0.95 (+4.0 of 4.0); valence 0.25 is close to target 0.30 (+1.0 of 1.0); acousticness 0.03 is close to target 0.05 (+0.5 of 0.5)
Storm Runner (rock/intense) - Score: 0.67
  Because: energy 0.91 is close to target 0.95 (+3.9 of 4.0); valence 0.48 is close to target 0.30 (+0.7 of 1.0); acousticness 0.10 is close to target 0.05 (+0.5 of 0.5)
Thunder Road Burnout (rock/intense) - Score: 0.63
  Because: energy 0.89 is close to target 0.95 (+3.7 of 4.0); acousticness 0.12 is close to target 0.05 (+0.5 of 0.5)
Gym Hero (pop/intense) - Score: 0.60
  Because: energy 0.93 is close to target 0.95 (+4.0 of 4.0); acousticness 0.05 is close to target 0.05 (+0.5 of 0.5)
```

### Loud Unplugged

```text
Storm Runner (rock/intense) - Score: 0.65
  Because: energy 0.91 is close to target 0.95 (+3.9 of 4.0); valence 0.48 is close to target 0.50 (+1.0 of 1.0)
Thunder Road Burnout (rock/intense) - Score: 0.63
  Because: energy 0.89 is close to target 0.95 (+3.7 of 4.0); valence 0.52 is close to target 0.50 (+1.0 of 1.0)
Broken Amp (rock/angry) - Score: 0.61
  Because: energy 0.94 is close to target 0.95 (+4.0 of 4.0); valence 0.30 is close to target 0.50 (+0.6 of 1.0)
Iron Tide (metal/angry) - Score: 0.59
  Because: energy 0.97 is close to target 0.95 (+4.0 of 4.0)
Gym Hero (pop/intense) - Score: 0.58
  Because: energy 0.93 is close to target 0.95 (+4.0 of 4.0)
```

### Unknown Genre/Mood

```text
Velvet Hours (r&b/romantic) - Score: 0.70
  Because: energy 0.49 is close to target 0.50 (+4.0 of 4.0); valence 0.64 is close to target 0.50 (+0.8 of 1.0); acousticness 0.38 is close to target 0.50 (+0.4 of 0.5)
Smoky Corner Trio (jazz/moody) - Score: 0.68
  Because: energy 0.46 is close to target 0.50 (+3.9 of 4.0); valence 0.52 is close to target 0.50 (+1.0 of 1.0)
Dusty Porch Light (country/nostalgic) - Score: 0.66
  Because: energy 0.52 is close to target 0.50 (+4.0 of 4.0); valence 0.68 is close to target 0.50 (+0.7 of 1.0); acousticness 0.74 is close to target 0.50 (+0.3 of 0.5)
Late Night Notes (lofi/focused) - Score: 0.65
  Because: energy 0.43 is close to target 0.50 (+3.6 of 4.0); valence 0.55 is close to target 0.50 (+1.0 of 1.0); acousticness 0.74 is close to target 0.50 (+0.3 of 0.5)
Midnight Coding (lofi/chill) - Score: 0.64
  Because: energy 0.42 is close to target 0.50 (+3.5 of 4.0); valence 0.56 is close to target 0.50 (+1.0 of 1.0); acousticness 0.71 is close to target 0.50 (+0.4 of 0.5)
```

### Out-of-Range Targets

```text
Neon Pulse Festival (edm/euphoric) - Score: 0.27
  Because: genre match (edm) (+0.5); mood match (euphoric) (+1.5)
Nocturne in Rain (classical/melancholic) - Score: 0.00
  Because: No close matches
Iron Tide (metal/angry) - Score: 0.00
  Because: No close matches
Broken Amp (rock/angry) - Score: 0.00
  Because: No close matches
Gym Hero (pop/intense) - Score: 0.00
  Because: No close matches
```

### Empty Profile

```text
Sunrise City (pop/happy) - Score: 0.00
  Because: No close matches
Midnight Coding (lofi/chill) - Score: 0.00
  Because: No close matches
Storm Runner (rock/intense) - Score: 0.00
  Because: No close matches
Library Rain (lofi/chill) - Score: 0.00
  Because: No close matches
Gym Hero (pop/intense) - Score: 0.00
  Because: No close matches
```

---

## Experiments You Tried

**Weight shift: energy 2.0 → 4.0, genre 1.0 → 0.5.** The final score is still `sum(weight * similarity) / sum(weights)`, now with a total weight of 7.5 instead of 6.0. Every similarity is between 0 and 1, so every score still falls between 0 and 1. I checked this across all 9 profiles and all songs (min 0.00, max 0.99), and a perfect match scores exactly 1.0. The tests still pass. Effects:

- The standard profiles keep the same #1 song. In Deep Intense Rock, Gym Hero (pop/intense) now beats Broken Amp (rock/angry) for #3, and Highway Anthem drops out of the top 5.
- Genre loyalty weakens. In Sad but Hyper, the pop songs leave the top 5 and high-energy rock and metal take over.
- Loud Unplugged flips. Willow Letters, which matched genre and mood but not energy, falls out, and high-energy rock wins. Energy now beats everything else.
- Scores for sparse profiles rise (Unknown Genre/Mood goes from about 0.5 to about 0.7), because energy dominates the average. A middling top score is now a weaker sign that nothing matched.

---

## Limitations and Risks

- **Tiny catalog.** It only has 28 songs. Nine of the 15 genres have a single song, and lofi has 6.
- **Thin at the extremes.** Only one song has energy below 0.2. Very calm listeners get weaker matches than everyone else.
- **Energy dominates.** Energy carries 4.0 of the 7.5 total weight. A song with the right energy can beat one with the right genre or mood.
- **Labels are all or nothing.** "Chill" gets no credit for "relaxed." A "sad" listener gets no mood credit, because no song is labeled "sad."
- **No "I don't know."** It shows five confident-looking results even when every score is near 0.00, such as for empty or impossible profiles.


See the [Model Card](model_card.md) for more detail.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

**How recommenders turn data into predictions.** My recommender does not learn anything. It scores every song by how close it is to what the listener says they want, adds up weighted points, and sorts the results. That is enough to feel like a real recommendation, especially because each song comes with a reason. But the weights are choices. When I doubled the weight on energy and halved the weight on genre, the same listener got different songs. A "prediction" is really a set of opinions about what matters, written as numbers.

**Where bias and unfairness can show up.** The bias came from the catalog and the labels, not only from the formula. Only one song has energy below 0.2, so very calm listeners get weaker matches than everyone else. Songs near mid-energy appear in far more top-5 lists than extreme ones, and lofi has 6 songs while nine genres have only one. Moods are exact labels, so a "sad" listener gets no mood credit when no song is labeled "sad." Worst of all, the system still shows five confident-looking results when nothing fits. In a real app, those gaps would quietly give some users worse recommendations and some artists less exposure, and no one would see it happen.



