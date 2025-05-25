import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk
import datetime

class FitDeskApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("FitDesk")
        self.geometry("1000x700")
        self.minsize(800, 600)
        
        self._mode = {
            "bg": "#FFFFFF",
            "fg": "#333333",
            "accent": "#3498db",
            "button_bg": "#3498db",
            "button_fg": "#FFFFFF",
            "highlight": "#e6f3fb",
            "border": "#d1d1d1"
        }
        
        self.light_mode = {
            "bg": "#333333",
            "fg": "#FFFFFF",
            "accent": "#3498db",
            "button_bg": "#3498db",
            "button_fg": "#FFFFFF",
            "highlight": "#444444",
            "border": "#555555"
        }
        
        self.theme = self.light_mode
        
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Dictionary to store frames
        self.frames = {}
        
        for F in (MenuPage, MyExercisesPage, LiveExercisePage, WorkoutHistoryPage, SettingsPage):
            frame = F(self.container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("MenuPage")
    
    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.configure(bg=self.theme["bg"])
        frame.tkraise()
    
    def toggle_theme(self):
        """Toggle between light and dark mode"""
        if self.theme == self.light_mode:
            self.theme = self.dark_mode
        else:
            self.theme = self.light_mode
            
        for frame in self.frames.values():
            frame.update_theme()


class BasePage(tk.Frame):
    """Base class for all pages"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()
    
    def create_widgets(self):
        pass
    
    def update_theme(self):
        """Update the theme colors for the page"""
        self.configure(bg=self.controller.theme["bg"])
        
        for widget in self.winfo_children():
            widget_type = widget.winfo_class()
            
            if widget_type in ("Frame", "Labelframe", "TFrame"):
                widget.configure(bg=self.controller.theme["bg"])
            
            elif widget_type in ("Label", "TLabel"):
                widget.configure(bg=self.controller.theme["bg"], 
                                fg=self.controller.theme["fg"])
            
            elif widget_type in ("Button", "TButton"):
                widget.configure(bg=self.controller.theme["button_bg"],
                                fg=self.controller.theme["button_fg"])
            
            if widget_type in ("Frame", "Labelframe", "TFrame"):
                for child in widget.winfo_children():
                    child_type = child.winfo_class()
                    if child_type in ("Label", "TLabel"):
                        child.configure(bg=self.controller.theme["bg"], 
                                      fg=self.controller.theme["fg"])
                    elif child_type in ("Button", "TButton"):
                        child.configure(bg=self.controller.theme["button_bg"],
                                      fg=self.controller.theme["button_fg"])


class MenuPage(BasePage):
    """Main menu page"""
    def create_widgets(self):
        self.configure(bg=self.controller.theme["bg"])
        
        header_frame = tk.Frame(self, bg=self.controller.theme["bg"])
        header_frame.pack(fill="x", padx=20, pady=30)
        
        logo_label = tk.Label(header_frame, text="FitDesk", font=("Arial", 32, "bold"), 
                             bg=self.controller.theme["bg"], fg=self.controller.theme["fg"])
        logo_label.pack(side="left")
        
        welcome_frame = tk.Frame(self, bg=self.controller.theme["bg"])
        welcome_frame.pack(fill="x", padx=40, pady=20)
        
        welcome_label = tk.Label(welcome_frame, text="Welcome back, Sarah!", 
                                font=("Arial", 24), bg=self.controller.theme["bg"], 
                                fg=self.controller.theme["fg"])
        welcome_label.pack(anchor="w")
        
        # Navigation buttons frame
        button_frame = tk.Frame(self, bg=self.controller.theme["bg"])
        button_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        my_exercises_btn = tk.Button(button_frame, text="My Exercises", font=("Arial", 14), 
                                   bg=self.controller.theme["button_bg"], fg=self.controller.theme["button_fg"],
                                   width=20, height=2, relief=tk.RAISED,
                                   command=lambda: self.controller.show_frame("MyExercisesPage"))
        my_exercises_btn.pack(pady=20)
        
        workout_history_btn = tk.Button(button_frame, text="Workout History", font=("Arial", 14), 
                                      bg=self.controller.theme["button_bg"], fg=self.controller.theme["button_fg"],
                                      width=20, height=2, relief=tk.RAISED,
                                      command=lambda: self.controller.show_frame("WorkoutHistoryPage"))
        workout_history_btn.pack(pady=20)
        
        settings_btn = tk.Button(button_frame, text="Settings", font=("Arial", 14), 
                               bg=self.controller.theme["button_bg"], fg=self.controller.theme["button_fg"],
                               width=20, height=2, relief=tk.RAISED,
                               command=lambda: self.controller.show_frame("SettingsPage"))
        settings_btn.pack(pady=20)


class MyExercisesPage(BasePage):
    """My Exercises page with categories and exercise options"""
    def create_widgets(self):
        self.configure(bg=self.controller.theme["bg"])
        
        # Header with navigation
        header_frame = tk.Frame(self, bg=self.controller.theme["bg"])
        header_frame.pack(fill="x", padx=20, pady=15)
        
        back_btn = tk.Button(header_frame, text="← Back", font=("Arial", 12),
                           bg=self.controller.theme["button_bg"], fg=self.controller.theme["button_fg"],
                           command=lambda: self.controller.show_frame("MenuPage"))
        back_btn.pack(side="left")
        
        title_label = tk.Label(header_frame, text="My Exercises", font=("Arial", 20, "bold"),
                             bg=self.controller.theme["bg"], fg=self.controller.theme["fg"])
        title_label.pack(side="left", padx=20)
        
        # Exercise categories
        categories_frame = tk.Frame(self, bg=self.controller.theme["bg"])
        categories_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Upper body exercises section
        upper_frame = tk.Frame(categories_frame, bg=self.controller.theme["bg"], pady=15)
        upper_frame.pack(fill="x")
        
        upper_label = tk.Label(upper_frame, text="Upper Body", font=("Arial", 16, "bold"),
                             bg=self.controller.theme["bg"], fg=self.controller.theme["fg"])
        upper_label.pack(anchor="w")
        
        upper_exercises = tk.Frame(upper_frame, bg=self.controller.theme["bg"])
        upper_exercises.pack(fill="x", pady=10)
        
        exercise_btn = tk.Button(upper_exercises, text="Shoulder Shrugs", font=("Arial", 12),
                               bg=self.controller.theme["button_bg"], fg=self.controller.theme["button_fg"],
                               width=15, command=lambda: self.start_exercise("Shoulder Shrugs"))
        exercise_btn.pack(side="left", padx=10)
        
        exercise_btn = tk.Button(upper_exercises, text="Bicep Curls", font=("Arial", 12),
                               bg=self.controller.theme["button_bg"], fg=self.controller.theme["button_fg"],
                               width=15, command=lambda: self.start_exercise("Bicep Curls"))
        exercise_btn.pack(side="left", padx=10)
        
        exercise_btn = tk.Button(upper_exercises, text="Push Ups", font=("Arial", 12),
                               bg=self.controller.theme["button_bg"], fg=self.controller.theme["button_fg"],
                               width=15, command=lambda: self.start_exercise("Push Ups"))
        exercise_btn.pack(side="left", padx=10)
        
        # Lower body exercises section
        lower_frame = tk.Frame(categories_frame, bg=self.controller.theme["bg"], pady=15)
        lower_frame.pack(fill="x")
        
        lower_label = tk.Label(lower_frame, text="Lower Body", font=("Arial", 16, "bold"),
                             bg=self.controller.theme["bg"], fg=self.controller.theme["fg"])
        lower_label.pack(anchor="w")
        
        lower_exercises = tk.Frame(lower_frame, bg=self.controller.theme["bg"])
        lower_exercises.pack(fill="x", pady=10)
        
        exercise_btn = tk.Button(lower_exercises, text="Squats", font=("Arial", 12),
                               bg=self.controller.theme["button_bg"], fg=self.controller.theme["button_fg"],
                               width=15, command=lambda: self.start_exercise("Squats"))
        exercise_btn.pack(side="left", padx=10)
        
        exercise_btn = tk.Button(lower_exercises, text="Lunges", font=("Arial", 12),
                               bg=self.controller.theme["button_bg"], fg=self.controller.theme["button_fg"],
                               width=15, command=lambda: self.start_exercise("Lunges"))
        exercise_btn.pack(side="left", padx=10)
        
        # Full body exercises section
        full_frame = tk.Frame(categories_frame, bg=self.controller.theme["bg"], pady=15)
        full_frame.pack(fill="x")
        
        full_label = tk.Label(full_frame, text="Full Body", font=("Arial", 16, "bold"),
                            bg=self.controller.theme["bg"], fg=self.controller.theme["fg"])
        full_label.pack(anchor="w")
        
        full_exercises = tk.Frame(full_frame, bg=self.controller.theme["bg"])
        full_exercises.pack(fill="x", pady=10)
        
        exercise_btn = tk.Button(full_exercises, text="Jumping Jacks", font=("Arial", 12),
                               bg=self.controller.theme["button_bg"], fg=self.controller.theme["button_fg"],
                               width=15, command=lambda: self.start_exercise("Jumping Jacks"))
        exercise_btn.pack(side="left", padx=10)
        
        exercise_btn = tk.Button(full_exercises, text="Burpees", font=("Arial", 12),
                               bg=self.controller.theme["button_bg"], fg=self.controller.theme["button_fg"],
                               width=15, command=lambda: self.start_exercise("Burpees"))
        exercise_btn.pack(side="left", padx=10)
    
    def start_exercise(self, exercise_name):
        """Start the selected exercise"""
        # Storing 
        self.controller.current_exercise = exercise_name
        
        # Updating the live exercise page with current exercise details
        live_page = self.controller.frames["LiveExercisePage"]
        live_page.update_exercise_info(exercise_name)
        
        # live exercise page
        self.controller.show_frame("LiveExercisePage")


class LiveExercisePage(BasePage):
    """Live exercise page with camera feed and exercise guidance"""
    def create_widgets(self):
        self.configure(bg=self.controller.theme["bg"])
        
        self.header_frame = tk.Frame(self, bg=self.controller.theme["bg"])
        self.header_frame.pack(fill="x", padx=20, pady=15)
        
        self.back_btn = tk.Button(self.header_frame, text="← Back", font=("Arial", 12),
                                bg=self.controller.theme["button_bg"], fg=self.controller.theme["button_fg"],
                                command=lambda: self.controller.show_frame("MyExercisesPage"))
        self.back_btn.pack(side="left")
        
        self.exercise_title = tk.Label(self.header_frame, text="Exercise Name", font=("Arial", 20, "bold"),
                                     bg=self.controller.theme["bg"], fg=self.controller.theme["fg"])
        self.exercise_title.pack(side="left", padx=20)
        
        # Main content - video feeds
        self.content_frame = tk.Frame(self, bg=self.controller.theme["bg"])
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left side: Camera feed placeholder
        self.camera_frame = tk.Frame(self.content_frame, bg="#222222", width=500, height=400)
        self.camera_frame.pack(side="left", fill="both", expand=True, padx=10)
        self.camera_frame.pack_propagate(False)
        
        self.camera_label = tk.Label(self.camera_frame, text="Camera Feed",
                                   font=("Arial", 18), fg="white", bg="#222222")
        self.camera_label.pack(fill="both", expand=True)
        
        # Right side: Exercise animation placeholder and instructions
        self.guide_frame = tk.Frame(self.content_frame, bg=self.controller.theme["bg"], width=350)
        self.guide_frame.pack(side="right", fill="both", expand=True, padx=10)
        self.guide_frame.pack_propagate(False)
        
        self.demo_frame = tk.Frame(self.guide_frame, bg="#333333", height=250)
        self.demo_frame.pack(fill="x", pady=10)
        self.demo_frame.pack_propagate(False)
        
        self.demo_label = tk.Label(self.demo_frame, text="Exercise Animation",
                                 font=("Arial", 16), fg="white", bg="#333333")
        self.demo_label.pack(fill="both", expand=True)
        
        self.instruction_label = tk.Label(self.guide_frame, text="Follow the exercise form shown in the animation.",
                                       font=("Arial", 12), bg=self.controller.theme["bg"], fg=self.controller.theme["fg"],
                                       wraplength=330, justify="left")
        self.instruction_label.pack(fill="x", pady=15, anchor="w")
        
        # Control buttons
        self.controls_frame = tk.Frame(self, bg=self.controller.theme["bg"])
        self.controls_frame.pack(fill="x", padx=20, pady=20)
        
        self.restart_btn = tk.Button(self.controls_frame, text="Restart", font=("Arial", 14),
                                   bg="#4CAF50", fg="white", width=15,
                                   command=self.restart_exercise)
        self.restart_btn.pack(side="left", padx=10)
        
        self.stop_btn = tk.Button(self.controls_frame, text="Stop", font=("Arial", 14),
                                bg="#F44336", fg="white", width=15,
                                command=lambda: self.controller.show_frame("MyExercisesPage"))
        self.stop_btn.pack(side="left", padx=10)
    
    def update_exercise_info(self, exercise_name):
        """Update the page with the selected exercise information"""
        self.exercise_title.config(text=exercise_name)
        
        # Exercise-specific instructions
        instructions = {
            "Shoulder Shrugs": "Stand straight with arms at your sides. Raise both shoulders up toward your ears, hold briefly, then lower.",
            "Bicep Curls": "Stand with feet shoulder-width apart, hold weights with palms facing forward. Bend elbows to bring weights toward shoulders.",
            "Push Ups": "Start in a plank position with hands slightly wider than shoulders. Lower your body until chest nearly touches the floor, then push back up.",
            "Squats": "Stand with feet shoulder-width apart. Lower your body by bending knees and pushing hips back as if sitting in a chair.",
            "Lunges": "Step forward with one leg, lowering your body until both knees are bent at 90 degrees. Push back to starting position.",
            "Jumping Jacks": "Start with feet together and arms at sides. Jump to spread legs and raise arms above head, then jump back to starting position.",
            "Burpees": "Begin in standing position, drop into a squat, kick feet back into plank, perform a push-up, return to squat, then jump up with arms extended."
        }
        
        if exercise_name in instructions:
            self.instruction_label.config(text=instructions[exercise_name])
    
    def restart_exercise(self):
        """Restart the current exercise"""
        # This would reset the exercise tracking logic
        # For now, just show a message
        print("Restarting exercise...")


class WorkoutHistoryPage(BasePage):
    """Workout history page with calendar view and statistics"""
    def create_widgets(self):
        self.configure(bg=self.controller.theme["bg"])
        
        # Header with navigation
        header_frame = tk.Frame(self, bg=self.controller.theme["bg"])
        header_frame.pack(fill="x", padx=20, pady=15)
        
        back_btn = tk.Button(header_frame, text="← Back", font=("Arial", 12),
                           bg=self.controller.theme["button_bg"], fg=self.controller.theme["button_fg"],
                           command=lambda: self.controller.show_frame("MenuPage"))
        back_btn.pack(side="left")
        
        title_label = tk.Label(header_frame, text="Workout History", font=("Arial", 20, "bold"),
                             bg=self.controller.theme["bg"], fg=self.controller.theme["fg"])
        title_label.pack(side="left", padx=20)
        
        # Main content
        content_frame = tk.Frame(self, bg=self.controller.theme["bg"])
        content_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # wweekly view of workout history
        calendar_frame = tk.Frame(content_frame, bg=self.controller.theme["bg"])
        calendar_frame.pack(fill="x", pady=10)
        
        # Title for the weekly view
        week_label = tk.Label(calendar_frame, text="This Week", font=("Arial", 16, "bold"),
                            bg=self.controller.theme["bg"], fg=self.controller.theme["fg"])
        week_label.pack(anchor="w", pady=5)

        # Weekly calendar view
        days_frame = tk.Frame(calendar_frame, bg=self.controller.theme["bg"])
        days_frame.pack(fill="x", pady=10)
        
        # current date and start of week (Monday)
        today = datetime.datetime.now()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        
        # a frame for each day of the week
        for i in range(7):
            day_date = start_of_week + datetime.timedelta(days=i)
            day_name = day_date.strftime("%a")
            day_num = day_date.strftime("%d")
            
            # if this day has a workout (mock data)
            has_workout = i in [0, 2, 4] # Monday, Wednesday, Friday
            
            day_frame = tk.Frame(days_frame, bg=self.controller.theme["highlight"] if has_workout else self.controller.theme["bg"],
                               width=110, height=100, bd=1, relief=tk.RAISED)
            day_frame.pack(side="left", padx=5)
            day_frame.pack_propagate(False)
            
            # Day name
            day_label = tk.Label(day_frame, text=day_name, font=("Arial", 14),
                               bg=self.controller.theme["highlight"] if has_workout else self.controller.theme["bg"],
                               fg=self.controller.theme["fg"])
            day_label.pack(pady=(10, 5))
            
            # Day number
            num_label = tk.Label(day_frame, text=day_num, font=("Arial", 16, "bold"),
                               bg=self.controller.theme["highlight"] if has_workout else self.controller.theme["bg"],
                               fg=self.controller.theme["fg"])
            num_label.pack(pady=5)
            
            # Workout indicator
            if has_workout:
                workout_label = tk.Label(day_frame, text="●", font=("Arial", 12),
                                       bg=self.controller.theme["highlight"],
                                       fg=self.controller.theme["accent"])
                workout_label.pack(pady=5)
                
        # Statistics section
        stats_frame = tk.Frame(content_frame, bg=self.controller.theme["bg"], pady=20)
        stats_frame.pack(fill="x")
        
        stats_label = tk.Label(stats_frame, text="Progress Statistics", font=("Arial", 16, "bold"),
                             bg=self.controller.theme["bg"], fg=self.controller.theme["fg"])
        stats_label.pack(anchor="w", pady=10)
        
        # a frame for the statistics cards
        cards_frame = tk.Frame(stats_frame, bg=self.controller.theme["bg"])
        cards_frame.pack(fill="x", pady=10)
        
        # Total workouts card
        workouts_card = tk.Frame(cards_frame, bg=self.controller.theme["highlight"],
                               width=220, height=150, bd=1, relief=tk.RAISED)
        workouts_card.pack(side="left", padx=10)
        workouts_card.pack_propagate(False)
        
        workouts_title = tk.Label(workouts_card, text="Total Workouts", font=("Arial", 14),
                                bg=self.controller.theme["highlight"], fg=self.controller.theme["fg"])
        workouts_title.pack(pady=(20, 10))
        
        workouts_value = tk.Label(workouts_card, text="12", font=("Arial", 36, "bold"),
                                bg=self.controller.theme["highlight"], fg=self.controller.theme["accent"])
        workouts_value.pack()
        
        # Calories card
        calories_card = tk.Frame(cards_frame, bg=self.controller.theme["highlight"],
                               width=220, height=150, bd=1, relief=tk.RAISED)
        calories_card.pack(side="left", padx=10)
        calories_card.pack_propagate(False)
        
        calories_title = tk.Label(calories_card, text="Calories Burned", font=("Arial", 14),
                                bg=self.controller.theme["highlight"], fg=self.controller.theme["fg"])
        calories_title.pack(pady=(20, 10))
        
        calories_value = tk.Label(calories_card, text="750", font=("Arial", 36, "bold"),
                                bg=self.controller.theme["highlight"], fg=self.controller.theme["accent"])
        calories_value.pack()
        
        # Streak card
        streak_card = tk.Frame(cards_frame, bg=self.controller.theme["highlight"],
                             width=220, height=150, bd=1, relief=tk.RAISED)
        streak_card.pack(side="left", padx=10)
        streak_card.pack_propagate(False)
        
        streak_title = tk.Label(streak_card, text="Current Streak", font=("Arial", 14),
                              bg=self.controller.theme["highlight"], fg=self.controller.theme["fg"])
        streak_title.pack(pady=(20, 10))
        
        streak_value = tk.Label(streak_card, text="3 days", font=("Arial", 36, "bold"),
                              bg=self.controller.theme["highlight"], fg=self.controller.theme["accent"])
        streak_value.pack()


class SettingsPage(BasePage):
    """Settings page with customization options"""
    def create_widgets(self):
        self.configure(bg=self.controller.theme["bg"])
        
        # Header with navigation
        header_frame = tk.Frame(self, bg=self.controller.theme["bg"])
        header_frame.pack(fill="x", padx=20, pady=15)
        
        back_btn = tk.Button(header_frame, text="← Back", font=("Arial", 12),
                           bg=self.controller.theme["button_bg"], fg=self.controller.theme["button_fg"],
                           command=lambda: self.controller.show_frame("MenuPage"))
        back_btn.pack(side="left")
        
        title_label = tk.Label(header_frame, text="Settings", font=("Arial", 20, "bold"),
                             bg=self.controller.theme["bg"], fg=self.controller.theme["fg"])
        title_label.pack(side="left", padx=20)
        
        # Settings content
        content_frame = tk.Frame(self, bg=self.controller.theme["bg"])
        content_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Theme settings
        theme_frame = tk.Frame(content_frame, bg=self.controller.theme["bg"], pady=15)
        theme_frame.pack(fill="x")
        
        theme_label = tk.Label(theme_frame, text="Appearance", font=("Arial", 16, "bold"),
                             bg=self.controller.theme["bg"], fg=self.controller.theme["fg"])
        theme_label.pack(anchor="w")
        
        theme_options = tk.Frame(theme_frame, bg=self.controller.theme["bg"], pady=10)
        theme_options.pack(fill="x")
        
        theme_mode_label = tk.Label(theme_options, text="Theme Mode:", font=("Arial", 12),
                                  bg=self.controller.theme["bg"], fg=self.controller.theme["fg"])
        theme_mode_label.pack(side="left", padx=(0, 10))
        
        # Light mode button
        light_button = tk.Button(theme_options, text="Light Mode", font=("Arial", 12),
                               bg=self.controller.theme["button_bg"], fg=self.controller.theme["button_fg"],
                               command=self.set_light_mode)
        light_button.pack(side="left", padx=5)
        
        # Dark mode button
        dark_button = tk.Button(theme_options, text="Dark Mode", font=("Arial", 12),
                              bg=self.controller.theme["button_bg"], fg=self.controller.theme["button_fg"],
                              command=self.set_dark_mode)
        dark_button.pack(side="left", padx=5)
        
        # Goal settings
        goals_frame = tk.Frame(content_frame, bg=self.controller.theme["bg"], pady=20)
        goals_frame.pack(fill="x")
        
        goals_label = tk.Label(goals_frame, text="Workout Goals", font=("Arial", 16, "bold"),
                             bg=self.controller.theme["bg"], fg=self.controller.theme["fg"])
        goals_label.pack(anchor="w")
        
        # Weekly workouts goal
        weekly_frame = tk.Frame(goals_frame, bg=self.controller.theme["bg"], pady=10)
        weekly_frame.pack(fill="x")
        
        weekly_label = tk.Label(weekly_frame, text="Weekly Workouts:", font=("Arial", 12),
                              bg=self.controller.theme["bg"], fg=self.controller.theme["fg"])
        weekly_label.pack(side="left")
        
        weekly_var = tk.StringVar(value="3")
        weekly_spinbox = ttk.Spinbox(weekly_frame, from_=1, to=7, width=5, textvariable=weekly_var)
        weekly_spinbox.pack(side="left", padx=10)
        
        # Calories goal
        calories_frame = tk.Frame(goals_frame, bg=self.controller.theme["bg"], pady=10)
        calories_frame.pack(fill="x")
        
        calories_label = tk.Label(calories_frame, text="Daily Calorie Target:", font=("Arial", 12),
                                bg=self.controller.theme["bg"], fg=self.controller.theme["fg"])
        calories_label.pack(side="left")
        
        calories_var = tk.StringVar(value="300")
        calories_spinbox = ttk.Spinbox(calories_frame, from_=100, to=1000, increment=50, width=5, textvariable=calories_var)
        calories_spinbox.pack(side="left", padx=10)
        
        # Notification settings
        notif_frame = tk.Frame(content_frame, bg=self.controller.theme["bg"], pady=20)
        notif_frame.pack(fill="x")
        
        notif_label = tk.Label(notif_frame, text="Notifications", font=("Arial", 16, "bold"),
                             bg=self.controller.theme["bg"], fg=self.controller.theme["fg"])
        notif_label.pack(anchor="w")
        
        # Reminder checkbox
        reminder_frame = tk.Frame(notif_frame, bg=self.controller.theme["bg"], pady=5)
        reminder_frame.pack(fill="x")
        
        reminder_var = tk.BooleanVar(value=True)
        reminder_check = tk.Checkbutton(reminder_frame, text="Daily workout reminders", 
                                      variable=reminder_var, bg=self.controller.theme["bg"], 
                                      fg=self.controller.theme["fg"])
        reminder_check.pack(anchor="w")
        
        # Progress updates checkbox
        progress_frame = tk.Frame(notif_frame, bg=self.controller.theme["bg"], pady=5)
        progress_frame.pack(fill="x")
        
        progress_var = tk.BooleanVar(value=True)
        progress_check = tk.Checkbutton(progress_frame, text="Weekly progress updates", 
                                      variable=progress_var, bg=self.controller.theme["bg"], 
                                      fg=self.controller.theme["fg"])
        progress_check.pack(anchor="w")
        
        # Save button
        save_frame = tk.Frame(content_frame, bg=self.controller.theme["bg"], pady=30)
        save_frame.pack(fill="x")
        
        save_button = tk.Button(save_frame, text="Save Settings", font=("Arial", 14),
                              bg=self.controller.theme["button_bg"], fg=self.controller.theme["button_fg"],
                              width=15, command=self.save_settings)
        save_button.pack()
    
    def set_light_mode(self):
        """Switch to light mode"""
        self.controller.theme = self.controller.light_mode
        self.controller.toggle_theme()
    
    def set_dark_mode(self):
        """Switch to dark mode"""
        self.controller.theme = self.controller.dark_mode
        self.controller.toggle_theme()
    
    def save_settings(self):
        """Save the current settings"""

        print("Settings saved!")


if __name__ == "__main__":
    app = FitDeskApp()
    app.mainloop()
