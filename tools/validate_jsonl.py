import orjson, sys, regex as re, os

def bad(s):
    return any([
        re.search(r"[\p{Emoji_Presentation}\p{Emoji}\u2600-\u27BF]+", s or ""),
        re.search(r"\n{2,}", s or ""),
    ])

def main(path):
    line_count = 0
    with open(path, "rb") as f:
        for i, line in enumerate(f, 1):
            line_count += 1
            try:
                obj = orjson.loads(line)
            except:
                print(f"Line {i}: invalid JSON")
                return 1
            keys = list(obj.keys())
            if keys != ["id","title","text","domain","url"]:
                print(f"Line {i}: wrong key order {keys}")
                return 1
            if len(obj["text"].split()) < 150:
                print(f"Line {i}: <150 words")
                return 1
            # if bad(obj["text"]) or bad(obj["title"]):
            #     print(f"Line {i}: emoji/multi-NL violation")
            #     return 1

    # # ---- thêm validate tổng số dòng ----
    # if line_count < 10000:
    #     print(f"FAIL: only {line_count} lines (< 10,000 required)")
    #     return 1
    #
    # # ---- thêm validate kích thước file ----
    # file_size = os.path.getsize(path)
    # if file_size < 1_000_000_000:  # 1GB
    #     print(f"FAIL: file size {file_size} bytes (< 1GB required)")
    #     return 1
    #
    # print(f"OK: {line_count} lines, {file_size} bytes")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
