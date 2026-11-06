#!/usr/bin/env python3
"""Build the BSCS Teaching & Learning site for GitHub Pages.

Usage: python3 build.py SRC_DIR OUT_DIR [SITE_URL]
SRC_DIR is the unzipped ChatGPT Sites export (contains data/ and dist/).
All internal links are relative, so the site works at a domain root or in a
GitHub project sub-folder. SITE_URL is only used for the sitemap, canonical
links, robots.txt and llms.txt.
"""
import json, re, sys, shutil, html
from pathlib import Path
from datetime import date
from lxml import html as LH

sys.path.insert(0, str(Path(__file__).resolve().parent))
from implementation import IMPL
from content import NEEDS, TIERS, CORE_TEXT, DEVELOP_INTRO, DEVELOP_GOAL, DEVELOP_OBS, DEVELOP_EVAL

SRC = Path(sys.argv[1]); OUT = Path(sys.argv[2])
SITE_URL = (sys.argv[3] if len(sys.argv) > 3 else "https://example.github.io/bscs-teaching-learning").rstrip("/")
DIST = SRC / "dist"
TODAY = date.today().isoformat()
NAME = "BSCS Teaching & Learning"

def clip(s, n):
    s = str(s)
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0].rstrip(",;:") + "…"
def esc(s): return html.escape(str(s), quote=True)
def slug(s):
    s = s.lower().replace("’", "").replace("'", "").replace("&", "and")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

# ---------------------------------------------------------------- model stages
STAGES = [
 ("lesson-preparation", "Lesson preparation", "Lesson Preparation", "Plan from the learning goal, anticipate barriers and decide how pupils will think."),
 ("climate-culture", "Climate & Culture", "Climate & Culture", "Build warm relationships and consistent routines that protect attention."),
 ("drive-thinking", "Drive Thinking for All", "Drive Thinking for All", "Give every pupil time to think, contribute and explain their reasoning."),
 ("check-adapt", "Check & Adapt", "Check & Adapt", "Gather useful evidence, choose a response and check again."),
 ("do-now", "Do Now", "Do Now", "Start calmly with independent retrieval and purposeful review."),
 ("explain", "Explain", "Explain", "Make new knowledge clear through small steps and expert modelling."),
 ("practice", "Secure learning through practice", "Secure Learning Through Practice", "Move from guided rehearsal to confident independent performance."),
 ("feedback", "Feedback to improve", "Feedback to Improve", "Make feedback precise and give pupils time to act on it."),
]
STAGE_BY_GUIDECAT = {s[2]: s[0] for s in STAGES}
STAGE_BY_GUIDECAT["Do Now / Retrieval across time"] = "do-now"
STAGE_TITLE = {s[0]: s[1] for s in STAGES}

EVIDENCE = {
 "bh": ("behaviour", "behaviour-interventions"),
 "cfu": ("checking-for-understanding", "checking-for-understanding-and-responsive-adaptation"),
 "cs": ("cognitive-science", "cognitive-science-approaches-retrieval-spacing-cognitive-load-worked-examples-and-dual-coding"),
 "cl": ("collaborative-learning", "collaborative-learning-approaches"),
 "ta": ("teaching-assistants", "deployment-of-teaching-assistants"),
 "voc": ("vocabulary-and-literacy", "disciplinary-literacy-and-explicit-vocabulary-instruction"),
 "ei": ("explicit-instruction", "explicit-instruction-guided-practice-and-scaffolding"),
 "fb": ("feedback", "feedback"),
 "send": ("send-five-a-day", "high-quality-teaching-for-pupils-with-send-eef-five-a-day"),
 "hw": ("homework", "homework"),
 "imp": ("implementation", "implementation-of-evidence-informed-strategies"),
 "ii": ("individualised-instruction", "individualised-instruction"),
 "ml": ("mastery-learning", "mastery-learning"),
 "meta": ("metacognition", "metacognition-and-self-regulation"),
 "ol": ("oral-language", "oral-language-interventions"),
 "pt": ("peer-tutoring", "peer-tutoring"),
 "rc": ("reading-comprehension", "reading-comprehension-strategies"),
 "dt": ("digital-technology", "using-digital-technology-to-improve-learning"),
 "ue": ("using-evidence", "using-evidence"),
}
EV_OLD2NEW = {old: new for new, old in EVIDENCE.values()}

# ---------------------------------------------------------------- load source pages
def main_of(path):
    doc = LH.document_fromstring(path.read_text(encoding="utf-8"))
    return doc

def extract(path):
    """Return dict(title, lede, pill, body_html) from an old article page."""
    doc = main_of(path)
    main = doc.xpath('//main')[0]
    h1 = main.xpath('.//h1')
    title = h1[0].text_content().strip() if h1 else ""
    lede = main.xpath('.//p[@class="lede"]')
    lede = lede[0].text_content().strip() if lede else ""
    pill = main.xpath('.//span[@class="pill"]')
    pill = pill[0].text_content().strip() if pill else ""
    content = main.xpath('.//div[contains(@class,"article-content")]')
    content = content[0] if content else main
    for sec in content.xpath('.//section[@class="related"]'):
        sec.getparent().remove(sec)
    body = "".join(LH.tostring(c, encoding="unicode") for c in content)
    if content.text and content.text.strip():
        body = esc(content.text) + body
    return dict(title=title, lede=lede, pill=pill, body=body)

guides = json.loads((SRC / "data/strategy-guides.json").read_text(encoding="utf-8"))

