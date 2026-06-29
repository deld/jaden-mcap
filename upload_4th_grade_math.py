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

# ── Grade 4 · Math · OA ──────────────────────────────────────────────

# Numeric: multi-step word problems from the Week 1 packet
numeric_oa = [
    # Road Trip Word Problems (packet p.9)
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,
     "text":"Joey and his family took a road trip. On Monday they drove 68 miles, on Tuesday 25 miles, and on Wednesday 33 miles. What was the average number of miles they drove per day?",
     "options":None,"correct":42,"hint":"Add all three days (68+25+33=126), then divide by 3 days.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,
     "text":"Joey's family drove for 3 hours on Monday, 1 and a half hours on Tuesday, and 1 and a half hours on Wednesday. How many total minutes did they spend driving?",
     "options":None,"correct":360,"hint":"Add the hours (3+1.5+1.5=6 hours), then multiply by 60 minutes per hour.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,
     "text":"Joey's family will travel 1,323 miles to the Grand Canyon, then 846 miles to Yellowstone, then 2,166 miles to the Washington Monument. How many total miles will they travel?",
     "options":None,"correct":4335,"hint":"Add all three distances: 1,323 + 846 + 2,166.","active":True},

    # Family Vacation Multiplication (packet p.16)
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,
     "text":"Gas costs $3 per gallon. The Smiths' tank holds 16 gallons and already has 3 gallons in it. How much will it cost to fill the tank completely?",
     "options":None,"correct":39,"hint":"Find gallons needed (16−3=13), then multiply by $3.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,
     "text":"An airplane has rows of 2, 3, and 2 seats (7 seats per row). There are 51 rows and 13 seats are empty. How many passengers are on board?",
     "options":None,"correct":344,"hint":"Total seats = 51 × 7 = 357. Subtract 13 empty seats.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,
     "text":"The Smiths flew for 14 hours. The airplane travels approximately 512 miles per hour. About how many miles did they travel in all?",
     "options":None,"correct":7168,"hint":"Multiply speed by time: 512 × 14.","active":True},

    # Math Skills: Word Problems (packet p.22)
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,
     "text":"Jean earned $157 in May, $210 in June, $377 in July, and $145 in August. A computer costs $695 and a printer costs $95. How much money will Jean have left after buying both?",
     "options":None,"correct":99,"hint":"Total earned = 157+210+377+145. Total cost = 695+95. Subtract cost from earnings.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,
     "text":"Maria traveled 536 miles on day 1, 259 miles on day 2, and 632 miles on day 3 in a video game. What is the total number of miles Maria traveled in the game?",
     "options":None,"correct":1427,"hint":"Add all three days: 536 + 259 + 632.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,
     "text":"Timmy logged 1,525 minutes online in January. In February he logged 5,182 minutes doing research. How many more minutes did Timmy log in February than in January?",
     "options":None,"correct":3657,"hint":"Subtract: 5,182 − 1,525.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,
     "text":"A city's population increased by 5,765 people in the first 4 years, 2,789 people in the next 2 years, and 8,723 people in the last 4 years. What is the total population increase over 10 years?",
     "options":None,"correct":17277,"hint":"Add all three increases: 5,765 + 2,789 + 8,723.","active":True},

    # Word Problems in Winter: Multi-Step Mixed Operations (packet p.28)
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,
     "text":"On Saturday, 4 groups of 5 people went to a ski resort restaurant. Everyone ordered hot chocolate. Rebecca, Malaki, and Jeffrey each ordered an extra cup. How many cups of hot chocolate were drunk in total?",
     "options":None,"correct":23,"hint":"Groups × people = 20 cups. Add 3 extra cups ordered by Rebecca, Malaki, and Jeffrey.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,
     "text":"On a snow day, 8 kids built snowmen using 2 buttons each for eyes. Then 7 more kids joined and also used 2 buttons each for their snowmen. How many buttons were used in all?",
     "options":None,"correct":30,"hint":"Total kids = 8 + 7 = 15. Each used 2 buttons. Multiply: 15 × 2.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,
     "text":"Mr. Ackerman's 9 boys went outside wearing 2 gloves each. Isaiah and Michael each lost 1 glove while outside. How many gloves did the boys bring back into the classroom?",
     "options":None,"correct":16,"hint":"Total gloves = 9 × 2 = 18. Subtract 2 lost gloves (one each for Isaiah and Michael).","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,
     "text":"The Jerico family (2 parents and 4 children) went ice skating. Each person had ice skates. They also brought 1 extra pair in case anyone else wanted to join. How many ice skates did the family bring?",
     "options":None,"correct":14,"hint":"Family members = 2 + 4 = 6. Each needs 2 skates (6×2=12). Add 1 extra pair (2 skates).","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,
     "text":"It snowed 3 inches each day for a week (7 days). By the following Monday, 6 inches had melted. How many inches of snow were still on the ground?",
     "options":None,"correct":15,"hint":"Total snow = 3 × 7 = 21 inches. Subtract 6 inches that melted.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"numeric","grade":4,
     "text":"Sheena baked 112 cookies. She kept 16 cookies at home for her family and shared the rest evenly with her 8 friends. How many cookies did each friend get?",
     "options":None,"correct":12,"hint":"Cookies shared = 112 − 16 = 96. Divide by 8 friends.","active":True},

    # Number Riddles / What's My Number? (packet p.35)
    {"subject":"Math","domain":"OA","category":"Number Riddles","type":"numeric","grade":4,
     "text":"What's My Number? Add 9 to me. Then multiply by 3. If you subtract 16 and then add 7, you get 27. What number am I?",
     "options":None,"correct":3,"hint":"Work backward: 27−7=20, 20+16=36, 36÷3=12, 12−9=3.","active":True},
    {"subject":"Math","domain":"OA","category":"Number Riddles","type":"numeric","grade":4,
     "text":"What's My Number? Add 5 to me. Then divide by 7. If you add 12 and then subtract 7, you get 10. What number am I?",
     "options":None,"correct":30,"hint":"Work backward: 10+7=17, 17−12=5, 5×7=35, 35−5=30.","active":True},
    {"subject":"Math","domain":"OA","category":"Number Riddles","type":"numeric","grade":4,
     "text":"What's My Number? Multiply me by 4. Then subtract 13. If you divide by 3 and add 17, you get 22. What number am I?",
     "options":None,"correct":7,"hint":"Work backward: 22−17=5, 5×3=15, 15+13=28, 28÷4=7.","active":True},
    {"subject":"Math","domain":"OA","category":"Number Riddles","type":"numeric","grade":4,
     "text":"What's My Number? Subtract 6 from me. Then multiply by 2. If you subtract 40 and divide by 4, you get 8. What number am I?",
     "options":None,"correct":42,"hint":"Work backward: 8×4=32, 32+40=72, 72÷2=36, 36+6=42.","active":True},

    # Mathematical Mindbenders (packet p.29)
    {"subject":"Math","domain":"OA","category":"Number Riddles","type":"numeric","grade":4,
     "text":"Mathematical Mindbender: What is the LARGER of two numbers that have a product of 48 and, when the larger is divided by the smaller, give a quotient of 3?",
     "options":None,"correct":12,"hint":"Let x = larger, y = smaller. x×y=48 and x÷y=3, so x=3y. Then 3y×y=48 → y²=16 → y=4 → x=12.","active":True},
]

