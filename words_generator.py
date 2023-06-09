import csv
import requests

response = requests.get("https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english.txt")
words = response.text.splitlines()
words_needed = 300

with open("top_300_words.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Word"])
    writer.writerows([[word] for word in words[:words_needed]])

print("CSV file 'top_300_words.csv' created successfully.")