# strategy (guide) slugs
used = {}
for g in guides:
    short, _, sub = g["title"].partition(":")
    g["short"] = short.strip(); g["sub"] = sub.strip(); g["sub"] = g["sub"][:1].upper() + g["sub"][1:]
    s = slug(g["short"])
    if s in used:
        s = slug(g["short"] + " " + g["sub"].split()[0] + " " + " ".join(g["sub"].split()[1:3]))
        prev = used[s] if s in used else None
    used[s] = g; g["new"] = s
# disambiguate the two visualiser guides explicitly
for g in guides:
    if g["code"] == "EX02": g["new"] = "visualiser-live-modelling"
    if g["code"] == "FI07": g["new"] = "visualiser-improving-student-work"
    g["stage"] = STAGE_BY_GUIDECAT[g["category"]]
    g.update(IMPL[g["code"]])
assert len({g["new"] for g in guides}) == 80
G = {g["code"]: g for g in guides}

# reference pages: practitioner profiles and Barton summaries
REF = []
for p in sorted((DIST / "strategies").glob("*/index.html")):
    d = extract(p); d["old"] = "/strategies/%s/" % p.parent.name; d["new"] = p.parent.name; d["kind"] = "Practitioner profile"; REF.append(d)
for p in sorted((DIST / "barton").glob("*/index.html")):
    d = extract(p); d["old"] = "/barton/%s/" % p.parent.name; d["new"] = "barton-" + p.parent.name; d["kind"] = "Practitioner summary (Craig Barton)"; REF.append(d)
EVPAGES = {}
for new, old in EVIDENCE.values():
    d = extract(DIST / "evidence" / old / "index.html"); d["new"] = new; d["old"] = "/evidence/%s/" % old; EVPAGES[new] = d
MODEL = {s[0]: extract(DIST / "model" / s[0] / "index.html") for s in STAGES}
MODEL_FEEDBACK_PRINCIPLES = extract(DIST / "model/feedback-principles-at-bscs/index.html")
ROUTINES = {r: extract(DIST / "routines" / r / "index.html") for r in ["entry", "attention", "exit"]}
SOURCES = extract(DIST / "sources/index.html")
ANSWERING = extract(DIST / "adviser/answering-guidance/index.html")
MODEL_INDEX = LH.document_fromstring((DIST / "model/index.html").read_text()).xpath('//main')[0]

# link each strategy to its reference pages (hand-mapped in implementation.REFS)
from implementation import REFS
REFBY = {r["new"]: r for r in REF}
for g in guides:
    g["refs"] = [REFBY[("barton-" + k[2:]) if k.startswith("b:") else k] for k in REFS[g["code"]]]
# ---------------------------------------------------------------- URL mapping for old internal links
OLDMAP = {"/": "", "/library/": "strategies/", "/guides/": "strategies/", "/sources/": "evidence/sources/",
          "/copilot/setup/": "copilot/", "/adviser/answering-guidance/": "copilot/answering-guidance/", "/model/": "model/"}
for g in guides: OLDMAP["/guides/%s/" % g["slug"]] = "strategies/%s/" % g["new"]
for r in REF: OLDMAP[r["old"]] = "reference/%s/" % r["new"]
for new, old in EVIDENCE.values(): OLDMAP["/evidence/%s/" % old] = "evidence/%s/" % new
for s in STAGES: OLDMAP["/model/%s/" % s[0]] = "model/%s/" % s[0]
OLDMAP["/model/feedback-principles-at-bscs/"] = "model/feedback-principles/"
for r in ROUTINES: OLDMAP["/routines/%s/" % r] = "routines/%s/" % r

def rewrite_links(body, p):
    def fix(m):
        href = m.group(1)
        if href.startswith("/"):
            path, _, frag = href.partition("#")
            if not path.endswith("/"): path += "/"
            new = OLDMAP.get(path)
            if new is None:
                if path.startswith("/guides/files/"):
                    new = "downloads/" + path.rstrip("/").split("/")[-1]
                else:
                    print("unmapped link", href); new = ""
            return 'href="%s%s%s"' % (p, new, ("#" + frag) if frag else "")
        return m.group(0)
    body = re.sub(r'href="([^"]*)"', fix, body)
    body = body.replace("https://bscs-teaching-learning.candidduck16.chatgpt.site", SITE_URL)
    return body

# ---------------------------------------------------------------- page shell
PAGES = []   # (path, title, desc, kind, text) for search/sitemap

NAV = [("strategies/", "Strategies"), ("needs/", "Pupil needs"), ("model/", "Our model"), ("develop/", "Individual Development"), ("evidence/", "Evidence")]

