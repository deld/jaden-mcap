import json, urllib.request, time

BASE = "https://zvffmucghcrqackghhlf.supabase.co/rest/v1"
KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp2ZmZtdWNnaGNycWFja2doaGxmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY3MjkyNTIsImV4cCI6MjA5MjMwNTI1Mn0.eJHX6LmInRdBd5nt9t_jBJwILGEQ6_SeN6ADorlsWic"
HEADERS = {"Content-Type":"application/json","apikey":KEY,"Authorization":f"Bearer {KEY}"}

# Tracked by: https://github.com/deld/jaden-mcap/issues/53
# Run this script from an environment with network access to Supabase, then close the issue.

# ── Register the packet (2-week window: Sept 16–30, 2026) ────────────
PACKET = {
    "student": "Jaden",
    "grade": 4,
    "subject": "Math",
    "week_of": "2026-09-16",
    "status": "approved",
    "notes": (
        "2-week packet (Sept 16–Sept 30, 2026) from Jaden's teacher. Covers: "
        "3-digit x 2-digit multiplication (cross-number puzzle), a place-value/rounding/"
        "factors-and-multiples review, and fraction addition (like and unlike denominators) "
        "and subtraction (like denominators). Practice questions below are newly generated "
        "with different numbers, modeled on the same skills/exercises."
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

# ── Grade 4 · Math · Packet (Sept 16–30, 2026) ───────────────────────
# New examples modeled on the packet's exercises, with the numbers changed.

# Multi-digit multiplication (3-digit x 2-digit), like the cross-number puzzle
multiplication = [
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 214 × 34",
     "options":None,"correct":7276,"hint":"Break it apart: 214 × 30 = 6,420 and 214 × 4 = 856. Add them together.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 356 × 42",
     "options":None,"correct":14952,"hint":"Break it apart: 356 × 40 = 14,240 and 356 × 2 = 712. Add them together.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 178 × 56",
     "options":None,"correct":9968,"hint":"Break it apart: 178 × 50 = 8,900 and 178 × 6 = 1,068. Add them together.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 462 × 29",
     "options":None,"correct":13398,"hint":"Break it apart: 462 × 30 = 13,860, then subtract one group of 462: 13,860 − 462.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 139 × 47",
     "options":None,"correct":6533,"hint":"Break it apart: 139 × 40 = 5,560 and 139 × 7 = 973. Add them together.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,"source":"packet",
     "text":"Multiply: 283 × 61",
     "options":None,"correct":17263,"hint":"Break it apart: 283 × 60 = 16,980 and 283 × 1 = 283. Add them together.","active":True},
]

# Place value, rounding, number patterns, expanded form (like Review 1)
place_value_review = [
    {"subject":"Math","domain":"NBT","category":"Place Value & Rounding","type":"numeric","grade":4,"source":"packet",
     "text":"Write 'forty-two thousand, six hundred seventeen' in figures.",
     "options":None,"correct":42617,"hint":"Forty-two thousand = 42,000. Add six hundred seventeen = 617.","active":True},
    {"subject":"Math","domain":"NBT","category":"Place Value & Rounding","type":"numeric","grade":4,"source":"packet",
     "text":"Write 'sixty thousand, nine' in figures.",
     "options":None,"correct":60009,"hint":"Sixty thousand = 60,000. There are no hundreds or tens, just 9 ones.","active":True},
    {"subject":"Math","domain":"NBT","category":"Place Value & Rounding","type":"single","grade":4,"source":"packet",
     "text":"How do you write 36,924 in words?",
     "options":["A Thirty-six thousand, nine hundred twenty-four","B Three thousand, six hundred ninety-two","C Thirty-six thousand, two hundred ninety-four","D Three hundred sixty-nine thousand, twenty-four"],
     "correct":["A"],"hint":"36,924 → 36 thousand, then 924 (nine hundred twenty-four).","active":True},
    {"subject":"Math","domain":"NBT","category":"Place Value & Rounding","type":"numeric","grade":4,"source":"packet",
     "text":"Find the missing number in the pattern: 17,340,  27,340,  ___,  47,340,  57,340",
     "options":None,"correct":37340,"hint":"Each number increases by 10,000. 27,340 + 10,000 = 37,340.","active":True},
    {"subject":"Math","domain":"NBT","category":"Place Value & Rounding","type":"numeric","grade":4,"source":"packet",
     "text":"Find the missing number in the pattern: ___,  32,150,  42,150,  52,150,  62,150",
     "options":None,"correct":22150,"hint":"Each number increases by 10,000, so the missing number is 10,000 less than 32,150.","active":True},
    {"subject":"Math","domain":"NBT","category":"Place Value & Rounding","type":"numeric","grade":4,"source":"packet",
     "text":"What number goes in the blank?\n72,509 = 70,000 + ___ + 500 + 9",
     "options":None,"correct":2000,"hint":"72,509 − 70,000 − 500 − 9 = 2,000.","active":True},
    {"subject":"Math","domain":"NBT","category":"Place Value & Rounding","type":"numeric","grade":4,"source":"packet",
     "text":"What number goes in the blank?\n84,027 = ___ + 27",
     "options":None,"correct":84000,"hint":"84,027 − 27 = 84,000.","active":True},
    {"subject":"Math","domain":"NBT","category":"Place Value & Rounding","type":"numeric","grade":4,"source":"packet",
     "text":"In 63,281, what is the value of the digit 3?",
     "options":None,"correct":3000,"hint":"63,281 → 6=ten-thousands, 3=thousands, 2=hundreds, 8=tens, 1=ones. The 3 is worth 3,000.","active":True},
    {"subject":"Math","domain":"NBT","category":"Place Value & Rounding","type":"single","grade":4,"source":"packet",
     "text":"In 54,239, which digit is in the hundreds place?",
     "options":["A 5","B 4","C 2","D 3"],
     "correct":["C"],"hint":"54,239 → 5=ten-thousands, 4=thousands, 2=hundreds, 3=tens, 9=ones.","active":True},
    {"subject":"Math","domain":"NBT","category":"Place Value & Rounding","type":"numeric","grade":4,"source":"packet",
     "text":"Round $73,640 to the nearest $100.",
     "options":None,"correct":73600,"hint":"Look at the tens digit (4). Since it's less than 5, round down.","active":True},
]

# Factors, multiples, and product/quotient puzzles (like Review 1, items 10-12)
factors_and_multiples = [
    {"subject":"Math","domain":"OA","category":"Factors & Multiples","type":"single","grade":4,"source":"packet",
     "text":"What is the greatest factor of 54 that is less than 54?",
     "options":["A 18","B 27","C 9","D 6"],
     "correct":["B"],"hint":"Factors of 54: 1, 2, 3, 6, 9, 18, 27, 54. The greatest one less than 54 is 27.","active":True},
    {"subject":"Math","domain":"OA","category":"Factors & Multiples","type":"single","grade":4,"source":"packet",
     "text":"Which of the following is NOT a factor of 42?",
     "options":["A 6","B 7","C 8","D 14"],
     "correct":["C"],"hint":"Factors of 42: 1, 2, 3, 6, 7, 14, 21, 42. Notice 8 is missing from that list.","active":True},
    {"subject":"Math","domain":"OA","category":"Factors & Multiples","type":"numeric","grade":4,"source":"packet",
     "text":"What is the smallest common multiple of 4 and 6?",
     "options":None,"correct":12,"hint":"Multiples of 4: 4, 8, 12... Multiples of 6: 6, 12... The smallest they share is 12.","active":True},
    {"subject":"Math","domain":"OA","category":"Factors & Multiples","type":"numeric","grade":4,"source":"packet",
     "text":"What is the second smallest common multiple of 8 and 12?",
     "options":None,"correct":48,"hint":"Common multiples of 8 and 12: 24, 48, 72... The second smallest is 48.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,"source":"packet",
     "text":"The product of two numbers is 195. One of the numbers is 13. What is the other number?",
     "options":None,"correct":15,"hint":"Divide the product by the number you know: 195 ÷ 13.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,"source":"packet",
     "text":"The product of two numbers is 312. One of the numbers is 8. What is the other number?",
     "options":None,"correct":39,"hint":"Divide the product by the number you know: 312 ÷ 8.","active":True},
]

# Multi-step money word problems (like Review 1, item 13)
money_word_problems = [
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,"source":"packet",
     "text":"Jasmine saved $12,450. Marcus saved $9,000. How much more money did Jasmine save than Marcus?",
     "options":None,"correct":3450,"hint":"Subtract: $12,450 − $9,000.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,"source":"packet",
     "text":"A vendor had 42 boxes of oranges. There were 18 oranges in each box. If he sold all the oranges at 4 for $1, how much money did he receive?",
     "options":None,"correct":189,"hint":"Total oranges = 42 × 18 = 756. Divide by 4 to find how many groups of 4 he sold: 756 ÷ 4.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,"source":"packet",
     "text":"A shopkeeper had 36 boxes of pears. There were 20 pears in each box. If she sold all the pears at 4 for $1, how much money did she receive?",
     "options":None,"correct":180,"hint":"Total pears = 36 × 20 = 720. Divide by 4 to find how many groups of 4 she sold: 720 ÷ 4.","active":True},
]

