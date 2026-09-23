import json, urllib.request, time

BASE = "https://zvffmucghcrqackghhlf.supabase.co/rest/v1"
KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp2ZmZtdWNnaGNycWFja2doaGxmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY3MjkyNTIsImV4cCI6MjA5MjMwNTI1Mn0.eJHX6LmInRdBd5nt9t_jBJwILGEQ6_SeN6ADorlsWic"
HEADERS = {"Content-Type":"application/json","apikey":KEY,"Authorization":f"Bearer {KEY}"}

# Tracked by: https://github.com/deld/jaden-mcap/issues/63
# Run this script from an environment with network access to Supabase, then close the issue.

# ── Register the packet ───────────────────────────────────────────────
PACKET = {
    "student": "Jaden",
    "grade": 4,
    "subject": "Math",
    "week_of": "2026-09-23",
    "status": "approved",
    "notes": (
        "Math packet from Jaden's teacher (pages 28-35, scanned Sept 22-23, 2026). Covers: "
        "4-digit x 1-digit multiplication and division with a color-by-answer puzzle "
        "(Exercise 12), 'times as many' ratio/comparison word problems (Exercise 13), "
        "multiplying by 10 / scaling word problems (Exercise 14), estimating products by "
        "rounding then multiplying exactly for 2-digit x 2-digit and 3-digit x 2-digit "
        "problems (Exercise 15), and a 2-digit x 2-digit multiplication cross-number puzzle "
        "(Exercise 16). Practice questions below are newly generated with different numbers, "
        "modeled on the same skills/exercises."
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

def upload_batch(batch):
    # Teacher packet -> Classwork track, grouped by the sheet it came home on.
    for q in batch:
        q.setdefault('track', 'classwork')
        q.setdefault('assignment', 'Sept 23 Math Packet')
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

# ── Grade 4 · Math · Packet (Sept 23, 2026) ──────────────────────────
# New examples modeled on the packet's exercises, with the numbers changed.

# 4-digit x 1-digit multiplication (like Exercise 12, part 1)
mult_4x1 = [
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 3,145 × 4",
     "options":None,"correct":12580,"hint":"Break it apart: 3,000×4=12,000 and 145×4=580. Add them together.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 4,260 × 6",
     "options":None,"correct":25560,"hint":"Break it apart: 4,000×6=24,000 and 260×6=1,560. Add them together.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 5,127 × 7",
     "options":None,"correct":35889,"hint":"Break it apart: 5,000×7=35,000 and 127×7=889. Add them together.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 6,083 × 8",
     "options":None,"correct":48664,"hint":"Break it apart: 6,000×8=48,000 and 83×8=664. Add them together.","active":True},
]

# 4-digit division (like Exercise 12, part 2)
div_4digit = [
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,"source":"packet",
     "text":"Divide: 6,324 ÷ 4",
     "options":None,"correct":1581,"hint":"4 × 1,500 = 6,000, leaving 324. 4 × 81 = 324. So 1,500 + 81 = 1,581.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,"source":"packet",
     "text":"Divide: 8,415 ÷ 5",
     "options":None,"correct":1683,"hint":"5 × 1,600 = 8,000, leaving 415. 5 × 83 = 415. So 1,600 + 83 = 1,683.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,"source":"packet",
     "text":"Divide: 4,816 ÷ 8",
     "options":None,"correct":602,"hint":"8 × 600 = 4,800, leaving 16. 8 × 2 = 16. So 600 + 2 = 602.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,"source":"packet",
     "text":"Divide: 3,690 ÷ 10",
     "options":None,"correct":369,"hint":"Dividing by 10 removes one zero from the end of the number.","active":True},
]

# "Times as many" ratio/comparison word problems (like Exercise 13)
ratio_word_problems = [
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,"source":"packet",
     "text":"A jar contains blue marbles and red marbles. The number of blue marbles is 4 times the number of red marbles. If there are 235 red marbles, what is the total number of marbles in the jar?",
     "options":None,"correct":1175,"hint":"Blue marbles = 4 × 235 = 940. Add the red marbles: 940 + 235.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,"source":"packet",
     "text":"A bakery made 4 times as many muffins as cookies. If they made 1,368 muffins, how many more muffins than cookies did they make?",
     "options":None,"correct":1026,"hint":"Cookies = 1,368 ÷ 4 = 342. Subtract from the muffins: 1,368 − 342.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,"source":"packet",
     "text":"Mia bought 3 tablets at $429 each. She had $215 left after buying them. How much money did she have at first?",
     "options":None,"correct":1502,"hint":"Cost of tablets = 3 × $429 = $1,287. Add what she had left: $1,287 + $215.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,"source":"packet",
     "text":"6 people shared a sum of money. 2 of them received $512 each. The other 4 received $389 each. Find the total sum of money.",
     "options":None,"correct":2580,"hint":"2 × $512 = $1,024. 4 × $389 = $1,556. Add them: $1,024 + $1,556.","active":True},
]

# Multiplying by 10 / scaling word problems (like Exercise 14, part 1)
scaling_word_problems = [
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,"source":"packet",
     "text":"A car can travel 9 km on 1 liter of gas. How far can it travel on 10 liters of gas?",
     "options":None,"correct":90,"hint":"Multiply by 10: 9 × 10.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,"source":"packet",
     "text":"1 baseball costs $12. How much do 10 baseballs cost?",
     "options":None,"correct":120,"hint":"Multiply by 10: $12 × 10.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,"source":"packet",
     "text":"Maria bakes 347 cookies every day. How many cookies does she bake in 10 days?",
     "options":None,"correct":3470,"hint":"Multiply by 10: 347 × 10.","active":True},
]

