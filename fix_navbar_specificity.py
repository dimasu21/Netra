
import os
import re

files = [
    r"d:\projectpribadi\Netra\templates\ocr.html",
    r"d:\projectpribadi\Netra\templates\document.html",
    r"d:\projectpribadi\Netra\templates\batch.html",
    r"d:\projectpribadi\Netra\templates\pricing.html",
    r"d:\projectpribadi\Netra\templates\about.html",
    r"d:\projectpribadi\Netra\templates\contact.html"
]

def fix_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to find the simple class selector
    # We want to replace .mobile-only-link { display: none !important; } 
    # with .navbar-tools .mobile-only-link { display: none !important; }
    # Note: Whitespace might vary.
    
    pattern = r"\.mobile-only-link\s*\{\s*display:\s*none\s*!important;\s*\}"
    replacement = ".navbar-tools .mobile-only-link { display: none !important; }"
    
    new_content = re.sub(pattern, replacement, content)
    
    # Also, specifically look for the min-width: 901px block and inject a rule if not present, 
    # just in case the base rule position matters or is overridden by some other logic.
    # But specificity should be enough. 
    # Let's also check if we can make it even stronger: .navbar-tools a.mobile-only-link
    
    replacement_strong = ".navbar-tools a.mobile-only-link { display: none !important; }"
    new_content = new_content.replace(replacement, replacement_strong)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {filepath}")
    else:
        print(f"No changes needed for {filepath} (pattern might not match exactly)")

if __name__ == "__main__":
    for f in files:
        fix_file(f)
