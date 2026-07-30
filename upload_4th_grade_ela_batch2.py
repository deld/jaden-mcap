# Tracked by: https://github.com/deld/jaden-mcap/issues/13
# Run this script from an environment with network access to Supabase, then close the issue.
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

# ── Grade 4 · Reading/ELA · Batch 2 ──────────────────────────────────

# ── RL: Literary Text ────────────────────────────────────────────────

rl_story_elements = [
    {"subject":"Reading","domain":"RL","category":"Story Elements","type":"single","grade":4,
     "text":"Read: 'Deep in the forest, a young fox named Ruma searched for her missing kit under the light of a full moon.'\n\nWho is the main character in this passage?",
     "options":["A Ruma","B The kit","C The moon","D The forest"],
     "correct":["A"],"hint":"Ruma is the fox doing the searching — she is the one the story focuses on.","active":True},
    {"subject":"Reading","domain":"RL","category":"Story Elements","type":"single","grade":4,
     "text":"Read: 'Deep in the forest, a young fox named Ruma searched for her missing kit under the light of a full moon.'\n\nWhere does this story take place?",
     "options":["A In a city at noon","B In a forest at night","C In a desert at sunrise","D In a classroom"],
     "correct":["B"],"hint":"The setting clues are 'forest' and 'full moon,' which shows it is nighttime.","active":True},
    {"subject":"Reading","domain":"RL","category":"Story Elements","type":"single","grade":4,
     "text":"The problem a character faces in a story, which must be solved, is called the story's ___.",
     "options":["A setting","B resolution","C conflict","D theme"],
     "correct":["C"],"hint":"The conflict is the main problem or struggle in a story.","active":True},
    {"subject":"Reading","domain":"RL","category":"Story Elements","type":"single","grade":4,
     "text":"The part of a story where the conflict is finally solved is called the ___.",
     "options":["A introduction","B rising action","C resolution","D setting"],
     "correct":["C"],"hint":"The resolution comes at the end, after the problem has been worked out.","active":True},
    {"subject":"Reading","domain":"RL","category":"Story Elements","type":"single","grade":4,
     "text":"Read: 'Marcus opened his eyes. Bright morning sunlight streamed through the tent. He smelled bacon cooking over a campfire.'\n\nWhat is the setting of this passage?",
     "options":["A A campsite in the morning","B A kitchen at night","C A hotel room","D A school cafeteria"],
     "correct":["A"],"hint":"Clues like 'tent,' 'campfire,' and 'morning sunlight' point to a campsite in the morning.","active":True},
]

rl_theme = [
    {"subject":"Reading","domain":"RL","category":"Theme","type":"single","grade":4,
     "text":"In a fable, the tortoise beats the hare in a race because the hare stops to nap while the tortoise keeps moving steadily. What is the theme of this fable?",
     "options":["A Racing is dangerous","B Slow and steady wins the race","C Hares are faster than tortoises","D Naps make you stronger"],
     "correct":["B"],"hint":"The tortoise wins by staying steady and not giving up, even though it is slower.","active":True},
    {"subject":"Reading","domain":"RL","category":"Theme","type":"single","grade":4,
     "text":"A story shows a character who lies to a friend and then loses that friend's trust. What lesson, or theme, does this story most likely teach?",
     "options":["A Honesty is important in friendships","B Friends always forgive lies","C Lying helps you avoid trouble","D It's fine to lie sometimes"],
     "correct":["A"],"hint":"Losing trust after lying teaches readers that honesty matters in friendships.","active":True},
    {"subject":"Reading","domain":"RL","category":"Theme","type":"single","grade":4,
     "text":"Which sentence BEST states a theme (a life lesson), rather than just a plot event?",
     "options":["A The boy ran to school","B Hard work leads to success","C It was raining outside","D The dog barked at the mailman"],
     "correct":["B"],"hint":"A theme is a general lesson about life, not a specific event that happened.","active":True},
    {"subject":"Reading","domain":"RL","category":"Theme","type":"single","grade":4,
     "text":"A theme is best described as:",
     "options":["A The setting of the story","B A lesson or message about life that the story teaches","C The name of the main character","D The order of events in the story"],
     "correct":["B"],"hint":"Theme is the deeper meaning or lesson readers take away from a story.","active":True},
    {"subject":"Reading","domain":"RL","category":"Theme","type":"single","grade":4,
     "text":"In a story, a shy girl practices her speech every night and finally gives a great presentation to the class. What is the most likely theme?",
     "options":["A Practice and preparation help you succeed","B Public speaking is impossible","C Shy people should avoid speeches","D Speeches are boring"],
     "correct":["A"],"hint":"Her hard work and practice led to her success — that's the lesson.","active":True},
]

