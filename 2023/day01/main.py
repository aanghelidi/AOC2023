with open("input.txt") as f:
    data = f.read().splitlines()
numsd = dict(zip("one two three four five six seven eight nine".split(), "123456789"))
ans, ans2 = 0, 0
for line in data:
    nums, nums2 = [], []
    for i, c in enumerate(line):
        if c.isdigit():
            nums.append(c)
            nums2.append(c)
        for k, v in numsd.items():
            if line[i:].startswith(k):
                nums2.append(v)
    ans += int(nums[0] + nums[-1])
    ans2 += int(nums2[0] + nums2[-1])
print(f"Part 1: {ans}")
print(f"Part 2: {ans2}")
