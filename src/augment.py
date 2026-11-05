import math                

import cv2                  
import numpy as np             
from PIL import Image       

OUT_W, OUT_H = 960, 720 


def random_background(rng, w, h):  
    c1 = np.array([rng.randrange(40, 220) for _ in range(3)], dtype=np.float32) 
    c2 = np.array([rng.randrange(40, 220) for _ in range(3)], dtype=np.float32) 
    t = np.linspace(0, 1, w, dtype=np.float32)[None, :, None]   
    bg = c1 * (1 - t) + c2 * t  
    return np.repeat(bg, h, axis=0)                     


def random_corners(rng, card_w, card_h):  
    scale = rng.uniform(0.55, 0.75) * OUT_W / card_w  
    w, h = card_w * scale, card_h * scale               
    cx = OUT_W / 2 + rng.uniform(-0.05, 0.05) * OUT_W    
    cy = OUT_H / 2 + rng.uniform(-0.05, 0.05) * OUT_H
    angle = math.radians(rng.uniform(-10, 10))           
    jitter = 0.05 * w                                
    corners = []                                        

    for sx, sy in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
        x, y = sx * w / 2, sy * h / 2                  
        xr = x * math.cos(angle) - y * math.sin(angle)   
        yr = x * math.sin(angle) + y * math.cos(angle) 
        corners.append((cx + xr + rng.uniform(-jitter, jitter), cy + yr + rng.uniform(-jitter, jitter)))
    return np.float32(corners)                       


def move_box(box, M):  
    x0, y0, x1, y1 = box                
    pts = np.float32([[[x0, y0], [x1, y0], [x1, y1], [x0, y1]]])   
    pts = cv2.perspectiveTransform(pts, M)[0]              
    return (float(pts[:, 0].min()), float(pts[:, 1].min()), float(pts[:, 0].max()), float(pts[:, 1].max()))


def add_glare(img, rng):           
    yy, xx = np.mgrid[0:OUT_H, 0:OUT_W]                        
    cx, cy = rng.uniform(0, OUT_W), rng.uniform(0, OUT_H)   
    rx, ry = rng.uniform(60, 200), rng.uniform(40, 140)     
    strength = rng.uniform(80, 200)                     
    glare = strength * np.exp(-(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2))
    return img + glare[..., None]                           


def augment(card, fields, rng):            
    card_w, card_h = card.size                               
    src = np.float32([[0, 0], [card_w, 0], [card_w, card_h], [0, card_h]])  
    dst = random_corners(rng, card_w, card_h)            
    M = cv2.getPerspectiveTransform(src, dst)                 

    card_np = np.asarray(card, dtype=np.float32)            
    warped = cv2.warpPerspective(card_np, M, (OUT_W, OUT_H))   
    ones = np.ones((card_h, card_w), np.float32)           
    mask = cv2.warpPerspective(ones, M, (OUT_W, OUT_H))[..., None]    
    img = random_background(rng, OUT_W, OUT_H) * (1 - mask) + warped * mask   

    img = img * rng.uniform(0.7, 1.2) + rng.uniform(-30, 30)    
    if rng.random() < 0.5:                                   
        img = add_glare(img, rng)                            
    if rng.random() < 0.5:                              
        img = cv2.GaussianBlur(img, (0, 0), rng.uniform(0.5, 2.0)) 
    np_rng = np.random.default_rng(rng.randrange(2**32))     
    img = img + np_rng.normal(0, rng.uniform(2, 12), img.shape)     
    img = np.clip(img, 0, 255).astype(np.uint8)              

    quality = rng.randrange(30, 95)                             
    _, jpg = cv2.imencode(".jpg", img[..., ::-1], [cv2.IMWRITE_JPEG_QUALITY, quality])   
    img = cv2.imdecode(jpg, cv2.IMREAD_COLOR)[..., ::-1]        

    new_fields = [{**f, "box": move_box(f["box"], M)} for f in fields]   
    return Image.fromarray(img), new_fields  