rl_figurative_language = [
    {"subject":"Reading","domain":"RL","category":"Figurative Language","type":"single","grade":4,
     "text":"'The classroom was a zoo after the substitute left.' This sentence is an example of a ___.",
     "options":["A simile","B metaphor","C personification","D idiom"],
     "correct":["B"],"hint":"A metaphor directly compares two things without using 'like' or 'as' — the classroom IS a zoo.","active":True},
    {"subject":"Reading","domain":"RL","category":"Figurative Language","type":"single","grade":4,
     "text":"'Her smile was as bright as the sun.' This sentence uses a ___.",
     "options":["A metaphor","B simile","C personification","D hyperbole"],
     "correct":["B"],"hint":"A simile compares two things using 'like' or 'as.'","active":True},
    {"subject":"Reading","domain":"RL","category":"Figurative Language","type":"single","grade":4,
     "text":"'The wind whispered through the trees.' This sentence is an example of ___, which gives human qualities to something that is not human.",
     "options":["A a simile","B a metaphor","C personification","D an idiom"],
     "correct":["C"],"hint":"Wind cannot really whisper — that's a human action being given to something nonhuman.","active":True},
    {"subject":"Reading","domain":"RL","category":"Figurative Language","type":"single","grade":4,
     "text":"What does the idiom 'it's raining cats and dogs' mean?",
     "options":["A Animals are falling from the sky","B It is raining very hard","C It is a sunny day","D Cats and dogs are playing outside"],
     "correct":["B"],"hint":"This idiom is a figure of speech meaning heavy rain — not literal animals falling.","active":True},
    {"subject":"Reading","domain":"RL","category":"Figurative Language","type":"single","grade":4,
     "text":"'Break a leg!' said before a performance is an idiom that means:",
     "options":["A Be careful not to fall","B Good luck","C You will get hurt","D Stop performing"],
     "correct":["B"],"hint":"This idiom is a traditional way to wish a performer good luck.","active":True},
]

# ── RI: Informational Text ───────────────────────────────────────────

ri_main_idea = [
    {"subject":"Reading","domain":"RI","category":"Main Idea & Details","type":"single","grade":4,
     "text":"Read: 'Bees are important pollinators. They carry pollen from flower to flower, helping plants make fruits and seeds. Without bees, many crops would not grow.'\n\nWhat is the main idea of this passage?",
     "options":["A Bees like flowers","B Bees are important because they help plants grow through pollination","C Bees make honey in hives","D Crops grow without any help"],
     "correct":["B"],"hint":"The whole passage explains why bees matter — because they help plants grow.","active":True},
    {"subject":"Reading","domain":"RI","category":"Main Idea & Details","type":"single","grade":4,
     "text":"Read: 'Bees are important pollinators. They carry pollen from flower to flower, helping plants make fruits and seeds. Without bees, many crops would not grow.'\n\nWhich sentence from the passage is a supporting DETAIL rather than the main idea?",
     "options":["A Bees are important pollinators","B They carry pollen from flower to flower, helping plants make fruits and seeds","C Without bees, many crops would not grow","D Bees are the most important insect"],
     "correct":["B"],"hint":"This sentence explains HOW bees help, which supports the bigger main idea.","active":True},
    {"subject":"Reading","domain":"RI","category":"Main Idea & Details","type":"single","grade":4,
     "text":"Read: 'Volcanoes form when melted rock, called magma, pushes up through cracks in the Earth's crust. When it reaches the surface, it is called lava.'\n\nWhat is this passage mostly about?",
     "options":["A Why the Earth has cracks","B How volcanoes form","C The difference between rocks and minerals","D Where lava comes from in oceans"],
     "correct":["B"],"hint":"The passage explains the process of how magma becomes lava and forms volcanoes.","active":True},
    {"subject":"Reading","domain":"RI","category":"Main Idea & Details","type":"single","grade":4,
     "text":"The topic sentence of a paragraph usually tells you the ___.",
     "options":["A smallest detail","B main idea","C author's name","D last event"],
     "correct":["B"],"hint":"A topic sentence introduces what the paragraph is mainly about.","active":True},
    {"subject":"Reading","domain":"RI","category":"Main Idea & Details","type":"single","grade":4,
     "text":"Details in a nonfiction text usually ___.",
     "options":["A replace the main idea","B support and explain the main idea","C contradict the main idea","D are always found in the title"],
     "correct":["B"],"hint":"Details give evidence and examples that back up the main idea.","active":True},
]

