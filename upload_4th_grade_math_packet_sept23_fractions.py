"""
Grade 4 Math packet, Sept 23 2026 — fractions (Exercises 20-23, pages 46-53).

The packet covers: missing numbers in fraction subtraction using equivalent
fractions (Ex 20), subtracting with unlike denominators in simplest form and
subtracting three fractions (pages 46/48), fraction word problems (Ex 21),
writing mixed numbers from models (Ex 22), and writing improper fractions
from models (Ex 23).

Questions below are NEW, with different numbers, modelled on the same skills.

Every computational answer carries a `verify` expression that this script
solves independently with `fractions.Fraction` before anything is uploaded --
the same generate-then-independently-solve idea as issue #69, done in code.

    python3 upload_4th_grade_math_packet_sept23_fractions.py           # dry run + verify
    python3 upload_4th_grade_math_packet_sept23_fractions.py --apply   # upload
"""
import json, re, sys, urllib.request
from fractions import Fraction
from collections import Counter

BASE = "https://zvffmucghcrqackghhlf.supabase.co/rest/v1"
KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp2ZmZtdWNnaGNycWFja2doaGxmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY3MjkyNTIsImV4cCI6MjA5MjMwNTI1Mn0.eJHX6LmInRdBd5nt9t_jBJwILGEQ6_SeN6ADorlsWic"
H    = {"Content-Type": "application/json", "apikey": KEY, "Authorization": f"Bearer {KEY}"}
L = "ABCDEFGH"

ASSIGNMENT = "Sept 23 Fractions Packet"
PACKET = {
    "student": "Jaden",
    "grade": 4,
    "subject": "Math",
    "week_of": "2026-09-23",
    "status": "approved",
    "notes": (
        "Fractions packet from Jaden's teacher (Exercises 20-23, pages 46-53, marked "
        "'4th week'). Covers: filling in missing numbers when subtracting fractions by "
        "rewriting with a common denominator (Ex 20), subtracting fractions with unlike "
        "denominators and writing the answer in simplest form, subtracting three fractions "
        "and 1 minus a fraction (pages 46/48), fraction word problems about cloth, money, "
        "lengths, juice and ribbon (Ex 21), writing a mixed number for a shaded model "
        "(Ex 22), and writing an improper fraction for a shaded model (Ex 23). Practice "
        "questions are newly generated with different numbers, modelled on the same skills."
    ),
}

# ── question builders ────────────────────────────────────────────────
def mc(text, options, i, hint, solution, verify=None):
    return {"type": "single", "text": text, "options": list(options), "correct": [L[i]],
            "hint": hint, "solution": solution, "_verify": verify, "_answer": options[i]}

def num(text, answer, hint, solution, verify=None, numerator=False):
    """`numerator=True` means the answer is the top of the rewritten fraction in
    `verify`, not its value -- 2/3 = 4/6 has the value 2/3 but the answer 4."""
    return {"type": "numeric", "text": text, "options": None, "correct": answer,
            "hint": hint, "solution": solution, "_verify": verify,
            "_answer": str(answer), "_numerator": numerator}

