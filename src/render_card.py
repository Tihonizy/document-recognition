from pathlib import Path 
from PIL import Image, ImageDraw, ImageFont 

FONT_DIR = Path("/System/Library/Fonts/Supplemental")
CLASSES = ["photo", "surname", "name", "patronymic", "birth_date", "number"]

TEMPLATE = {
    "size": (856, 540),
    "background": (222, 235, 247),
    "header": (30, 70, 130),
    "title": "УДОСТОВЕРЕНИЕ ЛИЧНОСТИ · ОБРАЗЕЦ",
    "photo": (40, 120, 260, 400),
    "fields": {
        "name": ("Имя", 300, 185),
        "patronymic": ("Отчество", 300, 260),
        "birth_date": ("Дата рождения", 300, 335),
        "number": ("Номер", 300, 410),
    },
    "label_font": "Arial.ttf",
    "value_font": "Arial Bold.ttf",
}

def make_photo(size: tuple[int, int]):

    w, h = size
    photo = Image.new("RGB", size, (200, 200, 205))
    draw = ImageDraw.Draw(photo)

    draw.ellipse((0.3, * w, 0.15 * h, 0.7 * w, 0.5 * h), fill=(110, 110, 120))
    draw.ellipse((0.1 * w, 0.55 * h, 0.9 * w, 1.2 * h), fill=(110, 110, 120))

    return photo 

def render_card(person: dict, t: dict = TEMPLATE):

    card = Image.new("RGB", t["size"], t["background"])
    draw = ImageDraw.Draw(card)

    title_font = ImageFont.truetype(FONT_DIR / t["value_font"], 28)
    label_font = ImageFont.truetype(FONT_DIR / t["label_font"], 18)
    value_font = ImageFont.truetype(FONT_DIR / t["value_font"], 32)

    draw.rectangle((0, 0, t["size"][0], 80), fill=t["header"])
    draw.text((40, 40), t["title"], font=title_font, fill="white", anchor="lm")

    x0, y0, x1, y1 = t["photo"]
    card.paste(make_photo((x1 - x0), (y1 - y0)), (x0, y0))
    fields = [{"cls": "photo", "box": t["photo"], "text": None}]

    for name, (label, x, y) in t["fields"].items():

        card.paste(make_photo((x1 - x0, y1 - y0)), (x0, y0))
    fields = [{"cls": "photo", "box": t["photo"], "text": None}]

    for name, (label, x, y) in t["fields"].items():
        
        draw.text((x, y), label, font=label_font, fill=(90, 90, 90))
        value = person[name]
        draw.text((x, y + 24), value, font=value_font, fill=(20, 20, 20))

        box = draw.textbbox((x, y + 24), value, font=value_font)
        fields.append({"cls": name, "box": box, "text": value})

    return card, fields               