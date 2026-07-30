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

# ── Grade 4 · Math · Batch 2 ─────────────────────────────────────────

# OA: Multi-step word problems
oa_word_problems = [
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,
     "text":"Maya had 245 stickers. She gave 87 stickers to a friend and then bought 3 packs of 12 more stickers. How many stickers does she have now?",
     "options":None,"correct":194,"hint":"245 − 87 = 158. Then add 3 × 12 = 36 new stickers.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,
     "text":"A baker makes 6 trays of 24 muffins each. She sells 3 dozen muffins. How many muffins are left?",
     "options":None,"correct":108,"hint":"Total muffins = 6 × 24 = 144. She sold 3 dozen = 36. Subtract: 144 − 36.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,
     "text":"Ethan read 18 pages a day for 5 days, then 25 pages a day for 3 more days. How many total pages did he read?",
     "options":None,"correct":165,"hint":"First 5 days: 18 × 5 = 90 pages. Next 3 days: 25 × 3 = 75 pages. Add them.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,
     "text":"A store had 500 pencils. It sold 45 pencils each day for 6 days. How many pencils are left?",
     "options":None,"correct":230,"hint":"Pencils sold = 45 × 6 = 270. Subtract from the starting amount: 500 − 270.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,
     "text":"Four friends split a $96 restaurant bill evenly. Each friend also leaves an extra $4 tip. How much does each person pay in total?",
     "options":None,"correct":28,"hint":"Each person's share of the bill = 96 ÷ 4 = 24. Add the $4 tip.","active":True},
]

# OA: What's My Sign? — determine the missing operations
oa_whats_my_sign = [
    {"subject":"Math","domain":"OA","category":"What's My Sign","type":"single","grade":4,
     "text":"What's My Sign? Fill in the operations to make it true:\n20 ○ 4 ○ 6 = 11",
     "options":["A divide, then add","B multiply, then subtract","C add, then divide","D subtract, then multiply"],
     "correct":["A"],"hint":"Try: 20 ÷ 4 = 5, then 5 + 6 = 11.","active":True},
    {"subject":"Math","domain":"OA","category":"What's My Sign","type":"single","grade":4,
     "text":"What's My Sign? Fill in the operations to make it true:\n9 ○ 6 ○ 3 = 51",
     "options":["A add, then multiply","B multiply, then subtract","C divide, then add","D subtract, then multiply"],
     "correct":["B"],"hint":"Try: 9 × 6 = 54, then 54 − 3 = 51.","active":True},
    {"subject":"Math","domain":"OA","category":"What's My Sign","type":"single","grade":4,
     "text":"What's My Sign? Fill in the operations to make it true:\n12 ○ 3 ○ 9 = 45",
     "options":["A multiply, then add","B add, then subtract","C divide, then multiply","D subtract, then divide"],
     "correct":["A"],"hint":"Try: 12 × 3 = 36, then 36 + 9 = 45.","active":True},
    {"subject":"Math","domain":"OA","category":"What's My Sign","type":"single","grade":4,
     "text":"What's My Sign? Fill in the operations to make it true:\n50 ○ 14 ○ 4 = 9",
     "options":["A add, then multiply","B multiply, then subtract","C subtract, then divide","D divide, then add"],
     "correct":["C"],"hint":"Try: 50 − 14 = 36, then 36 ÷ 4 = 9.","active":True},
    {"subject":"Math","domain":"OA","category":"What's My Sign","type":"single","grade":4,
     "text":"What's My Sign? Fill in the operations to make it true:\n36 ○ 6 ○ 5 = 30",
     "options":["A divide, then multiply","B multiply, then add","C subtract, then multiply","D add, then divide"],
     "correct":["A"],"hint":"Try: 36 ÷ 6 = 6, then 6 × 5 = 30.","active":True},
]

