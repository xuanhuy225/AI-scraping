from bs4 import BeautifulSoup
import re

def inject_images_at_positions(html: str, text: str):
    soup = BeautifulSoup(html, "lxml")
    imgs = [img.get("src") for img in soup.find_all("img") if img.get("src")]
    out = text
    for src in imgs:
        tok = f"[img_{src}]"
        if not re.search(re.escape(tok), out):
            out += f"\n{tok}"
    return out, imgs
