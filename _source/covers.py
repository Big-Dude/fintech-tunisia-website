"""Original cover illustrations for Fintech Tunisia articles (pure SVG, no external assets)."""
import math, random, hashlib, html

W, H = 1200, 630

PALETTES = {
    # bg1, bg2, accent, accent2
    "ecosystem":  ("#141c33", "#24335c", "#e31e24", "#ffd166"),
    "regulation": ("#1d1f2b", "#3a3d52", "#f2b134", "#e31e24"),
    "payments":   ("#b3141a", "#e31e24", "#ffd166", "#111111"),
    "banking":    ("#08303d", "#0f5268", "#4fd1e8", "#e31e24"),
    "inclusion":  ("#3b0f6b", "#6a2bb0", "#ffb703", "#ff6b6b"),
    "funding":    ("#10301f", "#1d5a3a", "#8be0b0", "#ffd166"),
    "africa":     ("#6d2a0c", "#b04a17", "#ffc46b", "#ffffff"),
    "startups":   ("#0f0f10", "#2a2a2e", "#e31e24", "#ffd166"),
}

L = "#ffffff"


def rng_for(seed):
    return random.Random(int(hashlib.md5(seed.encode()).hexdigest()[:8], 16))


# ---------- geography (lon, lat) ----------
TUNISIA = [(8.62, 36.94), (9.18, 37.17), (9.85, 37.33), (10.15, 37.05), (10.33, 36.85), (10.6, 36.88),
           (11.05, 37.08), (11.1, 36.85), (10.62, 36.42), (10.5, 36.2), (10.65, 35.85), (11.05, 35.6),
           (11.07, 35.25), (10.75, 34.75), (10.35, 34.42), (10.05, 34.15), (10.15, 33.75), (10.75, 33.6),
           (11.1, 33.45), (11.25, 33.2), (11.55, 33.17), (11.5, 32.6), (10.95, 32.3), (10.35, 31.75),
           (10.25, 30.95), (9.5, 30.23), (9.05, 32.1), (8.3, 32.55), (7.6, 33.3), (7.52, 33.85), (8.1, 34.3),
           (8.25, 34.65), (8.42, 35.25), (8.3, 35.75), (8.4, 36.45)]
AFRICA = [(-17.5, 14.7), (-16.9, 21.3), (-13.2, 27.6), (-9.8, 29.9), (-6.8, 34.0), (-5.9, 35.8),
          (-1.9, 35.1), (3.0, 36.8), (8.6, 36.9), (10.3, 37.3), (11.1, 36.8), (10.1, 34.2), (11.6, 33.2),
          (15.2, 32.3), (19.9, 30.9), (20.1, 32.4), (23.1, 32.6), (25.2, 31.6), (29.0, 30.9), (32.3, 31.3),
          (34.2, 27.8), (35.6, 23.8), (37.4, 18.6), (39.2, 15.6), (43.3, 12.6), (44.4, 10.4), (51.3, 11.8),
          (51.0, 10.4), (48.0, 4.9), (44.0, 1.0), (40.9, -2.1), (39.2, -6.5), (40.4, -10.5), (40.6, -15.2),
          (36.5, -19.0), (35.3, -22.3), (35.5, -24.0), (32.9, -26.0), (32.4, -28.6), (30.0, -31.3),
          (27.5, -33.2), (25.6, -34.0), (22.0, -34.1), (20.0, -34.8), (18.4, -34.1), (17.9, -31.5),
          (16.5, -28.6), (15.2, -26.6), (14.5, -22.9), (11.8, -17.3), (13.6, -11.6), (12.3, -6.1),
          (12.0, -5.0), (9.6, -1.0), (9.8, 2.4), (8.7, 4.5), (6.0, 4.3), (4.4, 6.4), (2.2, 6.3), (-0.9, 5.4),
          (-3.0, 5.1), (-7.5, 4.4), (-9.3, 5.6), (-11.4, 6.9), (-13.3, 9.0), (-15.1, 10.9), (-16.8, 12.6)]


