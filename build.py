#!/usr/bin/env python3
"""Genereert index.html (GitHub Pages) uit keukenprijs-index-2026.json.

Eén bron: de JSON. Draai na update.sh opnieuw: `python build.py`.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / "keukenprijs-index-2026.json").read_text(encoding="utf-8"))
SITE = "https://alfareclame.github.io/keukenprijs-index/"


def eur(n):
    return "€ " + f"{n:,}".replace(",", ".")


def band(r):
    s = f"{eur(r['min'])} – {eur(r['max'])}"
    if r.get("openBovengrens"):
        s += "+"
    if r.get("opmerking"):
        s += f" <small>({html.escape(r['opmerking'])})</small>"
    return s


def e(s):
    return html.escape(str(s))


def datum_nl(iso):
    j, m, d = iso.split("-")
    return f"{d}-{m}-{j}"


rows_opst = "\n".join(
    f"<tr><th scope=row>{e(o['opstelling'])}</th>"
    f"<td>{band(o['segmenten']['instap'])}</td>"
    f"<td>{band(o['segmenten']['middensegment'])}</td>"
    f"<td>{band(o['segmenten']['premium'])}</td></tr>"
    for o in DATA["perOpstelling"]
)
rows_merk = "\n".join(
    f"<tr><th scope=row><a href=\"{e(m['url'])}\">{e(m['merk'])}</a></th>"
    f"<td>{e(m['segment'])}</td><td>{band(m['vanaf'])}</td></tr>"
    for m in DATA["perMerk"]
)

bron = DATA["bronUrl"]
gem = DATA["landelijkGemiddelde"]
bijgewerkt = datum_nl(DATA["bijgewerkt"])
citatie = f"{DATA['citatie']} — {bron} — CC BY 4.0"

jsonld = {
    "@context": "https://schema.org",
    "@type": "Dataset",
    "name": f"{DATA['naam']} {DATA['editie']}",
    "description": DATA["beschrijving"],
    "url": SITE,
    "isBasedOn": bron,
    "license": DATA["licentie"],
    "inLanguage": DATA["taal"],
    "spatialCoverage": {"@type": "Country", "name": "Nederland"},
    "temporalCoverage": str(DATA["editie"]),
    "dateModified": DATA["bijgewerkt"],
    "creator": {
        "@type": "Organization",
        "name": DATA["uitgever"]["naam"],
        "url": "https://keukeninbeeld.nl/",
    },
    "distribution": [
        {
            "@type": "DataDownload",
            "encodingFormat": "application/json",
            "contentUrl": "https://keukeninbeeld.nl/keukenprijs-index.json",
        },
        {
            "@type": "DataDownload",
            "encodingFormat": "application/json",
            "contentUrl": SITE + "keukenprijs-index-2026.json",
        },
    ],
}

page = f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Keukenprijs-index Nederland {DATA['editie']} — open dataset (CC BY 4.0)</title>
<meta name="description" content="Open dataset met richtprijzen voor een nieuwe keuken in Nederland: per opstelling, prijssegment en keukenmerk. Gratis te gebruiken met bronvermelding (CC BY 4.0).">
<link rel="canonical" href="{SITE}">
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
<style>
:root{{--fg:#1d1d1b;--mut:#5b5b57;--bg:#fbfaf7;--line:#e4e1da;--acc:#8a5a2b}}
@media (prefers-color-scheme:dark){{:root{{--fg:#ecebe6;--mut:#a9a8a1;--bg:#191917;--line:#33322f;--acc:#d9a46b}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,-apple-system,Segoe UI,sans-serif}}
main{{max-width:860px;margin:0 auto;padding:32px 16px 64px}}
h1{{font-size:1.9rem;line-height:1.2;margin:0 0 8px}}h2{{margin-top:2.2em;font-size:1.25rem}}
p.lead{{color:var(--mut);margin-top:0}}a{{color:var(--acc)}}
.tbl{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}}
th,td{{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}}
thead th{{font-size:.85rem;color:var(--mut);font-weight:600}}
pre{{background:rgba(127,127,127,.12);padding:12px;border-radius:6px;overflow-x:auto;font-size:.9rem;white-space:pre-wrap}}
small,.mut{{color:var(--mut)}}footer{{margin-top:48px;font-size:.9rem;color:var(--mut)}}
</style>
</head>
<body>
<main>
<h1>Keukenprijs-index Nederland {DATA['editie']}</h1>
<p class="lead">Open dataset met richtprijzen voor een complete nieuwe keuken — per opstelling, prijssegment en keukenmerk. Bijgewerkt {bijgewerkt}. Licentie CC BY 4.0.</p>

<p>Een complete nieuwe keuken kost in Nederland gemiddeld <strong>{eur(gem['min'])} tot {eur(gem['max'])}</strong>. {e(DATA['grondslag'])}</p>
<p>De index wordt onafhankelijk samengesteld door <a href="https://keukeninbeeld.nl/">Keuken in Beeld</a>, dat zelf geen keukens verkoopt. Methode, toelichting en regiopatronen staan in de <a href="{e(bron)}">leesbare versie van de Keukenprijs-index</a>.</p>

<h2>Richtprijs per opstelling</h2>
<p class="mut">{e(DATA['toelichting']['opstelling'])}</p>
<div class="tbl"><table>
<thead><tr><th>Opstelling</th><th>Instap</th><th>Middensegment</th><th>Premium</th></tr></thead>
<tbody>
{rows_opst}
</tbody></table></div>
<p>Wat kost jouw eigen opstelling ongeveer? Zie <a href="https://keukeninbeeld.nl/keuken-kosten">wat een nieuwe keuken kost</a>.</p>

<h2>Vanaf-prijs per keukenmerk</h2>
<p class="mut">{e(DATA['toelichting']['merk'])}</p>
<div class="tbl"><table>
<thead><tr><th>Merk</th><th>Segment</th><th>Vanaf</th></tr></thead>
<tbody>
{rows_merk}
</tbody></table></div>
<p>Alle merken naast elkaar: <a href="https://keukeninbeeld.nl/keukenmerken">keukenmerken vergelijken</a>.</p>

<h2>Gebruiken en citeren</h2>
<p>Vrij te gebruiken in artikelen, onderzoek en tools, ook commercieel, met bronvermelding:</p>
<pre>{e(citatie)}</pre>
<p>Ruwe data (JSON): <a href="keukenprijs-index-2026.json">keukenprijs-index-2026.json</a> · altijd de nieuwste editie: <a href="https://keukeninbeeld.nl/keukenprijs-index.json">keukeninbeeld.nl/keukenprijs-index.json</a></p>
<pre>curl -s https://keukeninbeeld.nl/keukenprijs-index.json | jq '.perOpstelling'</pre>
<p>Op je eigen website tonen? Gebruik de <a href="https://keukeninbeeld.nl/keukenprijs-index-insluiten">embed-widget</a>. Grafieken en kerncijfers voor journalisten: <a href="https://keukeninbeeld.nl/pers">perskit</a>.</p>

<footer>
<p>Bron: <a href="https://keukeninbeeld.nl/">Keuken in Beeld</a> (onderdeel van {e(DATA['uitgever']['onderdeelVan'])}, KvK {e(DATA['uitgever']['kvk'])}). Broncode van deze pagina: <a href="https://github.com/alfareclame/keukenprijs-index">github.com/alfareclame/keukenprijs-index</a>.</p>
<p lang="en">English: open dataset of indicative new-kitchen prices in the Netherlands. <a href="https://keukeninbeeld.nl/en/kitchen-prices-netherlands">Kitchen prices in the Netherlands</a>.</p>
</footer>
</main>
</body>
</html>
"""

(ROOT / "index.html").write_text(page, encoding="utf-8", newline="\n")
print("index.html geschreven:", len(DATA["perOpstelling"]), "opstellingen,", len(DATA["perMerk"]), "merken")
