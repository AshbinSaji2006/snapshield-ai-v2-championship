"""Generate the v2 Championship visuals and eight-slide presentation.

This intentionally reuses the already-reviewed v1 visual system while replacing
its paths and claims with the verified v2 evidence ledger.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "scripts" / "final_submission" / "generate_submission_assets.py"
spec = importlib.util.spec_from_file_location("snapshield_submission_visuals", SOURCE)
visuals = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(visuals)

DOCS = ROOT / "docs" / "v2"
ASSETS = DOCS / "assets"
SCREENSHOTS = ASSETS / "screenshots"
GRAPHICS = ASSETS / "graphics"
OUTPUT = ROOT / "release" / "v2_championship"
PPTX = OUTPUT / "SnapShield_AI_v2_Championship_Presentation.pptx"

visuals.DOCS = DOCS
visuals.ASSETS = ASSETS
visuals.SCREENSHOTS = SCREENSHOTS
visuals.GRAPHICS = GRAPHICS
visuals.OUTPUT = OUTPUT
visuals.PPTX = PPTX


def clean(value: str) -> str:
    """Repair inherited console-encoding artifacts and update v1 claims."""
    if value.startswith("* UCI SMS Spam Collection test set;"):
        return (
            "* Named SMS datasets: 766-message UCI test and independently deduplicated "
            "521-message 2022 Mendeley holdout. Results are not universal phishing accuracy. "
            "CPU timing is not Snapdragon performance."
        )
    substitutions = {
        "â€¢": "•",
        "â€”": "—",
        "â€“": "–",
        "TF-IDF + ONNX": "Fast + Deep ONNX",
        "The compact text component is one signal inside the full defense pipeline.":
            "Named-dataset metrics, robustness checks, and local runtime evidence.",
        "retained deduplicated messages": "deduplicated UCI messages",
        "98.17%": "94.44%",
        "held-out accuracy*": "Deep Guard recall · UCI*",
        "95.37%": "98.04%",
        "macro F1*": "Deep Guard recall · external*",
        "86.67%": "__ADAPTIVE_FPR__",
        "spam recall*": "adaptive false-positive rate · UCI*",
        "0.30%": "100",
        "false-positive rate*": "__BACKEND_TESTS__",
        "across 766 held-out samples": "on UCI + external holdouts",
        "77": "20 / 20",
        "backend tests passed": "functional robustness checks",
        "5.09 ms": "28.69 ms",
        "median full text pipeline\non current CPU": "median full deep-routed pipeline\non current CPU",
        "* UCI SMS Spam Collection test set; these metrics do not represent universal phishing detection accuracy. 5.09 ms is a development CPU measurement, not Snapdragon performance.":
            "* Named SMS datasets: 766-message UCI test and independently deduplicated 521-message 2022 Mendeley holdout. Results are not universal phishing accuracy. CPU timing is not Snapdragon performance.",
        "The compact text component is one signal inside the full defense pipeline.":
            "Independent data, adaptive routing, and real local ONNX execution.",
        "Current provider: CPUExecutionProvider": "v2 · Current provider: CPUExecutionProvider",
        "REAL DATA  •  REAL ONNX  •  REAL MULTIMODAL PIPELINE":
            "ADAPTIVE ROUTING  •  THREAT GRAPH  •  REAL MULTIMODAL PIPELINE",
        "TEXT ML": "ADAPTIVE ML",
        "RISK FUSION": "THREAT GRAPH + RISK FUSION",
    }
    for old, new in substitutions.items():
        value = value.replace(old, new)
    return value.replace("__ADAPTIVE_FPR__", "0.30%").replace(
        "__BACKEND_TESTS__", "backend tests passed"
    )


original_bitmap_text = visuals.text
def bitmap_text(draw, xy, value, size, color=visuals.WHITE, bold=False, anchor=None):
    return original_bitmap_text(draw, xy, clean(value), size, color, bold, anchor)
visuals.text = bitmap_text

original_multiline = visuals.multiline
def bitmap_multiline(draw, xy, value, size, color=visuals.WHITE, bold=False, spacing=8, anchor=None, align="left"):
    return original_multiline(draw, xy, clean(value), size, color, bold, spacing, anchor, align)
visuals.multiline = bitmap_multiline

original_add_text = visuals.add_text
def slide_text(slide, x, y, w, h, value, size, color=visuals.WHITE, bold=False,
               align=visuals.PP_ALIGN.LEFT, font_name="Segoe UI"):
    return original_add_text(slide, x, y, w, h, clean(value), size, color, bold, align, font_name)
visuals.add_text = slide_text

original_picture = visuals.add_picture
def slide_picture(slide, path, x, y, w, h):
    mapping = {
        "01_snapshield_dashboard.png": "01_command_center.png",
        "03_phishing_analysis.png": "03_phishing_analysis.png",
        "04_multimodal_screenshot_analysis.png": "04_multimodal_analysis.png",
        "08_runtime_benchmarks.png": "06_runtime_provider.png",
    }
    source = Path(path)
    candidate = source if source.exists() else SCREENSHOTS / mapping.get(source.name, source.name)
    return original_picture(slide, candidate, x, y, w, h)
visuals.add_picture = slide_picture

original_notes = visuals.set_notes
def notes(slide, note):
    return original_notes(slide, clean(note).replace(
        "Pause on 86.67% recall and acknowledge the 13.33% false-negative rate. State that 5.09 ms is a development CPU result.",
        "Contrast UCI and external Deep Guard recall, then identify the 0.30% adaptive UCI false-positive rate. State that 28.69 ms is a development CPU result.",
    ))
visuals.set_notes = notes


def main() -> None:
    GRAPHICS.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    architecture = visuals.architecture()
    architecture_v2 = GRAPHICS / "09_architecture_v2.png"
    architecture.replace(architecture_v2)
    privacy = visuals.privacy()
    privacy_v2 = GRAPHICS / "10_privacy_comparison_v2.png"
    privacy.replace(privacy_v2)
    deck = visuals.deck(architecture_v2, privacy_v2)
    print(architecture_v2)
    print(privacy_v2)
    print(deck)


if __name__ == "__main__":
    main()
