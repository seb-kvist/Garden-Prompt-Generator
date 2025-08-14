import tkinter as tk
from tkinter import messagebox, filedialog
import os
from datetime import datetime
import pandas as pd
import random
import csv
import sys

# ---- Konstanter ----
OUTPUT_FILE = "generated_prompts.txt"
DEFAULT_PROMPT_COUNT = 5

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        # 👇 Detta pekar på den mapp där GUI-filen faktiskt ligger
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

CSV_FILE = resource_path("japanese_garden_objects.csv")
df = pd.read_csv(CSV_FILE)

INTROS = [
    "a tranquil Japanese garden at dusk, just after gentle rain",
    "a serene Japanese garden during a misty early morning",
    "a lush Japanese garden in the soft glow of twilight",
    "a peaceful Japanese garden after a spring rain",
    "a calm Japanese garden at golden hour with lingering mist",
    "a fog-kissed Japanese garden under warm lantern light",
    "a well-kept Japanese garden just after a passing rainstorm",
    "a vibrant Japanese garden under fading sunset light",
    "a moody Japanese garden just before nightfall",
    "a quiet Japanese garden with damp stone paths after rainfall"
]

RENDER_SETTINGS = [
    "Shot on full-frame DSLR", 
    "natural cinematic lighting", "volumetric lighting",
    "global illumination", "wide angle shot", "vibrant colors", "no bokeh", "lens simulation: 24mm ultra wide angle",
    "16:9 aspect ratio", "No stylization", "100% photo-realism"
]

THEMES = {
    "light": {
        "bg": "#f4f4f4", "fg": "#000", "entry": "#ffffff",
        "button": "#d0eaff", "button_fg": "#000", "header": "#e8f4fc",
        "prompt": "#ffffff", "exit": "#f9cccc", "csv": "#e8e8e8"
    },
    "dark": {
        "bg": "#2e2e2e", "fg": "#ffffff", "entry": "#3c3c3c",
        "button": "#446688", "button_fg": "#ffffff", "header": "#3d4f5c",
        "prompt": "#444444", "exit": "#883333", "csv": "#555555"
    }
}
current_theme = "light"

# Globala variabler för widgets (för att komma åt i funktioner)
prompt_count_entry = None
prompt_frame = None
canvas = None
canvas_window = None

def apply_theme(widget):
    colors = THEMES[current_theme]
    widget.configure(bg=colors["bg"])
    for w in widget.winfo_children():
        cls = w.__class__.__name__
        if cls in ("Frame", "LabelFrame"):
            w.configure(bg=colors["bg"])
            apply_theme(w)
        elif cls == "Label":
            w.configure(bg=colors["bg"], fg=colors["fg"])
        elif cls == "Button":
            w.configure(bg=colors["button"], fg=colors["button_fg"])
        elif cls == "Entry":
            w.configure(bg=colors["entry"], fg=colors["fg"], insertbackground=colors["fg"])

def toggle_theme(parent):
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    apply_theme(parent)
    show_saved_prompts()

def generate_prompt(df):
    intro = random.choice(INTROS)
    prompt = f"A high-resolution, ultra-realistic photograph of {intro}. "
    for column in df.columns:
        if column != "Camera/Render Settings":
            items = df[column].dropna().tolist()
            selected = random.sample(items, k=random.randint(1, min(6, len(items))))
            prompt += ", ".join(selected) + ". "
    prompt += ", ".join(RENDER_SETTINGS) + "."
    return prompt

def get_existing_prompt_count(file_path):
    if not os.path.exists(file_path):
        return 0
    highest = 0
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("Prompt "):
                try:
                    num = int(line.strip().split(" ")[1].replace(":", ""))
                    highest = max(highest, num)
                except:
                    pass
    return highest

