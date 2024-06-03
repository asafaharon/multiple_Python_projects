import tkinter as tk
from tkinter import simpledialog, messagebox


characters = {
    "Naruto": {
    "Naruto": "Naruto Uzumaki is a young ninja who seeks recognition from his peers and dreams of becoming the Hokage.",
    "Sasuke": "Sasuke Uchiha is one of the last surviving members of Konohagakure's Uchiha clan.",
    "Sakura": "Sakura Haruno is a kunoichi of Konohagakure and a member of Team 7.",
    "Kakashi": "Kakashi Hatake is the leader of Team 7 and the sixth Hokage.",
    "Asuma": "Asuma Sarutobi, Team 10's leader and son of the Third Hokage.",
    "Kurenai": "Kurenai Yuhi, Team 8's leader and a genjutsu specialist.",
    "Yamato": "Yamato, an ANBU member who leads Team 7 in Kakashi's absence.",
    "Minato": "Minato Namikaze, the Fourth Hokage and Naruto's father.",
    "Kushina": "Kushina Uzumaki, Naruto's mother and former host of the Nine-Tails.",
    "Sarutobi": "Hiruzen Sarutobi, the Third Hokage and mentor to the Sannin.",
    "Danzo": "Danzo Shimura, leader of the Root and a political rival to the Hokage.",
    "Pain": "Pain, the leader of Akatsuki and a former student of Jiraiya.",
    "Konan": "Konan, a member of Akatsuki and a paper-jutsu specialist.",
    "Hidan": "Hidan, an immortal member of Akatsuki who worships Jashin.",
    "Kakuzu": "Kakuzu, an Akatsuki member who stitches himself with threads.",
    "Sai": "Sai, a member of Root and Team 7 during Sasuke's absence.",
    "Killer B": "Killer B, the Eight-Tails Jinchuriki and a rapper.",
    "Madara": "Madara Uchiha, co-founder of Konoha and a major antagonist.",
    "Obito": "Obito Uchiha, a former Team Minato member and major antagonist.",
    "Hinata": "Hinata Hyuga is a member of Konohagakure's Hyuga clan and Naruto's love interest.",
    "Shikamaru": "Shikamaru Nara is a member of Konohagakure's Nara clan and is known for his strategic mind.",
    "Rock Lee": "Rock Lee is a ninja who lacks the ability to use ninjutsu or genjutsu, but excels in taijutsu.",
    "Gaara": "Gaara is the Kazekage of Sunagakure and has the One-Tailed Beast sealed within him.",
    "Jiraiya": "Jiraiya is one of Konohagakure's legendary Sannin and was Naruto's mentor.",
    "Tsunade": "Tsunade is one of Konohagakure's legendary Sannin and the fifth Hokage.",
    "Orochimaru": "Orochimaru is one of Konohagakure's legendary Sannin and a major antagonist.",
    "Minato": "Minato Namikaze was the fourth Hokage and Naruto's father.",
    "Kiba": "Kiba Inuzuka is a member of Konohagakure's Inuzuka clan and a member of Team 8.",
    "Neji": "Neji Hyuga was a member of Konohagakure's Hyuga clan and a member of Team Guy.",
    "Ino": "Ino Yamanaka is a member of Konohagakure's Yamanaka clan and a member of Team 10.",
    "Choji": "Choji Akimichi is a member of Konohagakure's Akimichi clan and a member of Team 10.",
    "Itachi": "Itachi Uchiha, Sasuke's older brother and a member of Akatsuki." },

    "One Piece": {
        "Luffy": "Monkey D. Luffy is the main protagonist, whose goal is to become the Pirate King.",
        "Zoro": "Roronoa Zoro, the swordsman of the Straw Hat Pirates and Luffy's right-hand man.",
        "Nami": "Nami, the navigator of the Straw Hat Pirates and an expert cartographer.",
        "Usopp": "Usopp, the sniper of the Straw Hat Pirates and a talented inventor.",
        "Sanji": "Sanji, the chef of the Straw Hat Pirates known for his powerful leg-based fighting style.",
        "Chopper": "Tony Tony Chopper, the doctor of the Straw Hat Pirates, who can transform into different forms.",
        "Robin": "Nico Robin, the archaeologist of the crew, with the ability to replicate her body parts.",
        "Franky": "Franky, the shipwright of the Straw Hat Pirates, known for his cyborg body.",
        "Brook": "Brook, the musician of the Straw Hat Pirates, a living skeleton brought back to life by the Revive-Revive Fruit.",
        "Jinbei": "Jinbei, a former Warlord of the Sea, a fish-man and a helmsman of the Straw Hat Pirates."
    },
    "Dragon Ball": {
        "Goku": "Son Goku, the main protagonist, known for his cheerful personality and love of fighting.",
        "Vegeta": "Prince Vegeta, the prince of the fallen Saiyan race and a key fighter.",
        "Frieza": "Frieza, a powerful tyrant who rules over the Universe 7.",
        "Piccolo": "Piccolo, a wise and strategic fighter, and a mentor to Gohan.",
        "Gohan": "Son Gohan, Goku's eldest son, known for his intellectual and fighting prowess.",
        "Krillin": "Krillin, Goku's best friend, known for his courage and determination.",
        "Bulma": "Bulma, a brilliant scientist and a close friend of Goku.",
        "Trunks": "Trunks, the son of Vegeta and Bulma, known for traveling back in time.",
        "Cell": "Cell, a bio-engineered android seeking to achieve his perfect form.",
        "Majin Buu": "Majin Buu, a powerful and ancient creature capable of destruction.",
        "Beerus": "Beerus, the God of Destruction of Universe 7.",
        "Whis": "Whis, the attendant to Beerus, known for his wisdom and strength.",
        "Android 18": "Android 18, a powerful android and Krillin's wife.",
        "Android 17": "Android 17, Android 18's twin brother and a park ranger.",
        "Tien": "Tien Shinhan, a martial artist with a third eye, known for his Tri-Beam technique.",
        "Yamcha": "Yamcha, a former desert bandit turned hero and baseball player.",
        "Chiaotzu": "Chiaotzu, Tien's best friend, known for his psychic abilities.",
        "Videl": "Videl, Gohan's wife and daughter of Mr. Satan.",
        "Goten": "Son Goten, Goku's youngest son, who resembles his father.",
        "Roshi": "Master Roshi, the Turtle Hermit and Goku's first martial arts master.",
        "Bardock": "Bardock, Goku's father, a Saiyan warrior with a sense of justice.",
        "Broly": "Broly, the Legendary Super Saiyan with immense power.",
        "Jiren": "Jiren, a member of the Pride Troopers and a formidable fighter in Universe 11.",
        "Zamasu": "Zamasu, a rogue Kai who despises mortals."
    },
    "Attack on Titan": {
        "Eren": "Eren Yeager, the main protagonist who vows to exterminate the Titans.",
        "Mikasa": "Mikasa Ackerman, Eren's adoptive sister and a skilled fighter.",
        "Armin": "Armin Arlert, a strategic mind and one of Eren's closest friends.",
        "Levi": "Levi Ackerman, a captain in the Survey Corps known for his extraordinary skill.",
        "Historia": "Historia Reiss, a member of the Survey Corps and the true heir to the throne.",
        "Jean": "Jean Kirstein, a member of the Survey Corps known for his leadership skills.",
        "Sasha": "Sasha Blouse, a member of the Survey Corps known for her marksmanship and love of food.",
        "Connie": "Connie Springer, a member of the Survey Corps known for his agility.",
        "Reiner": "Reiner Braun, a member of the Survey Corps and the Armored Titan.",
        "Annie": "Annie Leonhart, a member of the Military Police Brigade and the Female Titan.",
        "Bertholdt": "Bertholdt Hoover, a member of the Survey Corps and the Colossal Titan.",
        "Erwin": "Erwin Smith, the former commander of the Survey Corps, known for his strategic mind.",
        "Hange": "Hange Zoë, a former Squad Leader and later Commander of the Survey Corps, known for Titan research.",
        "Ymir": "Ymir, a member of the Survey Corps and a Titan shifter.",
        "Zeke": "Zeke Yeager, the Beast Titan and Eren's half-brother.",
        "Marco": "Marco Bott, a member of the 104th Training Corps who was close to Jean.",
        "Gabi": "Gabi Braun, a Warrior candidate from Marley and Reiner's cousin.",
        "Falco": "Falco Grice, a Warrior candidate from Marley who befriends Gabi."
    },
    "My Hero Academia": {
        "Deku": "Izuku Midoriya, a boy born without superpowers but dreams of becoming a hero.",
        "All Might": "All Might, the former No. 1 Pro Hero and Deku's mentor.",
        "Bakugo": "Katsuki Bakugo, Deku's childhood friend and rival.",
        "Todoroki": "Shoto Todoroki, a student known for his ice and fire powers.",
        "Uraraka": "Ochaco Uraraka, a student with the power to manipulate gravity.",
        "Iida": "Tenya Iida, the class representative known for his super speed.",
        "Kirishima": "Eijiro Kirishima, known for his hardening ability.",
        "Aizawa": "Shota Aizawa, the class's homeroom teacher who can erase quirks.",
        "Tsuyu": "Tsuyu Asui, a student with frog-like abilities.",
        "Momo": "Momo Yaoyorozu, a student who can create objects from her body.",
        "Tokoyami": "Fumikage Tokoyami, a student who controls a shadow beast.",
        "Jiro": "Kyoka Jiro, a student with sound-related abilities.",
        "Kaminari": "Denki Kaminari, a student who can control electricity.",
        "Mineta": "Minoru Mineta, a student with sticky spheres.",
        "Endeavor": "Enji Todoroki, the current No. 1 Pro Hero and Shoto's father.",
        "Stain": "Stain, a villain who believes in purging fake heroes.",
        "Tomura": "Tomura Shigaraki, the leader of the League of Villains.",
        "Dabi": "Dabi, a member of the League of Villains with fire abilities.",
        "Hawks": "Hawks, the No. 2 Pro Hero known for his winged flight.",
        "Mirio": "Mirio Togata, a senior student known as 'Lemillion'.",
        "Tamaki": "Tamaki Amajiki, a senior student known as 'Suneater'.",
        "Nejire": "Nejire Hado, a senior student known as 'Nejire-chan'."
    }
}

