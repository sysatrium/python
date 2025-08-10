from deck import (
    Deck,
    StandardDeck,
    SUITS,
    RANKS,
    RandomShuffle,
    RiffleShuffle,
    WeakShuffle,
    FisherYatesShuffle,
)

NCARDS = 8
SCORE = 50
# Example usage
shuffle_strategy = FisherYatesShuffle()  # or RiffleShuffle(), WeakShuffle()
deck = StandardDeck(shuffle_strategy)
game_deck = deck.create_deck(SUITS, RANKS).get_game_deck()
while True:
    if game_deck:
        currentCard = deck.get_current_card().get_card()
        print("The current card is: ", currentCard)

    for i in range(NCARDS):
        answer = input(
            "Will the next card be higher or lower than the current card? (h/l): "
        ).lower()
        if answer not in ("h", "l"):
            print("Invalid input. Please enter 'h' for higher or 'l' for lower.")
            continue
        nextCard = deck.get_current_card().get_card()
        print(f"The next card is {nextCard}. You have {SCORE} points.")
        if (answer == "h" and nextCard["value"] > currentCard["value"]) or (
            answer == "l" and nextCard["value"] < currentCard["value"]
        ):
            SCORE += 20
            print("Correct! You gain 20 points.")
        else:
            SCORE -= 15
            print("Incorrect! You lose 15 points.")
        currentCard = nextCard
        print(f"Your current card is now {currentCard}. You have {SCORE} points.")
        if SCORE <= 0:
            print("You have no points left. Game over.")
            break
        if len(game_deck) < NCARDS:
            print("There are no more cards left in the deck. Game over.")
            break
