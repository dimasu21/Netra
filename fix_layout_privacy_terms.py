import os
import re

BASE_DIR = r"d:\projectpribadi\Netra"
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

TARGET_FILES = [
    "privacy.html",
    "terms.html"
]

LEGAL_CSS = """
        /* ==================== LEGAL CONTENT LAYOUT ==================== */
        .legal-container {
            max-width: 800px;
            margin: 40px auto;
            padding: 40px;
            background: var(--white);
            border: var(--border-width) solid var(--black);
            box-shadow: 8px 8px 0 var(--black);
        }

        .legal-container h1 {
            font-family: 'Space Mono', monospace;
            font-size: 2.5rem;
            margin-bottom: 10px;
            color: var(--black);
            text-transform: uppercase;
            letter-spacing: -1px;
        }

        .last-updated {
            color: var(--gray);
            font-size: 0.9rem;
            margin-bottom: 40px;
            font-family: 'Space Mono', monospace;
            display: block;
        }

        .legal-content h2 {
            font-family: 'Space Mono', monospace;
            font-size: 1.5rem;
            margin-top: 40px;
            margin-bottom: 16px;
            color: var(--black);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .legal-content h2 i {
            font-size: 1.25rem;
            color: var(--blue-primary);
        }

        .legal-content p {
            font-size: 1rem;
            line-height: 1.7;
            color: var(--gray);
            margin-bottom: 16px;
        }

        .legal-content ul {
            margin-bottom: 24px;
            padding-left: 20px;
        }

        .legal-content li {
            font-size: 1rem;
            line-height: 1.7;
            color: var(--gray);
            margin-bottom: 8px;
            list-style-type: square;
        }
        
        .legal-content strong {
            color: var(--black);
            font-weight: 700;
        }
        
        .contact-box {
            background: var(--blue-pale);
            border: 2px solid var(--black);
            padding: 20px;
            margin-top: 30px;
        }
        
        .back-link {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-top: 40px;
            color: var(--blue-primary);
            text-decoration: none;
            font-weight: 600;
            font-family: 'Space Mono', monospace;
        }
        
        .back-link:hover {
            text-decoration: underline;
        }

        @media (max-width: 768px) {
            .legal-container {
                margin: 20px;
                padding: 24px;
                box-shadow: 5px 5px 0 var(--black);
            }
            
            .legal-container h1 {
                font-size: 2rem;
            }
        }
"""

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def process_file(filename):
    print(f"Processing {filename}...")
    path = os.path.join(TEMPLATES_DIR, filename)
    content = read_file(path)

    # 1. Inject CSS
    if '</style>' in content:
        # Check if legal css already exists to avoid duplication
        if 'legal-container' not in content:
            content = content.replace('</style>', LEGAL_CSS + "\n</style>")
            print("CSS Injected.")
        else:
            print("CSS seems to exist already.")

    # 2. Wrap Content
    # Logic: Find content between </nav> and Footer.
    # The navbar ends with </nav>
    # The content starts... usually with <h1>
    # The footer starts with <div class="footer-container"> or similar?
    # Actually, looking at index.html footer structure.
    # Wait, the footer in index.html starts with <footer class="footer">
    
    # Let's find the start of the content (after Navbar) and end (before Footer)
    # Pattern: </nav> ...content... <footer
    
    match = re.search(r'(</nav>)(.*)(<footer)', content, re.DOTALL)
    if match:
        nav_end = match.group(1)
        inner_content = match.group(2)
        footer_start = match.group(3)
        
        # Check if already wrapped
        if '<div class="legal-container">' in inner_content:
             print("Content already wrapped.")
        else:
            # Clean up inner content (trim whitespace)
            # inner_content = inner_content.strip() 
            # Be careful with stripping, might lose newlines needed.
            
            # Wrap it
            new_inner_content = f'\n    <div class="legal-container">\n        <div class="legal-content">\n{inner_content}\n        </div>\n    </div>\n'
            
            # Reconstruct content
            # We use match.start() and match.end() to replace exactly
            new_content = content[:match.end(1)] + new_inner_content + content[match.start(3):]
            
            write_file(path, new_content)
            print(f"Content wrapped in {filename}")
    else:
        print(f"Could not find content block in {filename}. Check structure.")

if __name__ == "__main__":
    for f in TARGET_FILES:
        process_file(f)
