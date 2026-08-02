---
name: Voice architecture strategy
purpose: Resolves how the "AI-tells" system and the "writing-style" system relate, separates the organization-vs-style axis, and defines the target layered architecture that the empirical per-voice profiles (item 2) plug into. Reference doc; read when deciding where a writing rule belongs or when building the voice router.
last_updated: 2026-07-25
---

# Voice Architecture Strategy

## Verdict up front

The AI-tells system and the writing-style system are not competing answers to one question; they are two orthogonal layers that fail in different ways, so "which is better" is the wrong frame. The AI-tells system is a **negative screen**: it removes the machine signature and is the same for every artifact, including chat. The writing-style system is a **positive model**: it adds Anup's specific fingerprint and changes with the genre. Passing the screen does not make text sound like Anup, and sounding like Anup does not by itself pass the screen. You need both. If forced to spend marginal effort on sounding like *him*, spend it on the positive voice models, because the screen is necessary, nearly complete, and cheap, while the higher ceiling lives in the voice layer.

The user's second intuition is also right and cuts a different way: some rules govern **organization** (what goes where) and others govern **sentence style** (word choice, rhythm, syntax). That axis is real, but it is a tag on each rule, not a reason to multiply files. The operational split that earns separate files is negative-vs-positive and universal-vs-per-voice.

---

## 1. The two systems solve different failure modes

The negative screen and the positive model are orthogonal because they answer different questions. The screen answers "does this read as machine-generated?" The model answers "does this read like Anup?" A draft can pass one and fail the other, which is what makes them independent rather than redundant.

The four-cell picture makes the independence concrete:

| | Sounds generic / faceless | Sounds like Anup |
|---|---|---|
| **Fails the screen** (has tells) | Raw AI slop: em-dashes, "moreover", "X, not Y" slogans, staccato runs. | A decent Anup imitation that still leaks one tell — a stray em-dash pause or a "furthermore". Plausible and common. |
| **Passes the screen** (clean) | Competent, plain, tell-free prose that could be any careful writer. This is where a scrubbed AI draft lands. | The target. |

Both off-diagonal cells exist, and that is the whole proof. Clean prose that sounds like no one in particular (top-right passing, bottom-left of the clean row) shows the screen alone does not confer a voice. An Anup imitation that still carries a tell (top-right of the fail row) shows the voice model alone does not clear the machine floor. Reaching the target cell requires both systems.

State each problem plainly:

- **The negative screen removes the machine floor.** Its failure mode is machine-ness leaking in. It is universal and voice-independent; the same 14 tics are banned in a tweet, a chat reply, a CMS memo, and an NBER paper.
- **The positive model raises the human ceiling.** Its failure mode is faceless competence, or the wrong face for the artifact. It is voice-specific; a memo voice and an academic-economics voice are different targets, and each is a fingerprint the screen knows nothing about.

Redundant, complementary, or orthogonal? Orthogonal. They share almost no content once the current duplication is cleaned up (see §4). The small apparent overlap — a couple of rules that appear in both files today — is an accident of how the files grew, not evidence that the two systems do the same job.

---

## 2. The second axis: organization vs sentence style

Organization and sentence style are a real second axis, and it cross-cuts the negative-positive axis rather than lining up with it. Organization rules govern document and paragraph architecture — what claim opens a paragraph, what order evidence arrives in, which section skeleton the piece follows. Sentence-style rules govern the inside of a sentence — word choice, rhythm, syntax, pronoun binding. Both axes are live at once, which is why the rules currently feel tangled: a given rule is either negative or positive *and* either organizational or sentence-level.

Crossing the two axes gives the map that should govern where every rule lives:

| | **Universal** (all his expository writing) | **Per-voice** (genre-specific) |
|---|---|---|
| **Organization** | Topic-sentence-first; lead with the finding; one idea per paragraph; roadmap paragraph and signposting; end-emphasis placement. | Section skeleton: IMRaD vs law-review parts vs numbered-theory-then-empirics vs memo sections. Result ordering: claim-then-caveat vs magnitude-then-significance. |
| **Sentence style** | The negative screen (ai-tells: em-dash, "X, not Y", antecedents, staccato, anaphora, connectives, sales verbs, hedges) **plus** positive universals: vary sentence length, active voice with a named actor, strong verbs over nominalization, plain over Latinate, one concrete image for an abstraction. | Hedge vocabulary and density (~13/1000; "I suspect", "we cannot rule out"); first-person I vs we; footnote load; re-glossing with "in other words"; coined-term reuse; passive ratio; sentence-length distribution. |