UNITS = [

# ── Ex 22: write a mixed number for the model ────────────────────────
("Mixed Numbers", [
  mc("Write a mixed number: 2 wholes and 3 fourths",
     ["2 3/4", "3 2/4", "2 4/3", "5 3/4"], 0,
     "The whole circles go in front, the shaded part of the last one goes after.",
     "2 whole shapes and 3 of 4 parts shaded.\nThat is 2 3/4.",
     verify=("2 + 3/4", "2 3/4")),
  mc("Write a mixed number: 4 wholes and 1 third",
     ["1 4/3", "4 1/3", "4 3/1", "5 1/3"], 1,
     "Wholes first, then the leftover fraction.",
     "4 whole shapes and 1 of 3 parts shaded.\nThat is 4 1/3.",
     verify=("4 + 1/3", "4 1/3")),
  mc("Write a mixed number: 3 wholes and 5 sixths",
     ["5 3/6", "3 6/5", "3 5/6", "8 5/6"], 2,
     "Wholes first, then the leftover fraction.",
     "3 whole shapes and 5 of 6 parts shaded.\nThat is 3 5/6.",
     verify=("3 + 5/6", "3 5/6")),
  mc("Write a mixed number: 2 wholes and 7 eighths",
     ["2 8/7", "9 7/8", "7 2/8", "2 7/8"], 3,
     "Wholes first, then the leftover fraction.",
     "2 whole shapes and 7 of 8 parts shaded.\nThat is 2 7/8.",
     verify=("2 + 7/8", "2 7/8")),
  mc("Write a mixed number: 5 wholes and 1 half",
     ["5 1/2", "1 5/2", "5 2/1", "6 1/2"], 0,
     "Wholes first, then the leftover fraction.",
     "5 whole shapes and 1 of 2 parts shaded.\nThat is 5 1/2.",
     verify=("5 + 1/2", "5 1/2")),
]),

# ── Ex 23: write an improper fraction for the model ──────────────────
("Improper Fractions", [
  mc("Write an improper fraction: 7 thirds",
     ["3/7", "7/3", "7/1", "1/7"], 1,
     "'Thirds' tells you the bottom number. Count how many you have for the top.",
     "7 thirds means 7 pieces, each one third.\nThat is 7/3.",
     verify=("7/3", "7/3")),
  mc("Write an improper fraction: 9 quarters",
     ["4/9", "9/4", "9/2", "9/1"], 1,
     "'Quarters' means the bottom number is 4.",
     "9 quarters means 9 pieces, each one quarter.\nThat is 9/4.",
     verify=("9/4", "9/4")),
  mc("Write an improper fraction: 13 sixths",
     ["13/6", "6/13", "13/1", "6/1"], 0,
     "'Sixths' means the bottom number is 6.",
     "13 sixths means 13 pieces, each one sixth.\nThat is 13/6.",
     verify=("13/6", "13/6")),
  mc("Write an improper fraction: 11 fifths",
     ["5/11", "11/1", "11/5", "1 1/5"], 2,
     "'Fifths' means the bottom number is 5.",
     "11 fifths means 11 pieces, each one fifth.\nThat is 11/5.",
     verify=("11/5", "11/5")),
  mc("Write an improper fraction: 15 eighths",
     ["8/15", "15/8", "15/1", "1 5/8"], 1,
     "'Eighths' means the bottom number is 8.",
     "15 eighths means 15 pieces, each one eighth.\nThat is 15/8.",
     verify=("15/8", "15/8")),
  mc("Write 2 3/4 as an improper fraction.",
     ["5/4", "23/4", "11/4", "6/4"], 2,
     "Each whole is 4 fourths. How many fourths are in 2 wholes?",
     "2 wholes = 8 fourths.\n8 fourths + 3 fourths = 11 fourths.\n2 3/4 = 11/4",
     verify=("2 + 3/4", "11/4")),
  mc("Write 17/5 as a mixed number.",
     ["3 2/5", "2 3/5", "3 1/5", "1 7/5"], 0,
     "How many whole groups of 5 fifths fit inside 17 fifths?",
     "17 / 5 = 3 remainder 2.\nSo 17/5 = 3 wholes and 2 fifths = 3 2/5.",
     verify=("17/5", "3 2/5")),
]),

# ── Ex 20: missing numbers via equivalent fractions ──────────────────
("Equivalent Fractions in Subtraction", [
  num("Fill in the missing number: 2/3 - 1/6 = ?/6 - 1/6",
      4,
      "Rewrite 2/3 with 6 on the bottom. What did 3 get multiplied by?",
      "3 x 2 = 6, so multiply the top by 2 as well.\n2 x 2 = 4\n2/3 = 4/6",
      verify=("2/3", "4/6"), numerator=True),
  num("Fill in the missing number: 5/6 - 1/2 = 5/6 - ?/6",
      3,
      "Rewrite 1/2 with 6 on the bottom. What did 2 get multiplied by?",
      "2 x 3 = 6, so multiply the top by 3 as well.\n1 x 3 = 3\n1/2 = 3/6",
      verify=("1/2", "3/6"), numerator=True),
  num("To work out 3/4 - 5/8, first rewrite 3/4 with 8 on the bottom. What is the new top number?",
      6,
      "4 x 2 = 8, so do the same to the top.",
      "3/4 = (3 x 2)/(4 x 2) = 6/8\nThen 6/8 - 5/8 = 1/8.",
      verify=("3/4", "6/8"), numerator=True),
]),

# ── p.48: subtract, simplest form ────────────────────────────────────
("Subtracting Fractions", [
  mc("Subtract. Write the answer in simplest form: 1/2 - 1/8",
     ["3/8", "1/6", "1/4", "4/8"], 0,
     "Rewrite halves as eighths first.",
     "1/2 = 4/8\n4/8 - 1/8 = 3/8",
     verify=("1/2 - 1/8", "3/8")),
  mc("Subtract. Write the answer in simplest form: 2/3 - 1/6",
     ["1/3", "5/6", "1/2", "1/6"], 2,
     "Rewrite thirds as sixths, then simplify at the end.",
     "2/3 = 4/6\n4/6 - 1/6 = 3/6\n3/6 = 1/2",
     verify=("2/3 - 1/6", "1/2")),
  mc("Subtract. Write the answer in simplest form: 3/4 - 1/6",
     ["2/2", "7/12", "1/2", "5/12"], 1,
     "Twelfths work for both fourths and sixths.",
     "3/4 = 9/12 and 1/6 = 2/12\n9/12 - 2/12 = 7/12",
     verify=("3/4 - 1/6", "7/12")),
  mc("Subtract. Write the answer in simplest form: 5/6 - 1/4",
     ["4/2", "1/2", "7/12", "5/24"], 2,
     "Twelfths work for both sixths and fourths.",
     "5/6 = 10/12 and 1/4 = 3/12\n10/12 - 3/12 = 7/12",
     verify=("5/6 - 1/4", "7/12")),
  mc("Subtract. Write the answer in simplest form: 7/10 - 1/5",
     ["6/5", "3/10", "1/2", "3/5"], 2,
     "Rewrite fifths as tenths, then simplify.",
     "1/5 = 2/10\n7/10 - 2/10 = 5/10\n5/10 = 1/2",
     verify=("7/10 - 1/5", "1/2")),
  mc("Subtract. Write the answer in simplest form: 5/8 - 1/2",
     ["4/6", "1/8", "1/4", "3/8"], 1,
     "Rewrite halves as eighths first.",
     "1/2 = 4/8\n5/8 - 4/8 = 1/8",
     verify=("5/8 - 1/2", "1/8")),
  mc("Subtract. Write the answer in simplest form: 11/12 - 1/4",
     ["10/8", "7/12", "2/3", "5/6"], 2,
     "Rewrite fourths as twelfths, then simplify.",
     "1/4 = 3/12\n11/12 - 3/12 = 8/12\n8/12 = 2/3",
     verify=("11/12 - 1/4", "2/3")),
  mc("Subtract. Write the answer in simplest form: 7/8 - 1/4",
     ["6/4", "3/4", "5/8", "1/2"], 2,
     "Rewrite fourths as eighths first.",
     "1/4 = 2/8\n7/8 - 2/8 = 5/8",
     verify=("7/8 - 1/4", "5/8")),
]),

# ── p.46 #4: subtract three fractions ────────────────────────────────
("Subtracting Three Fractions", [
  mc("Subtract. Write the answer in simplest form: 1 - 1/6 - 1/6",
     ["2/3", "1/6", "1/3", "5/6"], 0,
     "Write the 1 as 6/6 so everything is in sixths.",
     "1 = 6/6\n6/6 - 1/6 - 1/6 = 4/6\n4/6 = 2/3",
     verify=("1 - 1/6 - 1/6", "2/3")),
  mc("Subtract. Write the answer in simplest form: 7/8 - 1/8 - 2/8",
     ["3/8", "1/2", "5/8", "1/4"], 1,
     "All eighths already - just subtract, then simplify.",
     "7/8 - 1/8 - 2/8 = 4/8\n4/8 = 1/2",
     verify=("7/8 - 1/8 - 2/8", "1/2")),
  mc("Subtract. Write the answer in simplest form: 5/9 - 1/9 - 2/9",
     ["4/9", "2/9", "1/3", "8/9"], 1,
     "All ninths - subtract the tops and keep the bottom.",
     "5 - 1 - 2 = 2\n5/9 - 1/9 - 2/9 = 2/9",
     verify=("5/9 - 1/9 - 2/9", "2/9")),
  mc("Subtract. Write the answer in simplest form: 1 - 2/5 - 1/5",
     ["3/5", "2/5", "1/5", "2/10"], 1,
     "Write the 1 as 5/5.",
     "1 = 5/5\n5/5 - 2/5 - 1/5 = 2/5",
     verify=("1 - 2/5 - 1/5", "2/5")),
  mc("Subtract. Write the answer in simplest form: 1 - 3/10 - 1/10",
     ["7/10", "3/5", "2/5", "1/2"], 1,
     "Write the 1 as 10/10, then simplify at the end.",
     "1 = 10/10\n10/10 - 3/10 - 1/10 = 6/10\n6/10 = 3/5",
     verify=("1 - 3/10 - 1/10", "3/5")),
  mc("Subtract. Write the answer in simplest form: 11/12 - 5/12 - 2/12",
     ["1/6", "1/4", "1/3", "2/3"], 2,
     "All twelfths - subtract, then simplify.",
     "11 - 5 - 2 = 4\n4/12 = 1/3",
     verify=("11/12 - 5/12 - 2/12", "1/3")),
]),

# ── p.46 #3: the missing-number wheel, 1 minus a fraction ────────────
("One Minus a Fraction", [
  mc("Write the missing number: 1 - 1/4 = ?",
     ["1/4", "3/4", "1/2", "4/3"], 1,
     "Write the 1 as 4/4.",
     "1 = 4/4\n4/4 - 1/4 = 3/4",
     verify=("1 - 1/4", "3/4")),
  mc("Write the missing number: 1 - 2/5 = ?",
     ["3/5", "2/5", "1/5", "5/3"], 0,
     "Write the 1 as 5/5.",
     "1 = 5/5\n5/5 - 2/5 = 3/5",
     verify=("1 - 2/5", "3/5")),
  mc("Write the missing number: 1 - 5/8 = ?",
     ["5/8", "1/8", "3/8", "8/5"], 2,
     "Write the 1 as 8/8.",
     "1 = 8/8\n8/8 - 5/8 = 3/8",
     verify=("1 - 5/8", "3/8")),
  mc("Write the missing number: 1 - 3/7 = ?",
     ["7/4", "3/7", "1/7", "4/7"], 3,
     "Write the 1 as 7/7.",
     "1 = 7/7\n7/7 - 3/7 = 4/7",
     verify=("1 - 3/7", "4/7")),
  mc("Write the missing number: 1 - 7/12 = ?",
     ["5/12", "7/12", "1/12", "12/7"], 0,
     "Write the 1 as 12/12.",
     "1 = 12/12\n12/12 - 7/12 = 5/12",
     verify=("1 - 7/12", "5/12")),
  mc("Write the missing number: 1 - 5/9 = ?",
     ["5/9", "4/9", "1/9", "9/5"], 1,
     "Write the 1 as 9/9.",
     "1 = 9/9\n9/9 - 5/9 = 4/9",
     verify=("1 - 5/9", "4/9")),
]),

# ── Ex 21 / p.50: fraction word problems ─────────────────────────────
("Fraction Word Problems", [
  mc("Nadia bought a piece of cloth. She used 2/7 of it to make a dress. What fraction of the cloth did she have left?",
     ["2/7", "5/7", "1/7", "7/5"], 1,
     "The whole piece is 7/7. Take away the part she used.",
     "Whole cloth = 7/7\n7/7 - 2/7 = 5/7\nShe had 5/7 of the cloth left.",
     verify=("1 - 2/7", "5/7")),
  mc("A stick is 5/6 m long and a string is 1/3 m long. How much longer is the stick than the string?",
     ["1/2 m", "4/6 m", "1/3 m", "2/3 m"], 0,
     "Rewrite thirds as sixths, then subtract.",
     "1/3 = 2/6\n5/6 - 2/6 = 3/6\n3/6 = 1/2\nThe stick is 1/2 m longer.",
     verify=("5/6 - 1/3", "1/2")),
  mc("John spent 1/3 of his money on a toy car and 1/6 of his money on a pen. What fraction of his money did he spend altogether?",
     ["1/9", "2/9", "1/2", "2/3"], 2,
     "Rewrite thirds as sixths, then add, then simplify.",
     "1/3 = 2/6\n2/6 + 1/6 = 3/6\n3/6 = 1/2\nHe spent 1/2 of his money.",
     verify=("1/3 + 1/6", "1/2")),
  mc("Mary drank 2/5 liter of orange juice. Jim drank 1/10 liter less than Mary. How much orange juice did they drink altogether?",
     ["3/10 liter", "1/2 liter", "7/10 liter", "4/5 liter"], 2,
     "First find Jim's amount, then add the two together.",
     "Jim: 2/5 = 4/10, so 4/10 - 1/10 = 3/10 liter.\nTogether: 4/10 + 3/10 = 7/10 liter.",
     verify=("2/5 + (2/5 - 1/10)", "7/10")),
  mc("Lily bought 1 yd of ribbon. She used 1/3 yd to tie a package and 1/4 yd to make a bow. How much ribbon did she have left?",
     ["5/12 yd", "7/12 yd", "1/2 yd", "2/7 yd"], 0,
     "Twelfths work for both thirds and fourths. Write the 1 as 12/12.",
     "1 = 12/12, 1/3 = 4/12, 1/4 = 3/12\n12/12 - 4/12 - 3/12 = 5/12\nShe had 5/12 yd left.",
     verify=("1 - 1/3 - 1/4", "5/12")),
  mc("Sam had a whole pizza. He ate 3/8 of it and gave 1/4 of it to his sister. What fraction of the pizza was left?",
     ["1/2", "5/8", "3/8", "1/8"], 2,
     "Rewrite fourths as eighths and write the 1 as 8/8.",
     "1 = 8/8, 1/4 = 2/8\n8/8 - 3/8 - 2/8 = 3/8\n3/8 of the pizza was left.",
     verify=("1 - 3/8 - 1/4", "3/8")),
]),

# ── p.52: whole numbers and fractions together ───────────────────────
("Whole Numbers and Fractions", [
  mc("Fill in the blank: 3 + 1/2 =",
     ["3 1/2", "4 1/2", "1 3/2", "3/2"], 0,
     "A whole number plus a fraction makes a mixed number.",
     "3 + 1/2 = 3 1/2",
     verify=("3 + 1/2", "3 1/2")),
  mc("Fill in the blank: 4 - 1/4 =",
     ["3 1/4", "4 3/4", "3 3/4", "1/4"], 2,
     "Borrow one whole and write it as 4/4.",
     "4 = 3 + 4/4\n4/4 - 1/4 = 3/4\nSo 4 - 1/4 = 3 3/4",
     verify=("4 - 1/4", "3 3/4")),
  mc("Fill in the blank: 2 - 1/5 =",
     ["1 4/5", "2 1/5", "1 1/5", "2 4/5"], 0,
     "Borrow one whole and write it as 5/5.",
     "2 = 1 + 5/5\n5/5 - 1/5 = 4/5\nSo 2 - 1/5 = 1 4/5",
     verify=("2 - 1/5", "1 4/5")),
  mc("Fill in the blank: 3 - 1/3 =",
     ["3 1/3", "2 1/3", "2 2/3", "1 2/3"], 2,
     "Borrow one whole and write it as 3/3.",
     "3 = 2 + 3/3\n3/3 - 1/3 = 2/3\nSo 3 - 1/3 = 2 2/3",
     verify=("3 - 1/3", "2 2/3")),
  mc("Fill in the blank: 5 - 3/8 =",
     ["5 3/8", "4 3/8", "4 5/8", "2 5/8"], 2,
     "Borrow one whole and write it as 8/8.",
     "5 = 4 + 8/8\n8/8 - 3/8 = 5/8\nSo 5 - 3/8 = 4 5/8",
     verify=("5 - 3/8", "4 5/8")),
]),
]

