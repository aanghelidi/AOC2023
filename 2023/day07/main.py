import sys
from collections import Counter, deque
from dataclasses import dataclass
from enum import IntEnum
from functools import cmp_to_key

with open(sys.argv[1]) as f:
    data = f.read().splitlines()

CardLabel = IntEnum("CardLabel", "N2 N3 N4 N5 N6 N7 N8 N9 T J Q K A")
HandType = IntEnum("HandType", "HIGH_CARD ONE_PAIR TWO_PAIR THREE_OF_A_KIND FULL_HOUSE FOUR_OF_A_KIND FIVE_OF_A_KIND")


@dataclass(frozen=True)
class Card:
    label: CardLabel


@dataclass(frozen=True)
class Hand:
    cards: list[Card]
    bid: int = 0

    def __post_init__(self):
        assert len(self.cards) == 5


def type_of_hand(hand: Hand) -> HandType | int:
    cards = hand.cards
    counter = Counter(cards)
    most_common = counter.most_common()
    if len(counter) == 1:
        return HandType.FIVE_OF_A_KIND
    elif len(counter) == 2:
        if most_common[0][1] == 3 and most_common[1][1] == 2:
            return HandType.FULL_HOUSE
        return HandType.FOUR_OF_A_KIND
    elif len(counter) == 3 and most_common[0][1] == 3:
        return HandType.THREE_OF_A_KIND
    elif len(counter) == 3 and most_common[0][1] == 2:
        return HandType.TWO_PAIR
    elif len(counter) == 4:
        return HandType.ONE_PAIR
    else:
        return HandType.HIGH_CARD


def compare_hands(hand1: Hand, hand2: Hand) -> int:
    type1 = type_of_hand(hand1)
    type2 = type_of_hand(hand2)
    if type1 > type2:
        return 1
    elif type1 < type2:
        return -1
    else:
        cards1 = deque(hand1.cards)
        cards2 = deque(hand2.cards)
        while cards1 and cards2:
            card1 = cards1.popleft()
            card2 = cards2.popleft()
            if card1.label > card2.label:
                return 1
            elif card1.label < card2.label:
                return -1
    return 0


if __name__ == "__main__":
    number_of_hands = len(data)
    hands = []
    for line in data:
        line = line.strip()
        str_hand, bid = line.split()
        bid = int(bid)
        cards = []
        for c in str_hand:
            if c.isdigit():
                card_label = CardLabel(int(c) - 1)
                cards.append(Card(card_label))
            else:
                if c == "T":
                    card_label = CardLabel.T
                elif c == "J":
                    card_label = CardLabel.J
                elif c == "Q":
                    card_label = CardLabel.Q
                elif c == "K":
                    card_label = CardLabel.K
                else:
                    card_label = CardLabel.A
                cards.append(Card(card_label))
        hand = Hand(cards, bid)
        hands.append(hand)

    hands.sort(key=cmp_to_key(compare_hands))

    ans = 0
    for i, hand in enumerate(hands):
        ans += (i + 1) * hand.bid

    print(f"Part 1: {ans}")
