import random

SUIT_TUPLE = ("Пики", "Черви", "Крести", "Буби")
RANK_TUPLE = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
NCARDS = 8
SCORE = 50


def getCards(deckListIn):
    thisCard = deckListIn.pop(0)
    return thisCard


def shuffleDeck(deckListIn):
    deckListOut = deckListIn.copy()
    random.shuffle(deckListOut)
    return deckListOut


def createDeck():
    deckList = []
    for suit in SUIT_TUPLE:
        for value, rank in enumerate(RANK_TUPLE):
            deckList.append({"rank": rank, "suit": suit, "value": value + 1})
    return deckList


# Основной код
print("Welcome to Higher or Lower.")
print(
    "You have to choose whether the next card to be shown will be higher or lower than the current card."
)
print("Getting it right adds 20 points; get it wrong and you lose 15 points.")
print("You have 50 points to start.")
print()

while True:
    deckGame = shuffleDeck(createDeck())
    currentCard = getCards(deckGame)
    currentCardValue = currentCard["value"]
    currentCardRank = currentCard["rank"]
    currentCardSuit = currentCard["suit"]
    print(
        f"Your current card is {currentCardRank} of {currentCardSuit}. You have {SCORE} points."
    )
    if SCORE <= 0:
        print("You have no points left. Game over.")
        break
    if len(deckGame) < NCARDS:
        print("There are no more cards left in the deck. Game over.")
        break
    for i in range(NCARDS):
        answer = input(
            "Will the next card be higher or lower than the current card? (h/l): "
        ).lower()
        if answer not in ("h", "l"):
            print("Invalid input. Please enter 'h' for higher or 'l' for lower.")
            continue
        nextCard = getCards(deckGame)
        nextCardValue = nextCard["value"]
        nextCardRank = nextCard["rank"]
        nextCardSuit = nextCard["suit"]
        print(
            f"The next card is {nextCardRank} of {nextCardSuit}. You have {SCORE} points."
        )
        if (answer == "h" and nextCardValue > currentCardValue) or (
            answer == "l" and nextCardValue < currentCardValue
        ):
            SCORE += 20
            print("Correct! You gain 20 points.")
        else:
            SCORE -= 15
            print("Incorrect! You lose 15 points.")
        currentCard = nextCard
        currentCardValue = currentCard["value"]
        currentCardRank = currentCard["rank"]
        currentCardSuit = currentCard["suit"]
        print(
            f"Your current card is now {currentCardRank} of {currentCardSuit}. You have {SCORE} points."
        )