# ── independent verification ─────────────────────────────────────────
_MIXED = re.compile(r"^(\d+)\s+(\d+)/(\d+)$")

def parse_value(s):
    """'3 3/4' -> 15/4, '5/12' -> 5/12, '7' -> 7. Units like ' m' are stripped."""
    s = s.strip().rstrip(".").replace(" liter", "").replace(" yd", "").replace(" m", "")
    s = s.strip()
    m = _MIXED.match(s)
    if m:
        w, n, d = (int(x) for x in m.groups())
        return w + Fraction(n, d)
    return Fraction(s)

def evaluate(expr):
    """Evaluate a +/- expression over fractions, with one level of parentheses."""
    while "(" in expr:
        i = expr.index("(")
        j = expr.index(")", i)
        expr = expr[:i] + str(evaluate(expr[i + 1:j])) + expr[j + 1:]
    tokens = re.findall(r"[+-]?\s*\d+(?:/\d+)?", expr)
    total = Fraction(0)
    for t in tokens:
        t = t.replace(" ", "")
        sign = -1 if t.startswith("-") else 1
        total += sign * Fraction(t.lstrip("+-"))
    return total

def check(q):
    """Return a failure string, or None if the question verifies."""
    v = q["_verify"]
    if v is None:
        return None
    expr, claimed = v
    got = evaluate(expr)
    want = parse_value(claimed)
    if got != want:
        return f"{expr} = {got}, but the solution says {claimed}"
    if q.get("_numerator"):
        # Answer is the numerator of the rewritten fraction, which must be equivalent.
        if int(q["_answer"]) != int(claimed.split("/")[0]):
            return f"answer {q['_answer']} is not the numerator of {claimed}"
        return None
    # The stated answer must be what the marked-correct option actually says.
    if parse_value(q["_answer"]) != got:
        return f"marked answer {q['_answer']!r} != computed {got}"
    # Fraction answers must be in simplest form (mixed numbers excluded).
    if "/" in claimed and not _MIXED.match(claimed.strip()):
        n, d = (int(x) for x in claimed.replace(" liter", "").replace(" yd", "")
                .replace(" m", "").strip().split("/"))
        if Fraction(n, d) != Fraction(n, d).limit_denominator(d) or \
           (Fraction(n, d).denominator != d):
            return f"answer {claimed} is not in simplest form"
    # No distractor may also be correct.
    for o in (q["options"] or []):
        if o == q["_answer"]:
            continue
        try:
            if parse_value(o) == got:
                return f"distractor {o!r} is also correct"
        except (ValueError, ZeroDivisionError):
            pass
    return None

