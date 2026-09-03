"""
Strip letter prefixes baked into question option text.

Uploads stored options as ["A 35", "B 100", ...]. The app shuffles options at
render and draws its own A/B/C/D badge, so the baked-in letter and the badge
fall out of sync as soon as the order changes - the child sees "A) D 200".

Scoring is unaffected: `correct` stores letters that are remapped to the new
position during the shuffle. Positions are untouched here, so stored `correct`
values stay valid. This is a pure text cleanup.

Detection is deliberately strict. It requires the leading letters to run
A, B, C, D *in sequence across positions*, so legitimate text like
["A rhyme", "A simile", "A metaphor"] is never touched - only position 0
would match there, not positions 1 and 2.
"""
import json, urllib.request, sys, random

BASE = "https://zvffmucghcrqackghhlf.supabase.co/rest/v1"
KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp2ZmZtdWNnaGNycWFja2doaGxmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY3MjkyNTIsImV4cCI6MjA5MjMwNTI1Mn0.eJHX6LmInRdBd5nt9t_jBJwILGEQ6_SeN6ADorlsWic"
H    = {"Content-Type": "application/json", "apikey": KEY, "Authorization": f"Bearer {KEY}"}

LETTERS = "ABCDEFGH"
SEPS    = (" ", ".", ")", "-", ":")

DRY = "--apply" not in sys.argv


def strip_one(opt, letter):
    """Return the option minus a leading `<letter><sep>`, or None if absent."""
    if not isinstance(opt, str):
        return None
    t = opt.lstrip()
    if len(t) >= 2 and t[0] == letter and t[1] in SEPS:
        return t[2:].lstrip(" .)-:")
    return None


def is_prefixed(options):
    """True only when leading letters run A,B,C,D in sequence across positions."""
    if not isinstance(options, list) or len(options) < 2:
        return False
    hits = sum(1 for i, o in enumerate(options)
               if i < len(LETTERS) and strip_one(o, LETTERS[i]) is not None)
    return hits >= max(3, len(options) - 1)


def clean(options):
    out = []
    for i, o in enumerate(options):
        s = strip_one(o, LETTERS[i]) if i < len(LETTERS) else None
        out.append(s if s else o)
    return out


def fetch_all():
    rows, off = [], 0
    while True:
        url = f"{BASE}/questions?select=id,grade,subject,domain,options,correct&active=eq.true&order=id&offset={off}&limit=1000"
        req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
        with urllib.request.urlopen(req) as r:
            batch = json.loads(r.read())
        rows += batch
        if len(batch) < 1000:
            return rows
        off += 1000


def patch(qid, options):
    data = json.dumps({"options": options}).encode()
    req = urllib.request.Request(f"{BASE}/questions?id=eq.{qid}", data=data,
                                 method="PATCH", headers={**H, "Prefer": "return=minimal"})
    with urllib.request.urlopen(req) as r:
        return r.status


rows = fetch_all()
affected = [q for q in rows if is_prefixed(q.get("options"))]
print(f"active questions : {len(rows)}")
print(f"affected         : {len(affected)}")

# Refuse to write anything that would blank an option.
unsafe = []
for q in affected:
    if any(not str(o).strip() for o in clean(q["options"])):
        unsafe.append(q["id"])
if unsafe:
    print(f"ABORT: {len(unsafe)} would produce an empty option, e.g. {unsafe[:3]}")
    sys.exit(1)

random.seed(7)
print("\nsample (before -> after):")
for q in random.sample(affected, min(8, len(affected))):
    print(f"  {q['options']}\n   -> {clean(q['options'])}")

if DRY:
    print("\nDRY RUN. Re-run with --apply to write.")
    sys.exit(0)

ok = 0
for i, q in enumerate(affected, 1):
    if patch(q["id"], clean(q["options"])) in (200, 204):
        ok += 1
    if i % 100 == 0:
        print(f"  {i}/{len(affected)}")
print(f"\npatched {ok}/{len(affected)}")

left = [q for q in fetch_all() if is_prefixed(q.get("options"))]
print(f"remaining affected: {len(left)}")