# NBT: Place value, rounding, multi-digit multiplication/division
nbt_questions = [
    {"subject":"Math","domain":"NBT","category":"Place Value & Rounding","type":"numeric","grade":4,
     "text":"What is 7,482 rounded to the nearest hundred?",
     "options":None,"correct":7500,"hint":"Look at the tens digit (8). Since it's 5 or more, round the hundreds digit up.","active":True},
    {"subject":"Math","domain":"NBT","category":"Place Value & Rounding","type":"numeric","grade":4,
     "text":"What is 3,256 rounded to the nearest thousand?",
     "options":None,"correct":3000,"hint":"Look at the hundreds digit (2). Since it's less than 5, round down to 3,000.","active":True},
    {"subject":"Math","domain":"NBT","category":"Place Value & Rounding","type":"single","grade":4,
     "text":"In the number 58,392, what digit is in the thousands place?",
     "options":["A 5","B 8","C 3","D 9"],
     "correct":["B"],"hint":"58,392 → 5=ten-thousands, 8=thousands, 3=hundreds, 9=tens, 2=ones.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,
     "text":"Multiply: 234 × 6",
     "options":None,"correct":1404,"hint":"Break it apart: 200×6=1,200 and 34×6=204. Add them together.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,
     "text":"Divide: 936 ÷ 8",
     "options":None,"correct":117,"hint":"8 × 100 = 800, leaving 136. 8 × 17 = 136. So 100 + 17 = 117.","active":True},
    {"subject":"Math","domain":"NBT","category":"Place Value & Rounding","type":"single","grade":4,
     "text":"Which number is greatest?",
     "options":["A 45,672","B 45,067","C 45,720","D 44,999"],
     "correct":["C"],"hint":"Compare digit by digit from the left. 45,720 has the largest hundreds digit among numbers starting with 45,***.","active":True},
    {"subject":"Math","domain":"NBT","category":"Place Value & Rounding","type":"numeric","grade":4,
     "text":"What is 4,000 + 300 + 20 + 5 written in standard form?",
     "options":None,"correct":4325,"hint":"Line up the place values: thousands, hundreds, tens, ones.","active":True},
    {"subject":"Math","domain":"NBT","category":"Place Value & Rounding","type":"single","grade":4,
     "text":"Round 68,459 to the nearest ten thousand.",
     "options":["A 60,000","B 70,000","C 68,000","D 69,000"],
     "correct":["B"],"hint":"Look at the thousands digit (8). Since it's 5 or more, round the ten-thousands digit up.","active":True},
    {"subject":"Math","domain":"NBT","category":"Multi-Digit Arithmetic","type":"numeric","grade":4,
     "text":"Multiply: 47 × 32",
     "options":None,"correct":1504,"hint":"Break it apart: 47 × 30 = 1,410 and 47 × 2 = 94. Add them together.","active":True},
    {"subject":"Math","domain":"NBT","category":"Place Value & Rounding","type":"numeric","grade":4,
     "text":"A number has a 6 in the ten-thousands place, 3 in the thousands place, 0 in the hundreds place, 9 in the tens place, and 4 in the ones place. What is the number?",
     "options":None,"correct":63094,"hint":"Write the digits in order from the ten-thousands place down to the ones place.","active":True},
]

# NF: Fractions and decimals
nf_questions = [
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","grade":4,
     "text":"Which fraction is equivalent to 3/4?",
     "options":["A 6/8","B 4/5","C 5/6","D 2/3"],
     "correct":["A"],"hint":"Multiply the numerator and denominator of 3/4 by 2 to get 6/8.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","grade":4,
     "text":"Which symbol makes this true?\n3/8 ○ 5/8",
     "options":["A <","B >","C =","D Cannot be compared"],
     "correct":["A"],"hint":"When denominators are the same, compare the numerators: 3 is less than 5.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","grade":4,
     "text":"What is 1/2 + 1/4?",
     "options":["A 2/6","B 3/4","C 1/6","D 2/3"],
     "correct":["B"],"hint":"Rewrite 1/2 as 2/4, then add: 2/4 + 1/4 = 3/4.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","grade":4,
     "text":"Which decimal is equivalent to 3/10?",
     "options":["A 0.3","B 3.0","C 0.03","D 3.10"],
     "correct":["A"],"hint":"Tenths are written as one digit after the decimal point: 3/10 = 0.3.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","grade":4,
     "text":"Which fraction is greater: 2/3 or 3/5?",
     "options":["A 2/3","B 3/5","C They are equal","D Cannot be determined"],
     "correct":["A"],"hint":"Find a common denominator (15): 2/3 = 10/15 and 3/5 = 9/15. 10/15 is greater.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","grade":4,
     "text":"What is 4/6 written in simplest form?",
     "options":["A 2/3","B 1/2","C 4/6","D 3/4"],
     "correct":["A"],"hint":"Divide both the numerator and denominator by their greatest common factor, 2.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","grade":4,
     "text":"Which decimal is equivalent to 7/10?",
     "options":["A 0.07","B 7.10","C 0.7","D 1.7"],
     "correct":["C"],"hint":"Tenths are written as one digit after the decimal point: 7/10 = 0.7.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","grade":4,
     "text":"What is 5/6 − 1/6 written in simplest form?",
     "options":["A 4/6","B 2/3","C 4/5","D 5/5"],
     "correct":["B"],"hint":"5/6 − 1/6 = 4/6, which simplifies to 2/3.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"numeric","grade":4,
     "text":"A recipe uses 3/4 cup of sugar per batch. If Grace makes 4 batches, how many whole cups of sugar does she need?",
     "options":None,"correct":3,"hint":"Multiply 3/4 by 4: 3/4 × 4 = 12/4 = 3 cups.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"numeric","grade":4,
     "text":"Of the 20 students in class, 1/4 brought their lunch. How many students brought their lunch?",
     "options":None,"correct":5,"hint":"Find 1/4 of 20: 20 ÷ 4 = 5.","active":True},
]

