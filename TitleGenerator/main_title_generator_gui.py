
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
import sys
import random

# Paths
base_dir = os.path.dirname(os.path.abspath(__file__))
TITLE_FILE = os.path.join(base_dir, "generated_titles.txt")
HISTORY_FILE = os.path.join(base_dir, "title_history_log.txt")
CSV_FILE = os.path.join(base_dir, "thumbnail_title_word_lists_fully_filled_unique_200_final.csv")

# Globals
title_frame = None
selected_option = tk.StringVar(value="First_Word_Japanese")
current_theme = "light"

# Themes
THEMES = {
    "light": {
        "bg": "#fefefe", "fg": "#000", "entry": "#ffffff",
        "button": "#cdeeff", "button_fg": "#000", "frame": "#e8f4fc",
        "exit": "#fdd", "output": "#ffffff"
    },
    "dark": {
        "bg": "#2c2c2c", "fg": "#ffffff", "entry": "#3c3c3c",
        "button": "#557799", "button_fg": "#ffffff", "frame": "#3d4f5c",
        "exit": "#883333", "output": "#444"
    }
}

# Load CSV
try:
    df = pd.read_csv(CSV_FILE)
except Exception as e:
    messagebox.showerror("Error", f"Could not load:\n{os.path.basename(CSV_FILE)}\n\n{str(e)}")
    df = None

# Theme
def apply_theme(widget):
    colors = THEMES[current_theme]
    widget.configure(bg=colors["bg"])
    for w in widget.winfo_children():
        cls = w.__class__.__name__
        if cls in ("Frame", "LabelFrame"):
            w.configure(bg=colors["frame"])
            apply_theme(w)
        elif cls == "Label":
            w.configure(bg=colors["bg"], fg=colors["fg"])
        elif cls == "Button":
            w.configure(bg=colors["button"], fg=colors["button_fg"])
        elif cls == "Entry":
            w.configure(bg=colors["entry"], fg=colors["fg"], insertbackground=colors["fg"])
        elif cls == "Radiobutton":
            w.configure(bg=colors["bg"], fg=colors["fg"], selectcolor=colors["frame"])

def toggle_theme(root):
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    apply_theme(root)
    show_saved_titles()

# Title logic
def generate_title():
    if df is None:
        return "Error: CSV not loaded."

    try:
        first_col = selected_option.get()
        first_words = df[first_col].dropna().tolist()
        second_words = df["Second_Word"].dropna().tolist()

        if not first_words or not second_words:
            return "Error: Empty word list."

        first = random.choice(first_words)
        second = random.choice(second_words)
        return f"{first} {second}"
    except Exception as e:
        return f"Error generating title: {str(e)}"

def save_title(title_text):
    with open(TITLE_FILE, "a", encoding="utf-8") as f:
        f.write(f"{title_text}\n")

