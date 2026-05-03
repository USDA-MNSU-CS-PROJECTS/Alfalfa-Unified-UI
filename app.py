"""Alfalfa Unified UI — central launcher for the three alfalfa analysis tools.

This app does not run any models. It links out to three independent Gradio
apps that run on their own local ports.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import gradio as gr
import requests


@dataclass(frozen=True)
class Tool:
    key: str
    title: str
    purpose: str
    port: int
    url: str
    repo: str
    accent: str  # CSS color for the card accent


def _env(name: str, default: str) -> str:
    value = os.environ.get(name, "").strip()
    return value or default


OBJECT_DETECTION_URL = _env("OBJECT_DETECTION_URL", "http://127.0.0.1:7861")
FALL_SEGMENTATION_URL = _env("FALL_SEGMENTATION_URL", "http://127.0.0.1:7860")
SPRING_SEGMENTATION_URL = _env("SPRING_SEGMENTATION_URL", "http://127.0.0.1:7862")

ORG = "USDA-MNSU-CS-PROJECTS"

TOOLS: list[Tool] = [
    Tool(
        key="object_detection",
        title="Object Detection — Fall 2025",
        purpose="Detect stem/object regions and prepare images for downstream analysis.",
        port=7861,
        url=OBJECT_DETECTION_URL,
        repo=f"https://github.com/{ORG}/object-detection-Fall2025",
        accent="#f5a524",  # orange/yellow
    ),
    Tool(
        key="fall_segmentation",
        title="Segmentation — Fall 2025",
        purpose="Run the Fall 2025 segmentation and analysis workflow.",
        port=7860,
        url=FALL_SEGMENTATION_URL,
        repo=f"https://github.com/{ORG}/segmentation-Fall2025",
        accent="#3ea6ff",  # blue/green
    ),
    Tool(
        key="spring_segmentation",
        title="Segmentation & Ratio Analysis — Spring 2026",
        purpose="Run tissue segmentation and cross-section ratio analysis.",
        port=7862,
        url=SPRING_SEGMENTATION_URL,
        repo=f"https://github.com/{ORG}/segmentation-Spring2026",
        accent="#2dd4bf",  # teal/green
    ),
]


def check_url(url: str, timeout: float = 1.5) -> str:
    """Return 'Online' if the URL responds, otherwise 'Offline'."""
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code < 500:
            return "Online"
        return "Offline"
    except requests.RequestException:
        return "Offline"


def _status_html(label: str) -> str:
    color = "#22c55e" if label == "Online" else "#ef4444"
    return (
        f"<span class='status-pill' style='--dot:{color}'>"
        f"<span class='status-dot'></span>{label}</span>"
    )


def refresh_statuses() -> list[str]:
    return [_status_html(check_url(t.url)) for t in TOOLS]


_PER_CARD_CSS = "\n".join(
    f"#card-{t.key} {{ --accent: {t.accent}; }}" for t in TOOLS
)

CSS = """
.gradio-container { max-width: 1200px !important; margin: 0 auto; padding-top: 14px; }
#header { padding: 4px 0 18px 0; }
#header h1 { margin: 0; font-size: 32px; letter-spacing: 0.2px; }
#header p { margin: 6px 0 0 0; opacity: 0.72; font-size: 14.5px; }

#cards-row { gap: 18px !important; margin-bottom: 14px; }

