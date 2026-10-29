import json
import glob
import os
from parse_tg import parse_html_file

base_dir = r"C:\Users\dikan\projects\THE-REAWAKENING-PROJECT"
out_dir = os.path.join(base_dir, "knowledge-base")

# Parse 66666, 55555, 33333
sources = [
    ("66666", os.path.join(base_dir, "66666_2026-10-29")),
    ("55555", os.path.join(base_dir, "55555_2026-10-29")),
    ("33333", os.path.join(base_dir, "33333_2026-10-29"))
]

for label, folder in sources:
    html_files = sorted(glob.glob(os.path.join(folder, "messages*.html")))
    all_msgs = []
    for hf in html_files:
        msgs = parse_html_file(hf)
        all_msgs.extend(msgs)
    
    # Save per folder
    out_path = os.path.join(out_dir, f"parsed_{label}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_msgs, f, ensure_ascii=False, indent=2)
    print(f"[{label}] Processed {len(html_files)} files -> {len(all_msgs)} messages. Saved to {out_path}")
