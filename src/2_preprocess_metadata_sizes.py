# preprocess_metadata_sizes.py
import json, os
import pandas as pd


META_DIR = "data/raw/metadata"
OUT_FILE = "data/processed/asin_sizes.csv"

os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)

rows = []

def safe_get(item, key):
    """
    Returns item[key]["value"] if it exists, else None.
    """
    try:
        return item[key]["value"] if item.get(key) else None
    except:
        return None

for f in os.listdir(META_DIR):
    if f.endswith(".json"):
        with open(os.path.join(META_DIR, f), "r") as fp:
            data = json.load(fp)

        for asin, item in data.get("BIN_FCSKU_DATA", {}).items():

            rows.append({
                "asin": asin,
                "height": safe_get(item, "height"),
                "width": safe_get(item, "width"),
                "length": safe_get(item, "length")
            })

df = pd.DataFrame(rows)
df = df.drop_duplicates("asin")
df.to_csv(OUT_FILE, index=False)

