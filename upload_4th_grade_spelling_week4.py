import json, urllib.request, time

BASE = "https://zvffmucghcrqackghhlf.supabase.co/rest/v1"
KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp2ZmZtdWNnaGNycWFja2doaGxmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY3MjkyNTIsImV4cCI6MjA5MjMwNTI1Mn0.eJHX6LmInRdBd5nt9t_jBJwILGEQ6_SeN6ADorlsWic"
HEADERS = {"Content-Type":"application/json","apikey":KEY,"Authorization":f"Bearer {KEY}"}

# Tracked by: https://github.com/deld/jaden-mcap/issues/55
# Run this script from an environment with network access to Supabase, then close the issue.
#
# NOTE: subject='Spelling' is not yet wired up in index.html (only 'Math' and
# 'Reading' are hardcoded as subjects/tabs today). This script uploads real
# content now so it's ready the moment the Spelling section ships (see #55).
# Source: "Words Their Way Wk 4" list from Jaden's teacher (ClassroomParent
# email, Sept 15 2026), Google Doc word list, Sky/Sea group (Jaden's group).

# ── Register the packet (Week of Sept 14-18, 2026) ───────────────────
PACKET = {
    "student": "Jaden",
    "grade": 4,
    "subject": "Spelling",
    "week_of": "2026-09-14",
    "status": "approved",
    "notes": (
        "Words Their Way Week 4 spelling list (Sept 14-18, 2026), from Jaden's teacher "
        "Cathy Schwartz via ClassroomParent email. Jaden is in the 'Sky' group, which shares "
        "a word list with the 'Sea' group in the source doc. Theme: the prefixes micro-, "
        "mega-, super-, and hyper-. Questions below are 'which word is spelled correctly?' "
        "multiple choice (existing question format) as a stopgap until a real typed-spelling "
        "input exists (see issue #55)."
    ),
}

def insert_packet(packet):
    data = json.dumps(packet).encode()
    req = urllib.request.Request(
        f"{BASE}/packets", data=data, method="POST",
        headers={**HEADERS, "Prefer": "return=representation"}
    )
    with urllib.request.urlopen(req) as r:
        result = json.loads(r.read())
        print(f"  Packet inserted: HTTP {r.status} -> id {result[0]['id']}")
        return result[0]["id"]


# ── Guard: never upload options with letter prefixes baked in (issue #29) ──
_LETTERS, _SEPS = "ABCDEFGH", (" ", ".", ")", "-", ":")
def strip_option_prefixes(options):
    if not isinstance(options, list) or len(options) < 2: return options
    def cut(o, ch):
        if not isinstance(o, str): return None
        t = o.lstrip()
        return t[2:].lstrip(" .)-:") if len(t) >= 2 and t[0] == ch and t[1] in _SEPS else None
    hits = sum(1 for i, o in enumerate(options) if i < len(_LETTERS) and cut(o, _LETTERS[i]) is not None)
    if hits < max(3, len(options) - 1): return options
    return [(cut(o, _LETTERS[i]) if i < len(_LETTERS) else None) or o for i, o in enumerate(options)]

def upload_batch(batch):
    for q in batch:
        if q.get('options'): q['options'] = strip_option_prefixes(q['options'])
    data = json.dumps(batch).encode()
    req = urllib.request.Request(f"{BASE}/questions", data=data, method='POST')
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

