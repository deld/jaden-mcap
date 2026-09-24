"""
71 grade 4 multiplication questions (OA).

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

# 71 Multiplication questions (currently has 29, need 71 more)
questions = [
    # --- NUMERIC (36 questions) ---
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"3 × 4 = ?","options":None,"correct":12,"hint":"Add 3 four times: 3+3+3+3.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"5 × 6 = ?","options":None,"correct":30,"hint":"Count by 5s six times.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"7 × 8 = ?","options":None,"correct":56,"hint":"Remember: 7 × 8 = 56.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"6 × 9 = ?","options":None,"correct":54,"hint":"Think: 6 × 10 = 60, then subtract 6.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"4 × 7 = ?","options":None,"correct":28,"hint":"Count by 4s seven times.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"8 × 9 = ?","options":None,"correct":72,"hint":"Think: 8 × 10 = 80, then subtract 8.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"2 × 9 = ?","options":None,"correct":18,"hint":"Double 9.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"3 × 8 = ?","options":None,"correct":24,"hint":"Count by 3s eight times.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"5 × 7 = ?","options":None,"correct":35,"hint":"Count by 5s seven times.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"4 × 30 = ?","options":None,"correct":120,"hint":"4 × 3 = 12, then add a zero.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"6 × 6 = ?","options":None,"correct":36,"hint":"6 squared is 36.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"9 × 9 = ?","options":None,"correct":81,"hint":"9 squared is 81.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"7 × 7 = ?","options":None,"correct":49,"hint":"7 squared is 49.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"8 × 8 = ?","options":None,"correct":64,"hint":"8 squared is 64.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"3 × 6 = ?","options":None,"correct":18,"hint":"Count by 3s six times.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"2 × 50 = ?","options":None,"correct":100,"hint":"2 × 5 = 10, then add a zero.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"5 × 9 = ?","options":None,"correct":45,"hint":"Count by 5s nine times.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"4 × 8 = ?","options":None,"correct":32,"hint":"Double 4×4=16 to get 32.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"6 × 7 = ?","options":None,"correct":42,"hint":"Think: 6 × 7 = 42.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"3 × 9 = ?","options":None,"correct":27,"hint":"Count by 3s nine times.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"7 × 10 = ?","options":None,"correct":70,"hint":"Multiplying by 10 adds a zero.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"8 × 6 = ?","options":None,"correct":48,"hint":"Think: 8 × 6 = 48.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"9 × 4 = ?","options":None,"correct":36,"hint":"Count by 9s four times.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"5 × 40 = ?","options":None,"correct":200,"hint":"5 × 4 = 20, then add a zero.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"3 × 7 = ?","options":None,"correct":21,"hint":"Count by 3s seven times.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"2 × 8 = ?","options":None,"correct":16,"hint":"Double 8.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"6 × 4 = ?","options":None,"correct":24,"hint":"Count by 6s four times.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"9 × 7 = ?","options":None,"correct":63,"hint":"Think: 10 × 7 = 70, subtract 7.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"3 × 20 = ?","options":None,"correct":60,"hint":"3 × 2 = 6, then add a zero.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"8 × 7 = ?","options":None,"correct":56,"hint":"Remember: 8 × 7 = 56.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"4 × 9 = ?","options":None,"correct":36,"hint":"Think: 4 × 10 = 40, subtract 4.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"6 × 8 = ?","options":None,"correct":48,"hint":"Think: 6 × 8 = 48.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"5 × 8 = ?","options":None,"correct":40,"hint":"Count by 5s eight times.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"2 × 70 = ?","options":None,"correct":140,"hint":"2 × 7 = 14, then add a zero.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"9 × 6 = ?","options":None,"correct":54,"hint":"Think: 10 × 6 = 60, subtract 6.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"numeric","text":"4 × 6 = ?","options":None,"correct":24,"hint":"Count by 4s six times.","active":True},

    # --- SINGLE (35 questions) ---
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"What is 3 × 5?","options":["A 12","B 13","C 14","D 15"],"correct":["D"],"hint":"Count by 3s five times.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"What is 4 × 4?","options":["A 12","B 14","C 16","D 18"],"correct":["C"],"hint":"4 squared is 16.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"What is 6 × 5?","options":["A 25","B 28","C 30","D 35"],"correct":["C"],"hint":"Count by 5s six times.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"What is 7 × 3?","options":["A 18","B 21","C 24","D 27"],"correct":["B"],"hint":"Count by 7s three times.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"What is 8 × 4?","options":["A 28","B 30","C 32","D 34"],"correct":["C"],"hint":"Double 8 twice: 8, 16, 32.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"A garden has 5 rows of flowers with 8 flowers in each row. How many flowers are there in all?","options":["A 35","B 40","C 45","D 50"],"correct":["B"],"hint":"Multiply 5 × 8.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"What is 9 × 3?","options":["A 24","B 25","C 27","D 29"],"correct":["C"],"hint":"Count by 9s three times.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"Which shows 4 groups of 6?","options":["A 4 + 6","B 4 × 6","C 6 + 4","D 6 ÷ 4"],"correct":["B"],"hint":"Groups of means multiply.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"What is 6 × 10?","options":["A 16","B 60","C 66","D 600"],"correct":["B"],"hint":"Multiplying by 10 adds a zero.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"A bag holds 7 apples. How many apples are in 6 bags?","options":["A 36","B 42","C 48","D 49"],"correct":["B"],"hint":"Multiply 7 × 6.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"What is 8 × 3?","options":["A 21","B 22","C 24","D 26"],"correct":["C"],"hint":"Count by 8s three times.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"Which product equals 45?","options":["A 5 × 8","B 9 × 5","C 6 × 7","D 4 × 9"],"correct":["B"],"hint":"5 × 9 = 45.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"What is 7 × 6?","options":["A 40","B 42","C 44","D 48"],"correct":["B"],"hint":"Remember: 7 × 6 = 42.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"There are 4 shelves with 9 books each. How many books are there in all?","options":["A 32","B 34","C 36","D 38"],"correct":["C"],"hint":"Multiply 4 × 9.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"What is 5 × 30?","options":["A 35","B 100","C 150","D 200"],"correct":["C"],"hint":"5 × 3 = 15, then add a zero.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"An array has 7 rows and 7 columns. How many items are in the array?","options":["A 42","B 46","C 49","D 56"],"correct":["C"],"hint":"Multiply 7 × 7.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"What is 9 × 8?","options":["A 63","B 70","C 72","D 81"],"correct":["C"],"hint":"Think: 10 × 8 = 80, subtract 8.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"What is 3 × 40?","options":["A 43","B 100","C 120","D 140"],"correct":["C"],"hint":"3 × 4 = 12, then add a zero.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"There are 6 boxes with 8 crayons in each box. How many crayons are there in all?","options":["A 42","B 46","C 48","D 54"],"correct":["C"],"hint":"Multiply 6 × 8.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"What is 2 × 9?","options":["A 11","B 16","C 18","D 20"],"correct":["C"],"hint":"Double 9.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"Which multiplication equation represents the array with 3 rows and 8 columns?","options":["A 3 + 8 = 11","B 3 × 8 = 24","C 8 × 3 = 24","D Both B and C"],"correct":["D"],"hint":"An array can be read two ways.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"What is 7 × 9?","options":["A 56","B 61","C 63","D 72"],"correct":["C"],"hint":"Think: 10 × 7 = 70, subtract 7.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"A farmer plants 9 rows of corn with 9 plants in each row. How many plants are there in all?","options":["A 72","B 78","C 81","D 90"],"correct":["C"],"hint":"Multiply 9 × 9.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"What is 4 × 20?","options":["A 24","B 60","C 80","D 100"],"correct":["C"],"hint":"4 × 2 = 8, then add a zero.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"If one box has 6 chocolates, how many chocolates are in 7 boxes?","options":["A 36","B 40","C 42","D 48"],"correct":["C"],"hint":"Multiply 6 × 7.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"What is 5 × 5?","options":["A 20","B 22","C 24","D 25"],"correct":["D"],"hint":"Count by 5s five times.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"What is 8 × 10?","options":["A 18","B 80","C 88","D 800"],"correct":["B"],"hint":"Multiplying by 10 adds a zero.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"There are 3 bags with 7 oranges in each bag. How many oranges are there?","options":["A 18","B 21","C 24","D 27"],"correct":["B"],"hint":"Multiply 3 × 7.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"What is 6 × 60?","options":["A 66","B 120","C 360","D 600"],"correct":["C"],"hint":"6 × 6 = 36, then add a zero.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"Which property says 4 × 7 = 7 × 4?","options":["A Associative Property","B Commutative Property","C Distributive Property","D Identity Property"],"correct":["B"],"hint":"The order does not change the product.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"What is 9 × 10?","options":["A 81","B 89","C 90","D 99"],"correct":["C"],"hint":"Multiplying by 10 adds a zero.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"An auditorium has 8 rows of chairs with 9 chairs in each row. How many chairs are there in all?","options":["A 63","B 70","C 72","D 81"],"correct":["C"],"hint":"Multiply 8 × 9.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"What is 3 × 3?","options":["A 6","B 8","C 9","D 12"],"correct":["C"],"hint":"3 squared is 9.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"What is 7 × 50?","options":["A 57","B 350","C 357","D 700"],"correct":["B"],"hint":"7 × 5 = 35, then add a zero.","active":True},
    {"subject":"Math","domain":"OA","category":"Multiplication","type":"single","text":"A rectangle has a length of 9 and a width of 6. What is the area?","options":["A 15","B 45","C 54","D 63"],"correct":["C"],"hint":"Area = length × width.","active":True},
]

single_qs = [q for q in questions if q['type'] == 'single']
numeric_qs = [q for q in questions if q['type'] == 'numeric']

print(f"Multiplication: {len(single_qs)} single, {len(numeric_qs)} numeric = {len(questions)} total")

print("Uploading single-choice Multiplication questions...")
for i in range(0, len(single_qs), 25):
    upload_batch(single_qs[i:i+25])

print("Uploading numeric Multiplication questions...")
for i in range(0, len(numeric_qs), 25):
    upload_batch(numeric_qs[i:i+25])

print("Done.")
