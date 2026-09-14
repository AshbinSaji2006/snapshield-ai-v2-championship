"""Export the final PPTX to PDF and slide PNGs using installed PowerPoint."""
from __future__ import annotations

from pathlib import Path

import pythoncom
import win32com.client


ROOT = Path(__file__).resolve().parents[2]
RELEASE = ROOT / "release" / "final_submission"
PPTX = RELEASE / "SnapShield_AI_Final_Presentation.pptx"
PDF = RELEASE / "SnapShield_AI_Final_Presentation.pdf"
SLIDES = ROOT / "docs" / "final_submission" / "assets" / "slides"


def main():
    if not PPTX.exists():
        raise FileNotFoundError(PPTX)
    SLIDES.mkdir(parents=True, exist_ok=True)
    pythoncom.CoInitialize()
    app = win32com.client.DispatchEx("PowerPoint.Application")
    presentation = None
    try:
        app.Visible = True
        presentation = app.Presentations.Open(str(PPTX), False, False, False)
        if presentation.PageSetup.SlideWidth / presentation.PageSetup.SlideHeight < 1.77:
            raise RuntimeError("Presentation is not 16:9")
        presentation.SaveAs(str(PDF), 32)
        presentation.Export(str(SLIDES), "PNG", 1920, 1080)
        print(f"slides={presentation.Slides.Count}")
        print(PDF)
        print(SLIDES)
    finally:
        if presentation is not None:
            presentation.Close()
        app.Quit()
        pythoncom.CoUninitialize()


if __name__ == "__main__":
    main()