def page(path, title, desc, body, kind="Page", text="", crumbs=None, wide=False, search=True):
    depth = path.count("/") if path else 0
    p = "../" * depth
    nav = "".join('<a href="%s%s"%s>%s</a>' % (p, u, ' aria-current="page"' if path.startswith(u) else "", esc(t)) for u, t in NAV)
    crumb = ""
    if crumbs:
        crumb = '<nav class="breadcrumb" aria-label="Breadcrumb"><a href="%s">Home</a>' % (p or "./")
        for u, t in crumbs:
            crumb += '<span aria-hidden="true">/</span>' + ('<a href="%s%s">%s</a>' % (p, u, esc(t)) if u else "<span>%s</span>" % esc(t))
        crumb += "</nav>"
    canon = SITE_URL + "/" + path
    full = """<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · {name}</title><meta name="description" content="{desc}"><link rel="canonical" href="{canon}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website">
<link rel="stylesheet" href="{p}assets/style.css"><script defer src="{p}assets/site.js"></script>
<script type="application/ld+json">{ld}</script></head>
<body data-root="{p}"><a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="nav-wrap"><a class="brand" href="{home}"><span class="brand-mark" aria-hidden="true">B<span>+</span></span><span>BSCS<span class="brand-sub">Teaching &amp; Learning</span></span></a>
<button class="nav-toggle" aria-expanded="false" aria-controls="main-nav">Menu</button>
<nav id="main-nav" aria-label="Main navigation">{nav}<a class="nav-action" href="{p}copilot/">Copilot adviser</a></nav></div></header>
<main id="main" class="{mcls}">{crumb}{body}</main>
<footer class="site-footer"><div class="wrap"><div><strong>Bradley Stoke Community School</strong><br>Teaching &amp; Learning reference hub · Olympus Academy Trust</div>
<div class="foot-links"><a href="{p}strategies/">All strategies</a><a href="{p}evidence/">How we rate evidence</a><a href="{p}evidence/sources/">Source hierarchy</a><a href="{p}copilot/">Copilot adviser</a></div>
<p class="foot-note">Evidence informs the choice. Professional judgement shapes the practice. School-prepared guidance; EEF evidence snapshot checked August 2026.</p></div></footer>
</body></html>""".format(title=esc(title), name=esc(NAME), desc=esc(clip(desc, 300)), canon=esc(canon), p=p, home=p or "./",
                         ld=json.dumps({"@context": "https://schema.org", "@type": "WebPage", "name": title, "description": desc[:300], "url": canon, "inLanguage": "en-GB", "isPartOf": {"@type": "WebSite", "name": NAME, "url": SITE_URL + "/"}}),
                         nav=nav, crumb=crumb, body=body, mcls="wide" if wide else "article")
    f = OUT / path / "index.html" if (path == "" or path.endswith("/")) else OUT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(full, encoding="utf-8")
    if search:
        PAGES.append(dict(url=path, title=title, desc=clip(desc, 220), kind=kind, text=re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(text or body)))[:1500]))
    return p

def badges(g, p=""):
    name, cls, _ = TIERS[g["tier"]]
    b = '<span class="badge %s">%s</span>' % (cls, esc(name))
    if g["core"]: b += '<span class="badge core">Core strategy</span>'
    return b

def strategy_card(g, p):
    return ('<a class="s-card" href="{p}strategies/{u}/" data-stage="{st}" data-tier="{t}" data-core="{c}">'
            '<span class="s-code">{code} · {stage}</span><strong>{t1}</strong><span class="s-sub">{sub}</span><span class="s-badges">{b}</span></a>').format(
        p=p, u=g["new"], st=g["stage"], t=g["tier"], c="1" if g["core"] else "0", code=g["code"], stage=esc(STAGE_TITLE[g["stage"]]),
        t1=esc(g["short"]), sub=esc(g["sub"] or clip(g["intro"], 90)), b=badges(g))

def article(top_pill, title, lede, inner, toc=None, extra_top=""):
    t = '<div class="article-top">%s<h1>%s</h1>%s%s</div>' % (
        '<span class="pill">%s</span>' % esc(top_pill) if top_pill else "", esc(title), '<p class="lede">%s</p>' % esc(lede) if lede else "", extra_top)
    if toc:
        tocl = '<aside class="toc"><span class="eyebrow">On this page</span>' + "".join('<a href="#%s">%s</a>' % (a, esc(b)) for a, b in toc) + "</aside>"
        return t + '<div class="article-grid">%s<div class="article-content">%s</div></div>' % (tocl, inner)
    return t + '<div class="article-content standalone">%s</div>' % inner

