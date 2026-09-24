"""
173 grade 4 geometry and operations/algebraic thinking questions (G, OA).

ALREADY RUN -- these questions are live in Supabase. This file is kept as the
source of record for data that is already in the database.

There is no dry-run flag: running this uploads on sight, and running it again
would duplicate every question above for Jaden. Check the `questions` table
before re-running.
"""
import json
import urllib.request
import time

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


# =============================================================================
# MULT & DIVISION REASONING — 86 questions (domain: OA)
# 70 single-choice + 16 numeric
# =============================================================================

oa_single = [
    # --- Multiplication as repeated addition ---
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which addition equation shows the same amount as 3 x 4?",
        "options": ["A 4 + 4 + 4", "B 3 + 3 + 3", "C 4 + 3", "D 3 + 4 + 4"],
        "correct": ["A"], "hint": "3 x 4 means 3 groups of 4, so add 4 three times.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which multiplication equation matches: 5 + 5 + 5 + 5?",
        "options": ["A 4 x 5", "B 5 x 5", "C 5 + 4", "D 4 + 5"],
        "correct": ["A"], "hint": "Count how many times 5 is added -- that is the other factor.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Sara has 6 bags. Each bag has 3 apples. How can she find the total?",
        "options": ["A Multiply 6 x 3", "B Add 6 + 3", "C Divide 6 / 3", "D Subtract 6 - 3"],
        "correct": ["A"], "hint": "Equal groups problems use multiplication.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which shows 2 x 7 as repeated addition?",
        "options": ["A 7 + 7", "B 2 + 7", "C 2 + 2 + 2 + 2 + 2 + 2 + 2", "D 7 x 7"],
        "correct": ["A"], "hint": "2 x 7 means 2 groups of 7.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Tom skip counts by 4: 4, 8, 12. Which multiplication fact does this show?",
        "options": ["A 3 x 4 = 12", "B 4 x 4 = 16", "C 2 x 4 = 8", "D 3 + 4 = 7"],
        "correct": ["A"], "hint": "3 skips of 4 equals 3 x 4.", "active": True
    },
    # --- Arrays ---
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "An array has 4 rows and 6 columns. Which equation gives the total?",
        "options": ["A 4 x 6 = 24", "B 4 + 6 = 10", "C 6 - 4 = 2", "D 6 / 4 = 1 R2"],
        "correct": ["A"], "hint": "Rows times columns equals total dots in an array.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which array represents 3 x 5?",
        "options": ["A 3 rows with 5 dots each", "B 5 rows with 3 dots each", "C Both A and B", "D Neither"],
        "correct": ["C"], "hint": "Commutative property: 3 x 5 = 5 x 3, so both arrays work.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "A garden has 7 rows of flowers. Each row has 4 flowers. How many flowers are there?",
        "options": ["A 28", "B 11", "C 21", "D 32"],
        "correct": ["A"], "hint": "7 x 4 = 28.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "An array has 5 rows of 8 stickers. Which equation matches?",
        "options": ["A 5 x 8 = 40", "B 5 + 8 = 13", "C 8 x 0 = 0", "D 5 x 5 = 25"],
        "correct": ["A"], "hint": "5 rows times 8 per row = 5 x 8.", "active": True
    },
    # --- Equal groups ---
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "There are 4 boxes. Each box holds 9 crayons. How many crayons in all?",
        "options": ["A 36", "B 13", "C 27", "D 45"],
        "correct": ["A"], "hint": "4 x 9 = 36.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "6 children each have 5 stickers. Which equation shows the total?",
        "options": ["A 6 x 5 = 30", "B 6 + 5 = 11", "C 5 x 1 = 5", "D 6 / 5 = 1 R1"],
        "correct": ["A"], "hint": "Equal groups: multiply number of groups by group size.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which situation shows equal groups?",
        "options": ["A 3 plates with 4 cookies each", "B A pile of 12 mixed coins", "C 7 different-sized boxes", "D A row of 10 books of different widths"],
        "correct": ["A"], "hint": "Equal groups means the same number in each group.", "active": True
    },
    # --- Commutative property ---
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "If 6 x 7 = 42, what is 7 x 6?",
        "options": ["A 42", "B 48", "C 35", "D 13"],
        "correct": ["A"], "hint": "The commutative property says you can multiply in any order.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which property allows you to say 8 x 3 = 3 x 8?",
        "options": ["A Commutative", "B Associative", "C Distributive", "D Identity"],
        "correct": ["A"], "hint": "The commutative property lets you swap the order of factors.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Jake says 9 x 4 = 4 x 9. Is he correct?",
        "options": ["A Yes, because of the commutative property", "B No, they are different", "C Only if both equal 36", "D Yes, because of the identity property"],
        "correct": ["A"], "hint": "Multiplying in any order gives the same product.", "active": True
    },
    # --- Associative property ---
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which shows the associative property of multiplication?",
        "options": ["A (2 x 3) x 4 = 2 x (3 x 4)", "B 2 x 3 = 3 x 2", "C 5 x 1 = 5", "D 5 x 0 = 0"],
        "correct": ["A"], "hint": "The associative property lets you regroup factors.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "2 x (5 x 3) = (2 x 5) x 3. What property is this?",
        "options": ["A Associative", "B Commutative", "C Distributive", "D Zero"],
        "correct": ["A"], "hint": "Regrouping factors uses the associative property.", "active": True
    },
    # --- Distributive property ---
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which equation shows the distributive property for 6 x 7?",
        "options": ["A 6 x (5 + 2) = (6 x 5) + (6 x 2)", "B 6 + 7 = 7 + 6", "C (6 x 7) x 1 = 6 x 7", "D 6 x 0 = 0"],
        "correct": ["A"], "hint": "Break a factor into parts, then multiply each part.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "To find 8 x 6, Maya breaks it into (8 x 5) + (8 x 1). What property is she using?",
        "options": ["A Distributive", "B Commutative", "C Associative", "D Identity"],
        "correct": ["A"], "hint": "Distributing multiplication over addition is the distributive property.", "active": True
    },
    # --- Identity and zero properties ---
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "What is 9 x 1?",
        "options": ["A 9", "B 1", "C 0", "D 10"],
        "correct": ["A"], "hint": "Any number times 1 equals itself (identity property).", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "What is 7 x 0?",
        "options": ["A 0", "B 7", "C 1", "D 70"],
        "correct": ["A"], "hint": "Any number times 0 equals 0.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which equation uses the identity property of multiplication?",
        "options": ["A 5 x 1 = 5", "B 5 x 0 = 0", "C 5 + 0 = 5", "D 5 x 5 = 25"],
        "correct": ["A"], "hint": "Multiplying by 1 keeps the number the same.", "active": True
    },
    # --- Unknown factor ---
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "3 x ? = 18. What is the missing number?",
        "options": ["A 6", "B 5", "C 7", "D 4"],
        "correct": ["A"], "hint": "Think: what times 3 equals 18?", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "? x 8 = 40. What is the missing factor?",
        "options": ["A 5", "B 6", "C 4", "D 7"],
        "correct": ["A"], "hint": "5 x 8 = 40, so the missing factor is 5.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "7 x ? = 63. What is the missing number?",
        "options": ["A 9", "B 8", "C 7", "D 6"],
        "correct": ["A"], "hint": "7 x 9 = 63.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "? x 6 = 54. What is the missing factor?",
        "options": ["A 9", "B 7", "C 8", "D 6"],
        "correct": ["A"], "hint": "9 x 6 = 54.", "active": True
    },
    # --- Division as sharing equally ---
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "20 students are split into 4 equal teams. How many students are on each team?",
        "options": ["A 5", "B 4", "C 6", "D 10"],
        "correct": ["A"], "hint": "20 / 4 = 5.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "18 cookies are shared equally among 3 friends. How many cookies does each friend get?",
        "options": ["A 6", "B 5", "C 7", "D 9"],
        "correct": ["A"], "hint": "18 / 3 = 6.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which equation means '24 items put into groups of 6'?",
        "options": ["A 24 / 6 = 4", "B 24 x 6 = 144", "C 6 + 24 = 30", "D 24 - 6 = 18"],
        "correct": ["A"], "hint": "Dividing into equal groups uses division.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "35 / 7 = ?",
        "options": ["A 5", "B 6", "C 4", "D 7"],
        "correct": ["A"], "hint": "7 x 5 = 35, so 35 / 7 = 5.", "active": True
    },
    # --- Relationship between multiplication and division ---
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which division fact belongs to the same fact family as 4 x 7 = 28?",
        "options": ["A 28 / 7 = 4", "B 28 / 4 = 8", "C 7 / 4 = 1 R3", "D 4 / 7 = 0 R4"],
        "correct": ["A"], "hint": "Fact families use the same three numbers: 4, 7, 28.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "If 6 x 8 = 48, which division fact is in the same fact family?",
        "options": ["A 48 / 8 = 6", "B 48 / 6 = 9", "C 8 / 6 = 1 R2", "D 6 / 8 = 0 R6"],
        "correct": ["A"], "hint": "Use the same three numbers: 6, 8, 48.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which multiplication fact can help you solve 56 / 8 = ?",
        "options": ["A 8 x 7 = 56", "B 8 x 8 = 64", "C 7 x 6 = 42", "D 5 x 8 = 40"],
        "correct": ["A"], "hint": "Think: 8 times what equals 56?", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "What are all four facts in the fact family for 3, 9, and 27?",
        "options": [
            "A 3x9=27, 9x3=27, 27/3=9, 27/9=3",
            "B 3x9=27, 27+3=30, 27-9=18, 9/3=3",
            "C 3+9=12, 9-3=6, 3x9=27, 27/3=9",
            "D 3x9=27, 9x9=81, 27/3=9, 27/9=3"
        ],
        "correct": ["A"], "hint": "A fact family has 2 multiplication and 2 division facts.", "active": True
    },
    # --- Interpreting equations ---
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which word problem matches the equation 5 x 6 = 30?",
        "options": [
            "A 5 baskets each hold 6 apples. How many apples?",
            "B 5 apples are added to 6. How many?",
            "C 30 apples shared by 5 friends. How many each?",
            "D 6 apples taken from 30. How many left?"
        ],
        "correct": ["A"], "hint": "5 groups of 6 matches 5 x 6.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which equation shows dividing 42 into 7 equal groups?",
        "options": ["A 42 / 7 = 6", "B 7 x 6 = 42", "C 42 - 7 = 35", "D 42 + 7 = 49"],
        "correct": ["A"], "hint": "Dividing into equal groups is written with division.", "active": True
    },
    # --- Multiples / skip counting ---
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which number is a multiple of 6?",
        "options": ["A 54", "B 50", "C 52", "D 55"],
        "correct": ["A"], "hint": "6 x 9 = 54, so 54 is a multiple of 6.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "What is the 8th multiple of 4?",
        "options": ["A 32", "B 28", "C 36", "D 24"],
        "correct": ["A"], "hint": "8 x 4 = 32.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which list shows multiples of 3?",
        "options": ["A 3, 6, 9, 12, 15", "B 3, 5, 7, 9, 11", "C 3, 4, 7, 10, 13", "D 3, 6, 8, 12, 15"],
        "correct": ["A"], "hint": "Add 3 each time to get multiples of 3.", "active": True
    },
    # --- Division / grouping ---
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "30 pencils are put in groups of 5. How many groups are there?",
        "options": ["A 6", "B 5", "C 7", "D 4"],
        "correct": ["A"], "hint": "30 / 5 = 6.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "A baker puts 8 muffins in each box. He has 64 muffins. How many boxes does he need?",
        "options": ["A 8", "B 6", "C 9", "D 10"],
        "correct": ["A"], "hint": "64 / 8 = 8.", "active": True
    },
    # --- Word problems ---
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Each carton holds 6 eggs. There are 7 cartons. How many eggs are there?",
        "options": ["A 42", "B 36", "C 48", "D 13"],
        "correct": ["A"], "hint": "7 x 6 = 42.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Lena reads 8 pages a day. How many pages does she read in 9 days?",
        "options": ["A 72", "B 64", "C 81", "D 17"],
        "correct": ["A"], "hint": "9 x 8 = 72.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "36 students go on a trip. They ride in vans that each hold 9 students. How many vans are needed?",
        "options": ["A 4", "B 3", "C 5", "D 6"],
        "correct": ["A"], "hint": "36 / 9 = 4.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "5 friends equally share 45 grapes. How many grapes does each friend get?",
        "options": ["A 9", "B 8", "C 10", "D 7"],
        "correct": ["A"], "hint": "45 / 5 = 9.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "A store has 7 shelves. Each shelf has 8 books. How many books in all?",
        "options": ["A 56", "B 49", "C 63", "D 15"],
        "correct": ["A"], "hint": "7 x 8 = 56.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Mom buys 4 packs of juice boxes. Each pack has 8 boxes. How many juice boxes are there?",
        "options": ["A 32", "B 28", "C 36", "D 12"],
        "correct": ["A"], "hint": "4 x 8 = 32.", "active": True
    },
    # --- True/False / identify correct equation ---
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which equation is TRUE?",
        "options": ["A 9 x 6 = 54", "B 9 x 6 = 45", "C 9 x 6 = 63", "D 9 x 6 = 36"],
        "correct": ["A"], "hint": "9 x 6 = 54 is the correct fact.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which equation is FALSE?",
        "options": ["A 8 x 7 = 54", "B 8 x 7 = 56", "C 7 x 8 = 56", "D 56 / 8 = 7"],
        "correct": ["A"], "hint": "8 x 7 = 56, not 54.", "active": True
    },
    # --- Factors ---
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which pair of numbers are both factors of 24?",
        "options": ["A 4 and 6", "B 4 and 7", "C 5 and 6", "D 3 and 7"],
        "correct": ["A"], "hint": "4 x 6 = 24, so both 4 and 6 are factors of 24.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which number is NOT a factor of 36?",
        "options": ["A 8", "B 9", "C 6", "D 4"],
        "correct": ["A"], "hint": "36 / 8 is not a whole number, so 8 is not a factor.", "active": True
    },
    # --- Comparing / reasoning ---
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which is greater: 6 x 8 or 7 x 7?",
        "options": ["A 6 x 8 = 48", "B 7 x 7 = 49", "C They are equal", "D Both equal 42"],
        "correct": ["B"], "hint": "6 x 8 = 48 and 7 x 7 = 49, so 7 x 7 is greater.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Ben says multiplying always gives a bigger number. Which example proves him wrong?",
        "options": ["A 5 x 0 = 0", "B 5 x 2 = 10", "C 5 x 3 = 15", "D 5 x 4 = 20"],
        "correct": ["A"], "hint": "Multiplying by 0 gives 0, which is not bigger than 5.", "active": True
    },
    # --- More word problems / mixed ---
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "There are 9 rows of chairs with 7 chairs in each row. How many chairs are there?",
        "options": ["A 63", "B 54", "C 72", "D 16"],
        "correct": ["A"], "hint": "9 x 7 = 63.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "A carton has 3 rows of 8 oranges. Which equation finds the total?",
        "options": ["A 3 x 8 = 24", "B 3 + 8 = 11", "C 8 - 3 = 5", "D 8 / 3 = 2 R2"],
        "correct": ["A"], "hint": "Rows times per row = total, so 3 x 8.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "You know 5 x 9 = 45. How can you use this to find 5 x 10?",
        "options": ["A Add one more group of 5 to get 50", "B Add one more group of 9 to get 54", "C Multiply 45 x 2", "D Subtract 5 from 45"],
        "correct": ["A"], "hint": "5 x 10 = 5 x 9 + 5 = 45 + 5 = 50.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which operation would you use to find how many items are in 8 equal groups of 6?",
        "options": ["A Multiplication", "B Division", "C Subtraction", "D Addition only"],
        "correct": ["A"], "hint": "Equal groups means multiply.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "A number is multiplied by 6 and the product is 48. What is the number?",
        "options": ["A 8", "B 7", "C 9", "D 6"],
        "correct": ["A"], "hint": "6 x 8 = 48, so the unknown is 8.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which number sentence shows sharing 27 marbles equally among 9 children?",
        "options": ["A 27 / 9 = 3", "B 9 x 3 = 27", "C 27 + 9 = 36", "D 27 - 9 = 18"],
        "correct": ["A"], "hint": "Sharing equally means dividing.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "To use the distributive property, how can you break apart 7 x 8?",
        "options": ["A (7 x 5) + (7 x 3)", "B (7 + 5) x (7 + 3)", "C 7 x (8 + 0)", "D (7 + 8) x 1"],
        "correct": ["A"], "hint": "Break 8 into 5 + 3, then distribute.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which equation belongs in the same fact family as 6 x 9 = 54?",
        "options": ["A 54 / 9 = 6", "B 54 / 6 = 10", "C 6 + 9 = 15", "D 9 - 6 = 3"],
        "correct": ["A"], "hint": "Fact families include related multiplication and division facts.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Amy has 32 beads. She wants to put 4 beads on each bracelet. How many bracelets can she make?",
        "options": ["A 8", "B 7", "C 9", "D 6"],
        "correct": ["A"], "hint": "32 / 4 = 8.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which property says that (3 x 4) x 2 = 3 x (4 x 2)?",
        "options": ["A Associative", "B Commutative", "C Distributive", "D Identity"],
        "correct": ["A"], "hint": "Regrouping without changing order = associative property.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "4 x ? = 36. What is the missing factor?",
        "options": ["A 9", "B 8", "C 7", "D 6"],
        "correct": ["A"], "hint": "4 x 9 = 36.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which number completes the equation: 63 / ? = 9?",
        "options": ["A 7", "B 6", "C 8", "D 9"],
        "correct": ["A"], "hint": "63 / 7 = 9.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which of these is NOT a way to find 6 x 8?",
        "options": ["A 6 + 8 + 6 + 8", "B 8 + 8 + 8 + 8 + 8 + 8", "C (6 x 4) + (6 x 4)", "D 6 x 4 x 2"],
        "correct": ["A"], "hint": "6 + 8 + 6 + 8 = 28, not 48. The others all equal 48.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Theo has 5 sheets of stickers. Each sheet has 10 stickers. How many stickers does he have?",
        "options": ["A 50", "B 45", "C 55", "D 15"],
        "correct": ["A"], "hint": "5 x 10 = 50.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which multiplication equation has a product of 72?",
        "options": ["A 8 x 9", "B 7 x 9", "C 8 x 8", "D 6 x 9"],
        "correct": ["A"], "hint": "8 x 9 = 72.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "A school orders 6 boxes of crayons. Each box has 8 crayons. Which equation finds the total?",
        "options": ["A 6 x 8 = 48", "B 6 + 8 = 14", "C 8 / 6 = 1 R2", "D 8 - 6 = 2"],
        "correct": ["A"], "hint": "6 groups times 8 each = 6 x 8 = 48.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which fact shows the commutative property of 5 x 7?",
        "options": ["A 7 x 5 = 35", "B 5 + 7 = 12", "C (5 x 3) + (5 x 4) = 35", "D 5 x 7 x 1 = 35"],
        "correct": ["A"], "hint": "Swapping factors uses the commutative property.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Ms. Lee puts 6 candies in each of 9 bags. How many candies does she use?",
        "options": ["A 54", "B 48", "C 63", "D 15"],
        "correct": ["A"], "hint": "9 x 6 = 54.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which word means the answer to a multiplication problem?",
        "options": ["A Product", "B Sum", "C Difference", "D Quotient"],
        "correct": ["A"], "hint": "The result of multiplying two numbers is called the product.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "single",
        "text": "Which word means the answer to a division problem?",
        "options": ["A Quotient", "B Product", "C Sum", "D Factor"],
        "correct": ["A"], "hint": "The result of dividing is called the quotient.", "active": True
    },
]