def project(points, box, pad=10, lat_scale=True):
    x0, y0, bw, bh = box
    meanlat = sum(p[1] for p in points) / len(points)
    k = math.cos(math.radians(meanlat)) if lat_scale else 1
    xs = [p[0] * k for p in points]; ys = [-p[1] for p in points]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    s = min((bw - 2 * pad) / (maxx - minx), (bh - 2 * pad) / (maxy - miny))
    ox = x0 + (bw - (maxx - minx) * s) / 2; oy = y0 + (bh - (maxy - miny) * s) / 2
    f = lambda lon, lat: (ox + (lon * k - minx) * s, oy + (-lat - miny) * s)
    return [f(*p) for p in points], f


def poly(pts):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


# ---------- motifs: each draws inside a 400x400 box ----------
def m_map_tunisia(c, r):
    pts, f = project(TUNISIA, (60, 0, 280, 400), pad=6)
    out = [f'<path d="{poly(pts)}" fill="{L}" fill-opacity=".14" stroke="{L}" stroke-width="5" stroke-linejoin="round"/>']
    cities = [(10.18, 36.8), (10.64, 35.83), (10.76, 34.74), (10.1, 33.88), (8.78, 36.18), (9.4, 34.6)]
    cp = [f(*p) for p in cities]
    for i in range(len(cp)):
        for j in range(i + 1, len(cp)):
            if r.random() < .45:
                out.append(f'<line x1="{cp[i][0]:.1f}" y1="{cp[i][1]:.1f}" x2="{cp[j][0]:.1f}" y2="{cp[j][1]:.1f}" stroke="{c[2]}" stroke-opacity=".7" stroke-width="2.5" stroke-dasharray="6 6"/>')
    for i, (x, y) in enumerate(cp):
        rad = 14 if i == 0 else 9
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad*2.2:.0f}" fill="{c[2]}" fill-opacity=".18"/>')
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad}" fill="{c[2]}" stroke="{L}" stroke-width="3"/>')
    return "".join(out)


def m_map_africa(c, r):
    pts, f = project(AFRICA, (10, 10, 380, 380), pad=4)
    out = [f'<path d="{poly(pts)}" fill="{L}" fill-opacity=".14" stroke="{L}" stroke-width="4" stroke-linejoin="round"/>']
    mx, my = f(48, -19.5)
    out.append(f'<ellipse cx="{mx:.1f}" cy="{my:.1f}" rx="9" ry="22" transform="rotate(20 {mx:.1f} {my:.1f})" fill="{L}" fill-opacity=".14" stroke="{L}" stroke-width="3"/>')
    tx, ty = f(10.18, 36.8)
    hubs = [(3.4, 6.5), (36.8, -1.3), (-17.4, 14.7), (31.2, 30.0), (28.0, -26.2), (-7.6, 33.6)]
    for lon, lat in hubs:
        hx, hy = f(lon, lat)
        cx, cy = (tx + hx) / 2 + (hy - ty) * .18, (ty + hy) / 2 - (hx - tx) * .18
        out.append(f'<path d="M{tx:.1f},{ty:.1f} Q{cx:.1f},{cy:.1f} {hx:.1f},{hy:.1f}" fill="none" stroke="{c[2]}" stroke-width="3" stroke-linecap="round" stroke-dasharray="2 8"/>')
        out.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="7" fill="{L}"/>')
    out.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="30" fill="{c[2]}" fill-opacity=".25"/><circle cx="{tx:.1f}" cy="{ty:.1f}" r="12" fill="{c[2]}" stroke="{L}" stroke-width="4"/>')
    return "".join(out)


