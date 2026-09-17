"""
Grade 4 Math questions modelled on the Singapore Math Level 3A/3B sequence.
Issue #41.

These are ORIGINAL questions written in the Singapore Math style - bar-model
word problems, mental-calculation decomposition, multi-step reasoning. The
book's 18-unit sequence is used as the curriculum map (category = unit name)
but no exercises are reproduced from it.

    python3 upload_singapore_math_grade4.py           # dry run
    python3 upload_singapore_math_grade4.py --apply   # upload
"""
import json, sys, urllib.request

BASE = "https://zvffmucghcrqackghhlf.supabase.co/rest/v1"
KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp2ZmZtdWNnaGNycWFja2doaGxmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY3MjkyNTIsImV4cCI6MjA5MjMwNTI1Mn0.eJHX6LmInRdBd5nt9t_jBJwILGEQ6_SeN6ADorlsWic"
H    = {"Content-Type": "application/json", "apikey": KEY, "Authorization": f"Bearer {KEY}"}

GRADE = 4
L = "ABCDEFGH"

def mc(text, options, correct_idx, hint, solution):
    """Multiple choice. correct_idx is the 0-based index into options."""
    return {"type": "single", "text": text, "options": list(options),
            "correct": [L[correct_idx]], "hint": hint, "solution": solution}

def num(text, answer, hint, solution):
    return {"type": "numeric", "text": text, "options": None,
            "correct": answer, "hint": hint, "solution": solution}

