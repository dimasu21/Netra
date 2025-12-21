import os
import re

targets = [
    'templates/ocr.html',
    'templates/document.html',
    'templates/index.html',
    'templates/batch.html',
    'templates/pricing.html',
    'templates/about.html',
    'templates/contact.html'
]

def update_file(path):
    if not os.path.exists(path): return
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. HTML Move: Toggle after Auth
    pattern_html = r'(<button class="navbar-toggle">.*?</button>)(\s*)(<div class="navbar-auth">.*?</div>)'
    
    if re.search(pattern_html, content, re.DOTALL):
        # Swap: Auth (3) + Space (2) + Toggle (1)
        content = re.sub(pattern_html, r'\3\2\1', content, flags=re.DOTALL)
        print(f"  [HTML] Moved Toggle in {path}")
    else:
        # Check if already moved (Toggle after Auth)
        pattern_already = r'(<div class="navbar-auth">.*?</div>)(\s*)(<button class="navbar-toggle">.*?</button>)'
        if re.search(pattern_already, content, re.DOTALL):
             print(f"  [HTML] Already moved in {path}")
        else:
             print(f"  [HTML] Pattern not found in {path}")
        
    # 2. CSS Injection
    if '.navbar-tools.active {' not in content:
        css_code = """
            .navbar-tools.active {
                display: flex;
                flex-direction: column;
                position: absolute;
                top: 60px;
                left: 0;
                right: 0;
                background: var(--white);
                border-bottom: 2px solid var(--gray-light);
                padding: 16px;
                z-index: 1000;
                animation: slideDown 0.3s ease;
            }
            @keyframes slideDown {
                from { opacity: 0; transform: translateY(-10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .navbar-tools.active a {
                margin-bottom: 12px;
                width: 100%;
                display: block;
            }
            .navbar-tools.active .dropdown-content {
                position: static;
                box-shadow: none;
                border: none;
                border-left: 2px solid var(--gray-light);
                padding-left: 12px;
                margin-bottom: 12px;
                display: none; /* Keep hidden until hover or click? Mobile usually click */
            }
            /* Show dropdown on hover/active for mobile? Or simplified */
            .navbar-tools.active .dropdown:hover .dropdown-content {
                display: block;
            }
"""
        content = content.replace('@media (max-width: 900px) {', '@media (max-width: 900px) {' + css_code)
        print(f"  [CSS] Injected mobile styles in {path}")
        
    # 3. JS Injection
    # Check if logic already exists (simple check)
    if 'toolsMenu.classList.toggle(\'active\')' not in content:
        js_code = """
        // Mobile Menu Toggle
        const toggleBtn = document.querySelector('.navbar-toggle');
        const toolsMenu = document.querySelector('.navbar-tools');
        if (toggleBtn && toolsMenu) {
            toggleBtn.addEventListener('click', () => {
                toolsMenu.classList.toggle('active');
                const icon = toggleBtn.querySelector('i');
                if (icon) {
                    icon.classList.toggle('bi-list');
                    icon.classList.toggle('bi-x');
                }
            });
        }
    </script>"""
        # Replace only the last </script> tag
        parts = content.rsplit('</script>', 1)
        if len(parts) == 2:
            content = parts[0] + js_code + parts[1]
            print(f"  [JS] Injected JS logic in {path}")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

for t in targets:
    update_file(t)
    
print("Update Mobile Complete")
