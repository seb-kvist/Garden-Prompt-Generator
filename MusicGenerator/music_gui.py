import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import time
import os
import re

# === Configuration ===
INFER_SCRIPT_DIR = r"C:\Users\sebas\Downloads\LofiSongs\DiffRythmLocal\DiffRhythm"
BATCH_FILE_PATH = os.path.join(INFER_SCRIPT_DIR, "scripts", "infer_prompt_ref.bat")
FAVORITES_FILE = os.path.join(os.path.dirname(__file__), "prompt_favorites.txt")

# Counter to track total number of songs generated (across runs)
song_counter = 0

def build_gui(parent):
    from tkinter import font as tkfont
    global song_counter

    bold_font = ("Poppins", 10, "bold")
    regular_font = ("Poppins", 10)

    tk.Label(parent, text="🎵 Music Generator", font=("Poppins", 14)).pack(pady=(15, 10))

    prompt_frame = tk.Frame(parent)
    prompt_frame.pack(pady=5)

    tk.Label(prompt_frame, text="🎙 Prompt:", font=regular_font).grid(row=0, column=0, sticky="e", padx=(0, 5))
    prompt_entry = tk.Entry(prompt_frame, width=60)
    prompt_entry.insert(0, "slow Lo-fi ambience: instrumental with soft guitar, mellow piano, 40 BPM drum beat.")
    prompt_entry.grid(row=0, column=1, padx=5)

    tk.Label(prompt_frame, text="🎧 Song count:", font=regular_font).grid(row=0, column=2, padx=(20, 5))
    song_count = tk.IntVar(value=2)
    tk.Spinbox(prompt_frame, from_=1, to=1000, textvariable=song_count, width=5).grid(row=0, column=3)

    tk.Button(prompt_frame, text="💾 Save to Favorites", command=lambda: save_favorite(prompt_entry)).grid(row=0, column=4, padx=(20, 0))

    status_frame = tk.Frame(parent)
    status_frame.pack(pady=5)

    status_label = tk.Label(status_frame, text="⏹ Idle", fg="black", bg="lightgray", width=10)
    status_label.pack(side="left", padx=5)

    song_progress_label = tk.Label(status_frame, text="", font=regular_font)
    song_progress_label.pack(side="left", padx=10)

    results_frame = tk.Frame(parent, bg="#f0f0f0")
    results_frame.pack(fill="both", expand=True, padx=10, pady=(10, 5))

    def save_favorite(entry_widget):
        prompt = entry_widget.get().strip()
        if not prompt:
            messagebox.showwarning("Missing prompt", "Please enter a prompt to save.")
            return
        with open(FAVORITES_FILE, "a", encoding="utf-8") as f:
            f.write(prompt + "\n")
        messagebox.showinfo("Saved", "Prompt saved to favorites.")

    def open_file_location(filename):
        path = os.path.join(INFER_SCRIPT_DIR, "infer", "example", "output_en", filename)
        if os.path.exists(path):
            subprocess.Popen(f'explorer /select,"{path}"')
        else:
            messagebox.showwarning("File not found", f"Could not locate:\n{filename}")

    def add_song_card(index, duration, filename):
        card = tk.Frame(results_frame, bd=1, relief="solid", bg="white", padx=10, pady=5)
        card.pack(pady=5, fill="x")

        tk.Label(card, text=f"🎵 Song {index}", font=bold_font, bg="white").pack(anchor="w")
        tk.Label(card, text=f"⏱ Time to generate: {duration:.2f} seconds", bg="white").pack(anchor="w")
        tk.Label(card, text=f"💾 Saved: {filename}", bg="white", fg="green").pack(anchor="w")

        tk.Button(card, text="📂 Open Folder", command=lambda: open_file_location(filename)).pack(anchor="e", pady=3)

    def run_generation():
        global song_counter
        prompt = prompt_entry.get().strip()
        count = song_count.get()
        if not prompt:
            messagebox.showerror("Error", "Prompt cannot be empty.")
            return

        if not os.path.exists(BATCH_FILE_PATH):
            messagebox.showerror("Missing BAT file", f"Cannot find batch file at:\n{BATCH_FILE_PATH}")
            return

        # Update BAT file with prompt and count
        new_lines = []
        with open(BATCH_FILE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("set MAX="):
                    new_lines.append(f"set MAX={count}\n")
                elif "--ref-prompt" in line:
                    new_lines.append(f'python %~dp0..\\infer\\infer.py --ref-prompt "{prompt}" --audio-length 95 --repo-id ASLP-lab/DiffRhythm-1_2 --output-dir infer/example/output_en --chunked\n')
                else:
                    new_lines.append(line)
        with open(BATCH_FILE_PATH, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        def run():
            global song_counter
            status_label.config(text="🟢 Running", bg="green", fg="white")
            song_index = 0
            duration = 0
            process = subprocess.Popen(
                ["cmd.exe", "/c", BATCH_FILE_PATH],
                cwd=INFER_SCRIPT_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )

            for line in process.stdout:
                line = line.strip()
                if line.startswith("Loop "):
                    parts = line.split()
                    if len(parts) >= 3:
                        song_index = int(parts[1])
                        song_progress_label.config(text=f"🎶 Song {song_index} of {count}")
                elif "inference cost" in line:
                    duration = float(line.split()[-2])
                elif "Song saved as" in line:
                    filename = line.split("as")[-1].strip()
                    song_counter += 1
                    add_song_card(song_counter, duration, filename)
                elif "DONE" in line:
                    status_label.config(text="✅ Done", bg="lightgreen", fg="black")
                    song_progress_label.config(text="")

            process.wait()

        threading.Thread(target=run).start()

    tk.Button(parent, text="🎼 Generate Songs", font=("Poppins", 11),
              command=run_generation).pack(pady=15)