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

**Weakness: very-low-energy listeners are poorly served, and the high energy weight hides it.** Only 1 of the 28 songs has energy below 0.2 (Nocturne in Rain, 0.18), so for a listener who wants energy 0.0 the best song reaches only 0.49 energy similarity and no song reaches 0.6. Energy carries 4.0 of the 7.5 total weight, so those users cannot make up the loss with mood or genre, and their best possible score without a label match is about 0.71, against 0.94 to 0.95 for mid- or high-energy listeners. Because the system always returns five confident-looking results, a sleep or meditation listener sees a list of mediocre matches with no warning that the catalog has almost nothing for them. The same effect pushes mid-energy songs like Spacewalk Thoughts and Willow Letters into many more top-5 lists (450 and 417 of 1,200 test profiles) than extreme songs like Iron Tide (30).

---

## 7. Evaluation  

I ran nine listener profiles through the recommender and read the top 5 songs for each. Three are ordinary listeners and six are "tricky" ones built to confuse the scoring.

**Profiles tested**

- **High-Energy Pop:** wants happy pop, very energetic, cheerful, not acoustic.
- **Chill Lofi:** wants calm, quiet, mostly acoustic study music.
- **Deep Intense Rock:** wants loud, intense, non-acoustic rock.
- **Sad but Hyper:** asks for a "sad" mood but very high energy (conflicting).
- **Lofi Genre, Metal Everything Else:** says "lofi" but wants everything else to sound like metal (conflicting).
- **Loud Unplugged:** wants energy and acoustic-ness both near the maximum (nearly impossible).
- **Unknown Genre/Mood:** asks for a genre and mood that are not in the catalog.
- **Out-of-Range Targets:** asks for energy 1.5, valence -0.3, acousticness 2.0 (impossible numbers).
- **Empty Profile:** states no preferences at all.

**What I looked for:** whether the three ordinary profiles get songs a real person in that mood would accept, and whether the odd profiles fail in a way that is sensible or in a way that is silently wrong.

**What surprised me**

1. **"Gym Hero" keeps showing up.** It appears in the top 5 for seven of the nine profiles, including people who just wanted happy pop. Gym Hero is a pop song that is extremely energetic (0.93 out of 1) and not acoustic at all. The recommender gives the most points to energy, and then it checks if the song's genre is "pop". Gym Hero scores nearly full marks on both, so even though its mood is "intense" rather than "happy" (it loses only the mood points), it still beats songs that match the listener's mood but are a bit calmer. For the empty profile and the out-of-range profile it shows up only because every song scored 0 and ties are broken by the order in the file.
2. **The system never says "I don't know."** For the impossible and empty profiles it still gives five confident-looking answers, with scores of 0.00.
3. **Raising the energy weight (2.0 to 4.0) and lowering genre (1.0 to 0.5) changed more than I expected.** Genre fans were hurt the most, because a song with the right energy now beats a song with the right genre.
4. **A "sad" mood did nothing**, since no song in the catalog is labeled "sad". The "sad" listener was effectively treated as an angry-rock listener.

**Profile-by-profile comparisons (what changed, and does it make sense?)**

- **High-Energy Pop vs. Chill Lofi:** Pop gets Sunrise City and Gloss Pop Heart (loud, bright, electronic); Lofi gets Rainy Window Beats and Midnight Coding (quiet, soft, acoustic). They share no songs. This makes sense: the two profiles are opposites on energy (0.90 vs. 0.40) and acousticness (0.15 vs. 0.75), and the lists follow that.
- **High-Energy Pop vs. Deep Intense Rock:** Both want high energy and low acousticness, so Gym Hero lands in both lists. What differs is the label: pop/happy songs lead for Pop, rock/intense songs lead for Rock. It makes sense that they overlap in the "loud" songs and split on genre and mood. This is the pair that explains why Gym Hero keeps appearing: it is the loud-pop-with-an-intense-mood song that sits right between them.
- **Chill Lofi vs. Deep Intense Rock:** Completely different lists with no overlap, because they sit at opposite ends of energy (0.40 vs. 0.92) and acousticness. This is the cleanest sign the system tells apart calm and intense listeners.
- **Deep Intense Rock vs. Sad but Hyper:** Same loud songs (Broken Amp, Iron Tide, Gym Hero, rock tracks), but Sad but Hyper loses the pop songs it asked for and the top score drops from 0.99 to 0.63. It makes sense: the extremely low valence (0.15) pulls toward dark, angry songs, and with no "sad" songs and little genre weight, the profile drifts into rock. The low top score hints that nothing fits well, but the list is still shown without warning.
- **High-Energy Pop vs. Sad but Hyper:** Both ask for pop with energy 0.9, but Pop's list is cheerful pop while Sad but Hyper's is angry rock. The only difference is a "sad" mood and low valence. Valence and the label shifted the whole list, yet pop songs are gone, so the pop genre request was effectively overruled, which is a sign genre is now weighted too lightly.
- **Chill Lofi vs. Lofi Genre, Metal Everything Else:** Both say "lofi," but one gets lofi songs and the other gets Broken Amp and Iron Tide (rock and metal). That is sensible, because energy, valence and acousticness now carry most of the weight. It also shows the weakness: a listener who really does want lofi would never get it if they also ask for loud, dark sound.
- **Deep Intense Rock vs. Lofi Genre, Metal Everything Else:** Similar loud songs, but Rock's top score is 0.99 and the metal-fan's is 0.93, and Rock lists rock/intense first while the other lists rock/angry first. This matches the moods asked for ("intense" vs. "angry"), so it is a valid result.
- **Loud Unplugged vs. Chill Lofi:** Both want acoustic-ish sound, but Loud Unplugged wants maximum energy and gets rock songs, not folk. The acoustic request was lost, because energy has the largest weight and no song is both loud and acoustic. The system picks "loud" and drops "unplugged" without telling the user.
- **Unknown Genre/Mood vs. Chill Lofi:** Genre and mood were not found, so only the numbers count: it returns the mid-energy songs (Velvet Hours, Smoky Corner Trio) rather than a clear style. Scores of 0.64 to 0.70 look good but are only a "close to average" signal, not real taste. Chill Lofi scores 0.99 because it has labels to match on.
- **Out-of-Range Targets vs. Empty Profile:** Both give near-zero scores and meaningless lists. With the impossible targets, only the genre and mood (edm/euphoric) matched for Neon Pulse Festival (0.27); with no preferences, everything ties at 0.00 and the order is just the order in the CSV file. This makes sense mathematically, but it shows the system should reject or warn about bad input.

**Overall:** the three ordinary profiles behave sensibly and clearly differ from each other. The tricky profiles show the real limits: the system follows energy first, does not understand moods it has not seen, and does not admit when the catalog has nothing good to offer. I compared the profiles most useful for learning something (nine pairings), not all 36 possible pairs.

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
