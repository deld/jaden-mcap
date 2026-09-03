"""
Upload a classwork worksheet.

Classwork is kept separate from standardized test prep by the `track` column:
  track='classwork'  -> shows under the Classwork section, grouped by worksheet
  track='test_prep'  -> MCAP drill material (everything that existed before)

Edit ASSIGNMENT / GRADE / SUBJECT and the QUESTIONS list, then run:

    python3 upload_classwork.py            # dry run, prints what would upload
    python3 upload_classwork.py --apply    # actually write

To remove a worksheet you uploaded by mistake:

    python3 upload_classwork.py --delete "Week 3 - Multiplication"
"""
import json, sys, urllib.request, urllib.parse

BASE = "https://zvffmucghcrqackghhlf.supabase.co/rest/v1"
KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp2ZmZtdWNnaGNycWFja2doaGxmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY3MjkyNTIsImV4cCI6MjA5MjMwNTI1Mn0.eJHX6LmInRdBd5nt9t_jBJwILGEQ6_SeN6ADorlsWic"
H    = {"Content-Type": "application/json", "apikey": KEY, "Authorization": f"Bearer {KEY}"}

# ── edit these ───────────────────────────────────────────────────────────
GRADE      = 4
SUBJECT    = "Math"                      # "Math" | "Reading"
ASSIGNMENT = "Week 5 - Division"         # the name on the sheet
DOMAIN     = "NBT"                       # OA | NBT | NF | MD | G | RL | RI | L
CATEGORY   = "Division"                  # free text, shown as the chip

QUESTIONS = [
    # multiple choice: options + correct letter
    {"type": "single", "text": "What is 144 divided by 12?",
     "options": ["11", "12", "13", "14"], "correct": ["B"],
     "hint": "12 x 12 = 144"},

    # numeric: no options, correct is the number
    {"type": "numeric", "text": "What is 96 divided by 8?",
     "options": None, "correct": "12",
     "hint": "8 x 12 = 96"},
]
# ─────────────────────────────────────────────────────────────────────────

# Never upload options with letter prefixes baked in - the app shuffles
# options and draws its own A/B/C/D badge, so a baked-in letter contradicts
# the badge once the order changes. See issue #29.
_LETTERS, _SEPS = "ABCDEFGH", (" ", ".", ")", "-", ":")

def strip_option_prefixes(options):
    if not isinstance(options, list) or len(options) < 2:
        return options
    def cut(o, ch):
        if not isinstance(o, str):
            return None
        t = o.lstrip()
        return t[2:].lstrip(" .)-:") if len(t) >= 2 and t[0] == ch and t[1] in _SEPS else None
    hits = sum(1 for i, o in enumerate(options) if i < len(_LETTERS) and cut(o, _LETTERS[i]) is not None)
    if hits < max(3, len(options) - 1):
        return options
    return [(cut(o, _LETTERS[i]) if i < len(_LETTERS) else None) or o for i, o in enumerate(options)]


def rows():
    out = []
    for q in QUESTIONS:
        out.append({
            "grade": GRADE, "subject": SUBJECT, "domain": DOMAIN,
            "category": q.get("category", CATEGORY),
            "type": q["type"], "text": q["text"],
            "options": strip_option_prefixes(q.get("options")),
            "correct": q["correct"], "hint": q.get("hint"),
            "solution": q.get("solution"),
            "active": True, "source": "manual",
            "track": "classwork", "assignment": ASSIGNMENT,
        })
    return out


def post(batch):
    req = urllib.request.Request(f"{BASE}/questions", data=json.dumps(batch).encode(),
                                 method="POST", headers={**H, "Prefer": "return=minimal"})
    with urllib.request.urlopen(req) as r:
        return r.status


def delete(name):
    q = urllib.parse.quote(name)
    req = urllib.request.Request(
        f"{BASE}/questions?track=eq.classwork&assignment=eq.{q}",
        method="DELETE", headers={**H, "Prefer": "return=minimal"})
    with urllib.request.urlopen(req) as r:
        return r.status


if "--delete" in sys.argv:
    name = sys.argv[sys.argv.index("--delete") + 1]
    print(f"deleting worksheet {name!r}: HTTP {delete(name)}")
    sys.exit(0)

batch = rows()
print(f"{ASSIGNMENT}  ({SUBJECT}, grade {GRADE}) - {len(batch)} questions")
for r in batch:
    print(f"  [{r['type']:7}] {r['text'][:66]}")
    if r["options"]:
        print(f"            {r['options']}  -> {r['correct']}")

if "--apply" not in sys.argv:
    print("\nDRY RUN. Re-run with --apply to upload.")
    sys.exit(0)

print(f"\nHTTP {post(batch)} - uploaded")
