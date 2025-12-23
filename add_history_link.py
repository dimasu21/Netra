
import os
import re

files = [
    r"d:\projectpribadi\Netra\templates\index.html",
    r"d:\projectpribadi\Netra\templates\ocr.html",
    r"d:\projectpribadi\Netra\templates\document.html",
    r"d:\projectpribadi\Netra\templates\batch.html",
    r"d:\projectpribadi\Netra\templates\pricing.html",
    r"d:\projectpribadi\Netra\templates\about.html",
    r"d:\projectpribadi\Netra\templates\contact.html"
]

def update_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if link already exists
    if '/history' in content:
        print(f"History link already in {filepath}")
        return

    # Find the logout link to insert before
    # Pattern designed to match the start of the logout link tag
    # <a href="/logout" ...
    
    pattern = r'(<a href="/logout")'
    replacement = r"""<a href="/history" class="dropdown-item">
                            <i class="bi bi-clock-history"></i> Riwayat
                        </a>
                        <div class="dropdown-divider"></div>
                        \1"""
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
    else:
        print(f"Could not find injection point in {filepath}")

if __name__ == "__main__":
    for f in files:
        update_file(f)
