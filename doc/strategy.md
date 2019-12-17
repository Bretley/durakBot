Module strategy
===============
Contains various strategies for bots to employ.

The Strategy class is an interface for for the various strategies.
All strategies need an attack, defense, and shed.

Functions
---------

    
`lowest_defense(attack, hand, dank)`
:   Returns lowest card that can defend or None.
    
    Assumes sorted hand.
    
    Args:
        attack: The card to attack with
        hand: The list of cards in the hand
        dank: The suit of the dank card
    
    Returns:
        The lowest card that can defend or None if there is not a valid card

    
`rank_matches(cards, rank)`
:   Return all rank matches in a set of cards.
    
    Args:
        cards: A list of cards.
        rank: The rank to check for.
    
    Returns:
        The list of cards that match the rank.

Classes
-------

`Attack(*args, **kwargs)`
:   A class used to enumerate attack actions.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `done`
    :   A class used to enumerate attack actions.

    `play`
    :   A class used to enumerate attack actions.

`Defense(*args, **kwargs)`
:   A class used to enumerate defense actions.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `defend`
    :   A class used to enumerate defense actions.

    `pass_to`
    :   A class used to enumerate defense actions.

    `take`
    :   A class used to enumerate defense actions.

`S0()`
:   TODO(Bretley)
        
    
    Inits Strategy.

    ### Ancestors (in MRO)

    * strategy.Strategy

    ### Methods

    `attack(self, hand, table, dank, ranks)`
    :   TODO(Bretley)
        
        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            ranks: TODO(Bretley)
        
        Returns:
            TODO(Bretley)

    `defend(self, hand, table, dank, pass_is_legal, cards_to_defend)`
    :   TODO(Bretley)
        
        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            pass_is_legal: Whether or not a pass is legal.
            cards_to_defend: The number of cards to defend against.
        
        Returns:
            TODO(Bretley)

    `shed(self, hand, table, dank, max_shed_allowed, ranks)`
    :   TODO(Bretley)
        
        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            max_shed_allowed: The maximum amount of cards to shed.
            ranks: TODO(Bretley)
        
        Returns:
            A list of cards to shed.

`S1()`
:   TODO(Bretley)
    
    Identical to S0 except:
        does not shed danks
        does not pass if it requires a dank to do so
    
    Inits Strategy.

    ### Ancestors (in MRO)

    * strategy.Strategy

    ### Methods

    `attack(self, hand, table, dank, ranks)`
    :   TODO(Bretley)
        
        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            ranks: TODO(Bretley)
        
        Returns:
            TODO(Bretley)

    `defend(self, hand, table, dank, pass_is_legal, cards_to_defend)`
    :   TODO(Bretley)
        
        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            pass_is_legal: Whether or not a pass is legal.
            cards_to_defend: The number of cards to defend against.
        
        Returns:
            TODO(Bretley)

    `shed(self, hand, table, dank, max_shed_allowed, ranks)`
    :   TODO(Bretley)
        
        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            max_shed_allowed: The maximum amount of cards to shed.
            ranks: TODO(Bretley)
        
        Returns:
            A list of cards to shed.

`S2()`
:   TODO(Bretley)
    
    Identical to S0 except:
        does not shed danks
        does not shed if card rank > 10
        does not pass if it requires a dank to do so
    
    Inits Strategy.

    ### Ancestors (in MRO)

    * strategy.Strategy

    ### Methods

    `attack(self, hand, table, dank, ranks)`
    :   TODO(Bretley)
        
        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            ranks: TODO(Bretley)
        
        Returns:
            TODO(Bretley)

    `defend(self, hand, table, dank, pass_is_legal, cards_to_defend)`
    :   TODO(Bretley)
        
        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            pass_is_legal: Whether or not a pass is legal.
            cards_to_defend: The number of cards to defend against.
        
        Returns:
            TODO(Bretley)

    `shed(self, hand, table, dank, max_shed_allowed, ranks)`
    :   TODO(Bretley)
        
        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            max_shed_allowed: The maximum amount of cards to shed.
            ranks: TODO(Bretley)
        
        Returns:
            A list of cards to shed.

`Strategy()`
:   An interface for strategies.
        
    
    Inits Strategy.

    ### Descendants

    * strategy.S0
    * strategy.S1
    * strategy.S2

    ### Methods

    `attack(self, hand, table, dank, ranks)`
    :   An attack turn.
        
        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            ranks: TODO(Bretley)

    `defend(self, hand, table, dank, pass_is_legal, cards_to_defend)`
    :   A defense turn.
        
        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            pass_is_legal: Whether or not a pass is legal.
            cards_to_defend: The number of cards to defend against.

    `shed(self, hand, table, dank, max_shed_allowed, ranks)`
    :   A shed turn.
        
        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            max_shed_allowed: The maximum amount of cards to shed.
            ranks: TODO(Bretley)