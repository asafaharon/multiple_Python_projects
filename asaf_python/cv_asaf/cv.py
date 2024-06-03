import webbrowser
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Initialize the main window
window = tk.Tk()
window.title("Resume")
window.geometry("700x900")

# Configure the grid layout of the main window
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

# Create the main frame with padding for content
main_frame = tk.Frame(window, padx=20, pady=20)
main_frame.grid(sticky="nsew")

# Enable grid expansion in the main frame
main_frame.columnconfigure(1, weight=1)
for i in range(13):
    main_frame.rowconfigure(i, weight=1)

# Create dictionary for texts in English and Hebrew
texts = {
    "en": {
        "full_name": "Full Name:",
        "email": "Email:",
        "phone_number": "Phone Number:",
        "skills": "Skills:",
        "soft_skills": "Soft Skills:",
        "education": "Education:",
        "linkedin_profile": "LinkedIn Profile",
        "calculator": "Calculator",
        "backgammon": "Backgammon",
        "checkers": "Checkers",
        "calendar": "Calendar",
        "ping_pong": "Ping Pong",
        "snake": "Snake",
        "grade_sheet": "Grade Sheet",
        "painting": "Painting",
        "anima": "Anima",
        "tic_tac_toe": "Tic Tac Toe",
        "maze_game": "Maze Game",
        "skills_text": "Programming Languages: Java, Python, JavaScript, SQL\nWeb Development: HTML, CSS, server-side and client-side development\nOperating Systems: Linux, Windows\nTools and Technologies: Git, Docker, Continuous Integration/Continuous Deployment (CI/CD), Relational and NoSQL databases\nCloud Platforms: Basic knowledge in AWS, Azure, or Google Cloud Platform\n",
        "soft_skills_text": "Problem Solving: Strong analytical thinking and ability to tackle complex problems creatively.\nTeamwork: Experience working in multi-disciplinary teams, contributing to a positive and collaborative environment.\nCommunication: Ability to articulate ideas clearly and accurately to both technical and non-technical audiences.\n",
        "education_text": "Open University\nBachelor’s Degree in Computer Science (in progress, expected to graduate in 2024)\nOnline Courses\nAdditional courses in SQL, Python, JavaScript, Linux.\nProficient in Microsoft Office and various technological tools.\n",
        "switch_language": "Switch to Hebrew"
    },
    "he": {
        "full_name": "שם מלא:",
        "email": "אימייל:",
        "phone_number": "מספר טלפון:",
        "skills": "מיומנויות:",
        "soft_skills": "מיומנויות רכות:",
        "education": "השכלה:",
        "linkedin_profile": "פרופיל LinkedIn",
        "calculator": "מחשבון",
        "backgammon": "שש-בש",
        "checkers": "דמקה",
        "calendar": "לוח שנה",
        "ping_pong": "פינג פונג",
        "snake": "נחש",
        "grade_sheet": "דף ציונים",
        "painting": "ציור",
        "anima": "אנימציה",
        "tic_tac_toe": "איקס-עיגול",
        "maze_game": "משחק המבוך",
        "skills_text": "שפות תכנות: Java, Python, JavaScript, SQL\nפיתוח אתרים: HTML, CSS, פיתוח צד שרת וצד לקוח\nמערכות הפעלה: Linux, Windows\nכלים וטכנולוגיות: Git, Docker, אינטגרציה רציפה/פריסה רציפה (CI/CD), מסדי נתונים רלציוניים ולא רלציוניים\nפלטפורמות ענן: ידע בסיסי ב-AWS, Azure או Google Cloud Platform\n",
        "soft_skills_text": "פתרון בעיות: חשיבה אנליטית חזקה ויכולת להתמודד עם בעיות מורכבות בצורה יצירתית.\nעבודת צוות: ניסיון בעבודה בצוותים רב-תחומיים, תורם לסביבה חיובית ומשתפת.\nתקשורת: יכולת לבטא רעיונות בצורה ברורה ומדויקת לקהלים טכניים ולא טכניים כאחד.\n",
        "education_text": "האוניברסיטה הפתוחה\nתואר ראשון במדעי המחשב (במהלך הלימודים, צפוי לסיים ב-2024)\nקורסים מקוונים\nקורסים נוספים ב-SQL, Python, JavaScript, Linux.\nבקיא ב-Microsoft Office וכלים טכנולוגיים שונים.\n",
        "switch_language": "החלף לאנגלית"
    }
}

# Set the current language to English
current_language = "en"

# Function to switch between languages
def switch_language():
    global current_language
    current_language = "he" if current_language == "en" else "en"
    update_texts()

# Function to update all texts in the interface
def update_texts():
    lang = texts[current_language]
    name_label.config(text=lang["full_name"])
    email_label.config(text=lang["email"])
    phone_label.config(text=lang["phone_number"])
    skills_label.config(text=lang["skills"])
    soft_skills_label.config(text=lang["soft_skills"])
    education_label.config(text=lang["education"])
    linkedin_button.config(text=lang["linkedin_profile"])
    calculator_button.config(text=lang["calculator"])
    backgammon_button.config(text=lang["backgammon"])
    checkers_button.config(text=lang["checkers"])
    calendar_button.config(text=lang["calendar"])
    ping_pong_button.config(text=lang["ping_pong"])
    snake_button.config(text=lang["snake"])
    grade_sheet_button.config(text=lang["grade_sheet"])
    painting_button.config(text=lang["painting"])
    anima_button.config(text=lang["anima"])
    tic_tac_toe_button.config(text=lang["tic_tac_toe"])
    maze_game_button.config(text=lang["maze_game"])
    switch_button.config(text=lang["switch_language"])

    skills_text.delete(1.0, tk.END)
    skills_text.insert(tk.INSERT, lang["skills_text"])
    soft_skills_text.delete(1.0, tk.END)
    soft_skills_text.insert(tk.INSERT, lang["soft_skills_text"])
    education_text.delete(1.0, tk.END)
    education_text.insert(tk.INSERT, lang["education_text"])

