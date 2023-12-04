import sys
from collections import defaultdict
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Generator

with open(sys.argv[1]) as f:
    data = f.read().splitlines()


@dataclass
class Card:
    id: int
    winning_numbers: set[int] = field(default_factory=set)
    numbers: set[int] = field(default_factory=set)

    @classmethod
    def parse(cls, data, id):
        winning_numbers, numbers = data.split(": ")[1].split(" | ")
        winning_numbers = {int(x) for x in winning_numbers.split()}
        numbers = {int(x) for x in numbers.split()}
        return cls(id, winning_numbers, numbers)

    def matching_winning_numbers(self) -> set[int]:
        return self.winning_numbers & self.numbers


@lru_cache
def retrieve_copies(n_matches: int, current_id: int) -> Generator[Card, None, None]:
    return (Card(current_id + i) for i in range(1, n_matches + 1))


ans = 0
card_counter = defaultdict(int)
for i, line in enumerate(data, start=1):
    card = Card.parse(line, i)
    card_counter[card.id] += 1
    matching_winning_numbers = card.matching_winning_numbers()
    for _ in range(card_counter[card.id]):
        for copy in retrieve_copies(len(matching_winning_numbers), i):
            card_counter[copy.id] += 1
    if len(matching_winning_numbers) > 0:
        ans += 2 ** (len(matching_winning_numbers) - 1)

print(f"Part 1: {ans}")
print(f"Part 2: {sum(card_counter.values())}")
