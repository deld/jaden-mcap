"""
Week 4 spelling list (Sky group, Words Their Way) as TYPED-spelling questions.
Issue #55. Supplements the multiple-choice stopgap: recognising a correctly
spelled word among distractors is a weaker skill than spelling it.

type='spelling': the app reads the word aloud and shows the sentence with
the word blanked out; the child types it. `correct` is the word itself.

    python3 upload_spelling_week4_typed.py           # dry run
    python3 upload_spelling_week4_typed.py --apply   # upload
"""
import json, sys, urllib.request

BASE = "https://zvffmucghcrqackghhlf.supabase.co/rest/v1"
KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp2ZmZtdWNnaGNycWFja2doaGxmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY3MjkyNTIsImV4cCI6MjA5MjMwNTI1Mn0.eJHX6LmInRdBd5nt9t_jBJwILGEQ6_SeN6ADorlsWic"
H    = {"Content-Type": "application/json", "apikey": KEY, "Authorization": f"Bearer {KEY}"}

# (word, sentence with ___, hint)
WORDS = [
  ("microwave",      "Dad heated the soup in the ___ for two minutes.",                    "micro- means small. A small wave of energy heats the food."),
  ("microscope",     "We looked at a leaf cell through a ___ in science class.",           "micro- (small) + scope (to look). A tool for looking at small things."),
  ("microbe",        "A ___ is a living thing so tiny you need a microscope to see it.",   "micro- means small. Ends in -be, not -b."),
  ("microbus",       "The tour group rode in a ___ that seats only twelve people.",        "micro- (small) + bus. A small bus."),
  ("microfilm",      "The library keeps old newspapers on ___ to save space.",             "micro- (small) + film. Documents shrunk down tiny."),
  ("microsurgery",   "The doctor used ___ to repair the tiny blood vessels.",              "micro- (small) + surgery. Two r's in surgery, and -ery at the end."),
  ("microcosm",      "The classroom fish tank is a ___ of a real pond.",                   "micro- (small) + cosm (world). Ends in -cosm, no e."),
  ("megaphone",      "The coach shouted through a ___ so everyone could hear.",            "mega- (great) + phone (sound). Makes your voice great and loud."),
  ("megabyte",       "The photo file is about one ___ in size.",                           "mega- (large) + byte. Spelled b-y-t-e, like the computer word."),
  ("megahit",        "The new movie was such a ___ that every show sold out.",             "mega- (great) + hit. One t at the end."),
  ("megadose",       "Never take a ___ of vitamins without asking a doctor.",              "mega- (large) + dose. A very large amount."),
  ("megalopolis",    "The cities along the coast have grown into one huge ___.",           "mega- (great) + polis (city). It ends in -polis, like Minneapolis."),
  ("supermarket",    "We buy groceries at the ___ every Saturday.",                        "super- (above) + market. One p in super."),
  ("superhero",      "My favourite ___ can fly and lift a truck.",                         "super- (beyond) + hero. Ends in -hero, no e after."),
  ("superhighway",   "Cars sped along the eight-lane ___.",                                "super- (beyond) + highway. One w in highway."),
  ("superhuman",     "It took ___ strength to move the fallen tree.",                      "super- (beyond) + human. Beyond what a human can do."),
  ("superstar",      "The singer became a ___ after her first album.",                     "super- (above) + star. One r at the end."),
  ("superpower",     "If I had a ___, I would choose to become invisible.",                "super- (beyond) + power. Spelled p-o-w-e-r."),
  ("superego",       "In psychology, the ___ is the part of the mind that judges right and wrong.", "super- (above) + ego. Just ego at the end, nothing extra."),
  ("hyperactive",    "The puppy was so ___ it could not sit still for a second.",          "hyper- (over) + active. Starts with hy-, not hi-."),
  ("hyperventilate", "If you breathe too fast when you are scared, you might ___.",        "hyper- (over) + ventilate. Ends in -ilate, with an i."),
  ("hypercritical",  "A ___ judge finds fault with every single performance.",             "hyper- (over) + critical. Two i's in critical."),
  ("hypersensitive", "His skin is ___ to wool and gets itchy right away.",                 "hyper- (over) + sensitive. Sens-i-tive, with an i."),
]

def rows():
    return [{
        "grade": 4, "subject": "Spelling", "domain": "Words Their Way", "category": "Sky Group",
        "type": "spelling", "text": sent, "options": None, "correct": word,
        "hint": hint,
        "solution": f"Break it into parts: {word[:5] if word.startswith('super') or word.startswith('micro') or word.startswith('hyper') else word[:4]}- + {word[5:] if word.startswith(('super','micro','hyper')) else word[4:]}.\nSay each part slowly, then write it: {word}",
        "active": True, "source": "packet", "track": "test_prep",
    } for word, sent, hint in WORDS]

def post(batch):
    req = urllib.request.Request(f"{BASE}/questions", data=json.dumps(batch).encode(),
                                 method="POST", headers={**H, "Prefer": "return=minimal"})
    with urllib.request.urlopen(req) as r: return r.status

R = rows()
assert all("___" in r["text"] for r in R)
assert len({r["correct"] for r in R}) == len(R)
print(f"{len(R)} typed-spelling questions")
for r in R[:3]: print(f"  {r['correct']:15} {r['text']}")
if "--apply" not in sys.argv:
    print("\nDRY RUN. Re-run with --apply to upload."); sys.exit(0)
print(f"HTTP {post(R)} - uploaded")
