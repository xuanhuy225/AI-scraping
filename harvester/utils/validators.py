import regex as re

NO_MULTI_NL = re.compile(r"\n{2,}")
NO_EMOJI = re.compile(r"[\p{Emoji_Presentation}\p{Emoji}\u2600-\u27BF]+")

def is_viable_text(s: str) -> bool:
    if len([w for w in s.split() if w.strip()]) < 200:
        return False
    if NO_EMOJI.search(s):
        return False
    if NO_MULTI_NL.search(s):
        return False
    return True