# Adding fractions with LIKE denominators (like Exercise 17)
fractions_add_like = [
    {"subject":"Math","domain":"NF","category":"Adding Fractions","type":"single","grade":4,"source":"packet",
     "text":"1/3 + 1/3 = ?",
     "options":["A 2/3","B 1/3","C 2/6","D 1"],
     "correct":["A"],"hint":"When denominators match, add the numerators: 1 + 1 = 2, over 3.","active":True},
    {"subject":"Math","domain":"NF","category":"Adding Fractions","type":"single","grade":4,"source":"packet",
     "text":"1/5 + 3/5 = ?",
     "options":["A 4/5","B 3/5","C 4/10","D 1"],
     "correct":["A"],"hint":"When denominators match, add the numerators: 1 + 3 = 4, over 5.","active":True},
    {"subject":"Math","domain":"NF","category":"Adding Fractions","type":"single","grade":4,"source":"packet",
     "text":"2/7 + 4/7 = ?",
     "options":["A 6/7","B 6/14","C 2/7","D 1"],
     "correct":["A"],"hint":"When denominators match, add the numerators: 2 + 4 = 6, over 7.","active":True},
    {"subject":"Math","domain":"NF","category":"Adding Fractions","type":"single","grade":4,"source":"packet",
     "text":"3/9 + 2/9 = ? Write the answer in simplest form.",
     "options":["A 5/9","B 5/18","C 1/2","D 2/3"],
     "correct":["A"],"hint":"3 + 2 = 5, over 9. 5/9 is already in simplest form.","active":True},
    {"subject":"Math","domain":"NF","category":"Adding Fractions","type":"single","grade":4,"source":"packet",
     "text":"4/10 + 3/10 = ? Write the answer in simplest form.",
     "options":["A 7/10","B 7/20","C 3/5","D 4/5"],
     "correct":["A"],"hint":"4 + 3 = 7, over 10. 7/10 cannot be simplified further.","active":True},
    {"subject":"Math","domain":"NF","category":"Adding Fractions","type":"single","grade":4,"source":"packet",
     "text":"2/9 + 3/9 + 1/9 = ? Write the answer in simplest form.",
     "options":["A 2/3","B 6/9","C 1/3","D 5/9"],
     "correct":["A"],"hint":"2 + 3 + 1 = 6, over 9, which is 6/9. Simplify by dividing top and bottom by 3.","active":True},
]

