---
name: AI-tell blocklist
purpose: Canonical, greppable list of the AI-characteristic prose tics to suppress in ALL writing (chat, drafts, memos, papers). Source of truth consolidated from voice-critic/corpus.md (the user's own red-pen edits), appellate-style.md, the not-ai detector loop, and the social voice guide. A compressed version is embedded always-on in ~/.claude/CLAUDE.md; this file is the full reference, loaded on demand for a revision pass or when the compressed list is not enough.
last_updated: 2026-07-26
---

# AI-Tell Blocklist

## What this is

The single source of truth for the prose tics that make writing read as machine-generated.
Every rule below was earned from the user's own edits or from the appellate paragons, not
from generic advice. The empirical backing lives in
`~/.claude/skills/voice-critic/corpus.md` (19 before/after pairs in the user's red pen);
this file generalizes those into named, greppable rules. `corpus.md` stays as the evidence
base — do not delete it.

**Governing principle: tells are universal; register is artifact-specific.** Suppress every
tic below *everywhere*, including casual chat. That is different from the full formal
register (Memo Mode / Academic Mode in `style.md`), which loads only for a written artifact.
Killing the tells does not mean writing a chat reply as a memo — it means chat, drafts, and
memos alike are free of the tics. One rule is the exception: §22 (unglossed coined jargon) is
**audience-conditional**, not universal, because glossing a coined term is right for a general
reader and wrong for a peer one; it fires only when the audience is general. §23 is scoped to
reader-facing prose. Both are consequences of the same fact — a tell can be created by writing
to the wrong reader — which is a routing problem the screen sits downstream of.

**How to use:** read in five minutes, then apply the CHECK lines paragraph by paragraph
during a revision pass. When drafting, keep the compressed list (in `CLAUDE.md`) in mind and
return here when a call is close.

**Provenance.** Rules 1–14 and the dinner-table test were earned from the user's own edits and
the appellate paragons. Rules 15–19 were added 2026-07-25: §15–§16 from a register-and-rhythm
audit of the chat surface, §17–§19 from a cross-check against the published AI-writing
literature (Wikipedia's AI-cleanup guide, Kobak et al. excess-vocabulary study). They are
structural and checkable, not word lists. §20 was added 2026-07-26 from the user's own
observation — definite-article overuse, flagship instance "ran the test." §21–§23 were added
2026-07-26 from a field report on the fertility-review project, where a systematic-review chapter
written in a peer register was rejected by its general-audience target: §21 clefts (manufactured by
the no-copy constraint), §22 unglossed coined jargon (audience-conditional), §23 insider reference.

---

## 1. "X, not Y" antithesis — nuanced ban

Prohibited as a **slogan, a bold fragment, or a reflexive cadence**. Permitted only inside a
full clause where the "not Y" carries real, checkable information the reader needs.

Why: the antithesis fragment summarizes instead of arguing; it reads as a marketing pull-quote.
The same contrast inside a working clause reads as an argument.

BANNED (slogan / fragment / reflexive beat):
- "Blood-based serology is **complementary, not duplicative.**" (corpus 18)
- "It's not about X — it's about Y."
- "One case is the tail; the other is the rule." (corpus 8 — "decode-me antithesis as profundity")

PERMITTED (full clause, "not Y" adds a fact):
- "Congress passed the Affordable Care Act to improve health insurance markets, not to destroy them." (Riley/King register)

REWRITE: embed the contrast in a full clause with a concrete referent, or replace the
antithesis with the factual sentence the reader actually needs — the number, the share, the
comparison (corpus 8: "Naseema, handing over half her income for water alone, is at the tail
of this distribution: … only one in fifty was spending half or more …").

CHECK: does "not Y" add a fact, or just a beat? Beat → cut. Is it a fragment or a bolded
pull-quote? → rewrite as a full clause with a named referent.

---

## 2. Ambiguous antecedents and lazy pronouns

Every "it / this / that / these / they" must bind to exactly one noun — the nearest
unambiguous one. If a pronoun could attach to two nouns, write the noun instead.

Why: an ambiguous "it" forces the reader to solve a puzzle the writer should have solved.
Precise repeated nouns read as careful; floating pronouns read as generated.

Counter-rule (so this does not become clumsy): do not repeat a noun three times in a
sentence to avoid a pronoun. If the repetition gets heavy, restructure the sentence so a
single clear referent governs. **Precision first, then concision.**

CHECK: for each "it / this / these / they," name the noun it replaces out loud. If you
hesitate, or find two candidates, write the noun. If naming the noun three times reads badly,
recast the sentence.

---

## 3. Bare-noun and fragment openers

Do not open a paragraph or section with a bare-noun fragment or a mystery hook. Lead with a
subject-verb sentence that names whose idea and what structure follows.

BEFORE: "Two ingredients. People are loss averse: losses sting roughly twice as much …" (corpus 3)
AFTER: "Benartzi and Thaler's theory rests on two ingredients. First, people are loss averse …"

BEFORE: "Something hidden in precolonial Africa — ethnic groups that allowed women to hold office — turns out to predict …" (corpus 4)
AFTER: "Where women held political office in precolonial African societies, more women hold political office today."

CHECK: does the first sentence have a subject and a verb? Is it a documentary-teaser hook
("Something hidden in…", "Begin with…")? → replace with the plain claim or the scene itself.

---

## 4. Consecutive short sentences (staccato runs)

Vary sentence length naturally. A single short sentence lands, especially after a long one.
Two or more short sentences in a row read as fragments-for-effect and flatten the point, and
that run is the tell. Hold the register steady while length varies: a paragraph that lurches
from formal to clipped-informal and back reads as generated even when no single sentence is
wrong.

BEFORE: "Construction jobs paid well. College cost years of foregone wages. So the rational 18-year-old took the job." (corpus 2)
AFTER: "During the 2000s housing boom, a lot of American teenagers quietly skipped college. Not because tuition rose, but because construction jobs were suddenly paying so well that staying in school felt like leaving money on the table."

CHECK: mark word counts. Two or more consecutive sentences under about eight words is a run;
fold all but one back into their neighbors, keeping the register constant across the fold
(appellate B5). Sentence-length spread is a soft diagnostic that flags either a choppy run or a
flat monotone; it is never a numeric target.

---

## 5. Anaphora — repeated sentence-opening word

Do not stack short sentences that open with the same word (None / None / None; This / This /
This). Collapse into one complex sentence with coordinated clauses.

BEFORE: "None of these systems measures population immunity …. None can reliably estimate …. And none can track …." (corpus 15)
AFTER: "None of these systems measures population immunity … nor can they reliably estimate true infection rates … or track whether the population is entering a respiratory season with sufficient residual immunity …."

CHECK: read the first word of each sentence in a paragraph. Repeats → coordinate them.

---

## 6. Rhetorical questions (a frequency cap by register)

A rhetorical question is a tell when it becomes a reflexive tic, not when it appears once to
real effect. Anup uses them sparingly, and more in teaching than in formal argument, so cap the
rate rather than banning them outright.

- **Memo and formal argument: rare.** Convert most rhetorical questions into a declarative
  noun-phrase series. Allow at most one per section, and only when the answer is genuinely the
  reader's to supply.
- **Social and explainer: a few per piece.** Framing a point with a question ("What is
  demand?") is authentically his teaching voice. Still cap it: do not open successive paragraphs
  with questions, and never stack them.
- Never use a rhetorical question to dodge stating a claim you could state flat.

BEFORE: "It answers questions the traveler system cannot: How much immunity does the population carry …? How effective was last year's RSV vaccine …?" (corpus 17)
AFTER: "It addresses questions the traveler system is not designed to answer: the level of immunity the general population carries into a given respiratory season; the effectiveness of the prior year's RSV vaccine in the 65+ cohort; …"

CHECK: count the rhetorical questions, not the genuine ones the reader must answer. More than
one per section in formal prose, or a run of them in any register, is the tell; convert the
surplus to declaratives.

---

## 7. Tricolon / rule-of-three for cadence

A three-part parallel series is fine when each item carries distinct information. Cut it when
the parallelism is doing rhythm rather than work.

CHECK: does each of the three items add a fact the others do not? If one is there for the
beat, cut it or fold it in (appellate Conflicts — triads).

---

## 8. Decorative connectives

"Moreover / furthermore / additionally / in addition" only pile sentences up. A real
transition states what the next sentence does to the last.

BEFORE: "Furthermore, the migration account also faces difficulties. Moreover, it under-explains the timing." (appellate D1)
AFTER: "The migration account describes the change but not its timing."

CHECK: for each "moreover / furthermore / additionally," name the logical relation it marks.
"Another point" → replace with a transition that states the relation, or start a clean
paragraph.

NOTE (carve-out for rule 16): "Moreover" or "Finally" is allowed when it marks a genuine
enumeration beat, the second or third item in a real series, as distinct from piling on an
unrelated point. The ban targets the decorative pile-up, not the counted step.

---

## 9. Em-dash overuse (a frequency cap by register)

The em-dash reads as an AI signature because models overuse it. The dash itself is fine; its
frequency is the tell, and the rate is register-specific, set to Anup's own measured number. His
essay/argument register runs hottest, about 3.9 per 1,000 words; his academic, explainer, and
appellate prose run low, about 1 to 1.4; his memos are drafted to the same low ~1 (the higher
rate in the current memo corpus postdates his AI adoption and is most likely inflation, not his
hand). Nothing he writes runs above ~3.9 per 1,000; treat that as the hard ceiling for every
register. Measure with the full definition: literal "—", spaced " -- ", and runs of three or more
hyphens "---" (how his exported prose renders the dash). Counting only "—" and "--" undercounts by
roughly threefold — the error that produced the old ~1.3/1k essay figure.

- **Memo output and formal `.docx`: strict, effectively zero.** The `.docx` spec forbids the
  glyph; at export every dash becomes `--`/`---` or is recast. In drafting, keep memos low, about
  1 per 1,000 words.
- **Academic, explainer, appellate: about 1 to 1.4 per 1,000 words.** Low and steady; an
  occasional dash is authentically his, and the tell is density and pile-ups, not one dash.
- **Essay / argument register: up to about 3.9 per 1,000 words.** His genuinely runs this hot, so
  do not flag an essay for dashes until it clears ~3.9, stacks two in one sentence, or uses the
  dash as a reflexive pause several times a page. Never above ~3.9 anywhere.
- Keep a source's own em-dashes only inside verbatim quotations.

BEFORE: "broker commissions, customer service, eligibility infrastructure, ID verification -- the cancellation breaks" (corpus 14)
AFTER: "broker commissions, customer service, eligibility infrastructure, or ID verification, the cancellation breaks"

CHECK: grep for "—", " -- ", and "---" (all three; the triple-hyphen is how his exported prose
renders the dash, and missing it undercounts by ~3x), divide by words/1000. In a memo or `.docx`
output, cut every one. In a permissive register, at or under that register's cap leave them (essay
~3.9, academic/explainer/appellate ~1–1.4); well above the cap, or piled up, fold the extras into
commas, conjunctions, or periods.

---

## 10. Metaphor-as-structure

Name an idea with a metaphor once if it helps; do not push the metaphor past its first use
into structural tags, and do not use vague geometric metaphors ("shape," "curve,"
"trajectory") as ornament.

BEFORE: "That is the quality currency. And the time currency is paid most heavily …" (corpus 10)
AFTER: "The tax comes in three forms … The first is money … The second is quality … The third is time." (plain operative noun on every later reference)

BEFORE: "the gap is the same shape" (corpus 9)
AFTER: "The same gap appears for toilets: about a third of slum households without a decent one …"

CHECK: for each metaphor, ask "why this word?" If you cannot answer literally, cut it. After
first use, does a plain operative noun (money, time, gap) carry the later references? It should.

---

## 11. Triumphant / sales verbs

Policy and academic prose should not sound like a pitch. Prefer neutral, precise verbs.

BEFORE: "Blood-based serology **closes all three gaps simultaneously** …" (corpus 16)
AFTER: "Blood-based serology addresses all three of these gaps …"

Watch-list: "closes all gaps," "unlocks," "seamlessly," "supercharges," "revolutionizes,"
"empowers," "leverages."

CHECK: does the verb sell or state? Selling → replace with the neutral verb.

---

## 12. Clever / allusive ellipsis endings

Do not end on a knowing, ambiguous half-phrase. Close on a plain declarative.

BEFORE: "… a war shock that got institutionalized — and then slowly wasn't." (corpus 19)
AFTER: "… a wartime shock that postwar institutions preserved for 25 years, then went away."

CHECK: is the last clause plain and unambiguous, or is it winking? Winking → state it
straight.

---

## 13. Hollow topic sentences and scaffolding directives

Open each paragraph with the sentence that states what the paragraph will prove — not a
stage-direction to the reader ("Consider next…", "Begin with…", "Let us turn to…") and not a
throat-clearing setup.

BEFORE: "Begin with water, and begin with one man." (corpus 6)
AFTER: "Water is where the poverty tax falls hardest, and Raman is one of the men who collects it."

CHECK: read only the first sentence of each paragraph, end to end. Do they form the argument?
Is any of them a directive rather than a claim? Directive → replace with the paragraph's
actual conclusion (appellate A4).

---

## 14. Throat-clearing hedges and intensifiers

"It is worth noting," "clearly," "obviously," "arguably," "quite," "very," "rather" — each
adds nothing or quietly retracts the claim. State the thing and stop.

BEFORE: "It is worth noting that cost is arguably one of the most important and clearly significant barriers to enrollment." (appellate C3)
AFTER: "Cost is the largest barrier to enrollment, ahead of paperwork and eligibility rules combined."

A second family belongs here: emphatic intensifiers that inflate rather than hedge. "Exactly,"
"precisely," "simply," "just," "the very," and the reveal-frame "what no one [sees / does /
says]" read as machine-written when they amplify a rhetorical beat. The word itself is fine;
what flags is the amplifier function. Anup uses these words at a normal rate (exactly and
precisely each about 4 to 5 times per 100k words, simply and just far more), but for literal
or measured precision, never as a climax amplifier: "exactly equal to," "costs exactly p\*,"
"exactly what we observe" when a prediction meets the data. The tell is the amplifier use,
where the intensifier points at nothing measurable and only adds emphasis.

BEFORE: "A lease in a dense city is exactly what he cannot afford."
AFTER: "He cannot afford a lease in a dense city."

CHECK: grep the hedges "clearly / obviously / arguably / it is worth noting / quite / very /
rather," delete each, and confirm the sentence is stronger. For the emphatic set, grep the
low-noise constructions "exactly what / is exactly / are exactly / precisely what / the very /
what no one"; "just" and "simply" are too common to bulk-grep, so catch those by reading for
the amplifier use. On every emphatic hit apply the function test: delete the intensifier, and
cut it unless deleting it loses a literal fact (an equality, a measured quantity, or a pointer
to one specific referent the sentence names). Flag for function-review, do not swap in a
synonym.

---

## 15. Assistant sycophancy and manufactured enthusiasm

Do not praise the question, affirm the user's brilliance, or perform eagerness. This is the tic
that most dominates chat, and it is banned there like every other rule here.

BANNED: "Great question!", "That's insightful," "I'd be happy to help!", "Absolutely! Let's
dive in," a reflexive "You're absolutely right!", "I hope this helps! Let me know if you have
any questions," and exclamation marks used for enthusiasm rather than genuine surprise.

REWRITE: delete the affirmation and start on the answer. If the user is right, state the
substantive point that follows, not that they are right. State any real caveat flat.

CHECK: does the first sentence do work or warm up? Grep for "great," "happy to," "absolutely,"
"you're right," "hope this helps," and any "!". Each is a warm-up; cut it.

---

## 16. Rigid three-part enumeration and restating wrap-up

Enumeration itself is not a tell; two narrow moves are. The first is always landing on exactly
three items: vary the count to fit the material, and never pad to three or compress into three
for the rhythm. The second is a closing sentence that restates the paragraph's own topic
sentence.

PRESERVE (these are the user's own patterns, not tells): enumeration in any count; varied
enumerator forms, including a plain first point followed by "Moreover," or "Finally," for later
beats instead of a literal "First, Second, Third"; and forward hooks, where a paragraph ends by
raising the issue that the next paragraph's topic sentence answers, the opposite of a restating
wrap.

CHECK: count the items in each series; if it is always three, confirm the material actually had
three. Read each paragraph's last sentence; if it restates the first, cut it and end on the
strongest point or a forward hook.

---

## 17. Significance inflation

Do not puff an ordinary fact into historical or legacy language. This is the web literature's
single most-cited tell (Wikipedia lists it first), and it is the largest gap this file closes:
rules 10 and 11 catch metaphor and sales verbs, but not the specific move of inflating a
routine fact into a momentous one.

BANNED: "stands as a testament to," "underscores the importance of," "marks a turning point,"
"represents a fundamental shift," "leaves an indelible mark," "sets the stage for," and present
participles doing fake explanatory work ("symbolizing the region's commitment," "reflecting
decades of investment").

REWRITE: state what happened and let the reader weigh it. Replace "X underscores the importance
of Y" with the plain fact about X and Y, and drop the claim of significance unless you can name
the concrete stake.

CHECK: for each clause that asserts importance, a turning point, or a legacy, ask whether the
fact earns it. If the significance is asserted rather than shown, cut the inflation and state
the fact.

---

## 18. Copula avoidance

Do not dodge "is / are / has" by reaching for a fancier linking verb. "Serves as," "stands as,"
"functions as," "boasts," "features," and "represents" usually replace a plain "is" or "has"
with no gain in meaning.

BEFORE: "The program boasts three components and serves as a model for reform."
AFTER: "The program has three components and is a model for reform."

CHECK: grep for "serves as," "stands as," "functions as," "boasts," "features," "represents."
For each, try "is" or "has" in its place; if the sentence keeps its meaning, use the plain verb.

---

## 19. Vague and unnamed attribution

Do not launder an unsourced claim as consensus. "Studies show," "experts argue," "research
suggests," and "reports indicate," with no named source, assert an authority the writer has not
earned. This is an accuracy problem as much as a voice one, and it is dangerous in a memo, where
an unverified generalization dressed as settled fact can mislead a decision. (See the sourcing
standards in `style.md`.)

REWRITE: name the study, author, or body, and cite it; or, if you cannot, drop the appeal to
authority and make the claim on its own evidence, or cut it.

CHECK: for each "studies show / experts argue / research suggests / reports indicate," name the
specific source. If you cannot, the sentence is either unsupported or padded; cite it or cut it.

---

## 20. Definite-article overuse — "the" where "a" belongs

Models reach for the definite article by default, which quietly asserts a specific, shared
referent the text never established. "Ran the test," "the user," "the key insight," "the
problem" each presuppose one particular thing already in view. Use "a" (indefinite) unless a
specific object is genuinely in mind; the user's own usage is the standard — "the" when there
is a specific object he is thinking of, "a" otherwise. A definite article is a small claim that
the reader already knows which one; do not make it for free.

BEFORE: "I ran the test and it came back clean." (no test had been specified)
AFTER: "I ran a word-count on the draft, and the em-dash rate came back clean." (name the specific
thing, or use "a")

This is not a ban on "the" — it is the commonest word in English and usually right. It is a
function test on a definite article that introduces a noun the text has not already put in view.

CHECK: for each "the + noun" that introduces a referent (not one named earlier in the passage),
ask "is there one specific object already in view that the reader can point to?" If yes, keep
"the." If no, switch to "a," or name the specific thing. "ran the test" is the low-noise string
to grep; the general pattern is read-for-it, since "the" cannot be bulk-grepped.

---

## 21. Fronted and cleft constructions

A cleft or fronted frame ("Y is what X", "What X is is Y", "It is Y that X") holds the subject back
and reads as an evasion of a plain statement. It is worst in a topic sentence, where the reader most
needs the claim first. **Position matters more than density:** a single cleft opening a paragraph is a
tell even when the whole-document rate looks fine — one draft measured three clefts in 1,900 words, a
rate that looked acceptable, and the author flagged on sight the one that opened a paragraph. The tell
is also **manufactured by anti-copying pressure:** an agent told to rewrite from scratch and forbidden
to reuse the source's sentences reaches for one syntactic frame to restate them (one chapter came back
with 26 clefts in 6,060 words against a source carrying 8 in 5,975).

BANNED (front the real subject and say the claim straight):
- "Whose schooling does the work is what separates this stream from the child-economic-value hypothesis." → "This hypothesis turns on the girl's own schooling, not her future child's."
- "Four channels run from a schooling mandate to the timing of a birth, and they divide on whether…" → "A schooling mandate can delay a birth in four ways. Two of them work through…"
- "That possibility is what puts catch-up at the center of the debate." → "Catch-up is central because…"

Grep net (flag for review, not a hard ban — genuine questions and some fronting are fine, especially in
the explainer register): `is what`, `are what`, `was what`, `were what`, `^What `, `. What `.

CHECK: for each hit, and for every topic sentence, ask "is the grammatical subject the thing the
sentence is about, stated first?" If a cleft is holding the real subject back, front it and say the
claim plainly. Be most ruthless in topic sentences; assume a reader who is easily confused.

---

## 22. Unglossed insider jargon (audience-conditional)

**This rule is scoped to a general audience; it is the deliberate opposite of the peer-register move.**
When the reader is a general one — a public explainer, a web resource, a "smart undergrad" standard —
any term the writer or the project's own pipeline coined must be said in plain English on first use, or
dropped. In a peer register the inverse holds: Academic Mode's "coin and reuse a technical label" is a
feature, because the specialist reader gains precision from a named lens. So this is not a universal
ban; it fires only when the audience is general, and routing a public artifact to a peer register is
exactly what produces the failure it catches.

BANNED for a general reader (gloss in the same sentence, or cut): "effect-level extraction," "common
quantity," "citation-frame accounting," "version collapse," "prespecified pooling audit," "outcome
families," and pipeline labels like "the compulsory-schooling, teenage-pregnancy, and birth stream."

BEFORE: "No group contains three independent studies reporting a common quantity."
AFTER: "No group has three separate studies that measured the same thing — the same effect, in units you
could actually compare."

Say the plain meaning in the same breath as the term, or replace the term with the plain meaning outright
("We can't just pool the 17 estimates because they measure different outcomes"). Not greppable in general;
this is a read-for-it rule that wants a per-project list of the terms the pipeline coined.

CHECK: for each coined or technical noun phrase, ask whether THIS artifact's actual reader would know it.
General audience → gloss it in-sentence or drop it. Peer audience → a coined-and-reused label is fine
(see Academic Mode). If you cannot say which, you have an audience-routing problem, not a word problem —
resolve the audience first.

---

## 23. Insider reference in reader-facing prose

Reader-facing prose is written for a reader who does not know the team, the roadmap, or how the sausage
is made. Three moves break that, and all three reached the author as defects:

- **Naming teammates the reader does not know.** "Alexandra's relevance review left 10 papers" → "our
  review left 10 papers." The reader has no reason to track who did which step.
- **Describing methodology the project has not run,** or narrating its future roadmap ("the Phase 1
  keyword search the protocol will eventually require"). The reader is not following the protocol.
- **Smuggling collaborator-facing material into reader-facing text.** Anything genuinely aimed at
  co-authors goes in an explicit `[Note to co-authors: …]` block, or comes out.

Author, verbatim: "in the write-up, never refer to Alexandra, Shravan, or me. The reader does not know
us, nor does it care about specific things that Alexandra did. If it's relevant to the methodology, say
it." Scope: reader-facing prose only — a memo genuinely addressed to co-authors is a different artifact.

CHECK: grep for collaborator first names and for "we will / we plan / eventually / the protocol will";
for each, ask whether the reader is served. If not, recast to "our review / the review" and state only
the methodology that matters, or move the aside into a bracketed co-author note.

---

## The plain / dinner-table test (the meta-check)

Above every specific rule sits one test the user applies to his own drafts: **would you say
this sentence to a smart non-expert across a dinner table?** If a sentence performs —
rhetorical inversion, decorative parallel, ornamental metaphor, "in other words" / "what is
striking" tics — cut it or say it plainly. Plain ≠ shallow. The paragons (Banerjee/Duflo,
Levitt, Pinker) read plain because they *explain*; do not perform plainness as a style
(corpus 11).

---

## Appendix: grep-net (triage only, not a rule)

A fast first-pass grep for the highest-consensus AI hard-ban words. This is a triage net, not a
rule: a single hit may be legitimate, and the trigger is density. If grep finds two or more of
these in one paragraph, slow down and apply rules 1 through 19 plus the dinner-table test; do
not just swap in a synonym and move on. Formatting tells (title-case headings, bold-stemmed
bullets, emoji) are a presentation concern and live in the docx spec, not here.

`delve`, `delving`, `tapestry`, `testament`, `underscore(s)`, `meticulous`, `boast(s)`,
`showcase`, `pivotal`, `seamless`, `intricate`, `garner`, `leverage` (as a verb), `realm`,
`landscape` (metaphorical), `cutting-edge`, `game-changer`, `elevate`, `holistic`, `plethora`,
`multifaceted`, `groundbreaking`, `embark`, `resonate`, `harness` (as a verb), `empower`,
`poised`, `supercharge`, `commendable`, `burgeoning`, `revolutionize`.

Emphatic-intensifier constructions (see §14) are a second net with a different rule: `exactly
what`, `is exactly`, `are exactly`, `precisely what`, `the very`, `what no one`. These are
**flag for function-review, not synonym-swap.** Unlike the words above, Anup uses these same
strings legitimately for literal or measured precision, so a hit is not a hard-ban. On each
hit, apply the §14 function test (delete it; keep only if it carried a literal fact) instead
of reaching for a synonym.

A third low-noise string, `ran the test`, flags the definite-article overuse of §20, on the
same flag-for-function-review footing: ask whether a specific test is already in view; if not,
write "a test" or name it. The general "the"-for-"a" pattern cannot be grepped — "the" is the
commonest word in English — so catch it by reading, not by net.

The §21 cleft/fronted net is `is what`, `are what`, `was what`, `were what`, `^What `, `. What ` —
also flag-for-review, not a hard ban (questions and some fronting are legitimate, especially in the
explainer register), and weight topic-sentence position heavily: a cleft opening a paragraph is a tell
regardless of the whole-document rate. §22 (coined jargon) and §23 (insider reference) are read-for-it
and want a per-project list; grep collaborator first names for §23, but there is no general net for
either, and §22 fires only for a general audience.

---

## Related

- `~/.claude/skills/voice-critic/corpus.md` — the 19 empirical before/after pairs behind these rules.
- `~/.claude/refs/appellate-style.md` — positive voice target and sentence craft (layer on top of this).
- `~/.claude/style.md` — the register (Memo / Academic) to write in once the tells are suppressed.