# ---------------------------------------------------------------- strategy pages
def build_strategy(g):
    path = "strategies/%s/" % g["new"]; p = "../../"
    tname, tcls, texpl = TIERS[g["tier"]]
    ev_links = "".join('<li><a href="%sevidence/%s/">%s</a></li>' % (p, EVIDENCE[k][0], esc(EVPAGES[EVIDENCE[k][0]]["title"])) for k in g["ev"])
    steps = "".join("<li>%s</li>" % esc(s) for s in g["steps"])
    tips = "".join("<li>%s</li>" % esc(s) for s in g["tips"])
    do = "".join("<li>%s</li>" % esc(s) for s in g["do"]); avoid = "".join("<li>%s</li>" % esc(s) for s in g["avoid"])
    look = "".join("<li>%s</li>" % esc(s) for s in g["look"])
    links = "".join('<li><a href="%s" rel="noopener">%s ↗</a></li>' % (esc(l["url"]), esc(l["label"])) for l in g["links"])
    refs = "".join('<li><a href="%sreference/%s/">%s</a> <span class="muted">(%s)</span></li>' % (p, r["new"], esc(r["title"]), esc(r["kind"])) for r in g["refs"])
    related = [x for x in guides if x["stage"] == g["stage"] and x is not g]
    related.sort(key=lambda x: (not x["core"], x["tier"] != "S", x["code"]))
    rel = "".join('<a href="%sstrategies/%s/">%s</a>' % (p, x["new"], esc(x["short"])) for x in related[:4])
    inner = f"""
<section class="evidence-box {tcls}" aria-labelledby="evidence"><h2 id="evidence">Evidence: {esc(tname)}</h2><p>{esc(texpl)}</p>
<p class="ev-links"><strong>Read the evidence summary:</strong></p><ul>{ev_links}</ul><p class="small"><a href="{p}evidence/">How we rate evidence</a></p></section>
<h2 id="how-to-do-it">How to do it</h2><ol class="steps">{steps}</ol>
<h2 id="what-it-sounds-like">What it sounds like</h2><blockquote class="script">{esc(g["script"])}</blockquote>
<div class="two-col"><div class="panel do"><h3>Do</h3><ul>{do}</ul></div><div class="panel avoid"><h3>Avoid</h3><ul>{avoid}</ul></div></div>
<h2 id="top-tips">Top tips</h2><ul>{tips}</ul>
<h2 id="in-the-classroom">In the classroom</h2><p>{esc(g["example"])}</p>
<section class="develop-box" aria-labelledby="individual-development"><h2 id="individual-development">Use it for Individual Development</h2>
<h3>Example goal</h3><p class="goal">{esc(g["goal"])}</p><button class="copy" data-copy="{esc(g["goal"])}">Copy goal</button>
<h3>Peer observer look-fors</h3><ul>{look}</ul>
<h3>Quick check of impact</h3><p>{esc(g["check"])}</p>
<p class="small">Adapt the goal to your class and subject. See <a href="{p}develop/writing-your-goal/">writing a precise goal</a> and <a href="{p}develop/peer-observation/">peer observation</a>.</p></section>
<h2 id="further-reading">Further reading</h2>
{('<h3>On this site</h3><ul>' + refs + '</ul>') if refs else ''}
<h3>External sources</h3><ul>{links}</ul>
<h3>Download</h3><p class="downloads"><a href="{p}downloads/{esc(g['filename'])}.pdf">Original one-page guide (PDF)</a><a href="{p}downloads/{esc(g['filename'])}.docx">Editable Word version</a></p>
<p class="small muted">The downloadable guides are the original one-page versions. The evidence rating and Individual Development sections appear on this web page only.</p>
<section class="related"><h2>More in {esc(STAGE_TITLE[g["stage"]])}</h2><div class="related-links">{rel}</div></section>
"""
    toc = [("evidence", "Evidence"), ("how-to-do-it", "How to do it"), ("what-it-sounds-like", "What it sounds like"), ("top-tips", "Top tips"),
           ("in-the-classroom", "In the classroom"), ("individual-development", "Individual Development"), ("further-reading", "Further reading")]
    sub = '<p class="subtitle">%s</p>' % esc(g["sub"]) if g["sub"] else ""
    top = '<div class="badges">%s</div>' % badges(g)
    body = '<div class="article-top"><span class="pill">%s · %s</span><h1>%s</h1>%s<p class="lede">%s</p>%s<div class="article-tools"><button onclick="window.print()">Print page</button></div></div>' % (
        esc(STAGE_TITLE[g["stage"]]), g["code"], esc(g["short"]), sub, esc(g["intro"]), top)
    tocl = '<aside class="toc"><span class="eyebrow">On this page</span>' + "".join('<a href="#%s">%s</a>' % (a, esc(b)) for a, b in toc) + "</aside>"
    body += '<div class="article-grid">%s<div class="article-content">%s</div></div>' % (tocl, inner)
    page(path, g["short"], "%s %s" % (g["sub"] + "." if g["sub"] else "", g["intro"]), body, kind="Strategy",
         crumbs=[("strategies/", "Strategies"), ("model/%s/" % g["stage"], STAGE_TITLE[g["stage"]]), (None, g["short"])])

for g in guides: build_strategy(g)

# strategies index with filters
def build_strategies_index():
    p = "../"
    order = sorted(guides, key=lambda x: ([s[0] for s in STAGES].index(x["stage"]), x["code"]))
    stagebtn = '<button class="active" data-f-stage="all" aria-pressed="true">All areas</button>' + "".join('<button data-f-stage="%s" aria-pressed="false">%s</button>' % (s[0], esc(s[1])) for s in STAGES)
    tierbtn = '<button class="active" data-f-tier="all" aria-pressed="true">Any evidence</button>' + "".join('<button data-f-tier="%s" aria-pressed="false">%s</button>' % (k, esc(v[0])) for k, v in TIERS.items())
    cards = "".join(strategy_card(g, p) for g in order)
    body = f"""<span class="eyebrow">Strategy library</span><h1>80 strategies to explore and try</h1>
<p class="lede">Every strategy page explains how to do it, how strong the evidence is, and how to use it as your Individual Development focus, with an example goal, peer observer look-fors and a quick check of impact.</p>
<div class="search-box"><label for="search">Search all pages</label><div><input id="search" type="search" placeholder="Try mini-whiteboards, misconceptions or independent practice…" autocomplete="off"><button id="clear-search" type="button">Clear</button></div></div>
<div id="search-results" class="results" aria-live="polite"></div>
<div class="filters" role="group" aria-label="Filter by BSCS model area">{stagebtn}</div>
<div class="filters" role="group" aria-label="Filter by evidence">{tierbtn}<label class="core-toggle"><input type="checkbox" id="core-only"> Core strategies only</label></div>
<p id="result-count" class="muted" aria-live="polite">Showing 80 strategies</p>
<div class="s-grid" id="strategy-grid">{cards}</div>
<p class="small muted"><a href="{p}evidence/">How the evidence ratings work</a>. {esc(CORE_TEXT)}</p>"""
    page("strategies/", "Strategy library", "Search and filter 80 evidence-informed teaching strategies by BSCS model area and strength of evidence.", body, kind="Index", wide=True,
         crumbs=[(None, "Strategies")], text="Strategy library " + " ".join(g["title"] for g in guides))
build_strategies_index()

