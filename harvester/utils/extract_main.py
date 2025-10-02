from bs4 import BeautifulSoup
import trafilatura

def extract_main(html: str) -> str:
    text = trafilatura.extract(html, include_images=True, output="txt", favor_recall=False)
    if not text:
        soup = BeautifulSoup(html, "lxml")
        for tag in soup(["script","style","nav","footer","header","aside"]):
            tag.decompose()
        text = soup.get_text("\n")
    return text or ""
