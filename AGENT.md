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
- **ISW** – Russian Offensive Campaign Assessment. understandingwar.org je pro WebFetch blokovaný, čti zrcadlo `https://www.criticalthreats.org/analysis/russian-offensive-campaign-assessment-<month>-<d>-<yyyy>` (např. `october-6-2026`), nejnovější dostupný den.
- **Ukrajinský generální štáb** přes MO Ukrajiny: `https://mod.gov.ua/en/news/total-russian-combat-losses-in-ukraine-as-of-<month>-<d>-<yyyy>` (např. `october-6-2026`). Zkus dnešek, při 404 včerejšek, pak předevčírem. Minfin.index NEPOUŽÍVEJ – vrací zastaralá data z roku 2025.
- **Britské MO** – Defence Intelligence update (gov.uk / X).
- **Zpravodajství**: Kyiv Independent, Reuters, Meduza/Mediazona, Euromaidan Press.
- **Východní křídlo NATO**: jen pokud se ten den stalo něco podstatného (narušení vzdušného prostoru, drony, sabotáže, nasazení jednotek).
- Oryx / Russia Matters / think-tanky jen když vyšla nová data.

### Michalovy oblíbené OSINT zdroje (X a YouTube)
X i YouTube blokují přímé načítání (robots.txt), proto je nečti přes WebFetch na x.com / youtube.com.
Místo toho pro každý udělej jedno WebSearch omezené na posledních ~24–48 h a použij, co najdeš
v čitelné podobě (články, které je citují, přepisy, zrcadla):
- **Majakovsk73** (X, @Majakovsk73) – mapy a posuny fronty.
- **Clément Molin** (X) – francouzský analytik, mapy a souhrny fronty.
- **Denys Davydov** (YouTube) – denní videoshrnutí bývalého ukrajinského pilota.
Když nic čitelného nenajdeš, prostě je přeskoč – nevymýšlej, co v příspěvcích nebo videích „asi“ zaznělo.
Když je najdeš, uveď je ve zdrojích denního sitrepu a u tvrzení, která potvrzuje jen jeden z nich, to napiš.

Používej WebSearch a WebFetch. Když zdroj nejde načíst, přeskoč ho, pokračuj a v denním textu to uveď
jednou větou. Nikdy si čísla nevymýšlej a nepřebírej je z paměti – každé nové číslo musí mít zdroj z dnešního běhu.

## Pravidla ověřování čísel (závazná)
- Čísla ber z **primárního zdroje** (Mediazona, CSIS, OSN/HRMMU, MO Ukrajiny, Oryx, vládní a NATO data, renomovaná média citující primární zdroj). Anonymní agregátory (např. wardeathdata.com, factually.co) jako zdroj čísel NEPOUŽÍVEJ.
- Při WebFetch si vždy vyžádej **doslovnou citaci** věty s číslem a datem; shrnutí od fetch nástroje se může mýlit.
- U každého čísla uveď, **k jakému datu nebo období** platí, a ověř, že popis odpovídá zdroji (padlí × celkové ztráty, celkem × jen za rok).
- **Kontrola konzistence:** statistický odhad padlých musí být vyšší než jmenovitý (ověřený) počet; poměr ztrát musí odpovídat číslům v tabulkách; data se nesmí vzájemně vylučovat. Když něco nesedí, číslo nepřepisuj a uveď nesoulad v závěrečné zprávě.
- Údaj, který nejde ověřit, označ („nepodařilo se ověřit“) nebo ho ponech beze změny – nikdy ho nedomýšlej.

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
<figure class="isw-map" style="margin:20px 0;">
      <div style="position:relative;width:100%;height:0;padding-bottom:75%;min-height:420px;border-radius:8px;overflow:hidden;border:1px solid rgba(128,128,128,.25);">
        <iframe src="https://storymaps.arcgis.com/stories/36a7f6a6f5a9448496de641cf64bd375" title="Interaktivní mapa ISW – kontrola území na Ukrajině" loading="lazy" allowfullscreen style="position:absolute;inset:0;width:100%;height:100%;border:0;"></iframe>
      </div>
      <figcaption class="small">Interaktivní mapa: Institute for the Study of War a AEI Critical Threats Project (aktualizuje ISW). <a href="https://storymaps.arcgis.com/stories/36a7f6a6f5a9448496de641cf64bd375" target="_blank">Otevřít na celou obrazovku</a> · <a href="URL_DNESNIHO_HODNOCENI_ISW" target="_blank">dnešní hodnocení ISW se statickou mapou</a>.</figcaption>
    </figure>
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

### Mapa ISW (povinná součást denního sitrepu)
- Statický obrázek mapy z criticalthreats.org NEVKLÁDEJ – web blokuje zobrazení na cizích stránkách.
- Místo toho vždy vlož blok `<figure class="isw-map">` z formátu výše: interaktivní mapu ISW (iframe ArcGIS StoryMaps, adresa je stálá a ISW ji sám aktualizuje)
  a v popisku odkaz na dnešní hodnocení ISW (URL_DNESNIHO_HODNOCENI_ISW = adresa hodnocení na criticalthreats.org, ze kterého jsi čerpal).
- Nic z map nekopíruj do repozitáře – autorská práva má ISW.

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
případné výpadky zdrojů, a odkaz na https://sopikmi.github.io/Ukraine-war/ . Zprávu pošli vždy, i když se nic nezměnilo.

## Týdenní kompletní revize (každou neděli)
V neděli udělej nejdřív běžný denní sitrep a potom projdi CELOU stránku, sekci po sekci:

1. **Ztráty na životech** – aktualizuj všechny řádky obou tabulek (Mediazona, WarDeathData, odhady rozvědek, Russia Matters, OHCHR civilní oběti…) na nejnovější dostupná čísla. U každého změněného čísla aktualizuj datum v textu a odkaz na zdroj. Když novější číslo neexistuje, ponech staré.
2. **Ruská tvrzení o ztrátách UA** – doplň nová významná tvrzení a jejich ověření (EUvsDisinfo, ověřovací redakce).
3. **Technika** – kromě tabulky gen. štábu i nezávislé křížové odhady (Oryx, IISS, Kofman) a sekce o efektivitě ofenziv a ztrátách UA techniky.
4. **Personál, ekonomika, kapacita vůči NATO** – nová data o náboru, mobilizaci, rozpočtu, HDP, inflaci, příjmech z ropy, obnově výroby.
5. **Mírová jednání a časová osa** – doplň do časové osy důležité události uplynulého týdne (stejný HTML formát jako existující položky).
6. **Scénáře** – zhodnoť, zda vývoj týdne posouvá pravděpodobnost scénářů; upravuj jen se zdůvodněním a zdrojem.
7. **Východní křídlo NATO** – stav nasazení, incidenty, nové plány; mapu (obrázek) neměň.
8. **Zdroje** – ověř, že odkazy ve „Kompletní seznam odkazů“ fungují; nefunkční nahraď nebo označ.
9. Nadpisy s časovým rozsahem (např. „únor 2022 – srpen 2026“), lede v úvodu a datum „Stav k“ uveď do aktuálního stavu.

Pravidla revize: zachovej strukturu, CSS, id sekcí a všechny značky `<!--…-->`; měň obsah, ne layout.
Každé nové číslo či tvrzení musí mít zdroj z tohoto běhu. Commit pojmenuj `Týdenní revize RRRR-MM-DD`.
V závěrečné zprávě přidej odstavec „Týdenní revize“: co se v kterých sekcích změnilo a co zůstalo bez nových dat.
