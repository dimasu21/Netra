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

# Standard Footer HTML from index.html
STANDARD_FOOTER_HTML = """
    <!-- Footer -->
    <footer class="footer">
        <div class="footer-main">
            <div class="footer-brand">
                <h3>NETRA</h3>
                <p>Platform analisis dokumen cerdas berbasis OCR dan algoritma Rabin-Karp untuk membantu mahasiswa dalam
                    proses tinjauan pustaka.</p>
            </div>

            <div class="footer-column">
                <h4 data-i18n="footer.tools">TOOLS</h4>
                <ul>
                    <li><a href="/ocr">OCR Scanner</a></li>
                    <li><a href="/document">Document Parser</a></li>
                    <li><a href="/batch">Batch Analysis</a></li>
                </ul>
            </div>

            <div class="footer-column">
                <h4 data-i18n="footer.company">COMPANY</h4>
                <ul>
                    <li><a href="/about" data-i18n="footer.about">About</a></li>
                    <li><a href="/pricing" data-i18n="footer.pricing">Pricing</a></li>
                    <li><a href="/contact" data-i18n="footer.contact">Contact</a></li>
                </ul>
            </div>

            <div class="footer-column">
                <h4 data-i18n="footer.legal">LEGAL</h4>
                <ul>
                    <li><a href="/privacy" data-i18n="footer.privacy">Kebijakan Privasi</a></li>
                    <li><a href="/terms" data-i18n="footer.terms">Syarat & Ketentuan</a></li>
                </ul>
            </div>
        </div>

        <div class="footer-bottom">
            <div class="footer-copyright" data-i18n="footer.copyright">© 2025 NETRA. All rights reserved.</div>
        </div>
    </footer>
"""

# Standard Footer CSS from index.html (including responsive rules)
STANDARD_FOOTER_CSS = """
        /* ==================== FOOTER (Standardized) ==================== */
        .footer {
            background: #0f172a;
            color: #94a3b8;
            margin-top: auto; /* Ensure it pushes to bottom if flex column */
        }

        .footer-main {
            max-width: 1100px;
            margin: 0 auto;
            padding: 48px 24px;
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr;
            gap: 32px;
        }

        .footer-brand {
            font-family: 'Space Mono', monospace;
        }

        .footer-brand h3 {
            color: var(--white);
            font-size: 1.1rem;
            margin-bottom: 12px;
        }

        .footer-brand p {
            font-size: 0.85rem;
            line-height: 1.6;
        }

        .footer-column h4 {
            font-family: 'Space Mono', monospace;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--white);
            margin-bottom: 16px;
        }

        .footer-column ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .footer-column ul li {
            margin-bottom: 10px;
        }

        .footer-column ul li a {
            color: #94a3b8;
            text-decoration: none;
            font-size: 0.85rem;
            transition: color 0.2s;
        }

        .footer-column ul li a:hover {
            color: var(--blue-light);
        }

        .footer-bottom {
            border-top: 1px solid #1e293b;
            padding: 20px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1100px;
            margin: 0 auto;
        }

        .footer-copyright {
            font-size: 0.8rem;
            font-family: 'Space Mono', monospace;
        }

        /* Responsive Footer */
        @media (max-width: 1024px) {
            .footer-main {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media (max-width: 768px) {
            .footer-main {
                grid-template-columns: 1fr;
            }

            .footer-bottom {
                flex-direction: column;
                text-align: center;
                gap: 16px;
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
    
    # 1. Replace HTML Footer
    # Regex to find <footer ... > ... </footer>
    # We match <footer class="footer"> ... </footer> specifically or just <footer...</footer>
    
    # Check if footer exists
    if '<footer' in content:
        content = re.sub(r'<footer.*?</footer>', STANDARD_FOOTER_HTML, content, flags=re.DOTALL)
        print("  - Footer HTML replaced.")
    else:
        # If no footer, append before script or body end
        print("  - No footer found to replace. Appending.")
        if '<script>' in content:
            content = content.replace('<script>', STANDARD_FOOTER_HTML + '\n<script>', 1)
        else:
            content = content.replace('</body>', STANDARD_FOOTER_HTML + '\n</body>')

    # 2. Inject CSS
    # We append it to the end of the style block, same as before
    if '</style>' in content:
        # Avoid duplicate injection if possible, but our CSS block name is uniqueish
        if '/* ==================== FOOTER (Standardized) ==================== */' not in content:
            content = content.replace('</style>', STANDARD_FOOTER_CSS + "\n</style>")
            print("  - Footer CSS injected.")
        else:
            print("  - Footer CSS already present.")
    
    write_file(path, content)
    print("  - Done.")

if __name__ == "__main__":
    for f in TARGET_FILES:
        process_file(f)
