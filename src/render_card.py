"""Рисует синтетическую ID-карту по шаблону и возвращает точную рамку каждого поля."""
from pathlib import Path                       
from PIL import Image, ImageDraw, ImageFont    

FONT_DIR = Path("/System/Library/Fonts/Supplemental")
CLASSES = ["photo", "surname", "name", "patronymic", "birth_date", "number"]

TEMPLATES = [                                   
    {   
        "size": (856, 540),               
        "background": (222, 235, 247),        
        "header": (30, 70, 130),              
        "title": "УДОСТОВЕРЕНИЕ ЛИЧНОСТИ · ОБРАЗЕЦ",
        "photo": (40, 120, 260, 400),      
        "fields": {                
            "surname": ("Фамилия", 300, 110),
            "name": ("Имя", 300, 185),
            "patronymic": ("Отчество", 300, 260),
            "birth_date": ("Дата рождения", 300, 335),
            "number": ("Номер", 300, 410),
        },
        "label_font": "Arial.ttf",             
        "value_font": "Arial Bold.ttf",  
        "label_size": 18,                     
        "value_size": 32,                  
        "value_offset": (0, 24),                
    },
    {   
        "size": (856, 540),
        "background": (226, 242, 228),          
        "header": (30, 110, 70),                 
        "title": "КАРТА РЕЗИДЕНТА · ОБРАЗЕЦ",
        "photo": (600, 115, 816, 385),        
        "fields": {
            "surname": ("Фамилия", 40, 110),  
            "name": ("Имя", 40, 180),
            "patronymic": ("Отчество", 40, 250),
            "birth_date": ("Дата рождения", 40, 320),
            "number": ("Номер документа", 40, 410),
        },
        "label_font": "Verdana.ttf",          
        "value_font": "Verdana Bold.ttf",
        "label_size": 16,
        "value_size": 28,
        "value_offset": (0, 22),
    },
    {    
        "size": (856, 540),
        "background": (245, 236, 220),          
        "header": (120, 70, 40),          
        "title": "ИДЕНТИФИКАЦИОННАЯ КАРТА · ОБРАЗЕЦ",
        "photo": (40, 110, 230, 350), 
        "fields": {
            "surname": ("Фамилия", 270, 105),
            "name": ("Имя", 270, 175),
            "patronymic": ("Отчество", 270, 245),
            "birth_date": ("Дата рождения", 270, 315),
            "number": ("Номер", 40, 420),    
        },
        "label_font": "Georgia.ttf",
        "value_font": "Times New Roman Bold.ttf",  
        "label_size": 18,
        "value_size": 34,
        "value_offset": (0, 22),
    },
    {  
        "size": (856, 540),
        "background": (236, 232, 242),
        "header": (70, 60, 90),
        "title": "ID CARD · SPECIMEN", 
        "photo": (620, 120, 816, 370),
        "fields": {
            "surname": ("Фамилия", 40, 130),
            "name": ("Имя", 40, 195),
            "patronymic": ("Отчество", 40, 260),
            "birth_date": ("Дата рожд.", 40, 325),
            "number": ("Номер", 40, 420),
        },
        "label_font": "Tahoma.ttf",
        "value_font": "Trebuchet MS Bold.ttf",
        "label_size": 18,
        "value_size": 32,
        "value_offset": (150, -8),       
    },
]


def make_photo(size: tuple[int, int]):         
    w, h = size                                 
    photo = Image.new("RGB", size, (200, 200, 205))   
    draw = ImageDraw.Draw(photo)         
    draw.ellipse((0.3 * w, 0.15 * h, 0.7 * w, 0.5 * h), fill=(110, 110, 120))   
    draw.ellipse((0.1 * w, 0.55 * h, 0.9 * w, 1.2 * h), fill=(110, 110, 120)) 
    return photo


def render_card(person: dict, t: dict = TEMPLATES[0]):  
    card = Image.new("RGB", t["size"], t["background"]) 
    draw = ImageDraw.Draw(card)                       

    title_font = ImageFont.truetype(FONT_DIR / t["value_font"], 28)                
    label_font = ImageFont.truetype(FONT_DIR / t["label_font"], t["label_size"])   
    value_font = ImageFont.truetype(FONT_DIR / t["value_font"], t["value_size"]) 

    draw.rectangle((0, 0, t["size"][0], 80), fill=t["header"])           
    draw.text((40, 40), t["title"], font=title_font, fill="white", anchor="lm")    

    x0, y0, x1, y1 = t["photo"]                                 
    card.paste(make_photo((x1 - x0, y1 - y0)), (x0, y0))        
    fields = [{"cls": "photo", "box": t["photo"], "text": None}]  

    dx, dy = t["value_offset"]            
    for name, (label, x, y) in t["fields"].items():                        
        draw.text((x, y), label, font=label_font, fill=(90, 90, 90)) 
        value = person[name]                                            
        draw.text((x + dx, y + dy), value, font=value_font, fill=(20, 20, 20))  
        box = draw.textbbox((x + dx, y + dy), value, font=value_font)   
        fields.append({"cls": name, "box": box, "text": value})          

    return card, fields                          