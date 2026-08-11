# D.1.a — chasing the book-review leads to the books

`104_` routed 205 on-pair book reviews to `BOOK_REVIEW_LEAD` rather than deleting them,
on the ground that a review is not evidence but is a retrieval lead. This resolves the leads to the
works they review and asks the only question that matters: **is the book already in the corpus?**

## The leads are mostly false friends

| triage | n | what it is |
|---|---|---|
| `FERTILITY_SIGNAL` | 65 | carries a fertility, natality or family-formation term — chased below |
| `BIRTH_AS_ORIGIN` | 70 | "birth" meaning genesis: *…and the Birth of the Secular Age*, *The Birth of Modern Belief* |
| `NO_SIGNAL` | 70 | religion-history monographs caught on "baby boomers", "secular", bare "values" |

Only **65 of 205** leads are plausibly on-pair. The rescue rule
that created this pile is dominated by a demographic stem doing non-demographic work — the same
defect the prefilter already records for `secular trend`, where 65 of 117 fires were epidemiology.
**The rule earned its keep anyway**: it is what preserved the Jones and Grupp, Yaukey and Fukuda
leads that motivated it. The fix is to triage on the way out, not to narrow the rescue on the way in.

## What the chase found

65 fertility-signal leads collapse to 48 distinct candidate titles, and those
resolve to **46 distinct books** — 2 pairs of differently-cited reviews turned
out to name the same work. Deduping on the citation string is not enough, because one journal prints
the author ahead of the title and another does not; the identity that counts is the resolved record.

| outcome | n |
|---|---|
| resolved to a book record | 10 |
| — of those, already in the corpus | 0 |
| — of those, **missing from the corpus** | **10** |
| probable, year disagrees — needs an eyeball | 3 |
| unresolved (no book record found) | 33 |
| | 46 = 48 candidates − 2 collapsed |

### The books the search missed

| book | author | year | type | match | reviews | owner | OpenAlex |
|---|---|---|---|---|---|---|---|
| Birth Control Battles | Wilde | 2019 | book | RESOLVED_SUBTITLE | 4 | A.3/A.6 contraception | W3048199447 |
| Fertility Differences in a Modernizing Country | Yaukey | 1961 | book | RESOLVED_NOAUTHOR | 3 | D.1.a | W4302865405 |
| Religion and fertility | Chamie | 1981 | book | RESOLVED_NOAUTHOR | 2 | D.1.a | W2798418277 |
| Voicing Voluntary Childlessness: Narratives of Non-Mothering in French | Edwards | 2015 | book | RESOLVED_NOAUTHOR | 2 | D.1.a | W2970453049 |
| Women’s Education, Autonomy, and Reproductive Behaviour: Experience fr | Jejeebhoy | 1995 | book | RESOLVED_NOAUTHOR | 1 | D.2.a gender | W3022314024 |
| Marriage and Fertility Behaviour in Japan | Fukuda | 2016 | book | RESOLVED | 1 | D.1.a | W4252578261 |
| The Material Culture of Sex, Procreation, and Marriage in Premodern Eu | McClanan et al. | 2002 | book | RESOLVED_NOAUTHOR | 1 | D.1.a | W1989637569 |
| Religion and the Decline of Fertility in the Western World | Derosas et al. | 2006 | book | RESOLVED | 1 | D.1.a | W1182906368 |
| ISLAM AND NEW KINSHIP | Clarke | 2009 | book | RESOLVED_SUBTITLE | 1 | D.1.a | W4399625584 |
| Childless: No Choice: The Experience of Involuntary Childlessness | Monach | 1993 | book | RESOLVED | 1 | D.1.a | W567574339 |

### Probable, pending a human look

OpenAlex dates a book by the edition it indexed, not by first publication, so a right book can wear
a reprint year — *Godly Seed* indexed 2017 against a 2012 review, at containment 1.0. These match on
title but not on year, and are a third state rather than a rejection or a claim.

| book | author | review yr | indexed yr | j / c | OpenAlex |
|---|---|---|---|---|---|
| Two is Enough | — | 2019 | 2003 | 0.2 / 1.0 | W4252837795 |
| Godly Seed | Allan | 2012 | 2017 | 0.22 / 1.0 | W4243139168 |
| Fertility and Pleasure | Lindsey | 2007 | 2017 | 0.33 / 1.0 | W2262009069 |

`RESOLVED` carries a matching author and year. **`RESOLVED_NOAUTHOR` matched on title and year
only** — 5 of the resolutions, and a
weaker claim — because 126 of the 205 review titles are a bare book title with no parseable
author, leaving the author gate nothing to test. Those are flagged rather than promoted, since a
silent pass would grade an unverified match exactly like a verified one.

Not every missing book is a D.1.a book. Ownership is assigned from the title: contraception
monographs belong to A.3/A.6 under the rubric's own `OFF_CONTRACEPTIVE_ATTITUDE_A3_A6` cell.
By owner: D.1.a 8, A.3/A.6 contraception 1, D.2.a gender 1.

### Unresolved, and the most important lead is among them

33 candidates returned no book record. Some are review-essays covering four or five books
at once, which have no single title to resolve and are mostly off-pair anyway. But the pile also
contains **Jones and Grupp, *Modernization, Value Change, and Fertility in the Soviet Union*** — the
book that motivated the whole `BOOK_REVIEW_LEAD` rule. Its reviews are indexed; the monograph has no
book-type record in OpenAlex at all, checked by hand. Same for Musallam, *Sex and Society in Islam*
(three separate reviews) and Hoffert, *Private Matters*.

**This is the sixth independent hit on the books/chapters/dissertations indexing gap, and the
sharpest**: for these works the review is not merely the easiest trace in the corpus, it is the only
one that exists in the index. They cannot be retrieved by any query over OpenAlex, at any recall.
They need a library catalogue and a human.

| lead (as cited by its reviewers) | reviews |
|---|---|
| Private Matters: American Attitudes Toward Childbearing and Infant Nurture in the Urban  | 3 |
| Private Matters: American Attitudes toward Childbearing and Infant Nurture in the Urban  | 2 |
| Birth Control and Catholic Doctrine . Alvah W. Sulloway. Beacon Press | 2 |
| Susan E. Klepp . Revolutionary Conceptions: Women, Fertility, and Family Limitation in A | 1 |
| Book Review Private Matters: American attitudes toward childbearing and infant nurture i | 1 |
| sylvia d. hoffert . Private Matters: American Attitudes toward Childbearing and Infant N | 1 |
| A Sociology of Organisations, Political Woman, The Crisis of Industrial Civilization. Th | 1 |
| The American religious debate over birth control, 1907-1937 | 1 |
| Studies in Sociology, Race Mixture, Hunger and Work in a Savage Tribe, Interpretations,  | 1 |
| Sociological Theory in Transition, The Category of Person, Social Relations and Spatial  | 1 |

## What this does not settle

Resolution says a book record exists and is absent from the corpus. It does not say the book reports
an extractable estimate — most monographs of this vintage do not, and several will be narrative. The
10 rows are a **retrieval queue for the RA, not an inclusion list**, and they enter the
chapter's PRISMA flow as records identified through other sources.