# MD: Measurement and data
md_questions = [
    {"subject":"Math","domain":"MD","category":"Measurement","type":"numeric","grade":4,
     "text":"A movie starts at 2:15 PM and ends at 4:05 PM. How many minutes long is the movie?",
     "options":None,"correct":110,"hint":"From 2:15 to 4:15 is 120 minutes. Subtract the extra 10 minutes: 120 − 10.","active":True},
    {"subject":"Math","domain":"MD","category":"Measurement","type":"numeric","grade":4,
     "text":"A rectangular garden is 12 feet long and 7 feet wide. What is its perimeter in feet?",
     "options":None,"correct":38,"hint":"Perimeter = 2 × (length + width) = 2 × (12 + 7).","active":True},
    {"subject":"Math","domain":"MD","category":"Measurement","type":"numeric","grade":4,
     "text":"A rectangular room is 9 feet by 6 feet. What is its area in square feet?",
     "options":None,"correct":54,"hint":"Area = length × width = 9 × 6.","active":True},
    {"subject":"Math","domain":"MD","category":"Measurement","type":"single","grade":4,
     "text":"How many inches are in 3 feet?",
     "options":["A 24","B 30","C 36","D 42"],
     "correct":["C"],"hint":"There are 12 inches in 1 foot. Multiply: 12 × 3.","active":True},
    {"subject":"Math","domain":"MD","category":"Measurement","type":"numeric","grade":4,
     "text":"A recipe calls for 2 cups of flour. If Diego wants to triple the recipe, how many cups of flour does he need?",
     "options":None,"correct":6,"hint":"Multiply the original amount by 3: 2 × 3.","active":True},
    {"subject":"Math","domain":"MD","category":"Measurement","type":"single","grade":4,
     "text":"How many minutes are in 2 and a half hours?",
     "options":["A 120","B 130","C 150","D 180"],
     "correct":["C"],"hint":"1 hour = 60 minutes, so 2 hours = 120 minutes. Add half an hour (30 minutes).","active":True},
    {"subject":"Math","domain":"MD","category":"Measurement","type":"numeric","grade":4,
     "text":"Convert 5 pounds to ounces. (1 pound = 16 ounces)",
     "options":None,"correct":80,"hint":"Multiply: 5 × 16.","active":True},
    {"subject":"Math","domain":"MD","category":"Measurement","type":"single","grade":4,
     "text":"Which unit would you use to measure the length of a football field?",
     "options":["A Inches","B Yards","C Ounces","D Cups"],
     "correct":["B"],"hint":"Yards are used for measuring longer distances, like a football field.","active":True},
    {"subject":"Math","domain":"MD","category":"Measurement","type":"numeric","grade":4,
     "text":"A train leaves the station at 9:40 AM and arrives at 11:05 AM. How many minutes was the trip?",
     "options":None,"correct":85,"hint":"From 9:40 to 10:40 is 60 minutes. From 10:40 to 11:05 is 25 more minutes. Add them.","active":True},
    {"subject":"Math","domain":"MD","category":"Measurement","type":"numeric","grade":4,
     "text":"A pool is shaped like a rectangle, 25 meters long and 10 meters wide. What is the perimeter of the pool in meters?",
     "options":None,"correct":70,"hint":"Perimeter = 2 × (length + width) = 2 × (25 + 10).","active":True},
]