# Function to display character details in a pop-up message box
def show_details(character):
    series = series_var.get()  # Get selected series
    character = character_list.get(tk.ANCHOR)  # Get selected character
    if not character:  # Ensure a character is selected
        messagebox.showinfo("Error", "Please select a character.")
        return
    details = characters[series].get(character, "Character not found.")  # Fetch character details
    messagebox.showinfo(character, details)  # Show character details in a pop-up

# Function to update the character list based on the search query
def update_character_list(search_query=""):
    series = series_var.get()  # Get selected series
    character_list.delete(0, tk.END)  # Clear existing list
    for character in characters[series]:  # Populate list with characters that match the search query
        if search_query.lower() in character.lower():
            character_list.insert(tk.END, character)

# Function to search for a character
def search_character():
    search_query = simpledialog.askstring("Search", "Enter character name:")
    if search_query:  # If a search query was entered, update the list with the search results
        update_character_list(search_query)

# Add character to favorites
def add_to_favorites():
    character = character_list.get(tk.ANCHOR)  # Get selected character
    if not character:  # Ensure a character is selected
        messagebox.showinfo("Error", "Please select a character.")
        return
    favorites.append(character)  # Add character to favorites list
    messagebox.showinfo("Favorites", f"Added {character} to favorites.")

# Show favorites in a message box
def show_favorites():
    if not favorites:  # Check if favorites list is empty
        messagebox.showinfo("Favorites", "No favorites added.")
        return
    favs = '\n'.join(favorites)  # Join favorites into a string to display
    messagebox.showinfo("Favorites", f"Your Favorites:\n{favs}")