def m_phone_wallet(c, r):
    o = []
    o.append(f'<g transform="rotate(-14 110 250)"><rect x="20" y="190" width="190" height="118" rx="16" fill="{c[2]}"/>'
             f'<rect x="44" y="222" width="38" height="28" rx="6" fill="{L}" fill-opacity=".85"/>'
             f'<rect x="44" y="272" width="120" height="9" rx="4.5" fill="{L}" fill-opacity=".7"/></g>')
    o.append(f'<rect x="140" y="20" width="180" height="350" rx="30" fill="{c[1]}" stroke="{L}" stroke-width="8"/>')
    o.append(f'<rect x="200" y="34" width="60" height="8" rx="4" fill="{L}" fill-opacity=".6"/>')
    o.append(f'<rect x="162" y="62" width="136" height="70" rx="12" fill="{c[2]}"/>')
    o.append(f'<rect x="176" y="78" width="54" height="8" rx="4" fill="{L}" fill-opacity=".8"/><rect x="176" y="96" width="92" height="20" rx="6" fill="{L}"/>')
    for i in range(4):
        y = 152 + i * 46
        o.append(f'<circle cx="182" cy="{y+14}" r="12" fill="{L}" fill-opacity="{.85 if i%2==0 else .45}"/>'
                 f'<rect x="204" y="{y+4}" width="{60+r.randint(0,25)}" height="8" rx="4" fill="{L}" fill-opacity=".75"/>'
                 f'<rect x="204" y="{y+18}" width="{36+r.randint(0,20)}" height="7" rx="3.5" fill="{L}" fill-opacity=".35"/>'
                 f'<rect x="268" y="{y+8}" width="22" height="10" rx="5" fill="{c[3]}"/>')
    o.append(f'<circle cx="335" cy="315" r="44" fill="{c[3]}" stroke="{L}" stroke-width="6"/>'
             f'<text x="335" y="330" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-weight="800" font-size="38" fill="{c[0]}">DT</text>')
    return "".join(o)


def m_bank_building(c, r):
    o = [f'<path d="M30,130 L200,40 L370,130 Z" fill="{L}" fill-opacity=".9"/>',
         f'<circle cx="200" cy="100" r="16" fill="{c[2]}"/>',
         f'<rect x="45" y="134" width="310" height="22" rx="4" fill="{L}" fill-opacity=".9"/>']
    for i in range(5):
        x = 62 + i * 60
        o.append(f'<rect x="{x}" y="166" width="34" height="140" rx="5" fill="{L}" fill-opacity="{.75 if i%2 else .55}"/>')
    o.append(f'<rect x="35" y="312" width="330" height="20" rx="4" fill="{L}" fill-opacity=".9"/><rect x="15" y="338" width="370" height="22" rx="4" fill="{c[2]}"/>')
    nodes = [(60, 30), (340, 24), (385, 92), (14, 86)]
    for x, y in nodes:
        o.append(f'<line x1="200" y1="40" x2="{x}" y2="{y}" stroke="{c[2]}" stroke-width="3" stroke-dasharray="4 6"/><circle cx="{x}" cy="{y}" r="9" fill="{c[2]}" stroke="{L}" stroke-width="3"/>')
    return "".join(o)


def _bars(c, r, up=True):
    o = [f'<line x1="30" y1="350" x2="380" y2="350" stroke="{L}" stroke-width="5" stroke-linecap="round"/>']
    n = 6; vals = []
    v = 80 if up else 290
    for i in range(n):
        v = v + (r.randint(25, 55) if up else -r.randint(20, 50)); v = max(40, min(300, v)); vals.append(v)
    tops = []
    for i, v in enumerate(vals):
        x = 45 + i * 56
        o.append(f'<rect x="{x}" y="{350-v}" width="38" height="{v}" rx="7" fill="{L}" fill-opacity="{.35 + .1*i if up else .85 - .1*i:.2f}"/>')
        tops.append((x + 19, 350 - v - 22))
    o.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in tops)}" fill="none" stroke="{c[2]}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
    x1, y1 = tops[-2]; x2, y2 = tops[-1]
    ang = math.atan2(y2 - y1, x2 - x1)
    pts = [(x2 + 26 * math.cos(ang), y2 + 26 * math.sin(ang)), (x2 + 18 * math.cos(ang + 2.3), y2 + 18 * math.sin(ang + 2.3)), (x2 + 18 * math.cos(ang - 2.3), y2 + 18 * math.sin(ang - 2.3))]
    o.append(f'<path d="{poly(pts)}" fill="{c[2]}"/>')
    for x, y in tops:
        o.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{c[2]}" stroke="{L}" stroke-width="3"/>')
    return "".join(o)


def m_chart_up(c, r): return _bars(c, r, True)
def m_chart_down(c, r): return _bars(c, r, False)


