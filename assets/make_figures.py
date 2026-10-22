#!/usr/bin/env python3
"""Draw the figures used in README.md and the GitHub social preview.

  assets/lacing_n3.svg        one of the six n = 3 lacings and its mirror image
  assets/social_preview.svg   1280x640 preview card (render to PNG, see below)

Eyelets are numbered as in OEIS A072503 (Pfoertner): left side 1..n from top to
bottom, right side n+1..2n from bottom to top, so row k holds eyelets k and 2n+1-k.

Usage (from the repository root):
  python3 assets/make_figures.py
  # PNG for Settings -> Social preview (needs a Chromium binary and Pillow).
  # Headless Chromium paints less than the window height, so render taller and crop:
  chrome --headless --no-sandbox --hide-scrollbars --window-size=1280,900 \\
         --screenshot=/tmp/sp.png assets/social_preview.html
  python3 -c "from PIL import Image; Image.open('/tmp/sp.png').convert('RGB').crop((0, 0, 1280, 640)).save('assets/social_preview.png')"
"""
import os

N = 3
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "Helvetica, Arial, sans-serif"
LACE = "#d9480f"        # lace colour
EYELET = "#212529"
FORBID = "#c92a2a"


def eyelet_pos(e, x_left, x_right, y_top, dy):
    """Centre of eyelet e (1..2N)."""
    if e <= N:
        return x_left, y_top + (e - 1) * dy
    row = 2 * N + 1 - e
    return x_right, y_top + (row - 1) * dy


def panel(order, x0, y0, scale=1.0, title=None, step_labels=True):
    """SVG fragment: eyelets, forbidden horizontals and the lace for `order`."""
    xl, xr = x0 + 40 * scale, x0 + 220 * scale
    yt, dy, r = y0 + 50 * scale, 80 * scale, 13 * scale
    out = []
    if title:
        out.append(f'<text x="{x0 + 130 * scale:.1f}" y="{y0 + 12 * scale:.1f}" font-family="{FONT}" '
                   f'font-size="{17 * scale:.1f}" text-anchor="middle" fill="#212529">{title}</text>')
    # forbidden horizontals: rows 2..N
    for k in range(2, N + 1):
        (ax, ay), (bx, by) = eyelet_pos(k, xl, xr, yt, dy), eyelet_pos(2 * N + 1 - k, xl, xr, yt, dy)
        out.append(f'<line x1="{ax + r:.1f}" y1="{ay:.1f}" x2="{bx - r:.1f}" y2="{by:.1f}" stroke="{FORBID}" '
                   f'stroke-width="{2 * scale:.1f}" stroke-dasharray="{6 * scale:.1f} {5 * scale:.1f}" opacity="0.55"/>')
    # lace segments with arrowheads
    for i in range(len(order) - 1):
        (ax, ay) = eyelet_pos(order[i], xl, xr, yt, dy)
        (bx, by) = eyelet_pos(order[i + 1], xl, xr, yt, dy)
        dx, dyy = bx - ax, by - ay
        d = (dx * dx + dyy * dyy) ** 0.5
        ux, uy = dx / d, dyy / d
        sx, sy, ex, ey = ax + ux * r, ay + uy * r, bx - ux * (r + 4 * scale), by - uy * (r + 4 * scale)
        out.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{LACE}" '
                   f'stroke-width="{3.2 * scale:.1f}" stroke-linecap="round" marker-end="url(#arrow)"/>')
        if step_labels:
            mx, my = (ax + bx) / 2 - uy * 13 * scale, (ay + by) / 2 + ux * 13 * scale
            out.append(f'<text x="{mx:.1f}" y="{my + 5 * scale:.1f}" font-family="{FONT}" font-size="{13 * scale:.1f}" '
                       f'text-anchor="middle" fill="{LACE}" font-weight="bold">{i + 1}</text>')
    # eyelets
    for e in range(1, 2 * N + 1):
        x, y = eyelet_pos(e, xl, xr, yt, dy)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#ffffff" stroke="{EYELET}" '
                   f'stroke-width="{2.2 * scale:.1f}"/>')
        out.append(f'<text x="{x:.1f}" y="{y + 5 * scale:.1f}" font-family="{FONT}" font-size="{14 * scale:.1f}" '
                   f'text-anchor="middle" fill="{EYELET}">{e}</text>')
    return "\n".join(out)


