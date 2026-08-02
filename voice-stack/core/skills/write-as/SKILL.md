---
name: write-as
description: "Select the author's writing voice for an artifact and load its full voice stack BEFORE drafting, so the draft is conditioned on the right register from the first sentence. This is the voice router + the before-draft conditioning pass. Use when the user says 'write this as a memo / essay / paper', 'draft in my <voice> voice', 'write this in my memo/academic/appellate register', '/write-as <voice>', or asks for any written artifact where the register matters. Do NOT use for the after-draft screen of an existing draft (that is /voice-check or /voice-critic) or for ordinary chat with no artifact."
argument-hint: "<voice name or artifact type> — e.g. 'memo', 'academic-econ', 'essay about X'"
metadata:
  author: anup
  version: 0.1.0
  related:
    - voice-critic
  reads:
    - ~/.claude/refs/voice-registry.md
    - ~/.claude/refs/ai-tells.md
    - ~/.claude/refs/appellate-style.md
    - ~/.claude/style.md
---

# write-as — Voice Router + Before-Draft Conditioning

Drafting first and fixing voice afterward is backwards: the register has to be in context before the
first sentence, or the draft inherits the model's default voice and every later pass fights it. This
skill runs before drafting. It picks the author's voice for the artifact and loads the voice stack in
order, so the draft is conditioned on the right register, exemplars, and rules from the start. The
router lives inside this skill by design; there is no standalone selector. A sibling after-draft skill
(`voice-check`) handles the critique of a finished draft; this one owns the setup.

The data this skill runs on lives in `~/.claude/refs/voice-registry.md` — the six voices, their
exemplar-bank paths, their style.md Modes, their triggers, and their register caps. Read the registry
first every time; it is the source of truth and it changes as the system is tuned.

## When this skill fires

- "write this as a memo / essay / paper / brief"
- "draft in my <voice> voice" / "write this in my memo (or academic / appellate) register"
- "/write-as <voice>"
- any request to produce a written artifact where the register matters (a CMS memo, a law-review or
  economics paper, a Substack essay or explainer, an op-ed) and the voice has not already been loaded

Do NOT fire for: the after-draft screen of an existing draft (that is `/voice-check`, or `/voice-critic`
for a voice-only pass); ordinary chat with no artifact (Layer 0 is already always-on via `CLAUDE.md`,
nothing to load).

## Step 0 — Read the project for audience

Before inferring a voice from artifact form, check the working project for a stated audience — the input
the router otherwise never sees. Form usually implies audience for Anup's own writing, so this is often a
quick confirm; it earns its keep when a project has an academic form but a general reader.

Check two places:
- the project's `CLAUDE.md` (or `README`) for publication targets or intended audience — e.g. "living
  web resource (primary); book monograph (secondary)";
- any protocol or spec for a readability gate, an audience standard, or a named target reader — e.g. a
  stage that says "flag any passage that doesn't make sense to a smart undergrad."

When the project names a general-audience output or a specific reader standard, that **overrides** the
form-based inference in Step 1. "Systematic-review chapter" and "public explainer for a smart undergrad"
are different registers, and only the first reaches a form-based router. Absent any such signal, fall
back to form (the common case). Carry the detected audience into Step 1 and name it in the routing line.

## Step 1 — Route to a voice

Read `~/.claude/refs/voice-registry.md`, then select one voice by this precedence:

0. **Audience override (from Step 0).** If the project names a general audience for what would otherwise
   be an academic form, audience wins over form: route the **accessible-but-rigorous blend** —
   `social-explainer` primary, `academic-econ` consulted only for estimate-reporting conventions, its
   "coin and reuse" and "theory before empirics" **suppressed** (registry "Accessible-but-rigorous" edge
   case). An explicit user command still wins over this.
1. **Explicit command wins.** If the user names a voice (`memo`, `academic-law`, `academic-econ`,
   `social-essay`, `social-explainer`, `appellate`) or says "write this as a <type>", take that voice.
   A bare `/write-as memo` or "in my appellate register" is explicit. `appellate` fires **only** this
   way — never by inference.
2. **Else infer from artifact type** using the registry's "fires for" column: CMS/policy memo →
   `memo`; law review / legal scholarship → `academic-law`; economics journal / NBER paper →
   `academic-econ`; Substack essay / op-ed / long-form argument → `social-essay`; teaching or explainer
   post that builds a concept → `social-explainer`.
3. **Else ask.** When the artifact type is genuinely ambiguous, ask one question and stop:
   - "a paper" with no field → law or economics?
   - "a post" that could be argument or teaching → essay (make an argument) or explainer (build a
     concept from primitives)?
   - anything you cannot map to a row → name the closest two and ask.
4. **No artifact in play** (ordinary chat) → do not load Layer 2. The always-on Layer 0 in `CLAUDE.md`
   already governs. Stop here.

