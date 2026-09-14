"""Generate safe, inert demo assets. No remote content is accessed."""
from pathlib import Path
import qrcode
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
destination = root / "data" / "samples" / "demo_qr.png"
destination.parent.mkdir(parents=True, exist_ok=True)
image = qrcode.make("http://192.0.2.1:8080/verify/account/login.exe")
image.save(destination)


def font(size: int, bold: bool = False):
    candidates = [Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"), Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf")]
    match = next((path for path in candidates if path.exists()), None)
    return ImageFont.truetype(str(match), size) if match else ImageFont.load_default()


def screenshot(path: Path, include_qr: bool = False):
    canvas = Image.new("RGB", (1400, 780), "#eef3f1")
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((85, 65, 1315, 715), radius=22, fill="white", outline="#ced9d5", width=3)
    draw.text((135, 110), "State Bank of India Security Alert", font=font(42, True), fill="#172420")
    draw.text((135, 182), "To: priya@example.com", font=font(25), fill="#53635e")
    draw.line((135, 230, 1265, 230), fill="#dce5e2", width=3)
    lines = ["URGENT: Your bank account has been suspended.", "Verify your password and OTP immediately to avoid closure.", "http://192.0.2.1:8080/sbi/verify/login.exe"]
    y = 285
    for index, line in enumerate(lines):
        draw.text((135, y), line, font=font(31, index == 0), fill="#202b28")
        y += 72
    draw.rounded_rectangle((130, 545, 560, 620), radius=12, fill="#c83f49")
    draw.text((170, 563), "VERIFY ACCOUNT NOW", font=font(27, True), fill="white")
    draw.text((135, 655), "Safe synthetic competition demo - no live destination", font=font(19), fill="#73817d")
    if include_qr:
        qr = qrcode.make("http://192.0.2.1:8080/sbi/verify/login.exe").convert("RGB").resize((300, 300))
        canvas.paste(qr, (970, 340))
    canvas.save(path, optimize=True)


screenshot(root / "data" / "samples" / "demo_screenshot.png")
screenshot(root / "data" / "samples" / "demo_multimodal.png", include_qr=True)
clear = Image.open(root / "data" / "samples" / "demo_screenshot.png")
clear.resize((700, 390), Image.Resampling.LANCZOS).save(root / "data" / "samples" / "demo_low_resolution.jpg", quality=68, optimize=True)
print(root / "data" / "samples")
