---
name: Voice registry
purpose: The router's data table for the writing-voice system. Maps each of the six voices to its exemplar-bank path, its style.md Mode heading, its artifact-type triggers, its default injection set, and its register cap. Read by the before-draft skill (to select a voice and load its Layer 2 bundle) and by the after-draft skill (to know which voice to critique against). One canonical table; the skills hold the procedure, this file holds the data.
last_updated: 2026-07-27
related:
  - ~/.claude/refs/voice-architecture-strategy.md
  - ~/.claude/refs/ai-tells.md
  - ~/.claude/refs/appellate-style.md
  - ~/.claude/style.md
---

# Voice Registry

## What this is

The lookup table the voice router runs on. The full layer design lives in
`~/.claude/refs/voice-architecture-strategy.md`; this file is only the per-voice data the router
needs at selection time. Both the before-draft skill (`write-as`) and the sibling after-draft skill
read it, so a change to a bank path or a Mode heading updates in one place.

The writing stack has four layers, loaded in a fixed order (§ Load order below). This registry
governs **Layer 2 selection only** — which per-voice bundle to load. Layers 0 and 1 are the same for
every voice and sit above every row here.

---

## The six voices

| voice | exemplar bank | default injection | style.md Mode heading | fires for |
|---|---|---|---|---|
| **memo** | `~/.claude/refs/exemplars/memo.md` | **CORE (5), exemplar-primary** (Mode = reference, not co-injected — task #8, n=2) | `## Memo Mode` | CMS policy memo, decision memo, policy briefing, white paper, `.docx` memo |
| **academic-law** | `~/.claude/refs/exemplars/academic-law.md` | CORE (5) | `## Academic Mode (Law)` | law review article, legal scholarship, legal-register argument |
| **academic-econ** | `~/.claude/refs/exemplars/academic-econ.md` | **CORE (5) + Mode co-injected** (default confirmed — task #8, n=2) | `## Academic Mode (Economics)` | economics journal article, NBER working paper, handbook chapter |
| **social-essay** | `~/.claude/refs/exemplars/social-essay.md` | CORE (5) | `## Social Mode (Essay)` | Substack essay, op-ed, long-form argument for a general audience |
| **social-explainer** | `~/.claude/refs/exemplars/social-explainer.md` | CORE (5) | `## Social Mode (Explainer)` | teaching/explainer post that builds a concept from primitives |
| **appellate** | `~/.claude/refs/exemplars/appellate.md` | RECOMMENDED (5) | none — `appellate-style.md` is itself the base | ONLY when the user explicitly asks for the appellate / brief register |

Notes on the table:

- **Default injection** is the CORE set — one paragraph per archetype, injected verbatim as imitation
  targets. The bank's EXTENDED (or ALTERNATES) paragraphs are pulled on demand when the task matches a
  specific archetype the CORE set does not cover. The exact per-voice CORE-vs-EXTENDED mix is being
  A/B-tuned (task #8); until then, default to CORE. The exemplar-vs-Mode **source** mix is tuned per
  voice the same way — see § Injection mix (task #8) below; the memo row is now set to exemplar-primary.
- **`appellate` uses different section names.** Its bank is titled RECOMMENDED 5 + ALTERNATES 6, not
  CORE + EXTENDED, and it is **ASPIRATIONAL** — the voice of Roberts and Sutton, not Anup's own prose.
  Treat "RECOMMENDED 5" as the CORE set. This voice fires only on an explicit request, never by
  inference from an artifact type.
- **`appellate` has no style.md Mode** because `appellate-style.md` (Layer 1) *is* the appellate voice's
  craft reference. When drafting in the appellate register, its "Conflicts to reconcile" and
  "Do NOT transfer" sections become load-bearing (they set what the register permits and which legal
  habits not to carry into nonfiction).
- **social-essay / social-explainer Modes** are now derived (task #7) and live at `## Social Mode
  (Essay)` and `## Social Mode (Explainer)` in `style.md`. Load the Mode section together with the
  exemplar-bank CORE set; the bank's "Through-line" section remains a useful summary.

---

## Injection mix (task #8 — exemplar-vs-Mode A/B)

The `default injection` column records two things: CORE-vs-EXTENDED **depth**, and the **source** mix —
verbatim exemplar text vs. the derived `style.md` Mode prose. The before-draft skill (`write-as`) reads
this column to decide what Layer 2 loads. The mix is tuned voice by voice; results as they land below.

**memo — exemplar-primary (recorded 2026-07-27, n=2).** A two-round A/B (topics: a FedRAMP-Authorization
requirement; site-neutral OPPS payment) drafted the same ~250-word passage three ways — exemplar-heavy
(CORE verbatim only), Mode-heavy (Mode prose + checklist only), and both — screening each on a blind
voice-critic plus the ai-tells pass, with Anup's read as the tiebreaker.

- **Injecting the full Mode and the full CORE set together ("both") was the weakest arm in both rounds.**
  It over-conditions: round 1 it stacked "X, not Y" into an open-and-close frame; round 2 it dropped the
  first-person commission opener and led cold with a dense block. "Both" is the *former* load-order
  default (step 3 co-injected Mode + CORE), so the memo row now overrides it.
- **Exemplar-primary won** Anup's read in both rounds and the blind critic in round 2. The CORE exemplars
  carry the moves the Mode cannot encode (commission-naming "You asked…", "My read is", concrete named
  services, coined-and-defined terms). The Mode's real contribution was structural discipline (steelman,
  cabin, additive close); once that discipline is enforced upstream by a hardened Layer 0 (the
  announcing-opener tell added 2026-07-27), the Mode's marginal value shrinks and the exemplars pull ahead.
- **Recorded mix:** inject the CORE exemplar set as the Layer 2 voice model; keep `## Memo Mode` as the
  derivation/reference and do **not** co-inject its full prose. A compact checklist pointer — or reliance
  on Layer 0 plus appellate T1, which already carry the checklist — is sufficient.

**academic-econ — co-injection kept (recorded 2026-07-27, n=2).** A two-round A/B (topics: extreme heat and
manual-labor productivity; a conditional-cash-transfer-for-facility-birth decomposition) ran the same three
arms. The result is the opposite of memo's:

- **The blind voice-critic picked Mode-heavy in both rounds; Anup's read picked exemplar-heavy (round 1),
  then both (round 2).** His ear never picked Mode-heavy and rated exemplar and both at rough parity. The
  econ row therefore keeps the default **co-injection** (Mode + CORE) — the fuller conditioning he preferred
  — and is *not* switched to exemplar-primary.
- **Why econ differs from memo.** The econ register's authenticity is mechanical and nameable —
  first-person plural "we," magnitude-before-interpretation, coin-and-reuse, refuse-to-overclaim. The Mode
  encodes those explicitly, so co-injecting it *helps* rather than over-conditions (unlike memo, whose
  authenticity is idiosyncratic first-person moves — "You asked me", "My read is" — that the Mode cannot
  encode). Exemplar-only for econ also drifted once (round 1: dropped "we," produced an announcing opener);
  the co-injected Mode prevents that drift.
- **Recorded mix for econ:** keep load-order step 3 — inject `## Academic Mode (Economics)` **plus** the
  CORE exemplar set.

**Critic caveat (generalizes beyond econ — treat as a standing rule).** The blind voice-critic
systematically prefers the Mode-heavy arm (memo round 1, econ rounds 1 and 2) because it rewards mechanical
checklist-completion — magnitude-first every time, sustained "we," an explicit "our point is not…" — which
Mode-injection maximizes by construction. Anup's own ear repeatedly preferred exemplar or both. Treat the
voice-critic as a **tell-screen** — its concrete hits (announcing openers, cleft constructions, "X, not Y"
density) are valid and load-bearing — and **not** as the arbiter of "sounds most like Anup." His read
arbitrates voice; the critic screens tells.

**Resolved — the mix is voice-specific; no global load-order change.** The two voices tested land on
opposite mixes (memo → exemplar-primary; econ → co-injection), so there is no single global default to set.
Load-order step 3 (co-inject Mode + CORE) stays the default for every row **except memo**, which overrides
to exemplar-primary. The four untested voices (academic-law, social-essay, social-explainer, appellate)
keep the co-injection default until their own A/B is run.

---

## Register caps (em-dash and rhetorical question)

Tells are universal, but two of them (em-dash §9, rhetorical question §6 in `ai-tells.md`) have a
**register-sensitive frequency cap**, not an absolute ban. The cap is set to Anup's own corpus rate,
register by register. The router carries the cap for the selected voice into the draft.

| voice | em-dash cap | rhetorical-question cap |
|---|---|---|
| **memo** | drafting target ≈1 per 1,000 words (low, like academic — the current corpus runs ≈7–9/1k, but every memo in it postdates AI adoption, so that is not a clean read on his hand); **output** stays strict: the `.docx` spec hard-bans the glyph, converting it to `--`/`---` at export without stripping the appositive | rare; ≤1 per section, and only where the answer is genuinely the reader's |
| **academic-law** | ≈1.4 per 1,000 words (appositive/definitional, not pause) | rare; formal-argument cap |
| **academic-econ** | ≈1 per 1,000 words (runs lower than law) | rare; formal-argument cap (one authentic instance exists in the bank) |
| **social-essay** | ≈3.9 per 1,000 words (his hottest register; the earlier ≈1.3 was an undercount that missed the `---` convention) | a few per piece OK; do not open successive paragraphs with questions, never stack |
| **social-explainer** | ≈1.4 per 1,000 words (the earlier ≈0.4 was the same `---` undercount) | a few per piece OK as section pivots; same no-stacking rule |
| **appellate** | ≈1 per 1,000 words (register permits; see `appellate-style.md` Conflicts) | at most one per section; never stacked |

The tell is density and pile-ups, not a single dash. At or under the cap, leave them; well above it, or
two in one sentence, fold the extras into commas, conjunctions, or periods. Keep a source's own
em-dashes only inside verbatim quotations. **Nothing he writes runs above ≈3.9 per 1,000 words —
treat 3.9 as the hard ceiling for every register.** Full rules: `ai-tells.md` §6 and §9.

---

## Load order at write time

1. **Layer 0 — `ai-tells.md`** (negative screen). Always on, including chat; a compressed copy is in
   `~/.claude/CLAUDE.md`. Load the full file for the drafting/revision pass.
2. **Layer 1 — `appellate-style.md`** (universal positive base: structure universals + sentence-craft
   universals). Load for any artifact.
3. **Layer 2 — the selected voice's bundle**, from this registry: its style.md Mode section (if one
   exists) **plus** its exemplar-bank CORE set, injected verbatim as models to imitate. *(Exception,
   task #8, resolved 2026-07-27: the **memo** row is exemplar-primary — inject CORE only, not the full
   Mode. Every other row keeps this co-injection default; the academic-econ A/B confirmed it. The mix is
   voice-specific — see § Injection mix.)*
4. **Layer 3 — output formatting** (`style.md` formatting + docx/pptx) at export.

Ordinary chat with no artifact loads Layer 0 plus the compressed **briefing** voice (memo's answer-first, mechanism-explaining spine, adapted to teach rather than compress) bound in `~/.claude/CLAUDE.md` — no full Layer 2 Mode and no exemplar bank. The briefing voice is the chat conversational default (was social-explainer; changed 2026-07-29). It is a chat register only and alters no artifact voice.

---

## Router decision rule (summary)

The `write-as` skill holds the full procedure; in one line: **explicit voice command wins** (a voice
name or "write this as a <type>"), **else infer the voice from the artifact type** in the table above,
**else ask** which voice when the artifact type is genuinely ambiguous (a "paper" with no field → law
or econ; a "post" that could be argument or teaching → essay or explainer). No artifact in play → no
Layer 2.

---

## Audience (second routing axis)

Form usually implies audience for Anup's own writing — his memos go to policymakers, his papers to peers,
his essays and explainers to a general reader — so the router can pick a voice from form alone. It breaks
when a project has an academic **form** but a general **audience**: a systematic review published as a
public web resource, an empirical explainer for a lay reader. Audience is therefore a second routing
input. When a project names a general-audience output or a specific reader standard (in its `CLAUDE.md`,
a protocol, or a spec), that audience **overrides** form-based voice inference. `write-as` Step 0 reads
the project for this before routing; `voice-check` runs its dinner-table test against the named reader,
not the register. The accessible-but-rigorous case below is the concrete blend this axis produces.

---

## Edge cases and fallbacks

- **General academic / no clear field.** There is no separate general-academic voice row; the two
  retired parent banks (`exemplars/academic.md`, `exemplars/social.md`) are provenance-only, do not
  inject from them. For an academic piece that is neither clearly law nor clearly economics, ask the
  field, or default by field — `academic-econ` for empirical/quantitative work, `academic-law` for
  doctrinal/normative — **but only once the audience is settled.** Quantitative work aimed at a general
  reader does not go to `academic-econ`; see the accessible-but-rigorous case below. `style.md` also
  carries an `## Academic Mode (General)` section for the cross-field rules.
- **Biomedicine.** No dedicated exemplar bank exists. `style.md` has `## Academic Mode (Biomedicine)`,
  and the corpus practice is to draft in the general academic voice, then translate to the biomedical
  journal's house style (which strips roughly half the voice markers). Route a biomedical artifact to
  the `academic-econ` bank (its empirical, results-first register is the closest fit) plus the
  Biomedicine Mode section, and expect the translation step.
- **Mixed / hybrid request** (e.g., "an essay that teaches a concept"). Prefer the register whose
  primary job the piece does: making an argument → social-essay; building a concept from primitives →
  social-explainer. When both banks have a relevant archetype, the CORE set of the primary voice plus
  one on-point EXTENDED paragraph from the other is a reasonable blend.
- **Accessible-but-rigorous (quantitative work for a general audience).** An artifact can report point
  estimates, standard errors, confidence intervals, and GRADE certainty *and* be aimed at a general
  reader — a public web resource, an explainer, a project whose protocol names a "smart undergrad"
  standard. None of the six voices covers this on its own, and defaulting quantitative work to
  `academic-econ` sends it to the least accessible register available (the fertility-review failure).
  Route it as a **blend, not a new voice**: `social-explainer` is the **primary** register, and
  `academic-econ` is consulted **only** for estimate-reporting conventions (magnitude before
  significance, honest uncertainty, named specifications). **Suppress** academic-econ's "coin and reuse
  a technical label" and "theory before empirics" — those two Mode instructions are what produced the
  rejected draft. Gloss every coined term (`ai-tells.md` §22), since the audience is general.

---

## Related

- `~/.claude/refs/voice-architecture-strategy.md` — the full four-layer design and the router concept.
- `~/.claude/refs/ai-tells.md` — Layer 0, the always-on negative screen (§6, §9 hold the caps above).
- `~/.claude/refs/appellate-style.md` — Layer 1, the universal positive base.
- `~/.claude/style.md` — Layer 2 Modes + Layer 3 formatting.
- `~/.claude/skills/write-as/SKILL.md` — the before-draft skill (the router lives here).
- `~/.claude/skills/voice-check/SKILL.md` — the sibling after-draft screen; reads this registry to know
  the target voice for its critique.
</content>
</invoke>
