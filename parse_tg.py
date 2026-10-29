import re
import os
import json
from html.parser import HTMLParser

class TelegramHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.messages = []
        self.current_msg = None
        self.current_date = ""
        self.in_body_details = False
        self.in_text = False
        self.in_date = False
        self.current_text = []
        self.current_time = ""
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = attrs_dict.get('class', '').split()
        
        if tag == 'div':
            if 'message' in classes and 'service' in classes:
                pass
            elif 'message' in classes and 'default' in classes:
                msg_id = attrs_dict.get('id', '')
                self.current_msg = {
                    'id': msg_id,
                    'date': self.current_date,
                    'time': '',
                    'text': ''
                }
            elif 'body' in classes and 'details' in classes:
                self.in_body_details = True
            elif 'text' in classes and self.current_msg is not None:
                self.in_text = True
                self.current_text = []
            elif 'date' in classes and 'details' in classes and self.current_msg is not None:
                self.in_date = True
                
        if tag == 'br' and self.in_text:
            self.current_text.append('\n')
            
    def handle_endtag(self, tag):
        if tag == 'div':
            if self.in_body_details:
                self.in_body_details = False
            elif self.in_text:
                self.in_text = False
                if self.current_msg is not None:
                    full_text = "".join(self.current_text).strip()
                    self.current_msg['text'] = full_text
            elif self.in_date:
                self.in_date = False
            elif self.current_msg is not None and self.current_msg.get('text'):
                # end of message div
                if not any(m['id'] == self.current_msg['id'] for m in self.messages):
                    self.messages.append(self.current_msg)
                self.current_msg = None

    def handle_data(self, data):
        if self.in_body_details:
            cleaned = data.strip()
            # check if it looks like a date header e.g. "22 July 2026"
            if cleaned and any(month in cleaned for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']):
                self.current_date = cleaned
        elif self.in_text:
            self.current_text.append(data)
        elif self.in_date and self.current_msg is not None:
            self.current_msg['time'] = data.strip()

def parse_html_file(file_path):
    parser = TelegramHTMLParser()
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    parser.feed(content)
    return parser.messages

if __name__ == '__main__':
    base_dir = r"C:\Users\dikan\projects\THE-REAWAKENING-PROJECT"
    target_66666 = os.path.join(base_dir, "66666_2026-10-29", "messages.html")
    
    msgs = parse_html_file(target_66666)
    print(f"Total messages parsed in 66666: {len(msgs)}")
    
    out_dir = os.path.join(base_dir, "knowledge-base")
    os.makedirs(out_dir, exist_ok=True)
    
    out_json = os.path.join(out_dir, "parsed_66666.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(msgs, f, ensure_ascii=False, indent=2)
    print(f"Saved to {out_json}")
