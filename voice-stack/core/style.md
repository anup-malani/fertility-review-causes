---
name: Writing and document formatting standards
purpose: Full specification of writing voice/structure/craft (Memo Mode + Academic Mode with field sub-modes), file versioning rules, and python-docx formatting conventions. Read on-demand when producing a written artifact (memo, analysis draft, research summary, briefing material, .docx export). Not auto-loaded; pointed to from ~/.claude/CLAUDE.md.
voice_derivation: Academic Mode voice sections derived from 28 published Malani papers (12 sole + 8 first-author + 8 expansion, tier A/A2/B) via multi-factor weighted aggregation (role × coauthor × recency × genre × venue × length). Memo Mode derived from the authentic pre-AI CMS memos (Dec 2025–Feb 2026, hand-written-from-scratch), weighted to the fall data-liquidity report and the early-2026 briefings; it replaces the prior generic Memo Mode. Social Mode (Essay) derived from the mature Substack essays (2022+); Social Mode (Explainer) from the law-and-economics teaching series. Methodology, per-field rollups, and the exemplar banks live in ~/UChicago Law Dropbox/Anup Malani/assistants/research-manager/projects/style-analysis/ and ~/.claude/refs/exemplars/. Register em-dash / rhetorical-question caps live in ~/.claude/refs/voice-registry.md.
last_updated: 2026-07-26
---

# Writing Standards

These standards apply to all written work. Four register Modes are derived from Anup Malani's own corpus, each paired with an exemplar bank in the voice registry (`~/.claude/refs/voice-registry.md`):

- **Memo Mode** — the direct, decision-first register of his CMS policy memos, derived from the hand-written pre-AI memos of December 2025 through February 2026.
- **Academic Mode** (General, with Law, Economics, and Biomedicine sub-modes) — the empirical, first-person scholarly voice derived from ~28 published papers.
- **Social Mode (Essay)** — the essayistic, argument-driven register of his Substack posts on slums, development, caste, and population.
- **Social Mode (Explainer)** — the pedagogical register of his law-and-economics teaching series, which builds a concept from primitives.

The project CLAUDE.md or the voice router picks the Mode. When unspecified, Memo Mode is the default for short-form policy work and Academic Mode for papers and research summaries. Each Mode below describes the voice as it appears in the corpus rather than prescribing rules, and reports the quantitative targets the corpus supports. The register-sensitive caps on em-dashes and rhetorical questions live in the voice registry; Layer 0 (`~/.claude/refs/ai-tells.md`) is the negative screen that sits above every Mode.

---

## Memo Mode

The memo voice is an economist writing to decision-makers. It states the verdict or the governing constraint early, reduces a messy policy question to a few economic variables or an efficacy-ranked set of options, walks one clean mechanism for one claim at a time, and closes by bounding what the agency can do on its own authority against what needs Congress. It reasons in economic categories (incidence, incentives, selection, marginal return, the counterfactual) rather than in political ones. The register sits close to his academic voice, compressed and pointed for a reader who is intelligent and pressed for time. The organizing principle is **brutal clarity**: that reader has forty memos to get through and will not re-read a sentence, so every move below exists to buy her comprehension at the lowest possible cost, and persuasion rides on it. The pre-send checklist at the end of this Mode makes the principle concrete. What follows describes that voice as it appears in the hand-written pre-AI memos of December 2025 through February 2026, not a set of prescriptions. The universal structure habits (lead with the finding, topic-sentence-first, one idea per paragraph) are Layer 1 in `~/.claude/refs/appellate-style.md`; the negative screen is `~/.claude/refs/ai-tells.md`. Both sit above this Mode.

**In one line — a memo is an appellate brief's skeleton in an economist's voice.** Take the structural discipline of a first-rate brief (the pre-send checklist below) and nothing else from it: the register stays yours — first person, reasoning in incidence and incentives, and, unlike a brief, qualifying your own recommendation in the next sentence. Borrow the skeleton, keep the voice.

### Opening moves

A memo answers the ask in its first sentence. The commonest opener names the commission and states the finding in the same breath: `You asked me to examine the value of SDOH interventions ... Only three ... show credible evidence of cost-neutrality`. The recommendation follows immediately, with its qualification attached rather than deferred: `I recommend selective pilots with strict evaluation and program integrity controls, not broad expansion`. When the memo is a problem statement rather than a briefing, it states the goal and then partitions the failure into named effects before any analysis: `Its provisions, however, had two counterproductive effects. One is adverse selection ... The other is higher insurance costs`. There is no throat-clearing overview paragraph; the verdict or the partition is the opening.

### Argument structure

The memo organizes options by economic efficacy and then trades that ranking against political feasibility: `The most efficient solution is often the least politically feasible. Second- and third-best solutions ... account for political feasibility`. Tradeoff analysis is done in prose as a two-by-two, each option carried with its own weakness (`solves the problem prospectively but does nothing about the existing gap`), then synthesized into a sequence in which each mechanism covers the other's gap. Evidence is marshaled one claim at a time, and the magnitude arrives after the mechanism that produces it, not before. Headings signal structure but stay shallow, usually two levels. A recurring scaffold is the binary partition announced early (`two counterproductive effects`, `it does two things`) and reused through the rest of the memo, including the close.

### Register and first-person