# ---------------------------------------------------------------- needs pages
def build_needs():
    p = "../"
    cards = "".join('<a class="need-card" href="%sneeds/%s/"><strong>%s</strong><span>%s</span></a>' % (p, s, esc(t), esc(d)) for s, t, d, _, _ in NEEDS)
    body = f"""<span class="eyebrow">Start with your pupils</span><h1>What do your pupils need next?</h1>
<p class="lede">Choose the problem that is closest to what you see in your classroom. Each page suggests a small number of strategies, with the strongest and most relevant first.</p>
<div class="need-grid">{cards}</div>
<p class="small">Not sure which problem fits? See <a href="{p}develop/writing-your-goal/">writing a precise goal</a>, or ask the <a href="{p}copilot/">Copilot adviser</a>.</p>"""
    page("needs/", "Pupil needs", "Find strategies by the classroom problem you want to solve.", body, kind="Index", wide=True, crumbs=[(None, "Pupil needs")])
    for s, t, d, why, codes in NEEDS:
        p2 = "../../"
        items = ""
        for i, c in enumerate(codes):
            g = G[c]
            items += ('<li class="need-item"><a href="%sstrategies/%s/"><strong>%s</strong></a> %s<p>%s</p><p class="goal small"><span class="muted">Example goal:</span> %s</p></li>' % (
                p2, g["new"], esc(g["short"]), badges(g), esc(g["intro"]), esc(g["goal"])))
        others = "".join('<a href="%sneeds/%s/">%s</a>' % (p2, s2, esc(t2)) for s2, t2, *_ in NEEDS if s2 != s)
        body = f"""<div class="article-top"><span class="pill">Pupil need</span><h1>{esc(t)}</h1><p class="lede">{esc(d)}</p></div>
<div class="article-content standalone"><h2 id="where-to-start">Where to start</h2><p>{esc(why)}</p>
<h2 id="strategies">Strategies to consider</h2><p class="small muted">Choose one. Start with a core strategy unless another fits your class better.</p><ol class="need-list">{items}</ol>
<section class="related"><h2>Other pupil needs</h2><div class="related-links">{others}</div></section></div>"""
        page("needs/%s/" % s, t, d + " " + why, body, kind="Pupil need", crumbs=[("needs/", "Pupil needs"), (None, t)])
build_needs()

# ---------------------------------------------------------------- model, routines
def build_model():
    p = "../"
    tiles = "".join('<a class="model-tile" href="%smodel/%s/"><span class="number">%02d</span><h3>%s</h3><p>%s</p></a>' % (p, s[0], i + 1, esc(s[1]), esc(s[3])) for i, s in enumerate(STAGES))
    intro_p = MODEL_INDEX.xpath('.//p[@class="lede"]')
    lede = intro_p[0].text_content().strip() if intro_p else ""
    routines = "".join('<a class="link-card" href="%sroutines/%s/"><strong>%s</strong><span>%s</span></a>' % (p, r, esc(ROUTINES[r]["title"]), "BSCS agreed routine") for r in ROUTINES)
    body = f"""<span class="eyebrow">BSCS agreed practice</span><h1>Our model of highly effective teaching</h1><p class="lede">{esc(lede)}</p>
<div class="model-grid">{tiles}</div><h2>Agreed classroom routines</h2><div class="card-row">{routines}<a class="link-card" href="{p}model/feedback-principles/"><strong>{esc(MODEL_FEEDBACK_PRINCIPLES['title'])}</strong><span>BSCS agreed practice</span></a></div>"""
    page("model/", "Our model", lede, body, kind="BSCS agreed practice", wide=True, crumbs=[(None, "Our model")])
    for key, title, _, desc in STAGES:
        p2 = "../../"; m = MODEL[key]
        sts = [g for g in guides if g["stage"] == key]
        sts.sort(key=lambda x: (not x["core"], "SRP".index(x["tier"]), x["code"]))
        cards = "".join(strategy_card(g, p2) for g in sts)
        inner = rewrite_links(m["body"], p2) + f'<h2 id="strategies">Strategies for {esc(title)}</h2><p class="small muted">Core strategies first, then by strength of evidence.</p><div class="s-grid">{cards}</div>'
        page("model/%s/" % key, title, desc, article("BSCS agreed practice", title, desc, inner), kind="BSCS agreed practice",
             crumbs=[("model/", "Our model"), (None, title)], text=m["body"] + " " + " ".join(g["short"] for g in sts))
    m = MODEL_FEEDBACK_PRINCIPLES
    page("model/feedback-principles/", m["title"], m["lede"] or "BSCS feedback principles.", article("BSCS agreed practice", m["title"], m["lede"], rewrite_links(m["body"], "../../")),
         kind="BSCS agreed practice", crumbs=[("model/", "Our model"), (None, m["title"])])
    for r, m in ROUTINES.items():
        page("routines/%s/" % r, m["title"], (m["lede"] or m["title"])[:200], article("BSCS agreed routine", m["title"], "", rewrite_links(m["body"], "../../")),
             kind="BSCS agreed practice", crumbs=[("model/", "Our model"), (None, m["title"])])
build_model()

# ---------------------------------------------------------------- develop
def build_develop():
    pages = [("develop/", "Individual Development", "Use this site to choose, try and refine one change to your classroom practice.", DEVELOP_INTRO, "../"),
             ("develop/writing-your-goal/", "Writing a precise goal", "Turn a broad aim into one observable change: I will … so that students …", DEVELOP_GOAL, "../../"),
             ("develop/peer-observation/", "Developmental peer observation", "A short, focused protocol for observing one change and how pupils respond.", DEVELOP_OBS, "../../"),
             ("develop/evaluating-impact/", "Evaluating impact and deciding what next", "Separate how well you implemented the change from its effect on pupils, then refine, embed or rethink.", DEVELOP_EVAL, "../../")]
    for path, title, lede, bodyt, p in pages:
        inner = bodyt.replace("{p}", p)
        crumbs = [(None, "Individual Development")] if path == "develop/" else [("develop/", "Individual Development"), (None, title)]
        page(path, title, lede, article("Individual Development CPD", title, lede, inner), kind="Individual Development", crumbs=crumbs)
