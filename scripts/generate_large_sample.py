# scripts/generate_large_sample.py
import random
from datetime import datetime, timedelta

senders = ["Abhishek", "Priya", "Rahul", "Sneha"]
words = ["hey", "kya", "haal", "chal", "movie", "dekhte", "hain", "kal", "office", "mein"]

lines = []
current = datetime(2023, 1, 1, 9, 0)
for _ in range(50_000):
    current += timedelta(minutes=random.randint(1, 30))
    sender = random.choice(senders)
    text = " ".join(random.choices(words, k=random.randint(1, 10)))
    lines.append(f"{current.strftime('%d/%m/%y')}, {current.strftime('%H:%M')} - {sender}: {text}")

with open("large_sample.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Generated 50,000 message sample file: large_sample.txt")