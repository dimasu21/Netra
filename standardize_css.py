import os
import re

BASE_DIR = r"d:\projectpribadi\Netra"
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

TARGET_FILES = [
    "privacy.html",
    "terms.html"
]

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def get_css_template():
    index_path = os.path.join(TEMPLATES_DIR, "index.html")
    content = read_file(index_path)
    # Extract the STYLE block
    match = re.search(r'(<style>.*?</style>)', content, re.DOTALL)
    if match:
        return match.group(1)
    else:
        raise Exception("Could not find style block in index.html")

def process_files():
    print("Reading CSS from index.html...")
    try:
        css_block = get_css_template()
        print("CSS template extracted successfully.")
    except Exception as e:
        print(f"Error: {e}")
        return

    for filename in TARGET_FILES:
        file_path = os.path.join(TEMPLATES_DIR, filename)
        if not os.path.exists(file_path):
            print(f"Skipping {filename} (not found)")
            continue
            
        print(f"Processing {filename}...")
        content = read_file(file_path)
        
        # Replace existing style block
        new_content = re.sub(r'<style>.*?</style>', css_block, content, flags=re.DOTALL)
        
        if new_content == content:
            print(f"Warning: No style block replaced in {filename}")
        else:
            write_file(file_path, new_content)
            print(f"Successfully updated CSS in {filename}")

if __name__ == "__main__":
    process_files()