.tool-card {
    position: relative;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    padding: 28px 26px 22px 26px !important;
    background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.01)) !important;
    min-height: 270px;
    transition: transform 0.15s ease, box-shadow 0.2s ease, border-color 0.15s ease;
    overflow: hidden;
}
.tool-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: var(--accent, #888);
}
.tool-card::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: inherit;
    pointer-events: none;
    box-shadow: inset 3px 0 0 0 color-mix(in srgb, var(--accent, #888) 55%, transparent);
}
.tool-card:hover {
    border-color: color-mix(in srgb, var(--accent, #888) 45%, rgba(255,255,255,0.1)) !important;
    box-shadow: 0 10px 30px -14px color-mix(in srgb, var(--accent, #888) 70%, transparent);
    transform: translateY(-1px);
}
.tool-card h3 { margin: 0 0 10px 0; font-size: 20px; letter-spacing: 0.1px; }
.tool-card .purpose { opacity: 0.82; font-size: 14.5px; line-height: 1.55; min-height: 66px; }
.tool-card .meta {
    font-size: 12.5px; opacity: 0.6; margin: 14px 0 12px 0;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
}

.status-pill {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 12px; padding: 3px 10px; border-radius: 999px;
    background: rgba(255,255,255,0.06); margin-bottom: 10px;
}
.status-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--dot, #888); }

#refresh-row { margin: 4px 0 24px 0; }

.info-card {
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    padding: 18px 20px !important;
    background: rgba(255,255,255,0.02) !important;
    height: 100%;
}
.info-card h4 {
    margin: 0 0 10px 0; font-size: 12.5px; letter-spacing: 0.7px;
    text-transform: uppercase; opacity: 0.62;
}
.info-card p, .info-card li { font-size: 13.5px; line-height: 1.55; opacity: 0.88; }
.info-card ul, .info-card ol { margin: 0; padding-left: 18px; }
.info-card code { font-size: 12.5px; }
.info-row { gap: 16px !important; margin-bottom: 16px; }
"""


def _card(tool: Tool, status_html: str) -> gr.HTML:
    with gr.Column(elem_classes=["tool-card"], elem_id=f"card-{tool.key}"):
        gr.HTML(
            f"<h3>{tool.title}</h3>"
            f"<div class='purpose'>{tool.purpose}</div>"
            f"<div class='meta'>Port {tool.port} · {tool.url}</div>"
        )
        status = gr.HTML(status_html)
        with gr.Row():
            gr.Button("Open Tool", link=tool.url, variant="primary", size="sm")
            gr.Button("Repository", link=tool.repo, size="sm")
    return status


def _info_card(title: str, body_md: str) -> None:
    with gr.Column(elem_classes=["info-card"]):
        gr.HTML(f"<h4>{title}</h4>")
        gr.Markdown(body_md)


def build_ui() -> gr.Blocks:
    full_css = CSS + "\n" + _PER_CARD_CSS
    with gr.Blocks(title="Alfalfa Unified UI", theme=gr.themes.Base(), css=full_css) as demo:
        with gr.Column(elem_id="header"):
            gr.HTML(
                "<h1>Alfalfa Unified UI</h1>"
                "<p>Central access point for alfalfa image analysis tools.</p>"
            )

        initial = [_status_html(check_url(t.url)) for t in TOOLS]

        with gr.Row(equal_height=True, elem_id="cards-row"):
            status_components: list[gr.HTML] = [
                _card(tool, html) for tool, html in zip(TOOLS, initial)
            ]

        with gr.Row(elem_id="refresh-row"):
            refresh = gr.Button("Refresh Status", size="sm")
        refresh.click(fn=refresh_statuses, inputs=None, outputs=status_components)

        with gr.Row(equal_height=True, elem_classes=["info-row"]):
            _info_card(
                "Quick Start",
                "1. Start each individual tool in its own repo.\n"
                "2. Start this unified UI on port `7863`.\n"
                "3. Open the dashboard at <http://127.0.0.1:7863>.\n"
                "4. Use the *Open Tool* button on any card.",
            )
            _info_card(
                "Default Local Ports",
                "- `7860` — Fall 2025 Segmentation\n"
                "- `7861` — Object Detection\n"
                "- `7862` — Spring 2026 Segmentation\n"
                "- `7863` — Unified UI",
            )
        with gr.Row(equal_height=True, elem_classes=["info-row"]):
            _info_card(
                "Status Meaning",
                "- **Online** — the tool's local URL responded.\n"
                "- **Offline** means the individual tool is not currently "
                "running on its expected local port.\n\n"
                "Click *Refresh Status* after starting or stopping a tool.",
            )
            _info_card(
                "Notes for Future Teams",
                "- This repo is a launcher only — no model code lives here.\n"
                "- Tool URLs can be overridden via `OBJECT_DETECTION_URL`, "
                "`FALL_SEGMENTATION_URL`, `SPRING_SEGMENTATION_URL`.\n"
                "- Each tool stays in its own repository under "
                "[USDA-MNSU-CS-PROJECTS](https://github.com/USDA-MNSU-CS-PROJECTS).",
            )
    return demo


def main() -> None:
    host = _env("HOST", "127.0.0.1")
    port = int(_env("PORT", "7863"))
    demo = build_ui()
    demo.launch(server_name=host, server_port=port, share=False, show_api=False)


if __name__ == "__main__":
    main()