First-person is lighter than in his sole-authored papers (around 4 per 1,000 words) but load-bearing where it appears: the briefing voice uses `You asked me ...`, `I recommend ...`, `My read is ...`. The stance is direct and assertive; the memo states its position and owns the recommendation. It voices the reader's likely objection and answers it in the same paragraph. The tone is confident without false confidence, and it does not perform certainty it does not have.

### Hedging and uncertainty

Hedging runs lighter than in the academic voice (around 10 per 1,000 words) because the reader needs a decision, and the qualification travels with the claim rather than sitting in a separate limitations section. The signature move is to make the recommendation and qualify it against its own side effect in the next sentence: `price negotiation should be careful not to cut R&D ... A price cut that is too aggressive saves money now but risks discouraging the next treatment`. Uncertainty is expressed as a bounded magnitude (`roughly 25 percent`, `4 to 6 percent of filings`) rather than as a hedge on the whole claim.

### Examples and abstraction

The memo reasons like an economist with one worked example per claim. It walks a mechanism to its conclusion with a single concrete number (community-rating instability shown with a 5x cost against a 3x cap). It re-describes a policy as an economic object (EMTALA plus consumer bankruptcy law as an implicit zero-interest loan to the uninsured, then follows the equilibrium the two create). It defeats a bad inference with a homemade analogy the reader can run without help (`that a filer also has medical bills does not mean those bills caused the filing, any more than owning a car causes bankruptcy`). Pure abstraction without an anchoring case is rare, exactly as in the academic voice.

### Sentence rhythm and prose

Target ranges from the authentic memos:

- Mean sentence length ~19 words, but within-document standard deviation ~17, higher than the academic corpus, because the memo mixes very short verdict sentences (`Neither mechanism alone is sufficient.`) with long mechanism sentences. Tenth percentile ~5 words; ninetieth ~33.
- Paragraphs ~3 sentences, tighter than the academic ~4.
- Numbers are integrated into prose and given context (a percentage gets its base rate, a change gets its starting point); they are not stranded in tables the reader must decode alone. Prose carries the argument; bullets are reserved for true lists.

**Em-dashes.** He uses the em-dash as an appositive or definitional pair (`the individual market, where the MOOP actually binds, is a small fraction of the denominator`), never as a dramatic pause. His drafting target in a memo is low, about 1 per 1,000 words, the same low rate as his academic writing. The current memo corpus runs far hotter (≈7–9 per 1,000, higher still in options and briefing memos), but that corpus is not a clean measure of his hand: every memo in it is dated December 2025 or later, which postdates his adoption of AI-assisted drafting, so the high rate is most likely AI inflation rather than his voice. A genuinely pre-AI memo sample has not yet been gathered (he wrote memos from his first week and earlier ones exist on his work laptop; dating them is a pending step). Until then, draft memos at the ~1 per 1,000 target, not the corpus rate. Output is a separate stage: the `.docx` format spec below bans the em-dash glyph, so at export the appositive construction is preserved but the glyph is rendered as `--` or `---`. Convert the glyph, do not strip the appositive.

### Signature moves

- **Recommendation-first opener.** Name the commission, state the finding in one sentence, give the recommendation with its qualification attached.
- **The crisp two-part partition.** `One is ... The other is ...`; `it does two things. First ... Second ...`.
- **Two-by-two in prose, then a sequenced synthesis.** Each option carried with its weakness, then ordered so each covers the other's gap.
- **Mechanism first, number last.** Argue the claim from a payment structure or an incentive, then state the magnitude.
- **Coin and define the terms the memo needs.** `By history, I mean ... By counterfactual, I mean ...`, then reuse them.
- **Re-describe a policy as an economic object.** A statute becomes an implicit loan, a subsidy formula becomes a perverse incentive.
- **Bounded close.** Name what regulation can do on its own authority, what needs Congress, and the venue for the fix.

### Brutal clarity — the pre-send checklist

The reader will not work to understand you. The worst thing a memo can do is make her stop and re-read a sentence. Before sending, run the memo against these eight checks. Each is a technique elite appellate/SG briefs use systematically (`~/.claude/refs/exemplars/appellate.md`, T1–T8); the memo-bank entry that already shows it, or the gap to push on, is noted.

