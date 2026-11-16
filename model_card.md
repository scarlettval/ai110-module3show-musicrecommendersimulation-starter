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

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

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
