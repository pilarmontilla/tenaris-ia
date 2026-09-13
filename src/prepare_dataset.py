import json
import os
import shutil
import random

# Rutas originales
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_JSON = os.path.join(BASE_DIR, "dataset/Dataset hackathon/2026.09.09 Dataset hackathon/annotations.json")
IMG_DIR = os.path.join(BASE_DIR, "dataset/Dataset hackathon/2026.09.09 Dataset hackathon/images/train")

# Destino YOLO
YOLO_DIR = os.path.join(BASE_DIR, "dataset_yolo")
# Limpiar directorio YOLO si ya existe para evitar mezclar corridas anteriores
if os.path.exists(YOLO_DIR):
    shutil.rmtree(YOLO_DIR)

for split in ["train", "val", "test"]:
    os.makedirs(os.path.join(YOLO_DIR, f"images/{split}"), exist_ok=True)
    os.makedirs(os.path.join(YOLO_DIR, f"labels/{split}"), exist_ok=True)

# Mapeo de clases
CLASS_MAP = {
    "Melted Body": 0,
    "Melted Nose": 1,
    "Flattened Nose": 2
}

def normalize_bbox(x, y, w, h, img_w, img_h):
    center_x = (x + w / 2) / img_w
    center_y = (y + h / 2) / img_h
    norm_w = w / img_w
    norm_h = h / img_h
    
    # Saneamiento (Clamping)
    center_x = max(0.0, min(1.0, center_x))
    center_y = max(0.0, min(1.0, center_y))
    norm_w = max(0.0, min(1.0, norm_w))
    norm_h = max(0.0, min(1.0, norm_h))
    
    return center_x, center_y, norm_w, norm_h

def split_3way(lst, train_ratio=0.8, val_ratio=0.1):
    """Divide una lista en Train/Val/Test asegurando balance en clases raras."""
    total = len(lst)
    if total == 0: return [], [], []
    if total == 1: return lst, [], []
    if total == 2: return lst[:1], lst[1:], []
    if total == 3: return lst[:1], lst[1:2], lst[2:]
    
    n_train = int(total * train_ratio)
    n_val = int(total * val_ratio)
    
    if n_val == 0: n_val = 1
    n_test = total - n_train - n_val
    if n_test == 0:
        n_train -= 1
        n_test = 1
        
    return lst[:n_train], lst[n_train:n_train+n_val], lst[n_train+n_val:]

def main():
    print("Cargando anotaciones...")
    with open(DATASET_JSON, 'r') as f:
        data = json.load(f)

    flattened_nose_imgs = []
    melted_nose_imgs = []
    melted_body_imgs = []
    clean_imgs = []

    for item in data:
        defects = item.get("defects", [])
        if not defects:
            clean_imgs.append(item)
        else:
            classes = [d["class"] for d in defects]
            if "Flattened Nose" in classes:
                flattened_nose_imgs.append(item)
            elif "Melted Nose" in classes:
                melted_nose_imgs.append(item)
            else:
                melted_body_imgs.append(item)

    random.seed(42)
    random.shuffle(flattened_nose_imgs)
    random.shuffle(melted_nose_imgs)
    random.shuffle(melted_body_imgs)
    random.shuffle(clean_imgs)

    # Split 80/10/10
    fn_train, fn_val, fn_test = split_3way(flattened_nose_imgs)
    mn_train, mn_val, mn_test = split_3way(melted_nose_imgs)
    mb_train, mb_val, mb_test = split_3way(melted_body_imgs)
    cl_train, cl_val, cl_test = split_3way(clean_imgs)

    train_data = fn_train + mn_train + mb_train + cl_train
    val_data = fn_val + mn_val + mb_val + cl_val
    test_data = fn_test + mn_test + mb_test + cl_test

    print(f"Total Train: {len(train_data)} | Total Val: {len(val_data)} | Total Test: {len(test_data)}")

    def process_split(split_data, split_name):
        for item in split_data:
            img_name = item["file_name"]
            img_w = item["width"]
            img_h = item["height"]
            defects = item.get("defects", [])

            src_img = os.path.join(IMG_DIR, img_name)
            dst_img = os.path.join(YOLO_DIR, f"images/{split_name}", img_name)
            if os.path.exists(src_img):
                shutil.copy(src_img, dst_img)
            else:
                continue

            txt_name = img_name.replace(".png", ".txt").replace(".jpg", ".txt")
            txt_path = os.path.join(YOLO_DIR, f"labels/{split_name}", txt_name)
            
            with open(txt_path, 'w') as f:
                for d in defects:
                    c_id = CLASS_MAP[d["class"]]
                    nx, ny, nw, nh = normalize_bbox(d["x"], d["y"], d["width"], d["height"], img_w, img_h)
                    f.write(f"{c_id} {nx:.6f} {ny:.6f} {nw:.6f} {nh:.6f}\n")

    print("Procesando Train...")
    process_split(train_data, "train")
    print("Procesando Val...")
    process_split(val_data, "val")
    print("Procesando Test local...")
    process_split(test_data, "test")

    yaml_path = os.path.join(YOLO_DIR, "dataset.yaml")
    with open(yaml_path, 'w') as f:
        f.write(f"path: {YOLO_DIR}\n")
        f.write(f"train: images/train\n")
        f.write(f"val: images/val\n")
        f.write(f"test: images/test\n\n")
        f.write(f"names:\n")
        f.write(f"  0: Melted Body\n")
        f.write(f"  1: Melted Nose\n")
        f.write(f"  2: Flattened Nose\n")
    
    print("¡Finalizado! Datos listos en formato YOLO.")

if __name__ == "__main__":
    main()

