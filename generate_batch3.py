import sys, re, os
sys.path.insert(0, "/tmp/gen")
from leads_data_batch3 import LEADS

SRC = "/tmp/gen/master-template-v3.html"
with open(SRC) as f:
    MASTER = f.read()

with open("/tmp/gen/assets/hero_banner_b64.txt") as f:
    HERO_BANNER = f.read().strip()

# exact original 6 electrician service-icon lines (to be swapped per niche, in order)
ORIG_ICONS = [
 '<svg class="icon" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
 '<svg class="icon" viewBox="0 0 24 24"><path d="M9 2v4M15 2v4M6 8h12v4a6 6 0 0 1-6 6 6 6 0 0 1-6-6V8Z"/><path d="M12 18v4"/></svg>',
 '<svg class="icon" viewBox="0 0 24 24"><path d="M9 18h6M10 22h4M12 2a6 6 0 0 0-4 10.5c.7.7 1 1.4 1 2.5h6c0-1.1.3-1.8 1-2.5A6 6 0 0 0 12 2Z"/></svg>',
 '<svg class="icon" viewBox="0 0 24 24"><path d="m14.7 6.3-3.3 3.3M3 21l6.3-6.3a4 4 0 1 1 5.4-5.4L21 3l-3 3-3.3-3.3"/><path d="M14.7 6.3a4 4 0 1 0 3 3"/></svg>',
 '<svg class="icon" viewBox="0 0 24 24"><path d="M12 3 2 21h20L12 3Z"/><path d="M12 10v4"/><circle cx="12" cy="17.5" r=".6" fill="currentColor" stroke="none"/></svg>',
 '<svg class="icon" viewBox="0 0 24 24"><path d="M3 11 12 3l9 8"/><path d="M5 10v10h14V10"/></svg>',
]

