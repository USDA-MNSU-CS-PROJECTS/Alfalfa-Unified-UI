# Alfalfa Unified UI

This repository provides a centralized interface for accessing multiple alfalfa image analysis tools developed across different semesters.

## Unified UI Preview

![Unified UI Screenshot](assets/unified_ui_preview.png)

This is the main dashboard where users can select and launch different analysis tools.

## Quick Start

# Windows Setup Guide

These instructions are intended for Windows users running the tools locally for the first time. The paths below use the example Windows username `rusch051` (used during client setup/testing). If your Windows username is different, simply replace `rusch051` with your own username in the paths.

---

## Step 1: Install Python

Download Python:

https://www.python.org/downloads/

During installation, make sure to check:

```text
Add python.exe to PATH
```

After installation, open **Command Prompt** and verify:

```cmd
python --version
```

You should see a Python version number.

---

## Step 2: Install Git

Download Git:

https://git-scm.com/download/win

After installation, verify:

```cmd
git --version
```

---

## Step 3: Create Workspace Folder

Open **Command Prompt** and run:

```cmd
cd C:\Users\rusch051
mkdir alfalfa-tools
cd alfalfa-tools
```

---

## Step 4: Clone All Repositories

Copy and paste the commands below one at a time:

```cmd
git clone https://github.com/USDA-MNSU-CS-PROJECTS/segmentation-Fall2025.git
git clone https://github.com/USDA-MNSU-CS-PROJECTS/object-detection-Fall2025.git
git clone https://github.com/USDA-MNSU-CS-PROJECTS/segmentation-Spring2026.git
git clone https://github.com/USDA-MNSU-CS-PROJECTS/Alfalfa-Unified-UI.git
```

After cloning, all repositories should now exist inside:

```text
C:\Users\rusch051\alfalfa-tools
```

---

# First-Time Setup

Each repository uses its own Python virtual environment.

You only need to complete this section once.

---

## Fall 2025 Segmentation

```cmd
cd C:\Users\rusch051\alfalfa-tools\segmentation-Fall2025
python -m venv .venv
.venv\Scripts\activate
pip install gradio ultralytics pandas openpyxl pillow
```

---

## Object Detection — Fall 2025

Open a new Command Prompt window and run:

```cmd
cd C:\Users\rusch051\alfalfa-tools\object-detection-Fall2025
python -m venv .venv
.venv\Scripts\activate
pip install -r src\app\requirements.txt
```

---

## Spring 2026 Segmentation

Open another Command Prompt window and run:

```cmd
cd C:\Users\rusch051\alfalfa-tools\segmentation-Spring2026
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Unified UI

Open another Command Prompt window and run:

```cmd
cd C:\Users\rusch051\alfalfa-tools\Alfalfa-Unified-UI
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

# Running the Applications

After the first-time setup is complete, you do NOT need to reinstall everything again.

The next time you want to use the tools, simply open Command Prompt windows and run the applications below.

---

## Open Four Command Prompt Windows

Press:

```text
Windows Key → type "cmd" → press Enter
```

Repeat four times.

---

## Window 1 — Fall 2025 Segmentation

```cmd
cd C:\Users\rusch051\alfalfa-tools\segmentation-Fall2025
.venv\Scripts\activate
set PORT=7860
python app.py
```

---

## Window 2 — Object Detection

```cmd
cd C:\Users\rusch051\alfalfa-tools\object-detection-Fall2025
.venv\Scripts\activate
cd src\app
python main.py
```

---

## Window 3 — Spring 2026 Segmentation

```cmd
cd C:\Users\rusch051\alfalfa-tools\segmentation-Spring2026
.venv\Scripts\activate
set PORT=7862
python app.py
```

---

## Window 4 — Unified UI

```cmd
cd C:\Users\rusch051\alfalfa-tools\Alfalfa-Unified-UI
.venv\Scripts\activate
set PORT=7863
python app.py
```

Then open:

```text
http://127.0.0.1:7863
```

---

# Verify the Unified UI

After opening the Unified UI:

1. Click **Refresh Status**
2. Confirm all tools display **Online**
3. Open the desired tool from the dashboard

---

# Common Issues

## Missing gradio package

If you see:

```text
ModuleNotFoundError: No module named 'gradio'
```

run:

```cmd
pip install gradio
```

inside the affected repository folder, then try running the app again.

---

## Python is not recognized

If Windows reports:

```text
python is not recognized
```

Python was likely installed without enabling PATH.

Reinstall Python and enable:

```text
Add python.exe to PATH
```

---

## Tool appears Offline

Make sure the corresponding tool is running:

```text
Fall 2025 Segmentation → 7860
Object Detection → 7861
Spring 2026 Segmentation → 7862
Unified UI → 7863
```

Then click:

```text
Refresh Status
```

inside the Unified UI.

---

# Future Deployment Note

For long-term use, these tools can also be hosted on a centralized server or USDA computing environment. Once hosted, users would only need to access a web link instead of starting all applications locally.
