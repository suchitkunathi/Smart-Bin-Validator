import os
import json
import pandas as pd
from PIL import Image
import numpy as np


IMG_DIR = "data/processed/images"
CROP_DIR = "data/crops"
META_DIR = "data/raw/metadata"
OUT_DIR = "data/crop_labeled"

os.makedirs(OUT_DIR, exist_ok=True)

asin_sizes = pd.read_csv("data/processed/asin_sizes.csv").set_index("asin")

def find_closest_asin(asins, crop_w, crop_h):
    best_asin = None
    best_score = 1e9

    for asin in asins:
        if asin not in asin_sizes.index:
            print(f"Warning: ASIN {asin} not found in size data")
            continue
            
        phys_w = asin_sizes.loc[asin, "width"]
        phys_h = asin_sizes.loc[asin, "height"]
        
        score = abs(phys_w - crop_w) + abs(phys_h - crop_h)
        if score < best_score:
            best_score = score
            best_asin = asin

    if best_asin is None:
        print(f"Warning: Could not find matching ASIN for crop size {crop_w}x{crop_h}")
        
    return best_asin

def assign_labels():
    crops = os.listdir(CROP_DIR)

    for crop_name in crops:
        img_id = crop_name.split("_crop")[0] + ".json"

        meta_file = os.path.join(META_DIR, img_id)
        if not os.path.exists(meta_file):
            continue

        meta = json.load(open(meta_file))
        asins = list(meta["BIN_FCSKU_DATA"].keys())

        if not asins:
            print(f"Warning: No ASINs found in metadata for {crop_name}")
            continue

        crop_path = os.path.join(CROP_DIR, crop_name)
        crop_img = Image.open(crop_path)

        w, h = crop_img.size

        asin = find_closest_asin(asins, w, h)
        if asin is None:
            continue

        # save into class folder
        class_dir = os.path.join(OUT_DIR, asin)
        os.makedirs(class_dir, exist_ok=True)

        crop_img.save(os.path.join(class_dir, crop_name))

        print(f"{crop_name}: → {asin}")

if __name__ == "__main__":
    assign_labels()