1. **Topic sentences carry the argument.** Read only the headings and the first sentence of each paragraph. Do they, alone, tell the whole story? They must — this is the master check, and the paragon is **appellate T1** (Clement's Heller SG Summary of Argument: six paragraph-openers that, read alone, give the entire brief). You do this at your best — the ACA-reform memo's `###` headings are full assertive claims ("The ACA's regulation of insurance caused adverse selection that swapped uninsured high-risk enrollees for uninsured low-risk, young enrollees…") — but not consistently: other memos fall back on label headings ("Background," "Recommendations") that carry no argument. Make the assertive version the rule, and hold every heading and paragraph opener to the bar in appellate T1. *(Strongest lever. No memo-native specimen is this clean, so the bank points up to appellate T1 rather than mine a weaker one — the technique is register-neutral, so nothing is lost.)*
2. **Answer first (BLUF).** The finding or recommendation is in sentence one, its qualification attached, not deferred to a conclusion. *(memo.md CORE 1.)*
3. **Frame so your answer is the natural one.** Partition the problem into named effects up front, and reuse the partition through the memo and its close. *(CORE 2, EXT 9.)*
4. **One concrete anchor per claim.** At least one claim rides on a worked number, a re-described economic object, or a homemade analogy the reader can run without help — not pure abstraction. For a non-economist principal, consider *opening* on a concrete case rather than a mechanism. *(CORE 4, EXT 6, EXT 8; opening-on-a-case is the gap.)*
5. **Cabin the claim.** Say what you are *not* recommending before you press what you are. *(CORE 1, EXT 11, EXT 15.)*
6. **Steelman, then answer.** Voice the reader's strongest objection at full strength, in the same paragraph you answer it. *(EXT 8.)*
7. **Land the key point on a short, flat sentence.** After a long mechanism sentence, make the takeaway short enough to be unmisreadable ("Neither mechanism alone is sufficient."). *(CORE 3 rhythm; underused — push it.)*
8. **No sentence she must decode.** Bind every "this / it / they" to one nearby noun, keep the subject near the front, and don't stack clauses that have to be re-parsed. If a sentence needs a second read, recast it. *(This is `ai-tells.md` on ambiguous antecedents, applied as a clarity rule.)*

Item 1 is the master check; 2–8 are ways to buy the reader's comprehension cheaply. The same principle governs `appellate.md`, whose header states it in full.

---

## Academic Mode (General)

The academic voice is empirical, first-person, and argumentatively self-conscious. It tolerates long complex sentences and heavy footnotes, reads as a working scholar thinking out loud rather than pronouncing from above, and stakes clear positions while flagging what is unknown. What follows describes that voice as it appears in Malani's published work, not a list of prescriptions.

**Brutal clarity governs this register too** (Layer 1, `~/.claude/refs/appellate-style.md`). A reader who reads only the abstract's topic sentences and each section's roadmap restatement should already have the paper's argument. State the claim before the model or the citation that supports it, and define a coined term in the sentence where it first appears, not a paragraph later.

### Opening moves

Abstracts and introductions open with context roughly three times as often as with a direct claim (context opens 15 of 28 abstracts; claim opens 3). The characteristic move is to sketch the policy or empirical landscape in one or two sentences, then locate the paper within it. Representative openers:

- `Universal health coverage is a widely shared goal across lower-income countries.`
- `A growing scientific literature supports the existence of placebo effects from a wide range of health interventions and for a range of medical conditions.`
- `The conventional approach to evaluating a law is to examine its effect on proximate behavior.`

Introductions occasionally open instead with a historical hook (Tumbe on pandemics; Epstein on Clinton-era health reform) or a stylized fact with a specific number. Conclusions almost always restate the thesis first — summary before implications — and avoid rhetorical flourish.

### Argument structure

The dominant section pattern is numbered-theory-then-empirics (law and economics pieces lean on `law-review-parts` structure; biomedical venues impose IMRaD). Across modes, the paper announces what each section will do in a roadmap paragraph at the end of the introduction, then opens each section by restating that function. Empirical results are introduced claim-then-caveat more than any other way (9 of 28 papers); magnitude-then-significance is the next most common (5 of 28). Tables are discussed in prose immediately after being named; figures rarely stand alone.

A recurring structural tic is to announce a binary taxonomy (`two buckets`, `ex post vs. ex ante`, `direct vs. spillover effect`, `first-best vs. second-best`) early and then use it as a scaffold for the rest of the paper, including in the empirics and conclusion.

### Register and first-person

First-person is frequent in 14 of 28 papers, occasional in 5 more, and suppressed only where venue demands it. Sole-authored papers use `I` to stake positions (`I suspect`, `I conjecture`, `I argue`, `I focus on`, `I examine each in turn`); coauthored papers use `we find`, `we estimate`, `we propose`, `we contribute`. First-person is not a rhetorical flourish — it marks the moves where the author is choosing a side. It coexists with formal register elsewhere in the same sentence, and it is not avoided in methodological passages.

The overall tone is confident but explicitly fair. Generous concessions (`To be clear`, `That said`, `we stress, however`) appear alongside strong first-person claims. The writer voices the reader's likely objection and then answers it in the same paragraph.

### Hedging and uncertainty

Hedging runs around 13 per 1000 words. Caveats are placed close to the claim they modify, not deferred to a limitations section. The signature hedges are:

- `likely` (9 papers), `may` (8), `perhaps` (7)
- `it is possible that` (5)
- `I suspect` (4 papers, sole-authored)
- `we suspect`, `we cannot rule out`, `candidly`, `it may be too early to tell` (later working papers)

Uncertainty is often expressed through bounds rather than point estimates (`upper bound`, `lower bound`, `between X and Y percent`). A recurring pattern is to name a weakness of the author's own measure and then show the competing measure has the same weakness — symmetric critique rather than concession. Limitations are enumerated as numbered lists and each one is typically paired with a partial rebuttal; the paper never just concedes.

### Footnotes

Footnotes are heavy (10 of 28 papers) or moderate (6 more), and carry analytical load rather than mere citation. The predominant function mix is "citational plus digressive substantive asides" — footnotes contain mini-arguments, numerical worked examples, technical qualifications, model extensions, and cross-references to the author's own prior work. The main text is kept narrative by moving secondary objections, alternative specifications, and side critiques into footnotes, which often run several sentences each.

Citation format tracks venue. Economics papers use author-year inline; law review articles use Bluebook footnotes with `see, e.g.,` signals; biomedical venues use numbered superscripts.

### Examples and abstraction

The balance between example and abstraction is explicitly balanced in 15 of 28 papers and abstract-heavy in 3. Abstract claims are almost always re-glossed with a concrete example, and the pivot is telegraphed with `for example`, `to illustrate`, `consider`, or `suppose that`. Examples come in four varieties: extended hypotheticals (the charity founder for sick children in Africa; the pharmacist with specific dollar figures); stylized two-party thought experiments (State One and State Two; D1 and D2); real-case facts reused across a paper (RAND experiment; Georgine-period bankruptcy pause); and historical anecdotes used to calibrate stakes (1918 flu, McDonald's coffee case). Pure abstraction without an anchoring example is rare.

### Sentence rhythm and prose

Target ranges from the corpus:

- Mean sentence length ~21 words; within-document standard deviation ~13, so long complex sentences are expected alongside short ones. Tenth percentile ~7 words; ninetieth percentile ~36.
- Paragraph length ~4 sentences on average.
- Passive ratio ~15%. The passive appears roughly one sentence in seven, typically where agency is obvious from context or where the grammatical subject is the empirical result rather than an actor.
- Nominalization ~41 per 1000 words. The voice tolerates technical nominalizations (`selection bias`, `subject supply effect`, `non-distribution constraint`) where they are terms of art.

Recurring sentence-opener bigrams at the top of the distribution: `this is`, `for example`, `it is`, `if the`, `the reason`, `there are`, `in this`, `the first`, `in other [words]`, `we find`, `we estimate`, `first we`, `however the`. These are soft patterns, not formulas — they mark the connective tissue of an argument that moves by restatement, enumeration, and causal unpacking.

### Signature moves

- **Re-glossing.** A technical sentence is followed by `In other words,` or `that is,` and a plainer restatement. The move is pedagogical, used to make formal results available to readers outside the originating field. Appears in 9 of 28 papers as an explicit connective, and implicitly in more.
- **Enumerated causal unpacking.** `The reason is that ...` (3 papers) followed by one-sentence mechanism statements; or `For one thing, ... For another, ...`; or numbered first / second / third. Arguments advance by enumeration more often than by building a single sweeping paragraph.
- **Stage the debate.** `On one side of the debate ... On the other side of the debate ...`; `On the one hand ... On the other hand ...`. The author's position is introduced only after both sides have been fairly stated.
- **Name and reuse a coined term.** Most papers define a central construct (`subject supply effect`, `option value of the drug`, `EFR-compensatory change`, `coupling`, `veil of ignorance`, `adaptive control`, `placebo instructions`) and then use it systematically, including in section headings. Terms are often defined mid-paragraph with `We call this ...` or `We label ...`.
- **Pre-empt and rebut.** `One might argue ...`, `A possible objection to our argument is ...`, `one might worry` — each followed by the rebuttal in the same paragraph rather than a later section.
- **Enumerated open questions at close.** Conclusions often list what was not resolved and what future research should test, rather than declaring victory. `Fertile ground for future research` and `We leave these questions for future research` are recurring closers.
- **At first blush.** A minor but distinctive tic from early sole-authored work (`at first blush`, `at first glance`) marks a move where the author introduces the naive view in order to dismantle it.

---

## Academic Mode (Law)

**Brutal clarity holds in the legal register too** (Layer 1). The best law review articles can be read from their Part-opening sentences alone, so state the rule or the holding before the doctrine and the economics that support it, and gloss a term of art in the sentence that coins it, not a footnote two pages on.

When writing for a law review or in a legal register, three things change.

**Footnotes carry more weight.** Footnote density is heavy in all five law-review papers in the corpus, and the function mix shifts toward substantive digression. Footnotes routinely hold extended methodological critique, cross-references to the author's own prior empirical work, constitutional caveats, and full alternative arguments. The main text stays readable by pushing technical economics (equations, proofs, parameter restrictions) into footnotes with a Topkis or Hansmann cite.

**Bluebook, not author-year.** Citation format is Bluebook throughout, with superscript footnote numbers inline and `see, e.g.,` and `see supra` as the dominant signals. `Journal of ...` and `working paper` as opener bigrams appear because cross-discipline citations are included in the same footnote apparatus.

**Law-review parts.** Section structure follows numbered Parts and Subparts (I, II, III; I.A, I.B), with explicit cross-references like `as I explained in Part II.A`. The 2008 *Duke Law Journal* and *Harvard Law Review* pieces are the cleanest examples.

**Economics smuggled in.** The distinctive legal move is to translate doctrine into microeconomic categories — revenues, fixed costs, marginal costs, deterrence, overdeterrence, first-order effects — and then adjudicate among competing legal interpretations on economic grounds. Stylized hypotheticals (`State One` and `State Two`; specific dollar figures in pharmacist cases) are used to show that one rule creates perverse incentives and another does not. `So long as X, then Y` conditional claims make proposals robust to parameter uncertainty. Counterintuitive proposals are flagged as such (`at first blush`, `counterintuitive`) and then disarmed.

First-person `I` is heavy in sole-authored law work; coauthored pieces use `we`. Conspicuous fairness (`To be clear`, `That said`, `I stress, however`) is more pronounced here than in economics writing.

---

## Academic Mode (Economics)

**Brutal clarity applies at the same grain here** (Layer 1). Read only the abstract's topic sentences and the introduction's roadmap, and the reader should already have the whole paper. State the finding before the model that derives it, and coin a technical label in the sentence where it is minted, not several paragraphs into the section that uses it.

When writing for an economics journal, NBER working paper, or handbook chapter, the shifts are:

**Theory before empirics.** Section structure follows numbered-theory-then-empirics in 8 of 19 economics papers. The paper typically (1) states the puzzle or contribution, (2) develops a formal model, (3) derives testable predictions, (4) presents empirics against those predictions, (5) discusses policy. Citations are author-year inline (Lakdawalla and Philipson 1998), not Bluebook.

**Magnitude first.** Empirical results are introduced magnitude-then-significance more often than in other venues. A result is stated as a percent or dollar figure, often to two decimals, before any interpretive commentary. Parenthetical (= 0.61, p<0.01) inline reporting is routine. NBER working-paper conventions — preferred specification named up front, robustness checks enumerated in a single sentence, standard errors clustered — are followed.

**Equations are glossed in prose.** Equation density is moderate to heavy in most economics papers but light or absent in a minority. Where equations appear, each is preceded by a verbal statement of the intuition and followed by term-by-term unpacking. Formalism is never load-bearing on its own.

**Coin and reuse.** Economics papers especially rely on coining a crisp technical label (`subject supply effect`, `ex post effect`, `option value`, `dimensionality problem`) and then applying it systematically as a lens. Section headings often use the coined term.

**First-person plural.** `We find`, `we estimate`, `we propose`, `we contribute`, `our preferred specification` are the workhorse phrases. `We do not endorse any particular parameterization` is a characteristic refusal to overclaim.

**Policy framing.** Conclusions typically pivot to policy implications and a short research agenda, rather than closing with a summary alone.

---

## Academic Mode (Biomedicine)

Biomedical venues impose heavy house style, and the corpus shows it. IMRaD section structure, Vancouver/JAMA-style numbered superscript citations, short structured abstracts (context-puzzle openers dominate), and passive-voice expectations all compress the voice described in Academic Mode (General).

**Brutal clarity maps directly onto the structured abstract** (Layer 1), which is itself a forced topic-sentence discipline. Carry that discipline into the body: the first sentence of each Results paragraph should state the finding, not the assay that produced it.

Specific shifts to expect:

- **Passive ratio rises to ~21%** (versus ~15% across the full corpus), driven by Methods and Results conventions.
- **First-person use is muted.** Frequent in only 1 of 4 biomedical papers; the JAMA letter suppresses it entirely. `We` survives in preprints; journal articles trend toward impersonal construction.
- **Footnotes thin out.** Density is moderate, light, or absent. Analytical load that would go into a footnote in a law review must either move to the main text or drop.
- **Statistical definitions in plain English.** Numerator/denominator prose substitutes for notation even where formulas would be standard.
- **IMRaD scaffolding.** Methods and Results sub-headings mirror each other so findings and their methodological basis pair visually.

The voice described in Academic Mode (General) — first-person staking of positions, heavy analytical footnotes, re-glossing via `in other words`, staged debates — does not survive translation into a biomedical journal without modification. The working practice in the corpus is to write the argument first in the general academic voice (preprints on medRxiv show this), then translate to venue house style for journal submission. When drafting for a biomedical journal, expect the translation step to strip roughly half the voice markers described above. The policy-implications closing register (`These communities may require extra attention and support in infection control policies`) and the enumerated-limitations-with-rebuttals structure tend to survive; first-person stance-taking and digressive footnotes usually do not.

---

## Protocol for journal-specific work

When drafting for a specific target journal:

1. Look up the journal's submission guidelines (abstract length and structure, section structure, citation style, word limit, figure/table conventions).
2. Identify one or two recent representative papers in that journal (not by Malani) to check typical register.
3. Compose using the applicable field mode above, then adapt to journal conventions, flagging any place where a house-style requirement conflicts with a voice marker that ordinarily carries argumentative weight.

---

## Social Mode (Essay)

The essay voice is first-person, argument-driven writing for a general audience, the register of his Substack posts on slums, development, caste, and population. Its signature move is to re-anchor the reader's wrong default comparison: name the intuitive frame the reader already holds, then swap in the comparison that actually governs the answer. Around that move the voice grounds every abstraction in something concrete and usually personal, leads with the claim and unpacks it cause by cause, and closes plainly rather than on a flourish. The north star is the dinner-table test: a sentence he would say to a smart non-expert across a table. What follows describes the voice as it appears in the mature posts (2022 onward), not a set of prescriptions.

**Brutal clarity governs the essay register as much as the memo** (Layer 1, `~/.claude/refs/appellate-style.md`). One idea per paragraph, its point stated in the first line, so a reader skimming only first sentences gets the argument's shape before the re-anchoring move even lands. Put the concrete image first and let the abstraction follow.

### Opening moves

Essays open on a concrete, usually personal scene and end the opening on a forward hook. The archetypal opener names real people and admits his own view was overturned: `A few months ago I was listening to a podcast with the wonderful Alain Bertaud ... That podcast upended the way I viewed slums, a topic I have been researching for nearly 8 years`. A quieter variant is reading-driven: he read something, got surprised, and checked it against his own fieldwork (`I was reading Oscar Lewis's ... This surprised me`). The opening drops the reader into the scene that provoked the question rather than announcing a thesis.

### Argument structure

The spine of an essay is the re-anchoring move. He states the intuitive-but-wrong frame in the reader's own voice (`they imagine themselves living in slums`; `we worry about recessions`), supplies the comparison that actually applies (the village, not the apartment; 200,000 years, not this decade), then lands the consequence plainly (`They voted for urban slums with their feet`). He leads with the claim and unpacks it one cause at a time. He concedes and reverses his own prior in the middle of the argument when the evidence pushes him. Paragraphs build to a concrete case rather than to a summary.

### Register and first-person

First-person is frequent (around 15 per 1,000 words) and personal rather than methodological: `I have come to realize`, `one of my favorite podcasts`, `my reasonably well-off neighborhood (Wicker Park)`. The tone carries dry wit that usually lands on a concrete image, such as the abandoned Wicker Park mansion at the end of a list of counterexamples. He addresses the reader directly at the turns and is willing to say plainly that a common view, sometimes his own, is wrong.

### Hedging and uncertainty

Hedging runs around 14 per 1,000 words, close to the academic rate, but the essay register spends it differently. It flags where his own understanding shifted (`I have come to realize`, `at first blush`) rather than qualifying every claim. Numbers are used to re-scale a familiar worry (2 percent growth doubling income every 36 years; all but the last second of human history involving no growth). The uncertainty that matters is the reader's mistaken frame, and the essay's work is to correct it.

### Examples and abstraction

Every abstraction is grounded in something concrete, checkable, and often personal: a podcast that upended his view, running surveys in hundreds of villages, the Google Earth timeline the reader can walk for themselves. Examples build by accumulation to a memorable one, as when counterexamples to a bad slum definition end on the boarded-up mansion. Historical cases calibrate the stakes (the postwar US; Greg Clark on the year 1800). Pure abstraction without an anchoring scene is rare.

### Sentence rhythm and prose

Target ranges from the mature essays:

- Mean sentence length ~19 words, within-document standard deviation ~13. Tenth percentile ~6 words; ninetieth ~34.
- Paragraphs ~3 sentences.
- First-person ~15 per 1,000 words, the connective tissue of the register.
- The em-dash is authentic here (~3.9 per 1,000 words on the clean AI-free Substack measurement, his hottest register and the ceiling for any of his writing), as is the occasional rhetorical question (~2.7 per 1,000 words). Both are capped, not banned, in the voice registry; do not open successive paragraphs with questions or stack them. The prose is plain and specific, and the plainness is the craft.

### Signature moves

- **Re-anchor the wrong comparison.** Name the reader's intuitive frame, swap in the comparison that governs the answer, land the consequence plainly.
- **Ground in a personal scene.** Open on a real, usually first-person moment, and return to concrete images at the turns.
- **Admit the reversal.** Say that a view, often his own, was wrong, and show what changed it.
- **Close on a concrete case.** The postwar US, the village, the mansion, rather than a summary paragraph.
- **Dry wit on the landing.** Humor arrives through a concrete image, never as performed cleverness.

---

## Social Mode (Explainer)

The explainer voice is the pedagogical register of his law-and-economics teaching series. It builds a concept from primitives for a beginner: start from one atom, add one checkable step at a time, and name the concept only after the reader has already felt it. It addresses "you" and uses the reader's own life as the worked example, grounds every abstraction in something concrete, sources authority by name, and lets itself marvel at the ordinary machine. Its arc is define, then derive, then worked example. The dinner-table test governs here too. What follows describes the voice as it appears in the teaching posts, not a set of prescriptions.

**Brutal clarity means each step states its takeaway before its derivation** (Layer 1). Name what the reader gets from the step in its opening sentence, then walk the primitives that get her there. A reader skimming only those opening lines, step to step, should be able to follow the whole build before any concept is named.

### Opening moves

An explainer opens on the primitive it will build from and states it in a sentence a non-expert can follow: `Scarcity is central to economics. To 'economize' is to make the best use of limited resources`. A counterfactual often makes the primitive land (`If there were bountiful resources, predicting human behavior would be simple`). Sections frequently pivot on a genuine question the paragraph then answers (`Why do we care whether goods are excludable or rivalrous?`). The opening states the atom rather than a thesis.

### Argument structure

The arc is define, derive, worked example. He builds an abstraction out of a concrete producer or consumer and reasons one step at a time until the concept falls out and is named (`This generates what is called an individual firm's supply curve`). A common variant is numeric iteration: he walks concrete values until the mechanism settles (`arbitrarily pick a price, say 3 ... the price will adjust until it equates supply and demand, which happens at a price of 5`). The concept is named last, after the reader has felt it. The same primitive-by-primitive method serves both why a machine works and why it breaks, as when excludability leads to payment, then revenue, then profit, then undersupply.

### Register and first-person

First-person is the highest of any register (around 21 per 1,000 words), and it is inclusive and warm: `we all take prices for granted`, `I have a dog; his name is Clark`. He addresses "you" throughout and uses the reader's own day as the material (`You have 24 hours in a day ... your friends suggest going to a bar til 2am`). Authority is sourced by name rather than as "experts say": `as Tyler Cowen says, never underestimate supply elasticity`.

### Hedging and uncertainty

Hedging is modest (around 14 per 1,000 words) and mostly takes the form of qualifiers on scope (`Usually opportunity costs refer to costs denominated in time, but are general enough to encompass ...`). The teaching voice is confident about the mechanism because it has just built it in front of the reader. Where a claim has a limit, the limit is stated as a further worked case rather than as a caveat.

### Examples and abstraction

This is the most example-dense register. Every concept is grounded in a concrete, checkable case: a bakery's cakes, a carton of eggs, a $150 concert ticket, a 24-hour day, his dog Clark, and 5G and solar as datable proof of supply elasticity. The reader's own life is the default worked example. Abstractions are never left un-glossed; the concept name arrives attached to the case that produced it.

### Sentence rhythm and prose

Target ranges from the teaching posts:

- Mean sentence length ~20 words, within-document standard deviation ~12. Paragraphs ~4 sentences, slightly longer than the essay register because a derivation runs across several steps.
- Nominalization is lower than in the essay or academic registers (~29 per 1,000 words); the teaching voice prefers plain verbs to abstract nouns.
- The em-dash is used sparingly (~1.4 per 1,000 words, the lowest of the social registers), while genuine section-pivot questions are frequent (~4 per 1,000 words) and authentic. Both are capped, not banned, in the voice registry, under the same no-stacking rule. He lets himself marvel (`prices are ... somewhat magical`), with an exclamation for real delight.

### Signature moves

- **Build from the primitive.** Start from one atom and add one checkable step at a time.
- **Name the concept last.** Let the reader feel it before you label it.
- **Address "you," use the reader's day.** The 24-hour budget, the concert ticket, the bar at 2am.
- **Ground every abstraction in a concrete case.** The bakery, the eggs, the dog.
- **Source authority by name.** Attribute a takeaway to a named person (Tyler Cowen), never to anonymous "experts."
- **Marvel at the ordinary machine.** Convey why a price, a court, or a market is remarkable.

---

For sentence-level craft polish on long-form academic or memo prose during a revision pass, see `~/.claude/refs/appellate-style.md`.

## Formatting

- **One font size, one weight distinction.** Reserve size changes for unavoidable hierarchy; bold versus plain usually suffices.
- Use whitespace to aid comprehension, not to pad length
- Tables for structured comparisons; figures for trends and distributions
- Label figures and tables clearly; they should be interpretable without the surrounding text
- Keep formatting minimal and consistent

## File Versioning

When revising a document based on user feedback, never edit the file in place. Instead:

1. Rename the current file to include a version suffix (e.g., `v1`) if it doesn't already have one.
2. Save the revised version as the next version (e.g., `v2`).
3. If the user provided an annotated copy (e.g., with `-AM` suffix), rename it to include the version it annotates (e.g., `v1-AM`).

This preserves the full revision history in the filesystem. Version suffixes go at the end of the filename before the extension: `memo v1.md`, `memo v2.md`, `memo v1-AM.md`.

## Word Document Formatting

When generating `.docx` files with python-docx, apply these conventions:

### Basic Format

- **Font:** Times New Roman, 12pt throughout. No font size variation—12pt for all text including headers.
- **Color:** Black text throughout. No color variation—black for all text including headers. Do not use blue or any other colors.
- **Margins:** 1-inch margins on all sides (top, bottom, left, right).
- **Paragraph spacing:** Set `space_after` and `space_before` to 0 for all paragraphs. Do not use Word's default 6pt or 8pt after-paragraph spacing.
- **Line spacing:** Single (1.0).
- **Section separators:** Never use horizontal rules or lines between sections--spacing is sufficient.
- **Dashes:** Do not use em-dashes (—). Use single (-), double (--), or triple (---) hyphens instead, with no space between the dashes and adjacent text unless required for clarity.
- **Footer:** Centered page numbers in the footer on every page.

### Spacing Between Sections

Vertical rhythm comes from blank lines, not paragraph spacing:

- **Two blank lines before H1 headers**
- **One blank line after H1 headers**
- **One blank line before H2 headers**
- **Maximum two consecutive blank lines anywhere in the document.** Three or more consecutive blank lines never appear.

### Body Paragraph Indentation

All body paragraphs get a **0.5" first-line indent**. This is the primary visual separator between paragraphs--not blank lines or paragraph spacing. The only exceptions:

- **0" first-line indent** for the first paragraph after a heading (it is already visually separated by the heading)
- **0" first-line indent** for list items, table cells, and memo header fields

### Formatting Hierarchy

Create visual hierarchy through strategic use of **bold** and regular weight only—no italic, no underline, no font size changes:

- **H1 (Major sections):** ALL CAPS, BOLD. Examples: PURPOSE, BACKGROUND, RECOMMENDATIONS, NEXT STEPS
  - Implement using Word's Heading 1 style
  - Always preceded by one blank line
- **H2 (Subsections):** Title Case, Bold. Examples: Key Findings, Execution Tips
  - Use for primary subdivisions within major sections
- **No H3:** Avoid third-level headings. Use inline bold labels instead if needed.

### Inline Formatting

- **Field-value pairs:** Bold label followed by regular text
  - Example: **Tool:** Google Forms
  - For grouped pairs (consecutive lines with labels), apply 0.25" first-line indent to each line
- **Inline labels in paragraphs:** Bold followed by plain text within flowing prose
  - Example: The **key principle** is experiential contrast.
- **Checkboxes:** `[ ] **Item description**` flush left (no indent)
  - Bold the item description
  - No spacing between checkbox and text

### Lists

- **Indent:** 0.25" left indent, no first-line indent
- **Spacing:** Zero paragraph spacing between items
- **Bullet formatting:**
  - **First level:** Dot bullets (•)
  - **Second level:** Dash bullets (–)
  - Do not use plain indents without bullets for list items
- **Numbered lists:** Use Word's built-in `List Number` style, not manually typed numbers. This produces proper hanging indentation and automatic numbering.
- **No special formatting:** Regular text weight (not italic) for list items unless specific emphasis is needed

### Special Formats

- **Tables:** `Table Grid` style. Bold header row. Zero after-paragraph spacing in cells. No indentation in table cells. Font size 10--11pt in table cells (1--2 points smaller than body text). One blank line before and one blank line after every table.
- **Memo headers:** Begin with "MEMORANDUM" in bold on first line. Then TO/FROM/DATE/RE fields with bold labels (e.g., "TO:") followed by plain text. No indentation on memo header lines.
- **References:** Hanging indent format—0.5-inch left indent with -0.5-inch first-line indent. No space between entries.

### Implementation Notes

When using python-docx:

```python
# Set default font for all paragraphs
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Font
run.font.name = 'Times New Roman'
run.font.size = Pt(12)

# Ensure black text (not blue or theme colors)
run.font.color.rgb = RGBColor(0, 0, 0)  # Black

# Paragraph spacing (zero)
paragraph.paragraph_format.space_before = Pt(0)
paragraph.paragraph_format.space_after = Pt(0)

# First-line indent (default for all body paragraphs)
paragraph.paragraph_format.first_line_indent = Inches(0.5)   # Standard body paragraph
paragraph.paragraph_format.first_line_indent = Inches(0)     # First para after heading, lists, tables

# List indent
paragraph.paragraph_format.left_indent = Inches(0.25)
paragraph.paragraph_format.first_line_indent = Inches(0)  # No first-line for lists

# H1 using Heading 1 style
h1 = doc.add_paragraph("SECTION TITLE", style='Heading 1')
h1.runs[0].font.name = 'Times New Roman'
h1.runs[0].font.size = Pt(12)
h1.runs[0].bold = True
h1.runs[0].font.color.rgb = RGBColor(0, 0, 0)  # Black, not blue

# For bulleted lists
# First-level bullet (dot)
para = doc.add_paragraph(style='List Bullet')
para.paragraph_format.left_indent = Inches(0.25)
para.paragraph_format.first_line_indent = Inches(0)
para.paragraph_format.space_before = Pt(0)
para.paragraph_format.space_after = Pt(0)

# Second-level bullet (dash) - increase indent
para = doc.add_paragraph(style='List Bullet 2')
para.paragraph_format.left_indent = Inches(0.5)
para.paragraph_format.first_line_indent = Inches(0)
para.paragraph_format.space_before = Pt(0)
para.paragraph_format.space_after = Pt(0)
```

### Aesthetic Goal

Simple, crisp, utilitarian. Formatting should help the reader separate ideas, not draw attention to itself. Visual hierarchy comes from bold weight, indentation, and whitespace--not font size variation or decorative elements.

## PowerPoint Document Generation

**Always use the `/pptx` skill** to generate slide decks. Do not use python-pptx directly or other ad-hoc approaches. The skill wraps Anthropic's official PPTX skill (cloned at `~/github/anthropic-skills/skills/pptx/`) and produces native, editable .pptx files via PptxGenJS with built-in visual QA.

### Two workflows

- **Create from scratch:** Write a Node.js script using pptxgenjs. Best for new decks from markdown outlines or content files. Requires `NODE_PATH=/Users/amalani/.npm-global/lib/node_modules`.
- **Edit from template:** Unpack an existing .pptx, manipulate slide XML, repack. Best when the user provides a branded template or an existing deck to modify.

### Default style: MARP Default

The user's preferred presentation style. Minimal, content-forward, no decoration. The full preset (palette, typography, layout rules, and anti-patterns) is defined in the `/pptx` skill at `~/.claude/skills/pptx/SKILL.md`. Key properties:

- White background on every slide, no dark slides
- Helvetica Neue throughout (single font, no pairing)
- Titles: 28pt bold, #333333, with thin horizontal rule underneath
- Body: 13-14pt, #666666
- No shadows, no colored backgrounds, no accent bars, no decorative shapes
- Charts in dark gray (#333333) with minimal gridlines
- Tables with light gray header (#F5F5F5) and thin borders (#DDDDDD)

The user may request a different style for specific decks (e.g., Midnight Executive for CMS leadership briefings, or a branded template). Only deviate from MARP default when explicitly asked.

### Template usage

When the user provides a .pptx template, use the editing workflow (`unpack.py` -> edit XML -> `clean.py` -> `pack.py`). The template's slide master, fonts, and colors are preserved automatically. Run `thumbnail.py` on the template first to understand available layouts.

### QA requirement

Always generate slide images (`soffice` -> `pdftoppm`) and visually inspect before delivering. Use a subagent for fresh-eyes review. Fix issues and re-verify. Do not declare success without at least one fix-and-verify cycle.

### Fallback hierarchy

1. `/pptx` skill (preferred -- native editable .pptx, visual QA pipeline)
2. MARP (markdown-to-slides on work laptop -- good output but not editable as .pptx)
3. python-pptx (legacy -- functional but visually limited)
