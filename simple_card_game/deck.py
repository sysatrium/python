from abc import ABC, abstractmethod
from typing import List, Union
from dataclasses import dataclass
import random
from card import (
    Card,
    CardFactory,
    CardType,
    CardFactoryManager,
    StandardCard,
    StandardCardFactory,
    SUITS,
    RANKS,
)


class ShuffleStrategy(ABC):
    @abstractmethod
    def shuffle(self, cards: List[Union[str, int]]) -> List[Union[str, int]]:
        pass


class RandomShuffle(ShuffleStrategy):
    def shuffle(self, cards: List[Union[str, int]]) -> List[Union[str, int]]:
        shuffled_cards = cards.copy()
        random.shuffle(shuffled_cards)
        return shuffled_cards


class RiffleShuffle(ShuffleStrategy):
    def shuffle(self, cards: List[Card]) -> List[Card]:
        left, right = cards[: len(cards) // 2], cards[len(cards) // 2 :]
        mixed: List[Card] = []
        while left or right:
            if left and (not right or random.random() < 0.5):
                mixed.append(left.pop(0))
            if right and (not left or random.random() < 0.5):
                mixed.append(right.pop(0))
        return mixed


class FisherYatesShuffle(ShuffleStrategy):
    def shuffle(self, cards: List[Card]) -> List[Card]:
        result = cards.copy()
        for i in range(len(result) - 1, 0, -1):
            j = random.randint(0, i)
            result[i], result[j] = result[j], result[i]
        return result


class WeakShuffle(ShuffleStrategy):
    """N случайных свапов — плохой, но быстрый пример."""

    def __init__(self, swaps: int = 10) -> None:
        self.swaps = swaps

    def shuffle(self, cards: List[Card]) -> List[Card]:
        result = cards.copy()
        for _ in range(self.swaps):
            i, j = random.randrange(len(result)), random.randrange(len(result))
            result[i], result[j] = result[j], result[i]
        return result


class Deck(ABC):
    @abstractmethod
    def create_deck(self, *args, **kwargs):
        pass

    @abstractmethod
    def shuffle_deck(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_game_deck(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_current_card(self, *args, **kwargs):
        pass


class StandardDeck(Deck):
    def __init__(self, shuffle_strategy: ShuffleStrategy | None = None):
        self.deck = []
        self.shuffle_strategy = shuffle_strategy or RandomShuffle()
        self.factory = CardFactoryManager().get_factory(CardType.STANDARD)

    def create_deck(self, suits: List[str], ranks: List[str]):
        for suit in suits:
            for value, rank in enumerate(ranks):
                card = self.factory.create_card(suit, rank, value + 1)
                self.deck.append(card)
        return self

    def shuffle_deck(self) -> List[Union[str, int]]:
        return self.shuffle_strategy.shuffle(self.deck)

    def get_game_deck(self) -> List[Union[str, int]]:
        return self.shuffle_deck()

    def get_current_card(self) -> Union[str, int]:
        game_deck = self.get_game_deck()
        if not game_deck:
            raise ValueError("Deck is empty, please create a new deck.")
        return game_deck.pop(0)  # Return and remove the top card from the dec
