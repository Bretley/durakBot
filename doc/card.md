Module card
===========
A module used to store the Card class.

Represents a playing card from a Durak deck, which is a standard deck but with
the cards 2-5 removed.

Functions
---------

    
`create_comparator(dank_suit)`
:   Creates a comparator to compare two cards.
    
    Args:
    dank_suit: The suit of the dank card.
    
    Returns:
        A comparator function.

    
`suited(card, suit)`
:   Tells if the card matches the suit.
    
    Args
        card: The card to check.
        suit: The suit to check.
    
    Returns
        True if they are the same suit, false otherwise.

Classes
-------

`Card(rank, suit)`
:   A class used to represent a card.
    
    Attributes
        rank: The value of a card.
        suit: The suit of the card.
    
    Inits Cards with a rank and suit.
    
    Args:
        rank: The rank of the card 6-A.
        suit: The suit of the card, Diamonds, Spades, Clubs, or Hearts.