import os
import re

BASE_DIR = r"d:\projectpribadi\Netra"
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Index (source)
SOURCE_FILE = "index.html"

# Targets (excluding privacy/terms which we fully replaced)
TARGET_FILES = [
    "ocr.html",
    "document.html",
    "batch.html",
    "pricing.html",
    "about.html",
    "contact.html"
]

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def get_navbar_css():
    path = os.path.join(TEMPLATES_DIR, SOURCE_FILE)
    content = read_file(path)
    
    # We want to extract valid CSS for navbar/lang/auth/hero(parts)
    # Since extracting part by part is hard with regex, we will grab the whole style block 
    # BUT we must be careful not to double up too much junk.
    # However, to be SAFE and consistent, maybe we should just prepend the Index CSS to the file style?
    # Or, we can extract specific sections if they are marked.
    # The index.html CSS has comments like /* ==================== NAVBAR ==================== */
    
    # Heuristic: Extract everything from /* ==================== NAVBAR ==================== */ 
    # up to /* ==================== BRUTALIST CARD ==================== */ (or end of file if not found)
    # No, that's risky.
    
    # Let's extract specific known blocks based on index.html content viewed earlier.
    # We need:
    # 1. Navbar
    # 2. Language Dropdown
    # 3. User Dropdown
    # 4. Mobile Media Query parts for Navbar
    
    # Strategy: Replace the existing old navbar CSS in target files or Append new CSS?
    # The old CSS often has conflicting .navbar styles. replacing is better.
    # BUT finding "old navbar css" is hard.
    
    # Better Strategy: 
    # 1. Read Index CSS
    # 2. Find markers /* ==================== NAVBAR ==================== */ 
    #    and /* ==================== HERO SECTION (CAKE STYLE) ==================== */
    #    and grab everything between them + Layouts.
    
    # Let's simple Copy ALL styles from index.html that are relevant.
    # I'll construct a known good Clean Navbar CSS Block based on what I saw in index.html (lines 157 to 470 approx)
    
    # I will extract that exact chunk programmatically using start/end markers from index.html content
    
    match = re.search(r'(/\* ==================== NAVBAR ==================== \*/.*?/\* ==================== HERO SECTION \(CAKE STYLE\) ==================== \*/)', content, re.DOTALL)
    if match:
        # We also need the HERO styles because the navbar relies on some var definitions in :root which assume consistency,
        # but :root is usually at top.
        # We also need the @media (max-width: 900px) part which is usually at the bottom or inside.
        # In index.html, the media query was AFTER.
        
        # Let's return a manually constructed CSS block that definitely contains what we need.
        # It's safer to rely on my knowledge of the file content than regex guessing.
        pass
    
    # Let's use the actual content from the file to be precise
    # Extract Navbar + Lang + User + Mobile Query
    
    # Extract Navbar Section
    navbar_part = re.search(r'(/\* ==================== NAVBAR ==================== \*/.*?)(\n\s*/\* ==================== HERO SECTION)', content, re.DOTALL).group(1)
    
    # Extract Media Query Section (approximate)
    # Looking for @media (max-width: 900px) block
    media_part = re.search(r'(@media \(max-width: 900px\) \{.*$)', content, re.DOTALL).group(1)
    # This might capture too much (closing brackets), but usually ends the style block.
    # Let's assume the media block is the last thing.
    
    combined_css = "\n" + navbar_part + "\n" + media_part
    
    # We also need root vars? Subpages usually have them.
    return combined_css

def inject_css(filename, new_css):
    path = os.path.join(TEMPLATES_DIR, filename)
    content = read_file(path)
    
    # Identify where to inject.
    # 1. Remove old navbar/mobile CSS if possible to avoid conflicts?
    # The old CSS in ocr.html has /* ==================== iLovePDF-STYLE NAVBAR ==================== */
    # we should remove that block.
    
    # Remove old navbar style
    content = re.sub(r'/\* ==================== iLovePDF-STYLE NAVBAR ==================== \*/.*?(?=/\* ==================== MAIN CONTAINER)', '', content, flags=re.DOTALL)
    
    # Also remove any old @media (max-width: 900px) block if possible
    content = re.sub(r'@media \(max-width: 900px\) \{.*?(?=</style>)', '', content, flags=re.DOTALL)
    
    # Inject New CSS before </style>
    content = content.replace('</style>', new_css + "\n</style>")
    
    return content

