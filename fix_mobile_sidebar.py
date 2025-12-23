
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

    # We need to find the rule inside the max-width: 900px block.
    # The rule looks like:
    # .mobile-only-link {
    #     display: block !important;
    # }
    
    # We want to replace it with:
    # .navbar-tools a.mobile-only-link {
    #     display: block !important;
    # }
    
    # Regex to capture flexibility in whitespace
    pattern = r"(\.mobile-only-link\s*\{\s*display:\s*block\s*!important;\s*\})"
    
    # We replace it with the stronger selector. 
    # Note: We keep the original class too just in case it's used elsewhere, 
    # using a comma selector or just replacing it if we are sure it's the right place.
    # Given the context of previous files, this rule appears specifically in the mobile query.
    
    replacement = ".navbar-tools a.mobile-only-link, .mobile-only-link { display: block !important; }"
    
    # Perform replacement
    # This might match multiple times if defined multiple times, but typically it is once per file in the mobile block.
    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {filepath}")
    else:
        print(f"No changes needed for {filepath}")

if __name__ == "__main__":
    for f in files:
        fix_file(f)
