import re

with open("input.txt") as f:
    data = f.read().splitlines()
numsd = dict(zip("one two three four five six seven eight nine".split(), "123456789"))
ans, ans2 = 0, 0
numbers = re.compile(r"\d{1}")
numbers_or_str = re.compile(r"(?=(\d{1}|one|two|three|four|five|six|seven|eight|nine))")
for line in data:
    nums = numbers.findall(line)
    joined = nums[0] + nums[-1]
    ans += int(joined)
    # Part 2
    nums = [n for n in numbers_or_str.findall(line) if n != ""]  # ugly
    joined = numsd.get(nums[0], nums[0]) + numsd.get(nums[-1], nums[-1])
    ans2 += int(joined)
print(f"Part 1: {ans}")
print(f"Part 2: {ans2}")
