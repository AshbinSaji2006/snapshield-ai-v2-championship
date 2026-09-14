"""Generate premium technical visuals and the final eight-slide PPTX."""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE, MSO_CONNECTOR
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "final_submission"
ASSETS = DOCS / "assets"
SCREENSHOTS = ASSETS / "screenshots"
GRAPHICS = ASSETS / "graphics"
OUTPUT = ROOT / "release" / "final_submission"
PPTX = OUTPUT / "SnapShield_AI_Final_Presentation.pptx"

W, H = 1920, 1080
BG = "#071014"
PANEL = "#101a1e"
PANEL_2 = "#0b1519"
LINE = "#26383c"
WHITE = "#f2f6f4"
MUTED = "#95a8a2"
MINT = "#57e0ad"
MINT_DARK = "#143b30"
AMBER = "#f3c760"
AMBER_DARK = "#3a2d13"
CORAL = "#ff6975"
CORAL_DARK = "#3b1b21"
FONT_REG = Path(r"C:\Windows\Fonts\segoeui.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\segoeuib.ttf")


def font(size: int, bold: bool = False):
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REG), size)


def hex_rgb(value: str):
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def canvas():
    image = Image.new("RGB", (W, H), BG)
    pixels = image.load()
    top = hex_rgb("#091419")
    bottom = hex_rgb("#05090c")
    for y in range(H):
        t = y / (H - 1)
        color = tuple(round(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        for x in range(W):
            pixels[x, y] = color
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((1250, -500, 2250, 500), fill=(40, 160, 120, 65))
    glow = glow.filter(ImageFilter.GaussianBlur(150))
    image = Image.alpha_composite(image.convert("RGBA"), glow)
    draw = ImageDraw.Draw(image)
    for x in range(0, W, 80):
        draw.line((x, 0, x, H), fill=(64, 93, 94, 18), width=1)
    for y in range(0, H, 80):
        draw.line((0, y, W, y), fill=(64, 93, 94, 18), width=1)
    return image, ImageDraw.Draw(image)


def rounded(draw, box, radius=22, fill=PANEL, outline=LINE, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text(draw, xy, value, size, color=WHITE, bold=False, anchor=None):
    draw.text(xy, value, font=font(size, bold), fill=color, anchor=anchor)


def multiline(draw, xy, value, size, color=WHITE, bold=False, spacing=8, anchor=None, align="left"):
    draw.multiline_text(
        xy,
        value,
        font=font(size, bold),
        fill=color,
        spacing=spacing,
        anchor=anchor,
        align=align,
    )


def arrow(draw, start, end, color=MINT, width=4):
    draw.line((*start, *end), fill=color, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    length = 13
    spread = 0.55
    left = (
        end[0] - length * math.cos(angle - spread),
        end[1] - length * math.sin(angle - spread),
    )
    right = (
        end[0] - length * math.cos(angle + spread),
        end[1] - length * math.sin(angle + spread),
    )
    draw.polygon((end, left, right), fill=color)


def dashed_round(draw, box, radius, color, width=3, dash=14, gap=9):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=radius, fill=AMBER_DARK)
    # Clean segmented edge; corners remain subtly indicated by short arcs.
    for x in range(x1 + radius, x2 - radius, dash + gap):
        draw.line((x, y1, min(x + dash, x2 - radius), y1), fill=color, width=width)
        draw.line((x, y2, min(x + dash, x2 - radius), y2), fill=color, width=width)
    for y in range(y1 + radius, y2 - radius, dash + gap):
        draw.line((x1, y, x1, min(y + dash, y2 - radius)), fill=color, width=width)
        draw.line((x2, y, x2, min(y + dash, y2 - radius)), fill=color, width=width)
    draw.arc((x1, y1, x1 + radius * 2, y1 + radius * 2), 180, 270, fill=color, width=width)
    draw.arc((x2 - radius * 2, y1, x2, y1 + radius * 2), 270, 360, fill=color, width=width)
    draw.arc((x1, y2 - radius * 2, x1 + radius * 2, y2), 90, 180, fill=color, width=width)
    draw.arc((x2 - radius * 2, y2 - radius * 2, x2, y2), 0, 90, fill=color, width=width)


def panel_title(draw, x, y, eyebrow, title_value):
    text(draw, (x, y), eyebrow.upper(), 18, MINT, True)
    text(draw, (x, y + 34), title_value, 30, WHITE, True)


def architecture():
    image, draw = canvas()
    text(draw, (70, 64), "SNAPSHIELD AI  /  SYSTEM VIEW", 17, MINT, True)
    text(draw, (70, 102), "Local-first architecture", 56, WHITE, True)
    text(draw, (70, 174), "Every verdict stays explainable. Every execution claim stays verifiable.", 23, MUTED)

    rounded(draw, (65, 245, 380, 750), 28, PANEL_2, LINE)
    panel_title(draw, 95, 277, "01 / Inputs", "Suspicious content")
    input_labels = [("MESSAGE", "Text and email"), ("URL", "Parsed, never opened"), ("SCREENSHOT", "Defensive image decode"), ("QR", "Decoded locally")]
    for index, (name, caption) in enumerate(input_labels):
        y = 372 + index * 86
        rounded(draw, (95, y, 350, y + 66), 15, PANEL, "#2c4244")
        text(draw, (118, y + 14), name, 17, WHITE, True)
        text(draw, (118, y + 39), caption, 13, MUTED)

    rounded(draw, (455, 245, 1105, 750), 28, PANEL_2, "#2b5145")
    panel_title(draw, 485, 277, "02 / Local analysis", "Specialized engines")
    engines = [
        ("TEXT ML", "TF-IDF + ONNX"),
        ("URL FORENSICS", "Structural evidence"),
        ("RAPIDOCR", "Visible text"),
        ("QR DECODER", "OpenCV local"),
        ("PII", "Detection + redaction"),
        ("BRAND", "Domain mismatch"),
        ("SECURITY RULES", "Persuasion + evasion"),
    ]
    for index, (name, caption) in enumerate(engines):
        row, col = divmod(index, 2)
        x = 485 + col * 300
        y = 372 + row * 82
        rounded(draw, (x, y, x + 275, y + 62), 14, MINT_DARK if index == 0 else PANEL, "#33715d" if index == 0 else "#2c4244")
        text(draw, (x + 17, y + 13), name, 16, MINT if index == 0 else WHITE, True)
        text(draw, (x + 17, y + 37), caption, 13, MUTED)

    rounded(draw, (1180, 245, 1855, 750), 28, PANEL_2, LINE)
    panel_title(draw, 1210, 277, "03 / Decision", "Evidence becomes action")
    outcomes = [
        ("RISK FUSION", "Bounded score + severity", CORAL_DARK, CORAL),
        ("EXPLANATION + RECOMMENDATION", "Reason • evidence • action", MINT_DARK, MINT),
        ("SANITIZED LOCAL INCIDENT STORE", "Hash + derived metadata only", PANEL, MUTED),
    ]
    for index, (name, caption, fill, accent) in enumerate(outcomes):
        y = 375 + index * 112
        rounded(draw, (1210, y, 1825, y + 82), 17, fill, accent)
        text(draw, (1236, y + 18), name, 18, WHITE, True)
        text(draw, (1236, y + 49), caption, 14, MUTED)
        if index < len(outcomes) - 1:
            arrow(draw, (1517, y + 84), (1517, y + 106), accent, 3)

    arrow(draw, (390, 500), (444, 500), MINT, 5)
    arrow(draw, (1115, 500), (1169, 500), MINT, 5)

    rounded(draw, (65, 805, 1855, 1015), 28, "#0a1317", "#304247")
    text(draw, (95, 835), "RUNTIME / HARDWARE LAYER", 17, MINT, True)
    text(draw, (95, 872), "The application reports the provider it actually selected.", 19, MUTED)
    runtime_boxes = [
        (95, 925, 375, 990, "ONNX RUNTIME", "Portable local inference", PANEL, "#3a5053"),
        (450, 925, 770, 990, "PROVIDER ABSTRACTION", "Exact artifact gate", PANEL, "#3a5053"),
        (850, 925, 1245, 990, "CPU  /  VERIFIED", "CPUExecutionProvider", MINT_DARK, MINT),
    ]
    for x1, y1, x2, y2, name, caption, fill, accent in runtime_boxes:
        rounded(draw, (x1, y1, x2, y2), 14, fill, accent)
        text(draw, (x1 + 16, y1 + 12), name, 16, WHITE, True)
        text(draw, (x1 + 16, y1 + 37), caption, 13, MUTED)
    dashed_round(draw, (1325, 925, 1825, 990), 14, AMBER)
    text(draw, (1342, 937), "QNN / SNAPDRAGON NPU", 16, WHITE, True)
    text(draw, (1342, 962), "HARDWARE VALIDATION PENDING", 13, AMBER, True)
    arrow(draw, (383, 957), (438, 957), MINT, 4)
    arrow(draw, (778, 957), (838, 957), MINT, 4)
    arrow(draw, (1253, 957), (1313, 957), AMBER, 4)

    path = GRAPHICS / "09_architecture.png"
    image.convert("RGB").save(path, quality=96)
    return path


def privacy():
    image, draw = canvas()
    text(draw, (70, 64), "SNAPSHIELD AI  /  THE PROBLEM", 17, MINT, True)
    text(draw, (70, 102), "Security AI Has a Privacy Problem", 50, WHITE, True)
    text(draw, (70, 170), "Suspicious content may itself contain private information. Local analysis narrows the trust boundary.", 21, MUTED)

    rounded(draw, (75, 255, 890, 900), 30, "#11171b", "#49343a")
    text(draw, (115, 295), "CLOUD-DEPENDENT ANALYSIS", 18, AMBER, True)
    text(draw, (115, 333), "May require remote processing", 32, WHITE, True)
    text(draw, (115, 379), "An additional network and service boundary.", 17, MUTED)
    left = [
        ("PRIVATE CONTENT", "Messages • screenshots • URLs"),
        ("INTERNET", "External transport boundary"),
        ("CLOUD AI", "Remote processing service"),
        ("RESULT", "Decision returned to the PC"),
    ]
    for index, (name, caption) in enumerate(left):
        y = 455 + index * 100
        fill = CORAL_DARK if index in {1, 2} else PANEL
        accent = CORAL if index in {1, 2} else "#44575a"
        rounded(draw, (160, y, 805, y + 68), 15, fill, accent)
        text(draw, (185, y + 13), name, 17, WHITE, True)
        text(draw, (185, y + 40), caption, 14, MUTED)
        if index < 3:
            arrow(draw, (482, y + 70), (482, y + 93), CORAL if index in {0, 1} else MUTED, 3)

    rounded(draw, (1030, 255, 1845, 900), 30, "#0c1a17", "#2f755d")
    text(draw, (1070, 295), "SNAPSHIELD CORE FLOW", 18, MINT, True)
    text(draw, (1070, 333), "Local analysis by construction", 32, WHITE, True)
    text(draw, (1070, 379), "No cloud AI or URL navigation required.", 17, MUTED)
    right = [
        ("PRIVATE CONTENT", "Explicitly submitted by the user"),
        ("LOCAL AI + SECURITY RULES", "OCR • QR • ONNX • URL • PII"),
        ("RISK + EVIDENCE + ACTION", "Explainable result on the PC"),
    ]
    for index, (name, caption) in enumerate(right):
        y = 480 + index * 126
        rounded(draw, (1115, y, 1760, y + 82), 17, MINT_DARK if index == 1 else PANEL, MINT)
        text(draw, (1142, y + 17), name, 18, WHITE, True)
        text(draw, (1142, y + 49), caption, 14, MUTED)
        if index < 2:
            arrow(draw, (1437, y + 85), (1437, y + 117), MINT, 4)

    rounded(draw, (295, 948, 1625, 1020), 20, "#0c1816", "#2e5c4d")
    text(draw, (960, 977), "SENSITIVE SECURITY CONTENT CAN STAY ON THE PC", 18, MINT, True, "mm")
    text(draw, (960, 1003), "Endpoint trust still matters.", 13, MUTED, False, "mm")

    path = GRAPHICS / "10_privacy_comparison.png"
    image.convert("RGB").save(path, quality=96)
    return path


def ppt_color(value: str):
    return RGBColor(*hex_rgb(value))


def add_rect(slide, x, y, w, h, fill=PANEL, line=LINE, radius=True):
    shape_type = MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE if radius else MSO_AUTO_SHAPE_TYPE.RECTANGLE
    shape = slide.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = ppt_color(fill)
    shape.line.color.rgb = ppt_color(line)
    shape.line.width = Pt(1)
    return shape


def add_text(slide, x, y, w, h, value, size, color=WHITE, bold=False, align=PP_ALIGN.LEFT, font_name="Segoe UI"):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = frame.margin_right = Inches(0)
    frame.margin_top = frame.margin_bottom = Inches(0)
    frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    paragraph = frame.paragraphs[0]
    paragraph.alignment = align
    run = paragraph.add_run()
    run.text = value
    run.font.name = font_name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = ppt_color(color)
    return box


def add_picture(slide, path, x, y, w, h):
    return slide.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(w), Inches(h))


def background(slide, color=BG):
    bg = slide.background
    bg.fill.solid()
    bg.fill.fore_color.rgb = ppt_color(color)


def chrome(slide, number, section):
    add_text(slide, 0.42, 0.18, 4.2, 0.24, f"SNAPSHIELD AI  /  {section.upper()}", 9, MINT, True)
    add_text(slide, 12.2, 0.18, 0.7, 0.24, f"{number:02d} / 08", 9, MUTED, True, PP_ALIGN.RIGHT)


def line(slide, x1, y1, x2, y2, color=MINT, width=2):
    shape = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    shape.line.color.rgb = ppt_color(color)
    shape.line.width = Pt(width)
    return shape


def set_notes(slide, note):
    try:
        frame = slide.notes_slide.notes_text_frame
        frame.text = note
    except Exception:
        pass


def deck(architecture_path: Path, privacy_path: Path):
    prs = Presentation()
    prs.slide_width = Inches(13.333333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # Slide 1
    slide = prs.slides.add_slide(blank)
    background(slide)
    add_text(slide, 0.55, 0.52, 4.1, 0.3, "PRIVATE • LOCAL • EXPLAINABLE", 11, MINT, True)
    add_text(slide, 0.55, 1.15, 4.2, 0.8, "SNAPSHIELD AI", 33, WHITE, True, font_name="Bahnschrift")
    add_text(slide, 0.55, 2.0, 4.15, 1.0, "Private On-Device\nMultimodal Cyber Defense", 24, WHITE, True)
    line(slide, 0.55, 3.25, 1.3, 3.25, MINT, 4)
    add_text(slide, 0.55, 3.55, 4.15, 1.42, "Your data never needs to leave your device to protect your device.", 21, WHITE, False)
    add_text(slide, 0.55, 6.62, 4.2, 0.35, "Designed for Snapdragon-powered PCs", 11, MUTED, True)
    add_text(slide, 0.55, 7.02, 4.2, 0.22, "Current provider: CPUExecutionProvider", 9, MINT, True)
    add_rect(slide, 5.2, 0.46, 7.65, 4.54, "#0d171a", "#2c5f50", False)
    add_picture(slide, SCREENSHOTS / "01_snapshield_dashboard.png", 5.35, 0.61, 7.35, 4.134)
    add_rect(slide, 5.2, 5.36, 7.65, 1.2, MINT_DARK, "#2c735c")
    add_text(slide, 5.52, 5.57, 6.95, 0.28, "REAL APPLICATION  /  LOCAL PROCESSING", 13, MINT, True)
    add_text(slide, 5.52, 5.98, 6.95, 0.3, "ONNX Runtime  •  CPUExecutionProvider  •  cloud AI disabled", 11, WHITE)
    set_notes(slide, "0:00–0:30 — Introduce SnapShield and the local-first promise. Point to Local AI active, CPUExecutionProvider, and Local processing.")

    # Slide 2
    slide = prs.slides.add_slide(blank)
    background(slide)
    add_picture(slide, privacy_path, 0, 0, 13.333333, 7.5)
    add_text(slide, 12.2, 0.18, 0.7, 0.24, "02 / 08", 9, MUTED, True, PP_ALIGN.RIGHT)
    set_notes(slide, "0:30–1:05 — Explain that suspicious content itself may contain banking context, personal details, and authentication instructions. Remote analysis adds another trust boundary.")

    # Slide 3
    slide = prs.slides.add_slide(blank)
    background(slide)
    chrome(slide, 3, "The solution")
    add_text(slide, 0.55, 0.72, 5.0, 0.95, "One local security copilot.\nMultiple threat surfaces.", 28, WHITE, True)
    add_text(slide, 0.55, 1.82, 4.7, 0.55, "MESSAGE  •  URL  •  SCREENSHOT  •  QR", 12, MINT, True)
    items = [("RISK", "A bounded evidence-weighted score"), ("EVIDENCE", "The exact signals behind the result"), ("ACTION", "A safe, practical next step")]
    for i, (title, caption) in enumerate(items):
        y = 2.58 + i * 0.92
        add_rect(slide, 0.55, y, 4.45, 0.7, MINT_DARK if i == 1 else PANEL, "#2c5f50")
        add_text(slide, 0.78, y + 0.08, 1.05, 0.24, title, 12, MINT, True)
        add_text(slide, 1.65, y + 0.08, 3.0, 0.34, caption, 12, WHITE, False)
    add_text(slide, 0.55, 5.66, 4.8, 0.35, "LOCAL-FIRST  /  MULTIMODAL  /  EXPLAINABLE", 11, WHITE, True)
    add_text(slide, 0.55, 6.1, 4.8, 0.52, "No cloud AI required • URLs parsed, never opened • raw source excluded from incident history", 10, MUTED)
    add_picture(slide, SCREENSHOTS / "03_phishing_analysis.png", 5.35, 1.08, 7.55, 4.247)
    add_rect(slide, 5.35, 5.56, 7.55, 0.86, CORAL_DARK, "#7f343e")
    add_text(slide, 5.68, 5.73, 6.9, 0.24, "REAL APP • SYNTHETIC INERT DEMO • 100 / CRITICAL", 13, CORAL, True)
    add_text(slide, 5.68, 6.05, 6.9, 0.22, "Urgency + credential request + OTP + structural URL evidence", 11, WHITE)
    set_notes(slide, "1:05–1:40 — Describe the four outputs: risk, reason, evidence, and action. Emphasize that URLs are parsed but never opened and raw source is not stored in incidents.")

    # Slide 4
    slide = prs.slides.add_slide(blank)
    background(slide)
    add_picture(slide, architecture_path, 0, 0, 13.333333, 7.5)
    add_text(slide, 12.2, 0.18, 0.7, 0.24, "04 / 08", 9, MUTED, True, PP_ALIGN.RIGHT)
    set_notes(slide, "1:40–2:25 — Walk left to right: inputs, local OCR/QR/model/rules, evidence fusion, explanation, and sanitized incident metadata. Then point to the provider rail: CPU verified; QNN hardware validation pending.")

    # Slide 5
    slide = prs.slides.add_slide(blank)
    background(slide)
    chrome(slide, 5, "Engineering evidence")
    add_text(slide, 0.55, 0.67, 8.0, 0.55, "Real Engineering Results", 30, WHITE, True)
    add_text(slide, 0.55, 1.23, 8.2, 0.35, "The compact text component is one signal inside the full defense pipeline.", 13, MUTED)
    metrics = [
        ("5,105", "retained deduplicated messages", MINT),
        ("98.17%", "held-out accuracy*", WHITE),
        ("95.37%", "macro F1*", WHITE),
        ("86.67%", "spam recall*", AMBER),
        ("0.30%", "false-positive rate*", MINT),
        ("100%", "FP32 ONNX class agreement\nacross 766 held-out samples", WHITE),
        ("77", "backend tests passed", MINT),
        ("5.09 ms", "median full text pipeline\non current CPU", WHITE),
    ]
    for index, (value, caption, accent) in enumerate(metrics):
        row, col = divmod(index, 4)
        x = 0.55 + col * 3.12
        y = 1.92 + row * 2.0
        add_rect(slide, x, y, 2.84, 1.65, PANEL, "#2a3b3f")
        add_text(slide, x + 0.22, y + 0.24, 2.38, 0.52, value, 27, accent, True, font_name="Bahnschrift")
        add_text(slide, x + 0.22, y + 0.88, 2.38, 0.5, caption, 10, MUTED)
    add_rect(slide, 0.55, 6.1, 12.23, 0.78, "#0d171a", "#33474a")
    add_text(slide, 0.8, 6.24, 11.75, 0.42, "* UCI SMS Spam Collection test set; these metrics do not represent universal phishing detection accuracy. 5.09 ms is a development CPU measurement, not Snapdragon performance.", 10, WHITE)
    set_notes(slide, "2:25–3:15 — Name the UCI SMS dataset and fixed test split before giving metrics. Pause on 86.67% recall and acknowledge the 13.33% false-negative rate. State that 5.09 ms is a development CPU result.")

    # Slide 6
    slide = prs.slides.add_slide(blank)
    background(slide)
    chrome(slide, 6, "Multimodal")
    add_text(slide, 0.55, 0.67, 5.0, 0.68, "A screenshot becomes\nsecurity evidence.", 28, WHITE, True)
    flow = [("01", "OCR", "Visible text"), ("02", "QR", "Decoded destination"), ("03", "FUSION", "Risk + action")]
    for i, (number, title, caption) in enumerate(flow):
        y = 1.82 + i * 1.15
        add_text(slide, 0.55, y, 0.45, 0.3, number, 10, MINT, True)
        add_text(slide, 1.08, y - 0.02, 1.2, 0.34, title, 16, WHITE, True)
        add_text(slide, 2.28, y - 0.02, 2.15, 0.34, caption, 12, MUTED)
        if i < 2:
            line(slide, 0.76, y + 0.4, 0.76, y + 0.92, "#34544b", 2)
    add_text(slide, 0.55, 5.35, 3.85, 0.74, "One local result correlates text, URL, QR, PII, and brand/domain evidence.", 14, WHITE, True)
    add_text(slide, 0.55, 6.28, 3.9, 0.4, "Decoded and inspected—never opened.", 10, MINT, True)
    add_picture(slide, SCREENSHOTS / "04_multimodal_screenshot_analysis.png", 4.9, 0.98, 7.97, 4.483)
    add_rect(slide, 4.9, 5.72, 7.97, 0.83, MINT_DARK, "#2c735c")
    add_text(slide, 5.18, 5.9, 7.37, 0.2, "REAL OCR TEXT  +  REAL QR PAYLOAD  +  EXPLAINABLE RISK", 13, MINT, True)
    add_text(slide, 5.18, 6.2, 7.37, 0.2, "RapidOCR ONNX Runtime • OpenCV QRCodeDetector • CPUExecutionProvider", 10, WHITE)
    set_notes(slide, "3:15–3:55 — Point to the extracted text, decoded QR payload, detected destination, and fused critical assessment. Explain that the image is synthetic and the destination is never opened.")

    # Slide 7
    slide = prs.slides.add_slide(blank)
    background(slide)
    chrome(slide, 7, "Why Snapdragon")
    add_text(slide, 0.55, 0.66, 8.0, 0.62, "Security AI belongs close to the data.", 28, WHITE, True)
    add_text(slide, 0.55, 1.3, 5.9, 0.32, "Architecture readiness and hardware proof are reported separately.", 12, MUTED)
    columns = [
        ("VERIFIED TODAY", ["ONNX Runtime", "CPUExecutionProvider", "Local inference"], MINT),
        ("IMPLEMENTED", ["Provider abstraction", "QNN execution path", "Exact-artifact gate", "QDQ candidate"], WHITE),
        ("NEXT HARDWARE STEP", ["Snapdragon NPU\nvalidation"], AMBER),
    ]
    x_positions = [0.55, 2.68, 4.85]
    widths = [1.92, 1.96, 1.73]
    for (title, bullets, accent), x, width in zip(columns, x_positions, widths):
        add_rect(slide, x, 1.92, width, 3.55, PANEL, "#2b3e42")
        add_text(slide, x + 0.18, 2.12, width - 0.36, 0.38, title, 9, accent, True)
        for i, bullet in enumerate(bullets):
            add_text(slide, x + 0.18, 2.74 + i * 0.58, width - 0.36, 0.52, f"•  {bullet}", 10, WHITE)
    add_rect(slide, 0.55, 5.77, 6.03, 0.78, AMBER_DARK, "#8c6b25")
    add_text(slide, 0.77, 5.9, 5.62, 0.5, "No NPU latency, power, or battery claim without a real compatible-device run.", 10, AMBER, True)
    add_picture(slide, SCREENSHOTS / "08_runtime_benchmarks.png", 6.83, 1.48, 5.92, 3.33)
    add_text(slide, 6.83, 5.18, 5.9, 0.38, "EXPECTED ARCHITECTURAL BENEFITS", 10, MINT, True)
    add_text(slide, 6.83, 5.64, 5.9, 0.7, "Local inference  •  offline capability\nreduced cloud dependence  •  potential efficient continuous AI", 14, WHITE, True)
    add_text(slide, 6.83, 6.55, 5.9, 0.28, "QNN hardware validation pending", 11, AMBER, True)
    set_notes(slide, "3:55–4:30 — State the current provider first: CPUExecutionProvider, not a Snapdragon NPU. Then name the concrete implemented QNN path and the next hardware validation step. Do not claim speed or efficiency.")

    # Slide 8
    slide = prs.slides.add_slide(blank)
    background(slide)
    add_text(slide, 0.67, 0.62, 5.0, 0.28, "SNAPSHIELD AI", 13, MINT, True)
    add_text(slide, 0.67, 1.32, 6.1, 1.65, "Private AI.\nLocal Security.\nDesigned for Snapdragon.", 34, WHITE, True, font_name="Bahnschrift")
    line(slide, 0.67, 3.78, 1.55, 3.78, MINT, 4)
    add_text(slide, 0.67, 4.12, 5.95, 1.15, "A future where checking whether something is dangerous does not require giving it away first.", 18, WHITE)
    add_text(slide, 0.67, 6.48, 6.2, 0.32, "REAL DATA  •  REAL ONNX  •  REAL MULTIMODAL PIPELINE", 11, MINT, True)
    add_rect(slide, 7.25, 0.5, 5.55, 3.42, "#0d171a", "#2c5f50", False)
    add_picture(slide, SCREENSHOTS / "01_snapshield_dashboard.png", 7.38, 0.63, 5.29, 2.976)
    add_rect(slide, 7.25, 4.32, 5.55, 1.5, AMBER_DARK, "#8c6b25")
    add_text(slide, 7.58, 4.55, 4.9, 0.25, "CURRENTLY VERIFIED", 10, MINT, True)
    add_text(slide, 7.58, 4.92, 4.9, 0.3, "ONNX Runtime • CPUExecutionProvider", 13, WHITE, True)
    add_text(slide, 7.58, 5.35, 4.9, 0.26, "QNN hardware validation pending", 11, AMBER, True)
    set_notes(slide, "4:30–4:55 — Close on the product promise. State that the product is proven on CPU and the next measurable step is Snapdragon hardware validation.")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    prs.core_properties.title = "SnapShield AI — Final Competition Presentation"
    prs.core_properties.subject = "Private On-Device Multimodal Cyber Defense"
    prs.core_properties.author = "SnapShield AI"
    prs.core_properties.comments = "CPUExecutionProvider verified; QNN hardware validation pending."
    prs.save(PPTX)
    return PPTX


def main():
    GRAPHICS.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    architecture_path = architecture()
    privacy_path = privacy()
    deck_path = deck(architecture_path, privacy_path)
    print(architecture_path)
    print(privacy_path)
    print(deck_path)


if __name__ == "__main__":
    main()
