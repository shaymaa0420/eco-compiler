#Eco-Compiler: The clean code editor!
#Designed for HTML code.
#By Shaymaa Mourchid.

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import re
import webbrowser
import tempfile
import os

#Style Colors

LIGHT_GREEN = "#DFF5E1"
MED_GREEN = "#A8D5AF"
DARK_GREEN = "#3C7A4F"
TERMINAL_GREEN = "#E8F5E9"
EDITOR_BLACK = "#1e1e1e"
TEXT_WHITE = "#FFFFFF"
TEXT_DARK = "#1e1e1e"
ERROR_RED = "#FF6B6B"

#Editor Shell

print("------")
print("Welcome to EcoCompiler!")
print("Type/paste your HTML code below, line by line")
print("Type 'analyze' on its own line to check your code's score.")
print("Type 'reset' to clear your code and start over.")
print("Type 'done' to exit.")
print("------")

code_lines = []

#Live Analysis Engine

def analyze_code(code_text):
    issues = {}
   
    issues["images_no_size"] = len(re.findall(r"<img(?![^>]*width)(?![^>]*height)[^>]*>", code_text))
    issues["inline_styles"] = len(re.findall(r'style\s*=', code_text))
    issues["missing_alt"] = len(re.findall(r"<img(?![^>]*alt=)[^>]*>", code_text))
    issues["autoplay_media"] = len(re.findall(r"autoplay", code_text))
    issues["div_count"] = len(re.findall(r"<div", code_text))
    issues["file_size_kb"] = round(len(code_text.encode("utf-8")) / 1024, 2)

    return issues

def calculate_score(issues):
    score = 100

    score -= issues["images_no_size"] * 5
    score -= issues["inline_styles"] * 3
    score -= issues["missing_alt"] * 4
    score -= issues["autoplay_media"] * 10
    score -= issues["file_size_kb"] * 0.5

    if issues["div_count"] > 15:
        score -= 10
    
    score = max(0, min(100, round(score)))
    return score

def score_to_grade(score):
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 40:
        return "D"
    else:
        return "F"

#Carbon Meter Bar

def generate_meter_bar(score):
    filled_blocks = int(score / 5)   
    # score out of 100, bar has 20 total blocks
    empty_blocks = 20 - filled_blocks
    bar = "#" * filled_blocks + "-" * empty_blocks
    return f"[{bar}] {score}%"

#Energy Waste Message

def real_world_comparison(score):
    if score >= 90:
        return "Great job! Your page is efficient, barely any wasted energy."
    elif score >= 75:
        return "Your page's extra energy use is mild (roughly like leaving a phone charger plugged in overnight.)"
    elif score >= 60:
        return "Your page's energy waste is moderate (roughly like leaving a lightbulb on for a few minutes.)"
    elif score >= 40:
        return "Your page's energy waste is high (roughly like leaving a laptop running unused for an hour.)"
    else:
        return "Your page is using a lot of unnecessary energy (roughly like leaving multiple devices charging all day for no reason.)"

#Issue Explanation

issue_explanations = {
    "images_no_size": "image(s) are missing width/height, which can slow down page loading",
    "inline_styles": "inline style attribute(s) found, external CSS is cleaner and more efficient",
    "missing_alt": "image(s) are missing an alt attribute, which also hurts accessibility",
    "autoplay_media": "autoplay media detected, this wastes energy by playing automatically",
    "div_count": "a high number of <div> tags detected, try simplifying your layout",
    "file_size_kb": "your file size is adding to the overall energy cost"
}

