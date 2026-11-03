# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

The recommender works like a judge scoring every song in the catalog against what one listener says they like. It does not learn from listening history. It only compares a song's description to the listener's stated taste.

**What it looks at.** Each song is described by its genre (such as lofi or rock), its mood (such as chill or intense), and three numbers between 0 and 1: energy (calm to intense), valence (sad to cheerful), and acousticness (electronic to acoustic). The listener tells the system a favorite genre and mood, a target energy, and whether they like acoustic music. They can also give a target valence.

**How a song earns points.** Each feature is worth a different number of points, and the system adds them up:

- **Energy** is worth the most, up to 2 points.
- **Mood** is worth up to 1.5 points.
- **Genre** is worth up to 1 point.
- **Valence** is worth up to 1 point.
- **Acousticness** is worth up to half a point.

Genre and mood are all-or-nothing. A song gets the full points if its label matches the listener's favorite, and nothing if it doesn't. The three numbers work differently. The system rewards a song for being *close* to the listener's target, not for being higher or lower. A song with energy 0.38 earns nearly full points for a listener who wants 0.40, and a song at 0.90 earns almost none. A song that is too intense is penalized as much as one that is too mellow.

**Turning points into a score.** The points are added up and divided by the most a song could earn, so every song gets a score between 0 and 1. A score near 1 means the song is close to the listener's taste on every feature.

**Choosing what to recommend.** The system scores every song, sorts them from highest to lowest, and shows the top five. Each recommendation comes with a plain-language explanation listing which features earned points, for example "mood match (chill) (+1.5)", so the listener can see why a song was picked.

**Why energy and mood count more than genre.** Genre is a broad label, and the catalog has only 28 songs, mostly one or two per genre. If genre counted for the most, the top results would be just the songs with the right genre label, whatever they sound like. Giving more weight to energy and mood lets a song from another genre rank high when it matches how the listener wants to feel.

**Changes from the starter logic.**

- Genre counts for less than mood and energy. The common starting point gave genre the largest weight.
- Valence and acousticness are included, so the system looks at more than genre, mood and energy.
- Energy and the other numbers are scored by closeness to a target instead of "higher is better."
- Every recommendation shows its reasons along with the points each feature earned.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