oa_numeric = [
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "numeric", "text": "What is 8 x 7?",
        "options": None, "correct": 56, "hint": "Count 7 eight times or use the fact 8 x 7 = 56.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "numeric", "text": "What is 9 x 9?",
        "options": None, "correct": 81, "hint": "9 x 9 = 81.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "numeric", "text": "What is 72 / 8?",
        "options": None, "correct": 9, "hint": "8 x 9 = 72, so 72 / 8 = 9.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "numeric", "text": "What is 6 x 6?",
        "options": None, "correct": 36, "hint": "6 x 6 = 36.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "numeric", "text": "What is 45 / 9?",
        "options": None, "correct": 5, "hint": "9 x 5 = 45, so 45 / 9 = 5.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "numeric", "text": "What is 7 x 4?",
        "options": None, "correct": 28, "hint": "7 x 4 = 28.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "numeric", "text": "3 x ? = 21. Enter the missing factor.",
        "options": None, "correct": 7, "hint": "3 x 7 = 21.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "numeric", "text": "A bag holds 5 oranges. There are 8 bags. How many oranges are there in all?",
        "options": None, "correct": 40, "hint": "8 x 5 = 40.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "numeric", "text": "48 students are divided into groups of 6. How many groups are there?",
        "options": None, "correct": 8, "hint": "48 / 6 = 8.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "numeric", "text": "What is 10 x 7?",
        "options": None, "correct": 70, "hint": "10 x 7 = 70.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "numeric", "text": "What is 81 / 9?",
        "options": None, "correct": 9, "hint": "9 x 9 = 81, so 81 / 9 = 9.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "numeric", "text": "A classroom has 4 rows of desks with 7 desks in each row. How many desks are there?",
        "options": None, "correct": 28, "hint": "4 x 7 = 28.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "numeric", "text": "What is 3 x 9?",
        "options": None, "correct": 27, "hint": "3 x 9 = 27.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "numeric", "text": "What is 64 / 8?",
        "options": None, "correct": 8, "hint": "8 x 8 = 64, so 64 / 8 = 8.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "numeric", "text": "There are 5 rows and 9 columns in an array. How many objects are in the array?",
        "options": None, "correct": 45, "hint": "5 x 9 = 45.", "active": True
    },
    {
        "subject": "Math", "domain": "OA", "category": "Mult & Division Reasoning",
        "type": "numeric", "text": "What is 6 x 7?",
        "options": None, "correct": 42, "hint": "6 x 7 = 42.", "active": True
    },
]

