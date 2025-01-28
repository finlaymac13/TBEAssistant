import webbrowser
import datetime
import random
import os
import httpx
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify Integration Setup
SPOTIFY_CLIENT_ID = "30251b81b42d4a02b7a8663085554288"
SPOTIFY_CLIENT_SECRET = "2f4fea3f20f44d97a196b6ae7509c9bd"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"

def setup_spotify():
    """Set up Spotify client."""
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope="user-read-playback-state user-modify-playback-state user-read-currently-playing"
        ))
        return sp
    except Exception as e:
        print(f"Error setting up Spotify: {e}")
        return None

def play_song(sp, song_name):
    """Play a song by name (optionally with artist) on Spotify."""
    try:
        results = sp.search(q=song_name, type="track", limit=5)  # Fetch more results
        if results["tracks"]["items"]:
            print("Search results:")
            for idx, track in enumerate(results["tracks"]["items"], 1):
                print(f"{idx}. {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")

            # Let the user select the correct song
            choice = int(input("Select the correct song by number: ")) - 1
            if 0 <= choice < len(results["tracks"]["items"]):
                selected_track = results["tracks"]["items"][choice]
                sp.start_playback(uris=[selected_track["uri"]])
                print(f"Playing: {selected_track['name']} by {', '.join(artist['name'] for artist in selected_track['artists'])}")
            else:
                print("Invalid selection.")
        else:
            print("No matching songs found.")
    except Exception as e:
        print(f"Error playing song: {e}")

def pause_song(sp):
    """Pause the current song."""
    try:
        sp.pause_playback()
        print("Playback paused.")
    except Exception as e:
        print(f"Error pausing playback: {e}")

def resume_song(sp):
    """Resume the current song."""
    try:
        sp.start_playback()
        print("Playback resumed.")
    except Exception as e:
        print(f"Error resuming playback: {e}")

def show_current_song(sp):
    """Display the current song playing on Spotify."""
    try:
        current = sp.current_playback()
        if current and current["is_playing"]:
            track = current["item"]
            print(f"Currently playing: {track['name']} by {track['artists'][0]['name']}")
        else:
            print("No song is currently playing.")
    except Exception as e:
        print(f"Error fetching current song: {e}")

# Other functions for File Management, To-Do Lists, Web Scraping, and Main Program are above.

# File Management Functions
def display_files(path="."):
    """Display files and folders in the specified path."""
    try:
        entries = os.listdir(path)
        print(f"Contents of {os.path.abspath(path)}:")
        for entry in entries:
            print(f"- {entry}")
    except Exception as e:
        print(f"Error: {e}")

def create_new_file(file_name):
    """Create a new file."""
    try:
        with open(file_name, "w") as file:
            file.write("")
        print(f"File '{file_name}' created successfully.")
    except Exception as e:
        print(f"Error: {e}")

def remove_file(file_name):
    """Remove an existing file."""
    try:
        os.remove(file_name)
        print(f"File '{file_name}' removed successfully.")
    except Exception as e:
        print(f"Error: {e}")

def edit_file(file_name):
    """Edit an existing file in a nano-like interface."""
    try:
        if not os.path.exists(file_name):
            print(f"File '{file_name}' does not exist.")
            return

        print(f"Editing '{file_name}'. Type your content below. Type 'SAVE' on a new line to save and exit.")
        content = []
        while True:
            line = input(" > ")
            if line.strip().upper() == "SAVE":
                break
            content.append(line)

        with open(file_name, "w") as file:
            file.write("\n".join(content))

        print(f"File '{file_name}' saved successfully.")
    except Exception as e:
        print(f"Error: {e}")

# To-Do List Management Functions
def add_todo_item(todo_list, title, description, due_date, location):
    """Add a new item to the to-do list."""
    todo_list.append({
        "title": title,
        "description": description,
        "due_date": due_date,
        "location": location
    })
    print(f"To-Do item '{title}' added successfully.")

