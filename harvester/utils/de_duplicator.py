import hashlib
from simhash import Simhash

class DeDuplicator:
    def __init__(self):
        self.md5_seen = set()

    def md5_of(self, s: str) -> str:
        return hashlib.md5(s.encode("utf-8")).hexdigest()

    def is_dup(self, text: str) -> bool:
        h = self.md5_of(text)
        if h in self.md5_seen:
            return True   # trùng tuyệt đối
        self.md5_seen.add(h)
        return False