# G: Geometry
g_questions = [
    {"subject":"Math","domain":"G","category":"Geometry","type":"single","grade":4,
     "text":"Which term describes two lines that cross at a right angle?",
     "options":["A Parallel","B Perpendicular","C Intersecting only","D Symmetrical"],
     "correct":["B"],"hint":"Perpendicular lines meet and form a 90-degree angle.","active":True},
    {"subject":"Math","domain":"G","category":"Geometry","type":"single","grade":4,
     "text":"Which term describes two lines that never meet, no matter how far they extend?",
     "options":["A Perpendicular","B Parallel","C Adjacent","D Congruent"],
     "correct":["B"],"hint":"Parallel lines always stay the same distance apart and never cross.","active":True},
    {"subject":"Math","domain":"G","category":"Geometry","type":"single","grade":4,
     "text":"An angle that measures exactly 90 degrees is called a(n) ___ angle.",
     "options":["A Acute","B Right","C Obtuse","D Straight"],
     "correct":["B"],"hint":"A right angle looks like the corner of a square.","active":True},
    {"subject":"Math","domain":"G","category":"Geometry","type":"single","grade":4,
     "text":"An angle that measures less than 90 degrees is called a(n) ___ angle.",
     "options":["A Acute","B Right","C Obtuse","D Straight"],
     "correct":["A"],"hint":"Acute angles are smaller and sharper than a right angle.","active":True},
    {"subject":"Math","domain":"G","category":"Geometry","type":"single","grade":4,
     "text":"An angle that measures more than 90 degrees but less than 180 degrees is called a(n) ___ angle.",
     "options":["A Acute","B Right","C Obtuse","D Straight"],
     "correct":["C"],"hint":"Obtuse angles are wider than a right angle but not a straight line.","active":True},
    {"subject":"Math","domain":"G","category":"Geometry","type":"single","grade":4,
     "text":"A shape with exactly 4 right angles and 4 equal sides is a ___.",
     "options":["A Square","B Rectangle","C Rhombus","D Trapezoid"],
     "correct":["A"],"hint":"A rectangle has 4 right angles, but only a square also requires all 4 sides to be equal.","active":True},
    {"subject":"Math","domain":"G","category":"Geometry","type":"single","grade":4,
     "text":"How many lines of symmetry does a square have?",
     "options":["A 2","B 4","C 1","D 0"],
     "correct":["B"],"hint":"A square can be folded evenly along 2 diagonals and 2 lines through the middle of each side.","active":True},
    {"subject":"Math","domain":"G","category":"Geometry","type":"single","grade":4,
     "text":"A triangle with all three sides of different lengths is called a(n) ___ triangle.",
     "options":["A Equilateral","B Isosceles","C Scalene","D Right"],
     "correct":["C"],"hint":"Scalene triangles have no equal sides.","active":True},
    {"subject":"Math","domain":"G","category":"Geometry","type":"single","grade":4,
     "text":"A triangle with two sides of equal length is called a(n) ___ triangle.",
     "options":["A Equilateral","B Isosceles","C Scalene","D Obtuse"],
     "correct":["B"],"hint":"Isosceles triangles have exactly two equal sides.","active":True},
    {"subject":"Math","domain":"G","category":"Geometry","type":"single","grade":4,
     "text":"Which figure has no straight sides and no angles?",
     "options":["A Circle","B Triangle","C Hexagon","D Square"],
     "correct":["A"],"hint":"A circle is a curved shape with no straight edges or corners.","active":True},
]

all_math_batch2 = oa_word_problems + oa_whats_my_sign + nbt_questions + nf_questions + md_questions + g_questions

print(f"Total Grade 4 Math batch 2 questions: {len(all_math_batch2)}")
print(f"  Numeric: {sum(1 for q in all_math_batch2 if q['type']=='numeric')}")
print(f"  Single:  {sum(1 for q in all_math_batch2 if q['type']=='single')}")
by_domain = {}
for q in all_math_batch2:
    by_domain[q['domain']] = by_domain.get(q['domain'], 0) + 1
for d, n in sorted(by_domain.items()):
    print(f"  {d}: {n}")
print()

print("Uploading Grade 4 Math batch 2 questions...")
for i in range(0, len(all_math_batch2), 25):
    batch = all_math_batch2[i:i+25]
    upload_batch(batch)

print("Done!")