ri_text_structure = [
    {"subject":"Reading","domain":"RI","category":"Text Structure","type":"single","grade":4,
     "text":"A passage that explains what happened and why it happened uses a ___ text structure.",
     "options":["A sequence","B cause and effect","C compare and contrast","D description"],
     "correct":["B"],"hint":"Cause and effect structure connects an event (effect) to its reason (cause).","active":True},
    {"subject":"Reading","domain":"RI","category":"Text Structure","type":"single","grade":4,
     "text":"A passage that tells events in the order they happened uses a ___ text structure.",
     "options":["A cause and effect","B compare and contrast","C sequence","D problem and solution"],
     "correct":["C"],"hint":"Sequence structure lists events in time order, often using words like 'first' and 'then.'","active":True},
    {"subject":"Reading","domain":"RI","category":"Text Structure","type":"single","grade":4,
     "text":"A passage that shows how two things are alike and different uses a ___ text structure.",
     "options":["A sequence","B compare and contrast","C cause and effect","D description"],
     "correct":["B"],"hint":"Compare and contrast structure examines similarities and differences.","active":True},
    {"subject":"Reading","domain":"RI","category":"Text Structure","type":"single","grade":4,
     "text":"Read: 'First, the caterpillar hatches from an egg. Next, it eats leaves and grows. Then, it forms a chrysalis. Finally, it emerges as a butterfly.'\n\nThis passage uses which text structure?",
     "options":["A cause and effect","B compare and contrast","C sequence","D problem and solution"],
     "correct":["C"],"hint":"Words like 'first,' 'next,' 'then,' and 'finally' signal a sequence of events.","active":True},
    {"subject":"Reading","domain":"RI","category":"Text Structure","type":"single","grade":4,
     "text":"Read: 'Because it did not rain for two months, the crops died and farmers lost money.'\n\nThis passage is an example of which text structure?",
     "options":["A sequence","B cause and effect","C compare and contrast","D description"],
     "correct":["B"],"hint":"'Because' signals a cause (no rain) leading to effects (crops died, farmers lost money).","active":True},
]

ri_text_features = [
    {"subject":"Reading","domain":"RI","category":"Text Features","type":"single","grade":4,
     "text":"Words in a textbook that appear in bold print usually signal ___.",
     "options":["A unimportant details","B important vocabulary words","C the author's opinion","D a mistake in printing"],
     "correct":["B"],"hint":"Bold print draws attention to key vocabulary the reader should know.","active":True},
    {"subject":"Reading","domain":"RI","category":"Text Features","type":"single","grade":4,
     "text":"A ___ is a text feature that shows information organized in rows and columns.",
     "options":["A caption","B table","C heading","D glossary"],
     "correct":["B"],"hint":"Tables organize facts and numbers into rows and columns.","active":True},
    {"subject":"Reading","domain":"RI","category":"Text Features","type":"single","grade":4,
     "text":"You want to quickly find which page in a book discusses volcanoes. Which text feature should you check first?",
     "options":["A the glossary","B the index","C the caption","D the title"],
     "correct":["B"],"hint":"An index lists topics alphabetically along with the page numbers where they appear.","active":True},
    {"subject":"Reading","domain":"RI","category":"Text Features","type":"single","grade":4,
     "text":"A caption is used to ___.",
     "options":["A list all the chapters in a book","B describe or explain a picture or photo","C define difficult words","D show the page numbers"],
     "correct":["B"],"hint":"Captions appear near images and explain what the image shows.","active":True},
    {"subject":"Reading","domain":"RI","category":"Text Features","type":"single","grade":4,
     "text":"Headings and subheadings in a nonfiction article help readers ___.",
     "options":["A memorize every word","B find and organize information quickly","C skip the whole article","D make the text longer"],
     "correct":["B"],"hint":"Headings break the text into sections so readers can find topics quickly.","active":True},
]

# ── L: Language ──────────────────────────────────────────────────────

