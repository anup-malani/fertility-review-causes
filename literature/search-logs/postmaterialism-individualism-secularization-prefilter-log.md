# D.1.a — deterministic pre-filter before the LLM screen

Removes the clinical/veterinary collision and the book reviews mechanically, so the paid screen is not spent reading obstetrics abstracts. No model, no scoring, no threshold: a named term fires or it does not, and **every drop is attributable to the term that caused it**.

> ## ⚠ CALIBRATED ON AN INCOMPLETE CORPUS

> `GENERIC_VALUES` had not finished pulling when this ran, so the term list is tuned on **11,425** records rather than the full universe. The counts below will move. **This filter must be re-run and its rejected sample re-read once C1 completes** — a filter validated at one order of magnitude has been wrong at the next three times on this chapter.

- corpus in: **11,425**
- kept for screening: **10,234**
- dropped: **1,017** (8.9%)
- routed to the book-review retrieval worklist: **174**
- gold records present in the corpus and run through the filter: **303**
- **gold lost: 0**  ← gate passed

## Design

1. **Drops match the title only.** The collision is a title-vocabulary phenomenon. The abstract is read only as *rescue* evidence, so it can keep a record and never remove one.
2. **Every pattern is word-anchored.** Three unanchored-substring bugs are already on this codebase's record (`hous` in C.2.c, `reproduc\w+` in v1, a bare `429` matching a Unix timestamp in the transport layer).
3. **Any rescue signal overrides any drop term**, because a wrongly-kept record costs one LLM read and a wrongly-dropped record costs the study. The rescue vocabulary is demographic and religious only — it contains no value-scale words, since `individualis` and `materialis` are exactly what OpenAlex stemming corrupts.

## Terms proposed and refused, with the record that refused them

Kept in the source so a later reader does not re-propose an exclusion this run already measured and rejected. The last row concerns the *rescue* list rather than the drop list.