# Adding fractions with UNLIKE denominators using equivalent fractions (like Exercise 18)
fractions_add_unlike = [
    {"subject":"Math","domain":"NF","category":"Adding Fractions","type":"single","grade":4,"source":"packet",
     "text":"1/4 + 1/8 = ?\n(Hint: rewrite 1/4 as an equivalent fraction with a denominator of 8 first.)",
     "options":["A 3/8","B 2/12","C 1/2","D 1/6"],
     "correct":["A"],"hint":"1/4 = 2/8. Then 2/8 + 1/8 = 3/8.","active":True},
    {"subject":"Math","domain":"NF","category":"Adding Fractions","type":"single","grade":4,"source":"packet",
     "text":"3/10 + 1/5 = ?\n(Hint: rewrite 1/5 as an equivalent fraction with a denominator of 10 first.)",
     "options":["A 1/2","B 5/10","C 4/15","D 2/5"],
     "correct":["A"],"hint":"1/5 = 2/10. Then 3/10 + 2/10 = 5/10, which simplifies to 1/2.","active":True},
    {"subject":"Math","domain":"NF","category":"Adding Fractions","type":"single","grade":4,"source":"packet",
     "text":"1/9 + 1/3 = ?\n(Hint: rewrite 1/3 as an equivalent fraction with a denominator of 9 first.)",
     "options":["A 4/9","B 2/12","C 1/12","D 2/9"],
     "correct":["A"],"hint":"1/3 = 3/9. Then 1/9 + 3/9 = 4/9.","active":True},
    {"subject":"Math","domain":"NF","category":"Adding Fractions","type":"single","grade":4,"source":"packet",
     "text":"2/5 + 3/10 = ?\n(Hint: rewrite 2/5 as an equivalent fraction with a denominator of 10 first.)",
     "options":["A 7/10","B 5/15","C 1/2","D 6/10"],
     "correct":["A"],"hint":"2/5 = 4/10. Then 4/10 + 3/10 = 7/10.","active":True},
    {"subject":"Math","domain":"NF","category":"Adding Fractions","type":"single","grade":4,"source":"packet",
     "text":"1/2 + 1/6 = ?\n(Hint: rewrite 1/2 as an equivalent fraction with a denominator of 6 first.)",
     "options":["A 2/3","B 4/6","C 1/8","D 1/3"],
     "correct":["A"],"hint":"1/2 = 3/6. Then 3/6 + 1/6 = 4/6, which simplifies to 2/3.","active":True},
]

