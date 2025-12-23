import os
import re

BASE_DIR = r"d:\projectpribadi\Netra"
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

TARGET_FILES = [
    "ocr.html",
    "document.html",
    "batch.html",
    "pricing.html",
    "about.html",
    "contact.html",
    "privacy.html",
    "terms.html"
]

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def get_navbar_template():
    index_path = os.path.join(TEMPLATES_DIR, "index.html")
    content = read_file(index_path)
    
    # Extract the navbar block
    # Looking for <nav class="navbar"> ... </nav>
    # Using dotall to match newlines
    match = re.search(r'(<nav class="navbar">.*?</nav>)', content, re.DOTALL)
    if match:
        return match.group(1)
    else:
        raise Exception("Could not find navbar in index.html")

def customize_navbar(navbar_html, filename):
    # 1. Remove existing active classes
    navbar_html = navbar_html.replace('class="active"', '')
    navbar_html = navbar_html.replace('class="mobile-only-link"', 'CLASS_MOBILE_LINK_PLACEHOLDER') # Temporary protect mobile links
    
    # 2. Set active class based on filename
    if filename == "ocr.html":
        navbar_html = navbar_html.replace('href="/ocr"', 'href="/ocr" class="active"')
    elif filename == "document.html":
        navbar_html = navbar_html.replace('href="/document"', 'href="/document" class="active"')
    elif filename == "batch.html":
        navbar_html = navbar_html.replace('href="/batch"', 'href="/batch" class="active"')
    
    # Restore mobile link class
    navbar_html = navbar_html.replace('CLASS_MOBILE_LINK_PLACEHOLDER', 'class="mobile-only-link"')
    
    # Special Handling for Privacy and Terms (in dropdown) is tricky because they are inside dropdown
    # But usually we just leave them. The user wants consistency.
    
    return navbar_html

def process_files():
    print("Reading index.html...")
    try:
        navbar_template = get_navbar_template()
        print("Navbar template extracted successfully.")
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
        
        # customized navbar
        new_navbar = customize_navbar(navbar_template, filename)
        
        # Replace existing navbar
        # We use strict regex to find the navbar block
        new_content = re.sub(r'<nav class="navbar">.*?</nav>', new_navbar, content, flags=re.DOTALL)
        
        # Check if replacement actually happened
        if new_content == content:
            print(f"Warning: No navbar block found/replaced in {filename}")
        else:
            write_file(file_path, new_content)
            print(f"Successfully updated {filename}")

if __name__ == "__main__":
    process_files()