# HARDCODED CSS BLOCK FROM INDEX.HTML (Safe & Reliable)
NAVBAR_CSS = """
        /* ==================== NAVBAR (Standardized) ==================== */
        .navbar {
            background: var(--white);
            border-bottom: 2px solid var(--gray-light);
            padding: 0;
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        .navbar-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 24px 0 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: 60px;
        }

        .navbar-brand {
            display: flex;
            align-items: center;
            gap: 4px;
            text-decoration: none;
        }

        .navbar-brand .logo-text {
            font-family: 'Space Mono', monospace;
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--black);
        }

        .navbar-tools {
            display: flex;
            align-items: center;
            gap: 0;
            height: 100%;
            margin-left: auto;
        }

        .navbar-tools a {
            display: flex;
            align-items: center;
            height: 60px;
            padding: 0 16px;
            color: var(--gray);
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            text-decoration: none;
            letter-spacing: 0.5px;
            border-bottom: 3px solid transparent;
            transition: all 0.2s;
        }

        .navbar-tools a:hover {
            color: var(--blue-primary);
            border-bottom-color: var(--blue-primary);
            background: var(--blue-pale);
        }

        .navbar-tools a.active {
            color: var(--blue-primary);
            border-bottom-color: var(--blue-primary);
        }

        .navbar-tools .dropdown {
            position: relative;
        }

        /* Mobile-only links - hidden on desktop */
        .mobile-only-link {
            display: none !important;
        }

        .navbar-tools .dropdown-content {
            display: none;
            position: absolute;
            top: 100%;
            left: 0;
            background: var(--white);
            border: 1px solid var(--gray-light);
            border-radius: 8px;
            min-width: 150px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            padding: 4px 0;
        }

        .navbar-tools .dropdown:hover .dropdown-content {
            display: block;
        }

        .navbar-tools .dropdown-content a {
            display: block !important;
            width: 100%;
            height: auto !important;
            padding: 10px 16px !important;
            font-size: 0.9rem !important;
            border-bottom: none !important;
            text-transform: none !important;
            letter-spacing: normal !important;
        }

        .navbar-tools .dropdown-content a:hover {
            background: var(--gray-light);
            border-bottom-color: transparent !important;
        }

        .navbar-tools .dropdown-content a:last-child {
            border-bottom: none;
        }

        .navbar-auth {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .btn-login {
            padding: 8px 16px;
            color: var(--gray);
            font-size: 0.8rem;
            font-weight: 600;
            text-decoration: none;
            transition: color 0.2s;
        }

        .btn-login:hover {
            color: var(--blue-primary);
        }

        .btn-signup {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 8px 16px;
            background: var(--blue-primary);
            color: var(--white);
            border: 2px solid var(--black);
            font-size: 0.8rem;
            font-weight: 600;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-signup:hover {
            background: var(--blue-dark);
            transform: translate(-2px, -2px);
            box-shadow: 4px 4px 0 var(--black);
        }

        .navbar-toggle {
            display: none;
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: var(--black);
        }

        /* ==================== LANGUAGE DROPDOWN ==================== */
        .lang-dropdown {
            position: relative;
        }

        .lang-btn {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 8px 12px;
            background: transparent;
            border: 1px solid var(--gray-light);
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85rem;
            color: var(--gray);
            transition: all 0.2s;
        }

        .lang-btn:hover {
            border-color: var(--blue-primary);
            color: var(--blue-primary);
        }

        .lang-dropdown-content {
            display: none;
            position: absolute;
            top: calc(100% - 4px);
            right: 0;
            background: var(--white);
            border: 1px solid var(--gray-light);
            border-radius: 8px;
            min-width: 180px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            padding-top: 8px;
        }

        .lang-dropdown:hover .lang-dropdown-content,
        .lang-dropdown-content:hover {
            display: block;
        }

        .lang-option {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 16px;
            color: var(--gray);
            text-decoration: none;
            font-size: 0.9rem;
            transition: background 0.2s;
        }

        .lang-option:hover {
            background: var(--gray-light);
        }

        .lang-option.active {
            color: var(--blue-primary);
            font-weight: 600;
        }

        .lang-option i {
            display: none;
        }

        .lang-option.active i {
            display: inline;
            color: var(--blue-primary);
        }

        /* ==================== USER DROPDOWN ==================== */
        .user-dropdown {
            position: relative;
        }

        .user-btn {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            background: var(--blue-pale);
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85rem;
            color: var(--blue-primary);
            font-weight: 600;
        }

        .user-btn:hover {
            background: var(--blue-light);
            color: var(--white);
        }

        .user-dropdown-content {
            display: none;
            position: absolute;
            top: 100%;
            right: 0;
            background: var(--white);
            border: 1px solid var(--gray-light);
            border-radius: 8px;
            min-width: 200px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            margin-top: 4px;
        }

        .user-dropdown:hover .user-dropdown-content {
            display: block;
        }

        .user-info {
            padding: 12px 16px;
        }

        .user-info strong {
            display: block;
            color: var(--black);
            font-size: 0.95rem;
        }

        .user-info small {
            color: var(--gray);
            font-size: 0.8rem;
        }

        .user-dropdown-content hr {
            margin: 0;
            border: none;
            border-top: 1px solid var(--gray-light);
        }

        .user-dropdown-content a {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 10px 16px;
            color: var(--gray);
            text-decoration: none;
            font-size: 0.9rem;
            transition: background 0.2s;
        }

        .user-dropdown-content a:hover {
            background: var(--gray-light);
            color: var(--blue-primary);
        }

        @media (max-width: 900px) {
            .mobile-only-link {
                display: block !important;
            }

            .navbar-tools {
                display: flex;
                flex-direction: column;
                position: fixed;
                top: 0;
                right: 0;
                height: 100vh;
                width: 250px;
                background: var(--white);
                border-left: 3px solid var(--black);
                padding: 80px 24px 24px;
                z-index: 2000;
                transform: translateX(100%);
                transition: transform 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
                box-shadow: -10px 0 30px rgba(0, 0, 0, 0.1);
            }

            .navbar-tools.active {
                transform: translateX(0);
            }

            .navbar-tools a {
                padding: 16px 0 !important;
                border-bottom: 1px solid var(--gray-light) !important;
                width: 100% !important;
                display: block !important;
                height: auto !important;
                color: var(--black) !important;
            }

            .navbar-toggle {
                display: block;
                z-index: 2010;
            }

            .navbar-container {
                padding: 0 16px !important;
            }

            .navbar-brand .logo-text {
                font-size: 1.1rem;
            }
            
            .navbar-right {
                gap: 8px !important;
            }

            .lang-btn span, .user-btn span {
               display: none; 
            }
            
            .lang-btn {
                padding: 6px 8px;
            }
            
            .user-btn {
                padding: 6px 8px;
            }

            .navbar-tools .dropdown {
                display: none !important;
            }
        }
"""