build_develop()

# ---------------------------------------------------------------- evidence and reference
def build_evidence():
    p = "../"
    rows = "".join('<tr><td><span class="badge %s">%s</span></td><td>%s</td><td>%d</td></tr>' % (v[1], esc(v[0]), esc(v[2]), sum(1 for g in guides if g["tier"] == k)) for k, v in TIERS.items())
    evl = "".join('<li><a href="%sevidence/%s/">%s</a></li>' % (p, k, esc(d["title"])) for k, d in sorted(EVPAGES.items(), key=lambda x: x[1]["title"]))
    inner = f"""<p>Every strategy page shows how strong the evidence is for that kind of practice. The rating is a guide to how much weight the evidence can bear, not a promise that a strategy will work in every classroom.</p>
<h2 id="ratings">How strategies are rated</h2><table><tr><th scope="col">Rating</th><th scope="col">What it means</th><th scope="col">Strategies</th></tr>{rows}</table>
<h2 id="core">Core strategies</h2><p>{esc(CORE_TEXT)} There are {sum(g['core'] for g in guides)} core strategies.</p>
<h2 id="cautions">Using evidence well</h2><ul>
<li>EEF Toolkit estimates (for example, "+6 months") describe broad approaches across many studies. They are never an effect size for a single classroom routine such as cold calling or a Do Now.</li>
<li>Evidence describes what has tended to work on average. Implementation, subject and pupils all matter, so check how your pupils respond.</li>
<li>School agreement and practitioner advice are useful, but they are not research findings. Each page states its source and status.</li></ul>
<p>Evidence figures come from a school-prepared snapshot checked in August 2026. Check the <a href="https://educationendowmentfoundation.org.uk/education-evidence" rel="noopener">EEF website ↗</a> for current estimates.</p>
<h2 id="summaries">Evidence summaries</h2><ul class="columns">{evl}</ul>
<h2 id="sources">Sources</h2><p>See the <a href="{p}evidence/sources/">source hierarchy</a> for how research, school policy and practitioner guidance are used on this site, and the <a href="{p}reference/">reference library</a> for practitioner profiles and summaries.</p>"""
    page("evidence/", "How we rate evidence", "How strategy evidence ratings work, and summaries of the research behind them.", article("Evidence", "How we rate evidence", "Know what supports the advice, and how far the claim can travel.", inner), kind="Evidence", crumbs=[(None, "Evidence")])
    for k, d in EVPAGES.items():
        users = [g for g in guides if any(EVIDENCE[e][0] == k for e in g["ev"])]
        users.sort(key=lambda x: (not x["core"], "SRP".index(x["tier"])))
        extra = ('<h2 id="strategies">Strategies that draw on this evidence</h2><div class="related-links">' + "".join('<a href="../../strategies/%s/">%s</a>' % (g["new"], esc(g["short"])) for g in users) + "</div>") if users else ""
        lede = d["lede"] if not d["lede"].startswith("ALIASES") else ""
        page("evidence/%s/" % k, d["title"], (lede or d["title"] + ": evidence summary for BSCS staff.")[:220],
             article("Evidence summary", d["title"], lede, rewrite_links(d["body"], "../../") + extra), kind="Evidence summary",
             crumbs=[("evidence/", "Evidence"), (None, d["title"])])
    s = SOURCES
    page("evidence/sources/", s["title"], s["lede"], article("Source hierarchy", s["title"], s["lede"], rewrite_links(s["body"], "../../")), kind="Evidence",
         crumbs=[("evidence/", "Evidence"), (None, "Source hierarchy")])
    # reference library
    p = "../"
    prof = "".join('<li><a href="%sreference/%s/">%s</a></li>' % (p, r["new"], esc(r["title"])) for r in REF if r["new"].startswith("barton-") is False)
    bart = "".join('<li><a href="%sreference/%s/">%s</a></li>' % (p, r["new"], esc(r["title"])) for r in REF if r["new"].startswith("barton-"))
    inner = f"""<p>These pages hold the detailed practitioner material that informs the strategy pages. They are school-compiled summaries, not original publisher documents. Start with the <a href="{p}strategies/">strategy library</a> if you are choosing something to try.</p>
<h2 id="profiles">Practitioner strategy profiles</h2><ul class="columns">{prof}</ul><h2 id="barton">Craig Barton practitioner summaries</h2><ul class="columns">{bart}</ul>"""
    page("reference/", "Reference library", "Practitioner profiles and summaries that inform the strategy pages.", article("Reference", "Reference library", "Detailed practitioner material behind the strategy pages.", inner), kind="Reference", crumbs=[(None, "Reference library")])
    for r in REF:
        users = [g for g in guides if r in g["refs"]]
        extra = ('<h2 id="strategy-pages">Related strategy pages</h2><div class="related-links">' + "".join('<a href="../../strategies/%s/">%s</a>' % (g["new"], esc(g["short"])) for g in users) + "</div>") if users else ""
        page("reference/%s/" % r["new"], r["title"], (r["lede"] or r["title"])[:220], article(r["kind"], r["title"], r["lede"], rewrite_links(r["body"], "../../") + extra),
             kind=r["kind"], crumbs=[("reference/", "Reference library"), (None, r["title"])])
