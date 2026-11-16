# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Intended Use

**Goal:** Suggest the top 5 songs from a small catalog that best fit one listener's taste. The listener gives a favorite genre, a favorite mood, a target energy (0-1), and whether they like acoustic sound.

**Intended use:** A classroom project for learning how a simple, rule-based recommender works and where it goes wrong.

**Not intended for:** Real users or a real music app. The catalog is tiny, the songs are made up, and it knows nothing about lyrics, listening history, or how tastes change over time. It should not be used to judge what music is "good" or to make decisions about artists.

---

## 3. How the Model Works

Every song gets points for how well it matches the listener, out of 5:

- **Same genre:** +2 points.
- **Same mood:** +1 point.
- **Close energy:** up to +1.5 points. The closer the song's energy is to the target, the more points.
- **Acoustic fit:** up to +0.5 points. Acoustic songs earn more if the listener likes acoustic; non-acoustic songs earn more if they don't.

The songs are sorted by score, and the top 5 are shown with a short "why" list. Genre and mood must match exactly, but capital letters and extra spaces are ignored. Ties go to the song with the lower ID, so the results are always the same.

---

## 4. Data

- **20 songs** in `data/songs.csv`. The starter file had 10; I added 10 more to cover more genres and moods.
- **17 genres and 16 moods**, but most have only one song. Lofi has 3 songs; pop has 2.
- **Features:** title, artist, genre, mood, energy, tempo, valence, danceability, acousticness. The model only uses genre, mood, energy, and acousticness.
- **Limits:** Few middle-energy songs (only 3 between 0.45 and 0.70). Loud songs are almost never acoustic. No lyrics, languages, release years, or popularity.

---

## 5. Strengths

- Works well when the listener's genre has several songs. Chill Lofi got 3 strong lofi picks.
- Clear, opposite tastes get clearly different lists. High-Energy Pop and Chill Lofi share no songs.
- Every result explains itself, so it is easy to see why a song was picked.
- It handles messy input like "  Indie POP " correctly.

---

## 6. Limitations and Bias

The biggest weakness is a "loud song" filter bubble: 15 of the 17 genres have only one song, so once a listener's genre match is used up, the rest of their top 5 is picked almost entirely by energy. Because the catalog has 8 songs above 0.75 energy but only 3 in the middle range, the same few loud songs fill most lists, while 5 of the 20 songs (Velvet Hours, Hollow Pines, Dusty Backroads, Quiet Harbor Nocturne, Island Time) were never recommended to anyone. The "likes acoustic" setting does not break the bubble, because in this catalog loud songs are almost never acoustic, so it mostly repeats what the energy setting already says. As a result, a listener who wants energetic acoustic music (like folk-punk) or quiet electronic music is basically ignored.

---

## 7. Evaluation

**Profiles I tested.** I ran 8 taste profiles through the recommender and read the top 5 for each:

- 3 standard profiles: **High-Energy Pop** (pop, happy, energy 0.85, not acoustic), **Chill Lofi** (lofi, chill, 0.40, acoustic), and **Deep Intense Rock** (rock, intense, 0.90, not acoustic).
- 5 "tricky" profiles meant to confuse the scoring: **Energetic but Sad** (blues, sad, 0.90), **Unknown Genre/Mood** (opera, triumphant: neither exists in the catalog), **Acoustic Metalhead** (metal, angry, 0.95, but likes acoustic), **Energy Out of Range** (edm, euphoric, energy 1.5 on a 0-1 scale), and **Messy Casing / Near-Miss** ("  Indie POP ", "HAPPY", 0.80).

I checked whether the #1 song fit the profile, whether the rest of the list made sense, and whether the "Why" reasons matched the score. I also ran one experiment: turning the mood check off. Three profiles changed order, and every change made the list fit the user worse (for example, a sad blues song showed up for the Chill Lofi listener), so I turned mood back on.

**What surprised me**

- **Neon Petals showed up for 6 of my 8 listeners without ever matching what they asked for.** It is a k-pop song with an "energetic" mood, and none of my profiles asked for k-pop or that mood. It still landed at #4 or #5 for High-Energy Pop, Deep Intense Rock, Energetic but Sad, Acoustic Metalhead, Energy Out of Range, and Messy Casing, always with only two reasons listed: its energy (0.88) was close to the target, and it is not very acoustic. In plain terms: once a listener's genre runs out of songs, the system fills the list with whatever is loud enough, so a song that is loud and "average" ends up recommended to people with very different tastes.
- In "Energetic but Sad", I expected the energy conflict to cause trouble, but the quiet blues song still won easily because genre plus mood (3 points) outweighs a big energy miss.