def generate_prompt_batch():
    try:
        count = int(prompt_count_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number of prompts.")
        return
    starting_index = get_existing_prompt_count(OUTPUT_FILE) + 1
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n\n--- Prompt Batch Generated: {timestamp} ---\n")
        for i in range(count):
            prompt_number = starting_index + i
            prompt_text = generate_prompt(df)
            f.write(f"\nPrompt {prompt_number}:\n{prompt_text}\n")
    show_saved_prompts()
    messagebox.showinfo("Success", f"{count} prompts generated.")

def delete_prompt_by_number(number_to_delete):
    if not os.path.exists(OUTPUT_FILE):
        return
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    new_lines = []
    skip = False
    for line in lines:
        if line.startswith("Prompt "):
            current_num = int(line.strip().split(" ")[1].replace(":", ""))
            skip = (current_num == number_to_delete)
            if skip: continue
        if not skip:
            new_lines.append(line)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    show_saved_prompts()

def delete_batch(batch_header):
    if not os.path.exists(OUTPUT_FILE):
        return
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    keep = True
    new_lines = []
    for line in lines:
        if line.strip().startswith("--- Prompt Batch Generated"):
            keep = not line.strip() == batch_header
        if keep:
            new_lines.append(line)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    show_saved_prompts()

def show_saved_prompts():
    for widget in prompt_frame.winfo_children():
        widget.destroy()
    if not os.path.exists(OUTPUT_FILE):
        return
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    current_prompts = []
    prompt_number = None
    prompt_text = ""
    batches = []
    batch_header = None
    for line in lines:
        if line.startswith("--- Prompt Batch Generated"):
            if batch_header and current_prompts:
                batches.append((batch_header, current_prompts.copy()))
            batch_header = line.strip()
            current_prompts = []
        elif line.startswith("Prompt "):
            if prompt_number is not None and prompt_text:
                current_prompts.append((prompt_number, prompt_text.strip()))
            prompt_number = int(line.strip().split(" ")[1].replace(":", ""))
            prompt_text = ""
        else:
            prompt_text += line
    if prompt_number is not None and prompt_text:
        current_prompts.append((prompt_number, prompt_text.strip()))
    if batch_header and current_prompts:
        batches.append((batch_header, current_prompts))
    for batch_header, prompts in batches:
        display_batch(batch_header, prompts)

def display_batch(header, prompts):
    colors = THEMES[current_theme]
    outer = tk.LabelFrame(prompt_frame, text=f"{header} ({len(prompts)} prompts)",
                          bg=colors["header"], fg=colors["fg"], font=("Poppins", 10, "bold"), bd=2, relief="ridge")
    outer.pack(fill="x", padx=10, pady=8, ipadx=5, ipady=5)

    btn_frame = tk.Frame(outer, bg=colors["header"])
    btn_frame.pack(anchor="e", padx=10)
    collapsed = tk.BooleanVar(value=False)

    def toggle():
        collapsed.set(not collapsed.get())
        if collapsed.get():
            inner_frame.pack_forget()
            toggle_btn.config(text="▶")
        else:
            inner_frame.pack(fill="x")
            toggle_btn.config(text="▼")

    toggle_btn = tk.Button(btn_frame, text="▼", width=2, command=toggle)
    toggle_btn.pack(side="left")

    def copy_batch():
        full = "\n\n".join([p[1] for p in prompts])
        prompt_frame.clipboard_clear()
        prompt_frame.clipboard_append(full)
        messagebox.showinfo("Copied", f"Copied {len(prompts)} prompts.")

    def delete_entire_batch():
        delete_batch(header)

    tk.Button(btn_frame, text="📋 Copy All", command=copy_batch, bg=colors["button"],
              fg=colors["button_fg"], relief="flat", font=("Poppins", 9)).pack(side="left", padx=4)
    tk.Button(btn_frame, text="🗑 Delete Batch", command=delete_entire_batch,
              bg=colors["exit"], relief="flat", font=("Poppins", 9)).pack(side="left", padx=4)

    inner_frame = tk.Frame(outer, bg=colors["prompt"])
    inner_frame.pack(fill="x")
    for num, text in prompts:
        display_prompt(inner_frame, num, text)

def display_prompt(parent, number, text):
    colors = THEMES[current_theme]
    container = tk.Frame(parent, bg=colors["prompt"], bd=1, relief="solid")
    container.pack(anchor="w", fill="x", padx=10, pady=5)

    tk.Label(container, text=f"Prompt {number}:", font=("Poppins", 10, "bold"),
             fg="#69c", bg=colors["prompt"]).pack(anchor="w", padx=10, pady=(5, 0))

    tk.Label(container, text=text, font=("Poppins", 10), wraplength=900,
             justify="left", bg=colors["prompt"], fg=colors["fg"]).pack(anchor="w", padx=10, pady=(0, 5))

    button_frame = tk.Frame(container, bg=colors["prompt"])
    button_frame.pack(anchor="e", padx=10, pady=(0, 5))

    def copy_prompt():
        full_text = (
            "Instruction:\n"
            "Reinterpret the following prompt as a cinematic photographic scene. "
            "Do not return a rewritten version — only use it internally to generate the image.\n\n"
            f"Prompt:\n{text}"
        )
        prompt_frame.clipboard_clear()
        prompt_frame.clipboard_append(full_text)
        messagebox.showinfo("Copied", f"Prompt {number} copied with instruction.")


    def delete_prompt():
        delete_prompt_by_number(number)

    tk.Button(button_frame, text="📋 Copy", command=copy_prompt, bg=colors["button"],
              fg=colors["button_fg"], relief="flat", font=("Poppins", 9)).pack(side="left", padx=5)
    tk.Button(button_frame, text="🗑 Delete", command=delete_prompt,
              bg=colors["exit"], relief="flat", font=("Poppins", 9)).pack(side="left", padx=5)
def open_csv_editor():
    editor = tk.Toplevel()
    editor.title("Edit Object List (CSV)")
    editor.geometry("800x500")
    editor.configure(bg=THEMES[current_theme]["bg"])

    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        data = list(csv.reader(f))
    headers = data[0]
    rows = data[1:]

    table = []

    table_frame = tk.Frame(editor, bg=THEMES[current_theme]["bg"])
    table_frame.pack(fill="both", expand=True)

    for i, header in enumerate(headers):
        tk.Label(table_frame, text=header, font=("Poppins", 9, "bold"),
                 bg=THEMES[current_theme]["bg"], fg=THEMES[current_theme]["fg"]).grid(row=0, column=i)

    for r, row in enumerate(rows):
        row_widgets = []
        for c, cell in enumerate(row):
            e = tk.Entry(table_frame, width=18, bg=THEMES[current_theme]["entry"], fg=THEMES[current_theme]["fg"])
            e.insert(0, cell)
            e.grid(row=r+1, column=c, padx=1, pady=1)
            row_widgets.append(e)
        table.append(row_widgets)

    def save_csv():
        new_data = [headers]
        for row in table:
            new_data.append([cell.get() for cell in row])
        with open(CSV_FILE, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(new_data)
        messagebox.showinfo("Saved", "CSV file updated.")

    def add_row():
        r = len(table) + 1
        row_widgets = []
        for c in range(len(headers)):
            e = tk.Entry(table_frame, width=18, bg=THEMES[current_theme]["entry"], fg=THEMES[current_theme]["fg"])
            e.grid(row=r, column=c, padx=1, pady=1)
            row_widgets.append(e)
        table.append(row_widgets)

    def delete_last_row():
        if not table:
            return
        for cell in table[-1]:
            cell.destroy()
        table.pop()

    bottom = tk.Frame(editor, bg=THEMES[current_theme]["bg"])
    bottom.pack(pady=10)
    tk.Button(bottom, text="💾 Save", command=save_csv).pack(side="left", padx=6)
    tk.Button(bottom, text="➕ Add Row", command=add_row).pack(side="left", padx=6)
    tk.Button(bottom, text="➖ Delete Last Row", command=delete_last_row).pack(side="left", padx=6)
    tk.Button(bottom, text="❌ Close", command=editor.destroy).pack(side="left", padx=6)


def build_gui(parent):
    global prompt_count_entry, prompt_frame, canvas, canvas_window

    apply_theme(parent)

    tk.Label(parent, text="Japanese Garden Image Prompt Generator", font=("Poppins", 14)).pack(pady=10)

    top_controls_frame = tk.Frame(parent)
    top_controls_frame.pack(pady=(5, 0))

    prompt_row = tk.Frame(top_controls_frame)
    prompt_row.pack(pady=5)

    tk.Label(prompt_row, text="Prompts to Generate:", font=("Poppins", 10)).pack(side=tk.LEFT)
    prompt_count_entry = tk.Entry(prompt_row, width=5, font=("Poppins", 10))
    prompt_count_entry.insert(0, str(DEFAULT_PROMPT_COUNT))
    prompt_count_entry.pack(side=tk.LEFT, padx=6)

    tk.Button(prompt_row, text="📦 Generate Batch", command=generate_prompt_batch,
              relief="flat", padx=10, pady=4, font=("Poppins", 10)).pack(side=tk.LEFT, padx=5)

    # 📝 Edit CSV Button
    tk.Button(prompt_row, text="📝 Edit Object List (CSV)", command=open_csv_editor,
              relief="flat", padx=10, pady=4, font=("Poppins", 10)).pack(side=tk.LEFT, padx=5)

    tk.Button(prompt_row, text="🌙 Toggle Theme", command=lambda: toggle_theme(parent),
              relief="flat", padx=10, pady=4, font=("Poppins", 10)).pack(side=tk.LEFT, padx=5)

    canvas_frame = tk.Frame(parent)
    canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    canvas = tk.Canvas(canvas_frame)
    scrollbar = tk.Scrollbar(canvas_frame, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    prompt_frame = tk.Frame(canvas)
    canvas_window = canvas.create_window((0, 0), window=prompt_frame, anchor="nw", width=canvas.winfo_width())

    def resize_canvas(event): canvas.itemconfig(canvas_window, width=event.width)
    def on_configure(event): canvas.configure(scrollregion=canvas.bbox("all"))
    def _on_mousewheel(event): canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind("<Configure>", resize_canvas)
    prompt_frame.bind("<Configure>", on_configure)
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    show_saved_prompts()