build_evidence()

# ---------------------------------------------------------------- copilot
INSTRUCTIONS = """You are the BSCS Teaching and Learning Adviser for Bradley Stoke Community School. Answer teachers' teaching-and-learning questions directly, using the configured BSCS website as your primary knowledge source.

RETRIEVAL AND AUTHORITY
Search the website for the relevant topic before claiming what the school expects or what its sources say. Use the source hierarchy on the evidence/sources page. For research claims, retrieve the relevant evidence summary page. For BSCS expectations, retrieve the model or agreed routines pages. Use the strategy pages (under /strategies/) to recommend and explain practical strategies; each states its evidence rating (Strong evidence base, Research-informed or Established practice). Use the reference pages for further practitioner detail. These are different kinds of authority. Do not label practitioner advice or school policy as an EEF research finding.

The website contains an August 2026 evidence snapshot, with EEF sources checked on 18 August 2026. Say so when giving numerical Toolkit estimates. Do not describe them as newly verified. Never attach a Toolkit months-of-progress estimate to a single routine such as cold calling, mini-whiteboards or a Do Now. Treat approximate success thresholds as practitioner decision aids, not universal research rules.

RESPONSE
Start with useful advice when there is enough context. Ask at most one clarifying question when the answer would materially change your recommendation. Do not assume a subject or require baseline data before helping. When a teacher describes a classroom problem, check the matching pupil needs page (under /needs/). Normally give a short main recommendation, two to four prioritised strategies with their evidence rating, an implementation sequence, common pitfalls and what to look for in pupil learning. Cite the exact website page supporting each important claim. State when a source is missing or a recommendation is your own adaptation.

Keep curricular ambition high. Adjust access, examples, scaffolds, practice and support. Explain how to check whether the change helped. Do not equate compliant behaviour, task completion or one confident answer with secure learning.

If asked for a PGD or Individual Development CPD goal, offer one draft: I will [specific change in practice] so that students [observable intended response]. Use the example goal, peer observer look-fors and quick check of impact on the relevant strategy page, adapted to the teacher's context. Do not create a separate target or take the teacher through a formal enquiry unless requested.

For DDI feedback, use only the observation evidence supplied. Keep praise individual and the developmental point focused on one observable action. Use WHEN-GOAL-ACTION if requested. Do not invent student impact or official StepLab step titles. This public site does not contain the full verified StepFinder catalogue. Offer a clearly labelled custom action if no exact title can be verified.

SOURCE LIMITS
Search retrieval may miss pages. If you cannot find support, say that you cannot verify the answer from the BSCS website. Do not pretend to have read restricted Ambition, StepLab or DistilED originals. Summaries are not original publisher documents. Do not request identifiable pupil information, staffing records or confidential observation notes in order to answer general teaching questions."""

def build_copilot():
    p = "../"
    inner = f"""<h2 id="before-you-begin">Before you begin</h2>
<p>Use Microsoft 365 Copilot Chat with your school account. Your Trust needs to allow Agent Builder. Public-website grounding plus the instructions below is the intended setup. Adding internal organisational knowledge may change licensing or billing.</p>
<h2 id="create-the-agent">Create the agent</h2><ol>
<li>Open Copilot Chat and select <strong>New agent</strong>, then <strong>Configure</strong>.</li>
<li>Name it <strong>BSCS Teaching and Learning Adviser</strong>.</li>
<li>Under Knowledge, add this website as a public website source: <code class="url">{esc(SITE_URL)}</code></li>
<li>Paste the instructions below into the Instructions field.</li>
<li>Where available, turn on <strong>Only use specified sources</strong> and turn off searching all websites. Microsoft notes this does not completely block general AI knowledge.</li></ol>
<h2 id="test-the-answers">Test the answers</h2><p>Try these questions and check that the adviser cites the right pages:</p><ul>
<li>"Only a few pupils answer my questions. What should I try?"</li><li>"When should the Do Now timer start?"</li>
<li>"Write me an Individual Development goal about mini-whiteboards."</li><li>"Is cold calling proven to add a specific number of months of progress?"</li></ul>
<h2 id="when-a-page-is-missing">When a page is missing</h2><p>The adviser relies on Bing having indexed the site, so new or changed pages can take time to appear. Adding the website does not guarantee that every page is retrieved. Test with a standard staff account before sharing with all staff.</p>
<h2 id="personalise-carefully">Personalise carefully</h2><p>You can add your subject, phase and preferred response format. Keep the source and citation rules. Never upload confidential pupil or staffing information.</p>
<h2 id="instructions">Copyable agent instructions</h2><button class="copy" data-copy-target="agent-instructions">Copy instructions</button>
<pre id="agent-instructions" class="instructions">{esc(INSTRUCTIONS)}</pre>
<p>See also: <a href="{p}copilot/answering-guidance/">how the adviser should answer</a>.</p>"""
    page("copilot/", "Set up your Copilot adviser", "Build the BSCS Teaching and Learning Adviser in Microsoft 365 Copilot using this website as its knowledge source.",
         article("Staff guide", "Set up your Copilot adviser", "Build a Copilot agent that answers teaching questions using this site.", inner), kind="Staff guide", crumbs=[(None, "Copilot adviser")])
    a = ANSWERING
    page("copilot/answering-guidance/", a["title"], a["lede"][:220], article("Adviser guidance", a["title"], "", rewrite_links(a["body"], "../../")), kind="Adviser guidance",
         crumbs=[("copilot/", "Copilot adviser"), (None, a["title"])])
    (OUT / "copilot-instructions.txt").write_text(INSTRUCTIONS, encoding="utf-8")
