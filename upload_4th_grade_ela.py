import json, urllib.request, time

URL = "https://zvffmucghcrqackghhlf.supabase.co/rest/v1/questions"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp2ZmZtdWNnaGNycWFja2doaGxmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY3MjkyNTIsImV4cCI6MjA5MjMwNTI1Mn0.eJHX6LmInRdBd5nt9t_jBJwILGEQ6_SeN6ADorlsWic"

def upload_batch(batch):
    data = json.dumps(batch).encode()
    req = urllib.request.Request(URL, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('apikey', KEY)
    req.add_header('Authorization', f'Bearer {KEY}')
    req.add_header('Prefer', 'return=minimal')
    try:
        with urllib.request.urlopen(req) as r:
            print(f"  Batch of {len(batch)}: HTTP {r.status}")
    except urllib.error.HTTPError as e:
        print(f"  ERROR {e.code}: {e.read().decode()}")
    time.sleep(0.3)

# ── Grade 4 · Reading/ELA ────────────────────────────────────────────

# ── RL: Literary Text ────────────────────────────────────────────────

# Comparing Two Fiction Texts (packet p.12-13)
# Text 1: Marcela (Valentine's Day candy, sick sister Janet)
# Text 2: Jason (soccer ball hog, Coach Terry halftime talk)
rl_comparing_fiction = [
    {"subject":"Reading","domain":"RL","category":"Comparing Fiction Texts","type":"single","grade":4,
     "text":"In Text 1, why was Janet home from school on Valentine's Day?",
     "options":["A She had a dentist appointment","B She did not like parties","C She was sick","D School was cancelled"],
     "correct":["C"],"hint":"The text says Janet 'stayed home from school because she was sick.'","active":True},
    {"subject":"Reading","domain":"RL","category":"Comparing Fiction Texts","type":"single","grade":4,
     "text":"In Text 1, what did Marcela do when she got home from the Valentine's party?",
     "options":["A She shared her candy with Janet","B She walked right past her sister without sharing","C She hid the candy in her room","D She gave the candy to her friends"],
     "correct":["B"],"hint":"The text says 'Marcela walked right past her sister. She had no plan to give her any of the candy.'","active":True},
    {"subject":"Reading","domain":"RL","category":"Comparing Fiction Texts","type":"single","grade":4,
     "text":"In Text 1, who noticed that Marcela was being rude to Janet?",
     "options":["A Janet herself","B Marcela's teacher","C Their mother","D A neighbor"],
     "correct":["C"],"hint":"The text says 'Just then, their mother walked into the kitchen. She noticed that Marcela was being rude.'","active":True},
    {"subject":"Reading","domain":"RL","category":"Comparing Fiction Texts","type":"single","grade":4,
     "text":"In Text 2, why wouldn't Jason pass the ball to his teammates?",
     "options":["A He couldn't see them","B He loved the feeling of scoring goals himself","C His coach told him not to pass","D He was too far from the goal"],
     "correct":["B"],"hint":"The text says 'Jason was so close to scoring a goal, and he loved the feeling when he scored.'","active":True},
    {"subject":"Reading","domain":"RL","category":"Comparing Fiction Texts","type":"single","grade":4,
     "text":"What did Coach Terry tell Jason at halftime in Text 2?",
     "options":["A Jason was the team's best scorer and should keep scoring","B Soccer is a team sport and Jason needed to pass the ball","C Jason should play defense instead of forward","D The team was winning so keep doing the same thing"],
     "correct":["B"],"hint":"Coach Terry said: 'Soccer is a team sport. If you can't be a team player, you can't be on this team.'","active":True},
    {"subject":"Reading","domain":"RL","category":"Comparing Fiction Texts","type":"single","grade":4,
     "text":"How are the main characters in Text 1 (Marcela) and Text 2 (Jason) MOST similar?",
     "options":["A Both play soccer","B Both celebrate Valentine's Day","C Both act selfishly and learn a lesson","D Both share willingly with others"],
     "correct":["C"],"hint":"Both Marcela and Jason act selfishly and then are taught a lesson — Marcela by her mother, Jason by Coach Terry.","active":True},
    {"subject":"Reading","domain":"RL","category":"Comparing Fiction Texts","type":"single","grade":4,
     "text":"By the end of Text 2, how does Jason decide to change his behavior?",
     "options":["A He quits the soccer team","B He decides to start passing the ball to give teammates a chance","C He scores even more goals alone","D He switches to a different sport"],
     "correct":["B"],"hint":"'He would pass the ball to his teammates. It was time to give them a chance to know how great it feels to score a goal.'","active":True},
]

# Reading Comprehension: Drawing Conclusions (packet p.19)
# 5 passages with conclusion questions
rl_drawing_conclusions = [
    {"subject":"Reading","domain":"RL","category":"Drawing Conclusions","type":"single","grade":4,
     "text":"Read this passage and draw a conclusion:\n'Anxious faces stared at the clock. The groom fiddled with his thumbs and combed his hair nervously. Finally, the violinist began a sweet-sounding melody and everyone rose in their seats.'\n\nWhere are these people most likely?",
     "options":["A A concert hall","B A restaurant","C A birthday party","D A wedding"],
     "correct":["D"],"hint":"Clues: 'groom,' violinist playing as people rise — these are classic wedding details.","active":True},
    {"subject":"Reading","domain":"RL","category":"Drawing Conclusions","type":"single","grade":4,
     "text":"Read this passage and draw a conclusion:\n'My bags were ready. The only thing left to pack was the food. My parents were coming too. They always brought enough food to feed an army. I called Tempest to the car. She wagged her tail happily — ready for her first overnight adventure in nature.'\n\nWhere is the family going?",
     "options":["A A hotel","B A birthday party","C A camping or hiking trip","D A shopping mall"],
     "correct":["C"],"hint":"Clues: overnight adventure in nature, food provisions, dog going along — sounds like camping.","active":True},
    {"subject":"Reading","domain":"RL","category":"Drawing Conclusions","type":"single","grade":4,
     "text":"Read this passage and draw a conclusion:\n'Mia wiped sweat from her brow and looked down at the script one last time. She had rehearsed every waking moment. She walked on stage left, determined to show them just how hard she had worked.'\n\nWhat did Mia rehearse?",
     "options":["A A speech for class","B A play or theater performance","C A gymnastics routine","D A musical instrument"],
     "correct":["B"],"hint":"Clues: script, stage, walking on stage left — all point to a play or performance.","active":True},
    {"subject":"Reading","domain":"RL","category":"Drawing Conclusions","type":"single","grade":4,
     "text":"Read this passage and draw a conclusion:\n'The buses raced around the neighborhood making an unfamiliar sound after the long, blistering hot summer. Kids with shiny new backpacks put smiles on parents' faces. The nervous chatter at the bus stop eased some of the tension.'\n\nWhat time of year is it most likely?",
     "options":["A Winter break","B Spring break","C The start of a new school year in fall","D Summer vacation"],
     "correct":["C"],"hint":"Clues: after a long hot summer, new backpacks, buses, nervous kids — these signal the first day back to school.","active":True},
    {"subject":"Reading","domain":"RL","category":"Drawing Conclusions","type":"single","grade":4,
     "text":"Read this passage and draw a conclusion:\n'Santiago was going to have a blast, even if he didn't know anyone. He stood at the front door and took a deep breath. Earlier that morning he'd wrapped his gift in superhero wrapping paper and was sure his cousin would love it. He rang the bell.'\n\nWhy did Santiago have a present?",
     "options":["A It was his own birthday","B He was going to a birthday party","C He was delivering a package","D He found it on the street"],
     "correct":["B"],"hint":"Clues: gift wrapped in superhero paper for his cousin, ringing a doorbell, 'going to have a blast' — he's attending a birthday party.","active":True},
]

# Short and Sweet Summaries (packet p.5) — Elias and the project
rl_summaries = [
    {"subject":"Reading","domain":"RL","category":"Summarizing","type":"single","grade":4,
     "text":"Read the passage about Elias. What did Elias do INSTEAD of starting his social studies project?\n(Passage: Elias had a big project due. He had two weeks but put it off — he went skateboarding, played video games, and even cleaned his room to avoid it.)",
     "options":["A He read books about the topic","B He went skateboarding and played video games with his brother","C He asked his mom for help","D He worked on other homework first"],
     "correct":["B"],"hint":"The passage says Elias 'went skateboarding with his friends at the park, and he played video games with his brother.'","active":True},
    {"subject":"Reading","domain":"RL","category":"Summarizing","type":"single","grade":4,
     "text":"How did Elias feel when he turned in his finished project the next day?",
     "options":["A Proud and excited about his work","B Happy that he finished on time","C Not proud — he believed it would have been much better if he had spent more time","D Angry at his teacher for assigning the project"],
     "correct":["C"],"hint":"The passage says: 'Elias was not proud of the work he had completed. He believed it would have been much better if he spent more time on it.'","active":True},
    {"subject":"Reading","domain":"RL","category":"Summarizing","type":"single","grade":4,
     "text":"What is the MAIN lesson of the story about Elias?",
     "options":["A Projects are always boring and take too long","B You should start your work early and be responsible","C Friends are more important than school","D Moms always make you do homework"],
     "correct":["B"],"hint":"Elias wishes he had 'been more responsible.' The story is about the consequences of procrastination.","active":True},
    {"subject":"Reading","domain":"RL","category":"Summarizing","type":"single","grade":4,
     "text":"Which strategy does the Short and Sweet Summaries worksheet teach you to use when writing a fiction summary?",
     "options":["A Beginning, Middle, End","B Somebody, Wanted, But, So, Then","C Compare and Contrast","D Main Idea and Details"],
     "correct":["B"],"hint":"The worksheet says: 'Use the writing strategy of Somebody Wanted But So Then to help you write a short fiction summary!'","active":True},
]

# ── RI: Informational Text ───────────────────────────────────────────

# Comparing Two Nonfiction Texts: A Female Freedom Fighter (Harriet Tubman) (packet p.24-25)
ri_harriet_tubman = [
    {"subject":"Reading","domain":"RI","category":"Comparing Nonfiction Texts","type":"single","grade":4,
     "text":"According to Text 1, in what year did Harriet Tubman escape slavery and reach Pennsylvania?",
     "options":["A 1820","B 1849","C 1857","D 1863"],
     "correct":["B"],"hint":"Text 1 says: 'Harriet Tubman was born a slave in Maryland around 1820. In 1849, she escaped to Pennsylvania.'","active":True},
    {"subject":"Reading","domain":"RI","category":"Comparing Nonfiction Texts","type":"single","grade":4,
     "text":"What was the Underground Railroad?",
     "options":["A An actual underground train that carried slaves north","B A secret network of people and routes to help enslaved people escape to freedom","C A military railroad run by the Union Army","D A company that built tunnels underground"],
     "correct":["B"],"hint":"Text 1: 'The Underground Railroad was a network, or group, of people who worked together to bring slaves to freedom... a secret route, or path, that slaves could follow.'","active":True},
    {"subject":"Reading","domain":"RI","category":"Comparing Nonfiction Texts","type":"single","grade":4,
     "text":"According to Text 1, how many South Carolina slaves did Harriet Tubman help free in 1863?",
     "options":["A 19","B 70","C 750","D 1,820"],
     "correct":["C"],"hint":"Text 1 says: 'In 1863, she led a raid that freed 750 South Carolina slaves.'","active":True},
    {"subject":"Reading","domain":"RI","category":"Comparing Nonfiction Texts","type":"single","grade":4,
     "text":"What does the word 'conductor' mean in the context of the Underground Railroad?",
     "options":["A Someone who drives a train","B A music director","C A person who guided enslaved people from place to place along the route","D A person who owned safe houses"],
     "correct":["C"],"hint":"Text 1: 'The people who guided the slaves from place to place were called conductors.'","active":True},
    {"subject":"Reading","domain":"RI","category":"Comparing Nonfiction Texts","type":"single","grade":4,
     "text":"According to Text 2, why was running away from slavery so dangerous in the 1800s?",
     "options":["A There were no safe houses anywhere","B The journey was too cold","C If caught, owners would hurt and punish the runaway slave","D There was no Underground Railroad yet"],
     "correct":["C"],"hint":"Text 2: 'Running away was dangerous for slaves in the 1800s. If a runaway slave was found, their owners would often hurt them and punish them.'","active":True},
    {"subject":"Reading","domain":"RI","category":"Comparing Nonfiction Texts","type":"single","grade":4,
     "text":"What three roles did Harriet Tubman serve in the Union Army according to Text 2?",
     "options":["A General, soldier, and spy","B Cook, nurse, and spy","C Teacher, nurse, and soldier","D Cook, politician, and teacher"],
     "correct":["B"],"hint":"Text 2: 'she worked for the Union Army as a cook, a nurse, and even a spy.'","active":True},
    {"subject":"Reading","domain":"RI","category":"Comparing Nonfiction Texts","type":"single","grade":4,
     "text":"What topic do BOTH Text 1 and Text 2 have in common?",
     "options":["A Harriet Tubman's childhood birthday celebrations","B The Union Army's battles","C Harriet Tubman's role in helping enslaved people escape and the Underground Railroad","D John Tubman's life story"],
     "correct":["C"],"hint":"Both texts describe Harriet Tubman helping enslaved people escape and her connection to the Underground Railroad.","active":True},
    {"subject":"Reading","domain":"RI","category":"Comparing Nonfiction Texts","type":"single","grade":4,
     "text":"According to Text 2, where did Harriet Tubman go after escaping slavery to find work?",
     "options":["A New York","B Washington D.C.","C Philadelphia","D Boston"],
     "correct":["C"],"hint":"Text 2: 'She made it all the way to Philadelphia, where she was able to find work.'","active":True},
]

# Author's Viewpoint vs. My Viewpoint (packet p.31-32)
# Passages: manatees, soda, recess
ri_authors_viewpoint = [
    {"subject":"Reading","domain":"RI","category":"Author's Viewpoint","type":"single","grade":4,
     "text":"Read this passage:\n'The West Indian manatee has been listed as an endangered species... Federal and state laws protect the manatee. Scientists are working to find ways to help the manatee survive.'\n\nWhat is the author's viewpoint about manatees?",
     "options":["A There are too many manatees in the ocean","B Manatees are endangered and people should work to protect them","C Manatees are dangerous to humans","D Scientists should stop studying manatees"],
     "correct":["B"],"hint":"The author mentions laws protecting manatees and scientists working to help them survive — the viewpoint is that manatees need protection.","active":True},
    {"subject":"Reading","domain":"RI","category":"Author's Viewpoint","type":"single","grade":4,
     "text":"Which sentence from the manatee passage BEST shows the author believes manatees need help?",
     "options":["A 'It is hard for scientists to know how many West Indian manatees there are.'","B 'They estimate between 2,000 to 5,000.'","C 'Federal and state laws protect the manatee. Scientists are working to find ways to help the manatee survive.'","D 'Many die because of accidents with ships or other human causes.'"],
     "correct":["C"],"hint":"This sentence shows active efforts to save manatees, which supports the viewpoint that they need and deserve protection.","active":True},
    {"subject":"Reading","domain":"RI","category":"Author's Viewpoint","type":"single","grade":4,
     "text":"Read this passage:\n'Did you know how bad soda is for your health? Soda has a lot of calories and too much sugar. Soda has been linked to diabetes and obesity. Stick to water for a healthier life!'\n\nWhat is the author's viewpoint about soda?",
     "options":["A Soda is a fine treat in moderation","B Soda tastes great and is refreshing","C Soda is unhealthy and people should drink water instead","D Sugar in soda is not really a problem"],
     "correct":["C"],"hint":"The author lists soda's health problems and ends with 'Stick to water for a healthier life!' — clearly against drinking soda.","active":True},
    {"subject":"Reading","domain":"RI","category":"Author's Viewpoint","type":"single","grade":4,
     "text":"Which sentence from the soda passage MOST DIRECTLY shows the author's viewpoint?",
     "options":["A 'Soda is a drink that can taste very good, especially on a hot day.'","B 'Soda has a lot of calories, and it has too much sugar.'","C 'Stick to water for a healthier life!'","D 'Did you know how bad soda is for your health?'"],
     "correct":["C"],"hint":"'Stick to water for a healthier life!' is the author's direct recommendation — the clearest statement of their viewpoint.","active":True},
    {"subject":"Reading","domain":"RI","category":"Author's Viewpoint","type":"single","grade":4,
     "text":"Read this passage:\n'Recess helps kids focus and stay on-task better when they are in the classroom. Going outside for recess is good for your health... Kids get to run around, which is good for physical health. Recess is a great time for kids to play together and build relationships.'\n\nWhat is the author's viewpoint about recess?",
     "options":["A Recess takes away important learning time","B Recess is only helpful for kids who enjoy sports","C Recess is beneficial for kids' focus, health, and social development","D Schools should reduce recess to add more classroom time"],
     "correct":["C"],"hint":"The author lists multiple benefits of recess: better focus, physical health, and building relationships.","active":True},
    {"subject":"Reading","domain":"RI","category":"Author's Viewpoint","type":"single","grade":4,
     "text":"'Point of view' or 'viewpoint' is best described as:",
     "options":["A The setting of a story","B The way the author or reader feels about the topic or events in a text","C The main character's name","D The beginning of a story"],
     "correct":["B"],"hint":"The worksheet defines it: 'Point of view or viewpoint is the way we feel about the topic or events in a piece of text.'","active":True},
]

# ── L: Language ──────────────────────────────────────────────────────

# Their, There, They're (packet p.15)
l_their_there_theyre = [
    {"subject":"Reading","domain":"L","category":"Their, There, They're","type":"single","grade":4,
     "text":"Choose the correct word:\n'\"_______ up first,\" I told the team. Everyone ran out to _______ places on the field.'",
     "options":["A They're / their","B Their / there","C There / they're","D Their / they're"],
     "correct":["A"],"hint":"They're = they are (up first). Their = possessive (belonging to them — their places).","active":True},
    {"subject":"Reading","domain":"L","category":"Their, There, They're","type":"single","grade":4,
     "text":"Choose the correct word:\n'The air was perfectly still. _______ wasn't the slightest breeze.'",
     "options":["A Their","B They're","C There","D Theyre"],
     "correct":["C"],"hint":"There = an adverb used to indicate existence ('there was/wasn't').","active":True},
    {"subject":"Reading","domain":"L","category":"Their, There, They're","type":"single","grade":4,
     "text":"Choose the correct word:\n'_______ were still three more balls to go.'",
     "options":["A Their","B They're","C There","D Thier"],
     "correct":["C"],"hint":"'There were' uses 'there' as an adverb indicating existence.","active":True},
    {"subject":"Reading","domain":"L","category":"Their, There, They're","type":"single","grade":4,
     "text":"Choose the correct word:\n'From the stands I heard chanting: \"_______ gonna lose! We're gonna win!\"'",
     "options":["A Their","B There","C They're","D Theyr'e"],
     "correct":["C"],"hint":"They're = they are (they are going to lose).","active":True},
    {"subject":"Reading","domain":"L","category":"Their, There, They're","type":"single","grade":4,
     "text":"Choose the correct word:\n'I looked at the opposite team leaning against the fence. _______ faces were tense with determination.'",
     "options":["A They're","B There","C Their","D Thier"],
     "correct":["C"],"hint":"Their = possessive (the faces belonging to them).","active":True},
    {"subject":"Reading","domain":"L","category":"Their, There, They're","type":"single","grade":4,
     "text":"Choose the correct word:\n'I turned to my team, and saw smiles on _______ faces.'",
     "options":["A there","B they're","C their","D thier"],
     "correct":["C"],"hint":"Their = possessive (the faces belonging to them — my teammates).","active":True},
    {"subject":"Reading","domain":"L","category":"Their, There, They're","type":"single","grade":4,
     "text":"Which sentence uses 'there' correctly?",
     "options":["A There going to win the big game","B I love there new puppy","C Put the books over there on the shelf","D There team practiced all week"],
     "correct":["C"],"hint":"'Over there' uses 'there' correctly as an adverb of location.","active":True},
    {"subject":"Reading","domain":"L","category":"Their, There, They're","type":"single","grade":4,
     "text":"Which sentence uses 'their' correctly?",
     "options":["A Their going to be late for school","B Put the chairs over their","C The students forgot their homework again","D Their is no practice today"],
     "correct":["C"],"hint":"'Their homework' correctly uses 'their' as a possessive pronoun (belonging to the students).","active":True},
    {"subject":"Reading","domain":"L","category":"Their, There, They're","type":"single","grade":4,
     "text":"Which sentence uses 'they're' correctly?",
     "options":["A They're dog is very friendly","B I really love they're house","C They're going to the movies tonight","D Over they're is the park"],
     "correct":["C"],"hint":"'They're going' = 'they are going.' Only this option expands correctly to 'they are.'","active":True},
    {"subject":"Reading","domain":"L","category":"Their, There, They're","type":"single","grade":4,
     "text":"'Their' is a _______ pronoun — it shows something belongs to a group of people.",
     "options":["A contraction","B adverb","C possessive","D verb"],
     "correct":["C"],"hint":"'Their' shows ownership/possession, just like 'his,' 'her,' and 'its.'","active":True},
    {"subject":"Reading","domain":"L","category":"Their, There, They're","type":"single","grade":4,
     "text":"'They're' is a _______ — a shortened form of two words joined together.",
     "options":["A possessive pronoun","B adverb","C verb","D contraction"],
     "correct":["D"],"hint":"They're = they + are. The apostrophe replaces the letter 'a.'","active":True},
]

# Its or It's (packet p.21)
l_its_its = [
    {"subject":"Reading","domain":"L","category":"Its or It's","type":"single","grade":4,
     "text":"Choose the correct word:\n'The tiger licked _______ paw.'",
     "options":["A its","B it's","C their","D its'"],
     "correct":["A"],"hint":"'Its' (no apostrophe) is a possessive pronoun — the paw belonging to the tiger.","active":True},
    {"subject":"Reading","domain":"L","category":"Its or It's","type":"single","grade":4,
     "text":"Choose the correct word:\n'I wonder if _______ going to rain tomorrow.'",
     "options":["A its","B it's","C their","D its'"],
     "correct":["B"],"hint":"'It's' = it is. 'I wonder if it is going to rain' — the contraction fits here.","active":True},
    {"subject":"Reading","domain":"L","category":"Its or It's","type":"single","grade":4,
     "text":"Choose the correct word:\n'_______ time to go to school.'",
     "options":["A Its","B It's","C Their","D There"],
     "correct":["B"],"hint":"'It's time' = 'it is time.' The apostrophe shows the contraction of 'it is.'","active":True},
    {"subject":"Reading","domain":"L","category":"Its or It's","type":"single","grade":4,
     "text":"Choose the correct word:\n'My cat and _______ kittens are taking a nap.'",
     "options":["A its","B it's","C their","D they're"],
     "correct":["A"],"hint":"'Its kittens' = the kittens belonging to the cat. No apostrophe for possessive 'its.'","active":True},
    {"subject":"Reading","domain":"L","category":"Its or It's","type":"single","grade":4,
     "text":"Choose the correct word:\n'_______ going to be a long walk to the train.'",
     "options":["A Its","B It's","C Their","D There"],
     "correct":["B"],"hint":"'It's going to be' = 'it is going to be.' Use the contraction.","active":True},
    {"subject":"Reading","domain":"L","category":"Its or It's","type":"single","grade":4,
     "text":"Choose the correct word:\n'Your puppy is so cute — what's _______ name?'",
     "options":["A its","B it's","C their","D there"],
     "correct":["A"],"hint":"The name belonging to the puppy — 'its name' uses the possessive 'its' (no apostrophe).","active":True},
    {"subject":"Reading","domain":"L","category":"Its or It's","type":"single","grade":4,
     "text":"'Its' (without an apostrophe) is a _______ pronoun — it shows something belongs to it.",
     "options":["A contraction","B verb","C possessive","D adverb"],
     "correct":["C"],"hint":"'Its' works like 'his' and 'her' — it shows ownership. Possessive pronouns never use apostrophes.","active":True},
    {"subject":"Reading","domain":"L","category":"Its or It's","type":"single","grade":4,
     "text":"'It's' (with an apostrophe) is a _______ — a shortened form of 'it is.'",
     "options":["A possessive pronoun","B contraction","C verb","D adverb"],
     "correct":["B"],"hint":"The apostrophe replaces the letter 'i' in 'is.' It's = it is.","active":True},
    {"subject":"Reading","domain":"L","category":"Its or It's","type":"single","grade":4,
     "text":"'Have you seen my toy? _______ not in _______ box.'",
     "options":["A It's / its","B Its / it's","C It's / it's","D Its / its"],
     "correct":["A"],"hint":"'It's not in its box.' = 'It is not in the box belonging to it.' First blank: contraction. Second blank: possessive.","active":True},
    {"subject":"Reading","domain":"L","category":"Its or It's","type":"single","grade":4,
     "text":"Which sentence uses 'it's' correctly?",
     "options":["A The dog chased it's tail","B It's a beautiful day outside","C The bird flew back to it's nest","D The cat licked it's paw"],
     "correct":["B"],"hint":"'It's a beautiful day' = 'It is a beautiful day.' The other options misuse 'it's' where 'its' (possessive) is needed.","active":True},
]

all_ela = (
    rl_comparing_fiction +
    rl_drawing_conclusions +
    rl_summaries +
    ri_harriet_tubman +
    ri_authors_viewpoint +
    l_their_there_theyre +
    l_its_its
)

print(f"Total Grade 4 ELA questions: {len(all_ela)}")
by_domain = {}
for q in all_ela:
    by_domain[q['domain']] = by_domain.get(q['domain'], 0) + 1
for d, n in sorted(by_domain.items()):
    print(f"  {d}: {n}")
print()

print("Uploading Grade 4 ELA questions...")
for i in range(0, len(all_ela), 25):
    batch = all_ela[i:i+25]
    upload_batch(batch)

print("Done!")
