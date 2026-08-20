import sys, re, base64, os
sys.path.insert(0, "/tmp/gen")
from leads_data_v5 import LEADS

SRC = "/tmp/gen/master-template-v3.html"
with open(SRC) as f:
    MASTER = f.read()

def b64svg(svg):
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()

def darken(hexcolor, factor=0.65):
    h = hexcolor.lstrip('#')
    r,g,b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return "#{:02x}{:02x}{:02x}".format(int(r*factor), int(g*factor), int(b*factor))

# ---------- before/after: user-supplied AI-generated placeholder photos (same pair used across all sites) ----------
with open("/tmp/gen/assets/before_b64.txt") as _f:
    BEFORE_PHOTO = _f.read().strip()
with open("/tmp/gen/assets/after_b64.txt") as _f:
    AFTER_PHOTO = _f.read().strip()

# ---------- shared hero banner background (common across all 9 sites, replaces per-business hero photo) ----------
with open("/tmp/gen/assets/hero_banner_b64.txt") as _f:
    HERO_BANNER = _f.read().strip()

GALLERY_ICONS = ["panel", "bulb", "tools", "van"]

def gallery_icon(kind, primary, accent, caption):
    pd = darken(primary, 0.7)
    common_defs = f'''<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="{primary}"/><stop offset="1" stop-color="{pd}"/></linearGradient></defs>
<rect width="600" height="600" fill="url(#bg)"/>'''
    if kind == "panel":
        body = '''<rect x="190" y="130" width="220" height="340" rx="14" fill="#f4f5f7" opacity="0.95"/>
<rect x="215" y="160" width="170" height="26" rx="4" fill="#c7cad1"/>
<rect x="215" y="200" width="150" height="12" rx="3" fill="#a7abb5"/>
<rect x="215" y="222" width="150" height="12" rx="3" fill="#a7abb5"/>
<rect x="215" y="244" width="150" height="12" rx="3" fill="#a7abb5"/>
<rect x="215" y="270" width="70" height="60" rx="6" fill="#e2b23d"/>
<rect x="295" y="270" width="70" height="60" rx="6" fill="#e2b23d"/>
<rect x="215" y="340" width="70" height="60" rx="6" fill="#e2b23d"/>
<rect x="295" y="340" width="70" height="60" rx="6" fill="#e2b23d"/>
<rect x="215" y="410" width="150" height="30" rx="4" fill="#c7cad1"/>'''
    elif kind == "bulb":
        body = '''<circle cx="300" cy="250" r="90" fill="#f4f5f7" opacity="0.95"/>
<rect x="272" y="330" width="56" height="46" rx="8" fill="#c7cad1"/>
<rect x="278" y="380" width="44" height="14" rx="4" fill="#a7abb5"/>
<path d="M270 220 L300 260 L330 220" stroke="#e2b23d" stroke-width="10" fill="none" stroke-linecap="round"/>
<line x1="300" y1="130" x2="300" y2="100" stroke="#f4f5f7" stroke-width="8" stroke-linecap="round" opacity="0.7"/>
<line x1="380" y1="170" x2="405" y2="150" stroke="#f4f5f7" stroke-width="8" stroke-linecap="round" opacity="0.7"/>
<line x1="220" y1="170" x2="195" y2="150" stroke="#f4f5f7" stroke-width="8" stroke-linecap="round" opacity="0.7"/>'''
    elif kind == "tools":
        body = '''<g transform="translate(300,260) rotate(-20)"><rect x="-14" y="-140" width="28" height="220" rx="10" fill="#f4f5f7" opacity="0.95"/><rect x="-30" y="-170" width="60" height="46" rx="10" fill="#c7cad1"/></g>
<g transform="translate(300,260) rotate(30)"><rect x="-12" y="-150" width="24" height="230" rx="8" fill="#e2b23d" opacity="0.95"/><circle cx="0" cy="-160" r="26" fill="#c7cad1"/></g>'''
    else:  # van
        body = '''<rect x="130" y="260" width="340" height="120" rx="18" fill="#f4f5f7" opacity="0.95"/>
<rect x="130" y="220" width="150" height="70" rx="14" fill="#f4f5f7" opacity="0.95"/>
<rect x="150" y="235" width="90" height="45" rx="6" fill="#9fc7de"/>
<circle cx="200" cy="390" r="26" fill="#2a2d31"/><circle cx="200" cy="390" r="10" fill="#c7cad1"/>
<circle cx="400" cy="390" r="26" fill="#2a2d31"/><circle cx="400" cy="390" r="10" fill="#c7cad1"/>
<rect x="290" y="290" width="150" height="14" rx="4" fill="#e2b23d"/>'''
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 600 600">{common_defs}{body}' \
          f'<text x="300" y="560" font-family="Arial" font-size="16" fill="#ffffff" text-anchor="middle" opacity="0.85">{caption}</text></svg>'
    return b64svg(svg)

