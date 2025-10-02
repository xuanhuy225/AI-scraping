import regex as re

def replace_with_x(match):
    return "x"

def anonymize(s: str) -> str:
    patterns = [
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        r"(\+?\d[\d\s\-()]{7,}\d)",
        r"\b(?:\d[ -]?){13,19}\b",
        r"\b[A-Za-z]{1,2}\d{6,12}\b",
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        r"\b(\d{1,4}\s+(đường|duong|street|st\.|phường|phuong|xã|xa|thôn|thon|ấp|ap|quận|quan|huyện|huyen)\b[^,\n]*)",
        r"@[A-Za-z0-9_\.]{3,}",
        r"(facebook\.com|zalo\.me|whatsapp\.com|t\.me|instagram\.com)/[^\s]+",
    ]
    for p in patterns:
        s = re.sub(p, replace_with_x, s, flags=re.IGNORECASE)
    return s
