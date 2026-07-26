import json, urllib.request, urllib.parse, time

BASE = "https://zvffmucghcrqackghhlf.supabase.co/rest/v1"
KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp2ZmZtdWNnaGNycWFja2doaGxmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY3MjkyNTIsImV4cCI6MjA5MjMwNTI1Mn0.eJHX6LmInRdBd5nt9t_jBJwILGEQ6_SeN6ADorlsWic"
H    = {"Content-Type":"application/json","apikey":KEY,"Authorization":f"Bearer {KEY}"}

PASSAGE = {
    "id":     "gr4-elias-short-sweet-summary",
    "title":  "Short and Sweet Summaries: Elias",
    "byline": "A story about responsibility and procrastination",
    "body": (
        "Elias had a big social studies project due in two weeks. His teacher had given the class plenty of time to "
        "research and write. But Elias kept putting it off.\n\n"
        "On the first weekend, he went skateboarding with his friends at the park. On the second weekend, he played "
        "video games with his brother for hours. He even cleaned his room — something he never did — just to avoid "
        "sitting down to work on the project.\n\n"
        "Before he knew it, the night before the project was due had arrived. Elias stayed up late, scrambling to "
        "finish. He threw together whatever he could find and finally fell asleep long after midnight.\n\n"
        "The next morning, he turned in his project. His teacher thanked him and placed it on the pile. But Elias "
        "did not feel good about it. He was not proud of the work he had completed. He believed it would have been "
        "much better if he had spent more time on it — if he had just started earlier.\n\n"
        "As he walked back to his seat, Elias made a promise to himself: next time, he would be more responsible. "
        "He would start right away and do his very best work from the beginning.\n\n"
        "─────────────────────────────────────\n\n"
        "WRITING STRATEGY: Somebody, Wanted, But, So, Then\n\n"
        "Use this strategy to write a short fiction summary:\n"
        "• Somebody — Who is the main character?\n"
        "• Wanted — What did they want or need?\n"
        "• But — What was the problem or obstacle?\n"
        "• So — What did they do about it?\n"
        "• Then — How did it turn out / what did they learn?"
    ),
}

def upsert_passage(p):
    data = json.dumps(p).encode()
    req = urllib.request.Request(
        f"{BASE}/passages?on_conflict=id",
        data=data, method="POST",
        headers={**H, "Prefer": "resolution=merge-duplicates,return=minimal"}
    )
    with urllib.request.urlopen(req) as r:
        print(f"  passage '{p['id']}': HTTP {r.status}")

def fetch_questions_by_category(category, grade=4):
    url = f"{BASE}/questions?grade=eq.{grade}&category=eq.{urllib.parse.quote(category)}&select=id,text"
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

print("Inserting Elias passage...")
upsert_passage(PASSAGE)
time.sleep(0.2)

print("\nLinking Summarizing questions to passage...")
qs = fetch_questions_by_category("Summarizing")
print(f"  Found {len(qs)} Summarizing questions")
for q in qs:
    status = patch_passage_id(q["id"], "gr4-elias-short-sweet-summary")
    print(f"  [{status}] {q['text'][:70]}...")
    time.sleep(0.1)

print("\nDone!")