Three facts fall out of this map:

**The negative screen is exactly one quadrant** — universal, sentence-level, subtractive. That is why it deserves its own file and its own always-on status: it is the one quadrant that never changes and must bind even in chat.

**Organization is mostly universal, with a per-voice skeleton on top.** The habit of leading each paragraph with its claim is the same whether he is writing a memo or a paper. Which numbered section structure the piece uses is genre-specific. Do not put both in the same place: the universal organization habits belong in the base layer, the genre skeleton belongs in the per-voice model.

**"Should organization and style be separated?" — yes as concepts, no as files.** Label them as distinct sub-sections inside the base layer ("structure universals" and "sentence-craft universals") so the mental model stays visible, but do not spin up separate organization and style files. The boundary that earns a file is negative-vs-positive and universal-vs-per-voice. Splitting further multiplies files to maintain without buying a cleaner load rule.

---

## 3. Which is "better"

The honest answer is that they are different tools for different failure modes, so ranking them is like asking whether the spell-checker or the outline is more important. Both are load-bearing, and skipping either produces a recognizable defect: skip the screen and a tell leaks; skip the voice model and the prose is clean but faceless.

Forced to rank effort-to-payoff for the specific goal of sounding like *him*, the recommendation is unambiguous: **invest the marginal effort in the positive voice models.** Three reasons. The screen only clears a floor that many careful writers already clear, so it cannot, by construction, make text sound like one particular person. The screen is also nearly done — 14 named, greppable rules earned from his own red pen — and it is cheap to run as an always-on pass. The voice models are where the remaining upside sits, and they are where item 2's corpus work converts into signal. The screen is necessary but not sufficient; the ceiling is in the voice layer, and that is where to spend.

---

## 4. Target architecture

Four layers, each owning a disjoint slice, loaded in a fixed order. Every rule has exactly one canonical home; every other file that mentions it carries a one-line pointer, never a restatement.

**Layer 0 — Negative screen. `ai-tells.md`. Universal, subtractive.**
Owns the machine tells: the 14 tics plus the plain/dinner-table meta-test. Applies to everything, including chat and quick drafts. Voice-independent. A compressed copy lives always-on in `~/.claude/CLAUDE.md` so it binds without loading the full file.

**Layer 1 — Universal base. `appellate-style.md` (craft) + a small structure block. Universal, additive.**
Owns the positive rules that hold across all his expository writing regardless of genre, split into two labeled sub-sections:
- *Structure universals:* topic-sentence-first (lead every paragraph with its claim), lead with the finding, one idea per paragraph, roadmap and signposting, end-emphasis placement.
- *Sentence-craft universals:* vary sentence length, active voice with a named actor, strong verbs over nominalization, plain over Latinate words, one concrete image per abstraction.

`appellate-style.md` already *is* this layer for sentence craft — it is written as a universal supplement that any voice layers on. The structure universals currently buried in `style.md`'s Memo-Mode "Structure" and "Tufte" sections belong here too, hoisted out of Memo Mode so they are not mistaken for a memo-only rule.

**Layer 2 — Per-voice model. `style.md` Modes. Voice-specific, additive.**
Owns each fingerprint: Memo Mode, Academic Mode (General + Law + Economics + Biomedicine), and the future Substack/long-form-social and tweet profiles. Each profile specifies opening moves, hedge vocabulary and density, first-person I/we, footnote load, coined-term reuse, re-glossing, the genre section skeleton, passive ratio, and sentence-length distribution. This is the layer item 2 fills.

**Layer 3 — Output formatting. `style.md` formatting + docx/pptx specs + file versioning. Mechanical, not voice.**
Owns the python-docx spec, the pptx/MARP default, and the version-suffix rule. Keep it clearly separate from voice; it is about the rendered file, not the prose.