def process_file(filename):
    print(f"Processing {filename}...")
    path = os.path.join(TEMPLATES_DIR, filename)
    content = read_file(path)
    
    # Simple replacement/injection logic
    
    # 1. Look for existing closing style tag
    if '</style>' not in content:
        print(f"Warning: No style block in {filename}")
        return

    # 2. Remove old nav styles if we can identify them (heuristic)
    # Most files have /* ==================== iLovePDF-STYLE NAVBAR ==================== */
    content = re.sub(r'/\* ==================== iLovePDF-STYLE NAVBAR ==================== \*/.*?(?=/\* ==================== MAIN CONTAINER)', '', content, flags=re.DOTALL)
    
    # 3. Remove old media query at bottom
    # Regex to match the LAST @media block before </style>
    # Note: this is risky if there are other media queries.
    # But usually the navbar media query is the last one in these files.
    # Let's just APPEND the new CSS. The cascade will handle it (new overrides old).
    # Except for the conflicts. 
    # Let's try to remove known conflicting blocks.
    
    # Safe approach: Append the standard navbar CSS at the VERY END of the style block.
    # This ensures it overrides any previous conflicting navbar rules.
    new_content = content.replace('</style>', NAVBAR_CSS + "\n</style>")
    
    write_file(path, new_content)
    print(f"Updated {filename}")

if __name__ == "__main__":
    for f in TARGET_FILES:
        process_file(f)