def remove_todo_item(todo_list, title):
    """Remove an item from the to-do list by title."""
    for item in todo_list:
        if item["title"] == title:
            todo_list.remove(item)
            print(f"To-Do item '{title}' removed successfully.")
            return
    print(f"To-Do item '{title}' not found.")

def display_todo_list(todo_list):
    """Display all items in the to-do list."""
    if not todo_list:
        print("No items in the to-do list.")
    else:
        for item in todo_list:
            print(f"- Title: {item['title']}")
            print(f"  Description: {item['description']}")
            print(f"  Due Date: {item['due_date']}")
            print(f"  Location: {item['location']}")
            print("-------------------------")

# Web Scraper Function
def scrape_website():
    """Prompt a URL and return its text contents in a formatted way."""
    url = input("Enter the URL to scrape: ").strip()
    try:
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract text content and format it
            text = soup.get_text(separator="\n", strip=True)
            print("\n[Scraped Content]")
            print(text[:1000])  # Display the first 1000 characters for readability
            print("\n[End of Preview - Full content truncated for brevity]")

    except httpx.RequestError as e:
        print(f"Error: Unable to scrape the website. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
# Main Program
def display_help():
    """Display available commands."""
    print("\n[Available Commands]")

    print("[Open Commands]")
    print("  google       - Open Google")
    print("  youtube      - Open YouTube")
    print("  bbc news     - Open BBC News")
    print("  bbc sport    - Open BBC Sport")
    print("  hibs         - Open Hibs on BBC Sport")
    print("  bbc weather  - Open BBC Weather for locations:")
    print("  chess        - Open Chess.com")
    print("  chess start  - Start a 10-min unrated game on Chess.com")

    print("[Spotify Commands]")
    print("  play song <song name> - Play a song by name")
    print("  pause         - Pause the current song")
    print("  resume        - Resume the current song")
    print("  current song  - Display the current song playing")

    print("[Joke Commands]")
    print("  joke         - Get a random joke or knock-knock joke")

    print("[File Commands]")
    print("  create file <filename> - Create a new file")
    print("  delete file <filename> - Delete a file")
    print("  edit file <filename>   - Edit an existing file")
    print("  display files          - Show all files in the current directory")

    print("[Datetime Commands]")
    print("  time         - Get the current time")
    print("  date         - Get today's date")

    print("[To-Do List Commands]")
    print("  todo add     - Add a new to-do item")
    print("  todo remove <title> - Remove a to-do item by title")
    print("  todo display - Show all to-do items")

    print("[Web Scraping Command]")
    print("  scrape       - Scrape and display text content from a website")

    print("[LLM Commands]")
    print("  ask gpt <question> - Ask the language model a question <INACTIVE>")


    print("[Other Commands]")
    print("  help         - Show this help menu")
    print("  exit         - Exit the assistant")

def handle_open(user_input):
    if "google" in user_input:
        print("Opening Google...")
        webbrowser.open("https://www.google.com")
    elif "youtube" in user_input:
        print("Opening YouTube...")
        webbrowser.open("https://www.youtube.com")
    elif "bbc news" in user_input:
        print("Opening BBC News...")
        webbrowser.open("https://www.bbc.co.uk/news")
    elif "bbc sport" in user_input:
        print("Opening BBC Sport...")
        webbrowser.open("https://www.bbc.co.uk/sport")
    elif "hibs" in user_input:
        print("Opening Hibs on BBC Sport...")
        webbrowser.open("https://www.bbc.co.uk/sport/football/teams/hibernian")
    elif "chess start game" in user_input:
        print("Starting a 10-minute unrated game on Chess.com...")
        webbrowser.open("https://www.chess.com/play/online?time=10")
    elif "chess" in user_input:
        print("Opening Chess.com...")
        webbrowser.open("https://www.chess.com")
    else:
        print("Unknown website command.")

def handle_jokes():
    jokes = [
        "What do you call fake spaghetti? An impasta!",
        "Why don’t skeletons fight each other? They don’t have the guts.",
        "I went to the beekeeper and got 10 bees, when I opened the bees there were 11! I asked the beekeeper why I got an extra bee? He replied 'That's a Free-bee!' ",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What do you call cheese that isn’t yours? Nacho cheese!",
        "What did the grape do when he got stepped on? Nothing but let out a little wine!",
        "Why did the bicycle fall over? Because it was two tired!",
        "What do you call a fish with no eyes? Fsh!",
        "How does a penguin build its house? Igloos it together!",
        "Why did the math book look sad? Because it had too many problems!"
    ]

    knock_knock_jokes = [
        ("Atch", "Bless you!"),
        ("Cow says", "No, a cow says moooo!"),
        ("Boo", "Don’t cry, it’s just a joke!"),
        ("Lettuce", "Lettuce in, it’s freezing out here!"),
        ("Harry", "Harry up and answer the door!")
    ]
    if random.choice([True, False]):
        # Display a random joke
        print(random.choice(jokes))
    else:
        # Display a knock-knock joke
        joke = random.choice(knock_knock_jokes)
        print("Knock, knock!")
        response = input(" > Who's there? ").strip().lower()
        print(f"{joke[0]}.")
        response = input(f" > {joke[0]} who? ").strip().lower()
        print(joke[1])

def main():
    todo_list = []
    sp = setup_spotify()
    print("Hello! I am your virtual assistant. How can I assist you today?")
    print("Type 'help' to see available commands.")

    while True:
        user_input = input(" > Enter your command: ").strip().lower()

        if user_input.startswith("open"):
            handle_open(user_input)

        elif user_input == "joke":
            handle_jokes()

        elif user_input.startswith("create file"):
            file_name = user_input.replace("create file ", "", 1).strip()
            if file_name:
                create_new_file(file_name)
            else:
                print("Please specify a file name.")

        elif user_input.startswith("delete file"):
            file_name = user_input.replace("delete file ", "", 1).strip()
            if file_name:
                remove_file(file_name)
            else:
                print("Please specify a file name.")

        elif user_input.startswith("edit file"):
            file_name = user_input.replace("edit file ", "", 1).strip()
            if file_name:
                edit_file(file_name)
            else:
                print("Please specify a file name.")

        elif user_input == "display files":
            display_files()

        elif user_input == "time":
            now = datetime.datetime.now()
            print(f"Current Time: {now.strftime('%H:%M:%S')}")

        elif user_input == "date":
            today = datetime.date.today()
            print(f"Today's Date: {today.strftime('%B %d, %Y')}")

        elif user_input.startswith("todo add"):
            print("Enter details for the new to-do item:")
            title = input("Title: ").strip()
            description = input("Description: ").strip()
            due_date = input("Due Date (YYYY-MM-DD): ").strip()
            location = input("Location: ").strip()
            add_todo_item(todo_list, title, description, due_date, location)

        elif user_input.startswith("todo remove"):
            title = user_input.replace("todo remove ", "", 1).strip()
            if title:
                remove_todo_item(todo_list, title)
            else:
                print("Please specify the title of the to-do item to remove.")

        elif user_input == "todo display":
            display_todo_list(todo_list)

        elif user_input == "scrape":
            scrape_website()
        
        elif user_input.startswith("play song"):
            if sp:
                song_name = user_input.replace("play song ", "", 1).strip()
                play_song(sp, song_name)
            else:
                print("Spotify is not set up. Please check your credentials.")

        elif user_input == "pause":
            if sp:
                pause_song(sp)
            else:
                print("Spotify is not set up. Please check your credentials.")

        elif user_input == "resume":
            if sp:
                resume_song(sp)
            else:
                print("Spotify is not set up. Please check your credentials.")

        elif user_input == "current song":
            if sp:
                show_current_song(sp)
            else:
                print("Spotify is not set up. Please check your credentials.")

        elif user_input == "help":
            display_help()

        elif user_input in ("exit", "quit"):
            print("Goodbye! Have a great day!")
            break

        else:
            print("Unknown command. Type 'help' to see the list of available commands.")

if __name__ == "__main__":
    main()

