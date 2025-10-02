import sys, os

def shard(inpath, bytes_per_shard=1_000_000_000):
    base = os.path.splitext(os.path.basename(inpath))[0]
    outdir = os.path.dirname(inpath)
    idx, size = 0, 0
    out = open(os.path.join(outdir, f"{base}.{idx:03d}.jsonl"), "wb")
    with open(inpath, "rb") as f:
        for line in f:
            if size >= bytes_per_shard:
                out.close()
                idx += 1
                size = 0
                out = open(os.path.join(outdir, f"{base}.{idx:03d}.jsonl"), "wb")
            out.write(line)
            size += len(line)
    out.close()

if __name__ == "__main__":
    shard(sys.argv[1])