| proposed term | why it was refused | the record |
|---|---|---|
| `breastfeeding / lactation` | core proximate-determinants demography (Bongaarts), not clinical | *In Kenya, Modernization, Drop in Breastfeeding and Low Contraceptive Use Bring Rising Fertility* |
| `postpartum` | postpartum insusceptibility is a proximate determinant of natural fertility | *Birth and Breastfeeding Dynamics in a Modernizing Indigenous Community* |
| `the phrase "value of"` | matches 379 records of which only 118 are clinical; the rest are the Value of Children literature, which is on-pair S1/S5 | *Changing Value of Children and Fertility Transition in Turkey* |
| `birth interval / birth spacing` | the classic demographic spacing literature | *(pre-emptive: named in the scope's outcome vocabulary)* |
| `pregnancy / pregnant` | used throughout demography for reported pregnancies and intentions | *(pre-emptive: would drop fertility-intention surveys wholesale)* |
| `bare *secular* as a rescue term` | the religious senses are enumerated instead; `secular\w+` silently never matches the bare word and `secular\w*` rescues the term-of-art | *Secular Trends in Preterm Birth Rates (term of art) vs. Secular values and childbearing* |

## Per-term firing — what each term actually removed

`rescued` counts records where the term fired but a demographic or religious signal kept the record anyway. **A term with a high rescue share is doing little work and carrying real risk.**

| term | dropped | rescued | rescue share |
|---|---|---|---|
| `OBSTETRIC:birth ?weight` | 230 | 43 | 16% |
| `OBSTETRIC:preterm` | 140 | 24 | 15% |
| `type=book-review` | 88 | 0 | 0% |
| `AGRONOMY:soils?` | 81 | 3 | 4% |
| `SECULAR_TERM_OF_ART:secular trends?` | 75 | 38 | 34% |
| `OBSTETRIC:neonat\w+` | 61 | 10 | 14% |
| `ART_CLINICAL:embryos?` | 43 | 9 | 17% |
| `OBSTETRIC:gestational` | 39 | 6 | 13% |
| `ART_CLINICAL:in vitro` | 35 | 5 | 12% |
| `OBSTETRIC:obstetric\w*` | 32 | 14 | 30% |
| `OBSTETRIC:caesarean` | 32 | 3 | 9% |
| `OBSTETRIC:fetal` | 30 | 1 | 3% |
| `OBSTETRIC:cervical` | 27 | 5 | 16% |
| `OBSTETRIC:cesarean` | 24 | 13 | 35% |
| `SECULAR_TERM_OF_ART:secular changes?` | 23 | 11 | 32% |
| `ANIMAL_LAB:cattle` | 22 | 0 | 0% |
| `ART_CLINICAL:sperm` | 21 | 2 | 9% |
| `ART_CLINICAL:ovarian` | 19 | 5 | 21% |
| `OBSTETRIC:perinat\w+` | 18 | 12 | 40% |
| `OBSTETRIC:trimester` | 17 | 0 | 0% |
| `AGRONOMY:yields?` | 17 | 1 | 6% |
| `ART_CLINICAL:ivf` | 17 | 2 | 11% |
| `ART_CLINICAL:semen` | 17 | 2 | 11% |
| `AGRONOMY:crops?` | 17 | 1 | 6% |
| `OBSTETRIC:placent\w+` | 16 | 1 | 6% |
| `ANIMAL_LAB:rats?` | 15 | 0 | 0% |
| `OBSTETRIC:ultraso\w+` | 14 | 1 | 7% |
| `ART_CLINICAL:endometri\w+` | 13 | 2 | 13% |
| `OBSTETRIC:antenatal` | 13 | 13 | 50% |
| `ART_CLINICAL:assisted reproductive technolog\w+` | 11 | 8 | 42% |
| `ART_CLINICAL:blastocysts?` | 11 | 1 | 8% |
| `ART_CLINICAL:blastocyst` | 10 | 1 | 9% |
| `ANIMAL_LAB:sheep` | 9 | 1 | 10% |
| `ART_CLINICAL:follicles?` | 9 | 0 | 0% |
| `ART_CLINICAL:progesterone` | 8 | 2 | 20% |
| `ART_CLINICAL:oocytes?` | 8 | 7 | 47% |
| `ANIMAL_LAB:calves` | 7 | 0 | 0% |
| `ANIMAL_LAB:mice` | 6 | 1 | 14% |
| `OBSTETRIC:intrapartum` | 6 | 0 | 0% |
| `AGRONOMY:seedlings?` | 6 | 0 | 0% |
| `AGRONOMY:fertili[sz]ers?` | 6 | 0 | 0% |
| `AGRONOMY:manure` | 6 | 0 | 0% |
| `ANIMAL_LAB:calving` | 5 | 0 | 0% |
| `ART_CLINICAL:follitropin` | 5 | 0 | 0% |
| `AGRONOMY:maize` | 5 | 0 | 0% |
| `ANIMAL_LAB:goats?` | 5 | 0 | 0% |
| `OBSTETRIC:cervix` | 5 | 0 | 0% |
| `ART_CLINICAL:cryopreservation` | 4 | 7 | 64% |
| `AGRONOMY:wheat` | 4 | 0 | 0% |
| `AGRONOMY:forage` | 4 | 1 | 20% |
| `OBSTETRIC:apgar` | 4 | 0 | 0% |
| `ANIMAL_LAB:murine` | 4 | 0 | 0% |
| `ART_CLINICAL:insemination` | 4 | 2 | 33% |
| `ANIMAL_LAB:livestock` | 4 | 2 | 33% |
| `ANIMAL_LAB:sows?` | 4 | 0 | 0% |
| `AGRONOMY:pasture` | 3 | 0 | 0% |
| `ANIMAL_LAB:bovine` | 3 | 1 | 25% |
| `ART_CLINICAL:icsi` | 3 | 0 | 0% |
| `ANIMAL_LAB:swine` | 3 | 0 | 0% |
| `ANIMAL_LAB:boars?` | 3 | 0 | 0% |
| `ANIMAL_LAB:broilers?` | 3 | 0 | 0% |
| `OBSTETRIC:amniotic` | 3 | 0 | 0% |
| `ANIMAL_LAB:buffalo\w*` | 3 | 0 | 0% |
| `ART_CLINICAL:spermatid\w*` | 2 | 0 | 0% |
| `ANIMAL_LAB:drosophila` | 2 | 1 | 33% |
| `ART_CLINICAL:azoospermi\w+` | 2 | 0 | 0% |
| `AGRONOMY:cropping` | 2 | 0 | 0% |
| `AGRONOMY:agronom\w+` | 2 | 1 | 33% |
| `ANIMAL_LAB:heifers?` | 2 | 0 | 0% |
| `ANIMAL_LAB:stallions?` | 2 | 0 | 0% |
| `AGRONOMY:paddy` | 2 | 0 | 0% |
| `AGRONOMY:legumes?` | 2 | 0 | 0% |
| `AGRONOMY:nutrient uptake` | 2 | 0 | 0% |
| `ART_CLINICAL:embryonic` | 2 | 1 | 33% |
| `ART_CLINICAL:spermatozoa` | 2 | 0 | 0% |
| `ART_CLINICAL:in-vitro` | 2 | 0 | 0% |
| `ART_CLINICAL:intracytoplasmic` | 2 | 0 | 0% |
| `AGRONOMY:biochar` | 2 | 0 | 0% |
| `OBSTETRIC:uterocervical` | 1 | 0 | 0% |
| `AGRONOMY:horticultur\w+` | 1 | 0 | 0% |
| `ART_CLINICAL:luteal` | 1 | 1 | 50% |
| `ANIMAL_LAB:mares?` | 1 | 0 | 0% |
| `SECULAR_TERM_OF_ART:secular variations?` | 1 | 2 | 67% |
| `OBSTETRIC:foetal` | 1 | 0 | 0% |
| `ANIMAL_LAB:porcine` | 1 | 0 | 0% |
| `ART_CLINICAL:cryopreserved` | 1 | 0 | 0% |
| `ART_CLINICAL:follicular` | 1 | 0 | 0% |
| `ART_CLINICAL:ovulation` | 1 | 0 | 0% |
| `ANIMAL_LAB:hatchability` | 1 | 0 | 0% |
| `AGRONOMY:tillage` | 1 | 0 | 0% |
| `OBSTETRIC:neonate` | 1 | 1 | 50% |

Terms that fired but **never** caused a drop (every hit was rescued) — these are carrying no weight and are candidates for removal:

- `ANIMAL_LAB:semen quality` (1 rescued)
- `OBSTETRIC:eclampsi\w+` (1 rescued)
- `OBSTETRIC:stillbirths?` (5 rescued)
- `SECULAR_TERM_OF_ART:secular declines?` (1 rescued)
- `SECULAR_TERM_OF_ART:secular increases?` (1 rescued)

## Book reviews are a retrieval worklist, not a rejection class

The first version of this filter sent all 262 book reviews to `OFF_OTHER`. Reading the rejected sample showed what that deletes — reviews of **Jones and Grupp, *Modernization, Value Change, and Fertility in the Soviet Union***, **Yaukey, *Fertility Differences in a Modernizing Country***, and **Fukuda, *Marriage and fertility behaviour in Japan — Economic status and value orientation***. Those are on-pair monographs and the review is the only trace of them the pull returned. **This chapter has hit an indexing gap on books, chapters, dissertations and non-English work five separate times**, so dropping the reviews thins the corpus in precisely the direction it is already weakest.

A review carrying a demographic or religious signal is therefore routed to `BOOK_REVIEW_LEAD` — **174** records. It is not evidence and does not go to the screen; the *reviewed work* is what to chase. The remaining 88 carry no signal and drop.

### The leads

- Book review: Nobutaka Fukuda (2016) Marriage and fertility behaviour in Japan - Economic status and value orientation (Springer)
- Modernizing Racial Domination: South Africa's political dynamics by Heribert Adam Berkeley and Los Angeles, University of California Press, 1971. Pp. 
- Ellen Jones and Fred W. Grupp. <i>Modernization, Value Change, and Fertility in the Soviet Union</i>. (Soviet and East European Studies.) New York: Ca
- Modernization, Value Change And Fertility In The Soviet Union. By Ellen Jones and Fred W. Grupp. Soviet and East European Studies. Cambridge, U.K., Lo
- <i>Fertility Differences in a Modernizing Country: A Survey of Lebanese Couples.</i>David Yaukey
- FERTILITY DIFFERENCES IN A MODERNIZING COUNTRY: A SURVEY OF LEBANESE COUPLES. By David Yaukey. Princeton, New Jersey: Princeton University Press, 1961
- DAVID YAUKEY. Fertility Differences in a Modernizing Country: A Survey of Lebanese Couples. Pp. xviii, 204. Prince ton, N. J.: Princeton University Pr
- Book Reviews: Les Chemins de fer Privés des Franches Montagnes. Naissance, Exploitation et défis d'un réseau (1892–1943) [Private Railways of the Fran
- Women's education, autonomy, and reproductive behaviour: experience from developing countries
- BOOK REVIEW: Patrice Diquinzio. MODERN MATERNITY: A REVIEW OF<b>THE IMPOSSIBILITY OF MOTHERHOOD: FEMINISM, INDIVIDUALISM, AND THE PROBLEM OF MOTHERING
- Spiritual marketplace: baby boomers and the remaking of American religion
- After the baby boomers: how twenty- and thirty-somethings are shaping the future of American religion
- Vanishing boundaries: the religion of mainline Protestant baby boomers
- Founding faith: providence, politics, and the birth of religious freedom in America
- The American religious debate over birth control, 1907-1937
- The invention of air: a story of science, faith, revolution, and the birth of America
- A book forged in hell: Spinoza's scandalous treatise and the birth of the secular age
- Religious politics in Turkey: from the birth of the republic to the AKP
- Endowed by our creator: the birth of religious freedom in America
- Early Islam and the birth of capitalism
- The birth of conservative Judaism: Solomon Schechter's disciples and the creation of an American religious movement
- The wise king: a Christian prince, Muslim Spain, and the birth of the Renaissance
- Birth ethics: religious and cultural values in the genesis of life
- Book Review: Review of Fertility and Faith: The Demographic Revolution and the Transformation of World Religions
- A Book Forged In Hell: Spinoza’s Scandalous Treatise and the Birth of the Secular Age
- Religious Politics in Turkey: From the Birth of the Republic to the AKP
- Religious politics in Turkey. From the birth of the republic to the AKP
- The Birth of Modern Belief: Faith and Judgment from the Middle Ages to the Enlightenment
- <i>Birth Control and Catholic Doctrine</i> . Alvah W. Sulloway. Beacon Press, Boston, Mass., 1959. xxiii + 257 pp. $3.95.
- Review of the book by F.B. Batyrgarey “Registers of birth of muslims in the city of Tver”
- Book Review: Will Our Children Have Faith?
- Birth, marriage, and death: ritual, religion, and the life-cycle in Tudor and Stuart England
- <i>Birth Control and Catholic Doctrine</i> . Alvah W. Sulloway. Beacon Press, Boston, Mass., 1959. xxiii + 257 pp. $3.95.
- Book ReviewThe Time Has Come: A Catholic doctor's proposals to end the battle over birth control.
- Sex and Society in Islam: Birth Control before the Nineteenth Century, by Basim F. Musallam. (Cambridge Studies in Islamic Civilization.) Pp. ix + 176
- Christopher Hancock: Robert Morrison and the Birth of Chinese Protestantism. xii, 268 pp. London: T &amp; T Clark, 2008. £19.99. ISBN 978 0567031778.
- The Agonizing Choice: Birth Control, Religion and the Law by Norman St. John-Stevas (Indiana University Press; 340 pp.; $10.00)
- julie crawford. Marvelous Protestantism: Monstrous Births in Post-Reformation England. Pp. x + 270. Baltimore and London: The Johns Hopkins University
- The Birth of the Islamic Reform Movement in Saudi Arabia: Muhammad ibn Abd al-Wahhab (1703/4-1792) and the Beginnings of the Unitarian Empire in Arabi
- The Birth of a Legal Institution: The Formation of the Waqf in Third-Century A.H. Hanafi Legal Discourse, by Peter C. Hennigan. Studies in Islamic Law
- … and 134 more in `postmaterialism-individualism-secularization-prefilter.json`

## What this filter does NOT do

- It does not decide relevance. Everything it keeps still goes to the screen unjudged.
- It does not touch title-only records. The rubric routes those to `UNCERTAIN`, and a record with no title is kept by default.
- Drops are recorded with `prefilter_cell: OFF_OTHER` and the firing term, so the PRISMA count reconciles and any drop can be reversed by name.

