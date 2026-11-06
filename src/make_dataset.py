import json                               
import random                               
from pathlib import Path                    

from src.augment import augment           
from src.fake_person import random_person    
from src.render_card import CLASSES, TEMPLATES, render_card   

DATA_DIR = Path("data")                       

SPLITS = {
    "train": (1500, [0, 1, 2], 1),           
    "val": (300, [0, 1, 2], 2),               
    "test_seen": (300, [0, 1, 2], 3),      
    "test_unseen": (300, [3], 4),             
}


def yolo_line(cls_id, box, img_w, img_h):    
    x0, y0, x1, y1 = box                  
    cx = (x0 + x1) / 2 / img_w              
    cy = (y0 + y1) / 2 / img_h       
    w = (x1 - x0) / img_w                     
    h = (y1 - y0) / img_h                   
    return f"{cls_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}"   


def make_split(name, count, template_ids, seed):     
    rng = random.Random(seed)                       
    img_dir = DATA_DIR / "images" / name              
    label_dir = DATA_DIR / "labels" / name         
    img_dir.mkdir(parents=True, exist_ok=True)  
    label_dir.mkdir(parents=True, exist_ok=True)
    texts = []                                  

    for i in range(count):                         
        t = TEMPLATES[rng.choice(template_ids)]      
        card, fields = render_card(random_person(rng), t)    
        photo, fields = augment(card, fields, rng)          

        stem = f"{name}_{i:05d}"                    
        photo.save(img_dir / f"{stem}.jpg", quality=95)    
        lines = [yolo_line(CLASSES.index(f["cls"]), f["box"], *photo.size) for f in fields]   
        (label_dir / f"{stem}.txt").write_text("\n".join(lines) + "\n")   
        texts.append({"image": f"{stem}.jpg", "fields": fields})        

    with open(DATA_DIR / f"{name}.json", "w", encoding="utf-8") as f:     
        json.dump(texts, f, ensure_ascii=False)     
    print(f"{name}: {count} images")


def write_yaml():                            
    names = "\n".join(f"  {i}: {c}" for i, c in enumerate(CLASSES))   
    for test in ["test_seen", "test_unseen"]:         
        text = (f"path: {DATA_DIR.resolve()}\n"       
                "train: images/train\n"
                "val: images/val\n"
                f"test: images/{test}\n"
                f"names:\n{names}\n")
        (DATA_DIR / f"{test}.yaml").write_text(text) 


def main():
    for name, (count, template_ids, seed) in SPLITS.items():  
        make_split(name, count, template_ids, seed)
    write_yaml()


if __name__ == "__main__":
    main()