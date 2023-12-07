import pytest
from main import Card, CardLabel, Hand, HandType, compare_hands, type_of_hand


@pytest.mark.parametrize(
    "hand, expected",
    [
        (
            Hand([Card(CardLabel.A), Card(CardLabel.A), Card(CardLabel.A), Card(CardLabel.A), Card(CardLabel.A)]),
            HandType.FIVE_OF_A_KIND,
        ),
        (
            Hand([Card(CardLabel.A), Card(CardLabel.A), Card(CardLabel.N8), Card(CardLabel.A), Card(CardLabel.A)]),
            HandType.FOUR_OF_A_KIND,
        ),
        (
            # 23332
            Hand([Card(CardLabel.N2), Card(CardLabel.N3), Card(CardLabel.N3), Card(CardLabel.N3), Card(CardLabel.N2)]),
            HandType.FULL_HOUSE,
        ),
        (
            # TTT98
            Hand([Card(CardLabel.T), Card(CardLabel.T), Card(CardLabel.T), Card(CardLabel.N9), Card(CardLabel.N8)]),
            HandType.THREE_OF_A_KIND,
        ),
        (
            # 23432
            Hand([Card(CardLabel.N2), Card(CardLabel.N3), Card(CardLabel.N4), Card(CardLabel.N3), Card(CardLabel.N2)]),
            HandType.TWO_PAIR,
        ),
        (
            # A23A4
            Hand([Card(CardLabel.A), Card(CardLabel.N2), Card(CardLabel.N3), Card(CardLabel.A), Card(CardLabel.N4)]),
            HandType.ONE_PAIR,
        ),
        (
            Hand([Card(CardLabel.N2), Card(CardLabel.N3), Card(CardLabel.N4), Card(CardLabel.N5), Card(CardLabel.N6)]),
            HandType.HIGH_CARD,
        ),
    ],
)
def test_type_of_hand(hand, expected):
    assert type_of_hand(hand) == expected


@pytest.mark.parametrize(
    "hand1, hand2, expected",
    [
        # 33332 and 2AAAA
        (
            Hand([Card(CardLabel.N3), Card(CardLabel.N3), Card(CardLabel.N3), Card(CardLabel.N3), Card(CardLabel.N2)]),
            Hand([Card(CardLabel.N2), Card(CardLabel.A), Card(CardLabel.A), Card(CardLabel.A), Card(CardLabel.A)]),
            1,
        ),
        # 77888 and 77788
        (
            Hand([Card(CardLabel.N7), Card(CardLabel.N7), Card(CardLabel.N8), Card(CardLabel.N8), Card(CardLabel.N8)]),
            Hand([Card(CardLabel.N7), Card(CardLabel.N7), Card(CardLabel.N7), Card(CardLabel.N8), Card(CardLabel.N8)]),
            1,
        ),
    ],
)
def test_compare_hands(hand1, hand2, expected):
    assert compare_hands(hand1, hand2) == expected
