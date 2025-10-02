import hashlib
from simhash import Simhash

class DeDuplicator:
    def __init__(self, simhash_tol=3):
        self.md5_seen = set()
        self.simhashes = []

    def md5_of(self, s: str) -> str:
        return hashlib.md5(s.encode("utf-8")).hexdigest()

    def is_dup(self, text: str) -> bool:
        h = self.md5_of(text)
        if h in self.md5_seen:
            return True
        sh = Simhash(text).value
        for old, _ in self.simhashes:
            if bin(old ^ sh).count("1") <= 3:
                return True
        self.md5_seen.add(h)
        self.simhashes.append((sh, h))
        return False
