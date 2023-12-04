import sys
from dataclasses import dataclass, field
from typing import DefaultDict

with open(sys.argv[1]) as f:
    data = f.read().splitlines()


@dataclass
class Card:
    id: int
    winning_numbers: list[int] = field(default_factory=list)
    numbers: list[int] = field(default_factory=list)

    @classmethod
    def parse(cls, data, id):
        all_numbers = data.split(": ")[1]
        winning_numbers, numbers = all_numbers.split(" | ")
        winning_numbers = [int(x) for x in winning_numbers.split()]
        numbers = [int(x) for x in numbers.split()]
        return cls(id, winning_numbers, numbers)

    def matching_winning_numbers(self) -> list[int]:
        return [x for x in self.numbers if x in self.winning_numbers]

    def copies(self, n_matches: int, current_id: int) -> list["Card"]:
        return [Card(current_id + i) for i in range(1, n_matches + 1)]


ans = 0
card_counter = DefaultDict(int)
for i, line in enumerate(data, start=1):
    card = Card.parse(line, i)
    card_counter[card.id] += 1
    matching_winning_numbers = card.matching_winning_numbers()
    for _ in range(card_counter[card.id]):
        copies = card.copies(len(matching_winning_numbers), i)
        for copy in copies:
            card_counter[copy.id] += 1
    if len(matching_winning_numbers) > 0:
        ans += 2 ** (len(matching_winning_numbers) - 1)

print(f"Part 1: {ans}")
print(f"Part 2: {sum(card_counter.values())}")
