import base64
from pathlib import Path
import markdown
from jinja2 import Template
from playwright.sync_api import sync_playwright
import mimetypes
import re

def img_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"

def embed_images(html: str) -> str:
    def repl(match):
        src = match.group(1)
        if not src.startswith(("data:", "http://", "https://")):
            img_path = Path("docs/" + src)
            if img_path.is_file():
                mime, _ = mimetypes.guess_type(str(img_path))
                mime = mime or "image/png"
                b64 = base64.b64encode(img_path.read_bytes()).decode("utf-8")
                return f'src="data:{mime};base64,{b64}"'
        return match.group(0)

    return re.sub(r'src=["\']([^"\']+)["\']', repl, html)

def compile_whitepaper(file_list: list[str], output_pdf: str, doc_title: str, logo_path: str):
    # 1. Merge Markdown
    merged_md_parts = []
    for idx, filepath in enumerate(file_list):
        content = Path(filepath).read_text(encoding="utf-8").strip()
        if idx > 0:
            merged_md_parts.append('\n\n<div class="page-break"></div>\n\n')
        merged_md_parts.append(content)

    full_markdown = "\n\n".join(merged_md_parts)

    # 2. Markdown to HTML
    md = markdown.Markdown(
        extensions=["extra", "toc", "codehilite", "sane_lists"],
        extension_configs={
            "toc": {
                "permalink": False,
                "title": "Inhoudsopgave",
                "toc_depth": "1-2",
                "slugify": lambda value, sep: "sec-" + markdown.extensions.toc.slugify(value, sep)
            }
        }
    )
    body_html = embed_images(md.convert(full_markdown))
    toc_html = md.toc
    logo_base64 = img_to_base64(Path(logo_path))

    # 3. Layout Template with Paged.js & CSS Paged Media
    html_template = """
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <base href="{{ base_href }}">
          <!-- Polyfill for CSS Paged Media -->
          <script src="https://unpkg.com/pagedjs/dist/paged.polyfill.js"></script>
          <style>
          /* Document Setup & Page Margins */
          @page {
            size: A4;
            margin-top: 2.5cm;
            margin-bottom: 2.5cm;
            margin-left: 2cm;
            margin-right: 2cm;

            /* Running Header */
            @top-left {
              content: "";
              background-image: url("{{ logo }}");
              background-repeat: no-repeat;
              background-position: left center;
              background-size: contain;
              height: 45px;
              margin-top: 20px;
            }

            /* Running Footer */
            @bottom-left {
              content: "{{ doc_title }}";
              font-family: "Segoe UI", sans-serif;
              font-size: 8pt;
              color: #666;
              border-top: 1px solid #ddd;
              vertical-align: top;
              padding-top: 4px;
            }
            @bottom-right {
              content: "Pagina " counter(page) " van " counter(pages);
              font-family: "Segoe UI", sans-serif;
              font-size: 8pt;
              color: #666;
              border-top: 1px solid #ddd;
              vertical-align: top;
              padding-top: 4px;
            }
          }

          body {
            font-family: "Segoe UI", Helvetica, Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #222;
          }

          h1, h2, h3 { color: #003366; }
          .page-break { break-before: page; }

          .text-center { text-align: center; }

          .call-out {
            text-align: center;
            color: #003366;
            margin-left: 3rem;
            margin-right: 3rem;
            border-top: 1px solid #003366;
            border-bottom: 1px solid #003366;
          }

          img {
            width: 100%;
          }

          /* --- Inhoudsopgave (TOC) with Page Numbers & Dot Leaders --- */
          .toc {
            margin-bottom: 2rem;
            padding: 1rem 0;
          }
          .toc .toctitle {
            font-size: 1.4rem;
            font-weight: bold;
            color: #003366;
            margin-bottom: 1.2rem;
            display: block;
          }
          .toc ul {
            list-style: none;
            padding-left: 0;
            margin: 0;
          }
          .toc ul ul {
            padding-left: 1.5rem; /* Indentation for subheadings */
          }
          .toc li {
            margin: 0.35rem 0;
          }
          .toc a {
            text-decoration: none;
            color: inherit;
            display: flex;
            align-items: baseline;
          }
          /* CSS Dot Leaders */
          .toc a::after {
            content: target-counter(attr(href), page);
            margin-left: auto;
            font-weight: normal;
            font-variant-numeric: tabular-nums;
          }
          .toc a::before {
            content: "";
            order: 1;
            flex: 1;
            border-bottom: 1px dotted #999;
            margin: 0 0.5em;
          }
          .toc a span, .toc a {
            order: 0;
          }
          .toc a::after {
            order: 2;
          }

          /* Content lists */
          ul, ol { margin-top: 0.5em; margin-bottom: 1em; padding-left: 1.5em; }
          li { margin-bottom: 0.3em; break-inside: avoid; }

          /* Tables & formatting */
          table { border-collapse: collapse; width: 100%; margin: 1em 0; }
          th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
          th { background-color: #f8fafc; }
        </style>
        </head>
        <body>
          {{ toc }}
          <div class="page-break"></div>
          {{ body }}
        </body>
      </html>
      """

    base_href = Path.cwd().resolve().as_uri() + "/"

    full_html = Template(html_template).render(
        toc=toc_html,
        body=body_html,
        doc_title=doc_title,
        logo=logo_base64,
        base_href=base_href
    )

    # 4. Render with Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--allow-file-access-from-files"])
        page = browser.new_page()


        # Load content and wait for Paged.js to finish rendering pages
        page.set_content(full_html, wait_until="networkidle")
        page.wait_for_selector(".pagedjs_pages")  # Indicator that Paged.js layout is ready

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
        "docs/01-management_samenvatting.md",
        "docs/02-aanleiding_en_context.md",
        "docs/03-Begrippenkader_en_afbakening.md",
        "docs/04-architectuurvraagstuk.md",
        "docs/05-governance-en-architectuurprincipes.md",
        "docs/06-managen-van-systeemrisicos.md"
    ]

    compile_whitepaper(
        file_list=chapter_files,
        output_pdf="output/Een Enterprise Architectuur aanpak voor DIgitale Soevereiniteit.pdf",
        doc_title="Een Enterprise Architectuur aanpak voor DIgitale Soevereiniteit",
        logo_path="docs/images/DANW-logo-CMYK-compleet-LA.png"
    )
