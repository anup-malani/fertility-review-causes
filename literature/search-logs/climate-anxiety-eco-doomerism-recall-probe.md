# A6c production query + recall probe - climate-anxiety-eco-doomerism

Production query refit on full gold at CV breadth Nf=3, Np=30. Local recall is budget-free (compiled query against gold's cached title, then title+abstract); universe counts are one cheap OpenAlex request each.

Gold = 78 empirical records (10 Tier-A seeds, 68 screen-relevant empirical). Theory is excluded by design and does not count toward recall. **Caveat on the abstract row:** only 64 of 78 gold records carry a cached abstract, so the title+abstract line understates what a live abstract-indexed search would reach.

## Local recall - how much does abstract matching rescue?

| basis | overall | Recall(A) | Recall(B) | rare value-added core | realized fertility |
|---|---|---|---|---|---|
| title only | 65.4% | 80.0% | 63.2% | 57% (8/14) | 75% (6/8) |
| **title + abstract** | **85.9%** | 80.0% | 86.8% | 79% (11/14) | 100% (8/8) |

Abstract matching lifts overall recall 65% to **86%**, the rare value-added core 57% to **79%**, and realized-fertility recall 75% to **100%**.

## Live universe counts - the budget cost of abstract matching

| operationalization | universe (meta.count) |
|---|---|
| `title.search` | 27,543 |
| `title_and_abstract.search` | 712,579 |

## The fork (data-driven)

- `title.search`: faithful to the title-only CV; smaller universe; caps recall at the title-only number.
- `title_and_abstract.search`: recovers the abstract-only gold, at the cost of a larger universe, because the broad cause-side singles (climate, concern, crisis, environment) match across abstracts far more loosely than across titles.
- D.3.b-specific: the effect block carries `fertility`, which A6a found to be a NEGATIVE discriminator inside this frame. It is kept for scope-definitional reasons, but it is the main reason the universe inflates, since climate-and-fertility papers of the physical-exposure kind are exactly what it retrieves. If the universe is unmanageable, the first tightening to try is phrase-restricting the effect block rather than the cause block.

## Query (cleaned Boolean)

    (fertility OR fertilit OR birth OR childbearing OR childbear OR childless OR childfree OR "child free" OR "number of children" OR offspring OR "family size" OR reproductive OR reproduction OR reproducti OR procreat OR natality OR parity OR "have children" OR "having children" OR "fertility intention" OR "reproductive intention" OR "childbearing intention" OR "pregnancy intention" OR "remain childless" OR "voluntary childless" OR intentions) AND ("climate anxiety" OR "eco anxiety" OR "climate distress" OR "climate worry" OR "climate worries" OR "climate concern" OR "climate grief" OR "climate emotion" OR solastalgia OR "eco distress" OR "ecological grief" OR "eco doom" OR doomism OR "eco pessimis" OR "climate pessimis" OR "climate despair" OR "climate dread" OR "climate doom" OR apocalyp OR collapse OR "carbon footprint" OR "carbon legacy" OR antinatalis OR "anti natalis" OR "environmental antinatalis" OR "procreative ethic" OR "population ethic" OR overpopulation OR habitabilit OR "bring a child into" OR "world to bring" OR "future for children" OR "climate future" OR planetary OR "climate change" OR "global warming" OR "climate crisis" OR "ecological crisis" OR "environmental crisis" OR concerns OR climate OR anxiety OR "environmental concerns" OR worries OR concern OR crisis OR "decision making" OR eco OR "change anxiety" OR environmental OR "change concern" OR "age climate" OR "change concerns" OR "choices climate" OR "change worries" OR worried OR "worried environment" OR "era climate" OR "futures climate" OR existential OR "concerns deterring" OR environmentalism OR "environmental concern" OR environment OR attitudes)
