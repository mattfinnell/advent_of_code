from collections import namedtuple
from typing import List, Set, Dict
from pprint import pprint

import math

def get_values(line: List[str]) -> List[List[int]]:
    def _get_values(line: str) -> List[int]:
        return { int(value) for value in filter(lambda x: x != "", line.split(" ")) }

    return _get_values(line[0]), _get_values(line[1])

def get_match_count(card: List[Set[str]]) -> int:
    return len(card[0] & card[1])

def get_score(card: List[Set[str]]) -> int:
    return math.floor(2 ** (get_match_count(card) - 1))

def scratchcards_part_1(input_file):
    with open(input_file, "r") as f:
        cards = [
            get_values(line[:-1].split(":")[1].split("|")) 
            for line in f.readlines()
        ]

    return sum((get_score(card) for card in cards))

def count_cards(i: int, cards: Dict[int, int]) -> int: 
    if i > len(cards):
        return 0 

    value = 0
    if cards[i] > 0:
        for j in range(i + 1, min(i + cards[i] + 1, len(cards))):
            value += count_cards(j, cards)

    return value + 1

def count_cards_memoized(i: int, cards: Dict[int, int], memo_table: Dict[int, int]) -> int: 
    if i > len(cards):
        return 0 

    if i in memo_table:
        return memo_table[i]

    value = 0
    if cards[i] > 0:
        for j in range(i + 1, min(i + cards[i] + 1, len(cards))):
            value += count_cards_memoized(j, cards, memo_table)

    memo_table[i] = value + 1
    return memo_table[i]


def scratchcards_part_2(input_file):
    with open(input_file, "r") as f:
        cards = [line.split(":") for line in f.readlines()]
        cards = {
            int(card[0].split(" ")[-1]):
            get_match_count(get_values(card[1].split("|")))
            for card in cards
        }

    table = {}
    for i in reversed(range(1, len(cards) + 1)):
        table[i] = count_cards_memoized(i, cards, table)

    return sum(table.values())

    # class Card:
    #     def __init__(self, card_id, copies, points):
    #         self.card_id = card_id
    #         self.copies = copies
    #         self.points = points

    # cards = { k: Card(k, 1, v) for (k, v) in cards.items() }

    # pt2=0
    # for c in cards.keys():
    #     for i in range(cards[c].copies):
    #         for j in range(1, cards[c].points + 1):
    #             cards[c + j].copies += 1
    #     pt2 += cards[c].copies

    # return pt2


example, main = "scratchcards_example.txt", "scratchcards_main.txt"

pprint(scratchcards_part_2(main))