def delete_title(line_to_delete):
    if not os.path.exists(TITLE_FILE):
        return
    with open(TITLE_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(TITLE_FILE, "w", encoding="utf-8") as f:
        for line in lines:
            if line.strip() != line_to_delete.strip():
                f.write(line)
    show_saved_titles()

def show_saved_titles():
    for widget in title_frame.winfo_children():
        widget.destroy()

    if not os.path.exists(TITLE_FILE):
        return

    with open(TITLE_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        display_title(line.strip())

def display_title(text):
    container = tk.Frame(title_frame, bg=THEMES[current_theme]["output"], bd=1, relief="solid")
    container.pack(fill="x", padx=10, pady=5)

    tk.Label(container, text=text, bg=THEMES[current_theme]["output"],
             fg=THEMES[current_theme]["fg"], font=("Poppins", 10), wraplength=800, justify="left").pack(anchor="w", padx=10, pady=5)

    btn_frame = tk.Frame(container, bg=THEMES[current_theme]["output"])
    btn_frame.pack(anchor="e", padx=10, pady=(0, 5))

    def copy_title():
        title_frame.clipboard_clear()
        title_frame.clipboard_append(text)
        messagebox.showinfo("Copied", "Title copied to clipboard.")

    def delete_this():
        if messagebox.askyesno("Delete", f"Delete title:\n{text}?"):
            delete_title(text)

    def seo_prompt():
        prompt = f"""
I want you to give me SEO optimized for "{text}". The description:

I want you to follow these rules when getting SEO:

1. SEO-Optimized YouTube Title
Titles should include relevant keywords like example: Lo-Fi, Chill Beats, Japanese/Chinese/Asian Garden, Zen, Relaxing, Study, Sleep, Meditation, etc. It should include the title: "{text}"
Clear, simple, clickable language
Not repetitive or generic
Natural emojis that fit the vibe

2. YouTube Description
3–5 aesthetic and calming sentences
Tone: peaceful, poetic, and atmospheric
Includes this subscription link exactly once, on its own line:
👉 https://www.youtube.com/@CozyLofiGarden?sub_confirmation=1
Never mentions if it was a livestream

3. YouTube Tags
Up to 500 characters
Mix of broad and niche keywords
No hashtags

4. Pinned Comment Suggestion
Welcoming and aesthetic tone
Encourages audience interaction (question or prompt)
        """.strip()

        title_frame.clipboard_clear()
        title_frame.clipboard_append(prompt)
        messagebox.showinfo("Prompt Ready", "🧠 SEO Prompt copied to clipboard!")

    tk.Button(btn_frame, text="📋 Copy", command=copy_title,
              bg=THEMES[current_theme]["button"], fg=THEMES[current_theme]["button_fg"],
              font=("Poppins", 9), relief="flat").pack(side=tk.LEFT, padx=3)

    tk.Button(btn_frame, text="🗑 Delete", command=delete_this,
              bg=THEMES[current_theme]["exit"], fg="black",
              font=("Poppins", 9), relief="flat").pack(side=tk.LEFT, padx=3)

    tk.Button(btn_frame, text="✨ SEO Prompt", command=seo_prompt,
              bg=THEMES[current_theme]["button"], fg=THEMES[current_theme]["button_fg"],
              font=("Poppins", 9), relief="flat").pack(side=tk.LEFT, padx=3)

# GUI entrypoint
def build_gui(parent):
    global title_frame

    apply_theme(parent)

    tk.Label(parent, text="📘 Title Generator", font=("Poppins", 14)).pack(pady=10)

    radio_frame = tk.Frame(parent)
    radio_frame.pack(pady=5)

    tk.Label(radio_frame, text="Choose first word category: Japanese, Chinese, Rain-Themed", font=("Poppins", 10)).pack(anchor="w")

    options = {
        "Japanese": "First_Word_Japanese",
        "Chinese": "First_Word_Chinese",
        "Rain-Themed": "Rain_Word"
    }

    for label, value in options.items():
        tk.Radiobutton(radio_frame, text=label, variable=selected_option, value=value,
                       font=("Poppins", 10)).pack(anchor="w")

    btn_frame = tk.Frame(parent)
    btn_frame.pack(pady=5)

    def generate_and_display():
        title = generate_title()
        if "Error" in title:
            messagebox.showerror("Generation Failed", title)
            return

        if not os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                pass

        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = set(line.strip() for line in f if line.strip())

        if title in history:
            messagebox.showwarning("Duplicate Title", "⚠️ This title has already been generated before!")
            return

        save_title(title)
        display_title(title)

        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(title + "\n")

    tk.Button(btn_frame, text="✨ Generate Title", command=generate_and_display,
              font=("Poppins", 11)).pack(side=tk.LEFT, padx=6)

    tk.Button(btn_frame, text="🌙 Toggle Theme", command=lambda: toggle_theme(parent),
              font=("Poppins", 11)).pack(side=tk.LEFT, padx=6)

    canvas_frame = tk.Frame(parent)
    canvas_frame.pack(fill="both", expand=True, padx=10, pady=5)

    canvas = tk.Canvas(canvas_frame)
    scrollbar = tk.Scrollbar(canvas_frame, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    title_frame_container = tk.Frame(canvas)
    canvas_window = canvas.create_window((0, 0), window=title_frame_container, anchor="nw")

    def resize_canvas(event): canvas.itemconfig(canvas_window, width=event.width)
    def on_configure(event): canvas.configure(scrollregion=canvas.bbox("all"))
    def _on_mousewheel(event): canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind("<Configure>", resize_canvas)
    title_frame_container.bind("<Configure>", on_configure)
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    title_frame = title_frame_container
    show_saved_titles()
