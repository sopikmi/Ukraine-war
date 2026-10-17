#!/usr/bin/env python3
"""Denní automatická aktualizace (GitHub Actions, bez AI):
- čísla ukrajinského generálního štábu z mod.gov.ua (dnes, jinak včera / předevčírem)
- odkaz na nejnovější hodnocení ISW (criticalthreats.org)
- data na stránce
Upravuje jen obsah mezi značkami v index.html. Když zdroj selže, nic nepřepíše a skončí chybou.
"""
import datetime as dt, html, re, sys, urllib.request
from zoneinfo import ZoneInfo

UA = {"User-Agent": "Mozilla/5.0 (compatible; sitrep-bot; +https://github.com/sopikmi/Ukraine-war)"}
MONTHS_EN = ["january","february","march","april","may","june","july","august","september","october","november","december"]
MES_1 = ["leden","únor","březen","duben","květen","červen","červenec","srpen","září","říjen","listopad","prosinec"]
MES_3 = ["lednu","únoru","březnu","dubnu","květnu","červnu","červenci","srpnu","září","říjnu","listopadu","prosinci"]
NUM = r"(\d{1,3}(?:[   ]\d{3})*|\d+)"

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")

def text_of(raw):
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t).replace(" ", " ").replace(" ", " ")
    return re.sub(r"[ \t]+", " ", t)

def toint(x): return int(re.sub(r"\D", "", x))
def fmt(n): return f"{n:,}".replace(",", " ")

def parse_gs(t):
    out = {}
    m = re.search(r"personnel\s*[‒–—-]?\s*(?:approximately|about)?\s*" + NUM + r"\s*(?:\(\s*\+\s*" + NUM + r"\s*\))?", t, re.I)
    if not m: return None
    out["personnel"] = (toint(m.group(1)), toint(m.group(2)) if m.group(2) else None)
    for key, label in [("tanks","tanks"),("afv","armou?red (?:fighting|combat) vehicles"),("art","artillery systems"),
                       ("mlrs","MLRS"),("ad","air defen[cs]e (?:assets|systems|means)"),("air","aircraft")]:
        m = re.search(r"\b" + label + r"\s*[‒–—-]\s*" + NUM + r"\s*(?:\(\s*\+\s*" + NUM + r"\s*\))?", t, re.I)
        if not m: return None
        out[key] = (toint(m.group(1)), toint(m.group(2)) if m.group(2) else None)
    # plausibility: cumulative personnel must be large
    if out["personnel"][0] < 1_000_000: return None
    return out

def fetch_gs(today):
    for back in range(0, 3):
        d = today - dt.timedelta(days=back)
        url = f"https://mod.gov.ua/en/news/total-russian-combat-losses-in-ukraine-as-of-{MONTHS_EN[d.month-1]}-{d.day}-{d.year}"
        try:
            data = parse_gs(text_of(get(url)))
        except Exception as e:
            print("GS fetch failed", url, e, file=sys.stderr); continue
        if data: return d, url, data
        print("GS parse failed", url, file=sys.stderr)
    # Záloha: veřejné API zrcadlící denní údaje GŠ (mod.gov.ua blokuje servery GitHubu)
    try:
        import json
        j = json.loads(get("https://russianwarship.rip/api/v2/statistics/latest"))
        st, inc = j["stats"], j["increase"]
        d = dt.date.fromisoformat(j["date"])
        if (today - d).days > 3 or st["personnel_units"] < 1_000_000: raise ValueError("stale/implausible")
        m = {"personnel":"personnel_units","tanks":"tanks","afv":"armoured_fighting_vehicles","art":"artillery_systems",
             "mlrs":"mlrs","ad":"aa_warfare_systems","air":"planes"}
        data = {k: (int(st[v]), int(inc.get(v) or 0) or None) for k, v in m.items()}
        url = f"https://mod.gov.ua/en/news/total-russian-combat-losses-in-ukraine-as-of-{MONTHS_EN[d.month-1]}-{d.day}-{d.year}"
        return d, url, data
    except Exception as e:
        print("GS fallback failed", e, file=sys.stderr)
    return None

def fetch_isw():
    raw = get("https://www.criticalthreats.org/analysis")
    best = None
    for slug in set(re.findall(r"/analysis/(russian-offensive-campaign-assessment-([a-z]+)-(\d{1,2})-(\d{4})[a-z0-9-]*)", raw)):
        full, mon, day, yr = slug
        if mon not in MONTHS_EN: continue
        d = dt.date(int(yr), MONTHS_EN.index(mon) + 1, int(day))
        if best is None or d > best[0]: best = (d, "https://www.criticalthreats.org/analysis/" + full)
    return best

