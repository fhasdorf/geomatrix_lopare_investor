# Claude-Code-Patch: Contact-Section entfernen

**Stand:** 2026-06-20
**Repo:** `geomatrix_lopare_investor`
**Ziel:** Die Contact-Page komplett aus der App entfernen — Datei löschen + alle Verweise in Content-Files und Dashboard bereinigen.

**Out of scope:** Keine neue Funktionalität, keine Layout-Änderungen.

---

## Voraussetzungen

- [ ] Letzter Commit ist Phase 5 (Dashboard)
- [ ] App läuft fehlerfrei lokal
- [ ] `pytest -v` 9/9 grün

---

## Schritt 1 — Page-Datei löschen

```bash
rm app/pages/4_Contact.py
```

Die Streamlit-Multipage-Navigation entfernt den Sidebar-Eintrag automatisch, sobald die Datei weg ist.

## Schritt 2 — Verweise in Opportunity-Content entfernen

In `content/opportunity_en.md` die letzte Section "7. Get in Touch" komplett entfernen:

**Vorher:**
```markdown
## 7. Get in Touch

For access to the data room, the full CSA Global report, or to discuss the
investment opportunity, please use the [Contact](Contact) page.

---

*This page contains forward-looking statements and is subject to the
[Disclaimer](Disclaimer). All resource numbers are sourced from the public
CSA Global R268.2022 report.*
```

**Nachher:**
```markdown
---

*This page contains forward-looking statements and is subject to the
[Disclaimer](Disclaimer). All resource numbers are sourced from the public
CSA Global R268.2022 report.*
```

Numerierung der vorhergehenden Sections bleibt 1–6 (keine Renumerierung nötig — 7 fällt einfach weg).

In `content/opportunity_de.md` analog die Section "7. Kontakt aufnehmen" entfernen:

**Vorher:**
```markdown
## 7. Kontakt aufnehmen

Für Zugang zum Datenraum, dem vollständigen CSA-Global-Bericht oder für ein
Investitionsgespräch nutzen Sie bitte die [Kontakt](Contact)-Seite.

---

*Diese Seite enthält zukunftsgerichtete Aussagen und unterliegt dem
[Disclaimer](Disclaimer). Alle Ressourcenzahlen stammen aus dem öffentlichen
CSA-Global-Bericht R268.2022.*
```

**Nachher:**
```markdown
---

*Diese Seite enthält zukunftsgerichtete Aussagen und unterliegt dem
[Disclaimer](Disclaimer). Alle Ressourcenzahlen stammen aus dem öffentlichen
CSA-Global-Bericht R268.2022.*
```

## Schritt 3 — Disclaimer-Files auf Contact-Verweise prüfen

Falls in `content/disclaimer_en.md` oder `disclaimer_de.md` ein Link auf `Contact` existiert (z.B. im Privacy- oder Imprint-Block), den ebenfalls entfernen oder umformulieren:

```bash
grep -n "Contact\|Kontakt" content/disclaimer_*.md
```

Falls Treffer kommen — Frank entscheidet, ob die Verweise auf etwas anderes umgeschrieben werden (z.B. eine generische Email-Adresse) oder ganz raus. Für jetzt: ersatzlos streichen, sofern sie nicht für den juristischen Disclaimer erforderlich sind.

## Schritt 4 — Sanity-Check

```bash
pytest -v                                    # 9/9 grün halten
streamlit run app/streamlit_app.py
```

**Manuell prüfen:**
- [ ] Sidebar zeigt nur noch 4 Pages: `streamlit app` / `Project Map` / `Opportunity` / `Dashboard` / `Disclaimer` (Contact ist weg)
- [ ] Opportunity-Page Sections enden mit Section 6 ("About the Operator")
- [ ] Keine 404-/Broken-Link-Fehler in der Konsole
- [ ] `grep -rn "Contact" app/ content/` zeigt nur noch unkritische Treffer (z.B. im Disclaimer-Imprint, falls behalten)

---

## Definition of Done

- [ ] `app/pages/4_Contact.py` ist gelöscht
- [ ] Opportunity-MDs ohne Section 7
- [ ] Disclaimer-Verweise auf Contact bereinigt oder bewusst behalten
- [ ] `pytest -v` weiterhin 9/9 grün
- [ ] App startet und zeigt 5 Pages in der Sidebar (ohne Contact)

## Stop-Gate

Nach Abschluss: zeig Frank
1. Sidebar-Screenshot oder Liste der sichtbaren Pages
2. `git status` vor Commit
3. Bestätigung, dass keine Broken Links übrig sind

Erst dann committen.
