"""
78 grade 4 division questions (OA).

ALREADY RUN -- these questions are live in Supabase. This file is kept as the
source of record for data that is already in the database.

There is no dry-run flag: running this uploads on sight, and running it again
would duplicate every question above for Jaden. Check the `questions` table
before re-running.
"""
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

# 78 Division questions (currently has 22, need 78 more)
questions = [
    # --- NUMERIC (39 questions) ---
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"8 ÷ 2 = ?","options":None,"correct":4,"hint":"Think: 2 times what number equals 8?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"15 ÷ 3 = ?","options":None,"correct":5,"hint":"Think: 3 times what number equals 15?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"20 ÷ 4 = ?","options":None,"correct":5,"hint":"Think: 4 times what number equals 20?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"30 ÷ 5 = ?","options":None,"correct":6,"hint":"Think: 5 times what number equals 30?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"42 ÷ 6 = ?","options":None,"correct":7,"hint":"Think: 6 times what number equals 42?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"35 ÷ 7 = ?","options":None,"correct":5,"hint":"Think: 7 times what number equals 35?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"72 ÷ 8 = ?","options":None,"correct":9,"hint":"Think: 8 times what number equals 72?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"81 ÷ 9 = ?","options":None,"correct":9,"hint":"Think: 9 times what number equals 81?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"60 ÷ 10 = ?","options":None,"correct":6,"hint":"Dividing by 10 removes a zero.","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"18 ÷ 2 = ?","options":None,"correct":9,"hint":"Think: 2 times what number equals 18?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"24 ÷ 4 = ?","options":None,"correct":6,"hint":"Think: 4 times what number equals 24?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"45 ÷ 9 = ?","options":None,"correct":5,"hint":"Think: 9 times what number equals 45?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"56 ÷ 7 = ?","options":None,"correct":8,"hint":"Think: 7 times what number equals 56?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"36 ÷ 6 = ?","options":None,"correct":6,"hint":"Think: 6 times what number equals 36?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"27 ÷ 3 = ?","options":None,"correct":9,"hint":"Think: 3 times what number equals 27?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"40 ÷ 8 = ?","options":None,"correct":5,"hint":"Think: 8 times what number equals 40?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"50 ÷ 5 = ?","options":None,"correct":10,"hint":"Think: 5 times what number equals 50?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"63 ÷ 7 = ?","options":None,"correct":9,"hint":"Think: 7 times what number equals 63?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"48 ÷ 6 = ?","options":None,"correct":8,"hint":"Think: 6 times what number equals 48?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"64 ÷ 8 = ?","options":None,"correct":8,"hint":"Think: 8 times what number equals 64?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"90 ÷ 9 = ?","options":None,"correct":10,"hint":"Think: 9 times what number equals 90?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"16 ÷ 2 = ?","options":None,"correct":8,"hint":"Think: 2 times what number equals 16?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"21 ÷ 3 = ?","options":None,"correct":7,"hint":"Think: 3 times what number equals 21?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"28 ÷ 4 = ?","options":None,"correct":7,"hint":"Think: 4 times what number equals 28?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"25 ÷ 5 = ?","options":None,"correct":5,"hint":"Think: 5 times what number equals 25?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"54 ÷ 6 = ?","options":None,"correct":9,"hint":"Think: 6 times what number equals 54?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"49 ÷ 7 = ?","options":None,"correct":7,"hint":"Think: 7 times what number equals 49?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"32 ÷ 8 = ?","options":None,"correct":4,"hint":"Think: 8 times what number equals 32?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"36 ÷ 9 = ?","options":None,"correct":4,"hint":"Think: 9 times what number equals 36?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"70 ÷ 10 = ?","options":None,"correct":7,"hint":"Dividing by 10 removes a zero.","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"100 ÷ 10 = ?","options":None,"correct":10,"hint":"Think: 10 times what number equals 100?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"14 ÷ 2 = ?","options":None,"correct":7,"hint":"Think: 2 times what number equals 14?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"12 ÷ 3 = ?","options":None,"correct":4,"hint":"Think: 3 times what number equals 12?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"16 ÷ 4 = ?","options":None,"correct":4,"hint":"Think: 4 times what number equals 16?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"45 ÷ 5 = ?","options":None,"correct":9,"hint":"Think: 5 times what number equals 45?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"24 ÷ 6 = ?","options":None,"correct":4,"hint":"Think: 6 times what number equals 24?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"28 ÷ 7 = ?","options":None,"correct":4,"hint":"Think: 7 times what number equals 28?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"56 ÷ 8 = ?","options":None,"correct":7,"hint":"Think: 8 times what number equals 56?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"numeric","text":"18 ÷ 9 = ?","options":None,"correct":2,"hint":"Think: 9 times what number equals 18?","active":True},

    # --- SINGLE (39 questions) ---
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 12 ÷ 3?","options":["A 3","B 4","C 5","D 6"],"correct":["B"],"hint":"Think: 3 times what number equals 12?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 20 ÷ 5?","options":["A 3","B 4","C 5","D 6"],"correct":["B"],"hint":"Count by 5s: 5, 10, 15, 20 — that's 4 fives.","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 18 ÷ 6?","options":["A 2","B 3","C 4","D 5"],"correct":["B"],"hint":"Think: 6 times what number equals 18?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 32 ÷ 4?","options":["A 6","B 7","C 8","D 9"],"correct":["C"],"hint":"Think: 4 times what number equals 32?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 63 ÷ 9?","options":["A 5","B 6","C 7","D 8"],"correct":["C"],"hint":"Think: 9 times what number equals 63?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"A class of 24 students is divided into groups of 4. How many groups are there?","options":["A 4","B 5","C 6","D 8"],"correct":["C"],"hint":"Divide 24 by 4.","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"Jake has 35 stickers. He shares them equally among 7 friends. How many stickers does each friend get?","options":["A 4","B 5","C 6","D 7"],"correct":["B"],"hint":"Divide 35 by 7.","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"There are 48 apples to be placed into bags of 6. How many bags are needed?","options":["A 6","B 7","C 8","D 9"],"correct":["C"],"hint":"Divide 48 by 6.","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"Which multiplication fact helps you solve 54 ÷ 6?","options":["A 6 × 7 = 42","B 6 × 8 = 48","C 6 × 9 = 54","D 6 × 10 = 60"],"correct":["C"],"hint":"Division is the opposite of multiplication.","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 40 ÷ 5?","options":["A 6","B 7","C 8","D 9"],"correct":["C"],"hint":"Count by 5s until you reach 40.","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 72 ÷ 9?","options":["A 6","B 7","C 8","D 9"],"correct":["C"],"hint":"Think: 9 times what number equals 72?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 36 ÷ 4?","options":["A 7","B 8","C 9","D 10"],"correct":["C"],"hint":"Think: 4 times what number equals 36?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"Sara has 56 crayons and puts 8 in each box. How many boxes does she fill?","options":["A 5","B 6","C 7","D 8"],"correct":["C"],"hint":"Divide 56 by 8.","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 30 ÷ 6?","options":["A 4","B 5","C 6","D 7"],"correct":["B"],"hint":"Think: 6 times what number equals 30?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 21 ÷ 7?","options":["A 2","B 3","C 4","D 5"],"correct":["B"],"hint":"Think: 7 times what number equals 21?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"Which number completes the equation? 27 ÷ 3 = ?","options":["A 7","B 8","C 9","D 10"],"correct":["C"],"hint":"Think: 3 times what number equals 27?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"A farmer has 45 eggs and puts 9 in each carton. How many cartons does he use?","options":["A 4","B 5","C 6","D 7"],"correct":["B"],"hint":"Divide 45 by 9.","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 16 ÷ 8?","options":["A 1","B 2","C 3","D 4"],"correct":["B"],"hint":"Think: 8 times what number equals 16?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 90 ÷ 10?","options":["A 7","B 8","C 9","D 10"],"correct":["C"],"hint":"Dividing by 10 removes the zero.","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"There are 64 seats in 8 equal rows. How many seats are in each row?","options":["A 6","B 7","C 8","D 9"],"correct":["C"],"hint":"Divide 64 by 8.","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 15 ÷ 5?","options":["A 2","B 3","C 4","D 5"],"correct":["B"],"hint":"Count by 5s: 5, 10, 15 — that's 3 fives.","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 28 ÷ 7?","options":["A 3","B 4","C 5","D 6"],"correct":["B"],"hint":"Think: 7 times what number equals 28?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"Which equation belongs in the same fact family as 6 × 8 = 48?","options":["A 48 ÷ 6 = 8","B 48 ÷ 4 = 12","C 48 ÷ 8 = 5","D 48 ÷ 2 = 24"],"correct":["A"],"hint":"Division undoes multiplication.","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 100 ÷ 10?","options":["A 8","B 9","C 10","D 11"],"correct":["C"],"hint":"Think: 10 times what number equals 100?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"Tyler puts 6 cookies on each plate. He has 42 cookies total. How many plates does he need?","options":["A 5","B 6","C 7","D 8"],"correct":["C"],"hint":"Divide 42 by 6.","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 45 ÷ 5?","options":["A 7","B 8","C 9","D 10"],"correct":["C"],"hint":"Count by 5s until you reach 45.","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 24 ÷ 3?","options":["A 6","B 7","C 8","D 9"],"correct":["C"],"hint":"Think: 3 times what number equals 24?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"30 students sit equally in 5 rows. How many students are in each row?","options":["A 4","B 5","C 6","D 7"],"correct":["C"],"hint":"Divide 30 by 5.","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 18 ÷ 3?","options":["A 4","B 5","C 6","D 7"],"correct":["C"],"hint":"Think: 3 times what number equals 18?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 80 ÷ 10?","options":["A 6","B 7","C 8","D 9"],"correct":["C"],"hint":"Dividing by 10 removes the zero.","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 54 ÷ 9?","options":["A 4","B 5","C 6","D 7"],"correct":["C"],"hint":"Think: 9 times what number equals 54?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"A box of 36 pencils is shared equally among 4 students. How many pencils does each student get?","options":["A 7","B 8","C 9","D 10"],"correct":["C"],"hint":"Divide 36 by 4.","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 14 ÷ 2?","options":["A 5","B 6","C 7","D 8"],"correct":["C"],"hint":"Think: 2 times what number equals 14?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 48 ÷ 8?","options":["A 4","B 5","C 6","D 7"],"correct":["C"],"hint":"Think: 8 times what number equals 48?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"If 7 × 9 = 63, which division fact is in the same family?","options":["A 63 ÷ 9 = 7","B 63 ÷ 6 = 9","C 63 ÷ 7 = 9","D Both A and C"],"correct":["D"],"hint":"A multiplication fact has two related division facts.","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"Mrs. Lee has 40 markers to share equally among 8 students. How many markers does each student get?","options":["A 3","B 4","C 5","D 6"],"correct":["C"],"hint":"Divide 40 by 8.","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 60 ÷ 6?","options":["A 8","B 9","C 10","D 11"],"correct":["C"],"hint":"Think: 6 times what number equals 60?","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 35 ÷ 5?","options":["A 5","B 6","C 7","D 8"],"correct":["C"],"hint":"Count by 5s until you reach 35.","active":True},
    {"subject":"Math","domain":"OA","category":"Division","type":"single","text":"What is 12 ÷ 2?","options":["A 4","B 5","C 6","D 7"],"correct":["C"],"hint":"Think: 2 times what number equals 12?","active":True},
]

single_qs = [q for q in questions if q['type'] == 'single']
numeric_qs = [q for q in questions if q['type'] == 'numeric']

print(f"Division: {len(single_qs)} single, {len(numeric_qs)} numeric = {len(questions)} total")

print("Uploading single-choice Division questions...")
for i in range(0, len(single_qs), 25):
    upload_batch(single_qs[i:i+25])

print("Uploading numeric Division questions...")
for i in range(0, len(numeric_qs), 25):
    upload_batch(numeric_qs[i:i+25])

print("Done.")