Handle the edge cases per the registry's "Edge cases and fallbacks" section: general-academic with no
clear field (ask, or default econ for empirical / law for doctrinal); biomedicine (route to
`academic-econ` bank + the Biomedicine Mode, expect a translation step); hybrid essay/explainer
(pick the primary job; optionally add one on-point EXTENDED paragraph from the other); accessible-but-rigorous
(quantitative work for a general audience → `social-explainer` primary + `academic-econ` for estimate
conventions only, coin-and-reuse and theory-first suppressed).

State the selected voice **and the detected audience** in one line before loading, e.g. "Routing to
**memo** voice (CMS policy register), audience: agency decision-makers." or "Routing to
**social-explainer** (project names a living web resource; protocol sets the bar at 'smart undergrad')."
so the user can override a wrong voice or a wrong audience before drafting starts.

## Step 2 — Load the stack in order

Load, in this order, for the selected voice. Layers 0 and 1 are the same for every voice; Layer 2 is
what the router selected.

1. **Layer 0 — negative screen.** The compressed blocklist in `~/.claude/CLAUDE.md` is already on. Read
   the full `~/.claude/refs/ai-tells.md` so the 23 tells and the §6/§9 caps (including the §22 audience
   rule) are in context for drafting, not just for a later revision pass.
2. **Layer 1 — universal base.** Read `~/.claude/refs/appellate-style.md` (structure universals +
   sentence-craft universals). This is the positive craft that holds across every voice.
3. **Layer 2 — the per-voice bundle.** Two parts, both from the registry row:
   - **The style.md Mode.** If the row names one (`## Memo Mode`, `## Academic Mode (Law)`,
     `## Academic Mode (Economics)`), read that section of `~/.claude/style.md`. If the row says
     "none yet" (`social-essay`, `social-explainer`), skip it — the bank carries the signal. For
     `appellate`, there is no Mode; `appellate-style.md` from Layer 1 is the craft base, and its
     "Conflicts to reconcile" and "Do NOT transfer" sections are load-bearing for this register.
   - **The exemplar-bank CORE set, injected verbatim.** Read the exemplar bank at the registry path and
     hold its **CORE** paragraphs (for `appellate`, the **RECOMMENDED 5**) in context as models to
     imitate — for cadence, diction, and the archetypal move each one teaches, not for their content.
     These are imitation targets, not source material to quote.

Default to injecting the **CORE** set. Pull an **EXTENDED** (or `appellate` **ALTERNATE**) paragraph on
demand when the task matches an archetype the CORE set does not cover — the bank's per-paragraph
"Move"/"Anchor" note says what each teaches. The exact per-voice CORE-vs-EXTENDED mix is being A/B-tuned
(registry task #8); until that lands, CORE is the default.

## Step 3 — Draft in the voice

Draft with the whole stack live:

- The **exemplars** are the cadence and diction target — imitate the move, not the words.
- The **Mode** (where one exists) gives the register's rules: opening moves, hedge vocabulary and
  density, first-person I vs we, footnote load, section skeleton, re-glossing, coined-term reuse.
- The **ai-tells screen** stays on underneath the whole time. Honor the **register cap** for the
  selected voice from the registry: memo is strict (em-dashes effectively zero, rhetorical questions
  rare); academic / social / appellate allow about one em-dash per 1,000 words and register-appropriate
  rhetorical questions. The tell is density and pile-ups, not a single instance.
- The **plain / dinner-table test** is the meta-check for every voice: would you say this sentence to a
  smart non-expert across a table? If it performs, say it plainly.

Do not narrate the layers to the user while drafting. Load them, then write.

## Step 4 — Hand off to the after-draft pass (optional)

When the draft is done, **`/voice-check`** runs the full after-draft screen (Layer 0 tells with the
register caps, plus a voice-critic pass) against the same voice this router selected; `/voice-critic`
alone runs a voice-only pass. Name the selected voice in the handoff so the screen targets the right
register. Do not run the after-draft screen from here — it is a separate skill.

## Hard NOs

- Do not draft before loading the stack. The whole point is to condition the draft up front.
- Do not load Layer 2 for ordinary chat. No artifact → Layer 0 only.
- Do not fire `appellate` by inference. It is explicit-request-only, and it is aspirational (Roberts /
  Sutton), not the author's own voice.
- Do not inject from the retired parent banks (`exemplars/academic.md`, `exemplars/social.md`). They are
  provenance-only; use the register-specific banks the registry points to.
- Do not paraphrase or summarize the exemplars into "rules." They work by being present verbatim as
  imitation targets; a summary loses the cadence, which is the signal.
- Do not treat exemplar content as source material. Imitate the move; write the artifact's own content.

## Related

- `~/.claude/refs/voice-registry.md` — the router's data table (read this first, every time).
- `~/.claude/refs/voice-architecture-strategy.md` — the full four-layer design.
- `~/.claude/refs/ai-tells.md` (Layer 0), `~/.claude/refs/appellate-style.md` (Layer 1),
  `~/.claude/style.md` (Layer 2 Modes + Layer 3 formatting).
- `/voice-check` (full after-draft screen) and `/voice-critic` (voice-only pass) — the critique passes
  that run after drafting, against the voice this router selected.
</content>
