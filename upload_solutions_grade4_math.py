import json, urllib.request, urllib.parse, time

BASE = "https://zvffmucghcrqackghhlf.supabase.co/rest/v1"
KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp2ZmZtdWNnaGNycWFja2doaGxmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY3MjkyNTIsImV4cCI6MjA5MjMwNTI1Mn0.eJHX6LmInRdBd5nt9t_jBJwILGEQ6_SeN6ADorlsWic"
HEADERS = {"Content-Type":"application/json","apikey":KEY,"Authorization":f"Bearer {KEY}","Prefer":"return=minimal"}

# Maps question text → worked solution
SOLUTIONS = {
    # ── Road Trip Word Problems ──────────────────────────────────────────
    "Joey and his family took a road trip. On Monday they drove 68 miles, on Tuesday 25 miles, and on Wednesday 33 miles. What was the average number of miles they drove per day?":
        "Step 1: Add up all the miles.\n  68 + 25 + 33 = 126 miles total\n\nStep 2: Divide by the number of days (3).\n  126 ÷ 3 = 42\n\nThe average was 42 miles per day.",

    "Joey's family drove for 3 hours on Monday, 1 and a half hours on Tuesday, and 1 and a half hours on Wednesday. How many total minutes did they spend driving?":
        "Step 1: Add up the hours.\n  3 + 1.5 + 1.5 = 6 hours total\n\nStep 2: Convert hours to minutes (1 hour = 60 minutes).\n  6 × 60 = 360\n\nThey spent 360 minutes driving.",

    "Joey's family will travel 1,323 miles to the Grand Canyon, then 846 miles to Yellowstone, then 2,166 miles to the Washington Monument. How many total miles will they travel?":
        "Step 1: Add all three distances.\n  1,323\n+   846\n+ 2,166\n-------\n  4,335\n\nThey will travel 4,335 miles in total.",

    # ── Family Vacation Multiplication ───────────────────────────────────
    "Gas costs $3 per gallon. The Smiths' tank holds 16 gallons and already has 3 gallons in it. How much will it cost to fill the tank completely?":
        "Step 1: Find how many gallons are needed.\n  16 − 3 = 13 gallons\n\nStep 2: Multiply by the cost per gallon.\n  13 × $3 = $39\n\nIt will cost $39 to fill the tank.",

    "An airplane has rows of 2, 3, and 2 seats (7 seats per row). There are 51 rows and 13 seats are empty. How many passengers are on board?":
        "Step 1: Find the total number of seats.\n  51 rows × 7 seats per row = 357 seats\n\nStep 2: Subtract the empty seats.\n  357 − 13 = 344\n\nThere are 344 passengers on board.",

    "The Smiths flew for 14 hours. The airplane travels approximately 512 miles per hour. About how many miles did they travel in all?":
        "Step 1: Multiply speed by time.\n  512 miles/hour × 14 hours\n\nStep 2: Break it up to make multiplication easier.\n  512 × 10 = 5,120\n  512 × 4  = 2,048\n  5,120 + 2,048 = 7,168\n\nThey traveled approximately 7,168 miles.",

    # ── Math Skills: Word Problems ────────────────────────────────────────
    "Jean earned $157 in May, $210 in June, $377 in July, and $145 in August. A computer costs $695 and a printer costs $95. How much money will Jean have left after buying both?":
        "Step 1: Add Jean's earnings.\n  $157 + $210 + $377 + $145 = $889\n\nStep 2: Add the cost of computer and printer.\n  $695 + $95 = $790\n\nStep 3: Subtract the cost from the earnings.\n  $889 − $790 = $99\n\nJean will have $99 left.",

    "Maria traveled 536 miles on day 1, 259 miles on day 2, and 632 miles on day 3 in a video game. What is the total number of miles Maria traveled in the game?":
        "Step 1: Add all three distances.\n  536\n+ 259\n+ 632\n------\n1,427\n\nMaria traveled 1,427 miles in total.",

    "Timmy logged 1,525 minutes online in January. In February he logged 5,182 minutes doing research. How many more minutes did Timmy log in February than in January?":
        "Step 1: Subtract January's minutes from February's.\n  5,182\n− 1,525\n-------\n  3,657\n\nTimmy logged 3,657 more minutes in February.",

    "A city's population increased by 5,765 people in the first 4 years, 2,789 people in the next 2 years, and 8,723 people in the last 4 years. What is the total population increase over 10 years?":
        "Step 1: Add all three population increases.\n  5,765\n+ 2,789\n+ 8,723\n--------\n 17,277\n\nThe total population increase over 10 years was 17,277 people.",

    # ── Word Problems in Winter ───────────────────────────────────────────
    "On Saturday, 4 groups of 5 people went to a ski resort restaurant. Everyone ordered hot chocolate. Rebecca, Malaki, and Jeffrey each ordered an extra cup. How many cups of hot chocolate were drunk in total?":
        "Step 1: Find the total number of people.\n  4 groups × 5 people = 20 people → 20 cups\n\nStep 2: Add the extra cups.\n  20 + 3 (Rebecca, Malaki, Jeffrey) = 23\n\n23 cups of hot chocolate were drunk in total.",

    "On a snow day, 8 kids built snowmen using 2 buttons each for eyes. Then 7 more kids joined and also used 2 buttons each for their snowmen. How many buttons were used in all?":
        "Step 1: Find the total number of kids.\n  8 + 7 = 15 kids\n\nStep 2: Multiply by 2 buttons per kid.\n  15 × 2 = 30\n\n30 buttons were used in all.",

    "Mr. Ackerman's 9 boys went outside wearing 2 gloves each. Isaiah and Michael each lost 1 glove while outside. How many gloves did the boys bring back into the classroom?":
        "Step 1: Find the total gloves they started with.\n  9 boys × 2 gloves = 18 gloves\n\nStep 2: Subtract the lost gloves.\n  Isaiah lost 1, Michael lost 1 → 2 gloves lost\n  18 − 2 = 16\n\nThe boys brought back 16 gloves.",

    "The Jerico family (2 parents and 4 children) went ice skating. Each person had ice skates. They also brought 1 extra pair in case anyone else wanted to join. How many ice skates did the family bring?":
        "Step 1: Find the total number of family members.\n  2 parents + 4 children = 6 people\n\nStep 2: Each person needs 2 skates (one per foot).\n  6 × 2 = 12 skates\n\nStep 3: Add the extra pair.\n  12 + 2 = 14\n\nThe family brought 14 ice skates.",

    "It snowed 3 inches each day for a week (7 days). By the following Monday, 6 inches had melted. How many inches of snow were still on the ground?":
        "Step 1: Find total snow that fell.\n  3 inches/day × 7 days = 21 inches\n\nStep 2: Subtract what melted.\n  21 − 6 = 15\n\n15 inches of snow were still on the ground.",

    "Sheena baked 112 cookies. She kept 16 cookies at home for her family and shared the rest evenly with her 8 friends. How many cookies did each friend get?":
        "Step 1: Find how many cookies were shared.\n  112 − 16 = 96 cookies\n\nStep 2: Divide equally among 8 friends.\n  96 ÷ 8 = 12\n\nEach friend got 12 cookies.",

    # ── Number Riddles / What's My Number? ──────────────────────────────
    "What's My Number? Add 9 to me. Then multiply by 3. If you subtract 16 and then add 7, you get 27. What number am I?":
        "Work BACKWARD from 27 — undo each step in reverse order.\n\nThe steps were: +9, ×3, −16, +7 → result is 27\n\nStep 1 (undo +7): 27 − 7 = 20\nStep 2 (undo −16): 20 + 16 = 36\nStep 3 (undo ×3): 36 ÷ 3 = 12\nStep 4 (undo +9): 12 − 9 = 3\n\nThe mystery number is 3.\nCheck: 3 + 9 = 12 → 12 × 3 = 36 → 36 − 16 = 20 → 20 + 7 = 27 ✓",

    "What's My Number? Add 5 to me. Then divide by 7. If you add 12 and then subtract 7, you get 10. What number am I?":
        "Work BACKWARD from 10 — undo each step in reverse order.\n\nThe steps were: +5, ÷7, +12, −7 → result is 10\n\nStep 1 (undo −7): 10 + 7 = 17\nStep 2 (undo +12): 17 − 12 = 5\nStep 3 (undo ÷7): 5 × 7 = 35\nStep 4 (undo +5): 35 − 5 = 30\n\nThe mystery number is 30.\nCheck: 30 + 5 = 35 → 35 ÷ 7 = 5 → 5 + 12 = 17 → 17 − 7 = 10 ✓",

    "What's My Number? Multiply me by 4. Then subtract 13. If you divide by 3 and add 17, you get 22. What number am I?":
        "Work BACKWARD from 22 — undo each step in reverse order.\n\nThe steps were: ×4, −13, ÷3, +17 → result is 22\n\nStep 1 (undo +17): 22 − 17 = 5\nStep 2 (undo ÷3): 5 × 3 = 15\nStep 3 (undo −13): 15 + 13 = 28\nStep 4 (undo ×4): 28 ÷ 4 = 7\n\nThe mystery number is 7.\nCheck: 7 × 4 = 28 → 28 − 13 = 15 → 15 ÷ 3 = 5 → 5 + 17 = 22 ✓",

    "What's My Number? Subtract 6 from me. Then multiply by 2. If you subtract 40 and divide by 4, you get 8. What number am I?":
        "Work BACKWARD from 8 — undo each step in reverse order.\n\nThe steps were: −6, ×2, −40, ÷4 → result is 8\n\nStep 1 (undo ÷4): 8 × 4 = 32\nStep 2 (undo −40): 32 + 40 = 72\nStep 3 (undo ×2): 72 ÷ 2 = 36\nStep 4 (undo −6): 36 + 6 = 42\n\nThe mystery number is 42.\nCheck: 42 − 6 = 36 → 36 × 2 = 72 → 72 − 40 = 32 → 32 ÷ 4 = 8 ✓",

    "Mathematical Mindbender: What is the LARGER of two numbers that have a product of 48 and, when the larger is divided by the smaller, give a quotient of 3?":
        "Let the larger number = x and the smaller number = y.\n\nWe know:\n  x × y = 48   (product is 48)\n  x ÷ y = 3    (larger ÷ smaller = 3)\n\nFrom the second equation: x = 3y\n\nSubstitute into the first:\n  3y × y = 48\n  3y² = 48\n  y² = 16\n  y = 4\n\nSo x = 3 × 4 = 12\n\nCheck: 12 × 4 = 48 ✓ and 12 ÷ 4 = 3 ✓\n\nThe larger number is 12.",

    # ── What's My Sign? ───────────────────────────────────────────────────
    "What's My Sign? Fill in the operations to make it true:\n15 ○ 11 ○ 3 = 7":
        "Try each option by substituting the operations:\n\nOption A (subtract, then add):\n  15 − 11 = 4\n  4 + 3 = 7 ✓\n\nAnswer: subtract, then add (A).",

    "What's My Sign? Fill in the operations to make it true:\n22 ○ 22 ○ 4 = 4":
        "Try each option:\n\nOption C (subtract, then add):\n  22 − 22 = 0\n  0 + 4 = 4 ✓\n\nAnswer: subtract, then add (C).",

    "What's My Sign? Fill in the operations to make it true:\n16 ○ 40 ○ 16 = 40":
        "Try each option:\n\nOption C (add, then subtract):\n  16 + 40 = 56\n  56 − 16 = 40 ✓\n\nAnswer: add, then subtract (C).",

    "What's My Sign? Fill in the operations to make it true:\n32 ○ 4 ○ 3 = 24":
        "Try each option:\n\nOption D (divide, then multiply):\n  32 ÷ 4 = 8\n  8 × 3 = 24 ✓\n\nAnswer: divide, then multiply (D).",

    "What's My Sign? Fill in the operations to make it true:\n10 ○ 5 ○ 2 = 100":
        "Try each option:\n\nOption B (multiply, then multiply):\n  10 × 5 = 50\n  50 × 2 = 100 ✓\n\nAnswer: multiply, then multiply (B).",

    "What's My Sign? Fill in the operations to make it true:\n64 ○ 8 ○ 5 = 40":
        "Try each option:\n\nOption C (divide, then multiply):\n  64 ÷ 8 = 8\n  8 × 5 = 40 ✓\n\nAnswer: divide, then multiply (C).",

    "What's My Sign? Fill in the operations to make it true:\n6 ○ 7 ○ 20 = 22":
        "Try each option:\n\nOption C (multiply, then subtract):\n  6 × 7 = 42\n  42 − 20 = 22 ✓\n\nAnswer: multiply, then subtract (C).",

    "What's My Sign? Fill in the operations to make it true:\n12 ○ 4 ○ 8 = 56":
        "Try each option:\n\nOption B (multiply, then add):\n  12 × 4 = 48\n  48 + 8 = 56 ✓\n\nAnswer: multiply, then add (B).",

    "What's My Sign? Fill in the operations to make it true:\n43 ○ 21 ○ 17 = 47":
        "Try each option:\n\nOption B (add, then subtract):\n  43 + 21 = 64\n  64 − 17 = 47 ✓\n\nAnswer: add, then subtract (B).",

    "What's My Sign? Fill in the operations to make it true:\n9 ○ 1 ○ 8 = 72":
        "Try each option:\n\nOption C (divide, then multiply):\n  9 ÷ 1 = 9\n  9 × 8 = 72 ✓\n\nAnswer: divide, then multiply (C).",

    "What's My Sign? Fill in the operations to make it true:\n78 ○ 6 ○ 3 = 39":
        "Try each option:\n\nOption B (divide, then multiply):\n  78 ÷ 6 = 13\n  13 × 3 = 39 ✓\n\nAnswer: divide, then multiply (B).",

    "What's My Sign? Fill in the operations to make it true:\n10 ○ 3 ○ 3 = 10":
        "Try each option:\n\nOption B (add, then subtract):\n  10 + 3 = 13\n  13 − 3 = 10 ✓\n\nAnswer: add, then subtract (B).",

    "What's My Sign? Fill in the operations to make it true:\n52 ○ 2 ○ 31 = 73":
        "Try each option:\n\nOption C (multiply, then subtract):\n  52 × 2 = 104\n  104 − 31 = 73 ✓\n\nAnswer: multiply, then subtract (C).",

    "What's My Sign? Fill in the operations to make it true:\n2 ○ 7 ○ 3 = 42":
        "Try each option:\n\nOption B (multiply, then multiply):\n  2 × 7 = 14\n  14 × 3 = 42 ✓\n\nAnswer: multiply, then multiply (B).",

    # ── Single-choice Word Problems ──────────────────────────────────────
    "A school store sells pencils for $0.25 each. Elena buys 4 pencils and an eraser for $0.75. How much does she pay in all?":
        "Step 1: Find the cost of the pencils.\n  4 pencils × $0.25 = $1.00\n\nStep 2: Add the cost of the eraser.\n  $1.00 + $0.75 = $1.75\n\nElena pays $1.75 in all. Answer: B",

    "A factory produces 512 widgets per hour. How many widgets does it produce in 8 hours?":
        "Step 1: Multiply the rate by the time.\n  512 × 8\n\nStep 2: Break it up.\n  500 × 8 = 4,000\n   12 × 8 =    96\n  4,000 + 96 = 4,096\n\nThe factory produces 4,096 widgets. Answer: B",

    "Marcus has 1,248 baseball cards. He organizes them equally into 6 binders. How many cards are in each binder?":
        "Step 1: Divide total cards by number of binders.\n  1,248 ÷ 6\n\nStep 2: Work through the division.\n  6 × 200 = 1,200\n  1,248 − 1,200 = 48\n  6 × 8 = 48\n  So 200 + 8 = 208\n\nEach binder has 208 cards. Answer: C",

    "A bookstore sells 3 books for $7 each and 5 magazines for $3 each. What is the total cost?":
        "Step 1: Find the cost of the books.\n  3 × $7 = $21\n\nStep 2: Find the cost of the magazines.\n  5 × $3 = $15\n\nStep 3: Add them together.\n  $21 + $15 = $36\n\nThe total cost is $36. Answer: B",

    "A movie theater has 24 rows with 18 seats each. On Friday night, 315 seats were filled. How many seats were empty?":
        "Step 1: Find the total number of seats.\n  24 × 18\n  24 × 10 = 240\n  24 × 8  = 192\n  240 + 192 = 432 seats\n\nStep 2: Subtract the filled seats.\n  432 − 315 = 117\n\n117 seats were empty. Answer: C",

    "Layla earns $9 per hour babysitting. She babysits for 6 hours on Saturday and 4 hours on Sunday. How much does she earn over the weekend?":
        "Step 1: Find the total hours worked.\n  6 + 4 = 10 hours\n\nStep 2: Multiply by her hourly rate.\n  10 × $9 = $90\n\nLayla earns $90 over the weekend. Answer: C",

    "A farmer has 4 fields. Each field has 125 apple trees. He expects each tree to produce 48 apples. How many apples will the 4 fields produce in total?":
        "Step 1: Find the total number of trees.\n  4 fields × 125 trees = 500 trees\n\nStep 2: Multiply by apples per tree.\n  500 × 48\n  500 × 40 = 20,000\n  500 × 8  =  4,000\n  20,000 + 4,000 = 24,000\n\nThe 4 fields will produce 24,000 apples. Answer: C",
}

def fetch_grade4_questions():
    url = f"{BASE}/questions?grade=eq.4&subject=eq.Math&select=id,text&limit=200"
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def patch_solution(qid, solution):
    url = f"{BASE}/questions?id=eq.{qid}"
    data = json.dumps({"solution": solution}).encode()
    req = urllib.request.Request(url, data=data, method="PATCH", headers=HEADERS)
    with urllib.request.urlopen(req) as r:
        return r.status

print("Fetching grade 4 Math questions...")
questions = fetch_grade4_questions()
print(f"Found {len(questions)} questions")

matched = 0
skipped = 0
for q in questions:
    text = q["text"]
    solution = SOLUTIONS.get(text)
    if solution:
        status = patch_solution(q["id"], solution)
        print(f"  ✓ [{status}] {text[:60]}...")
        matched += 1
        time.sleep(0.1)
    else:
        print(f"  ⚠ No solution for: {text[:60]}...")
        skipped += 1

print(f"\nDone: {matched} updated, {skipped} skipped")