favorites = []  # Initialize an empty list for favorites

# Set up the main window
root = tk.Tk()
root.title("Anime Characters")

# Layout setup
top_frame = tk.Frame(root)
top_frame.pack()
bottom_frame = tk.Frame(root)
bottom_frame.pack()

# Dropdown menu.txt for series selection
series_var = tk.StringVar(root)
series_var.set("Naruto")  # Default series
series_option_menu = tk.OptionMenu(top_frame, series_var, *characters.keys(), command=lambda _: update_character_list())
series_option_menu.pack(side=tk.LEFT)

# Search button
search_button = tk.Button(top_frame, text="Search", command=search_character)
search_button.pack(side=tk.RIGHT)

# Favorites button
favorites_button = tk.Button(bottom_frame, text="Add to Favorites", command=add_to_favorites)
favorites_button.pack(side=tk.LEFT)

# Show favorites button
show_favs_button = tk.Button(bottom_frame, text="Show Favorites", command=show_favorites)
show_favs_button.pack(side=tk.RIGHT)

# Character selection listbox
character_label = tk.Label(root, text="Select a character:")
character_label.pack()
character_list = tk.Listbox(root)
character_list.pack()

# Details button
details_button = tk.Button(root, text="Show Details", command=lambda: show_details(character_list.get(tk.ANCHOR)))
details_button.pack()

update_character_list()  # Initialize character list for the default series

# Start the GUI event loop
root.mainloop()
