**EcoCompiler**
The Clean Code Editor
Created by Shaymaa Mourchid.

(**Actual Project Duration:** June 5 2026 – September 26 2026. **GitHub Timeline Discrepancy:** The code was first initialized and pushed to GitHub on July 19. Early coding and design phases took place prior to the first GitHub commit.)

EcoCompiler is a desktop HTML editor that helps you spot common code issues, make simple fixes, and explore more thoughtful coding habits.

Selected as a featured project for the [Girls in CS 2026 Showcase.](https://girlsincs.com/showcase) 

Write or paste your HTML, check its score, review suggested improvements, and preview your page in a browser—all from one app.

> EcoCompiler is a learning tool, not a scientific carbon calculator. Its scores, energy comparisons, and CO₂ estimates are simplified examples, not measurements of a website’s actual environmental impact.

## Features

- HTML editor with line numbers and a dark background.
- Code analysis with a score out of 100 and a letter grade.
- Highlighted lines to help you find certain issues.
- Automatic fixes for some image attributes and inline styles.
- A before-and-after view of your most recent fix.
- Browser previews of your HTML.
- File tabs for HTML files in a selected folder.
- Session reports showing your best, latest, and average scores.
- Eco Coder levels that increase as you complete clean runs.

## What You Need

- Python 3 with Tkinter available.
- Pillow, the image library used for the home-screen picture.
- The project image: `plantskeyboard.webp`.
- A browser to preview your HTML.

## Setup

### 1. Save the project files

For example, save the Python code as `ecocompiler.py` and place the home-screen image beside it:

```text
EcoCompiler/
├── ecocompiler.py
└── plantskeyboard.webp
```

The app expects the image to be named exactly `plantskeyboard.webp`.

### 2. Install Pillow

```bash
python -m pip install Pillow
```

### 3. Start the app

Run this command from the project folder:

```bash
python ecocompiler.py
```

If you saved the code with a different filename, use that name instead.

## How to Use It

1. Open EcoCompiler and click **Start Coding**.
2. Write or paste HTML into the editor, or use **Select Folder** to open an existing project.
3. Click **Analyze** to see your score and suggestions.
4. Use `Fix My Code` to apply supported fixes.
5. Check `See Changes` to review the latest update.
6. Click `Run Code` to open the page in your browser.
7. Analyze again to see how your score changed.

Analysis runs when you click the button, not automatically while you type.

### Buttons

| Button | What it does |
|---|---|
| Analyze | Checks your HTML, displays a score and grade, and highlights certain issues. |
| Fix My Code | Moves supported inline styles into CSS classes and adds missing image attributes. |
| See Changes | Opens a before-and-after view of the most recent automatic fix. |
| Run Code | Writes a preview HTML file and opens it in your default browser. |
| Session Report | Shows your analysis count, best score, latest score, average score, and level. |
| Select Folder | Lists `.html` files directly inside a folder and asks whether the app may save changes to them. |
| Remove Folder | Leaves the selected folder and returns to the starter HTML. |
| Reset | Returns the editor to its starter HTML. If a file is open, asks before closing it without saving the current edits. |

## What Gets Checked?

EcoCompiler looks for:

- Image tags with neither a width nor a height.
- Inline `style` attributes.
- Image tags missing an `alt` attribute.
- Occurrences of `autoplay`.
- More than 15 opening `<div>` tags.
- The size of the HTML text.

The size check covers only the HTML in the editor—not linked images, stylesheets, scripts, or other project files.

## How Scoring Works

Each analysis starts at 100 points.

| Check | Points deducted |
|---|---:|
| Image missing both width and height | 5 per image |
| Inline style | 3 per match |
| Image missing an alt attribute | 4 per image |
| Autoplay | 10 per match |
| More than 15 opening `<div>` tags | 10 total |
| HTML text size | 0.5 per KB |

The final score is rounded and kept between 0 and 100.

| Score | Grade |
|---|---|
| 90–100 | A |
| 75–89 | B |
| 60–74 | C |
| 40–59 | D |
| 0–39 | F |

The “Carbon Meter” displays this score as a bar. It does not measure carbon emissions.

## Automatic Fixes

`Fix My Code` can:

- Replace supported double-quoted inline styles with generated CSS classes.
- Add those CSS rules to a `<style>` block inside the HTML.
- Add `width="200"` and `height="200"` when an image has neither.
- Add `alt="description"` when an image has no detected alt attribute.

Review the results before keeping them:

- Replace `description` with appropriate alt text.
- Adjust image dimensions to suit your images.
- Preview the page to check its appearance.
- Handle autoplay and excessive `<div>` usage yourself.

The app keeps generated CSS inside the HTML; it does not create a separate CSS file. Automatic fixes may increase file size, so a fix does not guarantee a smaller file or a higher score.

## Working With Files

Selecting a folder creates tabs for its `.html` files. Files inside subfolders are not listed.

If you allow saving, edits to the currently open file are saved when you:

- Switch to another file tab.
- Click `Run Code`.
- Click `Remove Folder`.

There is no separate Save button, and closing the app does not trigger a save.

If you decline saving permission, those actions will not update the original HTML file. However, `Run Code` still writes a file named `ecocompiler_preview.html` in the selected folder—or the current working folder if none is selected. An existing file with that name will be overwritten.

Keep a backup of important files before trying automatic fixes.

## Session Progress

Each analysis scoring 75 or higher counts as a clean run. Every three clean runs adds one level:

- Level 1: 0–2 clean runs.
- Level 2: 3–5 clean runs.
- Level 3: 6–8 clean runs.

Repeated analyses of the same code count. Scores and levels last only until you close the app; `Reset` does not clear them.

## Limitations

- EcoCompiler checks HTML only.
- Its checks use simple text patterns, so unusual formatting, capitalization, or multiline tags may be missed or flagged incorrectly.
- It does not fully check whether your HTML is valid.
- It counts `<div>` tags, not how deeply they are nested.
- The before-and-after highlighting may not line up perfectly when lines are added or removed.
- Energy and CO₂ estimates are illustrative and based only on changes in HTML text size.

Despite its name, EcoCompiler is an editor and checker, not an HTML compiler.
