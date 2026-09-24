"""
69 grade 4 multi-digit addition and subtraction questions (NBT).

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

# 68 Addition & Subtraction questions (domain NBT)
questions = [
    # --- SINGLE CHOICE ---
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 348 + 275?","options":["A 613","B 623","C 523","D 633"],"correct":["A"],"hint":"Add the ones: 8+5=13, carry 1. Tens: 4+7+1=12, carry 1. Hundreds: 3+2+1=6.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 503 - 187?","options":["A 326","B 316","C 336","D 416"],"correct":["B"],"hint":"503 - 187: borrow from hundreds. 503 - 187 = 316.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 456 + 378?","options":["A 824","B 834","C 744","D 934"],"correct":["B"],"hint":"6+8=14, carry 1. 5+7+1=13, carry 1. 4+3+1=8. Answer: 834.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 700 - 263?","options":["A 437","B 447","C 537","D 427"],"correct":["A"],"hint":"700 - 263. Borrow across zeros. 700 - 263 = 437.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"Round 348 to the nearest hundred. Which is closest?","options":["A 300","B 400","C 350","D 340"],"correct":["A"],"hint":"348 is between 300 and 400. The tens digit is 4, so round down to 300.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"Which addition shows three numbers with a sum of 450?","options":["A 150 + 150 + 150","B 200 + 100 + 100","C 100 + 200 + 200","D 150 + 200 + 100"],"correct":["A"],"hint":"150 + 150 + 150 = 450.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"Jaden had 512 stickers. He gave away 278. How many does he have left?","options":["A 234","B 244","C 334","D 224"],"correct":["A"],"hint":"512 - 278 = 234.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"Which is the best estimate for 489 + 312?","options":["A 700","B 800","C 900","D 600"],"correct":["B"],"hint":"489 ≈ 500, 312 ≈ 300. 500 + 300 = 800.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 125 + 246 + 318?","options":["A 689","B 679","C 699","D 589"],"correct":["A"],"hint":"125 + 246 = 371. 371 + 318 = 689.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 900 - 456?","options":["A 454","B 444","C 544","D 434"],"correct":["B"],"hint":"900 - 456 = 444.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"Which best estimates 621 - 289?","options":["A 200","B 300","C 400","D 500"],"correct":["B"],"hint":"621 ≈ 600, 289 ≈ 300. 600 - 300 = 300.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"A library has 364 fiction books and 285 nonfiction books. How many books total?","options":["A 639","B 649","C 649","D 749"],"correct":["B"],"hint":"364 + 285 = 649.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 537 + 284?","options":["A 811","B 821","C 721","D 831"],"correct":["B"],"hint":"7+4=11, carry 1. 3+8+1=12, carry 1. 5+2+1=8. Answer: 821.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 600 - 348?","options":["A 252","B 262","C 352","D 242"],"correct":["A"],"hint":"600 - 348 = 252.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"Maria scored 175 points on Monday and 243 points on Tuesday. How many points total?","options":["A 408","B 418","C 318","D 428"],"correct":["B"],"hint":"175 + 243 = 418.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 472 - 195?","options":["A 287","B 277","C 377","D 267"],"correct":["B"],"hint":"472 - 195 = 277.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"Which shows a mental math strategy for 398 + 46?","options":["A 400 + 44","B 400 + 46","C 398 + 40 + 6","D Both A and C"],"correct":["D"],"hint":"398 + 46 = 400 + 44 = 444. Also 398 + 40 + 6 = 444.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 219 + 367 + 104?","options":["A 690","B 680","C 700","D 670"],"correct":["A"],"hint":"219 + 367 = 586. 586 + 104 = 690.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"A farmer harvested 423 apples and 359 oranges. How many fruits in all?","options":["A 782","B 772","C 792","D 682"],"correct":["A"],"hint":"423 + 359 = 782.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 801 - 356?","options":["A 455","B 445","C 545","D 465"],"correct":["B"],"hint":"801 - 356 = 445.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"Which is the best estimate for 712 - 398?","options":["A 200","B 300","C 400","D 100"],"correct":["B"],"hint":"712 ≈ 700, 398 ≈ 400. 700 - 400 = 300.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"A school collected 285 cans on Monday and 347 cans on Wednesday. How many total?","options":["A 622","B 632","C 532","D 642"],"correct":["B"],"hint":"285 + 347 = 632.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 563 - 278?","options":["A 295","B 285","C 385","D 275"],"correct":["B"],"hint":"563 - 278 = 285.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is the missing number? 436 + ___ = 700","options":["A 264","B 274","C 364","D 254"],"correct":["A"],"hint":"700 - 436 = 264.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"Tom read 132 pages in week 1, 215 pages in week 2, and 189 pages in week 3. How many total?","options":["A 526","B 536","C 436","D 546"],"correct":["B"],"hint":"132 + 215 = 347. 347 + 189 = 536.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 999 - 456?","options":["A 543","B 553","C 443","D 533"],"correct":["A"],"hint":"999 - 456 = 543.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"Which addition makes 1000?","options":["A 450 + 550","B 400 + 500","C 600 + 300","D 350 + 650"],"correct":["A"],"hint":"450 + 550 = 1000.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 675 + 248?","options":["A 923","B 913","C 833","D 933"],"correct":["A"],"hint":"5+8=13, carry 1. 7+4+1=12, carry 1. 6+2+1=9. Answer: 923.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"A pet store has 487 fish. They sell 193. How many remain?","options":["A 294","B 304","C 284","D 394"],"correct":["A"],"hint":"487 - 193 = 294.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 345 + 299 using mental math?","options":["A 644","B 654","C 634","D 664"],"correct":["A"],"hint":"345 + 300 = 645, then subtract 1: 644.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"Which is 500 - 237?","options":["A 273","B 263","C 363","D 253"],"correct":["B"],"hint":"500 - 237 = 263.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"There are 318 boys and 276 girls in a school. How many students in all?","options":["A 594","B 584","C 694","D 604"],"correct":["A"],"hint":"318 + 276 = 594.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 750 - 389?","options":["A 371","B 361","C 461","D 381"],"correct":["B"],"hint":"750 - 389 = 361.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 243 + 158 + 299?","options":["A 700","B 690","C 710","D 680"],"correct":["A"],"hint":"243 + 158 = 401. 401 + 299 = 700.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"A baker made 425 cookies. She sold 278. How many are left?","options":["A 157","B 147","C 247","D 167"],"correct":["B"],"hint":"425 - 278 = 147.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is the best estimate for 524 + 189?","options":["A 600","B 700","C 800","D 500"],"correct":["B"],"hint":"524 ≈ 500, 189 ≈ 200. 500 + 200 = 700.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 1000 - 573?","options":["A 427","B 437","C 527","D 417"],"correct":["A"],"hint":"1000 - 573 = 427.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"A truck carried 364 boxes on trip 1 and 287 boxes on trip 2. How many boxes total?","options":["A 651","B 641","C 741","D 661"],"correct":["A"],"hint":"364 + 287 = 651.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 408 - 169?","options":["A 249","B 239","C 339","D 259"],"correct":["B"],"hint":"408 - 169 = 239.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 199 + 399?","options":["A 598","B 588","C 608","D 598"],"correct":["A"],"hint":"200 + 400 = 600, subtract 2: 598.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"There were 825 people at the park. 369 left. How many remained?","options":["A 456","B 466","C 556","D 446"],"correct":["A"],"hint":"825 - 369 = 456.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 467 + 366?","options":["A 833","B 823","C 733","D 843"],"correct":["A"],"hint":"7+6=13, carry 1. 6+6+1=13, carry 1. 4+3+1=8. Answer: 833.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 300 - 148?","options":["A 152","B 142","C 162","D 252"],"correct":["A"],"hint":"300 - 148 = 152.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"A store sold 156 items on Friday, 234 on Saturday, and 178 on Sunday. How many total?","options":["A 568","B 558","C 578","D 468"],"correct":["A"],"hint":"156 + 234 = 390. 390 + 178 = 568.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 582 + 319?","options":["A 901","B 891","C 911","D 801"],"correct":["A"],"hint":"2+9=11, carry 1. 8+1+1=10, carry 1. 5+3+1=9. Answer: 901.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"single","text":"What is 643 - 298?","options":["A 345","B 355","C 245","D 335"],"correct":["A"],"hint":"643 - 298 = 345. (643 - 300 = 343, + 2 = 345)","active":True},
    # --- NUMERIC ---
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"numeric","text":"What is 348 + 275?","options":None,"correct":623,"hint":"Add ones: 8+5=13, carry 1. Tens: 4+7+1=12, carry 1. Hundreds: 3+2+1=6. Answer: 623.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"numeric","text":"What is 503 - 187?","options":None,"correct":316,"hint":"503 - 187 = 316.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"numeric","text":"What is 456 + 378?","options":None,"correct":834,"hint":"456 + 378 = 834.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"numeric","text":"What is 700 - 263?","options":None,"correct":437,"hint":"700 - 263 = 437.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"numeric","text":"What is 219 + 367 + 104?","options":None,"correct":690,"hint":"219 + 367 = 586. 586 + 104 = 690.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"numeric","text":"What is 900 - 456?","options":None,"correct":444,"hint":"900 - 456 = 444.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"numeric","text":"What is 537 + 284?","options":None,"correct":821,"hint":"537 + 284 = 821.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"numeric","text":"What is 601 - 348?","options":None,"correct":253,"hint":"601 - 348 = 253.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"numeric","text":"What is 472 - 195?","options":None,"correct":277,"hint":"472 - 195 = 277.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"numeric","text":"What is 563 - 278?","options":None,"correct":285,"hint":"563 - 278 = 285.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"numeric","text":"What is 675 + 248?","options":None,"correct":923,"hint":"675 + 248 = 923.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"numeric","text":"What is 1000 - 573?","options":None,"correct":427,"hint":"1000 - 573 = 427.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"numeric","text":"What is 243 + 158 + 299?","options":None,"correct":700,"hint":"243 + 158 = 401. 401 + 299 = 700.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"numeric","text":"What is 408 - 169?","options":None,"correct":239,"hint":"408 - 169 = 239.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"numeric","text":"What is 364 + 287?","options":None,"correct":651,"hint":"364 + 287 = 651.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"numeric","text":"What is 750 - 389?","options":None,"correct":361,"hint":"750 - 389 = 361.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"numeric","text":"What is 156 + 234 + 178?","options":None,"correct":568,"hint":"156 + 234 = 390. 390 + 178 = 568.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"numeric","text":"What is 582 + 319?","options":None,"correct":901,"hint":"582 + 319 = 901.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"numeric","text":"What is 643 - 298?","options":None,"correct":345,"hint":"643 - 300 + 2 = 345.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"numeric","text":"What is 825 - 369?","options":None,"correct":456,"hint":"825 - 369 = 456.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"numeric","text":"What is 467 + 366?","options":None,"correct":833,"hint":"467 + 366 = 833.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"numeric","text":"What is 300 - 148?","options":None,"correct":152,"hint":"300 - 148 = 152.","active":True},
    {"subject":"Math","domain":"NBT","category":"Addition & Subtraction","type":"numeric","text":"What is 436 + 264?","options":None,"correct":700,"hint":"436 + 264 = 700.","active":True},
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