def m_shield_lock(c, r):
    o = []
    for i in range(6):
        y = 60 + i * 55; side = -1 if i % 2 else 1
        x0 = 0 if side == 1 else 400
        o.append(f'<path d="M{x0},{y} H{60 if side==1 else 340} v{20 if i%3 else -20}" fill="none" stroke="{c[2]}" stroke-opacity=".6" stroke-width="3"/><circle cx="{x0}" cy="{y}" r="5" fill="{c[2]}"/>')
    o.append(f'<path d="M200,25 L345,78 L335,210 Q315,315 200,375 Q85,315 65,210 L55,78 Z" fill="{L}" fill-opacity=".14" stroke="{L}" stroke-width="8" stroke-linejoin="round"/>')
    o.append(f'<path d="M168,190 V158 a32,32 0 0 1 64,0 V190" fill="none" stroke="{L}" stroke-width="14" stroke-linecap="round"/>')
    o.append(f'<rect x="140" y="186" width="120" height="100" rx="16" fill="{c[2]}"/><circle cx="200" cy="226" r="14" fill="{c[0]}"/><rect x="194" y="232" width="12" height="30" rx="5" fill="{c[0]}"/>')
    return "".join(o)


def m_network_nodes(c, r):
    pts = []
    tries = 0
    while len(pts) < 11 and tries < 500:
        tries += 1
        p = (r.uniform(30, 370), r.uniform(30, 370))
        if all(math.dist(p, q) > 85 for q in pts): pts.append(p)
    o = []
    edges = set()
    for i, p in enumerate(pts):
        near = sorted(range(len(pts)), key=lambda j: math.dist(p, pts[j]))[1:3]
        for j in near: edges.add(tuple(sorted((i, j))))
    for i, j in edges:
        o.append(f'<line x1="{pts[i][0]:.0f}" y1="{pts[i][1]:.0f}" x2="{pts[j][0]:.0f}" y2="{pts[j][1]:.0f}" stroke="{L}" stroke-opacity=".45" stroke-width="3"/>')
    big = max(range(len(pts)), key=lambda i: -math.dist(pts[i], (200, 200)))
    for i, (x, y) in enumerate(pts):
        if i == big:
            o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="46" fill="{c[2]}" fill-opacity=".2"/><circle cx="{x:.0f}" cy="{y:.0f}" r="28" fill="{c[2]}" stroke="{L}" stroke-width="5"/>')
        else:
            rad = r.choice([10, 13, 16, 20])
            fill = c[2] if r.random() < .35 else L
            o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rad}" fill="{fill}" fill-opacity="{.95 if fill==L else 1}"/>')
    return "".join(o)


def m_coins(c, r):
    o = []
    for sx, n in [(85, r.randint(3, 5)), (200, r.randint(6, 8)), (315, r.randint(4, 6))]:
        base = 340
        for k in range(n):
            y = base - k * 26
            o.append(f'<rect x="{sx-58}" y="{y-14}" width="116" height="26" fill="{c[2]}"/>'
                     f'<ellipse cx="{sx}" cy="{y+12}" rx="58" ry="17" fill="{c[2]}" stroke="{c[0]}" stroke-width="3"/>'
                     f'<ellipse cx="{sx}" cy="{y-14}" rx="58" ry="17" fill="{c[3] if k==n-1 else c[2]}" stroke="{c[0]}" stroke-width="3"/>')
        top = base - (n - 1) * 26 - 14
        o.append(f'<text x="{sx}" y="{top+8}" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-weight="800" font-size="20" fill="{c[0]}">DT</text>')
    o.append(f'<path d="M40,60 C120,10 260,20 330,70" fill="none" stroke="{L}" stroke-width="5" stroke-linecap="round" stroke-dasharray="3 12"/>')
    o.append(f'<path d="M330,70 l-24,-2 l12,-18 Z" fill="{L}"/>')
    return "".join(o)