**Router.** A small dispatch selects the Layer 2 profile by artifact type: CMS memo → Memo Mode; NBER paper → Academic Economics; law review → Academic Law; Substack essay → long-form-social; tweet → tweet profile; ordinary chat → the compressed **briefing** voice bound in the always-on `CLAUDE.md` (memo's answer-first, mechanism-explaining spine, adapted to teach rather than compress) on top of Layer 0, with no full Layer 2 Mode. The briefing chat default replaced social-explainer on 2026-07-29; it is a chat register only and changes no artifact voice. Item 2 designs how the profiles are derived and stored; the router is only the selection step.

**Audience is a second routing axis (added 2026-07-26).** Artifact *form* usually implies *audience* for Anup's own writing — memos to policymakers, papers to peers, essays and explainers to a general reader — so form-only routing works for him. It fails when a project pairs an academic *form* with a general *audience*: a systematic review published as a public web resource, an empirical explainer for a lay reader. There, form-based routing sends the piece to the least accessible register (the fertility-review failure: an `academic-econ` route produced a chapter its "smart undergrad" target rejected). So the router takes a second input: when a project names a general-audience output or a reader standard (in its `CLAUDE.md`, a protocol, or a spec), audience **overrides** form and selects the accessible-but-rigorous blend (social-explainer primary + academic-econ for estimate conventions only, coin-and-reuse and theory-first suppressed). `write-as` Step 0 reads the project for this before routing; `voice-check` runs its dinner-table meta-test against the named reader, not the register, since a screen cannot catch a routing error made upstream of it. This axis also grounds three Layer 0 rules earned from the same failure — §21 clefts, §22 audience-conditional jargon, §23 insider reference.

**Load order at write time:**
1. Layer 0 (always, including chat — via the compressed block in CLAUDE.md, full file on a revision pass).
2. Layer 1 (any artifact; the most load-bearing universals — topic-sentence-first, plain/dinner-table — also sit in the always-on block for chat).
3. Router → the one Layer 2 profile for this artifact.
4. Layer 3 at export.

### Resolving the concrete overlaps

**Topic-sentence rule.** This is two rules wearing one name, and splitting them ends the duplication.
- The *negative* form — "do not write hollow topic sentences or scaffolding directives (Consider next…, Begin with…)" — is canonically `ai-tells.md` §13 (Layer 0).
- The *positive* form — "open every paragraph with the sentence that states its claim; first sentences read alone should carry the argument" — is canonically the Layer 1 structure block (currently appellate A4 and `style.md` Structure).
- Fix: keep the full negative rule only in ai-tells §13 and the full positive rule only in Layer 1. `style.md` Memo Mode's line 36 restatement shrinks to a pointer to the Layer 1 structure block. The CLAUDE.md always-on bullet stays as the compressed reminder and points to both.

**Ambiguous-antecedent rule.** Pure sentence-level style, and it is a tell, so it is negative. Canonical home: `ai-tells.md` §2 (Layer 0). `style.md` line 66 and appellate C5 shrink to one-line pointers to ai-tells §2 rather than restating the rule. (appellate C5 already cross-refs §2; just trim it to a pointer. `style.md` line 66 currently restates it in full; replace with the pointer.)

**General rule for one canonical home:**
- Negative, universal, sentence-level → `ai-tells.md` only.
- Positive, universal (structure or sentence craft) → Layer 1 only.
- Per-voice specifics → the relevant `style.md` Mode only.
- Every other appearance is a one-line cross-reference, never a restatement.

The existing "X, not Y" handling is the model to copy: `ai-tells.md` §1 owns the rule, and appellate B2's NOTE cross-refs it to explain why the "not to destroy them" clause form is permitted while the slogan form is banned. That is exactly the reference-not-restate discipline every other overlap should follow.

---

## 5. How item 2 plugs in

Item 2 derives empirical voice profiles from Anup's own corpora, and those profiles are Layer 2 content and nothing else. Item 2 does not touch Layer 0 (the screen is genre-independent) or Layer 1 (the universal craft is genre-independent). Its whole deliverable is to populate and refresh the per-voice models: replace the currently generic Memo Mode with a corpus-derived profile in the same schema Academic Mode already uses; add new Substack/long-form-social and tweet profiles; keep Academic Mode (already derived from 28 papers) as the schema template. The router then selects among them.

The combined picture item 2's designer plugs into:

```
   every artifact           ┌──────────────────────────────────────────────┐
   AND chat  ──────────────▶│  LAYER 0  ai-tells.md — negative screen       │  universal · subtractive
                            │  strip the 14 machine tells                   │  always on (compressed in CLAUDE.md)
                            └──────────────────────────────────────────────┘
                                              │ clears the machine floor
                                              ▼
   any artifact             ┌──────────────────────────────────────────────┐
             ──────────────▶│  LAYER 1  universal base                      │  universal · additive
                            │  appellate-style.md craft + structure block   │  topic-sentence-first, lead-with-finding,
                            │  (structure universals + sentence-craft       │  vary length, active voice, plain words
                            │   universals)                                 │
                            └──────────────────────────────────────────────┘
                                              │
                                     ROUTER (by artifact type)
              ┌───────────────┬───────────────┴───────────┬───────────────┐
              ▼               ▼                           ▼               ▼
        ┌──────────┐   ┌───────────────┐          ┌───────────────┐ ┌──────────┐
        │ Memo     │   │ Academic      │          │ Substack /    │ │ Tweet    │   LAYER 2 · per-voice
        │ Mode     │   │ (Law/Econ/Bio)│          │ long-form     │ │ profile  │   positive models
        └──────────┘   └───────────────┘          └───────────────┘ └──────────┘   ◀── item 2 fills these
              │               │                           │               │              (Academic already done,
              └───────────────┴─────────────┬─────────────┴───────────────┘               = the schema template)
                                            ▼
                            ┌──────────────────────────────────────────────┐
                            │  LAYER 3  output formatting                   │  mechanical
                            │  docx / pptx / file versioning                │
                            └──────────────────────────────────────────────┘
```

The frame item 2 hands its profiles to is Layer 2 plus the router. Each empirical profile is one Layer 2 box, written in the Academic-Mode schema (opening moves, hedge vocabulary and density, I/we, footnote load, re-gloss, coined terms, section skeleton, passive ratio, sentence-length distribution). The router maps artifact type to box. Layers 0 and 1 sit above every box unchanged, so item 2's designer can treat them as fixed and build only the per-voice content and the selection rule.

---

## Build punch list

Concrete edits that implement the architecture, smallest first:

1. **Trim the two duplicated rules to pointers.** `style.md` line 66 (antecedents) → pointer to `ai-tells.md` §2. `style.md` line 36 (topic sentence) → pointer to the Layer 1 structure block. appellate C5 → trim to a one-line pointer to `ai-tells.md` §2.
2. **Hoist the structure universals into Layer 1.** Move topic-sentence-first, lead-with-finding, one-idea-per-paragraph, and roadmap/signposting out of `style.md` Memo Mode into a labeled "structure universals" block in the base layer, so they read as universal rather than memo-only.
3. **Label the two sub-sections in Layer 1** — "structure universals" and "sentence-craft universals" — so the organization-vs-style distinction is visible without new files.
4. **Leave the always-on CLAUDE.md block as the compressed Layer 0 + the two or three most load-bearing Layer 1 universals** (topic-sentence-first, plain/dinner-table), each pointing to its canonical home.
5. **Item 2 writes into Layer 2 only:** corpus-derived Memo Mode replacing the generic one, plus new Substack/long-form-social and tweet profiles, all in the Academic-Mode schema, plus the router table.

---

## Related

- `~/.claude/refs/ai-tells.md` — Layer 0, the negative screen.
- `~/.claude/refs/appellate-style.md` — Layer 1, universal positive craft.
- `~/.claude/style.md` — Layer 2 per-voice Modes + Layer 3 formatting.
- `~/.claude/CLAUDE.md` — the always-on compressed block (Layer 0 + top Layer 1 universals).
- `handoffs/2026-07-06-writing-voice-rationalization.md` — the prior rationalization pass and the deferred empirical Memo Mode (item 2's blocking sub-step).
