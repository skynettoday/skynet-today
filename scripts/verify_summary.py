"""Deterministic checks on a generated summary against the source text it came from.

No LLM. Catches the failure modes that are mechanically decidable:
  - quotes that don't appear verbatim in any source
  - numbers and dates that appear in no source
  - passages copied too closely from a source

Causal claims and internal contradictions are NOT checkable here — see check_causal_claims()
in csv2newsletter.py for the narrow LLM pass that handles those.

Usage:
    warnings = verify_summary(summary_text, [main_text, *related_texts])
    for w in warnings:
        print(w)
"""
import re
import unicodedata

MIN_QUOTE_WORDS = 4        # ignore short quoted fragments like "risk"
COPY_NGRAM = 12            # a shared run this long is close paraphrase, not coincidence
_PUNCT = str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"',
                        '–': '-', '—': '-', '…': '...', '\xa0': ' '})


def _norm(text):
    """Fold quotes/dashes, strip accents, collapse whitespace, lowercase."""
    text = unicodedata.normalize('NFKC', text).translate(_PUNCT)
    return re.sub(r'\s+', ' ', text).strip().lower()


def _bare(text):
    """Words only — punctuation dropped, so a quote is not 'altered' by a trailing comma."""
    return ' '.join(re.findall(r"[a-z0-9$%]+(?:'[a-z]+)?", _norm(text)))


def _words(text):
    return re.findall(r"[a-z0-9$%.,'-]+", _norm(text))


def check_quotes(summary, sources):
    """Every quoted span of >=MIN_QUOTE_WORDS words must appear verbatim in some source."""
    joined = _bare(' '.join(sources))
    out = []
    for quote in re.findall(r'"([^"]{4,400})"', _norm(summary)):
        if len(quote.split()) < MIN_QUOTE_WORDS:
            continue
        bare = _bare(quote)
        if bare and bare not in joined:
            # near-miss: the opening words match but the rest does not — an altered quote,
            # which is worse than one invented whole, because it looks sourced.
            head = ' '.join(bare.split()[:MIN_QUOTE_WORDS])
            kind = 'ALTERED' if head in joined else 'NOT FOUND'
            out.append(f'QUOTE {kind}: "{quote[:110]}"')
    return out


def check_numbers(summary, sources):
    """Every number/date in the summary should appear in some source."""
    joined = ' '.join(_norm(s) for s in sources)
    src_nums = set(re.findall(r'\d[\d,.]*', joined))
    src_bare = {n.replace(',', '').rstrip('.') for n in src_nums}
    months = r'(?:january|february|march|april|may|june|july|august|september|october|november|december)'
    out = []
    for num in set(re.findall(r'\d[\d,.]*', _norm(summary))):
        if num.replace(',', '').rstrip('.') not in src_bare:
            out.append(f'NUMBER NOT IN SOURCE: {num}')
    for md in set(re.findall(months + r'\s+\d{1,2}', _norm(summary))):
        if md not in joined:
            out.append(f'DATE NOT IN SOURCE: {md}')
    return out


def check_copying(summary, sources, n=COPY_NGRAM):
    """Flag runs of n+ consecutive words shared with a source (close paraphrase).

    Quoted spans are excluded — verbatim quotation is the goal there, not a defect.
    """
    sw = _words(re.sub(r'"[^"]*"', ' ', summary))
    src_grams = set()
    for s in sources:
        w = _words(s)
        src_grams.update(tuple(w[i:i + n]) for i in range(len(w) - n + 1))
    out, i = [], 0
    while i <= len(sw) - n:
        if tuple(sw[i:i + n]) in src_grams:
            j = i + n
            while j < len(sw) and tuple(sw[j - n + 1:j + 1]) in src_grams:
                j += 1
            out.append(f'COPIED {j - i} WORDS: "{" ".join(sw[i:j])[:130]}"')
            i = j
        else:
            i += 1
    return out


def verify_summary(summary, sources):
    """Run all deterministic checks. Returns a list of warning strings (empty = clean)."""
    if not summary or not sources:
        return []
    sources = [s for s in sources if s]
    return (check_quotes(summary, sources)
            + check_numbers(summary, sources)
            + check_copying(summary, sources))
