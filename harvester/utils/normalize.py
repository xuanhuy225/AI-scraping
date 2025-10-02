import regex as re

PUNCT_MAP = {
    "“":"\"", "”":"\"", "‘":"'", "’":"'",
    "–":"-", "—":"-", "…":"...",
}
EMOJI_RE = re.compile(r"[\p{Emoji_Presentation}\p{Emoji}\u2600-\u27BF]+")
MULTI_NL = re.compile(r"\n{2,}")
MULTI_SPACE = re.compile(r"[ \t]{2,}")

def normalize_text(s: str) -> str:
    s = EMOJI_RE.sub("", s)
    for k, v in PUNCT_MAP.items():
        s = s.replace(k, v)
    s = MULTI_NL.sub("\n", s)
    s = MULTI_SPACE.sub(" ", s)
    return s.strip()