def setm(s, a, b, new):
    pat = re.escape(a) + r".*?" + re.escape(b)
    if len(re.findall(pat, s, flags=re.S)) != 1: raise SystemExit(f"marker {a} not found exactly once")
    return re.sub(pat, lambda m: a + new + b, s, flags=re.S)

def main():
    today = dt.datetime.now(ZoneInfo("Europe/Prague")).date()
    p = "index.html"; s = open(p, encoding="utf-8").read(); orig = s
    gs = fetch_gs(today)
    try: isw = fetch_isw()
    except Exception as e: print("ISW fetch failed", e, file=sys.stderr); isw = None
    if not gs and not isw: raise SystemExit("Ani jeden zdroj nejde načíst – stránka beze změny.")
    parts = []
    if gs:
        d, url, g = gs
        inc = lambda v: f"+{fmt(v)}" if v else "—"
        rows = "\n" + "".join(f'          <tr><td>{n}</td><td class="num">{fmt(g[k][0])}</td><td class="num">{inc(g[k][1])}</td></tr>\n'
            for n, k in [("Tanky","tanks"),("Obrněná bojová vozidla","afv"),("Dělostřelecké systémy","art"),
                         ("MLRS (raketomety)","mlrs"),("Systémy PVO","ad"),("Letadla","air")]) + "          "
        s = setm(s, "<!--GS_EQUIP_START-->", "<!--GS_EQUIP_END-->", rows)
        s = setm(s, "<!--GS_DATE-->", "<!--/GS_DATE-->", f"{d.day}. {d.month}. {d.year}")
        s = setm(s, "<!--GS_DATE_SHORT-->", "<!--/GS_DATE_SHORT-->", f"{d.day}.{d.month}.")
        s = setm(s, "<!--GS_PERSONNEL-->", "<!--/GS_PERSONNEL-->", f"~{fmt(round(g['personnel'][0], -3))} (k {d.day}.{d.month}.{d.year})")
        s = re.sub(r"https://mod\.gov\.ua/en/news/total-russian-combat-losses-in-ukraine-as-of-[a-z]+-\d+-\d{4}", url, s)
        p0, p1 = g["personnel"]
        parts.append(f'Ukrajinský generální štáb k {d.day}. {d.month}. {d.year}: přibližně {fmt(p0)} ruských ztrát na osobách'
                     + (f" (+{fmt(p1)} za den)" if p1 else "") + f', {fmt(g["tanks"][0])} tanků, {fmt(g["art"][0])} dělostřeleckých systémů '
                     f'(<a href="{url}" target="_blank">zdroj</a>; údaje strany konfliktu).')
    if isw:
        d, url = isw
        parts.append(f'Nejnovější hodnocení ISW: <a href="{url}" target="_blank">Russian Offensive Campaign Assessment, {d.day}. {d.month}. {d.year}</a> (se statickými mapami).')
    now = dt.datetime.now(ZoneInfo("Europe/Prague"))
    auto = ('\n    <div class="callout"><b>Automatická denní aktualizace ' + f"{today.day}. {today.month}. {today.year}" + ':</b> '
            + " ".join(parts) + ' Komentovaný souhrn níže může být o den či dva starší.</div>\n    ')
    s = setm(s, "<!--AUTO_START-->", "<!--AUTO_END-->", auto)
    s = setm(s, "<!--DATE_SHORT-->", "<!--/DATE_SHORT-->", f"SITREP · {today.day:02d}.{today.month:02d}.{today.year}")
    s = setm(s, "<!--DATE_FOOT-->", "<!--/DATE_FOOT-->", f"Aktualizace k {today.day}. {MES_3[today.month-1]} {today.year}.")
    s = setm(s, "<!--DATE_COVER-->", "<!--/DATE_COVER-->", f"{today.day}. {MES_1[today.month-1]} {today.year}")
    import html.parser; html.parser.HTMLParser().feed(s)
    if s != orig: open(p, "w", encoding="utf-8").write(s); print("updated")
    else: print("no change")
    if not gs or not isw: raise SystemExit("Jeden ze zdrojů nešel načíst (viz log) – druhý byl aktualizován.")

if __name__ == "__main__": main()
