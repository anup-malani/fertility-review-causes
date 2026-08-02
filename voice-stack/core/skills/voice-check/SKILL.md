---
name: voice-check
description: "Run the full after-draft screen on a finished or near-final draft: determine its register/voice, walk the ai-tells blocklist (Layer 0) with register-sensitive em-dash and rhetorical-question caps, run voice-critic conditioned on the target voice's exemplar bank, optionally run an AI-detector pass, then return a findings list and offer to apply fixes. Use when user says 'voice-check', 'check this draft', 'run the screen on this', 'final voice pass', 'does this sound like me and pass the tells', 'after-draft check', or '/voice-check'. Do NOT use for a voice-only pass with no tells screen (use /voice-critic), for the detector alone (use /not-ai), or before a draft exists (use the before-draft primer)."
argument-hint: "<path to draft file, or inline draft text> [voice: memo|academic-law|academic-econ|social-essay|social-explainer|appellate]"
metadata:
  author: anup
  version: 1.0.0
  related:
    - voice-critic
    - not-ai
---

# voice-check — the after-draft screen

> This is the after-draft half of the writing routine; `write-as` is the before-draft primer. The two names are final. It is an **orchestrator**: it composes the existing `voice-critic` and `not-ai` skills and adds the register-aware ai-tells pass on top. It does not reimplement either.