build_copilot()

# ---------------------------------------------------------------- home
def build_home():
    p = ""
    core = [g for g in guides if g["core"]]
    core.sort(key=lambda x: ([s[0] for s in STAGES].index(x["stage"]), x["code"]))
    needs = "".join('<a href="needs/%s/">%s <span aria-hidden="true">→</span></a>' % (s, esc(t)) for s, t, *_ in NEEDS[:6])
    cards = "".join(strategy_card(g, p) for g in core)
    tiles = "".join('<a class="model-tile" href="model/%s/"><span class="number">%02d</span><h3>%s</h3><p>%s</p></a>' % (s[0], i + 1, esc(s[1]), esc(s[3])) for i, s in enumerate(STAGES))
    body = f"""<section class="hero"><div class="hero-content"><span class="eyebrow">BSCS professional learning</span>
<h1>Find one change<br>that helps your<br><em>pupils learn more.</em></h1>
<p>Explore evidence-informed strategies that fit the BSCS teaching model, see how strong the evidence is, and turn one into a precise focus for your Individual Development.</p>
<div class="hero-links"><a class="button light" href="strategies/">Explore 80 strategies →</a><a href="develop/">How Individual Development works →</a></div></div>
<div class="hero-panel"><span class="eyebrow">Start with the learning</span><h2>What do your pupils need next?</h2>{needs}<a class="more" href="needs/">All pupil needs →</a></div></section>
<section class="wrap search-section"><div class="search-box"><label for="search">Find a strategy or answer a teaching question</label><div><input id="search" type="search" placeholder="Try mini-whiteboards, misconceptions or independent practice…" autocomplete="off"><button id="clear-search" type="button">Clear</button></div></div><div id="search-results" class="results" aria-live="polite"></div></section>
<section class="wrap"><div class="section-heading"><div><span class="eyebrow">Core strategies</span><h2>Where to start</h2></div><a href="strategies/">All strategies →</a></div>
<p class="muted">{esc(CORE_TEXT)}</p><div class="s-grid">{cards}</div></section>
<section class="wrap how"><span class="eyebrow">Individual Development</span><h2>From strategy to classroom change</h2><ol class="how-steps">
<li><strong>Identify</strong><span>Name a pupil problem you can see.</span></li><li><strong>Explore</strong><span>Find a strategy that fits.</span></li>
<li><strong>Plan</strong><span>Write: I will … so that students …</span></li><li><strong>Observe</strong><span>Use the look-fors with a colleague.</span></li>
<li><strong>Adapt</strong><span>Check impact, then refine or embed.</span></li></ol><a class="button" href="develop/">Read the guide →</a></section>
<section class="wrap"><div class="section-heading"><div><span class="eyebrow">The BSCS model</span><h2>A shared language for teaching</h2></div><a href="model/">View the model →</a></div><div class="model-grid">{tiles}</div></section>"""
    page("", "Home", "Explore and implement evidence-informed teaching strategies that fit the BSCS teaching model, and use them for Individual Development CPD.", body, kind="Home", wide=True)
build_home()

# ---------------------------------------------------------------- 404, assets, downloads, sitemap, search
def build_404():
    body = '<div class="article-top"><h1>Page not found</h1><p class="lede">This page may have moved when the site was rebuilt.</p></div><div class="article-content standalone"><p><a href="%s/">Go to the home page</a> or <a href="%s/strategies/">browse all strategies</a>.</p></div>' % (SITE_URL, SITE_URL)
    page("404.html", "Page not found", "Page not found.", body, search=False)
    t = (OUT / "404.html").read_text().replace('<head><meta charset="utf-8">', '<head><meta charset="utf-8"><base href="%s/">' % SITE_URL)
    (OUT / "404.html").write_text(t)
build_404()

shutil.copytree(Path(__file__).parent / "assets", OUT / "assets", dirs_exist_ok=True)
dl = OUT / "downloads"; dl.mkdir(exist_ok=True)
for f in (DIST / "guides/files").iterdir(): shutil.copy2(f, dl / f.name)
for f in (DIST / "guides/downloads").iterdir(): shutil.copy2(f, dl / f.name)
(OUT / ".nojekyll").write_text("")

(OUT / "assets/search.json").write_text(json.dumps(PAGES, ensure_ascii=False), encoding="utf-8")
urls = "".join("<url><loc>%s/%s</loc><lastmod>%s</lastmod></url>" % (esc(SITE_URL), esc(x["url"]), TODAY) for x in PAGES)
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\n' % urls, encoding="utf-8")
(OUT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE_URL)
llm = ["# BSCS Teaching & Learning", "", "Public teaching guidance for Bradley Stoke Community School staff. EEF evidence snapshot checked August 2026. Research evidence, BSCS agreed practice and practitioner guidance are kept distinct. Each strategy page states its evidence rating.", ""]
for kind in ["Home", "Strategy", "Pupil need", "BSCS agreed practice", "Individual Development", "Evidence", "Evidence summary", "Staff guide", "Adviser guidance", "Index", "Reference", "Practitioner profile", "Practitioner summary (Craig Barton)"]:
    items = [x for x in PAGES if x["kind"] == kind]
    if not items: continue
    llm.append("## " + kind); llm += ["- [%s](%s/%s): %s" % (x["title"], SITE_URL, x["url"], x["desc"][:140]) for x in items]; llm.append("")
(OUT / "llms.txt").write_text("\n".join(llm), encoding="utf-8")
print("pages:", len(PAGES))
