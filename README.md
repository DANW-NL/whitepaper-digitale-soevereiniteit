# whitepaper-digitale-soevereiniteit
Open review and development of the DANW whitepaper on digital sovereignty

## Writing instructions
Normal markdown instructions apply. However, there are a couple of additional tweaks you can do, that work via the CSS that is used in the script.

If you want to center a paragraph, add `{: .text-center }` directly under the paragraph.

If you want to start something on a new page, add `{: .page-break }` directly under the paragraph, or directly behind a heading.

Images are centered in the middle of the page. You can enter an image like so:
```
![Figuur 2 - Stakeholder Power Grid](images/stakeholders.png){: .medium }
```
The style can be omitted, which means full width. Use `{: .medium }` or `{: .small }` when you want to shrink the image a bit.

## Build instructions
In order to build a PDF from the source .md files, follow these instructions.
Python is required. This setup works in user space, no further software is needed.

In order to run the script, you have to set up a virtual environment (once at the beginning and every time a dependency is updated):

```
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

When you want to run the script. First make sure your Python virtual environment is activated:

```
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Now the script can be run:

```
scripts/md-pdf-conversion.py
```

The output will be written in the `output` folder. This folder is ignored by Git. Specific releases of the paper will be put in a dedicated folder.
