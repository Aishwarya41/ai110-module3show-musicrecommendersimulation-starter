# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

---

## 2. Goal / Task and Intended Use  

**Goal.** The model suggests songs a listener might like. It picks 5 songs from a small catalog. It also says why it picked each one.

**Who it is for.** It is for classroom learning. It shows how a simple recommender works.

**What it assumes.** The listener tells us what they like. They give a favorite genre, a favorite mood, and target numbers. The model does not learn from listening history.

**Intended use.**
- Learning how scoring and ranking work.
- Testing how profiles change the results.
- Explaining why a song was picked.

**Not intended for.**
- Real music apps with real users.
- Deciding what artists get heard or paid.
- Mood or health advice, like picking music for someone who is sad.
- Large catalogs. It was only tried on 28 songs.

---

## 3. Algorithm Summary  

The model gives every song a score from 0 to 1. A higher score means a better fit.

Each song earns points for five things:

| Feature | Max points | How it earns them |
|---|---|---|
| Energy | 4.0 | Closer to the target is better |
| Mood | 1.5 | Full points if it matches, else none |
| Valence (cheerfulness) | 1.0 | Closer to the target is better |
| Genre | 0.5 | Full points if it matches, else none |
| Acousticness | 0.5 | Closer to the target is better |

- Genre and mood are all or nothing.
- Energy, valence, and acousticness are about being close. A song that is too loud is penalized like one that is too quiet.
- The model adds up the points. It divides by the most a song could earn. That keeps every score between 0 and 1.
- If the listener skips a feature, it is left out.
- Then it sorts the songs and shows the top 5. Each one has a short reason.

**Why energy counts most.** Energy says how a song feels. Genre is just a label. The catalog is small, so a heavy genre weight would hide good songs from other genres.

**One change I made.** I doubled the energy weight (2.0 to 4.0). I halved the genre weight (1.0 to 0.5). Scores stayed between 0 and 1. The tests still passed.

---

## 4. Data Used  

- The catalog has **28 songs** in a CSV file.
- Each song has a genre, a mood, and numbers for energy, tempo, valence, danceability, and acousticness.
- There are **15 genres**. Lofi has 6 songs. Rock has 4. Nine genres have only 1 song.
- There are **16 moods**. Chill is the most common, with 4 songs.
- The model uses genre, mood, energy, valence, and acousticness. It ignores tempo and danceability.

**Limits.**
- The catalog is tiny.
- Only one song has energy below 0.2.
- There is no "sad" mood.
- Nothing about lyrics, language, artists, or culture.
- I did not add or remove songs.

---

## 5. Strengths  

- It works well for clear listeners. Chill Lofi, High-Energy Pop, and Deep Intense Rock all got sensible lists.
- Calm listeners and intense listeners get totally different songs.
- Every pick comes with a reason. That makes it easy to check.
- Scoring by closeness works better than "higher is better."
- The top picks matched my own sense of what fits.

---

## 6. Observed Behavior / Biases and Limitations  

**Biggest weakness: very-low-energy listeners are poorly served, and the high energy weight hides it.** Only 1 of the 28 songs has energy below 0.2 (Nocturne in Rain, 0.18), so for a listener who wants energy 0.0 the best song reaches only 0.49 energy similarity and no song reaches 0.6. Energy carries 4.0 of the 7.5 total weight, so those users cannot make up the loss with mood or genre, and their best possible score without a label match is about 0.71, against 0.94 to 0.95 for mid- or high-energy listeners. Because the system always returns five confident-looking results, a sleep or meditation listener sees a list of mediocre matches with no warning that the catalog has almost nothing for them. The same effect pushes mid-energy songs like Spacewalk Thoughts and Willow Letters into many more top-5 lists (450 and 417 of 1,200 test profiles) than extreme songs like Iron Tide (30).

**Other patterns I saw.**
- **Gym Hero shows up too much.** It is a loud pop song. It appeared in the top 5 for 7 of 9 profiles.
- **Energy beats everything.** A song with the right energy can win over one with the right genre.
- **Unknown moods count for nothing.** Nobody can get mood points for "sad."
- **Labels are all or nothing.** "Chill" gets no credit for "relaxed." "Indie pop" gets no credit for "pop."
- **Lofi is over-represented.** Lofi fans get a full list. Reggae fans get one song.
- **No warning for bad matches.** The model shows 5 songs even when the scores are 0.00.
- **One target per feature.** A listener who likes both very calm and very loud music cannot say so.

---

## 7. Evaluation  

**Short summary.** I tested nine listener profiles. Three were normal. Six were tricky. I read the top 5 songs for each. I also changed the weights and ran the tests again. Below are the details.

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

## 8. Ideas for Improvement  

1. **Add a "no good match" warning.** Say so when the top score is low.
2. **Add mood similarity.** Let "sad" partly match "melancholic" and "wistful." Do the same for close genres.
3. **Mix up the top 5.** Limit how many songs come from one genre, and add more low-energy and rare-genre songs.

---

## 9. Personal Reflection  

**Biggest learning moment.**  
When I doubled energy and halved genre, the same code gave different "taste." Songs moved in and out of the top 5, and a folk fan started getting rock. I had thought of the score as math. Now I see it as a set of choices about what matters. The tricky profiles taught me more than the normal ones. They showed where the model quietly breaks, like the "sad" mood that no song has.

**How AI helped, and when I double-checked it.** 
AI helped me write the profiles, run all of them, and give feedback on my plan and design. But I could not trust it blindly. After the weight change, I checked that scores stayed between 0 and 1 and that the tests passed. I also found that the AI had miscounted the genres. It said 8 genres had one song. The real number was 9. I fixed it. That small mistake reminded me to check every number that goes into a report. The AI is good at drafting. I still have to confirm the facts.

**What surprised me.** 
A few simple rules felt like real recommendations. Chill Lofi gave calm study songs, and the reasons next to each song made it feel like it understood me. But it does not understand anything. It just adds up points. The Gym Hero result showed this best. It kept appearing for people who wanted happy pop, because it is loud and poppy. That looks like a "taste" pattern, but it is really just one song that scores well on the heaviest feature.

**What I would try next.**
- Add a warning when no song is a good match.
- Let similar moods and genres share credit, so "sad" can match "melancholic."
- Limit how many songs from one genre can show up, and add more low-energy songs.