l_prefixes_suffixes = [
    {"subject":"Reading","domain":"L","category":"Prefixes & Suffixes","type":"single","grade":4,
     "text":"The prefix 're-' in the word 'rewrite' usually means:",
     "options":["A not","B again","C before","D without"],
     "correct":["B"],"hint":"'Re-' means to do something again, like 'rewrite' means to write again.","active":True},
    {"subject":"Reading","domain":"L","category":"Prefixes & Suffixes","type":"single","grade":4,
     "text":"Adding the suffix '-ful' to the word 'help' creates 'helpful,' which means:",
     "options":["A without help","B before helping","C full of help","D not helpful"],
     "correct":["C"],"hint":"'-ful' means 'full of,' so 'helpful' means full of help.","active":True},
    {"subject":"Reading","domain":"L","category":"Prefixes & Suffixes","type":"single","grade":4,
     "text":"What does the prefix 'un-' mean in the word 'unhappy'?",
     "options":["A very","B again","C not","D full of"],
     "correct":["C"],"hint":"'Un-' means 'not,' so 'unhappy' means not happy.","active":True},
    {"subject":"Reading","domain":"L","category":"Prefixes & Suffixes","type":"single","grade":4,
     "text":"Which suffix means 'without,' as in the word 'careless'?",
     "options":["A -ful","B -less","C -able","D -ness"],
     "correct":["B"],"hint":"'-less' means 'without,' so 'careless' means without care.","active":True},
    {"subject":"Reading","domain":"L","category":"Prefixes & Suffixes","type":"single","grade":4,
     "text":"The word 'disagree' uses the prefix 'dis-,' which means:",
     "options":["A again","B not / opposite of","C before","D with"],
     "correct":["B"],"hint":"'Dis-' means 'not' or the opposite of, so 'disagree' means to not agree.","active":True},
]

l_subject_verb_agreement = [
    {"subject":"Reading","domain":"L","category":"Subject-Verb Agreement","type":"single","grade":4,
     "text":"Choose the correct verb: 'The dogs ___ in the yard every afternoon.'",
     "options":["A run","B runs","C running","D ran"],
     "correct":["A"],"hint":"'Dogs' is plural, so it needs the plural verb form 'run,' not 'runs.'","active":True},
    {"subject":"Reading","domain":"L","category":"Subject-Verb Agreement","type":"single","grade":4,
     "text":"Choose the correct verb: 'She ___ to the store every Saturday.'",
     "options":["A go","B goes","C going","D gone"],
     "correct":["B"],"hint":"'She' is singular, so it needs the singular verb form 'goes.'","active":True},
    {"subject":"Reading","domain":"L","category":"Subject-Verb Agreement","type":"single","grade":4,
     "text":"Choose the sentence that has correct subject-verb agreement.",
     "options":["A The boys plays outside","B The boy play outside","C The boys play outside","D The boy playing outside"],
     "correct":["C"],"hint":"'Boys' is plural, so it must be paired with the plural verb 'play.'","active":True},
    {"subject":"Reading","domain":"L","category":"Subject-Verb Agreement","type":"single","grade":4,
     "text":"Choose the correct verb: 'The team of players ___ practicing hard for the championship.'",
     "options":["A is","B are","C were","D been"],
     "correct":["A"],"hint":"'Team' is a singular collective noun, so it takes the singular verb 'is.'","active":True},
    {"subject":"Reading","domain":"L","category":"Subject-Verb Agreement","type":"single","grade":4,
     "text":"Choose the correct verb: 'Either the cat or the dogs ___ responsible for the mess.'",
     "options":["A is","B are","C be","D being"],
     "correct":["B"],"hint":"When subjects are joined by 'or,' the verb agrees with the subject closer to it — 'dogs' is plural, so use 'are.'","active":True},
]

