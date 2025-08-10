from abc import ABC, abstractmethod
from typing import List, Union
from dataclasses import dataclass

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
RANKS = [
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "Jack",
    "Queen",
    "King",
    "Ace",
]


@dataclass
class CardType:
    STANDARD = "standard"
    JOKER = "joker"
    SPECIAL = "special"


class Card(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def get_card(self, *args, **kwargs):
        pass


class StandardCard(Card):
    def __init__(self, suit: str, rank: str, value: int):
        super().__init__(suit + rank + str(value))
        self.suit = suit
        self.rank = rank
        self.value = value

    def get_card(self):
        return {"suit": self.suit, "rank": self.rank, "value": self.value}


class CardFactory(ABC):
    @abstractmethod
    def create_card(self, *args, **kwargs):
        pass


class StandardCardFactory(CardFactory):
    def create_card(self, suit: str, rank: str, value: int) -> StandardCard:
        return StandardCard(suit, rank, value)


class CardFactoryManager:
    def __init__(self):
        self.factories = {
            CardType.STANDARD: StandardCardFactory(),
            # Add other card type factories here
        }

    def create_card(self, card_type: CardType, *args, **kwargs) -> Card:
        factory = self.factories.get(card_type)
        if not factory:
            raise ValueError(f"Factory for card type {card_type} not found.")
        return factory.create_card(*args, **kwargs)

    def get_factory(self, card_type: CardType) -> CardFactory:
        factory = self.factories.get(card_type)
        if not factory:
            raise ValueError(f"Factory for card type {card_type} not found.")
        return factory

    def get_all_factories(self) -> List[CardFactory]:
        return list(self.factories.values())

    def register_factory(self, card_type: CardType, factory: CardFactory):
        if not isinstance(factory, CardFactory):
            raise TypeError("Factory must be an instance of CardFactory")
        self.factories[card_type] = factory
        return self


if __name__ == "__main__":
    factory = CardFactoryManager()
    card = factory.create_all_cards(CardType.STANDARD, SUITS, RANKS)
    for c in card:
        print(c.get_card())