# (domain, category, [questions])
UNITS = [

("NBT", "Numbers to 10,000", [
  mc("What is the value of the digit 7 in 4,732?", ["7", "70", "700", "7,000"], 2,
     "Count the places from the right: ones, tens, hundreds.",
     "4,732 = 4 thousands + 7 hundreds + 3 tens + 2 ones.\nThe 7 is in the hundreds place, so its value is 700."),
  num("Write the number: six thousand, four hundred nine.", 6409,
      "There are no tens - put a 0 in the tens place.",
      "Six thousand = 6,000\nFour hundred = 400\nNine = 9\n6,000 + 400 + 0 + 9 = 6,409"),
  mc("Which number is greatest?", ["5,089", "5,098", "5,809", "5,088"], 2,
     "Compare the thousands first, then hundreds, then tens.",
     "All have 5 thousands.\nHundreds: 0, 0, 8, 0 - 5,809 has the most hundreds.\n5,809 is the greatest."),
  num("Round 3,468 to the nearest hundred.", 3500,
      "Look at the tens digit. 5 or more rounds up.",
      "3,468 is between 3,400 and 3,500.\nThe tens digit is 6, which is 5 or more, so round up.\n3,468 rounds to 3,500."),
  mc("What number is 1,000 more than 8,250?", ["8,350", "9,250", "8,251", "18,250"], 1,
     "Adding 1,000 changes only the thousands digit.",
     "8,250 + 1,000 = 9,250\nOnly the thousands digit changes: 8 becomes 9."),
  num("What is the missing number? 2,000 + ___ + 40 + 6 = 2,746", 700,
      "Match each part to its place value.",
      "2,746 = 2,000 + 700 + 40 + 6\nThe missing part is the hundreds: 700."),
]),

("NBT", "Adding to 10,000", [
  num("What is 2,345 + 1,829?", 4174,
      "Add ones, then tens, then hundreds, then thousands. Regroup when a column is 10 or more.",
      "Ones: 5 + 9 = 14 -> write 4, carry 1\nTens: 4 + 2 + 1 = 7\nHundreds: 3 + 8 = 11 -> write 1, carry 1\nThousands: 2 + 1 + 1 = 4\nAnswer: 4,174"),
  mc("A school library has 3,650 books. It receives 1,275 more. How many books does it have now?",
     ["4,825", "4,925", "4,915", "5,925"], 1,
     "Add the two amounts. Watch the regrouping in the hundreds.",
     "3,650 + 1,275\nOnes: 0 + 5 = 5\nTens: 5 + 7 = 12 -> write 2, carry 1\nHundreds: 6 + 2 + 1 = 9\nThousands: 3 + 1 = 4\nTotal: 4,925 books"),
  num("Find the sum of 4,999 and 2,001.", 7000,
      "Look for a friendly number. 4,999 is 1 less than 5,000.",
      "Think: 4,999 + 2,001 = (4,999 + 1) + (2,001 - 1) = 5,000 + 2,000 = 7,000"),
  num("What is 6,408 + 2,592?", 9000,
      "The ones and tens might add to make round numbers.",
      "Ones: 8 + 2 = 10 -> write 0, carry 1\nTens: 0 + 9 + 1 = 10 -> write 0, carry 1\nHundreds: 4 + 5 + 1 = 10 -> write 0, carry 1\nThousands: 6 + 2 + 1 = 9\nAnswer: 9,000"),
  mc("Which sum is closest to 8,000?", ["3,912 + 3,088", "4,500 + 4,499", "2,750 + 5,750", "6,010 + 1,090"], 2,
     "Work out each sum, then see how far each is from 8,000.",
     "3,912 + 3,088 = 7,000 (1,000 away)\n4,500 + 4,499 = 8,999 (999 away)\n2,750 + 5,750 = 8,500 (500 away)\n6,010 + 1,090 = 7,100 (900 away)\nClosest: 2,750 + 5,750 = 8,500"),
  num("Maya saved $1,860 in the spring and $2,375 in the summer. How much did she save in total?", 4235,
      "Draw a bar with two parts: spring and summer. The whole bar is the total.",
      "Spring: 1,860\nSummer: 2,375\nWhole = 1,860 + 2,375 = 4,235\nMaya saved $4,235."),
]),

("NBT", "Subtracting to 10,000", [
  num("What is 7,000 - 2,468?", 4532,
      "Subtracting from a round number needs regrouping all the way across.",
      "7,000 - 2,468\nThink of 7,000 as 6,999 + 1.\n6,999 - 2,468 = 4,531\n4,531 + 1 = 4,532"),
  mc("A stadium holds 9,500 people. 6,780 seats are taken. How many seats are empty?",
     ["2,720", "3,720", "2,820", "3,280"], 0,
     "Whole minus the part you know gives the missing part.",
     "Whole: 9,500\nTaken: 6,780\nEmpty = 9,500 - 6,780 = 2,720 seats"),
  num("Find the difference between 5,203 and 1,847.", 3356,
      "Line up the place values. Regroup where the top digit is smaller.",
      "5,203 - 1,847\nOnes: 3 - 7 can't do -> borrow: 13 - 7 = 6\nTens: 9 - 4 = 5 (after borrowing, 0 became 9)\nHundreds: 1 - 8 can't do -> borrow: 11 - 8 = 3\nThousands: 4 - 1 = 3\nAnswer: 3,356"),
  num("What is 8,000 - 3,999?", 4001,
      "3,999 is just 1 less than 4,000.",
      "8,000 - 4,000 = 4,000\nBut we subtracted 1 too many, so add it back: 4,000 + 1 = 4,001"),
  mc("Which subtraction gives 2,500?", ["6,000 - 3,500", "5,500 - 2,000", "7,000 - 4,600", "8,250 - 5,650"], 0,
     "Work out each one.",
     "6,000 - 3,500 = 2,500\n5,500 - 2,000 = 3,500\n7,000 - 4,600 = 2,400\n8,250 - 5,650 = 2,600\nOnly 6,000 - 3,500 gives 2,500."),
  num("A farmer had 4,320 apples. He sold 1,895. How many are left?", 2425,
      "Draw a bar for all the apples. Cut off the part sold.",
      "Whole: 4,320\nSold: 1,895\nLeft = 4,320 - 1,895 = 2,425 apples"),
]),

("OA", "Problem Solving: Add & Subtract", [
  num("Ben has 245 stickers. Amy has 180 more than Ben. How many stickers do they have altogether?", 670,
      "Find Amy's number first, then add both.",
      "Ben: 245\nAmy: 245 + 180 = 425\nAltogether: 245 + 425 = 670 stickers"),
  mc("A shop had 1,200 oranges. It sold 450 in the morning and 375 in the afternoon. How many are left?",
     ["375", "825", "425", "1,025"], 0,
     "Add the two parts sold first, then subtract from the whole.",
     "Sold: 450 + 375 = 825\nLeft: 1,200 - 825 = 375 oranges"),
  num("Sam scored 1,350 points. Lila scored 260 fewer than Sam. How many points did Lila score?", 1090,
      "'Fewer than' means Lila's bar is shorter.",
      "Sam: 1,350\nLila: 1,350 - 260 = 1,090 points"),
  num("Two numbers add up to 900. One number is 375. What is the other number?", 525,
      "Whole minus the known part.",
      "Whole: 900\nKnown part: 375\nOther part: 900 - 375 = 525"),
  mc("Mr. Lee drove 2,480 km in May and 1,695 km in June. How much farther did he drive in May?",
     ["785 km", "4,175 km", "885 km", "795 km"], 0,
     "'How much farther' means find the difference.",
     "May: 2,480\nJune: 1,695\nDifference: 2,480 - 1,695 = 785 km farther"),
  num("A tank holds 5,000 liters. After 1,850 liters are used, then 900 liters are added, how much is in the tank?", 4050,
      "Do the steps in order: subtract, then add.",
      "Start: 5,000\nAfter using: 5,000 - 1,850 = 3,150\nAfter adding: 3,150 + 900 = 4,050 liters"),
]),

("OA", "Multiplying by 6, 7, 8, 9", [
  num("What is 7 x 8?", 56, "7 x 8 = 7 x 4 x 2 = 28 x 2", "7 x 8 = 56\nThink: 7 x 4 = 28, then double it: 56."),
  mc("Which equals 9 x 6?", ["45", "54", "56", "63"], 1,
     "9 x 6 = (10 x 6) - 6",
     "10 x 6 = 60\n60 - 6 = 54\nSo 9 x 6 = 54."),
  num("A box holds 8 crayons. How many crayons are in 9 boxes?", 72,
      "9 groups of 8.",
      "9 x 8 = 72 crayons\nThink: 10 x 8 = 80, minus one group of 8 = 72."),
  num("What is 6 x 7?", 42, "6 x 7 = (5 x 7) + 7", "5 x 7 = 35\n35 + 7 = 42\nSo 6 x 7 = 42."),
  mc("There are 7 days in a week. How many days are in 9 weeks?", ["56", "61", "63", "70"], 2,
     "9 x 7 = (10 x 7) - 7",
     "10 x 7 = 70\n70 - 7 = 63\n9 weeks = 63 days"),
  num("Each spider has 8 legs. How many legs do 6 spiders have?", 48,
      "6 groups of 8.",
      "6 x 8 = 48 legs\nThink: 5 x 8 = 40, plus one more 8 = 48."),
]),

("NBT", "Multiplying Numbers", [
  num("What is 34 x 6?", 204,
      "Split 34 into 30 and 4. Multiply each by 6, then add.",
      "30 x 6 = 180\n4 x 6 = 24\n180 + 24 = 204"),
  mc("What is 125 x 4?", ["400", "480", "500", "520"], 2,
     "125 x 4: think of 125 as 100 + 25.",
     "100 x 4 = 400\n25 x 4 = 100\n400 + 100 = 500"),
  num("A carton has 48 eggs. How many eggs are in 7 cartons?", 336,
      "Break 48 into 40 and 8.",
      "40 x 7 = 280\n8 x 7 = 56\n280 + 56 = 336 eggs"),
  num("What is 209 x 3?", 627,
      "The 0 in the tens place means that column is 0.",
      "200 x 3 = 600\n0 x 3 = 0\n9 x 3 = 27\n600 + 0 + 27 = 627"),
  mc("Which is the same as 56 x 5?", ["50 x 5 + 6", "50 x 5 + 6 x 5", "56 + 5", "5 x 5 + 6 x 5"], 1,
     "Splitting 56 into 50 + 6 means multiplying BOTH parts by 5.",
     "56 x 5 = (50 + 6) x 5 = 50 x 5 + 6 x 5 = 250 + 30 = 280"),
  num("A bakery makes 175 muffins each day. How many does it make in 4 days?", 700,
      "175 x 4 - try 175 x 2 first, then double.",
      "175 x 2 = 350\n350 x 2 = 700\nSo 175 x 4 = 700 muffins"),
]),

("NBT", "Dividing Numbers", [
  num("What is 96 / 4?", 24,
      "Split 96 into 80 and 16 - both divide by 4.",
      "80 / 4 = 20\n16 / 4 = 4\n20 + 4 = 24"),
  mc("87 / 5 = ?", ["17 R2", "16 R7", "17 R3", "18 R1"], 0,
     "How many 5s fit in 87? What's left over?",
     "5 x 17 = 85\n87 - 85 = 2\nSo 87 / 5 = 17 R2"),
  num("Share 156 stickers equally among 6 friends. How many does each get?", 26,
      "Split 156 into 120 and 36.",
      "120 / 6 = 20\n36 / 6 = 6\n20 + 6 = 26 stickers each"),
  num("What is the remainder when 74 is divided by 8?", 2,
      "Find the biggest multiple of 8 that fits in 74.",
      "8 x 9 = 72\n74 - 72 = 2\nRemainder is 2."),
  mc("245 / 7 = ?", ["35", "34", "36", "33"], 0,
     "Split 245 into 210 and 35.",
     "210 / 7 = 30\n35 / 7 = 5\n30 + 5 = 35"),
  num("A rope 135 cm long is cut into 9 equal pieces. How long is each piece in cm?", 15,
      "Split 135 into 90 and 45.",
      "90 / 9 = 10\n45 / 9 = 5\n10 + 5 = 15 cm each"),
]),

("OA", "Problem Solving: Multiply & Divide", [
  num("A box has 24 cookies. Jaden buys 5 boxes and eats 17 cookies. How many cookies are left?", 103,
      "Multiply first to find the total, then subtract.",
      "Total: 24 x 5 = 120\nLeft: 120 - 17 = 103 cookies"),
  mc("Three friends share 72 marbles equally. Then each gives away 6. How many does each have left?",
     ["18", "24", "30", "66"], 0,
     "Divide first, then subtract.",
     "Each gets: 72 / 3 = 24\nAfter giving away: 24 - 6 = 18 marbles each"),
  num("A ribbon is 4 times as long as a pencil. The pencil is 18 cm. How long is the ribbon in cm?", 72,
      "'4 times as long' - draw 1 bar for the pencil and 4 equal bars for the ribbon.",
      "Pencil: 18 cm (1 unit)\nRibbon: 4 units = 4 x 18 = 72 cm"),
  num("Ana has 3 times as many books as Tom. Together they have 48 books. How many does Tom have?", 12,
      "Tom is 1 unit, Ana is 3 units. Together that's 4 units.",
      "4 units = 48\n1 unit = 48 / 4 = 12\nTom has 12 books."),
  mc("Pencils come in packs of 8. Mrs. Green needs 60 pencils. How many packs must she buy?",
     ["7", "8", "9", "60"], 1,
     "60 / 8 has a remainder - she needs a whole extra pack for the leftover.",
     "60 / 8 = 7 R4\n7 packs = 56 pencils, not enough.\nShe must buy 8 packs (64 pencils)."),
  num("A theater has 15 rows with 22 seats each. If 280 seats are taken, how many are empty?", 50,
      "Multiply to find total seats, then subtract.",
      "Total: 15 x 22 = 330\nEmpty: 330 - 280 = 50 seats"),
]),

("NBT", "Mental Calculations", [
  num("Calculate mentally: 47 + 38", 85,
      "Move 3 from the 38 to the 47 to make a round 50.",
      "47 + 38 = (47 + 3) + (38 - 3) = 50 + 35 = 85"),
  mc("Calculate mentally: 25 x 12", ["250", "300", "275", "325"], 1,
     "25 x 4 = 100, and 12 = 4 x 3.",
     "25 x 12 = 25 x 4 x 3 = 100 x 3 = 300"),
  num("Calculate mentally: 83 - 29", 54,
      "29 is 1 less than 30.",
      "83 - 30 = 53\nWe took away 1 too many, so add it back: 53 + 1 = 54"),
  num("Calculate mentally: 48 x 5", 240,
      "Multiplying by 5 is the same as multiplying by 10 and halving.",
      "48 x 10 = 480\n480 / 2 = 240"),
  mc("Calculate mentally: 199 + 356", ["545", "555", "565", "455"], 1,
     "199 is 1 less than 200.",
     "200 + 356 = 556\nWe added 1 too many, so subtract it: 556 - 1 = 555"),
  num("Calculate mentally: 600 / 25", 24,
      "How many 25s in 100? Then how many 100s in 600?",
      "100 / 25 = 4\n600 = 6 x 100, so 600 / 25 = 6 x 4 = 24"),
]),

("MD", "Money", [
  num("Jaden has $12.50. He spends $4.75. How much is left, in cents?", 775,
      "Convert to cents first: $12.50 = 1,250 cents.",
      "$12.50 = 1,250 cents\n$4.75 = 475 cents\n1,250 - 475 = 775 cents ($7.75)"),
  mc("A notebook costs $3.45 and a pen costs $1.80. What is the total?", ["$5.25", "$4.25", "$5.35", "$5.15"], 0,
     "Add the dollars and the cents.",
     "$3.45 + $1.80\nCents: 45 + 80 = 125 cents = $1.25\nDollars: 3 + 1 + 1 = 5\nTotal: $5.25"),
  num("How many quarters make $3.75?", 15,
      "4 quarters = $1.",
      "$3 = 12 quarters\n$0.75 = 3 quarters\n12 + 3 = 15 quarters"),
  num("Mia buys 4 packs of gum at $1.25 each. She pays with a $10 bill. How much change does she get, in cents?", 500,
      "Find the total cost first, then subtract from $10.",
      "Cost: 4 x $1.25 = $5.00\nChange: $10.00 - $5.00 = $5.00 = 500 cents"),
  mc("Which amount is greatest?", ["6 dimes and 3 nickels", "2 quarters and 2 dimes", "70 cents", "1 quarter and 4 dimes"], 0,
     "Convert each to cents.",
     "6 dimes + 3 nickels = 60 + 15 = 75 cents\n2 quarters + 2 dimes = 50 + 20 = 70 cents\n70 cents\n1 quarter + 4 dimes = 25 + 40 = 65 cents\nGreatest: 75 cents"),
  num("A toy costs $8.60. Leo has $5.35. How much more does he need, in cents?", 325,
      "Difference between the price and what he has.",
      "$8.60 = 860 cents\n$5.35 = 535 cents\n860 - 535 = 325 cents ($3.25)"),
]),

("MD", "Length, Mass & Volume", [
  num("How many centimeters are in 3 meters 45 centimeters?", 345,
      "1 m = 100 cm.",
      "3 m = 300 cm\n300 + 45 = 345 cm"),
  mc("Which is the heaviest?", ["2 kg", "1,500 g", "2,050 g", "1 kg 900 g"], 2,
     "Convert everything to grams. 1 kg = 1,000 g.",
     "2 kg = 2,000 g\n1,500 g\n2,050 g\n1 kg 900 g = 1,900 g\nHeaviest: 2,050 g"),
  num("A bottle holds 1 liter 250 milliliters. How many milliliters is that?", 1250,
      "1 L = 1,000 mL.",
      "1 L = 1,000 mL\n1,000 + 250 = 1,250 mL"),
  num("A rope is 5 m long. 180 cm is cut off. How many cm are left?", 320,
      "Convert 5 m to cm first.",
      "5 m = 500 cm\n500 - 180 = 320 cm"),
  mc("A watermelon has a mass of 3 kg 250 g. A pumpkin is 1 kg 800 g. How much heavier is the watermelon?",
     ["1 kg 450 g", "2 kg 450 g", "1 kg 550 g", "5 kg 50 g"], 0,
     "Convert both to grams, subtract, then convert back.",
     "3 kg 250 g = 3,250 g\n1 kg 800 g = 1,800 g\n3,250 - 1,800 = 1,450 g = 1 kg 450 g"),
  num("A jug holds 2 L. Sam pours out 750 mL. How many mL are left?", 1250,
      "2 L = 2,000 mL.",
      "2,000 - 750 = 1,250 mL"),
]),

("MD", "Problem Solving: Measurement", [
  num("A path is 240 m long. Kai walks it 3 times. How many meters does he walk in total?", 720,
      "3 groups of 240.",
      "240 x 3 = 720 m"),
  mc("A bag of rice weighs 2 kg 500 g. A shop sells 4 bags. What is the total mass?",
     ["8 kg", "10 kg", "9 kg 500 g", "10 kg 500 g"], 1,
     "2 kg 500 g = 2,500 g. Multiply by 4.",
     "2,500 g x 4 = 10,000 g = 10 kg"),
  num("A ribbon 3 m 60 cm long is cut into 4 equal pieces. How long is each piece in cm?", 90,
      "Convert to cm, then divide.",
      "3 m 60 cm = 360 cm\n360 / 4 = 90 cm each"),
  num("A tank had 5 L of water. 1 L 300 mL leaked out, then 800 mL was added. How many mL are in the tank now?", 4500,
      "Do it step by step in mL.",
      "Start: 5,000 mL\nAfter leak: 5,000 - 1,300 = 3,700 mL\nAfter adding: 3,700 + 800 = 4,500 mL"),
  mc("Ella is 1 m 32 cm tall. Her brother is 28 cm shorter. How tall is her brother?",
     ["1 m 4 cm", "1 m 14 cm", "1 m 60 cm", "104 m"], 0,
     "Convert to cm, subtract, convert back.",
     "1 m 32 cm = 132 cm\n132 - 28 = 104 cm = 1 m 4 cm"),
  num("A truck carries 6 boxes. Each box is 45 kg. What is the total mass in kg?", 270,
      "6 groups of 45.",
      "45 x 6 = 270 kg\nThink: 40 x 6 = 240, 5 x 6 = 30, total 270."),
]),

("MD", "Bar Graphs", [
  mc("A bar graph shows: Apples 12, Bananas 8, Cherries 15, Dates 5. Which fruit has the tallest bar?",
     ["Apples", "Bananas", "Cherries", "Dates"], 2,
     "The tallest bar is the biggest number.",
     "Cherries = 15, which is the largest.\nThe tallest bar is Cherries."),
  num("A bar graph shows: Apples 12, Bananas 8, Cherries 15, Dates 5. How many fruits in total?", 40,
      "Add all four bars.",
      "12 + 8 + 15 + 5 = 40"),
  num("A bar graph shows: Apples 12, Bananas 8, Cherries 15, Dates 5. How many more cherries than bananas?", 7,
      "Difference between the two bars.",
      "15 - 8 = 7 more cherries"),
  mc("A graph's scale goes up by 5 each line. A bar reaches 3 lines above zero. What value does it show?",
     ["3", "8", "15", "35"], 2,
     "Each line is worth 5.",
     "3 lines x 5 = 15"),
  num("Votes for class pet: Dog 15, Cat 11, Fish 6, Hamster 9. How many students voted?", 41,
      "Add all the votes.",
      "15 + 11 + 6 + 9 = 41 students"),
  mc("Votes for class pet: Dog 15, Cat 11, Fish 6, Hamster 9. Which two together equal the Dog votes?",
     ["Cat and Fish", "Fish and Hamster", "Cat and Hamster", "Dog and Fish"], 1,
     "Try adding pairs to reach 15.",
     "Cat + Fish = 17\nFish + Hamster = 15\nCat + Hamster = 20\nFish + Hamster = 15 = Dog"),
]),

("NF", "Fractions", [
  mc("Which fraction is equivalent to 2/3?", ["3/4", "4/6", "2/6", "6/8"], 1,
     "Multiply the top and bottom by the same number.",
     "2/3 = (2 x 2)/(3 x 2) = 4/6"),
  num("What is 3/8 + 2/8? Give the numerator of the answer (over 8).", 5,
      "Same denominator - just add the tops.",
      "3/8 + 2/8 = 5/8\nThe numerator is 5."),
  mc("Which is larger: 3/5 or 3/8?", ["3/5", "3/8", "They are equal", "Cannot tell"], 0,
     "Same numerator - the smaller denominator means bigger pieces.",
     "Fifths are bigger pieces than eighths.\n3 big pieces > 3 small pieces, so 3/5 is larger."),
  num("What is 3/4 of 24?", 18,
      "Find 1/4 first, then multiply by 3.",
      "1/4 of 24 = 24 / 4 = 6\n3/4 of 24 = 6 x 3 = 18"),
  mc("A pizza is cut into 8 equal slices. Jaden eats 3. What fraction is left?", ["3/8", "5/8", "3/5", "8/5"], 1,
     "Whole = 8/8. Take away 3/8.",
     "8/8 - 3/8 = 5/8 left"),
  num("Simplify 6/9. What is the numerator of the simplest form?", 2,
      "Divide top and bottom by their common factor.",
      "6 and 9 are both divisible by 3.\n6/9 = 2/3\nThe numerator is 2."),
]),

("MD", "Time", [
  mc("A movie starts at 2:45 PM and lasts 1 hour 30 minutes. When does it end?", ["3:15 PM", "4:15 PM", "4:05 PM", "3:45 PM"], 1,
     "Add the hour first, then the minutes.",
     "2:45 + 1 hour = 3:45\n3:45 + 30 min = 4:15 PM"),
  num("How many minutes are in 2 hours 25 minutes?", 145,
      "1 hour = 60 minutes.",
      "2 hours = 120 min\n120 + 25 = 145 minutes"),
  mc("Sofia started homework at 4:10 PM and finished at 5:35 PM. How long did it take?",
     ["1 hour 25 min", "1 hour 15 min", "1 hour 35 min", "55 min"], 0,
     "Count from 4:10 to 5:10, then to 5:35.",
     "4:10 to 5:10 = 1 hour\n5:10 to 5:35 = 25 min\nTotal: 1 hour 25 min"),
  mc("A train leaves at 9:20 AM and the trip takes 3 hours 50 minutes. When does it arrive?",
     ["12:10 PM", "1:10 PM", "12:50 PM", "1:50 PM"], 1,
     "Add 3 hours, then 50 minutes. Watch for crossing noon.",
     "9:20 + 3 hours = 12:20 PM\n12:20 + 50 min = 1:10 PM"),
  mc("How many seconds are in 4 minutes?", ["120", "180", "240", "400"], 2,
     "1 minute = 60 seconds.",
     "4 x 60 = 240 seconds"),
  num("A clock shows 7:55. What time will it show in 35 minutes? Enter the minutes part (0-59).", 30,
      "55 + 35 crosses the hour.",
      "7:55 + 5 min = 8:00\n8:00 + 30 min = 8:30\nThe minutes part is 30."),
]),

("G", "Angles", [
  mc("An angle that measures exactly 90 degrees is called a:", ["right angle", "acute angle", "obtuse angle", "straight angle"], 0,
     "Think of the corner of a square.",
     "A 90-degree angle is a right angle - like the corner of a book."),
  mc("An angle of 45 degrees is:", ["right", "acute", "obtuse", "straight"], 1,
     "Acute means less than 90.",
     "45 is less than 90, so it is acute."),
  mc("An angle of 120 degrees is:", ["right", "acute", "obtuse", "straight"], 2,
     "Obtuse means more than 90 but less than 180.",
     "120 is between 90 and 180, so it is obtuse."),
  num("How many degrees are in a straight angle?", 180,
      "A straight line is like two right angles side by side.",
      "2 x 90 = 180 degrees"),
  num("Two angles together make a right angle. One is 35 degrees. What is the other?", 55,
      "The two must add to 90.",
      "90 - 35 = 55 degrees"),
  mc("How many right angles are in a rectangle?", ["2", "3", "4", "6"], 2,
     "Count the corners.",
     "A rectangle has 4 corners, each a right angle."),
]),

("G", "Perpendicular & Parallel Lines", [
  mc("Two lines that never meet, no matter how far they go, are:", ["perpendicular", "parallel", "intersecting", "curved"], 1,
     "Think of railway tracks.",
     "Lines that stay the same distance apart and never meet are parallel."),
  mc("Two lines that cross to make right angles are:", ["parallel", "perpendicular", "equal", "obtuse"], 1,
     "Think of a plus sign (+).",
     "Lines that meet at 90 degrees are perpendicular."),
  mc("Which capital letter has a pair of parallel lines?", ["A", "T", "H", "V"], 2,
     "Look for two lines going the same direction.",
     "H has two vertical lines that are parallel."),
  mc("Which capital letter has perpendicular lines?", ["N", "L", "V", "W"], 1,
     "Look for a corner that makes a right angle.",
     "L has a vertical and a horizontal line meeting at a right angle."),
  num("How many pairs of parallel sides does a rectangle have?", 2,
      "Opposite sides of a rectangle are parallel.",
      "Top and bottom are one pair. Left and right are another. That's 2 pairs."),
  mc("A square has how many pairs of perpendicular sides?", ["1", "2", "4", "8"], 2,
     "Each corner is a right angle. Count the corners.",
     "A square has 4 right-angle corners, so 4 pairs of perpendicular sides."),
]),

("MD", "Area & Perimeter", [
  num("A rectangle is 9 cm long and 4 cm wide. What is its area in square cm?", 36,
      "Area = length x width.",
      "9 x 4 = 36 square cm"),
  num("A rectangle is 9 cm long and 4 cm wide. What is its perimeter in cm?", 26,
      "Perimeter = all four sides added, or 2 x (length + width).",
      "2 x (9 + 4) = 2 x 13 = 26 cm"),
  mc("A square has a side of 7 m. What is its area?", ["14 sq m", "28 sq m", "49 sq m", "77 sq m"], 2,
     "All sides of a square are equal.",
     "7 x 7 = 49 square meters"),
  num("A square has a perimeter of 32 cm. How long is one side in cm?", 8,
      "Four equal sides add up to 32.",
      "32 / 4 = 8 cm"),
  mc("A rectangle has an area of 48 sq cm and a length of 8 cm. What is its width?", ["4 cm", "6 cm", "40 cm", "56 cm"], 1,
     "Area = length x width, so width = area / length.",
     "48 / 8 = 6 cm"),
  num("A garden is 12 m by 5 m. A fence goes all the way around it. How many meters of fence are needed?", 34,
      "Fence = perimeter.",
      "2 x (12 + 5) = 2 x 17 = 34 m"),
]),
]