l_commas_punctuation = [
    {"subject":"Reading","domain":"L","category":"Commas & Punctuation","type":"single","grade":4,
     "text":"Which sentence uses commas correctly in a list?",
     "options":["A I packed shirts, socks, and shoes for the trip.","B I packed shirts socks, and shoes for the trip.","C I packed, shirts socks and shoes for the trip.","D I packed shirts, socks and, shoes for the trip."],
     "correct":["A"],"hint":"In a list of three or more items, place a comma after each item except the last.","active":True},
    {"subject":"Reading","domain":"L","category":"Commas & Punctuation","type":"single","grade":4,
     "text":"Where should a comma go in this sentence?\n'After the game we went out for pizza.'",
     "options":["A After the game, we went out for pizza.","B After, the game we went out for pizza.","C After the game we, went out for pizza.","D No comma is needed."],
     "correct":["A"],"hint":"A comma follows an introductory phrase like 'After the game' before the main clause.","active":True},
    {"subject":"Reading","domain":"L","category":"Commas & Punctuation","type":"single","grade":4,
     "text":"Which sentence correctly uses a comma before a conjunction joining two complete sentences?",
     "options":["A I wanted to go outside, but it started to rain.","B I wanted to go outside but, it started to rain.","C I wanted, to go outside but it started to rain.","D I wanted to go outside but it, started to rain."],
     "correct":["A"],"hint":"Place the comma right before the conjunction ('but') that joins two complete sentences.","active":True},
    {"subject":"Reading","domain":"L","category":"Commas & Punctuation","type":"single","grade":4,
     "text":"Which sentence correctly uses commas to set off the name of someone being spoken to?",
     "options":["A Thanks Grandma for the gift.","B Thanks, Grandma for the gift.","C Thanks, Grandma, for the gift.","D Thanks Grandma, for the gift."],
     "correct":["C"],"hint":"A name used in direct address is set off by commas on both sides.","active":True},
    {"subject":"Reading","domain":"L","category":"Commas & Punctuation","type":"single","grade":4,
     "text":"When writing a list of three or more items, a comma should be placed:",
     "options":["A only after the first item","B before each item including the first","C between each item in the series","D only at the very end of the sentence"],
     "correct":["C"],"hint":"Commas separate each item in a series so the list is easy to read.","active":True},
]

l_vocabulary_in_context = [
    {"subject":"Reading","domain":"L","category":"Vocabulary in Context","type":"single","grade":4,
     "text":"Read: 'The famished dog gobbled up its food in seconds.'\n\nWhat does 'famished' most likely mean?",
     "options":["A very hungry","B very tired","C very happy","D very slow"],
     "correct":["A"],"hint":"Gobbling up food in seconds is a clue that the dog was extremely hungry.","active":True},
    {"subject":"Reading","domain":"L","category":"Vocabulary in Context","type":"single","grade":4,
     "text":"Read: 'The ancient castle was in a state of disrepair, with crumbling walls and broken windows.'\n\nWhat does 'disrepair' mean?",
     "options":["A newly built","B damaged and in need of fixing","C beautifully decorated","D very expensive"],
     "correct":["B"],"hint":"'Crumbling walls' and 'broken windows' show the castle is damaged and needs repairs.","active":True},
    {"subject":"Reading","domain":"L","category":"Vocabulary in Context","type":"single","grade":4,
     "text":"Read: 'Maria was ecstatic when she found out she had won first place.'\n\nWhat does 'ecstatic' mean?",
     "options":["A extremely happy","B extremely angry","C extremely tired","D extremely confused"],
     "correct":["A"],"hint":"Winning first place would make someone feel extremely happy and excited.","active":True},
    {"subject":"Reading","domain":"L","category":"Vocabulary in Context","type":"single","grade":4,
     "text":"Read: 'The detective scrutinized every clue before making a decision.'\n\nWhat does 'scrutinized' mean?",
     "options":["A ignored","B examined closely","C threw away","D copied"],
     "correct":["B"],"hint":"A detective carefully studies clues before deciding — that's what 'scrutinized' means.","active":True},
    {"subject":"Reading","domain":"L","category":"Vocabulary in Context","type":"single","grade":4,
     "text":"Read: 'After the marathon, the runners were exhausted and could barely stand.'\n\nWhat does 'exhausted' mean?",
     "options":["A very tired","B very excited","C very hungry","D very cold"],
     "correct":["A"],"hint":"Being unable to barely stand after a marathon is a clue that the runners were extremely tired.","active":True},
]

all_ela_batch2 = (
    rl_story_elements +
    rl_theme +
    rl_figurative_language +
    ri_main_idea +
    ri_text_structure +
    ri_text_features +
    l_prefixes_suffixes +
    l_subject_verb_agreement +
    l_commas_punctuation +
    l_vocabulary_in_context
)

print(f"Total Grade 4 ELA batch 2 questions: {len(all_ela_batch2)}")
by_domain = {}
for q in all_ela_batch2:
    by_domain[q['domain']] = by_domain.get(q['domain'], 0) + 1
for d, n in sorted(by_domain.items()):
    print(f"  {d}: {n}")
print()

print("Uploading Grade 4 ELA batch 2 questions...")
for i in range(0, len(all_ela_batch2), 25):
    batch = all_ela_batch2[i:i+25]
    upload_batch(batch)

print("Done!")
