# Alfalfa Unified UI

This repository provides a centralized interface for accessing multiple alfalfa image analysis tools developed across different semesters.

## Unified UI Preview

![Unified UI Screenshot](assets/unified_ui_preview.png)

This is the main dashboard where users can select and launch different analysis tools.

## Quick Start

```bash
git clone https://github.com/USDA-MNSU-CS-PROJECTS/Alfalfa-Unified-UI.git
cd Alfalfa-Unified-UI
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
PORT=7863 python3 app.py
```

Then open <http://127.0.0.1:7863>. Tool cards will show **Offline** until each individual tool is started in its own repository — see [Running All Tools](#running-all-tools).

## Repository Structure

- `app.py` — Main Gradio application that provides the unified dashboard.
- `requirements.txt` — Contains only the dependencies required to run the unified UI.
- `start_all.sh` — Helper script to launch all related tools and the unified UI together.
- `docs/architecture.md` — Describes system design decisions and how the unified UI interacts with other tools.
- `assets/` — Contains images and documentation assets (e.g., UI screenshots).

## Integrated Tools

### Object Detection — Fall 2025
- Detects stem/object regions
- Runs on port `7861`

### Segmentation — Fall 2025
- Performs earlier segmentation workflows
- Runs on port `7860`

### Segmentation & Ratio Analysis — Spring 2026
- Performs tissue segmentation and cross-section ratio analysis
- Runs on port `7862`

Each tool runs independently in its own repository. This unified UI does not contain model code.

## How the Unified UI Works

- The UI acts as a launcher.
- It checks whether each tool is running locally.
- It provides quick access to each tool via buttons.
- It does not run models itself.

## Setup

```bash
git clone <repo>
cd Alfalfa-Unified-UI
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the Unified UI

```bash
PORT=7863 python3 app.py
```

Then open:

<http://127.0.0.1:7863>

## Running All Tools

Users must start each tool separately before using the unified UI.

- Start Fall 2025 Segmentation → port `7860`
- Start Object Detection → port `7861`
- Start Spring 2026 Segmentation → port `7862`
- Start Unified UI → port `7863`

## Tool Status

- **Online** — tool is running and reachable
- **Offline** — tool is not currently running

Offline means the individual tool is not currently running on its expected local port.

## Configuration

The following environment variables override the default tool URLs without editing code:

- `OBJECT_DETECTION_URL` — defaults to `http://127.0.0.1:7861`
- `FALL_SEGMENTATION_URL` — defaults to `http://127.0.0.1:7860`
- `SPRING_SEGMENTATION_URL` — defaults to `http://127.0.0.1:7862`

The unified UI itself binds to `127.0.0.1:7863` by default. Override with the `HOST` and `PORT` environment variables if needed.

## Project Clients

- Dr. D. Jo Heuschele — Research Agronomist, USDA ARS
- Dr. Hannah Rusch — Researcher, University of Minnesota

## Notes for Future Teams

- This repo is a launcher, not a model repo.
- Do not duplicate model code here.
- Keep tools modular.
- Update ports carefully.
- Keep UI simple and maintainable.