# Single-choice: What's My Sign? — determine the missing operations (packet p.17)
single_whats_my_sign = [
    {"subject":"Math","domain":"OA","category":"What's My Sign","type":"single","grade":4,
     "text":"What's My Sign? Fill in the operations to make it true:\n15 ○ 11 ○ 3 = 7",
     "options":["A subtract, then add","B add, then subtract","C multiply, then divide","D divide, then multiply"],
     "correct":["A"],"hint":"Try: 15 − 11 = 4, then 4 + 3 = 7.","active":True},
    {"subject":"Math","domain":"OA","category":"What's My Sign","type":"single","grade":4,
     "text":"What's My Sign? Fill in the operations to make it true:\n22 ○ 22 ○ 4 = 4",
     "options":["A multiply, then add","B divide, then add","C subtract, then add","D add, then subtract"],
     "correct":["C"],"hint":"Try: 22 − 22 = 0, then 0 + 4 = 4.","active":True},
    {"subject":"Math","domain":"OA","category":"What's My Sign","type":"single","grade":4,
     "text":"What's My Sign? Fill in the operations to make it true:\n16 ○ 40 ○ 16 = 40",
     "options":["A subtract, then add","B multiply, then subtract","C add, then subtract","D divide, then multiply"],
     "correct":["C"],"hint":"Try: 16 + 40 = 56, then 56 − 16 = 40.","active":True},
    {"subject":"Math","domain":"OA","category":"What's My Sign","type":"single","grade":4,
     "text":"What's My Sign? Fill in the operations to make it true:\n32 ○ 4 ○ 3 = 24",
     "options":["A multiply, then add","B subtract, then multiply","C add, then divide","D divide, then multiply"],
     "correct":["D"],"hint":"Try: 32 ÷ 4 = 8, then 8 × 3 = 24.","active":True},
    {"subject":"Math","domain":"OA","category":"What's My Sign","type":"single","grade":4,
     "text":"What's My Sign? Fill in the operations to make it true:\n10 ○ 5 ○ 2 = 100",
     "options":["A add, then multiply","B multiply, then multiply","C divide, then multiply","D subtract, then multiply"],
     "correct":["B"],"hint":"Try: 10 × 5 = 50, then 50 × 2 = 100.","active":True},
    {"subject":"Math","domain":"OA","category":"What's My Sign","type":"single","grade":4,
     "text":"What's My Sign? Fill in the operations to make it true:\n64 ○ 8 ○ 5 = 40",
     "options":["A multiply, then subtract","B subtract, then multiply","C divide, then multiply","D add, then divide"],
     "correct":["C"],"hint":"Try: 64 ÷ 8 = 8, then 8 × 5 = 40.","active":True},
    {"subject":"Math","domain":"OA","category":"What's My Sign","type":"single","grade":4,
     "text":"What's My Sign? Fill in the operations to make it true:\n6 ○ 7 ○ 20 = 22",
     "options":["A add, then subtract","B divide, then add","C multiply, then subtract","D subtract, then add"],
     "correct":["C"],"hint":"Try: 6 × 7 = 42, then 42 − 20 = 22.","active":True},
    {"subject":"Math","domain":"OA","category":"What's My Sign","type":"single","grade":4,
     "text":"What's My Sign? Fill in the operations to make it true:\n12 ○ 4 ○ 8 = 56",
     "options":["A add, then multiply","B multiply, then add","C divide, then add","D subtract, then multiply"],
     "correct":["B"],"hint":"Try: 12 × 4 = 48, then 48 + 8 = 56.","active":True},
    {"subject":"Math","domain":"OA","category":"What's My Sign","type":"single","grade":4,
     "text":"What's My Sign? Fill in the operations to make it true:\n43 ○ 21 ○ 17 = 47",
     "options":["A subtract, then add","B add, then subtract","C multiply, then divide","D divide, then subtract"],
     "correct":["B"],"hint":"Try: 43 + 21 = 64, then 64 − 17 = 47.","active":True},
    {"subject":"Math","domain":"OA","category":"What's My Sign","type":"single","grade":4,
     "text":"What's My Sign? Fill in the operations to make it true:\n9 ○ 1 ○ 8 = 72",
     "options":["A add, then multiply","B subtract, then multiply","C divide, then multiply","D multiply, then add"],
     "correct":["C"],"hint":"Try: 9 ÷ 1 = 9, then 9 × 8 = 72.","active":True},
    {"subject":"Math","domain":"OA","category":"What's My Sign","type":"single","grade":4,
     "text":"What's My Sign? Fill in the operations to make it true:\n78 ○ 6 ○ 3 = 39",
     "options":["A subtract, then multiply","B divide, then multiply","C multiply, then subtract","D add, then divide"],
     "correct":["B"],"hint":"Try: 78 ÷ 6 = 13, then 13 × 3 = 39.","active":True},
    {"subject":"Math","domain":"OA","category":"What's My Sign","type":"single","grade":4,
     "text":"What's My Sign? Fill in the operations to make it true:\n10 ○ 3 ○ 3 = 10",
     "options":["A multiply, then divide","B add, then subtract","C divide, then add","D subtract, then multiply"],
     "correct":["B"],"hint":"Try: 10 + 3 = 13, then 13 − 3 = 10.","active":True},
    {"subject":"Math","domain":"OA","category":"What's My Sign","type":"single","grade":4,
     "text":"What's My Sign? Fill in the operations to make it true:\n52 ○ 2 ○ 31 = 73",
     "options":["A divide, then add","B add, then multiply","C multiply, then subtract","D subtract, then divide"],
     "correct":["C"],"hint":"Try: 52 × 2 = 104, then 104 − 31 = 73.","active":True},
    {"subject":"Math","domain":"OA","category":"What's My Sign","type":"single","grade":4,
     "text":"What's My Sign? Fill in the operations to make it true:\n2 ○ 7 ○ 3 = 42",
     "options":["A add, then multiply","B multiply, then multiply","C divide, then subtract","D subtract, then add"],
     "correct":["B"],"hint":"Try: 2 × 7 = 14, then 14 × 3 = 42.","active":True},
]

