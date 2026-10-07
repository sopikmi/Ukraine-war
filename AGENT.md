# Denní agent SITREP Rusko–Ukrajina

Tento soubor je závazný návod pro automatický denní běh, který aktualizuje stránku
`index.html` (GitHub Pages, repozitář `sopikmi/ukraine-war`, větev `main`).
Každý běh začíná bez paměti, proto vše potřebné je zde.

## Cíl běhu
1. Zjistit, co se ve válce změnilo za posledních ~24 hodin.
2. Aktualizovat denní sekci, archiv a denně se měnící čísla v `index.html`.
3. Commitnout a pushnout do `main` (GitHub Pages se přegeneruje sám).
4. Poslat Michalovi krátké shrnutí v češtině.

## Zdroje (v tomto pořadí)
- **ISW** – Russian Offensive Campaign Assessment (understandingwar.org), nejnovější den.
- **Ukrajinský generální štáb** přes https://index.minfin.com.ua/en/russian-invading/casualties/ – kumulativní ztráty osob a techniky + denní přírůstky.
- **Britské MO** – Defence Intelligence update (gov.uk / X).
- **Zpravodajství**: Kyiv Independent, Reuters, Meduza/Mediazona, Euromaidan Press.
- **Východní křídlo NATO**: jen pokud se ten den stalo něco podstatného (narušení vzdušného prostoru, drony, sabotáže, nasazení jednotek).
- Oryx / Russia Matters / think-tanky jen když vyšla nová data.

Používej WebSearch a WebFetch. Když zdroj nejde načíst, přeskoč ho, pokračuj a v denním textu to uveď
jednou větou. Nikdy si čísla nevymýšlej a nepřebírej je z paměti – každé nové číslo musí mít zdroj z dnešního běhu.

## Co upravit v index.html
Upravuj VÝHRADNĚ obsah mezi značkami níže. Značky samotné nikdy nemaž ani nepřejmenovávej,
layout, CSS a ostatní sekce neměň.

| Značka | Obsah |
|---|---|
| `<!--DATE_SHORT-->…<!--/DATE_SHORT-->` | `SITREP · DD.MM.RRRR` (dnešní datum) |
| `<!--DATE_FOOT-->…<!--/DATE_FOOT-->` | `Aktualizace k D. měsíce RRRR.` (český 3. pád, např. „7. říjnu 2026“) |
| `<!--DATE_COVER-->…<!--/DATE_COVER-->` | `D. měsíc RRRR` (1. pád, např. „7. říjen 2026“) |
| `<!--DAILY_START-->…<!--DAILY_END-->` | Dnešní denní sitrep (viz formát níže) – nahraď celý předchozí obsah |
| `<!--ARCHIVE_START-->…<!--ARCHIVE_END-->` | Seznam odkazů na archiv, nejnovější nahoře, max. 14 položek |
| `<!--GS_DATE-->…<!--/GS_DATE-->` | Datum dat gen. štábu, např. `6. 10. 2026` |
| `<!--GS_DATE_SHORT-->…<!--/GS_DATE_SHORT-->` | Totéž krátce, např. `6.10.` |
| `<!--GS_PERSONNEL-->…<!--/GS_PERSONNEL-->` | `~1 xxx 000 (k D.M.RRRR)` – zaokrouhli na tisíce |
| `<!--GS_EQUIP_START-->…<!--GS_EQUIP_END-->` | 6 řádků tabulky techniky (Tanky, Obrněná bojová vozidla, Dělostřelecké systémy, MLRS, Systémy PVO, Letadla) se stejnou HTML strukturou; čísla s mezerou jako oddělovačem tisíců, přírůstek `+N` nebo `—` |

Ostatní analytické sekce (scénáře, ekonomika, NATO, personál…) měň jen tehdy, když vyšla
zásadní nová data, která dosavadní tvrzení zjevně vyvrací – a pak jen dotčenou větu/řádek
se zdrojovým odkazem. V pochybnostech to nech být a jen to zmiň v denním textu.

## Formát denního sitrepu (obsah DAILY)
```html
<p class="intro-text"><b>Stav k D. M. RRRR.</b> Jedna až dvě věty: nejdůležitější vývoj dne.</p>
<h3>Fronta</h3>
<p>Souvislý odstavec: kde se bojovalo, ověřené posuny (podle ISW), hlavní směry.</p>
<h3>Údery a protivzdušná obrana</h3>
<p>…</p>
<h3>Politika, jednání, pomoc</h3>
<p>…</p>
<h3>Východní křídlo NATO</h3>   <!-- jen když se něco stalo -->
<p>…</p>
<p class="small">Zdroje: <a href="…" target="_blank">ISW</a>, <a href="…" target="_blank">…</a>.</p>
```
Pravidla stylu: čeština, věcný OSINT tón, souvislé odstavce (ne odrážky), u tvrzení jedné strany
uveď, že jde o tvrzení strany konfliktu. Bez propagandy, bez spekulací. Celkem cca 250–450 slov.
Odkazy vždy `target="_blank"`.

## Archiv
- Každý den vytvoř soubor `sitrep/RRRR-MM-DD.html` podle šablony `sitrep/_template.html`
  (doplň datum a stejný obsah jako v DAILY).
- Pokud soubor pro dnešní datum už existuje (opakovaný běh), přepiš ho, nevytvářej duplikát.
- Do ARCHIVE vlož seznam `<ul class="archive-list"><li><a href="sitrep/RRRR-MM-DD.html">D. M. RRRR</a> – krátký titulek</li>…</ul>`,
  nejnovější nahoře, max. 14 položek (starší soubory zůstávají v repu, jen nejsou v seznamu).

## Kontrola před commitem
- `python3 -c "import html.parser,sys; html.parser.HTMLParser().feed(open('index.html',encoding='utf-8').read())"` projde.
- Všechny značky jsou v `index.html` stále přítomné právě jednou (`grep -c`).
- `git diff --stat` ukazuje jen `index.html` a soubor v `sitrep/`.

## Git
```
git fetch origin main && git rebase origin/main
git add index.html sitrep/
git commit -m "SITREP RRRR-MM-DD"
git push origin main
```
Když push selže kvůli konfliktu, jednou udělej `git pull --rebase` a zkus znovu. Nic nemaž, nepřepisuj historii, nepoužívej `--force`.

## Závěrečná zpráva
Česky, 4–8 vět: nejdůležitější vývoj dne, nová čísla gen. štábu (osoby + tanky/dělostřelectvo),
případné výpadky zdrojů, a odkaz na https://sopikmi.github.io/ukraine-war/ . Zprávu pošli vždy, i když se nic nezměnilo.