def build_reviews_html(testimonials):
    def card(quote, who, initials):
        return (f'<div class="t-card"><div class="stars">★★★★★</div>'
                f'<p>"{quote}"</p><div class="who"><div class="t-avatar">{initials}</div>'
                f'<div><b>{who}</b><span>Google review</span></div></div></div>')
    cards = [card(q, w, i) for (q, w, i) in testimonials]
    if len(testimonials) >= 3:
        return "\n        ".join(cards + cards), "", ""
    else:
        return "\n        ".join(cards), " static", " static"

outdir = "/tmp/gen/output"
os.makedirs(outdir, exist_ok=True)

for lead in LEADS:
    html = MASTER
    real_photos = lead["photo_urls"][:4]
    photos = list(real_photos)
    while len(photos) < 4:
        idx = len(photos)
        kind = GALLERY_ICONS[idx % len(GALLERY_ICONS)]
        cap = lead["gallery_captions"][idx] if idx < len(lead["gallery_captions"]) else lead["name"]
        photos.append(gallery_icon(kind, lead["primary"], lead["accent"], cap))

    reviews_html, shell_class, track_class = build_reviews_html(lead["testimonials"])
    years_label = lead.get("years_label", "Years serving {{CITY}}")

    tokens = {
        "{{BUSINESS_NAME}}": lead["name"],
        "{{BUSINESS_NAME_URL}}": lead["name_url"],
        "{{CITY}}": lead["city"],
        "{{PHONE}}": lead["phone"],
        "{{PHONE_TEL}}": lead["phone_tel"],
        "{{WHATSAPP_TEL}}": lead["wa_tel"],
        "{{EMAIL}}": lead["email"] if lead["email"] else f"contact-not-yet-found@{lead['slug']}.local",
        "{{RATING}}": lead["rating"],
        "{{REVIEW_COUNT}}": lead["reviews"],
        "{{YEARS_IN_BUSINESS}}": lead["years"],
        "{{LOGO_INITIALS}}": lead["logo"],
        "{{HERO_HEADLINE}}": lead["hero_headline"],
        "{{HERO_IMAGE}}": HERO_BANNER,
        "{{TAGLINE}}": lead["tagline"],
        "{{ABOUT_TEXT}}": lead["about"] + " " + lead["hook"],
        "{{YEAR}}": "2026",
        "{{BRAND_PRIMARY}}": lead["primary"],
        "{{BRAND_PRIMARY_DARK}}": lead["primary_dark"],
        "{{BRAND_ACCENT}}": lead["accent"],
        "{{FACEBOOK_URL}}": "#",
        "{{INSTAGRAM_URL}}": "#",
        "{{LINKEDIN_URL}}": "#",
        "{{BEFORE_IMAGE}}": BEFORE_PHOTO,
        "{{AFTER_IMAGE}}": AFTER_PHOTO,
        "{{REVIEWS_HTML}}": reviews_html,
        "{{MARQUEE_SHELL_CLASS}}": shell_class,
        "{{MARQUEE_TRACK_CLASS}}": track_class,
    }
    for i, (sname, sdesc) in enumerate(lead["services"], start=1):
        tokens[f"{{{{SERVICE_{i}_NAME}}}}"] = sname
        tokens[f"{{{{SERVICE_{i}_DESC}}}}"] = sdesc
    for i, cap in enumerate(lead["gallery_captions"], start=1):
        tokens[f"{{{{GALLERY_IMG_{i}}}}}"] = photos[i-1]
        tokens[f"{{{{GALLERY_CAPTION_{i}}}}}"] = cap
    for i, (q, a) in enumerate(lead["faqs"], start=1):
        tokens[f"{{{{FAQ_{i}_Q}}}}"] = q
        tokens[f"{{{{FAQ_{i}_A}}}}"] = a

    # YEARS_LABEL may itself contain {{CITY}} - resolve CITY first, then substitute label
    years_label_resolved = years_label.replace("{{CITY}}", lead["city"])
    tokens["{{YEARS_LABEL}}"] = years_label_resolved

    for k, v in tokens.items():
        html = html.replace(k, v)

    leftover = set(re.findall(r"\{\{[A-Z0-9_]+\}\}", html))
    if leftover:
        print(f"WARNING {lead['slug']} leftover tokens:", leftover)

    with open(f"{outdir}/{lead['slug']}.html", "w") as f:
        f.write(html)
    print(f"built {lead['slug']}.html  (real gallery photos: {len(real_photos)}/4, testimonials: {len(lead['testimonials'])}, marquee: {'static' if shell_class else 'animated'})")

print("ALL DONE")