# =============================================================================
# GEOMETRY -- 80 questions (domain: G)
# 72 single-choice + 8 numeric
# =============================================================================

g_single = [
    # --- 2D shapes: identify and properties ---
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "How many sides does a hexagon have?",
        "options": ["A 6", "B 5", "C 4", "D 8"],
        "correct": ["A"], "hint": "'Hex' means six.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "How many sides does a pentagon have?",
        "options": ["A 5", "B 6", "C 4", "D 3"],
        "correct": ["A"], "hint": "'Penta' means five.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which shape has exactly 4 equal sides and 4 right angles?",
        "options": ["A Square", "B Rectangle", "C Rhombus", "D Trapezoid"],
        "correct": ["A"], "hint": "A square has 4 equal sides AND 4 right angles.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which shape has 3 sides and 3 angles?",
        "options": ["A Triangle", "B Square", "C Pentagon", "D Hexagon"],
        "correct": ["A"], "hint": "'Tri' means three.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "A rectangle has 4 right angles. How many sides does it have?",
        "options": ["A 4", "B 3", "C 5", "D 6"],
        "correct": ["A"], "hint": "A rectangle is a quadrilateral -- it has 4 sides.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which of these is a quadrilateral?",
        "options": ["A Rectangle", "B Triangle", "C Pentagon", "D Hexagon"],
        "correct": ["A"], "hint": "A quadrilateral has 4 sides. Rectangle qualifies.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "What do all quadrilaterals have in common?",
        "options": ["A 4 sides and 4 vertices", "B 4 equal sides", "C 4 right angles", "D 2 pairs of parallel sides"],
        "correct": ["A"], "hint": "Any shape with 4 sides and 4 corners is a quadrilateral.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "A shape has 6 sides of equal length. What is it called?",
        "options": ["A Regular hexagon", "B Regular pentagon", "C Octagon", "D Rhombus"],
        "correct": ["A"], "hint": "Six equal sides make a regular hexagon.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which shape has vertices (corners)?",
        "options": ["A Triangle", "B Circle", "C Sphere", "D Cylinder"],
        "correct": ["A"], "hint": "Circles have no vertices; triangles have 3.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "How many vertices does a pentagon have?",
        "options": ["A 5", "B 6", "C 4", "D 3"],
        "correct": ["A"], "hint": "A pentagon has 5 sides and 5 vertices.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which shape has no sides and no vertices?",
        "options": ["A Circle", "B Triangle", "C Square", "D Pentagon"],
        "correct": ["A"], "hint": "A circle is a round closed curve with no corners.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "A stop sign has 8 sides. What is a stop sign's shape called?",
        "options": ["A Octagon", "B Hexagon", "C Pentagon", "D Decagon"],
        "correct": ["A"], "hint": "'Octa' means eight.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which statement about a square is TRUE?",
        "options": [
            "A All sides are equal and all angles are right angles",
            "B It has 3 sides",
            "C Opposite sides are equal but not all sides are equal",
            "D It has no right angles"
        ],
        "correct": ["A"], "hint": "A square has 4 equal sides and 4 right (90 degree) angles.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "How many right angles does a rectangle have?",
        "options": ["A 4", "B 2", "C 1", "D 0"],
        "correct": ["A"], "hint": "All four corners of a rectangle are right angles.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which best describes a rhombus?",
        "options": ["A 4 equal sides but angles are not necessarily right angles", "B 4 equal sides and 4 right angles", "C 3 equal sides", "D 6 sides"],
        "correct": ["A"], "hint": "A rhombus has all equal sides, but corners do not have to be 90 degrees.", "active": True
    },
    # --- 3D shapes ---
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which 3D shape looks like a can?",
        "options": ["A Cylinder", "B Cone", "C Cube", "D Sphere"],
        "correct": ["A"], "hint": "A cylinder has two circular faces and a curved side -- like a can.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which 3D shape has all flat square faces?",
        "options": ["A Cube", "B Rectangular prism", "C Cylinder", "D Cone"],
        "correct": ["A"], "hint": "A cube has 6 square faces of equal size.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "How many faces does a cube have?",
        "options": ["A 6", "B 4", "C 8", "D 5"],
        "correct": ["A"], "hint": "A cube has 6 square faces.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which 3D shape has 1 circular face and comes to a point?",
        "options": ["A Cone", "B Cylinder", "C Sphere", "D Cube"],
        "correct": ["A"], "hint": "A cone has a round base and a pointed top.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which 3D shape has no flat faces and no edges?",
        "options": ["A Sphere", "B Cylinder", "C Cone", "D Cube"],
        "correct": ["A"], "hint": "A sphere is perfectly round with no flat parts.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "A cereal box is what 3D shape?",
        "options": ["A Rectangular prism", "B Cube", "C Cone", "D Cylinder"],
        "correct": ["A"], "hint": "A rectangular prism has 6 rectangular faces.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "How many vertices does a cube have?",
        "options": ["A 8", "B 6", "C 4", "D 12"],
        "correct": ["A"], "hint": "A cube has 8 corners (vertices).", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which 3D shape has 2 circular faces and 1 curved surface?",
        "options": ["A Cylinder", "B Cone", "C Sphere", "D Rectangular prism"],
        "correct": ["A"], "hint": "A cylinder has top and bottom circles plus a curved side.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "A basketball is an example of which 3D shape?",
        "options": ["A Sphere", "B Cylinder", "C Cone", "D Cube"],
        "correct": ["A"], "hint": "A ball is a perfect sphere.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "How many edges does a cube have?",
        "options": ["A 12", "B 8", "C 6", "D 10"],
        "correct": ["A"], "hint": "A cube has 12 edges where faces meet.", "active": True
    },
    # --- Lines of symmetry ---
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which shape has a line of symmetry?",
        "options": ["A Square", "B Scalene triangle", "C Random squiggle", "D Letter Z"],
        "correct": ["A"], "hint": "A square can be folded in half to match perfectly.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "A line of symmetry divides a shape into:",
        "options": ["A Two matching halves", "B Two unequal parts", "C Three equal parts", "D Four equal parts"],
        "correct": ["A"], "hint": "A line of symmetry creates a mirror image on each side.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "How many lines of symmetry does a square have?",
        "options": ["A 4", "B 2", "C 1", "D 0"],
        "correct": ["A"], "hint": "A square has 4 lines of symmetry: horizontal, vertical, and two diagonal.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which letter has a vertical line of symmetry?",
        "options": ["A A", "B S", "C Z", "D F"],
        "correct": ["A"], "hint": "The letter A is the same on both sides if you draw a line down the middle.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "How many lines of symmetry does a circle have?",
        "options": ["A Infinitely many", "B 1", "C 2", "D 4"],
        "correct": ["A"], "hint": "Any line through the center of a circle is a line of symmetry.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "An equilateral triangle (all sides equal) has how many lines of symmetry?",
        "options": ["A 3", "B 1", "C 2", "D 0"],
        "correct": ["A"], "hint": "An equilateral triangle has 3 equal sides and 3 lines of symmetry.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which shape has NO line of symmetry?",
        "options": ["A Scalene triangle", "B Square", "C Rectangle", "D Regular hexagon"],
        "correct": ["A"], "hint": "A scalene triangle has all different side lengths -- it cannot be folded to match.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "A rectangle has how many lines of symmetry?",
        "options": ["A 2", "B 4", "C 1", "D 3"],
        "correct": ["A"], "hint": "A rectangle has 2 lines of symmetry: horizontal and vertical.", "active": True
    },
    # --- Partitioning shapes into equal parts ---
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "A circle is cut into 2 equal parts. What is each part called?",
        "options": ["A A half", "B A third", "C A fourth", "D A quarter"],
        "correct": ["A"], "hint": "2 equal parts means each part is one half.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "A rectangle is split into 4 equal parts. What is each part called?",
        "options": ["A A fourth (or quarter)", "B A third", "C A half", "D A fifth"],
        "correct": ["A"], "hint": "4 equal parts means each part is one fourth or one quarter.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "A pizza is cut into 3 equal slices. What fraction is one slice?",
        "options": ["A 1/3", "B 1/2", "C 1/4", "D 1/6"],
        "correct": ["A"], "hint": "3 equal parts means each part is 1/3.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which shape is divided into halves?",
        "options": ["A A square cut by one line through the middle into 2 equal parts", "B A triangle cut into 3 parts", "C A circle cut into 4 parts", "D A rectangle cut into 6 parts"],
        "correct": ["A"], "hint": "Halves means 2 equal parts.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "When you cut a shape into fourths, you have how many equal parts?",
        "options": ["A 4", "B 2", "C 3", "D 6"],
        "correct": ["A"], "hint": "Fourths = 4 equal parts.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "If a sandwich is cut into thirds, how many pieces are there?",
        "options": ["A 3", "B 2", "C 4", "D 6"],
        "correct": ["A"], "hint": "Thirds = 3 equal pieces.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Two shapes are each divided into 4 parts. Shape A's parts are equal; Shape B's are not. Which has fourths?",
        "options": ["A Shape A", "B Shape B", "C Both", "D Neither"],
        "correct": ["A"], "hint": "Fourths must be equal parts.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "When a shape is divided into 4 equal parts, each part is called a:",
        "options": ["A Quarter", "B Half", "C Third", "D Whole"],
        "correct": ["A"], "hint": "4 equal parts means each is a quarter or fourth.", "active": True
    },
    # --- Classifying shapes ---
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which shape is NOT a polygon?",
        "options": ["A Circle", "B Triangle", "C Square", "D Pentagon"],
        "correct": ["A"], "hint": "Polygons have straight sides. A circle has a curved side.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which is a property of ALL rectangles?",
        "options": ["A 4 right angles", "B 4 equal sides", "C Exactly 1 pair of parallel sides", "D 3 sides"],
        "correct": ["A"], "hint": "All rectangles have 4 right angles, but sides do not have to be equal.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Is a square also a rectangle?",
        "options": ["A Yes, because it has 4 right angles", "B No, because its sides are equal", "C Yes, but only if it is large enough", "D No, because it has fewer sides"],
        "correct": ["A"], "hint": "A square meets all requirements of a rectangle -- 4 sides, 4 right angles.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which shape has exactly one pair of parallel sides?",
        "options": ["A Trapezoid", "B Rectangle", "C Square", "D Rhombus"],
        "correct": ["A"], "hint": "A trapezoid has one pair of parallel sides.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "A polygon with 4 sides is called a:",
        "options": ["A Quadrilateral", "B Triangle", "C Pentagon", "D Hexagon"],
        "correct": ["A"], "hint": "'Quad' means four.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which of these shapes has the most sides?",
        "options": ["A Hexagon", "B Triangle", "C Square", "D Pentagon"],
        "correct": ["A"], "hint": "Hexagon: 6, Pentagon: 5, Square: 4, Triangle: 3.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "How many angles does a hexagon have?",
        "options": ["A 6", "B 5", "C 4", "D 8"],
        "correct": ["A"], "hint": "A hexagon has 6 sides and 6 angles.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which shape has 5 sides and 5 angles?",
        "options": ["A Pentagon", "B Hexagon", "C Quadrilateral", "D Triangle"],
        "correct": ["A"], "hint": "'Penta' = five.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which 3D shape has a rectangular base and 4 triangular faces?",
        "options": ["A Rectangular pyramid", "B Rectangular prism", "C Triangular prism", "D Cube"],
        "correct": ["A"], "hint": "A pyramid has a base and triangular faces that meet at a point.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which 3D shape can roll?",
        "options": ["A Sphere", "B Cube", "C Rectangular prism", "D Pyramid"],
        "correct": ["A"], "hint": "A sphere is round on all sides, so it can roll in any direction.", "active": True
    },
    # --- Angles / right angles ---
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "A right angle measures exactly:",
        "options": ["A 90 degrees", "B 45 degrees", "C 180 degrees", "D 60 degrees"],
        "correct": ["A"], "hint": "A right angle looks like the corner of a square -- 90 degrees.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which shape has all right angles?",
        "options": ["A Rectangle", "B Rhombus", "C Equilateral triangle", "D Regular pentagon"],
        "correct": ["A"], "hint": "A rectangle has 4 right (90 degree) angles.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "An angle smaller than a right angle is called:",
        "options": ["A Acute", "B Obtuse", "C Straight", "D Right"],
        "correct": ["A"], "hint": "Acute angles are less than 90 degrees.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "An angle larger than a right angle but smaller than a straight angle is called:",
        "options": ["A Obtuse", "B Acute", "C Right", "D Reflex"],
        "correct": ["A"], "hint": "Obtuse angles are greater than 90 degrees but less than 180 degrees.", "active": True
    },
    # --- Perimeter concept ---
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Perimeter is the distance:",
        "options": ["A Around the outside of a shape", "B Inside a shape", "C From one corner to the opposite corner", "D Of one side only"],
        "correct": ["A"], "hint": "Perimeter = the total length around the outside of a shape.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "A square has side length 5 cm. What is its perimeter?",
        "options": ["A 20 cm", "B 10 cm", "C 25 cm", "D 15 cm"],
        "correct": ["A"], "hint": "Perimeter of a square = 4 x side = 4 x 5 = 20 cm.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "A rectangle is 6 cm long and 3 cm wide. What is its perimeter?",
        "options": ["A 18 cm", "B 9 cm", "C 12 cm", "D 24 cm"],
        "correct": ["A"], "hint": "Perimeter = 2 x (length + width) = 2 x (6 + 3) = 18 cm.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which unit would you use to measure the perimeter of a playground?",
        "options": ["A Meters", "B Grams", "C Liters", "D Degrees"],
        "correct": ["A"], "hint": "Perimeter is a length measurement -- use meters or similar units.", "active": True
    },
    # --- Area concept ---
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Area measures the amount of:",
        "options": ["A Space inside a shape", "B Distance around a shape", "C Height of a shape", "D Weight of a shape"],
        "correct": ["A"], "hint": "Area = the inside space of a shape, measured in square units.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "A rectangle is 4 units wide and 5 units long. What is its area?",
        "options": ["A 20 square units", "B 9 square units", "C 18 square units", "D 40 square units"],
        "correct": ["A"], "hint": "Area = length x width = 5 x 4 = 20 square units.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Area is measured in:",
        "options": ["A Square units", "B Linear units", "C Cubic units", "D Degrees"],
        "correct": ["A"], "hint": "Area counts square tiles, so it uses square units.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "A square has side length 4 cm. What is its area?",
        "options": ["A 16 square cm", "B 8 square cm", "C 12 square cm", "D 4 square cm"],
        "correct": ["A"], "hint": "Area of square = side x side = 4 x 4 = 16 sq cm.", "active": True
    },
    # --- More shape identification / real world ---
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "The face of a clock is what shape?",
        "options": ["A Circle", "B Square", "C Rectangle", "D Triangle"],
        "correct": ["A"], "hint": "Most clock faces are round -- circles.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "A door is most like which shape?",
        "options": ["A Rectangle", "B Circle", "C Triangle", "D Hexagon"],
        "correct": ["A"], "hint": "A door is taller than it is wide -- a rectangle.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which shape could be used to tile a floor without leaving gaps or overlaps?",
        "options": ["A Square", "B Circle", "C Pentagon", "D Octagon"],
        "correct": ["A"], "hint": "Squares fit together perfectly to tile a flat surface.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "An ice cream cone is a combination of which two 3D shapes?",
        "options": ["A Cone and sphere", "B Cylinder and sphere", "C Cone and cylinder", "D Cube and cone"],
        "correct": ["A"], "hint": "The cone part is the wafer, and the ice cream scoop is a sphere.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which shape has parallel sides where both pairs of opposite sides are parallel?",
        "options": ["A Parallelogram", "B Triangle", "C Circle", "D Trapezoid"],
        "correct": ["A"], "hint": "A parallelogram has two pairs of parallel sides.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "How many faces does a rectangular prism have?",
        "options": ["A 6", "B 4", "C 8", "D 5"],
        "correct": ["A"], "hint": "A rectangular prism has 6 rectangular faces.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which 2D shape is found on each face of a cube?",
        "options": ["A Square", "B Rectangle", "C Triangle", "D Circle"],
        "correct": ["A"], "hint": "All 6 faces of a cube are squares.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which shape has 3 sides, where one angle is a right angle?",
        "options": ["A Right triangle", "B Equilateral triangle", "C Obtuse triangle", "D Scalene triangle"],
        "correct": ["A"], "hint": "A right triangle has one 90 degree angle.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "How many lines of symmetry does a regular pentagon have?",
        "options": ["A 5", "B 1", "C 2", "D 4"],
        "correct": ["A"], "hint": "A regular pentagon has 5 equal sides and 5 lines of symmetry.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "A shape is divided into 6 equal parts. Each part is called a:",
        "options": ["A Sixth", "B Fourth", "C Third", "D Half"],
        "correct": ["A"], "hint": "6 equal parts means each is one sixth.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "How many sides does an octagon have?",
        "options": ["A 8", "B 6", "C 7", "D 9"],
        "correct": ["A"], "hint": "'Octa' means eight.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "Which 3D shape has a triangular base?",
        "options": ["A Triangular pyramid", "B Rectangular prism", "C Cube", "D Cone"],
        "correct": ["A"], "hint": "A triangular pyramid (tetrahedron) has a triangular base.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "single",
        "text": "If you fold a shape on its line of symmetry, the two halves:",
        "options": ["A Match exactly", "B Are different sizes", "C Overlap slightly", "D Create a new shape"],
        "correct": ["A"], "hint": "A line of symmetry creates two identical halves.", "active": True
    },
]

