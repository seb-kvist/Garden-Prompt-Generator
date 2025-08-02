import tkinter as tk
from tkinter import messagebox, filedialog
import os

# Path to the .bat file (hardcoded to local path)
BAT_FILE_PATH = r"C:\Users\sebas\Downloads\LofiSongs\DiffRythmLocal\DiffRhythm\scripts\infer_prompt_ref.bat"
FAVORITES_FILE = os.path.join(os.path.dirname(__file__), "favorites.txt")

def load_bat_settings():
    try:
        with open(BAT_FILE_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
        max_line = next((l for l in lines if "set MAX=" in l), None)
        prompt_line = next((l for l in lines if "--ref-prompt" in l), None)
        max_count = int(max_line.split("=")[-1]) if max_line else 1
        prompt = prompt_line.split('--ref-prompt')[1].split('"')[1] if prompt_line else ""
        return max_count, prompt
    except Exception as e:
        messagebox.showerror("Error", f"Could not read BAT file:\n{e}")
        return 1, ""

def save_bat_settings(count, prompt):
    try:
        with open(BAT_FILE_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if "set MAX=" in line:
                lines[i] = f"set MAX={count}\n"
            elif "--ref-prompt" in line:
                parts = line.split("--ref-prompt")
                if len(parts) > 1:
                    rest = parts[1].split('"')
                    if len(rest) > 2:
                        lines[i] = parts[0] + f'--ref-prompt "{prompt}"' + '"' + '"'.join(rest[2:])

        with open(BAT_FILE_PATH, "w", encoding="utf-8") as f:
            f.writelines(lines)
        messagebox.showinfo("Saved", "BAT file updated.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not update BAT file:\n{e}")

def save_favorite(prompt):
    with open(FAVORITES_FILE, "a", encoding="utf-8") as f:
        f.write(prompt.strip() + "\n")
    messagebox.showinfo("Saved", "Prompt saved to favorites.")

def load_favorites():
    if not os.path.exists(FAVORITES_FILE):
        return []
    with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def build_gui():
    root = tk.Tk()
    root.title("🎵 Music Generator Configurator")
    root.geometry("700x400")

    count, prompt = load_bat_settings()

    tk.Label(root, text="🔁 Number of songs to generate:").pack(pady=5)
    count_var = tk.IntVar(value=count)
    tk.Entry(root, textvariable=count_var).pack(pady=5)

    tk.Label(root, text="🎼 Ref Prompt:").pack(pady=5)
    prompt_var = tk.StringVar(value=prompt)
    tk.Entry(root, textvariable=prompt_var, width=80).pack(pady=5)

    def save_all():
        save_bat_settings(count_var.get(), prompt_var.get())

    def add_to_favorites():
        save_favorite(prompt_var.get())

    def load_selected_prompt():
        selected = favorites_listbox.get(tk.ACTIVE)
        prompt_var.set(selected)

    tk.Button(root, text="💾 Save Settings", command=save_all).pack(pady=5)
    tk.Button(root, text="⭐ Save Prompt to Favorites", command=add_to_favorites).pack(pady=5)

    tk.Label(root, text="⭐ Favorite Prompts:").pack(pady=5)
    favorites_listbox = tk.Listbox(root, height=5)
    for fav in load_favorites():
        favorites_listbox.insert(tk.END, fav)
    favorites_listbox.pack(pady=5)

    tk.Button(root, text="⬇ Load Selected Prompt", command=load_selected_prompt).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    build_gui()