ARROW = (f'<defs><marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" '
         f'orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="{LACE}"/></marker></defs>')


def lacing_figure():
    w, h = 640, 420
    a, b = (1, 2, 4, 5, 3, 6), (1, 4, 2, 3, 5, 6)   # a lacing and its mirror image
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        ARROW,
        f'<rect x="0" y="0" width="{w}" height="{h}" rx="14" fill="#ffffff"/>',
        f'<text x="{w / 2}" y="34" font-family="{FONT}" font-size="20" text-anchor="middle" fill="#212529" '
        f'font-weight="bold">A072503, n = 3: one lacing and its mirror image</text>',
        panel(a, 40, 62, title="1 → 2 → 4 → 5 → 3 → 6"),
        panel(b, 340, 62, title="1 → 4 → 2 → 3 → 5 → 6"),
        f'<text x="{w / 2}" y="350" font-family="{FONT}" font-size="14" text-anchor="middle" fill="#495057">'
        f'Dashed red: forbidden horizontal connections (2–5, 3–4).</text>',
        f'<text x="{w / 2}" y="372" font-family="{FONT}" font-size="14" text-anchor="middle" fill="#495057">'
        f'No three consecutive eyelets of a lacing on the same side.</text>',
        f'<text x="{w / 2}" y="394" font-family="{FONT}" font-size="14" text-anchor="middle" fill="#495057">'
        f'n = 3 has 6 such lacings = 3 mirror pairs, so a(3) = 3.</text>',
        '</svg>',
    ]
    return "\n".join(parts)


def social_preview():
    w, h = 1280, 640
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        ARROW,
        f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>',
        f'<rect x="0" y="0" width="{w}" height="14" fill="{LACE}"/>',
        f'<text x="80" y="150" font-family="{FONT}" font-size="76" font-weight="bold" fill="#212529">OEIS A072503</text>',
        f'<text x="80" y="210" font-family="{FONT}" font-size="34" fill="#495057">Shoe lacings with no horizontal connections</text>',
        f'<text x="80" y="320" font-family="{FONT}" font-size="30" fill="#495057">New terms a(10) … a(400), e.g.</text>',
        f'<text x="80" y="380" font-family="{FONT}" font-size="46" font-weight="bold" fill="{LACE}">a(10) = 36441019601280</text>',
        f'<text x="80" y="470" font-family="{FONT}" font-size="27" fill="#212529">Two independent exact methods agree for n = 3..400</text>',
        f'<text x="80" y="512" font-family="{FONT}" font-size="27" fill="#212529">Computed with Claude Code</text>',
        f'<text x="80" y="590" font-family="{FONT}" font-size="24" fill="#868e96">github.com/kanestar2/oeis-a072503</text>',
        panel((1, 2, 4, 5, 3, 6), 860, 150, scale=1.45, step_labels=False),
        '</svg>',
    ]
    return "\n".join(parts)


if __name__ == "__main__":
    with open(os.path.join(HERE, "lacing_n3.svg"), "w", encoding="utf-8") as f:
        f.write(lacing_figure() + "\n")
    svg = social_preview()
    with open(os.path.join(HERE, "social_preview.svg"), "w", encoding="utf-8") as f:
        f.write(svg + "\n")
    with open(os.path.join(HERE, "social_preview.html"), "w", encoding="utf-8") as f:
        f.write('<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;padding:0;'
                'background:#fff}</style></head><body>' + svg + '</body></html>\n')
    print("written: lacing_n3.svg, social_preview.svg, social_preview.html")
