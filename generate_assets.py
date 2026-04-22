from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path("assets")
OUT.mkdir(parents=True, exist_ok=True)

def vertical_gradient(size, top_color, bottom_color):
    width, height = size
    # create a 1px wide gradient then resize to the full width (fast and robust)
    gradient = Image.new("RGB", (1, height), color=0)
    draw = ImageDraw.Draw(gradient)
    for y in range(height):
        t = y / max(height - 1, 1)
        r = int(top_color[0] * (1 - t) + bottom_color[0] * t)
        g = int(top_color[1] * (1 - t) + bottom_color[1] * t)
        b = int(top_color[2] * (1 - t) + bottom_color[2] * t)
        draw.point((0, y), fill=(r, g, b))
    return gradient.resize((width, height))

def draw_centered_text(img, text, font, y):
    draw = ImageDraw.Draw(img)
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
    except AttributeError:
        w, h = draw.textsize(text, font=font)
    x = (img.width - w) // 2
    draw.text((x, y), text, font=font, fill=(255, 255, 255))

titles = ["Mystic Forge", "Void Runner", "Green Meadows", "Nightfall", "Blockscape", "Skyhaven"]
for i, t in enumerate(titles, start=1):
    top = (30, 20 + i * 10, 60)
    bottom = (20 + i * 10, 120, 60)
    img = vertical_gradient((640, 360), top, bottom)
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except Exception:
        font = ImageFont.load_default()
    draw_centered_text(img, t, font, y=260)
    img.save(OUT / f"thumb_{i}.png")

# default thumbnail
img = vertical_gradient((640, 360), (50, 50, 70), (30, 200, 120))
draw = ImageDraw.Draw(img)
try:
    font = ImageFont.truetype("arial.ttf", 20)
except Exception:
    font = ImageFont.load_default()
draw.text((20, 20), "Default Thumbnail", font=font, fill=(255, 255, 255))
img.save(OUT / "default_thumb.png")

# platform icons
platforms = {"PC": "PC", "PS5": "PS5", "XBX": "XBX", "NS": "NS"}
for name, label in platforms.items():
    ic = vertical_gradient((128, 128), (10, 10, 20), (100, 160, 60))
    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except Exception:
        font = ImageFont.load_default()
    draw = ImageDraw.Draw(ic)
    try:
        bbox = draw.textbbox((0, 0), label, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
    except AttributeError:
        w, h = draw.textsize(label, font=font)
    draw.text(((128 - w) // 2, (128 - h) // 2), label, font=font, fill=(255, 255, 255))
    ic.save(OUT / f"platform_{name}.png")

print("Assets written to assets/ (thumb_*.png, default_thumb.png, platform_*.png)")

