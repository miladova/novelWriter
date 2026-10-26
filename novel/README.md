# A House of Graces

*A Novel of Rome — Trajan's Rome, AD 111–112*

A freedwoman who built a house is summoned by the family that sold her,
and the past she has spent twenty-four years paying for comes due in the
Senate of Rome.

**Read it in one file:** [`manuscript.md`](manuscript.md) — the complete novel,
25 chapters, ~127,400 words.

**Read it as a book:** [`out/A House of Graces.pdf`](out/A%20House%20of%20Graces.pdf)
— 329 pages, typeset, with contents, running heads and folios.

## Contents

| | |
|---|---|
| `chapters/ch01.md` … `ch25.md` | The novel, chapter by chapter (source of truth) |
| `manuscript.md` | Generated single-file edition of all 25 chapters |
| `build_pdf.py` | Typesetter: front matter, TOC, running heads, folios |
| `fonts/` | EB Garamond (SIL Open Font License) |
| `backmatter.md` | Author's note, glossary, note on the sequence |
| `notes/continuity.md` | Working continuity bible: dates, ages, canon, motifs |
| `out/` | Built PDF |

## Building

```sh
pip install reportlab==4.2.5 pyphen
python3 build_pdf.py            # writes out/A House of Graces.pdf
python3 build_pdf.py --count    # per-chapter word counts
```

The build expects exactly 25 files matching `chapters/ch*.md`.

## The novel

1. **The House** — December. A dinner for a senator, and a summons from the Palatine.
2. **The Dedication** — the Kalends; the Forum of Trajan; Corvinus seen across a crowd.
3. **The Heir** — the Sulpicius house; a loan; the accusation forming.
4. **The Baths** — Felix's first threat; a girl called Calpurnia; Ione freed.
5. **The Villa** — Tibur, autumn 88: the night, the cup, the birth, the sale.
6. **The Bargain** — the reunion, and what it costs.
7. **Februa** — the Lupercalia.
8. **The Price of a Brother** — the slave market.
9. **The Delator's Dinner** — Felix names his price.
10. **The Senate's Door** — the Asian command; the charge of parricide is laid.
11. **Fire** — the storeroom burns; a boy dies in a bolted passage.
12. **Tibur** — the midwife Psyche, the receipt, and the grave.
13. **The Shrine** — the pact with Corvinus.
14. **The Games** — a betrothal, and an arrest.
15. **The Wedding** — and the old woman's letter.
16. **The Ledger** — Ione's rupture; the black book burned; the boy missing.
17. **The Information** — the hearing in the Curia.
18. **The Question** — the prefect's cells; eleven come out of twelve.
19. **The Road to Ostia** — the palace, the bargain, and the deathbed.
20. **The Mother** — Sulpicia Varia's confession, death, funeral and will.
21. **The Trial, Part One** — Psyche; Corvinus speaks for himself; Anthus confesses.
22. **The Trial, Part Two** — the secretary; the verdicts; Nolus's funeral.
23. **The Ashes** — the clients go; Ione returns; the potter's letter.
24. **The Boy** — the Via Ostiensis, and a name spoken aloud.
25. **Saturnalia** — the house remade, and a coda of twenty-two years.

---

*This is a work of fiction. Names, characters, places and incidents are the
products of the author's imagination or are used fictitiously. The novel
contains explicit sexual content, sexual coercion, slavery, violence, torture
and death, and is intended for adult readers.*