# niche-specific replacement icons, monochrome stroke, same style, 6 per niche in service order
NICHE_ICONS = {
  "Garage Door Company": [
    '<svg class="icon" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M3 14h18"/></svg>',
    '<svg class="icon" viewBox="0 0 24 24"><path d="M6 20c0-5 2-6 2-9s-2-4-2-7M12 20c0-5 2-6 2-9s-2-4-2-7M18 20c0-5 2-6 2-9s-2-4-2-7"/></svg>',
    '<svg class="icon" viewBox="0 0 24 24"><path d="M3 10 12 3l9 7"/><rect x="5" y="10" width="14" height="10" rx="1"/><path d="M5 14h14"/></svg>',
    '<svg class="icon" viewBox="0 0 24 24"><rect x="7" y="3" width="10" height="18" rx="3"/><circle cx="12" cy="8" r="1.3" fill="currentColor" stroke="none"/><path d="M9 13h6M9 16h6"/></svg>',
    '<svg class="icon" viewBox="0 0 24 24"><path d="M12 3 2 21h20L12 3Z"/><path d="M12 10v4"/><circle cx="12" cy="17.5" r=".6" fill="currentColor" stroke="none"/></svg>',
    '<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M8.5 12.5 11 15l4.5-6"/></svg>',
  ],
  "Appliance Repair": [
    '<svg class="icon" viewBox="0 0 24 24"><rect x="6" y="2" width="12" height="20" rx="2"/><path d="M6 11h12"/><circle cx="9" cy="7" r=".6" fill="currentColor" stroke="none"/><circle cx="9" cy="16" r=".6" fill="currentColor" stroke="none"/></svg>',
    '<svg class="icon" viewBox="0 0 24 24"><rect x="4" y="3" width="16" height="18" rx="2"/><circle cx="12" cy="13" r="5"/><path d="M8 6h1"/></svg>',
    '<svg class="icon" viewBox="0 0 24 24"><path d="M12 2c-3 4-5 6.5-5 9.5A5 5 0 0 0 12 17a5 5 0 0 0 5-5.5C17 8.5 15 6 12 2Z"/></svg>',
    '<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/></svg>',
    '<svg class="icon" viewBox="0 0 24 24"><path d="M12 3 4 6.5V11c0 5 3.4 8.4 8 10 4.6-1.6 8-5 8-10V6.5L12 3Z"/><path d="m9 12 2 2 4-4.5"/></svg>',
    '<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M8.5 12.5 11 15l4.5-6"/></svg>',
  ],
  "HVAC Company": [
    '<svg class="icon" viewBox="0 0 24 24"><path d="M12 2c-3 4-5 6.5-5 9.5A5 5 0 0 0 12 17a5 5 0 0 0 5-5.5C17 8.5 15 6 12 2Z"/></svg>',
    '<svg class="icon" viewBox="0 0 24 24"><path d="M12 2v20M4.5 6l15 12M19.5 6l-15 12"/></svg>',
    '<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 8v4l3 2"/><circle cx="12" cy="12" r="1" fill="currentColor" stroke="none"/></svg>',
    '<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="2"/><path d="M12 4c2 1 2 4 0 5M12 20c2-1 2-4 0-5M4 12c1-2 4-2 5 0M20 12c-1 2-4 2-5 0"/></svg>',
    '<svg class="icon" viewBox="0 0 24 24"><path d="M12 3 2 21h20L12 3Z"/><path d="M12 10v4"/><circle cx="12" cy="17.5" r=".6" fill="currentColor" stroke="none"/></svg>',
    '<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3.2"/><path d="M12 4.5v2M12 17.5v2M4.5 12h2M17.5 12h2M6.5 6.5l1.5 1.5M16 16l1.5 1.5M17.5 6.5 16 8M8 16l-1.5 1.5"/></svg>',
  ],
  "Plumber": [
    '<svg class="icon" viewBox="0 0 24 24"><path d="M12 2c-3 4-5 6.5-5 9.5A5 5 0 0 0 12 17a5 5 0 0 0 5-5.5C17 8.5 15 6 12 2Z"/></svg>',
    '<svg class="icon" viewBox="0 0 24 24"><path d="M3 21 10 14M14 3l7 7-2.5 2.5L14 8l-3 3 2 2-2.5 2.5-2-2-3 3L3 21"/></svg>',
    '<svg class="icon" viewBox="0 0 24 24"><rect x="6" y="7" width="12" height="14" rx="2"/><path d="M9 7V5a3 3 0 0 1 6 0v2"/><path d="M9 12h6"/></svg>',
    '<svg class="icon" viewBox="0 0 24 24"><path d="M5 8h11a3 3 0 0 1 0 6H9"/><circle cx="6" cy="8" r="2"/><path d="M9 14a3 3 0 1 0 0 6"/></svg>',
    '<svg class="icon" viewBox="0 0 24 24"><path d="M12 3 2 21h20L12 3Z"/><path d="M12 10v4"/><circle cx="12" cy="17.5" r=".6" fill="currentColor" stroke="none"/></svg>',
    '<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M8.5 12.5 11 15l4.5-6"/></svg>',
  ],
}

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

    # 1. niche-correct icons (in order, exact string swap)
    icons = NICHE_ICONS[lead["niche_label"]]
    for orig, new in zip(ORIG_ICONS, icons):
        assert orig in html, f"icon not found for {lead['slug']}"
        html = html.replace(orig, new, 1)

    # 2. niche-correct title / schema type / services heading (only hardcoded electrician strings in template)
    html = html.replace("<title>{{BUSINESS_NAME}} | {{CITY}} Electrician</title>",
                         f'<title>{{{{BUSINESS_NAME}}}} | {{{{CITY}}}} {lead["niche_label"]}</title>')
    html = html.replace('"@type": "Electrician",', f'"@type": "{lead["schema_type"]}",')
    html = html.replace("<h2>Electrical work, done right the first time</h2>",
                         f'<h2>{lead["services_h2"]}</h2>')

    reviews_html, shell_class, track_class = build_reviews_html(lead["testimonials"])

    tokens = {
        "{{BUSINESS_NAME}}": lead["name"],
        "{{BUSINESS_NAME_URL}}": lead["name_url"],
        "{{CITY}}": lead["city"],
        "{{PHONE}}": lead["phone"],
        "{{PHONE_TEL}}": lead["phone_tel"],
        "{{WHATSAPP_TEL}}": lead["wa_tel"],
        "{{EMAIL}}": lead["email"],
        "{{RATING}}": lead["rating"],
        "{{REVIEW_COUNT}}": lead["reviews"],
        "{{YEARS_IN_BUSINESS}}": lead["years"],
        "{{YEARS_LABEL}}": lead["years_label"],
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
        "{{BEFORE_IMAGE}}": lead["before_after"][0],
        "{{AFTER_IMAGE}}": lead["before_after"][1],
        "{{REVIEWS_HTML}}": reviews_html,
        "{{MARQUEE_SHELL_CLASS}}": shell_class,
        "{{MARQUEE_TRACK_CLASS}}": track_class,
    }
    for i, (sname, sdesc) in enumerate(lead["services"], start=1):
        tokens[f"{{{{SERVICE_{i}_NAME}}}}"] = sname
        tokens[f"{{{{SERVICE_{i}_DESC}}}}"] = sdesc
    for i, cap in enumerate(lead["gallery_captions"], start=1):
        tokens[f"{{{{GALLERY_IMG_{i}}}}}"] = lead["photo_urls"][i-1]
        tokens[f"{{{{GALLERY_CAPTION_{i}}}}}"] = cap
    for i, (q, a) in enumerate(lead["faqs"], start=1):
        tokens[f"{{{{FAQ_{i}_Q}}}}"] = q
        tokens[f"{{{{FAQ_{i}_A}}}}"] = a

    for k, v in tokens.items():
        html = html.replace(k, v)

    leftover = set(re.findall(r"\{\{[A-Z0-9_]+\}\}", html))
    if leftover:
        print(f"WARNING {lead['slug']} leftover tokens:", leftover)

    os.makedirs(f"{outdir}/{lead['slug']}", exist_ok=True)
    with open(f"{outdir}/{lead['slug']}/index.html", "w") as f:
        f.write(html)
    print(f"built {lead['slug']}/index.html")

print("ALL DONE:", len(LEADS), "sites")
