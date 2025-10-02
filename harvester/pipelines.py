import os, hashlib
import orjson
import scrapy
import random

from harvester.utils.extract_main import extract_main
from harvester.utils.normalize import normalize_text
from harvester.utils.anonymize import anonymize
from harvester.utils.image_inject import inject_images_at_positions
from harvester.utils.de_duplicator import DeDuplicator
from harvester.utils.validators import is_viable_text
from harvester.utils.latexify import tables_to_latex, formulas_to_latex

OUT_DIR = "data/jsonl"
RAW_DIR = "data/raw_html"

class CleanAndWritePipeline:
    def __init__(self, max_shard_bytes=1_000_000_000):
        os.makedirs(OUT_DIR, exist_ok=True)
        os.makedirs(RAW_DIR, exist_ok=True)
        self.dd = DeDuplicator()
        self.shard_idx = 0
        self.curr_size = 0
        self.fp = open(self._shard_path(), "ab")

    def _shard_path(self):
        return os.path.join(OUT_DIR, f"vi_news_{self.shard_idx:03d}.jsonl")

    def _rollover_if_needed(self):
        if self.curr_size >= 1_000_000_000:
            self.fp.close()
            self.shard_idx += 1
            self.curr_size = 0
            self.fp = open(self._shard_path(), "ab")

    def process_item(self, item, spider):
        url = (item.get("url") or "").strip()
        title = (item.get("title") or "").strip()
        html  = item.get("html") or ""

        # Save raw html sample for audit
        if random.random() < 0.01:
            if url:
                hname = hashlib.md5(url.encode("utf-8")).hexdigest() + ".html"
            else:
                hname = hashlib.md5((title + html).encode("utf-8")).hexdigest() + ".html"
            with open(os.path.join(RAW_DIR, hname), "wb") as f:
                f.write(html.encode("utf-8", errors="ignore"))

        # Extract & image inject
        text0 = extract_main(html)
        text1, imgs = inject_images_at_positions(html, text0)

        # Normalize and latexify
        text1 = normalize_text(text1)
        text1 = tables_to_latex(text1)
        text1 = formulas_to_latex(text1)

        # Anonymize (replace with 'x')
        text1 = anonymize(text1)

        # De-duplicate
        if self.dd.is_dup(title + "\n" + text1):
            raise scrapy.exceptions.DropItem("duplicate")

        # Quality filter
        if not is_viable_text(text1):
            raise scrapy.exceptions.DropItem("quality_filter")

        # Domain category
        domain = getattr(spider, "domain_category", "News")

        # id = MD5(url + title + text)
        _id = hashlib.md5((url + title + text1).encode("utf-8")).hexdigest()

        record = {
            "id": _id,
            "title": title,
            "text": text1,
            "domain": domain,
            "url": url
        }
        b = orjson.dumps(record, option=orjson.OPT_APPEND_NEWLINE)
        self.fp.write(b)
        self.curr_size += len(b)
        self._rollover_if_needed()
        return item

    def close_spider(self, spider):
        if getattr(self, "fp", None):
            self.fp.close()
