# whitepaper-digitale-soevereiniteit
Open review and development of the DANW whitepaper on digital sovereignty

## Writing instructions
If you want to center a paragraph, add `{: .text-center }` directly under the paragraph.

## Build instructions
In order to build a PDF from the source .md files, follow these instructions.
Python is required. This setup works in user space, no further software is needed.

```
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```
