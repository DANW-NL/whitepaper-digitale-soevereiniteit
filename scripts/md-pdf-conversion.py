import base64
from pathlib import Path
import markdown
from jinja2 import Template
from playwright.sync_api import sync_playwright
import mimetypes
import re

def img_to_base64(image_path: Path) -> str:
    """Read a local image file and return it as a base64-encoded data URI."""
    with open(image_path, "rb") as f:
        return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"

def embed_images(html: str) -> str:
    """Find relative <img> src references in HTML and replace them with base64 data URIs.

    This ensures images render reliably when loaded by Playwright or headless browsers
    without needing a local web server or file:// URL resolution permissions.
    """
    def repl(match):
        src = match.group(1)
        # Skip external or already-embedded data URIs
        if not src.startswith(("data:", "http://", "https://")):
            # Resolve relative paths against the paper/ directory
            img_path = Path("paper/" + src)
            if img_path.is_file():
                mime, _ = mimetypes.guess_type(str(img_path))
                mime = mime or "image/png"
                b64 = base64.b64encode(img_path.read_bytes()).decode("utf-8")
                return f'src="data:{mime};base64,{b64}"'
        return match.group(0)

    return re.sub(r'src=["\']([^"\']+)["\']', repl, html)

def compile_whitepaper(file_list: list[str], output_pdf: str, doc_title: str, logo_path: str, template_path: str = "scripts/template.html"):
    """Compile Markdown source chapters into a paginated PDF using Paged.js and Playwright."""
    # 1. Merge Markdown: concatenate chapter files with page breaks in between
    merged_md_parts = []
    for idx, filepath in enumerate(file_list):
        content = Path(filepath).read_text(encoding="utf-8").strip()
        if idx > 0:
            # Force each subsequent chapter to begin on a fresh page
            merged_md_parts.append('\n\n<div class="page-break"></div>\n\n')
        merged_md_parts.append(content)

    full_markdown = "\n\n".join(merged_md_parts)

    # 2. Markdown to HTML: parse markdown and generate table of contents
    md = markdown.Markdown(
        extensions=["extra", "toc", "codehilite", "sane_lists"],
        extension_configs={
            "toc": {
                "permalink": False,
                "title": "Inhoudsopgave",
                "toc_depth": "1",
                "slugify": lambda value, sep: "sec-" + markdown.extensions.toc.slugify(value, sep)
            }
        }
    )

    body_html = embed_images(md.convert(full_markdown))
    toc_html = md.toc
    logo_base64 = img_to_base64(Path(logo_path))

    # 3. Layout Template with Paged.js & CSS Paged Media
    # Load HTML template containing Paged.js configuration, page setup, and CSS
    template_file = Path(template_path)
    if not template_file.is_file():
        # Fallback to look relative to the script directory if run from another CWD
        fallback = Path(__file__).resolve().parent / template_file.name
        if fallback.is_file():
            template_file = fallback
    html_template = template_file.read_text(encoding="utf-8")

    # Base href needed by the browser to resolve relative URLs
    base_href = Path.cwd().resolve().as_uri() + "/"

    # Populate Jinja2 placeholders (TOC, body, metadata, encoded logo)
    full_html = Template(html_template).render(
        toc=toc_html,
        body=body_html,
        doc_title=doc_title,
        logo=logo_base64,
        base_href=base_href
    )

    # Save intermediate HTML output for debugging and previewing
    with open("output/test.html", "w", encoding="utf-8") as file:
        file.write(full_html)

    # 4. Render with Playwright: use headless Chromium to execute Paged.js layout and export PDF
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--allow-file-access-from-files"])
        page = browser.new_page()

        # Load content and wait for Paged.js polyfill to finish paginating the DOM
        page.set_content(full_html, wait_until="networkidle")
        page.wait_for_function("() => window.pagedjsRendered === true", timeout=60000)

        # Print PDF (margins set to 0 here because @page CSS rules manage print margins)
        page.pdf(
            path=output_pdf,
            format="A4",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}  # Margins managed by @page
        )
        browser.close()

if __name__ == '__main__':
    # Explicit file order defines the document structure
    chapter_files = [
        "paper/00-bijdragen.md",
        "paper/01-management_samenvatting.md",
        "paper/02-aanleiding_en_context.md",
        "paper/03-Begrippenkader_en_afbakening.md",
        "paper/04-architectuurvraagstuk.md",
        "paper/05-governance-en-architectuurprincipes.md",
        "paper/06-managen-van-systeemrisicos.md",
        "paper/07-hulpmiddelen_voor_de_architect.md",
        "paper/08-governance_rollen_verantwoordelijkheden.md",
        "paper/09-conclusies_en_aanbevelingen.md",
        "paper/B1-begrippenlijst.md",
        "paper/B2-hulpmiddelen.md",
        "paper/B3-gebruikte_bronnen_en_inspiratiebronnen.md"
    ]

    compile_whitepaper(
        file_list=chapter_files,
        output_pdf="output/Een Enterprise Architectuur aanpak voor DIgitale Soevereiniteit.pdf",
        doc_title="Een Enterprise Architectuur aanpak voor DIgitale Soevereiniteit",
        logo_path="paper/images/DANW-logo-CMYK-compleet-LA.png",
        template_path="scripts/template.html"
    )
