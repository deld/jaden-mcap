"""
63 grade 4 fractions questions (NF).

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

# 63 Fractions questions (domain NF)
questions = [
    # --- SINGLE CHOICE ---
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction is larger: 1/3 or 1/4?","options":["A 1/3","B 1/4","C They are equal","D Cannot tell"],"correct":["A"],"hint":"With unit fractions, the smaller the denominator, the larger the piece. 1/3 > 1/4.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction is larger: 3/4 or 3/8?","options":["A 3/8","B 3/4","C They are equal","D Cannot tell"],"correct":["B"],"hint":"Same numerator. Larger denominator means smaller pieces. 3/4 > 3/8.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction equals 1/2?","options":["A 2/6","B 3/6","C 4/6","D 1/4"],"correct":["B"],"hint":"3/6 = 1/2 because 3 is half of 6.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"A pizza is cut into 8 equal slices. You eat 3. What fraction did you eat?","options":["A 3/5","B 5/8","C 3/8","D 8/3"],"correct":["C"],"hint":"You ate 3 out of 8 slices = 3/8.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which point on a number line from 0 to 1 shows 1/4?","options":["A Halfway between 0 and 1","B One quarter of the way from 0 to 1","C Three quarters of the way","D At the 1 mark"],"correct":["B"],"hint":"1/4 is one quarter of the way from 0 to 1.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction is equivalent to 2/4?","options":["A 1/4","B 1/2","C 2/6","D 3/4"],"correct":["B"],"hint":"2/4 = 1/2. Divide both numerator and denominator by 2.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"A ribbon is divided into 6 equal parts. 4 parts are red. What fraction is red?","options":["A 2/6","B 4/6","C 6/4","D 4/2"],"correct":["B"],"hint":"4 out of 6 parts = 4/6.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction is less than 1/2?","options":["A 3/4","B 2/3","C 3/8","D 5/6"],"correct":["C"],"hint":"3/8 < 1/2 because 3/8 < 4/8.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction is greater than 1/2?","options":["A 1/3","B 2/6","C 3/4","D 1/4"],"correct":["C"],"hint":"3/4 > 1/2 because 3/4 > 2/4.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"What fraction of a shape is shaded if 2 out of 3 equal parts are shaded?","options":["A 1/3","B 3/2","C 2/3","D 2/1"],"correct":["C"],"hint":"2 shaded out of 3 equal parts = 2/3.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which shows 1/3 on a number line from 0 to 1?","options":["A The point at 1/4","B The point one third of the way from 0 to 1","C The point at 1/2","D The point at 2/3"],"correct":["B"],"hint":"1/3 is one third of the way from 0 to 1.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction is equivalent to 4/8?","options":["A 1/4","B 2/4","C 1/2","D Both B and C"],"correct":["D"],"hint":"4/8 = 2/4 = 1/2. All are equivalent.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Compare: 5/6 ___ 5/8","options":["A <","B >","C =","D Cannot compare"],"correct":["B"],"hint":"Same numerator. 6 < 8, so pieces of sixths are bigger. 5/6 > 5/8.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction represents the whole?","options":["A 3/4","B 4/4","C 4/3","D 1/4"],"correct":["B"],"hint":"When numerator equals denominator, the fraction equals 1 whole. 4/4 = 1.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"A chocolate bar has 8 equal pieces. Sam ate 1 piece. What fraction remains?","options":["A 7/8","B 1/8","C 8/7","D 1/7"],"correct":["A"],"hint":"8 - 1 = 7 pieces left. 7 out of 8 = 7/8.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which is a unit fraction?","options":["A 3/4","B 2/3","C 1/6","D 5/8"],"correct":["C"],"hint":"A unit fraction has 1 as the numerator. 1/6 is a unit fraction.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Compare: 2/4 ___ 2/6","options":["A <","B >","C =","D Cannot compare"],"correct":["B"],"hint":"Same numerator. 4 < 6 means fourths are bigger pieces. 2/4 > 2/6.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction is closest to 0?","options":["A 1/2","B 1/8","C 1/3","D 1/4"],"correct":["B"],"hint":"Unit fractions: larger denominator = smaller fraction. 1/8 is closest to 0.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction is closest to 1?","options":["A 1/2","B 3/4","C 7/8","D 5/6"],"correct":["C"],"hint":"7/8 = 0.875, closest to 1 among the choices.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"A garden is divided into 4 equal sections. 3 sections have flowers. What fraction has flowers?","options":["A 1/4","B 3/4","C 4/3","D 3/1"],"correct":["B"],"hint":"3 out of 4 sections = 3/4.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction is equivalent to 2/3?","options":["A 4/6","B 3/6","C 2/6","D 6/9 and 4/6"],"correct":["D"],"hint":"2/3 = 4/6 (multiply by 2) = 6/9 (multiply by 3).","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"On a number line, which fraction comes between 1/4 and 3/4?","options":["A 1/8","B 1/2","C 7/8","D 1/3"],"correct":["B"],"hint":"1/2 = 2/4, which is between 1/4 and 3/4.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"A shape has 6 equal parts. 2 are blue. What fraction is NOT blue?","options":["A 2/6","B 4/6","C 6/4","D 2/4"],"correct":["B"],"hint":"6 - 2 = 4 parts not blue. 4 out of 6 = 4/6.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which set of fractions is in order from least to greatest?","options":["A 3/4, 1/2, 1/4","B 1/4, 1/2, 3/4","C 1/2, 1/4, 3/4","D 3/4, 1/4, 1/2"],"correct":["B"],"hint":"1/4 < 1/2 < 3/4. Order from least to greatest.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction is equivalent to 1/4?","options":["A 2/6","B 2/8","C 3/8","D 3/6"],"correct":["B"],"hint":"1/4 = 2/8. Multiply both by 2.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"A pie is cut into 3 equal slices. Jack eats 1 slice. What fraction did Jack eat?","options":["A 1/2","B 2/3","C 1/3","D 3/1"],"correct":["C"],"hint":"1 out of 3 equal slices = 1/3.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction means the same as 'half'?","options":["A 1/3","B 2/4","C 1/4","D 3/6 and 2/4"],"correct":["D"],"hint":"Both 3/6 and 2/4 equal 1/2.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Compare: 1/6 ___ 1/8","options":["A <","B >","C =","D Cannot compare"],"correct":["B"],"hint":"Unit fractions: smaller denominator = larger piece. 1/6 > 1/8.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"There are 8 crayons. 3 are red. What fraction are red?","options":["A 5/8","B 3/5","C 3/8","D 8/3"],"correct":["C"],"hint":"3 red out of 8 total = 3/8.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction is NOT equivalent to 1/2?","options":["A 2/4","B 3/6","C 4/6","D 4/8"],"correct":["C"],"hint":"4/6 = 2/3, not 1/2. The others all equal 1/2.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"A number line goes from 0 to 1. Where is 3/4 located?","options":["A At 1/4 of the way","B At the middle","C At 3/4 of the way from 0 to 1","D At the end"],"correct":["C"],"hint":"3/4 is three quarters of the way from 0 to 1.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction has the greatest value?","options":["A 1/2","B 1/3","C 1/6","D 1/8"],"correct":["A"],"hint":"With the same numerator of 1, the smallest denominator gives the greatest value. 1/2 is greatest.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"A sandwich is cut into 4 equal parts. Mom eats 2 parts. What fraction did Mom eat?","options":["A 1/4","B 2/4","C 3/4","D 4/2"],"correct":["B"],"hint":"2 out of 4 parts = 2/4 (or 1/2).","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which shows 5/6 on a number line from 0 to 1?","options":["A Five sixths of the way from 0 to 1","B One sixth of the way from 0 to 1","C At the 1 mark","D At the halfway point"],"correct":["A"],"hint":"5/6 is five sixths of the way from 0 to 1.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Compare: 4/6 ___ 4/8","options":["A <","B >","C =","D Cannot tell"],"correct":["B"],"hint":"Same numerator. Sixths are larger pieces than eighths. 4/6 > 4/8.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction is between 0 and 1/2 on the number line?","options":["A 3/4","B 5/6","C 1/4","D 2/3"],"correct":["C"],"hint":"1/4 = 0.25, which is between 0 and 0.5.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"What fraction of 8 equal parts is shaded if 6 are shaded?","options":["A 2/8","B 6/8","C 8/6","D 3/4"],"correct":["B"],"hint":"6 shaded out of 8 total = 6/8.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction equals 2/2?","options":["A 1/2","B 0","C 1","D 2"],"correct":["C"],"hint":"When numerator = denominator, fraction = 1 whole. 2/2 = 1.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Order from greatest to least: 7/8, 1/2, 3/8","options":["A 1/2, 3/8, 7/8","B 3/8, 1/2, 7/8","C 7/8, 1/2, 3/8","D 7/8, 3/8, 1/2"],"correct":["C"],"hint":"7/8 > 4/8 > 3/8. So 7/8 > 1/2 > 3/8.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"A class of 6 students split a cake equally. What fraction does each student get?","options":["A 1/3","B 1/6","C 6/1","D 2/6"],"correct":["B"],"hint":"6 students share equally = 1/6 each.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction is equivalent to 3/4?","options":["A 6/8","B 4/6","C 3/8","D 6/4"],"correct":["A"],"hint":"3/4 = 6/8. Multiply both by 2.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Compare 2/3 and 2/8. Which is larger?","options":["A 2/3","B 2/8","C They are equal","D Cannot compare"],"correct":["A"],"hint":"Same numerator. Thirds are larger pieces than eighths. 2/3 > 2/8.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"A rectangle is divided into 4 equal parts. 1 part is shaded. What fraction is shaded?","options":["A 4/1","B 1/3","C 1/4","D 3/4"],"correct":["C"],"hint":"1 shaded out of 4 equal parts = 1/4.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction is the smallest?","options":["A 3/4","B 5/8","C 2/3","D 1/6"],"correct":["D"],"hint":"1/6 is the smallest. Compare: 1/6 ≈ 0.17, less than all others.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"A number line is divided into 8 equal parts between 0 and 1. The point at the 4th mark equals what fraction?","options":["A 4/8","B 1/2","C Both A and B","D 3/8"],"correct":["C"],"hint":"The 4th mark out of 8 = 4/8 = 1/2. Both are correct.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Tom ate 3/8 of a pizza, Sara ate 5/8. Who ate more?","options":["A Tom","B Sara","C They ate the same","D Cannot tell"],"correct":["B"],"hint":"5/8 > 3/8. Sara ate more.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction is equivalent to 6/8?","options":["A 1/2","B 2/3","C 3/4","D 4/6"],"correct":["C"],"hint":"6/8 = 3/4. Divide both by 2.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"A shape is divided into 3 equal parts. All parts are shaded. What fraction is shaded?","options":["A 1/3","B 2/3","C 3/3","D 0/3"],"correct":["C"],"hint":"All 3 parts shaded = 3/3 = 1 whole.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction is closest to 1/2?","options":["A 1/3","B 3/8","C 1/4","D 1/8"],"correct":["B"],"hint":"3/8 = 0.375, closest to 0.5 among these choices.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"If you fold a square of paper in half and then in half again, what fraction is one part?","options":["A 1/2","B 1/4","C 1/3","D 1/8"],"correct":["B"],"hint":"Folding in half twice creates 4 equal parts. Each part = 1/4.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which pair of fractions is equivalent?","options":["A 1/2 and 2/6","B 1/3 and 2/6","C 2/4 and 3/8","D 3/4 and 6/10"],"correct":["B"],"hint":"1/3 = 2/6. Multiply both numerator and denominator by 2.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"A bag has 8 marbles. 3 are blue, 2 are red, 3 are green. What fraction are blue?","options":["A 5/8","B 3/5","C 3/8","D 2/8"],"correct":["C"],"hint":"3 blue marbles out of 8 total = 3/8.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction is greater: 4/4 or 3/4?","options":["A 3/4","B 4/4","C They are equal","D Cannot compare"],"correct":["B"],"hint":"4/4 = 1 whole, which is greater than 3/4.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"A number line from 0 to 1 is split into 6 equal parts. The second mark is at what fraction?","options":["A 1/6","B 2/6","C 3/6","D 4/6"],"correct":["B"],"hint":"The second mark out of 6 equal parts = 2/6.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which word describes a fraction where the top and bottom numbers are equal?","options":["A Zero","B A half","C One whole","D Improper"],"correct":["C"],"hint":"When numerator = denominator (like 4/4), the fraction equals 1 whole.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"A stick is divided into 8 equal parts. You color 6 parts. What fraction is colored?","options":["A 6/8","B 2/8","C 3/4","D Both A and C"],"correct":["D"],"hint":"6/8 is colored, which simplifies to 3/4. Both are correct.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction is NOT between 0 and 1/2?","options":["A 1/4","B 1/6","C 3/8","D 5/8"],"correct":["D"],"hint":"5/8 = 0.625 > 0.5. It is greater than 1/2, not between 0 and 1/2.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"What does the bottom number (denominator) of a fraction tell you?","options":["A How many parts are shaded","B How many equal parts the whole is divided into","C The size of the whole","D How many pieces you ate"],"correct":["B"],"hint":"The denominator tells you how many equal parts the whole is divided into.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which fraction is equivalent to 4/6?","options":["A 1/2","B 2/3","C 3/4","D 6/4"],"correct":["B"],"hint":"4/6 = 2/3. Divide both by 2.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"There are 6 flowers. 4 are yellow. What fraction are NOT yellow?","options":["A 4/6","B 2/6","C 1/3","D Both B and C"],"correct":["D"],"hint":"6 - 4 = 2 not yellow. 2/6 = 1/3. Both are correct.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which describes 1/2 on a number line from 0 to 2?","options":["A At the start","B At the end","C Halfway between 0 and 1","D Halfway between 1 and 2"],"correct":["C"],"hint":"1/2 is halfway between 0 and 1.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"A rectangle has 4 equal parts. 3 are shaded. Which fraction is shaded?","options":["A 1/4","B 3/4","C 4/3","D 3/3"],"correct":["B"],"hint":"3 shaded out of 4 equal parts = 3/4.","active":True},
    {"subject":"Math","domain":"NF","category":"Fractions","type":"single","text":"Which pair shows equivalent fractions?","options":["A 1/2 and 3/8","B 2/3 and 4/6","C 1/4 and 3/6","D 3/4 and 2/3"],"correct":["B"],"hint":"2/3 = 4/6. Multiply both by 2.","active":True},
]

print(f"Total questions: {len(questions)}")
single_qs = [q for q in questions if q['type'] == 'single']
numeric_qs = [q for q in questions if q['type'] == 'numeric']
print(f"Single: {len(single_qs)}, Numeric: {len(numeric_qs)}")

total_uploaded = 0
for qs in [single_qs, numeric_qs]:
    for i in range(0, len(qs), 25):
        upload_batch(qs[i:i+25])
        total_uploaded += len(qs[i:i+25])

print(f"Done. Total uploaded: {total_uploaded}")