# ── assemble ─────────────────────────────────────────────────────────
def rows():
    out = []
    for category, qs in UNITS:
        for q in qs:
            out.append({"grade": 4, "subject": "Math", "domain": "NF", "category": category,
                        "type": q["type"], "text": q["text"], "options": q["options"],
                        "correct": q["correct"], "hint": q["hint"], "solution": q["solution"],
                        "active": True, "source": "packet",
                        "track": "classwork", "assignment": ASSIGNMENT})
    return out

def post(path, payload, prefer="return=minimal"):
    req = urllib.request.Request(f"{BASE}/{path}", data=json.dumps(payload).encode(),
                                 method="POST", headers={**H, "Prefer": prefer})
    with urllib.request.urlopen(req) as r:
        body = r.read()
        return r.status, (json.loads(body) if body else None)

all_q = [q for _, qs in UNITS for q in qs]
failures = [(q["text"], msg) for q in all_q if (msg := check(q))]
verified = sum(1 for q in all_q if q["_verify"] is not None)

print(f"{len(all_q)} questions, {verified} with a checkable answer")
for k, v in Counter(c for c, qs in UNITS for _ in qs).items():
    print(f"  {v:2}  {k}")
print()
if failures:
    print(f"VERIFICATION FAILED ({len(failures)}):")
    for text, msg in failures:
        print(f"  - {text}\n      {msg}")
    sys.exit(1)
print(f"Verification passed: {verified}/{verified} computed answers agree.\n")

if "--apply" not in sys.argv:
    print("DRY RUN. Re-run with --apply to upload.")
    sys.exit(0)

print("Registering packet...")
status, body = post("packets", PACKET, prefer="return=representation")
print(f"  HTTP {status} -> packet id {body[0]['id']}")

print(f"\nUploading {len(all_q)} questions as '{ASSIGNMENT}'...")
batch_rows = rows()
for i in range(0, len(batch_rows), 25):
    print(f"  batch {i // 25 + 1}: HTTP {post('questions', batch_rows[i:i + 25])[0]}")
print("Done!")
