import tkinter as tk
from tkinter import ttk
import importlib.util
import os

# ---- Fönster ----
root = tk.Tk()
root.title("🌿 Garden Generator")
root.geometry("1000x800")

# ---- Notebook (flikar), startas EJ direkt ----
notebook = ttk.Notebook(root)
image_tab = tk.Frame(notebook)
title_tab = tk.Frame(notebook)
notebook.add(image_tab, text="🖼 Image Prompt Generator")
notebook.add(title_tab, text="🏷 Title Generator")

# ---- Ladda GUIs ----
def load_guis():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Image Prompt Generator
    image_gui_path = os.path.abspath(os.path.join(base_dir, "..", "ImagePromptGenerator", "gui_prompt_generator.py"))
    spec_img = importlib.util.spec_from_file_location("image_gui", image_gui_path)
    image_gui = importlib.util.module_from_spec(spec_img)
    spec_img.loader.exec_module(image_gui)
    image_gui.build_gui(image_tab)

    # Title Generator
    title_gui_path = os.path.abspath(os.path.join(base_dir, "..", "TitleGenerator", "main_title_generator_gui.py"))
    spec_title = importlib.util.spec_from_file_location("title_gui", title_gui_path)
    title_gui = importlib.util.module_from_spec(spec_title)
    spec_title.loader.exec_module(title_gui)
    title_gui.build_gui(title_tab)

# ---- Startskärm ----
start_frame = tk.Frame(root)
start_frame.pack(expand=True)

tk.Label(start_frame, text="🌿 Welcome to Garden Generator", font=("Poppins", 18)).pack(pady=(30, 15))

# ---- Lägg till lokal bild ----
image_path = os.path.join(os.path.dirname(__file__), "welcome_image3.png")
try:
    welcome_img = tk.PhotoImage(file=image_path)
    img_label = tk.Label(start_frame, image=welcome_img)
    img_label.image = welcome_img  # Prevent garbage collection
    img_label.pack(pady=(0, 25))
except Exception as e:
    print(f"⚠️ Could not load image: {e}")

# ---- Knappar för val ----
def open_app(tab_index):
    start_frame.destroy()
    load_guis()
    notebook.pack(fill="both", expand=True)
    notebook.select(tab_index)

tk.Button(start_frame, text="🖼 Open Image Prompt Generator", width=30,
          font=("Poppins", 12), command=lambda: open_app(0)).pack(pady=10)

tk.Button(start_frame, text="🏷 Open Title Generator", width=30,
          font=("Poppins", 12), command=lambda: open_app(1)).pack(pady=10)

# ---- Start app ----
root.mainloop()