# Multiplying by 10 patterns (like Exercise 14, part 2)
multiply_by_10_patterns = [
    {"subject":"Math","domain":"NBT","category":"Multiplying by 10","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 57 × 4",
     "options":None,"correct":228,"hint":"57 × 4 = 228.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multiplying by 10","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 57 × 40",
     "options":None,"correct":2280,"hint":"57 × 40 is 10 times 57 × 4. Since 57 × 4 = 228, 57 × 40 = 2,280.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multiplying by 10","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 90 × 6",
     "options":None,"correct":540,"hint":"90 × 6 = 540.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multiplying by 10","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 90 × 60",
     "options":None,"correct":5400,"hint":"90 × 60 is 10 times 90 × 6. Since 90 × 6 = 540, 90 × 60 = 5,400.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multiplying by 10","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 215 × 3",
     "options":None,"correct":645,"hint":"215 × 3 = 645.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multiplying by 10","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 215 × 30",
     "options":None,"correct":6450,"hint":"215 × 30 is 10 times 215 × 3. Since 215 × 3 = 645, 215 × 30 = 6,450.","active":True},
]

# Estimate by rounding, then multiply exactly (like Exercise 15)
estimation = [
    {"subject":"Math","domain":"NBT","category":"Estimation","type":"numeric","grade":4,"source":"packet",
     "text":"Estimate 46 × 22 by rounding each number to the nearest ten, then multiplying the rounded numbers. What is the estimate?",
     "options":None,"correct":1000,"hint":"46 rounds to 50. 22 rounds to 20. 50 × 20 = 1,000.","active":True},
    {"subject":"Math","domain":"NBT","category":"Estimation","type":"numeric","grade":4,"source":"packet",
     "text":"What is the exact answer to 46 × 22?",
     "options":None,"correct":1012,"hint":"46 × 22 = 1,012. Compare this to your estimate of 1,000 — they should be close.","active":True},
    {"subject":"Math","domain":"NBT","category":"Estimation","type":"numeric","grade":4,"source":"packet",
     "text":"Estimate 67 × 48 by rounding each number to the nearest ten, then multiplying the rounded numbers. What is the estimate?",
     "options":None,"correct":3500,"hint":"67 rounds to 70. 48 rounds to 50. 70 × 50 = 3,500.","active":True},
    {"subject":"Math","domain":"NBT","category":"Estimation","type":"numeric","grade":4,"source":"packet",
     "text":"What is the exact answer to 67 × 48?",
     "options":None,"correct":3216,"hint":"67 × 48 = 3,216. Compare this to your estimate of 3,500 — they should be close.","active":True},
    {"subject":"Math","domain":"NBT","category":"Estimation","type":"numeric","grade":4,"source":"packet",
     "text":"Estimate 326 × 52 by rounding 326 to the nearest hundred and 52 to the nearest ten, then multiplying the rounded numbers. What is the estimate?",
     "options":None,"correct":15000,"hint":"326 rounds to 300. 52 rounds to 50. 300 × 50 = 15,000.","active":True},
    {"subject":"Math","domain":"NBT","category":"Estimation","type":"numeric","grade":4,"source":"packet",
     "text":"What is the exact answer to 326 × 52?",
     "options":None,"correct":16952,"hint":"326 × 52 = 16,952. Compare this to your estimate of 15,000 — they should be close.","active":True},
]

# 2-digit x 2-digit multiplication (like Exercise 16 cross-number puzzle)
mult_2x2 = [
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 34 × 17",
     "options":None,"correct":578,"hint":"Break it apart: 34 × 10 = 340 and 34 × 7 = 238. Add them together.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 26 × 48",
     "options":None,"correct":1248,"hint":"Break it apart: 26 × 40 = 1,040 and 26 × 8 = 208. Add them together.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 63 × 39",
     "options":None,"correct":2457,"hint":"Break it apart: 63 × 40 = 2,520, then subtract one group of 63: 2,520 − 63.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 91 × 24",
     "options":None,"correct":2184,"hint":"Break it apart: 91 × 20 = 1,820 and 91 × 4 = 364. Add them together.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 58 × 63",
     "options":None,"correct":3654,"hint":"Break it apart: 58 × 60 = 3,480 and 58 × 3 = 174. Add them together.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 47 × 82",
     "options":None,"correct":3854,"hint":"Break it apart: 47 × 80 = 3,760 and 47 × 2 = 94. Add them together.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 39 × 54",
     "options":None,"correct":2106,"hint":"Break it apart: 39 × 50 = 1,950 and 39 × 4 = 156. Add them together.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 72 × 19",
     "options":None,"correct":1368,"hint":"Break it apart: 72 × 20 = 1,440, then subtract one group of 72: 1,440 − 72.","active":True},
]

all_packet_questions = (
    mult_4x1 +
    div_4digit +
    ratio_word_problems +
    scaling_word_problems +
    multiply_by_10_patterns +
    estimation +
    mult_2x2
)

print(f"Total Grade 4 Math packet questions: {len(all_packet_questions)}")
by_domain = {}
for q in all_packet_questions:
    by_domain[q['domain']] = by_domain.get(q['domain'], 0) + 1
for d, n in sorted(by_domain.items()):
    print(f"  {d}: {n}")
print()

print("Registering packet...")
packet_id = insert_packet(PACKET)

print("\nUploading Grade 4 Math packet questions...")
for i in range(0, len(all_packet_questions), 25):
    batch = all_packet_questions[i:i+25]
    upload_batch(batch)

print("Done!")