A finished draft can be factually right and structurally sound and still read as machine-written or off-voice. This skill runs the whole after-draft screen in one pass: the negative screen (are the AI tells absent, at the frequency this register allows?) and the positive target (does it sound like the author's own paragraphs in this register?).

## The stack it screens against

- **Layer 0 — negative screen:** `~/.claude/refs/ai-tells.md` (23 named tells + register-sensitive frequency caps for em-dash §9 and rhetorical questions §6 + a grep-net appendix + the plain/dinner-table meta-test).
- **Layer 1 — universal base:** `~/.claude/refs/appellate-style.md` (structure + sentence-craft universals; consult its CHECK lines when a finding is structural).
- **Layer 2 — per-voice positive target:** the exemplar bank at `~/.claude/refs/exemplars/<voice>.md` (its CORE paragraphs are what the draft should sound like).
- **Registry (built separately):** `~/.claude/refs/voice-registry.md` maps voice → exemplar bank + caps + Mode. If it exists, read it and let it override the inline table below. If it does not exist yet, use the inline table.

## When this skill fires

User says any of: "voice-check", "check this draft", "run the screen on this", "final voice pass", "does this sound like me and pass the tells", "after-draft check", "voice-check `<path>`", "/voice-check".

Distinguish from siblings: `/voice-critic` is the voice-only pass (this skill *calls* it); `/not-ai` is the detector alone (this skill *offers* it). voice-check is the full screen that runs both plus the register-aware tells pass.

## Argument

`$ARGUMENTS` is a path to the draft (markdown/text) or inline draft text, optionally with an explicit `voice:`. If no draft is obvious, ask which draft. If both a path and inline text are given, prefer the inline text and note the redundancy.

## Step 0 — Determine the register/voice

This choice sets which frequency caps apply and which exemplar bank is the positive target. It is the load-bearing first decision.

1. If the user named a voice (or the draft lives in a project whose CLAUDE.md fixes a Mode), use it.
2. Else infer from the artifact: a CMS/policy memo or briefing → `memo`; a law-review-style paper → `academic-law`; an economics paper (theory-then-empirics) → `academic-econ`; a narrative essay for a general audience → `social-essay`; a "what is X" teaching thread/post → `social-explainer`; a brief or opinion-style legal argument → `appellate`.
3. If inference is genuinely ambiguous (e.g., a hybrid memo/essay), state your best guess, name the alternative, and ask before proceeding. The caps differ enough (memo targets ~1/1k in drafting and bans the glyph at `.docx` export; social-essay allows ~3.9/1k) that guessing wrong misreports the draft.
4. **Determine the audience, not just the voice.** Check the project's `CLAUDE.md` and any protocol/spec for a named reader standard or a general-audience output (the same read `write-as` Step 0 does). Audience is a separate axis from voice: an academic *form* (systematic review, GRADE, pooled estimates) can target a general *reader* (a public web resource, a "smart undergrad" standard). When the project names a general audience, screen against the **accessible-but-rigorous blend** (social-explainer primary + academic-econ for estimate conventions only), and — load-bearing — run the Step 1c dinner-table test against that named reader, not the register. **A screen cannot catch a routing error made upstream of it:** if the draft was written to the wrong reader, every check here inherits that and ratifies it. If the detected audience looks wrong for the draft, say so and recommend re-routing via `write-as` before screening further.

### Register → caps + exemplar bank (inline table; registry overrides if present)

| Voice | Exemplar bank | Em-dash flag threshold | Rhetorical-question ceiling |
|---|---|---|---|
| `memo` | `exemplars/memo.md` | ~1 / 1,000 words drafting (low, like academic); at `.docx` export the glyph is banned and auto-converted to `--`/`---`. The current memo corpus runs ≈7–9/1k, but it postdates AI adoption — do not emulate that density | Rare. ≤1 per section, and only when the answer is genuinely the reader's. Prefer a colon-led list or a "The question we address is…" declarative. |
| `academic-law` | `exemplars/academic-law.md` | ~1.4 / 1,000 words | Rare; ≤1 per section. |
| `academic-econ` | `exemplars/academic-econ.md` | ~1 / 1,000 words (runs lower than law) | Rare; ≤1 per section. |
| `social-essay` | `exemplars/social-essay.md` | ~3.9 / 1,000 words (his hottest register; the old ~1.3 was a `---`-convention undercount) | A few per piece OK (his teaching voice). No successive-paragraph openers; never stack. |
| `social-explainer` | `exemplars/social-explainer.md` | ~1.4 / 1,000 words (old ~0.4 was the same undercount) | A few per piece OK. No successive-paragraph openers; never stack. |
| `appellate` | `exemplars/appellate.md` | ~1 / 1,000 words | ≤1 per section; only when the answer is the reader's to supply. |

These are flag thresholds set to Anup's own corpus rate, not hard targets. **Nothing he writes runs above ~3.9/1k — that is the hard ceiling for every register.** Measure the rate counting "—", " -- ", AND "---" (the triple-hyphen is how his exported prose renders the dash; missing it undercounts ~3x). The tell is running **well above** the threshold, stacking two dashes in one sentence, or a reflexive pause several times a page. One dash in a permissive register is fine.

## Step 1 — Layer 0 ai-tells CHECK pass (register-aware)

Read `~/.claude/refs/ai-tells.md`, then run these three things in order.

**1a. Mechanical density triage (grep + arithmetic).** Word-count the draft and compute the frequency-capped counts:
```
wc -w <draft>                         # N words
grep -v '^#' <draft> | grep -o "—" | wc -l           # em-dash count (markdown headers excluded)
grep -v '^#' <draft> | grep -o -- "--" | wc -l       # double-hyphen count (models' ASCII em-dash), headers excluded
```
Markdown header lines (^#) are excluded from the em-dash and double-hyphen counts so section-title dashes don't inflate the rate. Em-dash rate = (em-dash + double-hyphen) / N × 1000. Compare to the register's threshold above. For rhetorical questions, count only the *rhetorical* "?" (not genuine reader-answered ones) and check against the ceiling — per section for formal registers, per piece plus no-successive-openers for social. Then run the grep-net appendix as a density net (`delve`, `tapestry`, `testament`, `underscore(s)`, `boast(s)`, `showcase`, `pivotal`, `seamless`, `leverage`-as-verb, `realm`, `landscape`, `garner`, `harness`-as-verb, `empower`, `poised`, `supercharge`, `commendable`, `burgeoning`, `revolutionize`, etc.). Two or more hits in one paragraph means slow down and apply the rules there — do not just swap a synonym. Also grep the §14 emphatic-intensifier constructions (`exactly what`, `is exactly`, `are exactly`, `precisely what`, `the very`, `what no one`). Treat these as **flag for function-review, not synonym-swap**: on each hit apply the §14 function test (delete the intensifier; keep it only if it carried a literal or measured precision, such as an equality, a measured quantity, or a pointer to one specific referent), because Anup uses the same strings legitimately. Also grep `ran the test` for the §20 definite-article overuse — same flag-for-function-review footing: ask whether a specific test is already in view; if not, write "a test" or name it. The general "the"-for-"a" pattern cannot be grepped (`the` is the commonest word in English), so catch it by reading during the 1b walk. Grep the §21 cleft/fronted net (`is what`, `are what`, `was what`, `were what`, `^What `, `. What `) — flag-for-review, and weight topic-sentence position heavily (a cleft opening a paragraph is a tell regardless of the whole-document rate). For a general-audience draft, also read for §22 unglossed coined jargon and grep collaborator first names for §23 insider reference.

**1b. Walk the 23 rules' CHECK lines, paragraph by paragraph.** Use each rule's own CHECK line from `ai-tells.md`. The quick index: §1 "X, not Y" antithesis (slogan/fragment/reflexive beat — banned; full clause with a real fact — allowed); §2 ambiguous antecedents; §3 bare-noun/mystery-hook openers; §4 staccato runs (3+ short in a row); §5 anaphora; **§6 rhetorical-question cap (register-sensitive, from the table)**; §7 tricolon-for-cadence; §8 decorative connectives (moreover/furthermore); **§9 em-dash cap (register-sensitive, from the table)**; §10 metaphor-as-structure; §11 sales verbs; §12 clever/allusive ellipsis endings; §13 hollow topic sentences / scaffolding directives; §14 throat-clearing hedges and intensifiers; §15 sycophancy / manufactured enthusiasm; §16 rigid three-part enumeration + restating wrap-up; §17 significance inflation; §18 copula avoidance (serves as / boasts / represents); §19 vague unnamed attribution ("studies show"); §20 definite-article overuse ("the" where "a" belongs — function-test a definite article that introduces a referent the text has not established); §21 fronted/cleft constructions (flag-for-review, worst in a topic sentence); §22 unglossed coined jargon (audience-conditional — fires only for a general reader); §23 insider reference (teammate names, unrun methodology, co-author asides in reader-facing prose). Apply §6 and §9 by the register's numbers from the table, not a blanket ban.

**1c. Plain / dinner-table meta-test — against the named reader, not the register.** For any sentence that performs (rhetorical inversion, decorative parallel, ornamental metaphor, "what is striking" / "in other words" tics), flag it: would he say this to a smart non-expert across a dinner table? If not, say it plainly. **Run this against the project's actual reader standard from Step 0, not against the register.** "Would a smart undergrad understand this on one pass" is a different question from "does this sound like an economics paper," and it is the one check that catches a wrong-audience draft — the failure every register-conditioned check above will miss, because it was baked in before drafting. When the audience is general, apply §22 (gloss coined jargon) and §23 (no insider reference) here too.

For a long draft, this pass can run inline or be handed to a `sonnet` subagent whose task is exactly steps 1a–1c against `ai-tells.md`; return its findings into the consolidated list.

## Step 1.5 — Measurement gates (counting, not prose)

Two defects are caught by counting, not by the tells walk. Both are a few lines of Python, no model call, and belong in the loop for any **rewrite** (skip for an original draft with no source).

**Verbatim overlap against the source.** A "rewrite from scratch" instruction silently degrades into a light edit when the source prose is already good — and the better the source, the more the model copies (measured: a hand-edited source came back 50.8% copied, and it *passed* the tells screen because it had inherited already-clean sentences). The screen cannot tell prose the model wrote from prose it copied, so measure it. On body-prose sentences of eight or more words, excluding quotations, table cells, and reference entries, compute the fraction of draft sentences that appear verbatim or near-verbatim in the source. Flag anything above a few percent for a genuine "from scratch" rewrite, and report the number in the findings header.

**Cleft density (§21).** Count the §21 net hits per 1,000 words, and separately flag every cleft that opens a paragraph. Position outranks density: report both, but a topic-sentence cleft is a finding even at an acceptable overall rate.

Both are computed by a ready tool, no model call: `python3 ~/.claude/skills/voice-check/voice-metrics.py both <draft> <source>` (verbatim-overlap + cleft density), or `clefts <draft>` when there is no source. It reports the overlap %, the cleft rate, and every paragraph-opening cleft. Fold the numbers into the findings header.

## Step 2 — voice-critic, conditioned on the target voice's exemplar bank

Invoke `/voice-critic` on the draft. It runs its own red-pen corpus pass (the 19 empirical before/after pairs in `corpus.md`). **Supplement it with the target voice's exemplar bank CORE paragraphs as the positive imitation target** — this is exactly the extension `voice-critic`'s own SKILL.md already contemplates (see its "Related empirical voice guide" note, which supplements the critic with a voice-specific guide). Concretely: read `~/.claude/refs/exemplars/<voice>.md`, extract its CORE section (5 paragraphs, one per archetype; for `appellate`, the RECOMMENDED 5), and give those to the critic as the "does the draft sound like these?" target alongside the red-pen corpus. Do not reimplement voice-critic; call it and hand it the CORE paragraphs as supplement. Surface its structured output (violations, rewrites, confidence note) verbatim into the findings.

## Step 3 (optional) — not-ai detector pass

Offer `/not-ai` as a cross-check. It is opt-in by design (not automatic in this screen) because it hits a paid detector API (Pangram/GPTZero) and only proves the text is not machine-*flagged*, which is a different claim from "sounds like Anup." Run it when the user asks, when a `PANGRAM_API_KEY`/`GPTZERO_API_KEY` is set and the draft is high-stakes (a paper or public essay), or when the tells pass and voice-critic disagree and a third signal would help. Fold its score and any residual flagged spans into the findings; note if it was critic-only (no key).

## Step 4 — Return findings, then offer to apply

Assemble one consolidated list. Header line first: the detected voice, **the audience it was screened for**, word count, measured em-dash rate vs. the register threshold, rhetorical-question count vs. ceiling, and (for a rewrite) the verbatim-overlap percentage. Naming the audience in the header makes a wrong one visible before the findings rather than never. Then group findings:

- **A. AI-tells screen** — each finding as: `[§N rule name] "offending text" → suggested fix`.
- **B. Voice-critic** — its verbatim output (violations, rewrites, confidence).
- **C. Detector** — score + residual flagged spans, or "not run (opt-in)".

Then **ask before applying**: "Apply these fixes to the draft? I can edit in place and show you the diff, or hand you the list to apply yourself." Do not edit the draft until the user says yes. When applying, change phrasing only — never a claim, number, date, name, caveat, or a verbatim quotation (real quotes/data/citations are exempt from the detector, per `not-ai`). Re-run steps 1–2 on the edited draft if the user wants confirmation; each pass is independent.

**Sweep, do not spot-fix.** When the draft is one of several sibling files (book chapters, review chapters, a doc set), a defect found in it almost certainly recurs in the siblings — one cleft problem found in one chapter was shipped in three others, one of which was the chapter the author actually read. Before any of them ship, sweep the confirmed defect across every sibling and say explicitly which siblings you checked.

## Hard NOs

- Do not apply a blanket em-dash or rhetorical-question ban. The cap is register-sensitive; memo is strict, social/academic/appellate allow the author's own low rate. Misapplying the memo ban to an essay is itself a failure.
- Do not reimplement `voice-critic` or `not-ai`. Compose them.
- Do not edit the draft before the user approves.
- Do not change content — phrasing only. If a flagged sentence cannot be fixed without touching substance, leave it and flag it for the author.
- Do not flatter the draft. "Clean, nothing to flag" is the right answer when true; harmful when false.
- Do not build or edit the router or the registry — that is the sibling skill's job. This skill only *reads* `voice-registry.md` when present.
- Do not trust the screen to catch a wrong-audience draft. Only the dinner-table test conditioned on the true reader (Step 1c) can; if the audience is uncertain, resolve it — or re-route via `write-as` — before screening, because every register-conditioned check ratifies the register it was handed.

## Related

- `/voice-critic` — the voice-only red-pen pass this skill calls (Step 2).
- `/not-ai` — the detector loop this skill offers (Step 3).
- `~/.claude/refs/ai-tells.md` — Layer 0 negative screen (Step 1).
- `~/.claude/refs/appellate-style.md` — Layer 1 structure/craft universals.
- `~/.claude/refs/exemplars/<voice>.md` — Layer 2 positive target per voice.
- `~/.claude/refs/voice-registry.md` — voice → bank + caps map (built separately; read if present).