def m_globe_links(c, r):
    o = [f'<circle cx="200" cy="200" r="160" fill="{L}" fill-opacity=".08" stroke="{L}" stroke-width="6"/>']
    for k in (0.35, 0.7):
        o.append(f'<ellipse cx="200" cy="200" rx="{160*k:.0f}" ry="160" fill="none" stroke="{L}" stroke-opacity=".45" stroke-width="3"/>')
    for dy in (-90, 0, 90):
        rx = math.sqrt(160 ** 2 - dy ** 2)
        o.append(f'<ellipse cx="200" cy="{200+dy}" rx="{rx:.0f}" ry="{rx*0.18:.0f}" fill="none" stroke="{L}" stroke-opacity=".45" stroke-width="3"/>')
    pts = [(r.uniform(80, 320), r.uniform(80, 320)) for _ in range(5)]
    for i in range(len(pts) - 1):
        (x1, y1), (x2, y2) = pts[i], pts[i + 1]
        o.append(f'<path d="M{x1:.0f},{y1:.0f} Q{(x1+x2)/2:.0f},{min(y1,y2)-90:.0f} {x2:.0f},{y2:.0f}" fill="none" stroke="{c[2]}" stroke-width="5" stroke-linecap="round"/>')
    for x, y in pts:
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="11" fill="{c[2]}" stroke="{L}" stroke-width="4"/>')
    return "".join(o)


def m_scales_law(c, r):
    tilt = r.choice([-8, 8])
    o = [f'<rect x="192" y="70" width="16" height="270" rx="6" fill="{L}"/>',
         f'<path d="M120,370 L280,370 L250,335 L150,335 Z" fill="{L}"/>',
         f'<circle cx="200" cy="62" r="20" fill="{c[2]}" stroke="{L}" stroke-width="5"/>']
    g = [f'<rect x="50" y="88" width="300" height="12" rx="6" fill="{L}"/>']
    for px in (70, 330):
        g.append(f'<line x1="{px}" y1="98" x2="{px-45}" y2="215" stroke="{L}" stroke-width="3"/><line x1="{px}" y1="98" x2="{px+45}" y2="215" stroke="{L}" stroke-width="3"/>'
                 f'<path d="M{px-60},215 A60,30 0 0 0 {px+60},215 Z" fill="{c[2]}"/>')
    o.append(f'<g transform="rotate({tilt} 200 94)">{"".join(g)}</g>')
    return "".join(o)


def m_rocket(c, r):
    o = []
    for i in range(7):
        x = 60 + i * 22 + r.randint(-8, 8); y = 340 - i * 22 + r.randint(-8, 8)
        o.append(f'<circle cx="{x}" cy="{y}" r="{26-i*2.5:.0f}" fill="{L}" fill-opacity="{.12+i*.03:.2f}"/>')
    g = [f'<path d="M200,30 C250,80 258,170 250,250 L150,250 C142,170 150,80 200,30 Z" fill="{L}"/>',
         f'<circle cx="200" cy="130" r="26" fill="{c[2]}" stroke="{c[0]}" stroke-width="7"/>',
         f'<path d="M150,195 L105,270 L152,252 Z" fill="{c[2]}"/><path d="M250,195 L295,270 L248,252 Z" fill="{c[2]}"/>',
         f'<path d="M165,256 Q200,360 235,256 Z" fill="{c[3]}"/><path d="M182,256 Q200,315 218,256 Z" fill="{L}"/>']
    o.append(f'<g transform="rotate(40 200 200)">{"".join(g)}</g>')
    for i in range(5):
        x, y = r.uniform(250, 390), r.uniform(20, 160)
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.choice([3,4,5])}" fill="{L}"/>')
    return "".join(o)


def m_people(c, r):
    o = []
    pos = [(110, 150, 1), (290, 150, 1), (200, 120, 1.25), (70, 290, .9), (200, 290, 1), (330, 290, .9)]
    for i, (x, y, s) in enumerate(pos):
        fill = c[2] if i in (2, 4) else L
        op = 1 if fill == c[2] else .9
        o.append(f'<circle cx="{x}" cy="{y-30*s:.0f}" r="{28*s:.0f}" fill="{fill}" fill-opacity="{op}"/>'
                 f'<path d="M{x-48*s:.0f},{y+60*s:.0f} Q{x-48*s:.0f},{y+4*s:.0f} {x},{y+4*s:.0f} Q{x+48*s:.0f},{y+4*s:.0f} {x+48*s:.0f},{y+60*s:.0f} Z" fill="{fill}" fill-opacity="{op}"/>')
    o.append(f'<path d="M110,215 Q200,250 290,215" fill="none" stroke="{c[3]}" stroke-width="4" stroke-dasharray="4 8"/>')
    return "".join(o)


