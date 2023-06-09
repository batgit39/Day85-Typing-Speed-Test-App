import csv
import random
import tkinter as tk
from tkinter import ttk

BG_COLOR = "#F1DDBF"
TEXT_COLOR = "#78938A"
TEST_TEXT_COLOR = "#DE8971"

BUTTON_COLORS = {
    "15": "#B6E2A1",
    "30": "#FCDDB0",
    "60": "#E97777"
}

RANDOM_SENTENCE = ""
CURRENT_INDEX = 0

total_words_typed = 0
correct_words = 0
wrong_words = 0

timer = None
start_button = None
reset_button = None

def main_window():
    window = tk.Tk()
    window.geometry("800x600")
    window.configure(bg=BG_COLOR)

    style = ttk.Style()
    style.theme_use("default")

    text = "Speed Test"
    font_style = ("Arial", 84, "bold")

    style.configure("Title.TLabel", font=font_style, background=BG_COLOR, foreground=TEXT_COLOR)

    style.configure("TestText.TLabel", font=("Arial", 14), background=BG_COLOR,
                    foreground=TEST_TEXT_COLOR, wraplength=700)

    label = ttk.Label(window, style="Title.TLabel", text=text)
    label.pack(pady=50)

    button_frame = ttk.Frame(window, style="ButtonFrame.TFrame")
    button_frame.pack()
    style.configure("ButtonFrame.TFrame", background=BG_COLOR)

    def start_test(level):
        window.destroy()
        test(level)

    for level, color in BUTTON_COLORS.items():
        style_name = f"{level}.TButton"
        style.configure(style_name, background=color, padding=10)
        button = ttk.Button(button_frame, text=level, style=style_name, command=lambda lvl=level: start_test(lvl))
        button.pack(side="left", padx=30)

    window.mainloop()

