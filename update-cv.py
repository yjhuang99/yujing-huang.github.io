#!/usr/bin/env python3
"""
update-cv.py — regenerate the view-only CV for yujing-huang.com

The website shows the CV in a view-only canvas viewer (cv.html) that reads the
PDF bytes from cv-data.js (base64). There is no downloadable cv.pdf on the
server. To update the CV you only need to regenerate cv-data.js — nothing else
changes.

USAGE
    python3 update-cv.py /path/to/NEW_CV.pdf

    # then, to publish:
    git add cv-data.js
    git commit -m "Update CV"
    git push origin master        # GitHub Pages rebuilds in ~1 min

AFTER PUSHING
    Verify in an INCOGNITO window (Cmd+Shift+N) — not your normal browser,
    which caches for ~10 min. Confirm the new CV renders and there is still
    no download button.

WATCH
    If your CV source is LaTeX/Word, strip any phone number before exporting
    the PDF — it is embedded as real text and will show in the viewer.
"""

import base64
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cv-data.js")


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: python3 update-cv.py /path/to/NEW_CV.pdf")

    pdf_path = sys.argv[1]
    if not os.path.isfile(pdf_path):
        sys.exit(f"error: file not found: {pdf_path}")
    if not pdf_path.lower().endswith(".pdf"):
        sys.exit("error: expected a .pdf file")

    with open(pdf_path, "rb") as f:
        data = f.read()

    b64 = base64.b64encode(data).decode("ascii")

    with open(OUT, "w") as f:
        f.write("// Embedded CV (base64). Rendered to canvas by cv.html for "
                "view-only display.\n")
        f.write('window.CV_B64 = "%s";\n' % b64)

    print(f"Wrote {OUT}")
    print(f"  source PDF : {pdf_path} ({len(data):,} bytes)")
    print(f"  base64     : {len(b64):,} chars")
    print()
    print("Next:")
    print("  git add cv-data.js && git commit -m 'Update CV' && git push origin master")
    print("  then verify in an incognito window (no download button).")


if __name__ == "__main__":
    main()
