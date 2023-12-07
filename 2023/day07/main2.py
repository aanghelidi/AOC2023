import sys
from collections import Counter, deque
from dataclasses import dataclass
from enum import IntEnum
from functools import cmp_to_key

with open(sys.argv[1]) as f:
    data = f.read().splitlines()

CardLabel = IntEnum("CardLabel", "J N2 N3 N4 N5 N6 N7 N8 N9 T Q K A")
HandType = IntEnum("HandType", "HIGH_CARD ONE_PAIR TWO_PAIR THREE_OF_A_KIND FULL_HOUSE FOUR_OF_A_KIND FIVE_OF_A_KIND")


@dataclass(frozen=True)
class Card:
    label: CardLabel


@dataclass
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


def convert_with_joker(hand: Hand) -> Hand:
    # Base case
    if Card(CardLabel.J) not in hand.cards:
        return hand
    type_hand = type_of_hand(hand)
    cards = hand.cards
    counter = Counter(cards)
    most_common = counter.most_common()
    # Full hand of jokers
    if type_hand == HandType.FIVE_OF_A_KIND:
        new_cards = [Card(CardLabel.A)] * 5
        return Hand(new_cards, bid=hand.bid)
    elif type_hand == HandType.FOUR_OF_A_KIND:
        max_card = max(hand.cards, key=lambda c: c.label)
        new_cards = [max_card] * 5
        return Hand(new_cards, bid=hand.bid)
    elif type_hand == HandType.FULL_HOUSE:
        max_card = max(hand.cards, key=lambda c: c.label)
        new_cards = [max_card] * 5
        return Hand(new_cards, bid=hand.bid)
    elif type_hand == HandType.THREE_OF_A_KIND:
        most_common_card = most_common[0][0]
        new_cards = [most_common_card if card.label == CardLabel.J else card for card in hand.cards]
        return Hand(new_cards, bid=hand.bid)
    elif type_hand == HandType.TWO_PAIR:
        joker_counts = hand.cards.count(Card(CardLabel.J))
        if joker_counts == 1:
            max_card = max(hand.cards, key=lambda c: c.label)
            new_cards = [max_card if card.label == CardLabel.J else card for card in hand.cards]
            return Hand(new_cards, bid=hand.bid)
        most_common_card = most_common[0][0]
        new_cards = [most_common_card if card.label == CardLabel.J else card for card in hand.cards]
        return Hand(new_cards, bid=hand.bid)
    elif type_hand == HandType.ONE_PAIR:
        joker_counts = hand.cards.count(Card(CardLabel.J))
        if joker_counts == 2:
            max_card = max(hand.cards, key=lambda c: c.label)
            new_cards = [max_card if card.label == CardLabel.J else card for card in hand.cards]
            return Hand(new_cards, bid=hand.bid)
        most_common_card = most_common[0][0]
        new_cards = [most_common_card if card.label == CardLabel.J else card for card in hand.cards]
        return Hand(new_cards, bid=hand.bid)
    elif type_hand == HandType.HIGH_CARD:
        max_card = max(hand.cards, key=lambda c: c.label)
        new_cards = [max_card if card.label == CardLabel.J else card for card in hand.cards]
        return Hand(new_cards, bid=hand.bid)
    else:
        raise ValueError(f"Unknown hand type: {type_hand}")


def compare_hands(hand1: Hand, hand2: Hand) -> int:
    type1 = type_of_hand(convert_with_joker(hand1))
    type2 = type_of_hand(convert_with_joker(hand2))
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
                card_label = CardLabel(int(c))
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

    print(f"Part 2: {ans}")
