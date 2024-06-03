import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import calendar
import datetime


# Main class for the Calendar application
class CalendarApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calendar with Events")  # Window title
        self.geometry("600x650")  # Window size

        # Initialize current date, year, and month
        self.current_date = datetime.datetime.now()
        self.current_year = self.current_date.year
        self.current_month = self.current_date.month

        # Dictionary to store events, where key is a tuple of (year, month, day)
        self.events = {}

        # Frame for navigation controls
        self.controls_frame = tk.Frame(self)
        self.controls_frame.pack(pady=10)

        # Navigation buttons
        self.prev_year_button = tk.Button(self.controls_frame, text="<<", command=self.prev_year)
        self.prev_year_button.grid(row=0, column=0, padx=5)

        self.prev_month_button = tk.Button(self.controls_frame, text="<", command=self.prev_month)
        self.prev_month_button.grid(row=0, column=1, padx=5)

        self.today_button = tk.Button(self.controls_frame, text="Today", command=self.go_to_today)
        self.today_button.grid(row=0, column=2, padx=5)

        self.month_year_label = tk.Label(self.controls_frame, font=("Arial", 16))
        self.month_year_label.grid(row=0, column=3, padx=5)

        self.next_month_button = tk.Button(self.controls_frame, text=">", command=self.next_month)
        self.next_month_button.grid(row=0, column=4, padx=5)

        self.next_year_button = tk.Button(self.controls_frame, text=">>", command=self.next_year)
        self.next_year_button.grid(row=0, column=5, padx=5)

        # Frame for the calendar display
        self.calendar_frame = tk.Frame(self)
        self.calendar_frame.pack(pady=20)

        # Buttons for managing events
        self.add_event_button = tk.Button(self, text="Add Event", command=self.add_event)
        self.add_event_button.pack(side=tk.LEFT, padx=10)

        self.show_events_button = tk.Button(self, text="Show All Events", command=self.show_all_events)
        self.show_events_button.pack(side=tk.RIGHT, padx=10)

        # Updates and displays the calendar
        self.update_calendar()

    def update_calendar(self):
        # Clears the current calendar display before updating
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # Updates the month and year label
        self.month_year_label.config(text=f"{calendar.month_name[self.current_month]} {self.current_year}")

        # Display day labels (Sun, Mon, etc.)
        day_labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for col, day in enumerate(day_labels):
            tk.Label(self.calendar_frame, text=day, width=10, height=2, font=("Arial", 10, "bold")).grid(row=0,
                                                                                                         column=col)

        # Generate and display calendar days
        first_day_of_month = datetime.date(self.current_year, self.current_month, 1)
        cal = calendar.monthcalendar(self.current_year, self.current_month)
        for row, week in enumerate(cal, start=1):
            for col, day in enumerate(week):
                if day == 0:  # Empty day cells
                    tk.Label(self.calendar_frame, text="", width=10, height=2).grid(row=row, column=col)
                else:
                    # Highlight today's date and dates with events
                    event_date_key = (self.current_year, self.current_month, day)
                    events_for_day = self.events.get(event_date_key, [])
                    day_label = tk.Label(self.calendar_frame, text=str(day), width=10, height=2, relief=tk.RAISED)
                    if event_date_key == (self.current_date.year, self.current_date.month, self.current_date.day):
                        day_label.config(bg="yellow")
                    elif events_for_day:
                        day_label.config(bg="light blue")
                    # Bind left-click to show events and right-click to delete events for the day
                    day_label.bind("<Button-1>", lambda e, year=self.current_year, month=self.current_month,
                                                        day=day: self.show_events(year, month, day))
                    day_label.bind("<Button-3>", lambda e, year=self.current_year, month=self.current_month,
                                                        day=day: self.delete_event(year, month, day))
                    day_label.grid(row=row, column=col)

    # Navigation functions to move between months and years
    def prev_month(self):
        self.current_month -= 1
        if self.current_month == 0:  # Wrap to December of the previous year
            self.current_month = 12
            self.current_year -= 1
        self.update_calendar()

    def next_month(self):
        self.current_month += 1
        if self.current_month == 13:  # Wrap to January of the next year
            self.current_month = 1
            self.current_year += 1
        self.update_calendar()

    def prev_year(self):
        self.current_year -= 1
        self.update_calendar()

    def next_year(self):
        self.current_year += 1
        self.update_calendar()

    def go_to_today(self):
        # Set the calendar to the current month and year
        self.current_year = self.current_date.year
        self.current_month = self.current_date.month
        self.update_calendar()

    # Event management functions (add, show, delete)
    def add_event(self):
        # Opens a new window to input event details
        event_window = tk.Toplevel(self)
        event_window.title("Add Event")
        # Event details form
        tk.Label(event_window, text="Title:").grid(row=0, column=0, padx=10, pady=5)
        title_entry = tk.Entry(event_window)
        title_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(event_window, text="Date:").grid(row=1, column=0, padx=10, pady=5)
        date_entry = Calendar(event_window, selectmode='day', year=self.current_year, month=self.current_month,
                              day=self.current_date.day)
        date_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(event_window, text="Description:").grid(row=2, column=0, padx=10, pady=5)
        description_entry = tk.Entry(event_window)
        description_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(event_window, text="Add", command=lambda: self.save_event(event_window, title_entry.get(), date_entry,
                                                                            description_entry.get())).grid(row=3,
                                                                                                           column=0,
                                                                                                           columnspan=2,
                                                                                                           pady=5)

    def show_events(self, year, month, day):
        # Displays events for a specific date
        date_key = (year, month, day)
        events = self.events.get(date_key, [])
        events_list = '\n'.join([f"Title: {event['title']}, Description: {event['description']}" for event in events])
        messagebox.showinfo("Events", events_list or "No Events")

    def delete_event(self, year, month, day):
        # Deletes all events for a specific date
        date_key = (year, month, day)
        if date_key in self.events and messagebox.askyesno("Delete Events",
                                                           "Do you want to delete all events for this date?"):
            del self.events[date_key]
            self.update_calendar()

    def save_event(self, window, title, calendar_widget, description):
        # Saves a new event and updates the calendar
        if not title or not description:
            messagebox.showerror("Error", "Title and description must not be empty.")
            return
        event_date = calendar_widget.selection_get()
        if event_date < datetime.date.today():
            messagebox.showerror("Error", "Event date must not be in the past.")
            return
        date_key = (event_date.year, event_date.month, event_date.day)
        self.events.setdefault(date_key, []).append({"title": title, "description": description})
        self.update_calendar()
        window.destroy()

    def show_all_events(self):
        # Displays a list of all upcoming events
        all_events_list = '\n\n'.join([f"{date}: " + '\n'.join(
            [f"Title: {event['title']}, Description: {event['description']}" for event in events]) for date, events in
                                       sorted(self.events.items())])
        messagebox.showinfo("All Events", all_events_list or "No upcoming events")


app = CalendarApp()
app.mainloop()