def generate_hints(issues):
    hints = []

    if issues["images_no_size"] > 0:
        hints.append(f"- {issues['images_no_size']} {issue_explanations['images_no_size']}")
    if issues["inline_styles"] > 0:
        hints.append(f"- {issues['inline_styles']} {issue_explanations['inline_styles']}")
    if issues["missing_alt"] > 0:
        hints.append(f"- {issues['missing_alt']} {issue_explanations['missing_alt']}")
    if issues["autoplay_media"] > 0:
        hints.append(f"- {issues['autoplay_media']} {issue_explanations['autoplay_media']}")
    if issues["div_count"] > 15:
        hints.append(f"- {issue_explanations['div_count']} ({issues['div_count']} total)")
    if issues["file_size_kb"] > 5:
        hints.append(f"- {issue_explanations['file_size_kb']} ({issues['file_size_kb']} KB)")

    if not hints:
        hints.append("No issues found! Your code looks clean.")

    return hints

#Locate Line Number for Issue

def find_issue_lines(code_text):
    line_reports = []
    error_line_numbers = []

    for index, line in enumerate(code_text.split("\n"), start=1):
        line_has_issue = False
        if re.search(r"<img(?![^>]*width)(?![^>]*height)[^>]*>", line):
            line_reports.append(f"Line {index}: image missing width/height")
            line_has_issue = True
        if re.search(r'style\s*=', line):
            line_reports.append(f"Line {index}: inline style attribute found")
            line_has_issue = True
        if re.search(r"<img(?![^>]*alt=)[^>]*>", line):
            line_reports.append(f"Line {index}: image missing alt attribute")
            line_has_issue = True
        if re.search(r"autoplay", line):
            line_reports.append(f"Line {index}: autoplay media found")
            line_has_issue = True
        if line_has_issue:
            error_line_numbers.append(index)

    return line_reports, error_line_numbers

#Auto-Rewrite Issues

def fix_code(code_text):
    fixed = code_text
    fixed = re.sub(r'\s+style="[^"]*"', '', fixed)

    def add_size(match):
        tag = match.group(0)
        if "width" not in tag and "height" not in tag:
            tag = tag[:-1] + ' width="200" height="200">'
        return tag
    fixed = re.sub(r"<img[^>]*>", add_size, fixed)

    def add_alt(match):
        tag = match.group(0)
        if "alt=" not in tag:
            tag = tag[:-1] + ' alt="description">'
        return tag
    fixed = re.sub(r"<img[^>]*>", add_alt, fixed)

    return fixed

#Eco-Score

def calculate_eco_score(before_code, after_code):
    before_kb = len(before_code.encode("utf-8")) / 1024
    after_kb = len(after_code.encode("utf-8")) / 1024
    kb_saved = round(before_kb - after_kb, 2)

    # Rough illustrative estimates for demo purposes, not scientifically precise
    energy_saved_wh = round(kb_saved * 0.0072, 4)
    co2_saved_g = round(kb_saved * 0.03, 4)

    return kb_saved, energy_saved_wh, co2_saved_g

#Session Tracker & Levels

session_history = []
clean_runs = 0

