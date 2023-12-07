from dataclasses import dataclass
from functools import cmp_to_key
import utils

@dataclass
class Hand:
    cards: str
    bid: int

joker = "J"
card_values = {
    "A": 14, "K": 13, "Q": 12, joker: 1, "T": 10, "9": 9, "8": 8, "7": 7, "6": 6, "5": 5, "4": 4, "3": 3, "2": 2
}

def get_hand_strength(hand: Hand) -> int:
    card_set = set(hand.cards)
    jokers = hand.cards.count(joker)
    occurrences = sorted([hand.cards.count(card) for card in card_set if card != joker], reverse=True)

    max_occurrence = jokers
    if len(occurrences):
        max_occurrence = max_occurrence + occurrences[0]

    if max_occurrence == 5:
        return 7
    
    if max_occurrence == 4:
        return 6
    
    if max_occurrence == 3 and occurrences[1] == 2:
        return 5
    
    if max_occurrence == 3:
        return 4
    
    if occurrences[1] == 2:
        return 3
    
    if max_occurrence == 2:
        return 2
    
    return 1

def compare_hands(hand1: Hand, hand2: Hand) -> int:
    if (diff := get_hand_strength(hand=hand2) - get_hand_strength(hand=hand1)) != 0:
        return diff
    return next((diff for i in range(len(hand1.cards)) if (diff := card_values[hand2.cards[i]] - card_values[hand1.cards[i]]) != 0), 0)

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

split_lines = [line.split(" ") for line in lines]
hands = [Hand(cards=words[0], bid=int(words[1])) for words in split_lines]

ranked_hands = sorted(hands, key=cmp_to_key(compare_hands), reverse=True)
#print(ranked_hands)

hand_sum = 0
for i in range(len(ranked_hands)):
    hand = ranked_hands[i]
    hand_sum = hand_sum + ((i+1) * hand.bid)
print(hand_sum)