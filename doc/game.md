Module game
===========
A module used to store classes related to the representation of a game

Mostly used for playing bots against each other and developing strategies.

Functions
---------

    
`main()`
:   The main function for the game.

    
`pad_after(input_str)`
:   Pads a string with extra spaces.
    
    Args:
        input_str: The string to pad
    
    Returns:
        A padded string.

Classes
-------

`Game(strategies, print_trace)`
:   A class used to represent a game.
    
    Attributes:
        players: The list of players.
        table_card: The card on the table.
        dank: The suit of the trump card.
        cmp: A card comparator function.
        turns: A count of turns that have passed.
        table: The cards on the table.
        attacker: The player that is attacking.
    
    Inits Game with strategy and print trace data.
    
    visual:
        2
    1       3
        0
    
    Deal 6 to each
    Determine who has initial lowest dank (otherwise default to 0)
    
    Args:
        strategies: Contains the instantiated strategies for the players.
        print_trace: Whether or not to print a human readable trace.

    ### Methods

    `add_mod(self, start, offset)`
    :   Returns the player that is offset after the start/
        
        Args:
            start: The starting position.
            offset: The amount to offset by.
        
        Returns:
            The player that is offset after the start.

    `get_players(self)`
    :   Returns players involved in a turn.
        
        Returns:
            The Attacker, the Defender, and the next Player.

    `inc_attacker(self, increment)`
    :   Updates the attacker value mod number of players"
        
        Args:
            increment: The amount to increment by.

    `play(self)`
    :   Begins and runs the game.

    `print_hands(self)`
    :   Prints the cards in both hands.

    `step(self)`
    :   TODO(Bretley)

    `turn(self)`
    :   Method reflecting a single turn.
        
        General gist:
        Attacker attacks to + 1 % len(self.players):
            Play 1 card:
        Defender has 3 choices:
            Pass -> Can only be done if all cards on table match rank (i.e attack with 6 -> pass to next with 6 -> pass with 6).
                As soon as a non-6 is played cards can't be passed.
            Defend -> Plays a card higher rank and same suit.
            Take -> Takes up to 12 cards, gets skipped.
                After that, the attackers can shed.
        
        Back and forth.
        Can't play more than min(6, len(defender.cars)).
        Round is over when either a player runs out of cards.

    `turn2(self)`
    :   Turn reflecting a guaranteed 2 person game.