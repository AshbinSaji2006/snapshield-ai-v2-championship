"""Export the v2 Championship PPTX through installed Microsoft PowerPoint."""
from pathlib import Path

import pythoncom
import win32com.client


ROOT = Path(__file__).resolve().parents[2]
RELEASE = ROOT / "release" / "v2_championship"
PPTX = RELEASE / "SnapShield_AI_v2_Championship_Presentation.pptx"
PDF = RELEASE / "SnapShield_AI_v2_Championship_Presentation.pdf"
SLIDES = ROOT / "docs" / "v2" / "assets" / "slides"


def main() -> None:
    if not PPTX.exists():
        raise FileNotFoundError(PPTX)
    SLIDES.mkdir(parents=True, exist_ok=True)
    pythoncom.CoInitialize()
    app = win32com.client.DispatchEx("PowerPoint.Application")
    presentation = None
    try:
        presentation = app.Presentations.Open(str(PPTX), False, False, False)
        ratio = presentation.PageSetup.SlideWidth / presentation.PageSetup.SlideHeight
        if not 1.77 < ratio < 1.79:
            raise RuntimeError(f"Expected 16:9 deck, got ratio {ratio:.4f}")
        if presentation.Slides.Count != 8:
            raise RuntimeError(f"Expected 8 slides, got {presentation.Slides.Count}")
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