g_numeric = [
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "numeric", "text": "How many sides does a hexagon have?",
        "options": None, "correct": 6, "hint": "'Hex' means six.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "numeric", "text": "How many faces does a cube have?",
        "options": None, "correct": 6, "hint": "A cube has 6 equal square faces.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "numeric", "text": "A square has a side length of 7 cm. What is its perimeter in cm?",
        "options": None, "correct": 28, "hint": "Perimeter = 4 x side = 4 x 7 = 28 cm.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "numeric", "text": "A rectangle is 8 units long and 3 units wide. What is its area in square units?",
        "options": None, "correct": 24, "hint": "Area = length x width = 8 x 3 = 24.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "numeric", "text": "How many vertices does a pentagon have?",
        "options": None, "correct": 5, "hint": "A pentagon has 5 sides and 5 vertices.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "numeric", "text": "How many edges does a cube have?",
        "options": None, "correct": 12, "hint": "A cube has 12 edges.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "numeric", "text": "A square has a side of 6 cm. What is its area in square cm?",
        "options": None, "correct": 36, "hint": "Area = 6 x 6 = 36 sq cm.", "active": True
    },
    {
        "subject": "Math", "domain": "G", "category": "Geometry",
        "type": "numeric", "text": "How many lines of symmetry does a square have?",
        "options": None, "correct": 4, "hint": "A square has 4 lines of symmetry.", "active": True
    },
]

