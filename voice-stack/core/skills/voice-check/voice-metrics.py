#!/usr/bin/env python3
"""voice-metrics.py — deterministic gates for voice-check Step 1.5.

Two measurements, NO model call, stdlib only:

  overlap  <draft> <source>   Verbatim / near-verbatim sentence overlap of a
                              "rewrite from scratch" draft against its source.
                              A high number means the model copied rather than
                              rewrote; the tells screen cannot see this, because
                              copied sentences may already pass the tells.

  clefts   <draft>            §21 fronted/cleft density per 1,000 words, plus a
                              list of clefts that OPEN a paragraph. Position
                              outranks density: a topic-sentence cleft is a
                              finding even at an acceptable overall rate.

Usage:
  python3 voice-metrics.py overlap DRAFT.md SOURCE.md
  python3 voice-metrics.py clefts  DRAFT.md
  python3 voice-metrics.py both    DRAFT.md SOURCE.md

Body prose only: fenced code, markdown headers, blockquotes, tables, and
horizontal rules are stripped; quotations are excluded from the overlap count.
Heuristic and deliberately conservative — it triages, it does not adjudicate.
"""
import re
import sys
import argparse
from difflib import SequenceMatcher

# §21 cleft / fronted net (mirrors ai-tells.md §21 and the grep-net appendix)
CLEFT_PATTERNS = [
    (r'\bis what\b', 'is what'),
    (r'\bare what\b', 'are what'),
    (r'\bwas what\b', 'was what'),
    (r'\bwere what\b', 'were what'),
    (r'^\s*What\s', '^What'),
    (r'\.\s+What\s', '. What'),
]


def strip_to_prose(text):
    """Return (prose_text, paragraphs). Drops code, headers, tables, rules, blockquotes."""
    out, in_code = [], False
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith('```') or s.startswith('~~~'):
            in_code = not in_code
            continue
        if in_code:
            continue
        if s.startswith('#'):                       # markdown header
            continue
        if s.startswith('>'):                       # blockquote
            continue
        if s.startswith('|'):                       # table row
            continue
        if re.match(r'^[\s|:_-]+$', s) and s:        # horizontal rule / table divider
            continue
        if re.match(r'^\[\d+\]', s):                # bracketed reference entry
            continue
        out.append(ln)
    prose = '\n'.join(out)
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', prose) if p.strip()]
    return prose, paragraphs


def split_sentences(text):
    text = re.sub(r'\s+', ' ', text).strip()
    parts = re.split(r'(?<=[.!?])\s+(?=[A-Z"“‘\'])', text)
    return [p.strip() for p in parts if p.strip()]


def normalize(s):
    s = s.lower()
    s = re.sub(r'[^a-z0-9 ]', '', s)
    return re.sub(r'\s+', ' ', s).strip()


def word_count(text):
    return len(re.findall(r"\b[\w'-]+\b", text))


def has_quote(s):
    return any(q in s for q in ('"', '“', '”'))


def overlap(draft_path, source_path, min_words=8, near=0.90):
    draft = open(draft_path, encoding='utf-8').read()
    source = open(source_path, encoding='utf-8').read()
    d_prose, _ = strip_to_prose(draft)
    s_prose, _ = strip_to_prose(source)

    src = [normalize(x) for x in split_sentences(s_prose)]
    src = [n for n in src if len(n.split()) >= min_words]
    src_set = set(src)

    cand = [normalize(x) for x in split_sentences(d_prose) if not has_quote(x)]
    cand = [n for n in cand if len(n.split()) >= min_words]
    if not cand:
        return {'draft_sentences': 0, 'copied': 0, 'pct': 0.0, 'examples': []}

    copied, examples = 0, []
    for n in cand:
        if n in src_set:
            copied += 1
            examples.append(('verbatim', n))
            continue
        best = max((SequenceMatcher(None, n, sn).ratio() for sn in src), default=0.0)
        if best >= near:
            copied += 1
            examples.append((f'near {best:.2f}', n))
    return {
        'draft_sentences': len(cand),
        'copied': copied,
        'pct': 100.0 * copied / len(cand),
        'examples': examples[:10],
    }


def clefts(draft_path):
    prose, paras = strip_to_prose(open(draft_path, encoding='utf-8').read())
    wc = word_count(prose)
    hits = sum(len(re.findall(pat, prose, flags=re.M)) for pat, _ in CLEFT_PATTERNS)
    opening = []
    for p in paras:
        sents = split_sentences(p)
        if not sents:
            continue
        first = sents[0]
        if any(re.search(pat, first, flags=re.M) for pat, _ in CLEFT_PATTERNS):
            opening.append(first[:120])
    return {
        'words': wc,
        'cleft_hits': hits,
        'rate_per_1k': (1000.0 * hits / wc) if wc else 0.0,
        'topic_sentence_clefts': opening,
    }


def print_overlap(r):
    print(f"VERBATIM OVERLAP vs source:")
    print(f"  draft body sentences (>=8 words): {r['draft_sentences']}")
    print(f"  copied verbatim/near-verbatim:    {r['copied']}")
    print(f"  overlap:                          {r['pct']:.1f}%")
    flag = "  -> FLAG: high copy for a 'from scratch' rewrite" if r['pct'] > 5 else "  -> ok for a genuine rewrite"
    print(flag)
    if r['examples']:
        print("  copied examples:")
        for kind, s in r['examples']:
            print(f"    [{kind}] {s[:100]}")


def print_clefts(r):
    print(f"CLEFT / FRONTED (§21):")
    print(f"  words: {r['words']}   cleft hits: {r['cleft_hits']}   rate: {r['rate_per_1k']:.2f}/1k")
    if r['topic_sentence_clefts']:
        print(f"  -> FLAG: {len(r['topic_sentence_clefts'])} cleft(s) OPEN a paragraph (topic-sentence position):")
        for s in r['topic_sentence_clefts']:
            print(f"    - {s}")
    else:
        print("  -> no paragraph-opening clefts")


def main():
    ap = argparse.ArgumentParser(description="voice-check measurement gates")
    ap.add_argument('mode', choices=['overlap', 'clefts', 'both'])
    ap.add_argument('draft')
    ap.add_argument('source', nargs='?')
    a = ap.parse_args()
    if a.mode in ('overlap', 'both'):
        if not a.source:
            ap.error("overlap/both require a SOURCE file")
        print_overlap(overlap(a.draft, a.source))
        if a.mode == 'both':
            print()
    if a.mode in ('clefts', 'both'):
        print_clefts(clefts(a.draft))


if __name__ == '__main__':
    main()
