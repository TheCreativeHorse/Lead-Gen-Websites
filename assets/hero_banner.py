import base64

def build_hero_banner():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">
<defs>
<linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#333d4a"/>
<stop offset="0.55" stop-color="#4a5768"/>
<stop offset="1" stop-color="#2b333e"/>
</linearGradient>
<radialGradient id="accentGlow" cx="0.82" cy="0.85" r="0.65">
<stop offset="0" stop-color="#d98a3f" stop-opacity="0.38"/>
<stop offset="1" stop-color="#d98a3f" stop-opacity="0"/>
</radialGradient>
<radialGradient id="accentGlow2" cx="0.12" cy="0.1" r="0.5">
<stop offset="0" stop-color="#ffffff" stop-opacity="0.10"/>
<stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
</radialGradient>
</defs>
<rect x="0" y="0" width="1920" height="1080" fill="url(#bgGrad)"/>
<rect x="0" y="0" width="1920" height="1080" fill="url(#accentGlow2)"/>
<rect x="0" y="0" width="1920" height="1080" fill="url(#accentGlow)"/>
<line x1="0" y1="0" x2="1920" y2="1080" stroke="#ffffff" stroke-opacity="0.045" stroke-width="2"/>
<g stroke="#ffffff" stroke-opacity="0.14" stroke-width="2" fill="none">
<path d="M1180 110 L1180 220 L1330 220 L1330 340"/>
<path d="M1330 340 L1470 340"/>
<path d="M1410 85 L1410 170 L1580 170"/>
<path d="M1580 170 L1580 280 L1720 280"/>
<path d="M1690 420 L1800 420 L1800 530"/>
<path d="M1240 450 L1240 560 L1130 560"/>
<path d="M1630 530 L1630 640 L1770 640"/>
<path d="M1270 250 L1270 170"/>
<path d="M1500 480 L1500 380 L1420 380"/>
</g>
<g fill="#ffffff" fill-opacity="0.28">
<circle cx="1180" cy="110" r="7"/>
<circle cx="1330" cy="220" r="7"/>
<circle cx="1470" cy="340" r="7"/>
<circle cx="1410" cy="85" r="7"/>
<circle cx="1580" cy="170" r="7"/>
<circle cx="1720" cy="280" r="7"/>
<circle cx="1800" cy="420" r="7"/>
<circle cx="1800" cy="530" r="7"/>
<circle cx="1130" cy="560" r="7"/>
<circle cx="1770" cy="640" r="7"/>
<circle cx="1270" cy="170" r="7"/>
<circle cx="1500" cy="480" r="7"/>
<circle cx="1420" cy="380" r="7"/>
</g>
<g fill="#d98a3f" fill-opacity="0.7">
<circle cx="1580" cy="170" r="8"/>
<circle cx="1690" cy="420" r="8"/>
<circle cx="1630" cy="530" r="8"/>
<circle cx="1330" cy="340" r="8"/>
</g>
<rect x="0" y="0" width="1920" height="1080" fill="#20252d" fill-opacity="0.12"/>
</svg>'''
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()

if __name__ == "__main__":
    out = build_hero_banner()
    with open("/tmp/gen/assets/hero_banner_b64.txt", "w") as f:
        f.write(out)
    print("bytes:", len(out))