def get_random_sentence():
    global RANDOM_SENTENCE
    word_list = []

    with open("top_300_words.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            word_list.append(row[0])

    random_words = random.sample(word_list, 80)

    sentence_parts = [random_words[i:i + 8] for i in range(0, len(random_words), 10)]
    formatted_parts = [" ".join(part) for part in sentence_parts]
    formatted_sentence = "\n".join(formatted_parts)

    RANDOM_SENTENCE = formatted_sentence


def check_input(event, window, input_entry, section):
    global CURRENT_INDEX, correct_words, wrong_words, total_words_typed

    user_input = input_entry.get().replace(" ", "")
    input_entry.delete(0, "end")

    total_words_typed += 1
    current_section_words = RANDOM_SENTENCE.split()[CURRENT_INDEX:CURRENT_INDEX + 8]

    if user_input in current_section_words:
        CURRENT_INDEX += 1
        if CURRENT_INDEX >= len(RANDOM_SENTENCE.split()):
            print("End of sentence")
            window.unbind("<space>")
    else:
        wrong_words += 1
        print("Incorrect input")
        current_word = RANDOM_SENTENCE.split()[CURRENT_INDEX]
        start_index = section.search(current_word, "1.0", stopindex="end", count=tk.IntVar(), regexp=True)
        if start_index:
            end_index = f"{start_index}+{len(current_word)}c"
            section.tag_add("incorrect", start_index, end_index)
            section.tag_config("incorrect", foreground="red")

    if user_input == RANDOM_SENTENCE.split()[CURRENT_INDEX - 1]:
        correct_words += 1
        section.configure(state="normal")
        current_word = RANDOM_SENTENCE.split()[CURRENT_INDEX - 1]
        start_index = section.search(current_word, "1.0", stopindex="end", count=tk.IntVar(), regexp=True)
        if start_index:
            end_index = f"{start_index}+{len(current_word)}c"
            section.tag_add("correct", start_index, end_index)
            section.tag_config("correct", foreground="green")

def test(level):
    level = int(level)
    get_random_sentence()

    window = tk.Tk()
    window.geometry("800x600")
    window.configure(bg=BG_COLOR)

    style = ttk.Style()
    style.theme_use("default")

    label_font = ("Arial", 20, "bold")

    wpm_label = ttk.Label(window, text="WPM: ?", font=label_font, background=BG_COLOR, foreground=TEXT_COLOR)
    wpm_label.place(x=10, y=10)

    accuracy_label = ttk.Label(window, text="Accuracy: ?", font=label_font, background=BG_COLOR, foreground=TEXT_COLOR)
    accuracy_label.place(x=10, y=50)

    raw_label = ttk.Label(window, text="Raw: ?", font=label_font, background=BG_COLOR, foreground=TEXT_COLOR)
    raw_label.place(x=600, y=10)

    time_label = ttk.Label(window, text="Time:", font=label_font, background=BG_COLOR, foreground=TEXT_COLOR)
    time_label.place(x=600, y=50)

    section = tk.Text(window, font=("Arial", 20), wrap="word", bg="#C3AED6")
    section.place(relx=0.5, rely=0.5, anchor="center", y=-40, width=700, height=300)
    input_entry = ttk.Entry(window, font=("Arial", 14))

    def run_test():
        section.insert("1.0", RANDOM_SENTENCE)
        section.tag_configure("incorrect", foreground="red")
        section.tag_configure("correct", foreground="green")

        input_entry.place(relx=0.5, rely=0.5, anchor="center", y=80)
        input_entry.focus()

        window.bind("<space>", lambda event: check_input(event, window, input_entry, section))

    def reset_test():
        global CURRENT_INDEX, correct_words, wrong_words, total_words_typed
        total_words_typed = 1
        correct_words = 0
        wrong_words = 0
        CURRENT_INDEX = 0
        stop_timer()
        total_words_typed = 0
        correct_words = 0
        wrong_words = 0
        CURRENT_INDEX = 0

        get_random_sentence()
        start_button.config(state="normal")
        input_entry.config(state="disabled")
        section.tag_remove("correct", "1.0", "end")
        section.tag_remove("incorrect", "1.0", "end")
        section.delete("1.0", "end")
        start_test()

    def start_test():
        countdown(level)
        run_test()
        input_entry.config(state="normal")
        input_entry.delete(0, "end")
        input_entry.focus()
        section.delete("1.0", "end")
        section.insert("1.0", RANDOM_SENTENCE)
        window.bind("<space>", lambda event: check_input(event, window, input_entry, section))

    global start_button, reset_button

    button_frame = ttk.Frame(window, style="ButtonFrame.TFrame")
    button_frame.place(relx=0.5, rely=0.5, anchor="center", y=200)
    style.configure("ButtonFrame.TFrame", background=BG_COLOR)

    start_button = ttk.Button(button_frame, text="Start", style="Start.TButton", command=start_test)
    start_button.pack(side="left", padx=20)

    reset_button = ttk.Button(button_frame, text="Reset", style="Reset.TButton", command=reset_test)
    reset_button.pack(side="left", padx=20)

    def countdown(time):
        global timer, correct_words, wrong_words

        if time > 0:
            timer = window.after(1000, countdown, time - 1)
            if time < 10:
                time = f"0{time}"
            time_label["text"] = f"Time: {time}"
            window.bind("<space>")
        else:
            stop_timer()

    def stop_timer():
        window.config(bg=BG_COLOR)
        window.unbind("<space>")
        show_results()
        window.after_cancel(timer)
        input_entry.config(state="disabled")

    def show_results():
        time_label["text"] = f"Time: {level}"
        accuracy_label["text"] = f"Accuracy: {(correct_words / total_words_typed * 100):.2f}%"
        wpm_label["text"] = f"WPM: {calculate_wpm()}"
        raw_label["text"] = f"Raw: {total_words_typed}"

    def calculate_wpm():
        elapsed_time = level
        seconds_per_minute = 60
        words_per_minute = (correct_words / elapsed_time) * seconds_per_minute
        return round(words_per_minute)

    style.configure(
        "Start.TButton",
        background="#B6E2A1",
        padding=10
    )

    style.configure(
        "Reset.TButton",
        background="#FCDDB0",
        padding=10
    )
    window.mainloop()


main_window()

