"""Читает поля документа с помощью EasyOCR и сравнивает с правильным текстом."""
import json                                
from pathlib import Path           

import numpy as np                      
import pandas as pd                         
from PIL import Image                      

from src.metrics import cer                   

DATA_DIR = Path("data")                    


def crop_field(image, box, pad=4):          
    x0, y0, x1, y1 = box              
    return image.crop((x0 - pad, y0 - pad, x1 + pad, y1 + pad))   


def read_field(reader, crop, mode="recognize"):   
    array = np.asarray(crop)           
    if mode == "recognize":                   
        parts = reader.recognize(array, detail=0)
    else:                                  
        parts = reader.readtext(array, detail=0)
    return " ".join(parts).strip()    


def best_boxes(detector, image, device="mps"):    
    result = detector.predict(image, conf=0.25, device=device, verbose=False)[0]  

    found = zip(result.boxes.cls.tolist(), result.boxes.conf.tolist(), result.boxes.xyxy.tolist())
    boxes = {}                            
    for cls_id, conf, box in sorted(found, key=lambda x: -x[1]):  
        name = result.names[int(cls_id)]  
        if name not in boxes:               
            boxes[name] = box
    return boxes


def evaluate(reader, split, n_images=100, detector=None, mode="recognize"):   
    items = json.loads((DATA_DIR / f"{split}.json").read_text(encoding="utf-8"))[:n_images] 
    rows = []                       
    for item in items:                   
        image = Image.open(DATA_DIR / "images" / split / item["image"])  
        boxes = best_boxes(detector, image) if detector else None 
        for field in item["fields"]:        
            if field["text"] is None:        
                continue 

            box = boxes.get(field["cls"]) if detector else field["box"]
            pred = read_field(reader, crop_field(image, box), mode) if box else ""   
            rows.append({"image": item["image"], "cls": field["cls"], "true": field["text"],
                         "pred": pred, "cer": cer(pred, field["text"])})
    return pd.DataFrame(rows)          