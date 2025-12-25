import os
import re
import time
import datetime
import random
import webbrowser
import urllib.request
import urllib.parse
import html
import json
import textwrap
import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

# GREETINGS

class Greeting:
  def greet(name = None):
    greetings = [
        "Hey there! I am Buddy, your assistant.",
        "Hello! I am Buddy let me know how can i help you?",
        "Namaskaar! Humahara subhnaam Buddy aapki seva me humesha uplabdh!!",
        "Hey! Buddy here, ready to assist!"
    ]

    if name:
      print(f"Hello {name}! I am Buddy. How can i help you?")
    else:
      print(random.choice(greetings))

# TIME & DATE

class DateTime:
  # Time
  def show_time():
    print("Current Time is:", datetime.datetime.now().strftime("%H:%M:%S"))

  # Date

  def show_date():
    print("Today's Date is:", datetime.date.today().strftime("%B %d,%Y"))

# REMINDER

class Reminder:
  def set_reminder():
    try:
      minutes = int(input("In how many minutes should i remind you?: "))
      message = input("What should i remind you about? ")
      print(f"Done! I remind you in {minutes} minutes.")
      time.sleep(minutes * 60)
      print(f"\n Reminder: {message}")
    except ValueError:
      print("Please enter a valid number of minutes!!")

# CALCULATOR

class Calculator:
  def open_calculator():
    print("Opeaning Calculator....")
    try:
      os.system("calc")
    except Exception as e:
      print(f"Unable to open calculator: {e}")

# NOTES

class Notes:
  # Taking Notes

  def take_note():
    note = input("Enter your note: ")
    with open("notes.txt", "a") as n:
      n.write(note + "\n")
    print("Your Notes saved successfully!!")

  # Reading Notes

  def read_notes():
    try:
      with open("notes.txt", "r") as n:
        notes = n.readlines()
      if notes:
        print("\n Your Notes")

        for i, n in enumerate(notes, 1):
          print(f"{i}. {n.strip()}")
      else:
        print("No Notes Yet!")
    except FileNotFoundError:
      print("No Notes Found! Try to Adding one first.")

# MEMORY

class Memory:
  # Remembering the person

  def remember_name(name):
    with open("memory.txt", "w") as m:
      m.write(name)
    print(f"GOt It! I will Remember Your Name, {name}.")

  # Reading That Name

  def get_name():
    try:
      with open("memory.txt", "r") as m:
        name = m.read().strip()
        if name.lower().startswith("my name is"):
          name = name.replace("my name is", "").strip().capitalize()
        return name
    except FileNotFoundError:
      return None

# Music

class Music:
  def play_music():
    song = input("Enter a song you want to enjoy: ")
    if not song.strip():
      print("Please enter a song name.")
      return
    print(f"Searching for your Song {song}")
    search_query = song.replace(' ','+')
    youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
    print(f"\n Click the link & Enjoy your Music")
    print(f"\n Link: {youtube_url}")

# SMART SEARCH

class SmartSearch:

  # Using a Generic Browser
  def __init__(self):
    self.headers = {"user-Agent": "Mozilla/5.0"}     # Here Mozilla used by websites through Headers to send the HTML Content Normally

  # Building the goggle search Url
  def fetch_html(self, query):
    encoded = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded}"
    res = requests.get(url, headers = self.headers)
    return res.text

  # Extracting Meaningful search result by (Title + Link) from HTML
  def extract_results(self, html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    results = []
    for g in soup.find_all("div", class_="tF2Cxc"):   # Here the class_="tF2Cxcc" extracting the exact result for questions and ignoring ads, menu, footer, etc.
      title = g.find("h3")
      link = g.find("a")
      if title and link:
        results.append((title.text, link["herf"]))
    return results

  # Searching for results in wikipedia with highest similarity of  question

  def fetch_wikipedia_page(self, query):
    try:

        # Encoding the query for URL
        encoded = urllib.parse.quote_plus(query)
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={encoded}&format=json"

        # Making the request
        req = urllib.request.Request(url, headers=self.headers)
        with urllib.request.urlopen(req, timeout=10) as res:
            data = json.loads(res.read().decode("utf-8"))
            search_results = data.get("query", {}).get("search", [])

            if not search_results:
                return None

            # Finding the result with the highest similarity to the query
            best_title = None
            highest_ratio = 0
            for result in search_results:
                title = result["title"]
                ratio = SequenceMatcher(None, query.lower(), title.lower()).ratio()
                if ratio > highest_ratio:
                    highest_ratio = ratio
                    best_title = title

            return best_title
    except Exception:
        return None

  # Fetching a short summary of question which getting asked

  def fetch_wikipedia_summary(self, title):

    if not title:
      return "Definition not found."

    try:
        encoded = urllib.parse.quote(title)

        # Wikipedia Url for fetching page summary
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}"

        # Make the request with headers to avoid being blocked
        req = urllib.request.Request(url, headers=self.headers)
        with urllib.request.urlopen(req, timeout=10) as res:

            # Parse the JSON response
            data = json.loads(res.read().decode("utf-8"))

            # Get the summary text; default to "Definition not found." if missing
            summary = data.get("extract", "Definition not found.")

            # Split into sentences
            summary_lines = summary.split(". ")

            # Return first 2-3 sentences joined together
            return ". ".join(summary_lines[:3]) + "."

    except Exception:
        return "Definition not found."

