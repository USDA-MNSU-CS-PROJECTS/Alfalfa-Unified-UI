# Alfalfa Unified UI

Central Gradio-based launcher for the three alfalfa image analysis tools
maintained under the [USDA-MNSU-CS-PROJECTS](https://github.com/USDA-MNSU-CS-PROJECTS)
organization.

This repository is a **launcher only**. It does not contain trained models or
prediction logic. Each tool runs in its own repository on its own port. The
unified UI provides one dashboard that links out to each tool.

## Related repositories

| Tool | Repository | Default port |
| --- | --- | --- |
| Object Detection — Fall 2025 | `USDA-MNSU-CS-PROJECTS/object-detection-Fall2025` | `7861` |
| Segmentation — Fall 2025 | `USDA-MNSU-CS-PROJECTS/segmentation-Fall2025` | `7860` |
| Segmentation & Ratio Analysis — Spring 2026 | `USDA-MNSU-CS-PROJECTS/segmentation-Spring2026` | `7862` |
| Unified UI (this repo) | `USDA-MNSU-CS-PROJECTS/Alfalfa-Unified-UI` | `7863` |

## Setup

```bash
git clone https://github.com/USDA-MNSU-CS-PROJECTS/Alfalfa-Unified-UI.git
cd Alfalfa-Unified-UI
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the unified UI

```bash
python3 app.py
```

The dashboard is then available at <http://127.0.0.1:7863>.

To override host or port:

```bash
HOST=0.0.0.0 PORT=7863 python3 app.py
```

`share=True` is intentionally not used. Run on a trusted network only.

## Run each individual tool first

The unified UI only links to tools that are already running locally. Start each
tool in its own terminal from its own repository before opening the dashboard.

```bash
# Fall 2025 segmentation (port 7860)
cd ../segmentation-Fall2025 && python3 app.py

# Object detection (port 7861)
cd ../object-detection-Fall2025 && python3 app.py

# Spring 2026 segmentation (port 7862)
cd ../segmentation-Spring2026 && python3 app.py
```

The exact entry filename may differ between repositories; check each repo's
README.

## Default local ports

- `7860` — Fall 2025 Segmentation
- `7861` — Object Detection
- `7862` — Spring 2026 Segmentation
- `7863` — Unified UI

## Environment variables

Override any tool URL without editing code:

| Variable | Default |
| --- | --- |
| `OBJECT_DETECTION_URL` | `http://127.0.0.1:7861` |
| `FALL_SEGMENTATION_URL` | `http://127.0.0.1:7860` |
| `SPRING_SEGMENTATION_URL` | `http://127.0.0.1:7862` |
| `HOST` | `127.0.0.1` |
| `PORT` | `7863` |

Example:

```bash
OBJECT_DETECTION_URL=http://10.0.0.5:7861 python3 app.py
```

## `start_all.sh`

`start_all.sh` is a best-effort helper that starts all four services. It
expects the four repositories to live as siblings (for example under `~/`),
and it writes per-tool logs to `logs/`.

Edit the path variables at the top of the script if your layout differs:

```bash
OBJECT_DETECTION_DIR=~/object-detection-Fall2025
FALL_SEGMENTATION_DIR=~/segmentation-Fall2025
SPRING_SEGMENTATION_DIR=~/segmentation-Spring2026
UNIFIED_UI_DIR=~/Alfalfa-Unified-UI
```

Run it with:

```bash
bash start_all.sh
```

If a tool repo uses a different entry filename, update the matching `python3
app.py` line in the script — there is a comment marking each spot.

## Troubleshooting

- **Port already in use.** Another process is bound to one of the ports. Stop
  it (`lsof -i :7863`, then `kill <pid>`) or pass a different `PORT`.
- **A tool button does not open / shows offline.** The corresponding tool is
  not running yet. Start it from its own repo, then click *Refresh Status*.
- **Dependency mismatch.** Each tool repo manages its own dependencies. Use a
  separate virtual environment per tool. This launcher only needs the
  packages in `requirements.txt`.
- **Virtual environment not activated.** Re-run `source .venv/bin/activate`
  before `pip install` or `python3 app.py`.

## Important note

This repository does not contain trained models or prediction logic. Models
and analysis code remain in their respective tool repositories. See
[`docs/architecture.md`](docs/architecture.md) for the rationale.