# Single-choice: word problem multiple choice (4th grade level)
single_word_problems = [
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"single","grade":4,
     "text":"A school store sells pencils for $0.25 each. Elena buys 4 pencils and an eraser for $0.75. How much does she pay in all?",
     "options":["A $1.50","B $1.75","C $1.00","D $2.00"],
     "correct":["B"],"hint":"Pencils: 4 × $0.25 = $1.00. Add $0.75 for the eraser.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"single","grade":4,
     "text":"A factory produces 512 widgets per hour. How many widgets does it produce in 8 hours?",
     "options":["A 3,096","B 4,096","C 4,196","D 5,012"],
     "correct":["B"],"hint":"Multiply: 512 × 8.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"single","grade":4,
     "text":"Marcus has 1,248 baseball cards. He organizes them equally into 6 binders. How many cards are in each binder?",
     "options":["A 186","B 200","C 208","D 216"],
     "correct":["C"],"hint":"Divide: 1,248 ÷ 6.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"single","grade":4,
     "text":"A bookstore sells 3 books for $7 each and 5 magazines for $3 each. What is the total cost?",
     "options":["A $30","B $36","C $32","D $28"],
     "correct":["B"],"hint":"Books: 3 × $7 = $21. Magazines: 5 × $3 = $15. Add them.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"single","grade":4,
     "text":"A movie theater has 24 rows with 18 seats each. On Friday night, 315 seats were filled. How many seats were empty?",
     "options":["A 107","B 115","C 117","D 121"],
     "correct":["C"],"hint":"Total seats = 24 × 18 = 432. Subtract 315 filled seats.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"single","grade":4,
     "text":"Layla earns $9 per hour babysitting. She babysits for 6 hours on Saturday and 4 hours on Sunday. How much does she earn over the weekend?",
     "options":["A $72","B $81","C $90","D $54"],
     "correct":["C"],"hint":"Total hours = 6 + 4 = 10. Multiply: 10 × $9.","active":True},
    {"subject":"Math","domain":"OA","category":"Word Problems","type":"single","grade":4,
     "text":"A farmer has 4 fields. Each field has 125 apple trees. He expects each tree to produce 48 apples. How many apples will the 4 fields produce in total?",
     "options":["A 19,200","B 20,000","C 24,000","D 18,400"],
     "correct":["C"],"hint":"Trees total = 4 × 125 = 500. Then 500 × 48.","active":True},
]

all_math = numeric_oa + single_whats_my_sign + single_word_problems

print(f"Total Grade 4 Math questions: {len(all_math)}")
print(f"  Numeric: {sum(1 for q in all_math if q['type']=='numeric')}")
print(f"  Single:  {sum(1 for q in all_math if q['type']=='single')}")
print()

print("Uploading Grade 4 Math questions...")
for i in range(0, len(all_math), 25):
    batch = all_math[i:i+25]
    upload_batch(batch)

print("Done!")
