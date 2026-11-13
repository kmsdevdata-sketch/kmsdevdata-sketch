"""Generate the profile README SVGs (light + dark) into assets/svg/.

Run: python3 tools/build_svgs.py
Edit the CONTENT section below, then re-run and commit the SVGs.
"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "svg"
OUT.mkdir(parents=True, exist_ok=True)

FONT = "Pretendard, 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', -apple-system, 'Segoe UI', sans-serif"
MONO = "'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "light": dict(bg="#ffffff", card="#ffffff", border="#d0d7de", text="#1f2328", muted="#59636e",
                  faint="#818b98", chip="#f6f8fa", chip_border="#d0d7de", accent="#1f883d", node="#f6f8fa"),
    "dark": dict(bg="#0d1117", card="#0d1117", border="#30363d", text="#e6edf3", muted="#9198a1",
                 faint="#6e7681", chip="#161b22", chip_border="#30363d", accent="#3fb950", node="#161b22"),
}

# ----------------------------- CONTENT -----------------------------
NAME = "Minseo Kim"
ROLE = "Backend Developer"
TAGLINE_1 = "“됐다”고 말하기 전에,"
TAGLINE_2 = "무엇으로 확인했는지부터 묻는 백엔드 개발자입니다."

PROJECTS = [
    dict(slug="wihada", eyebrow="PROJECT INTERNSHIP · TEAM",
         title="위하다",
         desc=["주문제작 케이크 매장의 상담 · 주문 · 결제를", "한 흐름으로 묶은 서비스의 백엔드"],
         tags=["Java", "Spring Boot", "PostgreSQL", "Redis", "AWS ECS"]),
    dict(slug="jackal", eyebrow="SOFTBANK HACKATHON 2026 · FINAL",
         title="Cloud Migration Platform",
         desc=["EKS의 앱 · PostgreSQL을 온프레미스 K3s · GKE로", "옮기는 플랫폼의 프로비저닝과 데이터 경로"],
         tags=["Python", "Temporal", "Terraform", "Helm", "WireGuard"]),
    dict(slug="koro", eyebrow="SOFTBANK HACKATHON 2026 · PRELIM",
         title="코로의 이사",
         desc=["한 번 빌드한 이미지를 AWS · 온프레미스에 배포하는", "플랫폼의 배포 검증과 장애 전환"],
         tags=["TypeScript", "Node.js", "PostgreSQL", "Docker", "Cloudflare"]),
]

# -------------------------------------------------------------------


def text_width(s, size):
    """Rough width estimate: Hangul ~1.0em, ASCII ~0.58em."""
    w = 0.0
    for ch in s:
        if ord(ch) > 0x2E80:
            w += 1.0
        elif ch == " ":
            w += 0.3
        else:
            w += 0.6
    return w * size


def svg_open(w, h, title, extra_style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>'
            f'<style>text{{font-family:{FONT};}} .mono{{font-family:{MONO};}}{extra_style}</style>')


def chip(x, y, label, t, size=12.5, pad=10, h=24):
    w = text_width(label, size) + pad * 2
    return (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{t["chip"]}" stroke="{t["chip_border"]}"/>'
            f'<text x="{x + w/2:.1f}" y="{y + h/2 + size*0.36:.1f}" text-anchor="middle" font-size="{size}" font-weight="600" fill="{t["muted"]}">{escape(label)}</text>'), w


def header(t, mode):
    W, H = 860, 210
    anim = """
      .flow{stroke-dasharray:6 6;animation:flow 1.6s linear infinite}
      .ok{transform-origin:778px 105px;animation:pop 3.2s ease-in-out infinite}
      @keyframes flow{to{stroke-dashoffset:-24}}
      @keyframes pop{0%,70%,100%{transform:scale(1)}80%{transform:scale(1.12)}}
      @media (prefers-reduced-motion: reduce){.flow,.ok{animation:none}}"""
    s = [svg_open(W, H, f"{NAME} · {ROLE}", anim)]
    s.append(f'<rect width="{W}" height="{H}" rx="14" fill="{t["card"]}" stroke="{t["border"]}"/>')
    s.append(f'<text x="40" y="62" class="mono" font-size="13" font-weight="600" letter-spacing="2" fill="{t["faint"]}">{escape(ROLE.upper())}</text>')
    s.append(f'<text x="38" y="112" font-size="44" font-weight="800" fill="{t["text"]}">{escape(NAME)}</text>')
    s.append(f'<text x="40" y="150" font-size="17" font-weight="700" fill="{t["text"]}">{escape(TAGLINE_1)}</text>')
    s.append(f'<text x="40" y="176" font-size="17" font-weight="700" fill="{t["text"]}">{escape(TAGLINE_2)}</text>')
    # verify pipeline motif
    nodes = [(548, "Plan"), (650, "Apply")]
    for x, label in nodes:
        s.append(f'<rect x="{x-40}" y="85" width="80" height="40" rx="9" fill="{t["node"]}" stroke="{t["border"]}"/>')
        s.append(f'<text x="{x}" y="110" text-anchor="middle" class="mono" font-size="14" font-weight="600" fill="{t["muted"]}">{label}</text>')
    s.append(f'<path class="flow" d="M588 105 H610" stroke="{t["faint"]}" stroke-width="2" fill="none"/>')
    s.append(f'<path class="flow" d="M690 105 H740" stroke="{t["accent"]}" stroke-width="2" fill="none"/>')
    s.append(f'<g class="ok"><circle cx="778" cy="105" r="30" fill="none" stroke="{t["accent"]}" stroke-width="2.5"/>'
             f'<path d="M765 106 l9 9 l18 -20" stroke="{t["accent"]}" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>')
    s.append(f'<text x="778" y="158" text-anchor="middle" class="mono" font-size="12" font-weight="600" fill="{t["accent"]}">verified</text>')
    s.append("</svg>")
    return "".join(s)


def project_card(p, t):
    W, H = 860, 150
    s = [svg_open(W, H, f'{p["title"]} — {" ".join(p["desc"])}')]
    s.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="{t["card"]}" stroke="{t["border"]}"/>')
    s.append(f'<text x="28" y="38" class="mono" font-size="11.5" font-weight="600" letter-spacing="1.5" fill="{t["faint"]}">{escape(p["eyebrow"])}</text>')
    s.append(f'<text x="27" y="72" font-size="25" font-weight="800" fill="{t["text"]}">{escape(p["title"])}</text>')
    s.append(f'<text x="28" y="100" font-size="15.5" fill="{t["muted"]}">{escape(" ".join(p["desc"]))}</text>')
    x = 28
    for tag in p["tags"]:
        c, w = chip(x, 113, tag, t, size=12, pad=9, h=23)
        s.append(c)
        x += w + 6
    s.append(f'<text x="{W-28}" y="72" text-anchor="end" class="mono" font-size="13" font-weight="600" fill="{t["faint"]}">Case Study →</text>')
    s.append("</svg>")
    return "".join(s)


for mode, t in THEMES.items():
    (OUT / f"header-{mode}.svg").write_text(header(t, mode))
    for p in PROJECTS:
        (OUT / f"project-{p['slug']}-{mode}.svg").write_text(project_card(p, t))
print("written:", sorted(f.name for f in OUT.glob("*.svg")))
