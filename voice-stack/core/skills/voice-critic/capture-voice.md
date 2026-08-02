# Voice Capture — Auto-Extract Edit Pairs from This Session

This file is a sub-routine of voice-critic, not a standalone skill. It gets called at session end (by /mexit or manually) to extract before/after edit pairs from the current session and append them to the voice corpus.

## When to run

Run this routine when ALL of these are true:
1. The current session involved drafting work (tweets, memos, briefs, any AI-generated prose)
2. The user corrected the AI-generated prose (either by saying "change X to Y," providing a rewrite, rejecting a draft with a reason, or editing the text directly)
3. The corrections were about VOICE or TONE (not facts, not content additions, not formatting)

Do NOT run if:
- The session was purely research/exploration (no drafting)
- The only corrections were factual ("that number is wrong") or structural ("move this paragraph up")
- The user explicitly said "don't capture" or "skip voice capture"

## Steps

### 1. Scan the session for corrections

Look through the conversation for places where:
- Claude produced draft text (a tweet, a paragraph, a memo section, a thread)
- The user then modified it by:
  - Saying "change X to Y" or "rewrite this as..."
  - Providing their own version after rejecting Claude's
  - Editing the file directly (visible in subsequent Read calls showing different text)
  - Saying "no" to a draft and explaining why in voice/tone terms ("too academic," "sounds like a press release," "I'd never say it that way")

### 2. Extract candidate pairs

For each correction found, extract:
- **Before:** The AI-generated text (the specific sentence or phrase that was changed)
- **After:** The user's version (what they changed it to, or what they asked for)
- **Candidate pattern:** A one-line guess at what voice rule the correction reveals

Keep only corrections that are about VOICE — how something is said, not what is said. Skip:
- Factual corrections ("the number is 22% not 21%")
- Content additions ("also mention X")
- Structural moves ("put this before that")
- Formatting changes (bold, bullets, indentation)

### 3. Present candidates to the user

Show each candidate pair in this format:

```
Voice capture found N candidate edit pairs this session.

1. BEFORE: "[AI-generated text]"
   AFTER:  "[User's version]"
   PATTERN (suggested): [one-line pattern guess]
   → Add to corpus? [y/n/edit pattern]

2. BEFORE: "..."
   ...
```

Wait for user approval on each. The user can:
- **y** — approve as-is (append to corpus with suggested pattern)
- **n** — skip (don't add)
- **edit** — approve but rewrite the pattern note

Do NOT add anything without explicit approval. The corpus must stay high-signal.

### 4. Append approved pairs to corpus.md

For each approved pair, append to `~/.claude/skills/voice-critic/corpus.md` in the standard format:

```markdown

---

## Entry N

**Draft:**
> [before text]

**Rewrite:**
> [after text]

**Pattern:** [approved pattern note]
```

Increment the entry number based on what's already in the file. If corpus.md doesn't exist yet, create it with the first entry.

### 5. Report

Tell the user:
- How many candidates were found
- How many were approved and appended
- Current corpus size (total entries)
- Reminder: "thicker corpus = sharper critic — you'll see the difference next time you run /voice-critic"

## Integration with /mexit

When /mexit runs at session end, it should check whether drafting work happened in the session. If yes, run this capture routine before logging and exiting. The check is simple: did the session produce any draft text (tweets, memos, thread content) that the user subsequently modified?

If /mexit detects drafting but the user is in a hurry ("just log and exit"), skip the capture without complaint.