def m_document(c, r):
    o = [f'<g transform="rotate(-6 200 200)"><rect x="70" y="40" width="210" height="290" rx="14" fill="{L}" fill-opacity=".3"/></g>',
         f'<path d="M110,30 H270 L320,80 V350 a14,14 0 0 1 -14,14 H110 a14,14 0 0 1 -14,-14 V44 a14,14 0 0 1 14,-14 Z" fill="{L}"/>',
         f'<path d="M270,30 V80 H320" fill="{c[0]}" fill-opacity=".15"/>',
         f'<rect x="124" y="64" width="110" height="16" rx="6" fill="{c[2]}"/>']
    for i in range(7):
        w = r.randint(120, 190) if i % 3 else 190
        o.append(f'<rect x="124" y="{104+i*28}" width="{w}" height="9" rx="4.5" fill="{c[0]}" fill-opacity=".25"/>')
    o.append(f'<circle cx="300" cy="320" r="50" fill="{c[2]}" stroke="{L}" stroke-width="6"/><path d="M278,320 l16,16 l28,-32" fill="none" stroke="{L}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')
    return "".join(o)


def m_chip_ai(c, r):
    o = []
    for i in range(5):
        p = 130 + i * 35
        for (x1, y1, x2, y2) in [(p, 110, p, 60), (p, 290, p, 340), (110, p, 60, p), (290, p, 340, p)]:
            o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{L}" stroke-width="7" stroke-linecap="round"/>')
        for (x, y) in [(p, 40 - (i % 2) * 14), (p, 360 + (i % 2) * 14), (40 - (i % 2) * 14, p), (360 + (i % 2) * 14, p)]:
            if r.random() < .55:
                o.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{c[2]}"/>')
    o.append(f'<rect x="100" y="100" width="200" height="200" rx="26" fill="{c[1]}" stroke="{L}" stroke-width="8"/>')
    o.append(f'<rect x="132" y="132" width="136" height="136" rx="16" fill="{c[2]}"/>')
    o.append(f'<text x="200" y="224" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-weight="800" font-size="62" fill="{c[0]}">AI</text>')
    return "".join(o)


def m_handshake(c, r):
    o = [f'<rect x="20" y="110" width="170" height="210" rx="18" fill="{L}"/>',
         f'<rect x="210" y="80" width="170" height="210" rx="18" fill="{c[2]}"/>']
    for i in range(4):
        o.append(f'<rect x="42" y="{150+i*32}" width="{r.randint(80,126)}" height="10" rx="5" fill="{c[0]}" fill-opacity=".3"/>')
        o.append(f'<rect x="232" y="{120+i*32}" width="{r.randint(80,126)}" height="10" rx="5" fill="{L}" fill-opacity=".7"/>')
    o.append(f'<circle cx="200" cy="205" r="52" fill="{c[0]}" stroke="{L}" stroke-width="6"/>')
    o.append(f'<path d="M178,190 h44 l-12,-12 M222,220 h-44 l12,12" fill="none" stroke="{L}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>')
    return "".join(o)


def m_card(c, r):
    return (f'<g transform="rotate(-10 200 200)"><rect x="70" y="80" width="280" height="175" rx="20" fill="{L}" fill-opacity=".3"/></g>'
            f'<rect x="50" y="130" width="300" height="190" rx="22" fill="{c[2]}"/>'
            f'<rect x="80" y="180" width="54" height="40" rx="8" fill="{L}" fill-opacity=".85"/>'
            f'<path d="M290,175 a20,20 0 0 1 0,40 M302,163 a34,34 0 0 1 0,64" fill="none" stroke="{L}" stroke-width="6" stroke-linecap="round"/>'
            f'<rect x="80" y="250" width="200" height="12" rx="6" fill="{L}" fill-opacity=".8"/><rect x="80" y="280" width="90" height="10" rx="5" fill="{L}" fill-opacity=".5"/>')


MOTIFS = {k[2:].replace("_", "-"): v for k, v in globals().items() if k.startswith("m_")}


