#!/usr/bin/env bash
# start_all.sh — best-effort launcher for all four alfalfa services.
#
# Adjust the directory variables below to match your layout. The defaults
# assume the four repos live as siblings under your home directory.
#
# Usage:
#   bash start_all.sh
#
# Logs are written to ./logs/<tool>.log relative to this script.

set -u

# -----------------------------------------------------------------------------
# Paths to each repository. Edit these if your layout differs.
# -----------------------------------------------------------------------------
OBJECT_DETECTION_DIR="${OBJECT_DETECTION_DIR:-$HOME/object-detection-Fall2025}"
FALL_SEGMENTATION_DIR="${FALL_SEGMENTATION_DIR:-$HOME/segmentation-Fall2025}"
SPRING_SEGMENTATION_DIR="${SPRING_SEGMENTATION_DIR:-$HOME/segmentation-Spring2026}"
UNIFIED_UI_DIR="${UNIFIED_UI_DIR:-$(cd "$(dirname "$0")" && pwd)}"

# -----------------------------------------------------------------------------
# Port assignments. These match the unified UI defaults.
# -----------------------------------------------------------------------------
FALL_SEGMENTATION_PORT=7860
OBJECT_DETECTION_PORT=7861
SPRING_SEGMENTATION_PORT=7862
UNIFIED_UI_PORT=7863

LOG_DIR="$UNIFIED_UI_DIR/logs"
mkdir -p "$LOG_DIR"

PIDS=()

# Start a Python entry point in the background.
#   $1 = human-readable label
#   $2 = working directory
#   $3 = port
#   $4 = log filename (without directory)
#   $5 = entry file (default: app.py — adjust per repo if needed)
start_tool() {
    local label="$1"
    local dir="$2"
    local port="$3"
    local logfile="$LOG_DIR/$4"
    local entry="${5:-app.py}"

    if [[ ! -d "$dir" ]]; then
        echo "[skip] $label — directory not found: $dir"
        return 0
    fi
    if [[ ! -f "$dir/$entry" ]]; then
        echo "[skip] $label — entry file not found: $dir/$entry"
        echo "       (edit start_all.sh if this repo uses a different filename)"
        return 0
    fi

    echo "[start] $label on port $port  (log: $logfile)"
    (
        cd "$dir" && PORT="$port" python3 "$entry"
    ) >"$logfile" 2>&1 &
    PIDS+=($!)
}

# ---- Fall 2025 Segmentation -------------------------------------------------
# If this repo uses a different entry filename, change "app.py" below.
start_tool "Fall 2025 Segmentation" \
    "$FALL_SEGMENTATION_DIR" \
    "$FALL_SEGMENTATION_PORT" \
    "fall_segmentation.log" \
    "app.py"

# ---- Object Detection -------------------------------------------------------
# If this repo uses a different entry filename, change "app.py" below.
start_tool "Object Detection" \
    "$OBJECT_DETECTION_DIR" \
    "$OBJECT_DETECTION_PORT" \
    "object_detection.log" \
    "app.py"

# ---- Spring 2026 Segmentation ----------------------------------------------
# If this repo uses a different entry filename, change "app.py" below.
start_tool "Spring 2026 Segmentation" \
    "$SPRING_SEGMENTATION_DIR" \
    "$SPRING_SEGMENTATION_PORT" \
    "spring_segmentation.log" \
    "app.py"

# ---- Unified UI -------------------------------------------------------------
start_tool "Unified UI" \
    "$UNIFIED_UI_DIR" \
    "$UNIFIED_UI_PORT" \
    "unified_ui.log" \
    "app.py"

if [[ ${#PIDS[@]} -eq 0 ]]; then
    echo "No services were started. Check the directory variables at the top of this script."
    exit 1
fi

echo
echo "Started ${#PIDS[@]} process(es). PIDs: ${PIDS[*]}"
echo "Open the unified dashboard: http://127.0.0.1:$UNIFIED_UI_PORT"
echo "Tail logs with:  tail -f $LOG_DIR/*.log"
echo "Stop everything: kill ${PIDS[*]}"
