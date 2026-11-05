import math, sys
W, H = 1200, 600
BG = "#1b3a82"
SANS = "'Geist', system-ui, sans-serif"
MONO = "'Geist Mono', ui-monospace, monospace"

def t(x, y, s, size=13, font=MONO, weight=500, anchor="start", op=1, ls=0):
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="#fff" fill-opacity="{op}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>'

def line(x1, y1, x2, y2, w=1.5, op=1, dash=None, extra=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#fff" stroke-width="{w}" stroke-opacity="{op}"{d}{extra}/>'

def circle(cx, cy, r, w=1.5, op=1, fill="none", dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="#fff" stroke-width="{w}" stroke-opacity="{op}"{d}/>'

b = ['<defs><pattern id="g" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#fff" stroke-opacity="0.08" stroke-width="1"/></pattern>'
     '<pattern id="h" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0 0V7" stroke="#fff" stroke-width="1.5" stroke-opacity="0.75"/></pattern>'
     '<marker id="ar" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 1L10 5L0 9Z" fill="#fff"/></marker>'
     '<path id="lab" d="M 110 300 A 180 180 0 0 0 470 300"/></defs>',
     f'<rect width="{W}" height="{H}" fill="{BG}"/><rect width="{W}" height="{H}" fill="url(#g)"/>',
     f'<rect x="20" y="20" width="{W-40}" height="{H-40}" fill="none" stroke="#fff" stroke-width="2.5"/>',
     f'<rect x="36" y="36" width="{W-72}" height="{H-72}" fill="none" stroke="#fff" stroke-width="1" stroke-opacity="0.8"/>']
for i in range(6):
    x0 = 36 + i * (W - 72) / 6
    if i: b += [line(x0, 20, x0, 36), line(x0, H - 36, x0, H - 20)]
    cx = x0 + (W - 72) / 12
    b += [t(cx, 32, str(i + 1), 10, anchor="middle", op=0.8), t(cx, H - 24, str(i + 1), 10, anchor="middle", op=0.8)]
for i, L in enumerate("ABC"):
    y0 = 36 + i * (H - 72) / 3
    if i: b += [line(20, y0, 36, y0), line(W - 36, y0, W - 20, y0)]
    cy = y0 + (H - 72) / 6 + 4
    b += [t(28, cy, L, 10, anchor="middle", op=0.8), t(W - 28, cy, L, 10, anchor="middle", op=0.8)]

# roundel
CX, CY = 290, 300
b += [circle(CX, CY, 212, 5), circle(CX, CY, 196, 1, 0.6)]
# the record, drafted
R = 132
b.append(circle(CX, CY, R, 3.5))
for r in range(58, R - 6, 9):
    b.append(circle(CX, CY, r, 0.8, 0.45))
b.append(circle(CX, CY, 42, 2.5, fill="url(#h)"))
b.append(circle(CX, CY, 42, 2.5))
b.append(circle(CX, CY, 6, 2, fill=BG))
# centre lines
b += [line(CX - R - 22, CY, CX + R + 22, CY, 1, 0.8, "14 4 3 4"), line(CX, CY - R - 22, CX, CY + R + 22, 1, 0.8, "14 4 3 4")]
# dimension: diameter over the top
b += [line(CX - R, CY - R - 6, CX - R, CY - 6, 1, 0.8), line(CX + R, CY - R - 6, CX + R, CY - 6, 1, 0.8)]
b.append(line(CX - R, CY - R - 14, CX + R, CY - R - 14, 1.2, 1, None, ' marker-start="url(#ar)" marker-end="url(#ar)"'))
b.append(f'<rect x="{CX-42}" y="{CY-R-24}" width="84" height="20" fill="{BG}"/>')
b.append(t(CX, CY - R - 9, "33⅓ RPM", 12, anchor="middle", ls=0.5))
# tone arm, dashed (hidden line)
b.append(circle(CX + 140, CY - 108, 9, 1.5))
b.append(f'<path d="M {CX+140} {CY-108} L {CX+146} {CY-10} L {CX+98} {CY+52}" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="7 5"/>')
b.append(f'<rect x="{CX+86}" y="{CY+44}" width="20" height="12" transform="rotate(-50 {CX+96} {CY+50})" fill="{BG}" stroke="#fff" stroke-width="1.5"/>')
b.append(f'<text font-family="{MONO}" font-size="14" font-weight="500" fill="#fff" letter-spacing="5"><textPath href="#lab" startOffset="50%" text-anchor="middle">NOW PLAYING</textPath></text>')

X = 640
b.append(t(X, 112, "DWG. TEL-NP · FIG. 1", 12, op=0.75, ls=2.4))
b.append(t(X - 3, 196, "now playing", 72, SANS, 600, ls=-2.8))
b += [line(X, 218, X, 242, 1.2, 0.8), line(X + 400, 218, X + 400, 242, 1.2, 0.8)]
b.append(line(X, 232, X + 400, 232, 1.2, 1, None, ' marker-start="url(#ar)" marker-end="url(#ar)"'))
b.append(f'<rect x="{X+140}" y="222" width="120" height="20" fill="{BG}"/>')
b.append(t(X + 200, 237, "ORCA PLUGIN", 11, anchor="middle", ls=2))
for i, s in enumerate(["What your Mac is playing, in Orca.", "Spotify, Music, a browser tab: anything that", "reports to Now Playing, one click from the bar."]):
    b.append(t(X, 288 + i * 27, s, 18, SANS, 400, op=0.92))
b.append(t(X, 410, "NOTES", 11, op=0.75, ls=2.4))
b.append(line(X, 418, X + 230, 418, 1, 0.6))
for i, s in enumerate(["1. READ THE TRACK.", "2. ⏮ BACK.", "3. ⏯ PLAY, PAUSE.", "4. ⏭ NEXT.", "5. KEEP WORKING."]):
    b.append(t(X, 440 + i * 21, s.replace(" ", "&#160;"), 12.5, op=0.95, ls=0.6))
x0, y0, x1, y1 = 900, 440, W - 36, H - 36
b.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="{BG}" stroke="#fff" stroke-width="1.5"/>')
b += [line(x0, y0 + 62, x1, y0 + 62, 1), line(x0 + 116, y0 + 62, x0 + 116, y1, 1), line(x0 + 180, y0 + 62, x0 + 180, y1, 1)]
b.append(t(x0 + 10, y0 + 18, "TITLE", 9, op=0.7, ls=1.5)); b.append(t(x0 + 10, y0 + 48, "now playing", 24, SANS, 600, ls=-0.8))
b.append(t(x1 - 10, y0 + 18, "telchine/orca-now-playing", 9, anchor="end", op=0.7, ls=0.5))
for xx, lab, val in ((x0 + 10, "DWG. NO.", "TEL-NP"), (x0 + 126, "SCALE", "1:1"), (x0 + 190, "SHEET", "1 OF 1")):
    b.append(t(xx, y0 + 78, lab, 9, op=0.7, ls=1.5)); b.append(t(xx, y0 + 100, val, 13))

svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{"".join(b)}</svg>'
open(sys.argv[1], "w").write(svg)
open(sys.argv[2], "w").write('<!doctype html><html><head><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;600&family=Geist+Mono:wght@500&display=block"><style>html,body{margin:0;background:'+BG+'}svg{display:block}</style></head><body>'+svg+'</body></html>')