# Function to create labeled entry with consistent styling
def create_labeled_entry(parent, label, row, default_value=""):
    entry_label = tk.Label(parent, text=label, font=("Arial", 12, "bold"))
    entry_label.grid(row=row, column=0, sticky="w", pady=5)
    entry_var = tk.StringVar(value=default_value)
    entry = tk.Entry(parent, textvariable=entry_var, font=("Arial", 12), width=40)
    entry.grid(row=row, column=1, sticky="ew", pady=5)
    return entry_label, entry_var

# Function to create scrolled text area with consistent styling
def create_scrolled_text(parent, label, row, default_text=""):
    text_label = tk.Label(parent, text=label, font=("Arial", 12, "bold"))
    text_label.grid(row=row, column=0, sticky="w", pady=(10, 2))
    text_area = scrolledtext.ScrolledText(parent, height=5, width=40, font=("Arial", 12))
    text_area.grid(row=row, column=1, sticky="ew", pady=2)
    text_area.insert(tk.INSERT, default_text)
    return text_label, text_area

# Create entry fields and scrolled text areas for user information
name_label, name_var = create_labeled_entry(main_frame, texts["en"]["full_name"], 0, "Asaf Aharon")
email_label, email_var = create_labeled_entry(main_frame, texts["en"]["email"], 1, "asafasaf16@gmail.com")
phone_label, phone_var = create_labeled_entry(main_frame, texts["en"]["phone_number"], 2, "0547989141")

skills_label, skills_text = create_scrolled_text(main_frame, texts["en"]["skills"], 3, texts["en"]["skills_text"])
soft_skills_label, soft_skills_text = create_scrolled_text(main_frame, texts["en"]["soft_skills"], 4, texts["en"]["soft_skills_text"])
education_label, education_text = create_scrolled_text(main_frame, texts["en"]["education"], 5, texts["en"]["education_text"])

# Function to open LinkedIn profile
def open_linkedin():
    webbrowser.open('https://www.linkedin.com/in/asaf-aharon-02a194237?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3ByyLU7XooSYG3OZ9HYgsgEg%3D%3D')

# Function to create and place a LinkedIn link button
def create_linkedin_button(parent, label, row, col):
    btn = tk.Button(parent, text=label, command=open_linkedin, font=("Arial", 12), padx=10, pady=5, bg="lightblue")
    btn.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
    return btn

# Place the LinkedIn button in the main frame
linkedin_button = create_linkedin_button(main_frame, texts["en"]["linkedin_profile"], 6, 0)

# Functions to open various applications
def open_anima_app():
    import anima

def open_paint_app():
    import painting

def open_grade_app():
    import grade_sheet
    grade_sheet.show_resume()

def open_snake_app():
    import snake
    snake.main()

def open_ping_pong_app():
    import ping_pong

def open_calculater_app():
    import calculator

def open_calendar_app():
    import calandertry

def open_checkers_app():
    import Checkers_main

def open_backgammon_app():
    import main_Backgammon
    main_Backgammon.initialize()
    main_Backgammon.play_game()

def open_tic_tac_toe_app():
    import tic_tac
    tic_tac.open_tic_tac_app()

def open_maze_app():
    import maze
    maze.main()

# Function to create and place a button
def create_app_button(parent, label, command, row, col):
    btn = tk.Button(parent, text=label, command=command, font=("Arial", 12), padx=10, pady=5, bg="lightgrey")
    btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
    return btn

# Create buttons for applications
calculator_button = create_app_button(main_frame, texts["en"]["calculator"], open_calculater_app, 7, 0)
backgammon_button = create_app_button(main_frame, texts["en"]["backgammon"], open_backgammon_app, 7, 1)
checkers_button = create_app_button(main_frame, texts["en"]["checkers"], open_checkers_app, 8, 0)
calendar_button = create_app_button(main_frame, texts["en"]["calendar"], open_calendar_app, 8, 1)
ping_pong_button = create_app_button(main_frame, texts["en"]["ping_pong"], open_ping_pong_app, 9, 0)
snake_button = create_app_button(main_frame, texts["en"]["snake"], open_snake_app, 9, 1)
grade_sheet_button = create_app_button(main_frame, texts["en"]["grade_sheet"], open_grade_app, 10, 0)
painting_button = create_app_button(main_frame, texts["en"]["painting"], open_paint_app, 10, 1)
anima_button = create_app_button(main_frame, texts["en"]["anima"], open_anima_app, 11, 0)
tic_tac_toe_button = create_app_button(main_frame, texts["en"]["tic_tac_toe"], open_tic_tac_toe_app, 11, 1)
maze_game_button = create_app_button(main_frame, texts["en"]["maze_game"], open_maze_app, 12, 0)

# Create language switch button
switch_button = tk.Button(main_frame, text=texts["en"]["switch_language"], command=switch_language, font=("Arial", 12), padx=10, pady=5, bg="lightgreen")
switch_button.grid(row=13, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Function to update the language switch button text
def update_switch_button():
    switch_button.config(text=texts[current_language]["switch_language"])

# Update texts and switch button text initially
update_texts()
update_switch_button()

# Main loop
window.mainloop()
