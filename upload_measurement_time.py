"""
10 grade 4 measurement and time questions (MD).

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

# 10 Measurement & Time questions (domain MD)
questions = [
    # --- SINGLE CHOICE ---
    {"subject":"Math","domain":"MD","category":"Measurement & Time","type":"single","text":"A clock shows the hour hand on 3 and the minute hand on 12. What time is it?","options":["A 12:03","B 3:00","C 3:12","D 12:15"],"correct":["B"],"hint":"Hour hand on 3, minute hand on 12 = 3:00.","active":True},
    {"subject":"Math","domain":"MD","category":"Measurement & Time","type":"single","text":"School starts at 8:15 AM and ends at 3:15 PM. How many hours is the school day?","options":["A 6 hours","B 7 hours","C 8 hours","D 5 hours"],"correct":["B"],"hint":"From 8:15 AM to 3:15 PM = 7 hours.","active":True},
    {"subject":"Math","domain":"MD","category":"Measurement & Time","type":"single","text":"Which unit would you use to measure the length of a classroom?","options":["A Inches","B Feet or meters","C Miles","D Pounds"],"correct":["B"],"hint":"A classroom is best measured in feet or meters.","active":True},
    {"subject":"Math","domain":"MD","category":"Measurement & Time","type":"single","text":"A clock shows 7:45. What time will it be in 30 minutes?","options":["A 7:15","B 8:15","C 8:45","D 7:75"],"correct":["B"],"hint":"7:45 + 30 minutes = 8:15.","active":True},
    {"subject":"Math","domain":"MD","category":"Measurement & Time","type":"single","text":"A desk is about 3 feet long. How many inches is that?","options":["A 24 inches","B 36 inches","C 12 inches","D 30 inches"],"correct":["B"],"hint":"1 foot = 12 inches. 3 × 12 = 36 inches.","active":True},
    {"subject":"Math","domain":"MD","category":"Measurement & Time","type":"single","text":"Which is the best unit to measure the mass of a backpack?","options":["A Grams","B Kilograms","C Meters","D Liters"],"correct":["B"],"hint":"Kilograms are used to measure the mass of larger objects like backpacks.","active":True},
    {"subject":"Math","domain":"MD","category":"Measurement & Time","type":"single","text":"Jaden wakes up at 6:30 AM. He takes 45 minutes to get ready. What time does he finish?","options":["A 7:00 AM","B 7:15 AM","C 7:45 AM","D 6:45 AM"],"correct":["B"],"hint":"6:30 + 45 minutes = 7:15 AM.","active":True},
    # --- NUMERIC ---
    {"subject":"Math","domain":"MD","category":"Measurement & Time","type":"numeric","text":"A movie starts at 2:10 PM and lasts 50 minutes. At what time (in minutes past 2 PM) does it end? Write the minutes only (e.g. 60 for 3:00 PM).","options":None,"correct":60,"hint":"2:10 PM + 50 minutes = 3:00 PM. That is 60 minutes past 2 PM.","active":True},
    {"subject":"Math","domain":"MD","category":"Measurement & Time","type":"numeric","text":"A rope is 2 meters long. How many centimeters long is it? (1 meter = 100 centimeters)","options":None,"correct":200,"hint":"2 meters × 100 cm = 200 cm.","active":True},
    {"subject":"Math","domain":"MD","category":"Measurement & Time","type":"numeric","text":"A juice pitcher holds 4 liters. How many cups is that if 1 liter = 4 cups?","options":None,"correct":16,"hint":"4 liters × 4 cups per liter = 16 cups.","active":True},
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
