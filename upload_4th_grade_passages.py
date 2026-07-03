import json, urllib.request, time

BASE = "https://zvffmucghcrqackghhlf.supabase.co/rest/v1"
KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp2ZmZtdWNnaGNycWFja2doaGxmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY3MjkyNTIsImV4cCI6MjA5MjMwNTI1Mn0.eJHX6LmInRdBd5nt9t_jBJwILGEQ6_SeN6ADorlsWic"
H    = {"Content-Type":"application/json","apikey":KEY,"Authorization":f"Bearer {KEY}"}

# ── Passages to insert ────────────────────────────────────────────────

PASSAGES = [
    {
        "id":     "gr4-comparing-fiction-marcela-jason",
        "title":  "Comparing Fiction: Marcela & Jason",
        "byline": "Text 1 — Marcela | Text 2 — Jason",
        "body":   (
            "TEXT 1 — Marcela\n\n"
            "Valentine's Day was Marcela's favorite holiday. She loved the candy, the cards, and the pink decorations "
            "all over the classroom. Her little sister Janet had stayed home from school that day because she was sick. "
            "Marcela felt bad for her sister at first, but once she got to school and the party started, she forgot all about it.\n\n"
            "When the party ended, Marcela's bag was stuffed with chocolates, gummy bears, and lollipops. She raced home, "
            "burst through the front door, and ran straight to her room. She had no plan to give Janet any of the candy.\n\n"
            "Just then, their mother walked into the kitchen. She noticed that Marcela was being rude — walking right past "
            "her sick little sister without even a glance. \"Marcela,\" her mother said quietly, \"Janet stayed home sick today. "
            "Don't you think she could use a little something to cheer her up?\"\n\n"
            "Marcela looked at her bag of candy, then looked at Janet curled up on the couch with a blanket. She sighed, "
            "reached into the bag, and pulled out a handful of gummy bears — Janet's favorite. Janet's eyes lit up. "
            "\"Thank you, Marcie,\" she whispered. Marcela smiled. It felt even better than she expected.\n\n"
            "─────────────────────────────────────\n\n"
            "TEXT 2 — Jason\n\n"
            "The score was tied 1–1 with five minutes left in the game. Jason had the ball at midfield and was sprinting "
            "toward the goal. His teammates were wide open on both sides, waving for the pass. But Jason didn't pass. "
            "He was so close to scoring a goal, and he loved the feeling when he scored. He took the shot — and missed.\n\n"
            "At halftime, Coach Terry gathered the team. He looked directly at Jason. \"Soccer is a team sport,\" Coach said "
            "calmly. \"There were three open players who could have scored. If you can't be a team player, you can't be "
            "on this team.\"\n\n"
            "Jason stared at his cleats. He knew Coach was right. In the second half, when he got the ball, he looked up "
            "and found his teammate Darius wide open near the goal. He passed. Darius shot — and scored. The crowd erupted.\n\n"
            "After the game, Jason walked over to Darius. \"Nice shot,\" he said. Darius grinned. Jason realized something: "
            "he would pass the ball to his teammates from now on. It was time to give them a chance to know how great "
            "it feels to score a goal."
        ),
    },
    {
        "id":     "gr4-harriet-tubman-nonfiction",
        "title":  "A Female Freedom Fighter: Harriet Tubman",
        "byline": "Text 1 — The Underground Railroad | Text 2 — A Spy for Freedom",
        "body":   (
            "TEXT 1 — The Underground Railroad\n\n"
            "Harriet Tubman was born a slave in Maryland around 1820. Growing up, she worked long hours in the fields "
            "and suffered greatly under slavery. In 1849, she made a daring escape and reached Pennsylvania — finally free.\n\n"
            "But Harriet did not forget those she left behind. She soon began working with the Underground Railroad — "
            "a network, or group, of people who worked together to bring slaves to freedom in the North. It was not a real "
            "railroad; it was a secret route, or path, that slaves could follow from safe house to safe house. "
            "The people who guided the slaves from place to place were called conductors.\n\n"
            "Harriet became one of the most famous conductors in history. She made 13 missions back into the South and "
            "led more than 70 enslaved people to freedom without losing a single one. She became known as 'Moses' because, "
            "like the biblical leader, she led her people out of bondage.\n\n"
            "When the Civil War began, Harriet's work grew even bolder. In 1863, she led a raid on a plantation in South "
            "Carolina that freed 750 slaves in a single night — one of the largest liberation efforts of the war.\n\n"
            "─────────────────────────────────────\n\n"
            "TEXT 2 — A Spy for Freedom\n\n"
            "Running away from slavery was one of the most dangerous things a person could do in the 1800s. If a runaway "
            "slave was found by slave catchers, their owners would often hurt them and punish them severely. Even so, "
            "thousands of brave men and women risked everything for a chance at freedom.\n\n"
            "When Harriet Tubman finally escaped, she made it all the way to Philadelphia, where she was able to find work "
            "and begin a new life. But like in Text 1, she could not rest while others remained enslaved.\n\n"
            "When the Civil War broke out between the North and the South, Harriet volunteered to help the Union Army. "
            "She served in three remarkable roles: she worked as a cook, a nurse caring for sick and wounded soldiers, "
            "and even as a spy — using her knowledge of the land and her network of contacts in the South to gather "
            "information for Union generals.\n\n"
            "Harriet Tubman spent her life fighting for the freedom and dignity of others. She is remembered as one of "
            "the greatest heroes in American history."
        ),
    },
]

def upsert_passage(p):
    data = json.dumps(p).encode()
    req = urllib.request.Request(
        f"{BASE}/passages?on_conflict=id",
        data=data, method="POST",
        headers={**H, "Prefer": "resolution=merge-duplicates,return=minimal"}
    )
    with urllib.request.urlopen(req) as r:
        print(f"  passage '{p['id']}': HTTP {r.status}")

def fetch_questions_by_category(category):
    url = f"{BASE}/questions?grade=eq.4&category=eq.{urllib.parse.quote(category)}&select=id,text"
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def patch_passage_id(qid, passage_id):
    data = json.dumps({"passage_id": passage_id}).encode()
    req = urllib.request.Request(
        f"{BASE}/questions?id=eq.{qid}",
        data=data, method="PATCH", headers={**H, "Prefer": "return=minimal"}
    )
    with urllib.request.urlopen(req) as r:
        return r.status

import urllib.parse

print("Inserting passages...")
for p in PASSAGES:
    upsert_passage(p)
    time.sleep(0.2)

print("\nLinking questions to passages...")

# Comparing Fiction: Marcela & Jason → all 7 RL comparing fiction questions
comparing_qs = fetch_questions_by_category("Comparing Fiction Texts")
print(f"  Found {len(comparing_qs)} Comparing Fiction Texts questions")
for q in comparing_qs:
    status = patch_passage_id(q["id"], "gr4-comparing-fiction-marcela-jason")
    print(f"    [{status}] {q['text'][:60]}...")
    time.sleep(0.1)

# Harriet Tubman nonfiction → all 8 RI Comparing Nonfiction Texts questions
harriet_qs = fetch_questions_by_category("Comparing Nonfiction Texts")
print(f"  Found {len(harriet_qs)} Comparing Nonfiction Texts questions")
for q in harriet_qs:
    status = patch_passage_id(q["id"], "gr4-harriet-tubman-nonfiction")
    print(f"    [{status}] {q['text'][:60]}...")
    time.sleep(0.1)

print("\nDone!")
