import json
import re
from collections import Counter

with open(r"C:\Users\dikan\projects\THE-REAWAKENING-PROJECT\knowledge-base\parsed_66666.json", encoding="utf-8") as f:
    msgs = json.load(f)

# Sort by length or substantive content
long_msgs = [m for m in msgs if len(m['text']) > 150]

with open(r"C:\Users\dikan\projects\THE-REAWAKENING-PROJECT\knowledge-base\analysis_66666_overview.txt", "w", encoding="utf-8") as out:
    out.write(f"Total msgs: {len(msgs)}\n")
    out.write(f"Long substantive msgs (>150 chars): {len(long_msgs)}\n\n")
    for i, m in enumerate(long_msgs):
        out.write(f"--- [#{i+1}] ID: {m['id']} | Date: {m['date']} {m['time']} ({len(m['text'])} chars) ---\n")
        out.write(m['text'] + "\n\n")

print(f"Written {len(long_msgs)} substantive messages to analysis_66666_overview.txt")
