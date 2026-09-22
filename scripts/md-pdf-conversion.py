import base64
from pathlib import Path
import markdown
from jinja2 import Template
from playwright.sync_api import sync_playwright

def img_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"

def compile_whitepaper(file_list: list[str], output_pdf: str, doc_title: str, logo_path: str):
    # 1. Merge Markdown files with explicit page breaks between them
    merged_md_parts = []
    for idx, filepath in enumerate(file_list):
        content = Path(filepath).read_text(encoding="utf-8").strip()
        # Add a page break marker before each chapter, except the very first one
        if idx > 0:
            merged_md_parts.append('\n\n<div class="page-break"></div>\n\n')
        merged_md_parts.append(content)

    full_markdown = "\n\n".join(merged_md_parts)

    # 2. Configure the Markdown parser with TOC support
    md = markdown.Markdown(
        extensions=[
            "extra",
            "toc",
            "codehilite"
        ],
        extension_configs={
            "toc": {
                "permalink": False,
                "title": "Inhoudsopgave",
                "toc_depth": "1-2"  # Focuses on H2 and H3; excludes document title H1 if needed
            }
        }
    )

    body_html = md.convert(full_markdown)
    toc_html = md.toc  # Generated TOC with functioning anchor links

    # 3. Layout Template
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body { font-family: "Segoe UI", Helvetica, Arial, sans-serif; font-size: 11pt; line-height: 1.6; color: #222; }
        h1, h2, h3 { color: #003366; }

        /* Page break utilities */
        .page-break { page-break-before: always; }

        /* Table of Contents styling */
        .toc {
          background: #fdfdfd;
          border: 1px solid #e2e8f0;
          padding: 1.5rem 2rem;
          margin-bottom: 2rem;
          border-radius: 4px;
        }
        .toc .toctitle {
          font-size: 1.3rem;
          font-weight: bold;
          margin-bottom: 1rem;
          color: #003366;
        }
        .toc ul { list-style-type: none; padding-left: 1.2rem; margin: 0; }
        .toc > ul { padding-left: 0; }
        .toc li { margin: 0.3rem 0; }
        .toc a { text-decoration: none; color: #1a56db; }
        .toc a:hover { text-decoration: underline; }

        .text-center { text-align: center; }

        ul, ol {
          margin-top: 0.5em;
          margin-bottom: 1em;
          padding-left: 1.5em; /* Controls left indentation */
        }

        li {
          margin-bottom: 0.3em; /* Adds breathing room between items */
          line-height: 1.5;
        }

        /* Prevents page breaks from cutting an individual bullet point in half */
        li {
          page-break-inside: avoid;
        }

        /* Tables & formatting */
        table { border-collapse: collapse; width: 100%; margin: 1em 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f8fafc; }
      </style>
    </head>
    <body>
      <!-- Place TOC at the desired position (e.g., right after an introduction or on a dedicated page) -->
      {{ toc }}
      <div class="page-break"></div>

      {{ body }}
    </body>
    </html>
    """

    full_html = Template(html_template).render(toc=toc_html, body=body_html)

    # 4. Running Header & Footer
    logo_data = img_to_base64(Path(logo_path))
    header_template = f"""
    <div style="font-size: 9pt; width: 100%; display: flex; justify-content: flex-begin; padding: 0 1.5cm; align-items: center;">
        <img src="{logo_data}" style="height: 45px; object-fit: contain;" />
    </div>
    """
    footer_template = f"""
    <div style="font-size: 8pt; width: 100%; display: flex; justify-content: space-between; padding: 0 1.5cm; color: #666; margin-top: 5px;">
        <span>{doc_title}</span>
        <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
    </div>
    """

    # 5. Playwright Print Execution
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(full_html, wait_until="networkidle")
        page.pdf(
            path=output_pdf,
            format="A4",
            display_header_footer=True,
            header_template=header_template,
            footer_template=footer_template,
            margin={"top": "2.5cm", "bottom": "2.5cm", "left": "2cm", "right": "2cm"},
            print_background=True
        )
        browser.close()


if __name__ == '__main__':
    # Explicit file order defines the document structure
    chapter_files = [
        "docs/01-management_samenvatting.md",
        "docs/02-aanleiding_en_context.md"
    ]

    compile_whitepaper(
        file_list=chapter_files,
        output_pdf="output/Een Enterprise Architectuur aanpak voor DIgitale Soevereiniteit.pdf",
        doc_title="Een Enterprise Architectuur aanpak voor DIgitale Soevereiniteit",
        logo_path="docs/images/DANW-logo-CMYK-compleet-LA.png"
    )
