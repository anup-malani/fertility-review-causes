# Make it your voice (or someone else's)

The architecture in this package is generic; the *voice* is Anup's. To retarget it, you swap the
personal layer and leave the generic layer alone. The whole point of the design is that this is a
file swap, not a rebuild. Budget about ten minutes for a first pass and an hour to do it well.

## The one required swap: the exemplar banks

`voice/exemplars/*.md` is the voice. Each file is a bank of paragraphs from the author's own writing
in one register (`memo`, `academic-econ`, `academic-law`, `social-essay`, `social-explainer`,
`appellate`). The agent imitates their **cadence and moves** — not their content — when it drafts.

Replace the contents of each bank you care about with your own writing:

1. Open `voice/exemplars/memo.md` (or whichever register you write in). Look at its **CORE** section:
   five paragraphs, each tagged with the *move* it teaches (a recommendation-first opener, a crisp
   two-part partition, a mechanism-first argument, and so on).
2. Find five paragraphs of **your own** best writing in that register — ideally one that shows each
   of those moves. Paste them in verbatim, replacing Anup's. Keep the "Move:" annotation under each,
   rewritten to say what your paragraph demonstrates.
3. Delete Anup's paragraphs you replaced. If you have no paragraph for a given move, drop that CORE
   slot rather than inventing one — a smaller honest bank beats a padded one.
4. Repeat for each register you use. You do not need all six; unused banks can stay as Anup's or be
   deleted.

That is the substitution Anup described: "modify exemplar, substitute your own writing, and you have
your writing layer."

## Secondary swaps (optional, higher fidelity)

- **`core/skills/voice-critic/corpus.md`** — the before/after edit pairs the critic learns your taste
  from. Anup's are his red-pen edits. Start empty and add your own as you correct drafts, or paste a
  handful you already have. `example-corpus.md` in the same folder is the template.
- **Register caps.** `core/refs/ai-tells.md` §9 (em-dash rate) and the per-voice caps in
  `core/refs/voice-registry.md` are Anup's corpus numbers. They are conservative and safe to keep. If
  your natural rate differs, retune those two spots; nothing else depends on the numbers.
- **The style.md Modes.** `core/style.md` describes Anup's memo and academic registers, derived from
  his corpus. If your structure differs materially, edit the relevant `## ... Mode` section. For a
  first pass, the exemplar swap alone carries most of the signal — leave the Modes until you see the
  drafts drift.
- **Name and pronouns.** `AGENTS.md` says "Anup" and "he" in the chat block. Change them to yours.
- **Grill-me (not included in this package).** Anup's full private system has a `grill-me` skill
  that interactively sharpens the tell rules against your own edits over time. It's a maintainer
  tool and isn't part of this RA build — skip any reference to it you see elsewhere; nothing here
  depends on it.

## What you must NOT touch

Two layers are register-neutral — they remove machine-ness and add universal craft, and they are the
same for every writer:

- **`core/refs/ai-tells.md`** (the tell rules themselves, as opposed to the §9 rate numbers). These
  are the 23 machine tics; they are bad in anyone's writing.
- **`core/refs/appellate-style.md`** (universal structure and sentence craft).

Leave both as shipped. Editing them is not personalizing your voice; it is degrading the base.

## Deriving a bank from a corpus, properly

Hand-picking five paragraphs works. If you want the rigorous version — score a corpus of your writing,
rank paragraphs by how authentically they carry each move, and weight toward pre-AI drafts — that
derivation pipeline lives with the voice system's maintainer (Anup's `research-manager` style-analysis
project), not in this package. Ask for it if a hand build is not enough.

## After you swap

Re-copy `AGENTS.md` to your repo root (if you changed it), then draft a throwaway artifact in one
register and read it against your own ear. If it sounds like a
generic-but-clean writer rather than *you*, your exemplar bank is too thin or too polished — add
paragraphs that show more of your idiosyncratic moves.
