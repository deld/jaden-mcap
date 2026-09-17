"""
Deeper grade 4 fractions set (NF). Issue #43.

Original questions in the Singapore Math style: bar models, unit-fraction
reasoning in the hints, worked solutions. Covers the whole grade 4 NF
standard, not just the single fractions unit in the Singapore Math book.

    python3 upload_grade4_fractions.py           # dry run
    python3 upload_grade4_fractions.py --apply   # upload
"""
import json, sys, urllib.request

BASE = "https://zvffmucghcrqackghhlf.supabase.co/rest/v1"
KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp2ZmZtdWNnaGNycWFja2doaGxmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY3MjkyNTIsImV4cCI6MjA5MjMwNTI1Mn0.eJHX6LmInRdBd5nt9t_jBJwILGEQ6_SeN6ADorlsWic"
H    = {"Content-Type": "application/json", "apikey": KEY, "Authorization": f"Bearer {KEY}"}
L = "ABCDEFGH"

def mc(text, options, i, hint, solution):
    return {"type":"single","text":text,"options":list(options),"correct":[L[i]],"hint":hint,"solution":solution}
def num(text, answer, hint, solution):
    return {"type":"numeric","text":text,"options":None,"correct": answer,"hint":hint,"solution":solution}

UNITS = [

("Equivalent Fractions", [
  mc("Which fraction is equivalent to 3/4?", ["6/8", "4/5", "3/8", "9/16"], 0,
     "Multiply the top and the bottom by the same number.",
     "3/4 = (3 x 2)/(4 x 2) = 6/8"),
  mc("Which fraction is NOT equivalent to 1/2?", ["2/4", "5/10", "3/5", "6/12"], 2,
     "For 1/2, the top must be exactly half the bottom.",
     "2/4: 2 is half of 4 - yes\n5/10: 5 is half of 10 - yes\n3/5: 3 is not half of 5 - NO\n6/12: 6 is half of 12 - yes"),
  num("Fill in the missing number: 2/5 = ?/15", 6,
      "What did 5 get multiplied by to become 15? Do the same to the 2.",
      "5 x 3 = 15, so multiply the top by 3 too.\n2 x 3 = 6\n2/5 = 6/15"),
  num("Fill in the missing number: 4/6 = 2/?", 3,
      "What did 4 get divided by to become 2? Do the same to the 6.",
      "4 / 2 = 2, so divide the bottom by 2 too.\n6 / 2 = 3\n4/6 = 2/3"),
  mc("A strip is cut into 8 equal parts and 4 are shaded. Which is the same amount?", ["1/4", "1/2", "4/4", "2/8"], 1,
     "4 out of 8 - what simpler fraction is that?",
     "4/8 = (4 / 4)/(8 / 4) = 1/2\nHalf the strip is shaded."),
  mc("Which list shows only fractions equivalent to 2/3?", ["4/6, 6/9, 8/12", "4/6, 5/8, 6/9", "2/6, 4/6, 6/6", "3/4, 6/8, 9/12"], 0,
     "Each must be 2/3 scaled up by the same factor on top and bottom.",
     "2/3 x 2/2 = 4/6\n2/3 x 3/3 = 6/9\n2/3 x 4/4 = 8/12\nAll three in the first list are equivalent to 2/3."),
  num("Write 5/10 in its simplest form. What is the denominator?", 2,
      "Divide top and bottom by their biggest common factor.",
      "5 and 10 share the factor 5.\n5/10 = 1/2\nThe denominator is 2."),
]),

("Comparing Fractions", [
  mc("Which is greater: 5/8 or 3/8?", ["5/8", "3/8", "Equal", "Cannot tell"], 0,
     "Same denominator - compare the numerators.",
     "Both are eighths. 5 eighths is more than 3 eighths.\n5/8 > 3/8"),
  mc("Which is greater: 2/5 or 2/9?", ["2/5", "2/9", "Equal", "Cannot tell"], 0,
     "Same numerator - the SMALLER denominator means BIGGER pieces.",
     "Fifths are bigger pieces than ninths.\n2 big pieces > 2 small pieces.\n2/5 > 2/9"),
  mc("Which fraction is less than 1/2?", ["5/8", "3/8", "4/6", "7/12"], 1,
     "Compare each numerator to half its denominator.",
     "5/8: half of 8 is 4, and 5 > 4 - more than half\n3/8: 3 < 4 - LESS than half\n4/6: half of 6 is 3, 4 > 3 - more\n7/12: half of 12 is 6, 7 > 6 - more\nOnly 3/8 is less than 1/2."),
  mc("Order from least to greatest: 3/4, 1/4, 2/4", ["1/4, 2/4, 3/4", "3/4, 2/4, 1/4", "2/4, 1/4, 3/4", "1/4, 3/4, 2/4"], 0,
     "Same denominator, so order by the numerators.",
     "1 < 2 < 3, so 1/4 < 2/4 < 3/4"),
  mc("Which is greater: 3/4 or 5/6?", ["3/4", "5/6", "Equal", "Cannot tell"], 1,
     "Rewrite both with denominator 12.",
     "3/4 = 9/12\n5/6 = 10/12\n10/12 > 9/12, so 5/6 is greater."),
  mc("Which symbol makes this true?  4/10 ___ 2/5", ["<", ">", "="], 2,
     "Simplify 4/10.",
     "4/10 = 2/5\nThey are equal: 4/10 = 2/5"),
  mc("Jaden ate 3/8 of a pizza. Mia ate 1/3 of a same-size pizza. Who ate more?", ["Jaden", "Mia", "Same amount", "Cannot tell"], 0,
     "Rewrite both with denominator 24.",
     "3/8 = 9/24\n1/3 = 8/24\n9/24 > 8/24, so Jaden ate more."),
]),

("Adding & Subtracting Fractions", [
  mc("What is 2/6 + 3/6?", ["5/6", "5/12", "6/6", "1/6"], 0,
     "Same denominator - add the numerators, keep the denominator.",
     "2/6 + 3/6 = 5/6"),
  mc("What is 7/10 - 4/10?", ["3/10", "3/20", "11/10", "3"], 0,
     "Same denominator - subtract the numerators.",
     "7/10 - 4/10 = 3/10"),
  num("What is 3/8 + 3/8 + 2/8? Give the numerator (over 8).", 8,
      "Add all three numerators.",
      "3 + 3 + 2 = 8\n3/8 + 3/8 + 2/8 = 8/8 = 1 whole"),
  mc("Which shows 5/6 broken into a sum of smaller fractions?", ["1/6 + 4/6", "5/12 + 5/12", "1/2 + 1/3", "5/6 + 0"], 0,
     "The parts must have the same denominator and add to 5/6.",
     "1/6 + 4/6 = 5/6\nThat breaks 5/6 into two sixths-parts."),
  num("A ribbon is 9/10 m long. 4/10 m is cut off. How many tenths of a meter are left?", 5,
      "Draw a bar in 10 parts. Take away 4.",
      "9/10 - 4/10 = 5/10\n5 tenths of a meter are left."),
  mc("Sam ran 3/5 km before lunch and 1/5 km after. How far did he run in total?", ["4/5 km", "4/10 km", "2/5 km", "3/25 km"], 0,
     "Same denominator - add the numerators.",
     "3/5 + 1/5 = 4/5 km"),
  mc("What is 1 - 3/8?", ["5/8", "3/8", "1/8", "8/3"], 0,
     "Write 1 as 8/8 first.",
     "1 = 8/8\n8/8 - 3/8 = 5/8"),
]),

("Mixed Numbers", [
  mc("Write 7/4 as a mixed number.", ["1 3/4", "1 1/4", "2 1/4", "3 1/4"], 0,
     "How many whole 4/4 fit in 7/4? What is left over?",
     "7/4 = 4/4 + 3/4 = 1 + 3/4 = 1 3/4"),
  mc("Write 2 1/3 as an improper fraction.", ["7/3", "5/3", "6/3", "2/3"], 0,
     "Each whole is 3/3.",
     "2 wholes = 6/3\n6/3 + 1/3 = 7/3"),
  num("What is the whole-number part of 13/5?", 2,
      "How many times does 5 go into 13?",
      "13 / 5 = 2 remainder 3\n13/5 = 2 3/5\nThe whole-number part is 2."),
  mc("What is 1 2/5 + 2 1/5?", ["3 3/5", "3 1/5", "3 2/5", "4"], 0,
     "Add the wholes, then add the fractions.",
     "Wholes: 1 + 2 = 3\nFractions: 2/5 + 1/5 = 3/5\nTotal: 3 3/5"),
  mc("What is 3 5/8 - 1 2/8?", ["2 3/8", "2 7/8", "1 3/8", "2 1/8"], 0,
     "Subtract wholes from wholes and fractions from fractions.",
     "Wholes: 3 - 1 = 2\nFractions: 5/8 - 2/8 = 3/8\nAnswer: 2 3/8"),
  mc("Lila drank 1 1/4 liters of water in the morning and 3/4 liter in the afternoon. How much in total?",
     ["2 liters", "1 4/4 liters", "1 1/2 liters", "2 1/4 liters"], 0,
     "Add the fractions first - they may make a whole.",
     "1/4 + 3/4 = 4/4 = 1 whole\n1 + 1 = 2 liters"),
  num("How many quarters are in 3 1/4? (Give the numerator over 4.)", 13,
      "Each whole is 4 quarters.",
      "3 wholes = 12 quarters\n12 + 1 = 13\n3 1/4 = 13/4"),
]),

("Multiplying Fractions by Whole Numbers", [
  mc("What is 3 x 1/5?", ["3/5", "1/15", "3/15", "4/5"], 0,
     "3 x 1/5 means three fifths.",
     "1/5 + 1/5 + 1/5 = 3/5"),
  mc("What is 4 x 2/3?", ["8/3", "6/3", "2/12", "8/12"], 0,
     "Multiply the numerator by 4, keep the denominator.",
     "4 x 2/3 = 8/3 = 2 2/3"),
  num("What is 6 x 1/2?", 3,
      "Six halves make how many wholes?",
      "6 x 1/2 = 6/2 = 3"),
  num("A recipe needs 3/4 cup of flour. How many cups for 4 recipes?", 3,
      "4 groups of 3/4.",
      "4 x 3/4 = 12/4 = 3 cups"),
  mc("Each lap is 2/5 km. How far is 5 laps?", ["2 km", "10 km", "1 km", "2/25 km"], 0,
     "5 x 2/5 - the 5s cancel.",
     "5 x 2/5 = 10/5 = 2 km"),
  num("How many thirds are in 3 wholes?", 9,
      "Each whole is 3 thirds.",
      "3 x 3 = 9 thirds"),
]),

("Tenths & Hundredths", [
  mc("Which fraction equals 3/10?", ["30/100", "3/100", "13/100", "300/100"], 0,
     "Multiply top and bottom by 10.",
     "3/10 = (3 x 10)/(10 x 10) = 30/100"),
  num("What is 3/10 + 45/100? Give the numerator over 100.", 75,
      "Change 3/10 to hundredths first.",
      "3/10 = 30/100\n30/100 + 45/100 = 75/100"),
  mc("Which is greater: 7/10 or 68/100?", ["7/10", "68/100", "Equal", "Cannot tell"], 0,
     "Write 7/10 as hundredths.",
     "7/10 = 70/100\n70/100 > 68/100, so 7/10 is greater."),
  num("How many hundredths are in 1/2?", 50,
      "1/2 = 5/10 = ?/100",
      "1/2 = 50/100\nThere are 50 hundredths in a half."),
  mc("Write 9/100 + 4/10 as a single fraction over 100.", ["49/100", "13/100", "94/100", "13/110"], 0,
     "Change 4/10 to hundredths.",
     "4/10 = 40/100\n9/100 + 40/100 = 49/100"),
]),

("Decimals", [
  mc("Write 7/10 as a decimal.", ["0.7", "0.07", "7.0", "0.17"], 0,
     "Tenths go in the first place after the decimal point.",
     "7/10 = 0.7"),
  mc("Write 0.25 as a fraction.", ["25/100", "25/10", "2/5", "1/25"], 0,
     "Two places after the point means hundredths.",
     "0.25 = 25/100 (which simplifies to 1/4)"),
  mc("Which is greater: 0.6 or 0.58?", ["0.6", "0.58", "Equal", "Cannot tell"], 0,
     "Write both with two decimal places.",
     "0.6 = 0.60\n0.60 > 0.58, so 0.6 is greater."),
  mc("Which decimal equals 4/100?", ["0.04", "0.4", "4.0", "0.004"], 0,
     "Hundredths need two places after the point.",
     "4/100 = 0.04"),
  mc("Order from least to greatest: 0.5, 0.05, 0.55", ["0.05, 0.5, 0.55", "0.5, 0.05, 0.55", "0.55, 0.5, 0.05", "0.05, 0.55, 0.5"], 0,
     "Line up the decimal points and compare place by place.",
     "0.05 = 5 hundredths\n0.50 = 50 hundredths\n0.55 = 55 hundredths\n0.05 < 0.5 < 0.55"),
  num("What is 0.3 + 0.4? Give the answer as tenths (the digit after the point).", 7,
      "3 tenths plus 4 tenths.",
      "0.3 + 0.4 = 0.7\nThat is 7 tenths."),
  mc("A pencil is 0.8 dm long. That is the same as:", ["8/10 dm", "8/100 dm", "80 dm", "1/8 dm"], 0,
     "One place after the point means tenths.",
     "0.8 = 8/10 dm"),
]),
]

