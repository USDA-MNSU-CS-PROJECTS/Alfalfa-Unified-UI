# Architecture

## Why a launcher, not a merged app

The three alfalfa analysis tools were built in different semesters with
different model stacks, dependency pins, and data layouts. Merging them into
a single repository would force them to share one Python environment and one
release cycle. We deliberately avoided that.

Instead, this repository is a thin **launcher**. It runs its own Gradio app
on port `7863` and links to each tool running on its own port. Each tool
remains an independent repository with its own environment, models, and
maintainers.

### Benefits

- **No duplicated model code.** Trained weights and prediction logic stay in
  the tool repos.
- **No dependency conflicts.** Each tool can pin its own versions of
  `torch`, `ultralytics`, `opencv`, etc. The launcher only depends on
  `gradio` and `requests`.
- **Independently maintainable.** A change in one tool repo cannot break the
  others or the launcher.
- **Handover-friendly.** Future teams can replace, rename, or retire a
  single tool by changing one URL — no migration of code is required.

## Tool responsibilities

| Tool | Responsibility |
| --- | --- |
| Object Detection — Fall 2025 | Detect stem / object regions and prepare images for downstream segmentation. |
| Segmentation — Fall 2025 | Previous semester's segmentation and image-analysis workflow (lignin/pectin style analysis). |
| Segmentation & Ratio Analysis — Spring 2026 | Tissue segmentation and cross-section ratio analysis. |
| Unified UI (this repo) | Dashboard with status checks and one-click links to each tool. |

## Port map

| Port | Service |
| --- | --- |
| `7860` | Fall 2025 Segmentation |
| `7861` | Object Detection |
| `7862` | Spring 2026 Segmentation |
| `7863` | Unified UI |

URLs are configurable via environment variables (`OBJECT_DETECTION_URL`,
`FALL_SEGMENTATION_URL`, `SPRING_SEGMENTATION_URL`) so the launcher can also
point at remote hosts if a tool is deployed off-machine.

## How navigation works

The dashboard renders one card per tool. The *Open Tool* button is a plain
link to the tool's local URL (`gr.Button(link=...)`), which opens the
tool's own Gradio UI in a new tab. We avoid embedding the tools in iframes
because each Gradio app sets its own headers and assumes it owns the page.

A lightweight `requests.get` against each URL drives the *Online* / *Offline*
status pill. The check has a short timeout and silently falls back to
*Offline* on any network error, so the launcher itself is never blocked by
an unreachable tool.

## Future improvements

- **Embedded iframes.** If all three tools agree on the relevant
  `frame-ancestors` / CORS headers, individual tools could be embedded
  directly inside the launcher.
- **Automatic process management.** A small supervisor (e.g. `honcho`,
  `pm2`, or a systemd unit) could replace `start_all.sh` and restart tools
  that crash.
- **Centralized output folder.** Each tool currently writes to its own
  `outputs/`. A shared, dated output root would make multi-tool sessions
  easier to archive.
- **Shared authentication.** If the launcher is ever exposed beyond
  `127.0.0.1`, a single auth layer (e.g. an OAuth proxy in front of all
  four ports) is preferable to per-tool basic auth.
- **Shared model registry.** A common location for trained weights would
  let the tools share large checkpoints instead of each repo carrying its
  own copy.
