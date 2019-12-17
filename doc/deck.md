Module deck
===========
A module used to store the Deck class.

Represents a deck of cards for a game of Durak.

Classes
-------

`Deck()`
:   A class used to represent a deck of cards.
    
    Attributes:
        cards: The list of cards in the deck
    
    Inits Deck.

    ### Methods

    `draw(self)`
    :   Takes a card from the top of the deck.
        
        Returns:
            The top card or None if there is not a card in the deck

    `flip(self)`
    :   Reveals the bottom card of the deck.
        
        Returns:
            The bottom card in the deck or None if the deck is empty

    `is_empty(self)`
    :   Returns whether the deck is empty.
        
        Returns:
            True if the deck is empty, False otherwise

    `shuffle_deck(self)`
    :   Randomizes the order of the deck