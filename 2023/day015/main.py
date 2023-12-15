import sys
from collections import defaultdict

with open(sys.argv[1]) as f:
    sequences = f.read().strip().split(",")


def hash_algorithm(s: str) -> int:
    current = 0
    for c in s:
        current += ord(c)
        current *= 17
        current %= 256
    return current


def focusing_power(key: int, boxes: defaultdict[int, list[tuple[str, int]]]) -> int:
    return sum((key + 1) * sn * fl for sn, (_, fl) in enumerate(boxes[key], start=1))


print(f"Part 1: {sum(hash_algorithm(seq) for seq in sequences)}")

boxes = defaultdict(list)
for seq in sequences:
    if "-" in seq:
        label, _ = seq.split("-")
        bn = hash_algorithm(label)
        if bn not in boxes:
            continue
        labels = {lab for lab, _ in boxes[bn]}
        e_to_remove = None
        if label in labels:
            for lens in boxes[bn]:
                if lens[0] == label:
                    e_to_remove = lens
                    break
            boxes[bn].remove(e_to_remove)
    else:
        label, _, fl = seq.partition("=")
        bn = hash_algorithm(label)
        fl = int(fl)
        labels = {lab for lab, _ in boxes[bn]}
        if label in labels:
            for i, (ilabel, _) in enumerate(boxes[bn]):
                if ilabel == label:
                    boxes[bn][i] = (label, fl)
                    break
        else:
            boxes[bn].append((label, fl))

print(f"Part 2: {sum(focusing_power(key, boxes) for key in boxes)}")