# Subtracting fractions with LIKE denominators (like Exercise 19)
fractions_subtract = [
    {"subject":"Math","domain":"NF","category":"Subtracting Fractions","type":"single","grade":4,"source":"packet",
     "text":"5/7 − 2/7 = ?",
     "options":["A 3/7","B 3/14","C 2/7","D 1/7"],
     "correct":["A"],"hint":"When denominators match, subtract the numerators: 5 − 2 = 3, over 7.","active":True},
    {"subject":"Math","domain":"NF","category":"Subtracting Fractions","type":"single","grade":4,"source":"packet",
     "text":"7/9 − 4/9 = ? Write the answer in simplest form.",
     "options":["A 1/3","B 3/9","C 2/9","D 4/9"],
     "correct":["A"],"hint":"7 − 4 = 3, over 9, which is 3/9. Simplify by dividing top and bottom by 3.","active":True},
    {"subject":"Math","domain":"NF","category":"Subtracting Fractions","type":"single","grade":4,"source":"packet",
     "text":"9/10 − 3/10 = ? Write the answer in simplest form.",
     "options":["A 3/5","B 6/10","C 2/5","D 1/2"],
     "correct":["A"],"hint":"9 − 3 = 6, over 10, which is 6/10. Simplify by dividing top and bottom by 2.","active":True},
    {"subject":"Math","domain":"NF","category":"Subtracting Fractions","type":"single","grade":4,"source":"packet",
     "text":"11/12 − 7/12 = ? Write the answer in simplest form.",
     "options":["A 1/3","B 4/12","C 1/2","D 2/3"],
     "correct":["A"],"hint":"11 − 7 = 4, over 12, which is 4/12. Simplify by dividing top and bottom by 4.","active":True},
    {"subject":"Math","domain":"NF","category":"Subtracting Fractions","type":"single","grade":4,"source":"packet",
     "text":"5/8 − 3/8 = ? Write the answer in simplest form.",
     "options":["A 1/4","B 2/8","C 3/8","D 1/2"],
     "correct":["A"],"hint":"5 − 3 = 2, over 8, which is 2/8. Simplify by dividing top and bottom by 2.","active":True},
    {"subject":"Math","domain":"NF","category":"Subtracting Fractions","type":"single","grade":4,"source":"packet",
     "text":"1 − 3/7 = ?",
     "options":["A 4/7","B 3/7","C 1/7","D 3/4"],
     "correct":["A"],"hint":"Think of 1 as 7/7. Then 7/7 − 3/7 = 4/7.","active":True},
]

all_packet_questions = (
    multiplication +
    place_value_review +
    factors_and_multiples +
    money_word_problems +
    fractions_add_like +
    fractions_add_unlike +
    fractions_subtract
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
