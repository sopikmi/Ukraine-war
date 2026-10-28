#!/usr/bin/env python3
"""Denní komentovaný SITREP psaný Claudem přes Anthropic API (GitHub Actions).

- vezme nejnovější hodnocení ISW (criticalthreats.org) a čísla GŠ (z auto_update.py),
- nechá Clauda napsat český denní text výhradně z dodaných podkladů,
- zkontroluje výstup (HTML, struktura, délka, čísla GŠ) a teprve pak ho vloží do index.html
  a do archivu sitrep/RRRR-MM-DD.html.
Bez API klíče nebo při jakékoli chybě stránku nemění (stará verze zůstane).
"""
import datetime as dt, html, html.parser, json, os, re, sys, urllib.request
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(__file__))
import auto_update as au  # noqa: E402

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5-5")
SM = "https://storymaps.arcgis.com/stories/36a7f6a6f5a9448496de641cf64bd375"
MAX_ARCHIVE = 14


def claude(system, user):
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise SystemExit("ANTHROPIC_API_KEY chybí – komentovaný text se nepíše.")
    body = json.dumps({"model": MODEL, "max_tokens": 4000, "system": system,
                       "messages": [{"role": "user", "content": user}]}).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body, headers={
        "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        j = json.loads(r.read())
    return "".join(b.get("text", "") for b in j["content"] if b.get("type") == "text").strip()


def isw_text(url):
    raw = au.get(url)
    t = au.text_of(raw)
    t = re.sub(r"\s*\n\s*", "\n", t)
    k = t.lower().find("key takeaways")
    if k > 0:
        t = t[max(0, k - 3000):]
    print(f"ISW raw {len(raw)} B, text {len(t)} znaků; ukázka: {t[:300]!r}", file=sys.stderr)
    if len(t) < 8000 or "Key Takeaways" not in t and "key takeaways" not in t.lower():
        raise SystemExit("Text hodnocení ISW se nepodařilo načíst (stránka bez obsahu) – nic neměním.")
    return t[:120_000]


SYSTEM = """Jsi analytik píšící český denní OSINT SITREP o válce Rusko–Ukrajina pro web Michala Šopíka.
Pravidla (závazná):
- Používej VÝHRADNĚ fakta z dodaných podkladů (hodnocení ISW a čísla ukrajinského GŠ). Nic nedomýšlej, nepřidávej vlastní znalosti ani čísla, která v podkladech nejsou.
- U každého tvrzení jedné strany uveď, že jde o tvrzení (ruské MO, ruští blogeři, ukrajinská strana). Rozlišuj, co ISW potvrdil a co ne.
- Čísla přebírej přesně, s mezerou jako oddělovačem tisíců (1 562 970).
- Věcný, nestranný tón, souvislé odstavce, žádné odrážky, žádné spekulace. Celkem 300–550 slov.
- Výstup je POUZE HTML fragment přesně v této struktuře (nic před ani za ním, žádné ```):
<p class="intro-text"><b>Stav k {DATUM}.</b> 2–3 věty: nejdůležitější vývoj.</p>
<h3>Fronta</h3>
<p>…</p>
<h3>Údery a protivzdušná obrana</h3>
<p>…</p>
<h3>Politika a diplomacie</h3>
<p>…</p>
<h3>Ztráty podle ukrajinského generálního štábu</h3>
<p>…přesně dodaná čísla GŠ… Jde o údaje strany konfliktu, nezávisle neověřené.</p>
- Sekci „Politika a diplomacie“ vynech jen tehdy, když v podkladech nic takového není."""


def validate(frag, gs):
    if "```" in frag or "<script" in frag.lower() or "<iframe" in frag.lower():
        raise ValueError("nepovolený obsah")
    for h in ["<h3>Fronta</h3>", "<h3>Údery a protivzdušná obrana</h3>", "<h3>Ztráty podle ukrajinského generálního štábu</h3>"]:
        if h not in frag:
            raise ValueError("chybí sekce " + h)
    if not frag.startswith('<p class="intro-text">'):
        raise ValueError("chybný začátek")
    words = len(re.sub(r"<[^>]+>", " ", frag).split())
    if not 200 <= words <= 800:
        raise ValueError(f"nepřiměřená délka ({words} slov)")
    html.parser.HTMLParser().feed(frag)
    if gs:
        sect = frag.split("<h3>Ztráty podle ukrajinského generálního štábu</h3>", 1)[1]
        if au.fmt(gs["personnel"][0]) not in sect.replace(" ", " "):
            raise ValueError("číslo GŠ v textu nesouhlasí s podklady")


def main():
    today = dt.datetime.now(ZoneInfo("Europe/Prague")).date()
    p = "index.html"; s = open(p, encoding="utf-8").read()
    try:
        isw = au.fetch_isw()
    except Exception as e:
        if os.path.exists(f"sitrep/{today.isoformat()}.html"):
            # Dnešní komentář už existuje – další běh jen dobírá novější ISW; dočasný výpadek zdroje není chyba.
            print("ISW nejde načíst (", e, ") – dnešní SITREP už je hotový, beze změny.", file=sys.stderr); return
        raise
    if not isw:
        raise SystemExit("Hodnocení ISW nenalezeno.")
    isw_date, isw_url = isw
    m = re.search(r"<!--DAILY_ISW:(.*?)-->", s)
    if m and m.group(1) == isw_url:
        print("Toto hodnocení ISW už je zpracované – beze změny."); return
    gsr = au.fetch_gs(today)
    gs_note, gs = "Čísla GŠ nejsou k dispozici – sekci ztrát napiš jen obecně bez čísel.", None
    if gsr:
        d, gs_url, gs = gsr
        gs_note = (f"Čísla ukrajinského GŠ k {d.day}. {d.month}. {d.year} (kumulativně, v závorce denní přírůstek): "
                   + "; ".join(f"{n} {au.fmt(gs[k][0])}" + (f" (+{au.fmt(gs[k][1])})" if gs[k][1] else "")
                               for n, k in [("osoby", "personnel"), ("tanky", "tanks"), ("obrněná vozidla", "afv"),
                                            ("dělostřelectvo", "art"), ("MLRS", "mlrs"), ("PVO", "ad"), ("letadla", "air")]))
    datum = f"{today.day}. {today.month}. {today.year}"
    user = (f"Dnešní datum: {datum}. Hodnocení ISW je z {isw_date.day}. {isw_date.month}. {isw_date.year}.\n\n"
            f"{gs_note}\n\n=== HODNOCENÍ ISW ({isw_url}) ===\n{isw_text(isw_url)}")
    frag = claude(SYSTEM.replace("{DATUM}", datum), user)
    validate(frag, gs)
    src = (f'<p class="small">Zdroje: <a href="{isw_url}" target="_blank">ISW – Russian Offensive Campaign Assessment, '
           f'{isw_date.day}. {isw_date.month}. {isw_date.year}</a>'
           + (f', <a href="{gs_url}" target="_blank">Ministerstvo obrany Ukrajiny / generální štáb</a>' if gs else "")
           + '. Text automaticky sestavil Claude (Anthropic) výhradně z uvedených zdrojů, bez lidské kontroly.</p>')
    fig = (f'<figure class="isw-map" style="margin:20px 0;">\n      <div style="position:relative;width:100%;height:0;padding-bottom:75%;'
           f'min-height:420px;border-radius:8px;overflow:hidden;border:1px solid rgba(128,128,128,.25);">\n        <iframe src="{SM}" '
           f'title="Interaktivní mapa ISW – kontrola území na Ukrajině" loading="lazy" allowfullscreen style="position:absolute;inset:0;'
           f'width:100%;height:100%;border:0;"></iframe>\n      </div>\n      <figcaption class="small">Interaktivní mapa: Institute for the '
           f'Study of War a AEI Critical Threats Project (aktualizuje ISW). <a href="{SM}" target="_blank">Otevřít na celou obrazovku</a> · '
           f'<a href="{isw_url}" target="_blank">hodnocení ISW se statickou mapou</a>.</figcaption>\n    </figure>')
    intro, rest = frag.split("</p>", 1)
    rest = rest.strip()
    k = rest.find("<h3>Ztráty podle ukrajinského")
    rest = (rest[:k] + fig + "\n    " + rest[k:]) if k >= 0 else (rest + "\n    " + fig)
    content = f"\n    <!--DAILY_ISW:{isw_url}-->\n    {intro}</p>\n    {rest}\n    {src}\n    "
    s = au.setm(s, "<!--DAILY_START-->", "<!--DAILY_END-->", content)
    # archiv
    iso = today.isoformat()
    tpl = open("sitrep/_template.html", encoding="utf-8").read()
    open(f"sitrep/{iso}.html", "w", encoding="utf-8").write(tpl.replace("{{DATUM}}", datum).replace("{{OBSAH}}", content))
    title = re.sub(r"<[^>]+>", "", intro).replace(f"Stav k {datum}.", "").strip()
    title = (title.split(". ")[0][:110]).rstrip(".")
    m = re.search(r"<!--ARCHIVE_START-->(.*?)<!--ARCHIVE_END-->", s, re.S)
    items = [li for li in re.findall(r"<li>.*?</li>", m.group(1), re.S) if f"sitrep/{iso}.html" not in li]
    items = [f'<li><a href="sitrep/{iso}.html">{datum}</a> – {html.escape(title)}</li>'] + items
    s = au.setm(s, "<!--ARCHIVE_START-->", "<!--ARCHIVE_END-->",
                '\n    <ul class="archive-list">' + "".join(items[:MAX_ARCHIVE]) + '</ul>\n    ')
    html.parser.HTMLParser().feed(s)
    open(p, "w", encoding="utf-8").write(s)
    print("Komentovaný SITREP zapsán:", iso, isw_url)


if __name__ == "__main__":
    main()