_LETTERS, _SEPS = "ABCDEFGH", (" ", ".", ")", "-", ":")
def strip_option_prefixes(options):
    if not isinstance(options, list) or len(options) < 2: return options
    def cut(o, ch):
        if not isinstance(o, str): return None
        t = o.lstrip()
        return t[2:].lstrip(" .)-:") if len(t) >= 2 and t[0] == ch and t[1] in _SEPS else None
    hits = sum(1 for i, o in enumerate(options) if i < len(_LETTERS) and cut(o, _LETTERS[i]) is not None)
    if hits < max(3, len(options) - 1): return options
    return [(cut(o, _LETTERS[i]) if i < len(_LETTERS) else None) or o for i, o in enumerate(options)]

def rows():
    out = []
    for category, qs in UNITS:
        for q in qs:
            out.append({"grade": 4, "subject": "Math", "domain": "NF", "category": category,
                        "type": q["type"], "text": q["text"], "options": strip_option_prefixes(q["options"]),
                        "correct": q["correct"], "hint": q["hint"], "solution": q["solution"],
                        "active": True, "source": "manual", "track": "test_prep"})
    return out

def post(batch):
    req = urllib.request.Request(f"{BASE}/questions", data=json.dumps(batch).encode(),
                                 method="POST", headers={**H, "Prefer": "return=minimal"})
    with urllib.request.urlopen(req) as r: return r.status

all_rows = rows()
from collections import Counter
print(f"{len(all_rows)} NF questions")
for k, v in Counter(r["category"] for r in all_rows).items(): print(f"  {v:2}  {k}")
if "--apply" not in sys.argv:
    print("\nDRY RUN. Re-run with --apply to upload."); sys.exit(0)
for i in range(0, len(all_rows), 25):
    print(f"  batch {i//25+1}: HTTP {post(all_rows[i:i+25])}")
print("Done!")