# word, misspelling1, misspelling2, misspelling3, correct_letter, prefix hint
WORDS = [
    ("microwave",      "microwav",      "micorwave",     "microwaive",     "A", "micro- means 'small.'"),
    ("microcosm",       "microcosum",    "micracosm",     "microcosem",     "B", "micro- means 'small' — a microcosm is a small version of something bigger."),
    ("microscope",      "microscop",     "micrscope",     "microscoop",     "C", "micro- means 'small' — a microscope helps you see tiny things."),
    ("microbus",         "microbuss",     "micobus",       "microbuse",      "A", "micro- means 'small' — a microbus is a small bus."),
    ("microfilm",        "microfilim",    "micorfilm",     "microphilm",     "A", "micro- means 'small' — microfilm shrinks documents down to tiny size."),
    ("microsurgery",     "microsurgury",  "microssurgery", "micrasurgery",   "A", "micro- means 'small' — microsurgery is done on very small, delicate parts."),
    ("microbe",          "microb",        "micobe",        "microbee",       "B", "micro- means 'small' — a microbe is a tiny living thing you need a microscope to see."),
    ("megaphone",        "megaphon",      "magaphone",     "megaphoen",      "A", "mega- means 'great' or 'large' — a megaphone makes your voice loud."),
    ("megalopolis",      "megalopoliss",  "megalapolis",   "megalopolus",    "A", "mega- means 'great' or 'large' — a megalopolis is a huge, sprawling city area."),
    ("megabyte",         "megabite",      "magabyte",      "megabytte",      "A", "mega- means 'great' or 'large' — a megabyte is a large unit of computer storage."),
    ("megadose",         "megados",       "magadose",      "megadoze",       "A", "mega- means 'great' or 'large' — a megadose is a very large amount of something."),
    ("megahit",          "megahitt",      "magahit",       "meagahit",       "A", "mega- means 'great' or 'large' — a megahit is a huge success."),
    ("supermarket",      "supermarkett",  "supermaket",    "suppermarket",   "A", "super- means 'above' or 'beyond' — a supermarket is bigger than a regular market."),
    ("superhero",        "superheroe",    "superhoro",     "supperhero",     "A", "super- means 'above' or 'beyond' — a superhero has powers beyond a normal person."),
    ("superhighway",     "superhighwway", "supperhighway", "superhighwa",    "A", "super- means 'above' or 'beyond' — a superhighway is bigger than a normal highway."),
    ("superhuman",       "superhumin",    "supperhuman",   "superhuma",      "A", "super- means 'above' or 'beyond' — superhuman abilities go beyond normal human limits."),
    ("superstar",        "superstarr",    "supperstar",    "superstahr",     "A", "super- means 'above' or 'beyond' — a superstar is far more famous than most stars."),
    ("superego",         "supperego",     "superegoh",     "superrego",      "A", "super- means 'above' or 'beyond' — the superego is a part of the mind above basic instinct."),
    ("superpower",       "supperpower",   "superpowr",     "superpowor",     "A", "super- means 'above' or 'beyond' — a superpower is an ability beyond ordinary power."),
    ("hyperactive",      "hiperactive",   "hyperactivve",  "hyperacttive",   "A", "hyper- means 'over' or 'excessive' — hyperactive means overly active."),
    ("hyperventilate",   "hyperventalate","hiperventilate","hyperventilait", "A", "hyper- means 'over' or 'excessive' — to hyperventilate is to breathe too fast."),
    ("hypercritical",    "hipercritical", "hypercritcal",  "hypercriticle",  "A", "hyper- means 'over' or 'excessive' — hypercritical means overly critical."),
    ("hypersensitive",   "hipersensitive","hypersensative","hypersensitivve","A", "hyper- means 'over' or 'excessive' — hypersensitive means overly sensitive."),
]

spelling_questions = []
for word, wrong1, wrong2, wrong3, letter, hint in WORDS:
    slots = ["A", "B", "C", "D"]
    wrongs = [wrong1, wrong2, wrong3]
    opts = {}
    wi = 0
    for slot in slots:
        if slot == letter:
            opts[slot] = word
        else:
            opts[slot] = wrongs[wi]
            wi += 1
    options_list = [f"{slot} {opts[slot]}" for slot in slots]
    spelling_questions.append({
        "subject": "Spelling", "domain": "Words Their Way", "category": "Sky Group",
        "type": "single", "grade": 4, "source": "packet",
        "text": "Which word is spelled correctly?",
        "options": options_list,
        "correct": [letter],
        "hint": hint,
        "active": True,
    })

print(f"Total Grade 4 Spelling questions: {len(spelling_questions)}")
print()

print("Registering packet...")
packet_id = insert_packet(PACKET)

print("\nUploading Grade 4 Spelling questions...")
for i in range(0, len(spelling_questions), 25):
    batch = spelling_questions[i:i+25]
    upload_batch(batch)

print("Done!")