def background(c, r, uid):
    o = [f'<defs><linearGradient id="g{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c[0]}"/><stop offset="1" stop-color="{c[1]}"/></linearGradient>'
         f'<pattern id="p{uid}" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.6" fill="{L}" fill-opacity=".10"/></pattern></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#g{uid})"/><rect width="{W}" height="{H}" fill="url(#p{uid})"/>']
    for _ in range(2):
        x, y, rad = r.randint(0, W), r.randint(0, H), r.randint(160, 300)
        o.append(f'<circle cx="{x}" cy="{y}" r="{rad}" fill="{c[2]}" fill-opacity=".10"/>')
    for _ in range(2):
        x, y, rad = r.randint(0, W), r.randint(0, H), r.randint(90, 220)
        o.append(f'<circle cx="{x}" cy="{y}" r="{rad}" fill="none" stroke="{L}" stroke-opacity=".10" stroke-width="2"/>')
    return "".join(o)


def cover_svg(slug, category, motif, title=None, label=None, site="fintechtunisia.com", variant=0, rtl=False):
    """Return SVG text. If title given, produces a social (OG) card with text on the left."""
    c = PALETTES.get(category, PALETTES["ecosystem"])
    if variant % 2 == 1 and category != "payments": c = (c[0], c[1], c[3], c[2])
    if variant >= 2: c = (c[1], c[0], c[2], c[3])
    r = rng_for(slug)
    uid = hashlib.md5(slug.encode()).hexdigest()[:6]
    fn = MOTIFS.get(motif, m_network_nodes)
    parts = [background(c, r, uid)]
    if title is None:
        flip = f" translate(400 0) scale(-1 1)" if variant % 2 == 1 and motif not in ("map-tunisia", "map-africa", "chip-ai", "coins", "phone-wallet") else ""
        parts.append(f'<g transform="translate({W/2+90-200*1.3:.0f} {H/2-200*1.3:.0f}) scale(1.3){flip}">{fn(c, r)}</g>')
    else:
        mx = 30 if rtl else W - 430 - 30
        parts.append(f'<g transform="translate({mx} {H/2-200*1.0:.0f}) scale(1.0)" opacity=".95">{fn(c, r)}</g>')
        size = 54 if not rtl else 58
        per = 22 if not rtl else 24
        def wrap(t, n):
            words, lines, cur = t.split(), [], ""
            for w in words:
                if len(cur) + len(w) + 1 > n and cur: lines.append(cur); cur = w
                else: cur = (cur + " " + w).strip()
            lines.append(cur); return lines
        lines = wrap(title, per)
        if len(lines) > 4: size = size - 10; lines = wrap(title, per + 5)
        if len(lines) > 5: lines = lines[:5]; lines[-1] += "…"
        y0 = H / 2 - (len(lines) * size * 1.2) / 2 + size * .85
        font = "'IBM Plex Sans Arabic',Inter,Arial,sans-serif" if rtl else "Inter,Arial,sans-serif"
        lab = (label or "") if rtl else (label or "").upper()
        pill_w = len(lab) * (13 if rtl else 12) + 40
        tx = W - 70 if rtl else 70
        anchor = ' direction="rtl" text-anchor="start"' if rtl else ""
        px = W - 70 - pill_w if rtl else 70
        parts.append(f'<rect x="{px}" y="{y0-size*0.85-70:.0f}" width="{pill_w}" height="40" rx="20" fill="{c[2]}"/>')
        parts.append(f'<text x="{px + pill_w - 20 if rtl else 90}" y="{y0-size*0.85-43:.0f}"{anchor} font-family="{font}" font-weight="700" font-size="19" letter-spacing="{0 if rtl else 1.5}" fill="{c[0]}">{html.escape(lab)}</text>')
        for i, line in enumerate(lines):
            parts.append(f'<text x="{tx}" y="{y0 + i*size*1.2:.0f}"{anchor} font-family="{font}" font-weight="700" font-size="{size}" fill="{L}">{html.escape(line)}</text>')
        bx = W - 70 - 34 if rtl else 70
        parts.append(f'<rect x="{bx}" y="{H-82}" width="34" height="34" rx="8" fill="#e31e24"/><text x="{bx+17}" y="{H-58}" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-weight="800" font-size="16" fill="#fff">FT</text>')
        sx = bx - 12 if rtl else 116
        parts.append(f'<text x="{sx}" y="{H-58}"{" text-anchor=\"end\"" if rtl else ""} font-family="Inter,Arial,sans-serif" font-weight="600" font-size="22" fill="{L}" fill-opacity=".85">{site}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">{"".join(parts)}</svg>'
