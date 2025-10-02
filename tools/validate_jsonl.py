import orjson, sys, regex as re

def bad(s): 
    return any([
        re.search(r"[\p{Emoji_Presentation}\p{Emoji}\u2600-\u27BF]+", s or ""),
        re.search(r"\n{2,}", s or ""),
    ])

def main(path):
    with open(path, "rb") as f:
        for i, line in enumerate(f, 1):
            try:
                obj = orjson.loads(line)
            except:
                print(f"Line {i}: invalid JSON")
                return 1
            keys = list(obj.keys())
            if keys != ["id","title","text","domain","url"]:
                print(f"Line {i}: wrong key order {keys}")
                return 1
            if len(obj["text"].split()) < 200:
                print(f"Line {i}: <200 words")
                return 1
            if bad(obj["text"]) or bad(obj["title"]):
                print(f"Line {i}: emoji/multi-NL violation")
                return 1
    print("OK")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
