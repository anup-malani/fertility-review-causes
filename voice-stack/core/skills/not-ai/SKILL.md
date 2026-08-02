---
name: not-ai
description: "Run a draft through a top AI-writing detector, then rewrite only the flagged spans to sound human (specifically, to sound like the author) without changing content — looping detect→rewrite until it passes. Use when user says 'run not-ai', 'de-AI this', 'make this not sound like AI', 'AI-detector pass', or after writing/revising any chapter prose. Built for the Slums book chapter-recipe pipeline (apply at first draft and every revision). Do NOT use to launder real interview quotes, data, or citations — those are exempt."
argument-hint: "<path to draft file> [--threshold 0.5] [--provider pangram|gptzero]"
metadata:
  author: anup
  version: 1.0.0
  related:
    - voice-critic
    - editorial-committee
---

# not-AI — detect, then de-AI without changing content

A drafting pipeline can pass every content and style check and still *read* like a model wrote it. Readers (and reviewers) increasingly run prose through AI detectors, and the author's standing rule is blunt: **"People do NOT want to buy AI-written papers."** This skill closes that gap with a measured loop: run the draft through a real AI-writing detector, take the *specific* sentences it flags, rewrite only those to sound like the author, and repeat until the draft passes — without changing a single claim, number, quote, or citation.

This is the **not-AI pass** referenced in `CHAPTER-RECIPE` (A6 first draft; B5 every revision).

## When this skill fires

User says any of: "run not-ai", "de-AI this", "make this not sound like AI", "AI-detector pass", "not-ai <path>" — or any chapter prose draft/revision has just been assembled (the recipe calls it automatically at A6 and B5).

## Argument

`$ARGUMENTS` is a path to the draft (markdown/text), optionally with `--threshold` / `--provider`. If no path is obvious, ask which draft.

## The detector (step 1 — already chosen)

**Primary: Pangram.** The most accurate detector in independent 2026 testing (validated by a University of Chicago study; false-positive rate ≤ 0.005 at high recall), with per-segment highlighting and a developer API. Endpoint `POST https://text.external-api.pangram.com/task` then poll `GET /task/{task_id}`, header `x-api-key`. Returns `fraction_human` / `fraction_ai` / `fraction_ai_assisted` plus a `windows[]` array (each with `text`, `label`, `ai_assistance_score`). The skill scores overall AI-likelihood as **`1 − fraction_human`** so AI-*assisted* prose is caught, not just fully-AI text, and flags the individual windows.

**Free fallback: GPTZero.** Near-Pangram accuracy, **synchronous** API with a free tier, returns `sentences[].highlight_sentence_for_ai` + `generated_prob`. Endpoint `POST https://api.gptzero.me/v2/predict/text`.

Set one key and the runner picks it automatically (Pangram preferred):
```
export PANGRAM_API_KEY=...        # get one at app/dashboard on pangram.com
# or
export GPTZERO_API_KEY=...        # https://app.gptzero.me/app/api  (free tier)
```

## The loop

Run from `~/.claude/skills/not-ai/`:

1. **Detect.** `python3 detect.py <draft> --json`
   - Prints the overall AI score and the list of flagged sentences (with per-sentence scores). Exit 0 = PASS, 1 = FAIL (flags remain), 2 = config/network error.
2. **Rewrite the flagged spans only.** For each flagged sentence, rewrite it to read like the author — conditioned on `~/.claude/refs/ai-tells.md` (the canonical AI-tell blocklist), the project-local `STYLE-GUIDE.md` §3 where one exists, and the voice anchor (the Kenya cartels narrative essay). Change phrasing, never substance. Leave every *un*flagged sentence untouched (surgical-convergence rule).
3. **Re-detect.** Run `detect.py` again on the rewritten draft.
4. **Repeat** until PASS or the iteration cap (default **3**). If it still fails after 3 rounds, **stop** and surface the residual flagged sentences for human judgment — do not loop forever, and do not keep mangling a sentence just to drop its score.

## Guardrails (these override "make it pass")

1. **Never change content.** No claim added or dropped, no number/date/name altered, no caveat lost. The rewrite is phrasing only. If a flagged sentence cannot be rewritten without touching substance, leave it and flag it for the author.
2. **Real quotes, data, and citations are exempt.** Verbatim interview quotes are *human speech* — never launder them, even if a detector flags them. Same for quoted statistics and bibliographic citations. Exclude these from the rewrite set; if they dominate the flags, the draft likely already passes on the prose that matters.
3. **Sound like Anup, not just "not like AI."** The target is the author's real voice (anchor: his slums essays), not detector-evasion text. A sentence that beats the detector but fails the **plain / dinner-table test** (`STYLE-GUIDE.md` §6) is not done. Voice and plainness win ties over the score.
4. **Calibrate the threshold against real human prose.** Before trusting a number, run the author's own Kenya cartels essay through `detect.py` once. Whatever genuine Anup prose scores is the floor — set `--threshold` at or just above it. Chasing 0.00 is wrong; even human writing scores nonzero.
5. **Bounded effort.** Cap at 3 detect→rewrite rounds per draft. Diminishing returns past that mean the problem is structural, not sentence-level — kick it to the author or the editorial committee.

## Fallbacks when no API key is set

- **Browser (no key, programmatic):** use the Claude-in-Chrome tools to paste the draft into the Pangram or GPTZero web UI and read the highlighted sentences back. Same loop, manual detector call.
- **LLM-critic (offline):** run an internal critic conditioned on `~/.claude/refs/ai-tells.md` (canonical blocklist), plus the project-local `STYLE-GUIDE.md` §3 where one exists, that flags AI-tell spans (staccato, parallelism-for-effect, "It's not X; it's Y", decorative connectives, em-dash pile-ups, hollow topic sentences). Less authoritative than a real detector — note in the handoff that the pass was critic-only, not detector-verified.

## Integration with the chapter recipe

- **A6 (first prose draft):** run the loop on `ch{N}-…-PROSE-v1.md` before handing it to the author.
- **B5 (assemble & ship):** run the loop on the assembled `vN+1` after the seam check, before writing the clean file and the `-am` copy.
- Record the final score in the `session-log.md` entry so we can see de-AI trend across versions.

## Cost

Pangram API ≈ $0.05 / 1,000 words → a ~9,000-word chapter ≈ $0.45 per scan; 3 rounds ≈ ~$1.35/chapter. GPTZero free tier covers lighter use. Negligible against the value of not shipping AI-tell prose.

## Open question carried to the author

In `CHAPTER-RECIPE` B3, this automated pass partly substitutes for the old voice/de-AI editor's mechanical job — but a detector only proves text *isn't* machine-flagged; it doesn't prove the prose sounds like *you*. The recipe currently keeps a narrowed "sound-like-Anup" voice editor alongside this skill. Confirm that split or collapse it.