# Sumarize the search results and providing some extra links

# Find the best matching Wikipedia page for the query
  def summarize(self, query, results):
      page_title = self.fetch_wikipedia_page(query)
      definition = self.fetch_wikipedia_summary(page_title)
      print(f"\nSearch Summary for '{query.title()}':\n")

      # Wraping the long definitions for better readability in console
      wrapped_def = textwrap.fill(definition, width=100)
      print(f"1. Definition:\n   {wrapped_def}\n")

      wiki_link = (
          f"https://en.wikipedia.org/wiki/{urllib.parse.quote(page_title.replace(' ', '_'))}"
          if page_title else None
      )
      extra_links = [l for _, l in results if "wikipedia.org" not in l][:2]

      print("2. Links to Learn More:")
      if wiki_link:
          print(f"   Wikipedia: {wiki_link}")
      for i, link in enumerate(extra_links, 1):
          print(f"   {i}. {link}")


# Performing a smart search for the given query by fetching Wikipedia summary and extra links

  def search(self, query):
      # Checking if the user entered a query
      if not query:
          print("Please enter something to search.")
          return

      print(f"Searching for '{query}'...\n")

      try:
          # Fetching HTML content from Google search
          html_data = self.fetch_html(query)

          # Extracting links from the fetched HTML
          results = self.extract_results(html_data)

          # Summarizing the query by fetching Wikipedia summary and shows links
          self.summarize(query, results)

      except Exception as e:
          print(f"Error while searching: {e}")

# Help

class Help:
    def show_help():
        print("""
Available Commands:
- time : Show current time
- date : Show today's date
- remind : Set a reminder
- open calculator : Open system calculator
- hello : Greet Buddy
- help : Show this help
- exit : Exit Buddy
- note take : Save a note
- note read/list : Read saved notes
- play music : Play songs on YouTube
- my name is [name] : Tell Buddy your name
- who am i : Buddy recalls your name
- search [query] : Get smart search summary from Google & Wikipedia
""")

# Main Class to run all the programs

class BuddyAssistant:
    def __init__(self):
        self.user_name = Memory.get_name()
        Greeting.greet(self.user_name)
        self.search_engine = SmartSearch()

    def run(self):
        while True:
            command = input("\nEnter your command: ").lower()

            if command == "time":
                DateTime.show_time()
            elif command == "date":
                DateTime.show_date()
            elif command == "remind":
                Reminder.set_reminder()
            elif command == "open calculator":
                Calculator.open_calculator()
            elif command == "note take":
                Notes.take_note()
            elif command in ["note read", "note list"]:
                Notes.read_notes()
            elif command == "play music":
                Music.play_music()
            elif command.startswith("my name is"):
                name = command.replace("my name is", "").strip().capitalize()
                if name:
                    Memory.remember_name(name)
                    self.user_name = name
                else:
                    print("Please tell me your name properly.")
            elif command == "who am i":
                if self.user_name:
                    print(f"You are {self.user_name}. I remember you!")
                else:
                    print("I don't know yet. Tell me your name using 'my name is ...'")
            elif command.startswith("search"):
                query = command.replace("search", "").strip()
                self.search_engine.search(query)
            elif command == "hello":
                Greeting.greet()
            elif command == "help":
                Help.show_help()
            elif command == "exit":
                print("Bye bye! Have a great day!")
                break
            else:
                print("Sorry, I didn't understand that. Type 'help' to see all commands.")

# Running The Entire Program

if __name__ == "__main__":
    BuddyAssistant().run()

