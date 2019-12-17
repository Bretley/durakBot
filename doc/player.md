Module player
=============
A module used to store classes related the the representation of a player.

Classes
-------

`Player(num, strategy)`
:   A class used to represent a Player (simple bot).
    
    Attributes:
        hand: The list of cards in the player's hand.
        num : The Player's ID.
        dank: The suit of the Dank card.
        strategy: The strategy the bot uses.
    
    Inits Player with an ID and strategy.
    
    Args:
        num: The Player's ID
        strategy: Class must implement shed, attack, and defend for the bot.

    ### Methods

    `attack(self, table, ranks)`
    :   Does an attack action.
        
        Args:
            table: The cards on the table.
            ranks: TODO(Bretley)
        
        Returns:
            The return of the strategy's attack.

    `defend(self, table, pass_is_legal, cards_to_defend)`
    :   Does a defense action.
        
        Args:
            table: The cards on the table.
            pass_is_legal: Whether or not a pass is legal.
            cards_to_defend: The number of cards to defend against.
        
            Returns:
                The return of the strategy's defend.

    `shed(self, table, max_shed_allowed, ranks)`
    :   Sheds cards to the player's hand
        
        Args:
            table: The list of cards on the table.
            max_shed_allowed: The maximum amount of cards to shed.
            ranks: TODO(Bretley)
        
            Returns:
                The return of the strategy's shed.

    `sort(self)`
    :   Sorts the player's hand

    `take(self, card)`
    :   Adds card to the player's hand.
        
        Args:
            card: The card to add to the hand.

    `take_table(self, cards)`
    :   Adds cards to the player's hand
        
        Args:
            cards: The list of cards to add to the player's hand.

    `verify_hand(self)`
    :   Method to ensure that the hand contains 0 duplicates