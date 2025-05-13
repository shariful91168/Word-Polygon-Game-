import tkinter as tk
from tkinter import messagebox
import random
import math


# --- Load Dictionary ---
def load_wordlist():
    with open("wordlist.txt", "r") as f:
        return [word.strip().lower() for word in f if len(word.strip()) >= 3]


# --- Generate Letters ---
def generate_letter_set(wordlist):
    long_words = [w for w in wordlist if len(w) == 7]
    base_word = random.choice(long_words)
    letters = list(set(base_word.upper()))

    while len(letters) < 7:
        letters.append(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

    random.shuffle(letters)
    return letters, random.choice(letters)


# --- Word Check ---
def is_valid(word):
    word = word.lower()
    if len(word) < 3:
        messagebox.showinfo("Invalid", "Word must be at least 3 letters.")
        return False
    if MANDATORY_LETTER.lower() not in word:
        messagebox.showinfo("Invalid", f"Word must include the letter '{MANDATORY_LETTER}'.")
        return False
    if any(ch not in [l.lower() for l in LETTERS] for ch in word):
        messagebox.showinfo("Invalid", "Use only the given letters.")
        return False
    if word not in VALID_WORDS:
        messagebox.showinfo("Invalid", "Not a valid word.")
        return False
    if word in found_words:
        messagebox.showinfo("Oops!", "You already found this word.")
        return False
    return True


# --- Game Actions ---
def check_word():
    word = ent_word.get()
    ent_word.delete(0, tk.END)
    if is_valid(word):
        found_words.append(word)
        listbox.insert(tk.END, word)
        lbl_score.config(text=f"Score: {len(found_words)}")


def reset_game():
    global LETTERS, MANDATORY_LETTER, found_words, time_left
    found_words.clear()
    listbox.delete(0, tk.END)
    LETTERS, MANDATORY_LETTER = generate_letter_set(VALID_WORDS)
    draw_hexagons()
    lbl_score.config(text="Score: 0")
    ent_word.config(state='normal')
    btn_submit.config(state='normal')
    time_left = 60
    lbl_timer.config(text=f"Time: {time_left}s")
    update_timer()


def update_timer():
    global time_left
    if time_left > 0:
        time_left -= 1
        lbl_timer.config(text=f"Time: {time_left}s")
        root.after(1000, update_timer)
    else:
        ent_word.config(state='disabled')
        btn_submit.config(state='disabled')
        letter_set = [l.lower() for l in LETTERS]
        possible = []
        for word in VALID_WORDS:
            if len(word) >= 3 and MANDATORY_LETTER.lower() in word:
                if all(word.count(c) <= letter_set.count(c) for c in set(word)):
                    possible.append(word)
        messagebox.showinfo("Time's Up!",
                            f"Score: {len(found_words)}\nWords You Could Have Made:\n\n" + "\n".join(possible))


def click_letter(letter):
    ent_word.insert(tk.END, letter)


# --- Draw Honeycomb ---
def draw_hexagons():
    canvas.delete("all")
    hex_size = 40
    center_x, center_y = 250, 130  # Center of the canvas

    # Define positions for honeycomb layout: center + 6 surrounding hexes
    offsets = [
        (0, 0),  # Center
        (0, -hex_size * math.sqrt(3)),  # Top
        (-hex_size * 1.5, -hex_size * math.sqrt(3) / 2),  # Top-left
        (hex_size * 1.5, -hex_size * math.sqrt(3) / 2),  # Top-right
        (0, hex_size * math.sqrt(3)),  # Bottom
        (-hex_size * 1.5, hex_size * math.sqrt(3) / 2),  # Bottom-left
        (hex_size * 1.5, hex_size * math.sqrt(3) / 2)  # Bottom-right
    ]

    # Ensure there are 7 letters
    if len(LETTERS) < 7:
        while len(LETTERS) < 7:
            LETTERS.append(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

    random.shuffle(LETTERS)

    # Draw each hexagon in the correct position
    for i, (dx, dy) in enumerate(offsets):
        x = center_x + dx
        y = center_y + dy
        draw_single_hex(x, y, LETTERS[i], LETTERS[i] == MANDATORY_LETTER)


def draw_single_hex(x, y, letter, is_mandatory):
    size = 40
    points = []
    for angle in range(0, 360, 60):
        rad = math.radians(angle)
        px = x + size * math.cos(rad)
        py = y + size * math.sin(rad)
        points.extend([px, py])

    # Set colors
    color = "red" if is_mandatory else "lightblue"

    # Unique tag for this letter
    tag = f"hex_{letter}_{x}_{y}"

    # Draw hexagon and text
    canvas.create_polygon(points, fill=color, outline="black", tags=(tag,))
    canvas.create_text(x, y, text=letter, font=("Helvetica", 16, "bold"), tags=(tag,))

    # Bind click event to this hex tag
    canvas.tag_bind(tag, "<Button-1>", lambda event, l=letter: click_letter(l))


# --- Setup ---
VALID_WORDS = load_wordlist()
LETTERS, MANDATORY_LETTER = generate_letter_set(VALID_WORDS)
found_words = []
time_left = 60

# --- Window ---
root = tk.Tk()
root.title("Word Polygon")
root.geometry("500x650")
root.configure(padx=10, pady=10)

# --- Title + Timer ---
top_frame = tk.Frame(root)
top_frame.pack(fill="x")
lbl_title = tk.Label(top_frame, text="Word Polygon", font=("Helvetica", 22, "bold"))
lbl_title.pack(side="left")
lbl_timer = tk.Label(top_frame, text="Time: 60s", font=("Helvetica", 14))
lbl_timer.pack(side="right")

# --- Canvas ---
canvas = tk.Canvas(root, width=500, height=250, bg="#FFF9C4", highlightthickness=0)
canvas.pack(pady=10)

# --- Input + Submit ---
input_frame = tk.Frame(root)
input_frame.pack(pady=10)
ent_word = tk.Entry(input_frame, font=("Helvetica", 14), width=20)
ent_word.pack(side="left", padx=5)
ent_word.bind("<Return>", lambda e: check_word())
btn_submit = tk.Button(input_frame, text="Submit", font=("Helvetica", 12), command=check_word)
btn_submit.pack(side="left", padx=5)

# --- Word List ---
tk.Label(root, text="Words You Found:", font=("Helvetica", 14)).pack()
word_list_frame = tk.Frame(root)
word_list_frame.pack()
listbox = tk.Listbox(word_list_frame, font=("Helvetica", 12), width=35, height=10)
listbox.pack(side="left", pady=5)
scrollbar = tk.Scrollbar(word_list_frame, orient="vertical", command=listbox.yview)
scrollbar.pack(side="right", fill="y")
listbox.config(yscrollcommand=scrollbar.set)

# --- Score + Reset ---
lbl_score = tk.Label(root, text="Score: 0", font=("Helvetica", 14, "bold"))
lbl_score.pack(pady=5)
btn_reset = tk.Button(root, text="Restart", font=("Helvetica", 12), command=reset_game)
btn_reset.pack(pady=10)

# --- Start Game ---
draw_hexagons()
update_timer()

root.mainloop()