# ── Option-prefix guard (issue #29) ─────────────────────────────────────
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
    for domain, category, qs in UNITS:
        for q in qs:
            out.append({
                "grade": GRADE, "subject": "Math", "domain": domain, "category": category,
                "type": q["type"], "text": q["text"],
                "options": strip_option_prefixes(q["options"]),
                "correct": q["correct"], "hint": q["hint"], "solution": q["solution"],
                "active": True, "source": "manual", "track": "test_prep",
            })
    return out

def post(batch):
    req = urllib.request.Request(f"{BASE}/questions", data=json.dumps(batch).encode(),
                                 method="POST", headers={**H, "Prefer": "return=minimal"})
    with urllib.request.urlopen(req) as r: return r.status

all_rows = rows()
from collections import Counter
print(f"{len(all_rows)} questions across {len(UNITS)} units")
for k, v in Counter(r["domain"] for r in all_rows).items(): print(f"  {k}: {v}")
print(f"  single: {sum(1 for r in all_rows if r['type']=='single')}, numeric: {sum(1 for r in all_rows if r['type']=='numeric')}")

if "--apply" not in sys.argv:
    print("\nDRY RUN. Re-run with --apply to upload."); sys.exit(0)

for i in range(0, len(all_rows), 25):
    print(f"  batch {i//25+1}: HTTP {post(all_rows[i:i+25])}")
print("Done!")