# =============================================================================
# COUNTS
# =============================================================================
print(f"OA single: {len(oa_single)}, OA numeric: {len(oa_numeric)}, Total OA: {len(oa_single)+len(oa_numeric)}")
print(f"G single: {len(g_single)}, G numeric: {len(g_numeric)}, Total G: {len(g_single)+len(g_numeric)}")

# =============================================================================
# UPLOAD
# =============================================================================
print("\n--- Uploading Mult & Division Reasoning (OA) ---")
for i in range(0, len(oa_single), 25):
    batch = oa_single[i:i+25]
    print(f"  Uploading OA single batch {i//25+1} ({len(batch)} questions)...")
    upload_batch(batch)

for i in range(0, len(oa_numeric), 25):
    batch = oa_numeric[i:i+25]
    print(f"  Uploading OA numeric batch {i//25+1} ({len(batch)} questions)...")
    upload_batch(batch)

print(f"\nTotal OA uploaded: {len(oa_single) + len(oa_numeric)}")

print("\n--- Uploading Geometry (G) ---")
for i in range(0, len(g_single), 25):
    batch = g_single[i:i+25]
    print(f"  Uploading G single batch {i//25+1} ({len(batch)} questions)...")
    upload_batch(batch)

for i in range(0, len(g_numeric), 25):
    batch = g_numeric[i:i+25]
    print(f"  Uploading G numeric batch {i//25+1} ({len(batch)} questions)...")
    upload_batch(batch)

print(f"\nTotal G uploaded: {len(g_single) + len(g_numeric)}")
print("\nDone!")