**Comparing pairs of profiles**

- **High-Energy Pop vs Chill Lofi:** The two lists have no songs in common. Pop got loud, non-acoustic songs (energy 0.76-0.93) and lofi got quiet, acoustic ones (energy 0.28-0.42). This makes sense: the two profiles ask for opposite energy and opposite sound, so they pull from opposite ends of the catalog.
- **High-Energy Pop vs Deep Intense Rock:** They share 3 of their 5 songs (Gym Hero, Neon Petals, Storm Runner); only the #1 pick really differs. Gym Hero is #2 in both lists, but for different reasons: for pop because of the genre, for rock because its mood is "intense". This makes sense, since both ask for loud, non-acoustic music, but it shows the loud-song filter bubble.
- **Chill Lofi vs Deep Intense Rock:** Lofi's top 3 all score close to the max because the catalog has 3 lofi songs, while rock drops from 4.93 at #1 to 2.93 at #2 because there is only one rock song. Both lists are reasonable, but the lofi listener simply gets a better list because their genre has more songs.
- **Deep Intense Rock vs Energetic but Sad:** Both ask for 0.90 energy and non-acoustic sound, so #2-#5 are almost the same loud songs. The only real difference is #1, where the sad profile gets Rainy Window, the catalog's one blues/sad song. This makes sense: below the top spot, both profiles are really just asking for loud, non-acoustic music.
- **Chill Lofi vs Unknown Genre/Mood:** Both like acoustic, mid-low energy music, so they get many of the same quiet songs (Focus Flow, Midnight Coding, Library Rain, Coffee Shop Stories). The difference is that the unknown profile's scores are all low and nearly tied (1.70-1.75), because without a genre or mood match only small energy differences decide the order. This makes sense, but the system never tells the user that "opera" isn't in the catalog.
- **Deep Intense Rock vs Acoustic Metalhead:** Both want very loud music and get mostly the same songs (Festival Heat, Gym Hero, Storm Runner, Neon Petals). The acoustic preference only changes the scores (about +0.45 per song for rock, +0.01 to +0.06 for the metalhead), not which songs appear. This shows that an acoustic preference is quietly ignored when it conflicts with energy, because no loud song in the catalog is acoustic.
- **Deep Intense Rock vs Energy Out of Range (1.5):** The same loud songs fill both lists, but every score in the out-of-range profile is lower (about 1.0-1.2 for the songs after #1, vs about 1.9 for rock). The order still goes from loudest to quietest, so the system accidentally does what the user probably meant ("as loud as possible"), but the scores look worse than the songs deserve.
- **High-Energy Pop vs Messy Casing / Near-Miss (indie pop):** Rooftop Lights jumps from #3 to #1, Sunrise City falls from #1 to #2, and Gym Hero disappears. This makes sense: the messy capitals and spaces were cleaned up correctly, so "indie pop" matched. But it also shows that "pop" and "indie pop" are treated as completely separate genres.

---

## 8. Future Work

- **Give partial credit for related genres**, so "pop", "indie pop", and "k-pop" are treated as close instead of totally different.
- **Add more songs, especially middle-energy and loud-acoustic ones**, so lists are not filled by the same few loud songs.
- **Check the input**: keep energy between 0 and 1, and warn when a genre or mood is not in the catalog.

---

## 9. Personal Reflection

**Biggest learning moment:** Turning off the mood check. I expected the results to just shift, but every change made the lists worse. That showed me that even a 1-point feature can hold the rankings together.

**Using AI tools:** AI helped me write the profiles, run the experiments, and draft this card quickly. I still had to double-check its claims against the actual output. For example, it first said "Gym Hero" kept showing up for Happy Pop, but in my results it only appeared once, at #2, so I replaced that example with one I could see in the data.

**What surprised me:** Four simple rules and some addition already "feel" like a real recommender. The "why" lines make the picks seem thoughtful, even when a song is only there because it is loud.

**What I'd try next:** Use more features, like tempo and valence, and add some variety to the top 5 so one artist or energy level doesn't take over the list.