def get_current_level():
    return (clean_runs // 3) + 1
    
def update_session_stats(score):
    global clean_runs
    session_history.append(score)
    if score >= 75:
        clean_runs += 1

#Sustainability Report

def generate_session_report():
    if not session_history:
        print("\nNo analyses have been run yet this session. Type 'analyze' first!!\n")
        return
    
    best_score = max(session_history)
    latest_score = session_history[-1]
    average_score = round(sum(session_history) / len(session_history))
    level = get_current_level()

    print("\nSustainability Report\n")
    print("-----")
    print(f"-> Total analyses run: {len(session_history)}")
    print(f"Best score achieved: {best_score}/100")
    print(f"Latest score: {latest_score}/100 (Grade: {score_to_grade(latest_score)})")
    print(f"Average score: {average_score}/100")
    print(f"Current EcoCoder Level: {level}")
    print("-----")


#Main Screen Visuals

root = tk.Tk()
root.title("EcoCompiler - The Clean Code Editor!")
root.geometry("1000x750")
root.resizable(True, True)
root.configure(bg=LIGHT_GREEN)

#Home Screen

home_frame = tk.Frame(root, bg=LIGHT_GREEN)
home_frame.pack(fill="both", expand=True)

tk.Label(home_frame, text="EcoCompiler!", fg=DARK_GREEN, bg=LIGHT_GREEN, font=("Consolas", 28, "bold")).pack(pady=(0,40))
tk.Label(home_frame, text="The Eco-Friendly Code Editor", fg=DARK_GREEN, bg=LIGHT_GREEN, font=("Consolas", 14)).pack(pady=(0, 40))

def open_code_page():
    home_frame.pack_forget()
    code_page_frame.pack(fill="both", expand=True)

tk.Button(home_frame, text="Start Coding", font=("Consolas", 14, "bold"), width=20, bg=MED_GREEN, fg=TEXT_DARK, command=open_code_page).pack()

def open_instructions():
    home_frame.pack_forget()
    instructions_frame.pack(fill="both", expand=True)

tk.Button(home_frame, text="Instructions", font=("Consolas", 12, "bold"), width=20, bg=MED_GREEN, fg=TEXT_DARK, command=open_instructions).pack(pady=(10, 0))

def open_about():
    home_frame.pack_forget()
    about_frame.pack(fill="both", expand=True)

tk.Button(home_frame, text="About", font=("Consolas", 12, "bold"), width=20, bg=MED_GREEN, fg=TEXT_DARK, command=open_about).pack(pady=(10, 0))
plants_keyboard_img_raw = Image.open("plantskeyboard.webp")
plants_keyboard_img_raw = plants_keyboard_img_raw.resize((300, 200))
plants_keyboard_img = ImageTk.PhotoImage(plants_keyboard_img_raw)

tk.Label(home_frame, image=plants_keyboard_img, bg=LIGHT_GREEN).pack(pady=(20, 0))

#Instructions Screen

instructions_frame = tk.Frame(root, bg=LIGHT_GREEN)

def close_instructions():
    instructions_frame.pack_forget()
    home_frame.pack(fill="both", expand=True)

tk.Button(instructions_frame, text="< Go Back", font=("Consolas", 10, "bold"),
          bg=MED_GREEN, fg=TEXT_DARK, command=close_instructions).pack(anchor="w", padx=10, pady=10)

instructions_text = (
    "HOW TO USE ECOCOMPILER\n\n"
    "Write your code using HTML. This is the only language\n"
    "EcoCompiler currently reads and analyzes.\n\n"

    "BUTTONS:\n"
    "Analyze: scans your current code and shows a Carbon Meter,\n"
    "grade, real-world energy comparison, and specific issues found,\n"
    "including which line numbers to look at (highlighted in red).\n\n"

    "Fix My Code: automatically rewrites common issues for you,\n"
    "such as removing inline styles and adding missing image\n"
    "width/height/alt attributes. Also shows your Eco-Score —\n"
    "how much file size, energy, and CO2 were saved by the fix.\n\n"

    "See Changes: shows a before and after comparison of your code,\n"
    "with the specific lines that changed highlighted in red (before)\n"
    "and green (after).\n\n"

    "Select Folder: choose the folder where your project's image\n"
    "files are, so Run Code can find them correctly.\n\n"

    "Run Code: opens your current HTML in your default browser\n"
    "so you can check it still works after making changes.\n\n"

    "Session Report:  shows your best, latest, and average score\n"
    "across every analysis you've run this session, plus your\n"
    "current Eco Coder Level.\n\n"

    "Reset: clears the editor back to the starter code.\n\n"

    "LEVELING UP:\n"
    "Every time you click Analyze and score 75 or higher, it counts\n"
    "as a clean run.\n"
    "Level 1: starting level\n"
    "Level 2: reach 3 clean runs\n"
    "Level 3: reach 5 clean runs\n"
    "And so on!"
)

tk.Label(instructions_frame, text=instructions_text, fg=DARK_GREEN, bg=LIGHT_GREEN,
         font=("Consolas", 11), justify="left").pack(padx=30, pady=10)

#About Screen

about_frame = tk.Frame(root, bg=LIGHT_GREEN)

def close_about():
    about_frame.pack_forget()
    home_frame.pack(fill="both", expand=True)

tk.Button(about_frame, text="< Go Back", font=("Consolas", 10, "bold"),
          bg=MED_GREEN, fg=TEXT_DARK, command=close_about).pack(anchor="w", padx=10, pady=10)

about_text = (
    "WHY CLEAN CODE SAVES ENERGY\n\n"
    "Every time a website loads, data has to travel from a server\n"
    "to your device, and servers themselves use electricity to store\n"
    "and process that data. Larger, messier files mean more data\n"
    "has to be transferred and processed every single time someone\n"
    "visits a page.\n\n"
    "Common issues like oversized images, unnecessary inline styles,\n"
    "and autoplay media all increase file size and processing load,\n"
    "which increases the energy a server and a user's device must\n"
    "spend to load the page.\n\n"
    "To some, one webpage's extra energy use seems small.\n"
    "But websites are visited millions of times, and servers run\n"
    "constantly worldwide, so small inefficiencies add up into a\n"
    "significant amount of unnecessary electricity use and carbon\n"
    "emissions across the entire internet.\n\n"
    "Writing 'clean code'- code that avoids unnecessary bloat,\n"
    "properly sized images, and efficient styling- is a small,\n"
    "practical way developers can reduce that impact, one webpage\n"
    "at a time!!\n"
)

tk.Label(about_frame, text=about_text, fg=DARK_GREEN, bg=LIGHT_GREEN,
         font=("Consolas", 11), justify="left").pack(padx=30, pady=10)

#Code Page

code_page_frame = tk.Frame(root, bg=LIGHT_GREEN)

#Go Back Button

top_bar_frame = tk.Frame(code_page_frame, bg=LIGHT_GREEN)
top_bar_frame.pack(fill="x", padx=10, pady=(10, 0))

def go_back_home():
    code_page_frame.pack_forget()
    home_frame.pack(fill="both", expand=True)

tk.Button(top_bar_frame, text="< Go Back", font=("Consolas", 10, "bold"),
          bg=MED_GREEN, fg=TEXT_DARK, command=go_back_home).pack(side="left")

project_folder = None
allow_file_saving = False

folder_label = tk.Label(top_bar_frame, text="No folder selected", fg=DARK_GREEN, bg=LIGHT_GREEN,
                         font=("Consolas", 9, "italic"))
folder_label.pack(side="left", padx=15)

def select_project_folder():
    global project_folder, current_open_file, allow_file_saving
    chosen = filedialog.askdirectory(title="Select your project folder (where your images are)")
    if chosen:
        project_folder = chosen
        folder_label.config(text=f"Folder: {project_folder}")
        current_open_file = None
        code_editor.delete("1.0", "end")
        update_line_numbers()

        allow_file_saving = messagebox.askyesno(
            "Permission Needed",
            "EcoCompiler can save changes (like Fix My Code) directly back to your "
            "files when you switch tabs or run code.\n\n"
            "Allow EcoCompiler to save changes to your files in this folder?"
        )

        load_file_tabs(project_folder)

tk.Button(top_bar_frame, text="Select Folder", font=("Consolas", 10, "bold"),
          bg=MED_GREEN, fg=TEXT_DARK, command=select_project_folder).pack(side="left")

def remove_project_folder():
    global project_folder, current_open_file
    save_current_file_if_open()
    project_folder = None
    current_open_file = None
    folder_label.config(text="No folder selected")

    for widget in tabs_frame.winfo_children():
        widget.destroy()

    code_editor.delete("1.0", "end")
    code_editor.insert("1.0", starter_code)
    update_line_numbers()
    print_to_terminal("Folder removed. Back to the default EcoCompiler template.\n")

tk.Button(top_bar_frame, text="Remove Folder", font=("Consolas", 10, "bold"),
          bg=MED_GREEN, fg=TEXT_DARK, command=remove_project_folder).pack(side="left", padx=5)

#File Tabs

tabs_frame = tk.Frame(code_page_frame, bg=LIGHT_GREEN)
tabs_frame.pack(fill="x", padx=10, pady=(5, 0))

current_open_file = None

def load_file_tabs(folder):
    for widget in tabs_frame.winfo_children():
        widget.destroy()

    try:
        html_files = [f for f in os.listdir(folder)
                      if f.lower().endswith(".html") and f != "ecocompiler_preview.html"]
    except Exception as e:
        print_to_terminal(f"Could not read folder: {e}\n")
        return

    if not html_files:
        tk.Label(tabs_frame, text="No .html files found in this folder", fg=DARK_GREEN,
                 bg=LIGHT_GREEN, font=("Consolas", 9, "italic")).pack(side="left")
        return

    for filename in html_files:
        filepath = os.path.join(folder, filename)
        tk.Button(tabs_frame, text=filename, font=("Consolas", 9),
                  bg=MED_GREEN, fg=TEXT_DARK,
                  command=lambda p=filepath: open_file_in_editor(p)).pack(side="left", padx=3)

def save_current_file_if_open():
    if current_open_file and allow_file_saving:
        try:
            with open(current_open_file, "w", encoding="utf-8") as f:
                f.write(get_current_code())
        except Exception as e:
            print_to_terminal(f"Could not save {os.path.basename(current_open_file)}: {e}\n")

def open_file_in_editor(filepath):
    global current_open_file
    save_current_file_if_open()
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        code_editor.delete("1.0", "end")
        code_editor.insert("1.0", content)
        update_line_numbers()
        current_open_file = filepath
        print_to_terminal(f"Opened: {os.path.basename(filepath)}\n")
    except Exception as e:
        print_to_terminal(f"Could not open file: {e}\n")

#Editor Shell

editor_frame = tk.Frame(code_page_frame, bg=LIGHT_GREEN)
editor_frame.pack(fill="both", expand=True, padx=10, pady=(10, 5))

line_numbers = tk.Text(editor_frame, width=4, bg=EDITOR_BLACK, fg=MED_GREEN,
                        font=("Consolas", 12), state="disabled", wrap="none")
line_numbers.pack(side="left", fill="y")

code_editor = tk.Text(editor_frame, bg=EDITOR_BLACK, fg=TEXT_WHITE, insertbackground="white",
                       font=("Consolas", 12), wrap="none", undo=True, height=15)
code_editor.pack(side="left", fill="both", expand=True)

editor_scrollbar = tk.Scrollbar(editor_frame, command=code_editor.yview)
editor_scrollbar.pack(side="right", fill="y")

def on_editor_scroll(*args):
    line_numbers.yview_moveto(args[0])
    editor_scrollbar.set(*args)

code_editor.config(yscrollcommand=on_editor_scroll)

code_editor.tag_config("error_line", foreground=ERROR_RED)
code_editor.tag_config("fixed_line", foreground="#4CAF50")

last_fix_before = ""
last_fix_after = ""
last_fix_message = ""

def update_line_numbers(event=None):
    total_lines = code_editor.get("1.0", "end-1c").count("\n") + 1
    line_numbers.config(state="normal")
    line_numbers.delete("1.0", "end")
    line_numbers.insert("1.0", "\n".join(str(n) for n in range(1, total_lines + 1)))
    line_numbers.config(state="disabled")

code_editor.bind("<KeyRelease>", update_line_numbers)

starter_code = "<html>\n  <head>\n  </head>\n  <body>\n\n  </body>\n</html>"
code_editor.insert("1.0", starter_code)
update_line_numbers()

#Command Buttons
button_frame = tk.Frame(code_page_frame, bg=LIGHT_GREEN)
button_frame.pack(pady=8)

def get_current_code():
    return code_editor.get("1.0", "end-1c")

def print_to_terminal(text):
    terminal_output.config(state="normal")
    terminal_output.insert("end", text + "\n")
    terminal_output.see("end")
    terminal_output.config(state="disabled")

def highlight_error_lines(error_line_numbers):
    code_editor.tag_remove("error_line", "1.0", "end")
    for line_num in error_line_numbers:
        code_editor.tag_add("error_line", f"{line_num}.0", f"{line_num}.end")

def handle_analyze():
    current_code = get_current_code()
    issues = analyze_code(current_code)
    score = calculate_score(issues)
    grade = score_to_grade(score)
    update_session_stats(score)

    print_to_terminal("ANALYSIS RESULT")
    print_to_terminal(f"Carbon Meter: {generate_meter_bar(score)}")
    print_to_terminal(f"Grade: {grade}")
    print_to_terminal(real_world_comparison(score))
    print_to_terminal("Issues found:")
    for hint in generate_hints(issues):
        print_to_terminal(hint)
    line_reports, error_line_numbers = find_issue_lines(current_code)
    if line_reports:
        print_to_terminal("Where to look:")
        for report in line_reports:
            print_to_terminal(f"  {report}")
    highlight_error_lines(error_line_numbers)
    print_to_terminal(f"Eco Coder Level: {get_current_level()}")
    print_to_terminal("------------------------\n")

def handle_fix():
    global last_fix_before, last_fix_after, last_fix_message
    current_code = get_current_code()
    fixed_code = fix_code(current_code)

    before_lines = current_code.split("\n")
    after_lines = fixed_code.split("\n")
    changed_line_numbers = []
    for index, (before_line, after_line) in enumerate(zip(before_lines, after_lines), start=1):
        if before_line != after_line:
            changed_line_numbers.append(index)

    if not changed_line_numbers:
        remaining_issues = analyze_code(current_code)
        has_other_issues = (remaining_issues["autoplay_media"] > 0 or remaining_issues["div_count"] > 15)

        print_to_terminal("FIX MY CODE")
        if has_other_issues:
            print_to_terminal("No auto-fixable issues found (inline styles, image sizes/alt are already clean).")
            print_to_terminal("However, other issues remain that need manual fixing — click Analyze to see them.")
        else:
            print_to_terminal("No fixable issues found — your code is already clean!")
        print_to_terminal("------------------------\n")
        return

    before_issues = analyze_code(current_code)
    after_issues = analyze_code(fixed_code)

    styles_removed = before_issues["inline_styles"] - after_issues["inline_styles"]
    sizes_added = before_issues["images_no_size"] - after_issues["images_no_size"]
    alts_added = before_issues["missing_alt"] - after_issues["missing_alt"]

    fixed_parts = []
    if styles_removed > 0:
        fixed_parts.append(f"{styles_removed} inline style(s) removed")
    if sizes_added > 0:
        fixed_parts.append(f"{sizes_added} image width/height attribute(s) added")
    if alts_added > 0:
        fixed_parts.append(f"{alts_added} image alt attribute(s) added")

    unresolved_parts = []
    if after_issues["autoplay_media"] > 0:
        unresolved_parts.append(f"{after_issues['autoplay_media']} autoplay media tag(s) — not auto-fixable, remove manually")
    if after_issues["div_count"] > 15:
        unresolved_parts.append(f"{after_issues['div_count']} nested <div> tags — not auto-fixable, simplify layout manually")

    last_fix_before = current_code
    last_fix_after = fixed_code
    last_fix_message = "; ".join(fixed_parts) if fixed_parts else "Minor formatting adjustments made"

    code_editor.delete("1.0", "end")
    code_editor.insert("1.0", fixed_code)
    update_line_numbers()
    code_editor.tag_remove("error_line", "1.0", "end")
    code_editor.tag_remove("fixed_line", "1.0", "end")

    for line_num in changed_line_numbers:
        code_editor.tag_add("fixed_line", f"{line_num}.0", f"{line_num}.end")

    kb_saved, energy_saved_wh, co2_saved_g = calculate_eco_score(current_code, fixed_code)

    print_to_terminal("CODE FIXED")
    print_to_terminal(last_fix_message + ".")
    print_to_terminal(f"{len(changed_line_numbers)} line(s) updated — shown in green.")
    if unresolved_parts:
        print_to_terminal("\nStill needs manual attention:")
        for part in unresolved_parts:
            print_to_terminal(f"- {part}")
    print_to_terminal("\nECO-SCORE")
    print_to_terminal(f"File size reduced by: {kb_saved} KB")
    print_to_terminal(f"Estimated energy saved: {energy_saved_wh} Wh")
    print_to_terminal(f"Estimated CO2 reduction: {co2_saved_g} g")
    print_to_terminal("------------------------\n")

tk.Button(button_frame, text="Analyze", font=("Consolas", 11, "bold"), width=14,
          bg=MED_GREEN, fg=TEXT_DARK, command=handle_analyze).pack(side="left", padx=5)

tk.Button(button_frame, text="Fix My Code", font=("Consolas", 11, "bold"), width=14,
          bg=MED_GREEN, fg=TEXT_DARK, command=handle_fix).pack(side="left", padx=5)

def handle_see_changes():
    if not last_fix_after:
        print_to_terminal("No fixes have been applied yet. Click 'Fix My Code' first.\n")
        return

    changes_win = tk.Toplevel(root)
    changes_win.title("See Changes")
    changes_win.geometry("700x500")
    changes_win.configure(bg=LIGHT_GREEN)

    before_lines = last_fix_before.split("\n")
    after_lines = last_fix_after.split("\n")
    changed_line_numbers = []
    for index, (before_line, after_line) in enumerate(zip(before_lines, after_lines), start=1):
        if before_line != after_line:
            changed_line_numbers.append(index)

    tk.Label(changes_win, text="Most Recent Change", fg=DARK_GREEN, bg=LIGHT_GREEN,
             font=("Consolas", 13, "bold")).pack(anchor="w", padx=10, pady=(10, 0))

    tk.Label(changes_win, text="BEFORE", fg=DARK_GREEN, bg=LIGHT_GREEN,
             font=("Consolas", 11, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    before_box = tk.Text(changes_win, bg=EDITOR_BLACK, fg=TEXT_WHITE, font=("Consolas", 10), height=10)
    before_box.pack(fill="both", expand=True, padx=10)
    before_box.insert("1.0", last_fix_before)
    before_box.tag_config("changed_before", foreground=ERROR_RED)
    for line_num in changed_line_numbers:
        before_box.tag_add("changed_before", f"{line_num}.0", f"{line_num}.end")
    before_box.config(state="disabled")

    tk.Label(changes_win, text="AFTER", fg=DARK_GREEN, bg=LIGHT_GREEN,
             font=("Consolas", 11, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    after_box = tk.Text(changes_win, bg=EDITOR_BLACK, fg=TEXT_WHITE, font=("Consolas", 10), height=10)
    after_box.pack(fill="both", expand=True, padx=10)
    after_box.insert("1.0", last_fix_after)
    after_box.tag_config("changed_after", foreground="#4CAF50")
    for line_num in changed_line_numbers:
        after_box.tag_add("changed_after", f"{line_num}.0", f"{line_num}.end")
    after_box.config(state="disabled")

    tk.Label(changes_win, text=last_fix_message + ".",
             fg=DARK_GREEN, bg=LIGHT_GREEN, font=("Consolas", 10, "italic")).pack(pady=10)

    tk.Button(changes_win, text="Close", bg=MED_GREEN, fg=TEXT_DARK,
              command=changes_win.destroy).pack(pady=(0, 10))

tk.Button(button_frame, text="See Changes", font=("Consolas", 11, "bold"), width=14,
          bg=MED_GREEN, fg=TEXT_DARK, command=handle_see_changes).pack(side="left", padx=5)

def handle_run():
    save_current_file_if_open()
    current_code = get_current_code()
    try:
        if project_folder:
            target_dir = project_folder
        else:
            target_dir = os.getcwd()

        temp_path = os.path.join(target_dir, "ecocompiler_preview.html")
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(current_code)
        webbrowser.open("file://" + temp_path)
        print_to_terminal("RUNNING CODE")
        print_to_terminal(f"Opened your HTML in your default browser.")
        print_to_terminal(f"Preview saved in: {target_dir}")
        if not project_folder:
            print_to_terminal("(No folder selected... using the script's current folder.")
            print_to_terminal(" Click 'Select Folder' to point to your image files instead.)")
        print_to_terminal("------------------------\n")
    except Exception as e:
        print_to_terminal(f"Could not run code: {e}\n")

tk.Button(button_frame, text="Run Code", font=("Consolas", 11, "bold"), width=14,
          bg=MED_GREEN, fg=TEXT_DARK, command=handle_run).pack(side="left", padx=5)

def handle_report():
    if not session_history:
        print_to_terminal("No analyses have been run yet this session. Click Analyze first!\n")
        return

    best_score = max(session_history)
    latest_score = session_history[-1]
    average_score = round(sum(session_history) / len(session_history))
    level = get_current_level()

    print_to_terminal("-> SUSTAINABILITY REPORT <-")
    print_to_terminal(f"Total analyses run this session: {len(session_history)}")
    print_to_terminal(f"Best score achieved: {best_score}/100")
    print_to_terminal(f"Latest score: {latest_score}/100 (Grade: {score_to_grade(latest_score)})")
    print_to_terminal(f"Average score: {average_score}/100")
    print_to_terminal(f"Current Eco Coder Level: {level}")
    print_to_terminal("--------------------------------------\n")

tk.Button(button_frame, text="Session Report", font=("Consolas", 11, "bold"), width=14,
          bg=MED_GREEN, fg=TEXT_DARK, command=handle_report).pack(side="left", padx=5)

def handle_reset():
    global current_open_file
    if current_open_file:
        confirmed = messagebox.askyesno(
            "Close File?",
            f"This will close '{os.path.basename(current_open_file)}',"
            " and return you to the default EcoCompiler template.\n\n"
            "Your file on disk will NOT be modified. Continue?"
        )
        if not confirmed:
            print_to_terminal("Reset cancelled.\n")
            return

        current_open_file = None
        code_editor.delete("1.0", "end")
        code_editor.insert("1.0", starter_code)
        update_line_numbers()
        code_editor.tag_remove("error_line", "1.0", "end")
        code_editor.tag_remove("fixed_line", "1.0", "end")

        for widget in tabs_frame.winfo_children():
            widget.destroy()

        print_to_terminal("File closed. Your file on disk was not changed. Back to default template.\n")
    else:
        code_editor.delete("1.0", "end")
        code_editor.insert("1.0", starter_code)
        update_line_numbers()
        code_editor.tag_remove("error_line", "1.0", "end")
        code_editor.tag_remove("fixed_line", "1.0", "end")
        print_to_terminal("Code editor has been reset.\n")

tk.Button(button_frame, text="Reset", font=("Consolas", 11, "bold"), width=14,
          bg=MED_GREEN, fg=TEXT_DARK, command=handle_reset).pack(side="left", padx=5)

#Terminal Output
terminal_frame = tk.Frame(code_page_frame, bg=LIGHT_GREEN)
terminal_frame.pack(fill="both", expand=True, padx=10, pady=(5,10))
tk.Label(terminal_frame, text="Report Terminal", fg=DARK_GREEN, bg=LIGHT_GREEN, font=("Consolas", 10, "bold")).pack(anchor="w")

terminal_output = tk.Text(terminal_frame, bg=TERMINAL_GREEN, fg=TEXT_DARK, font=("Consolas", 10), height=12, state="disabled", wrap="word")
terminal_output.pack(fill="both", expand=True)

root.mainloop()