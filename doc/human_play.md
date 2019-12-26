Module human_play
=================
A module used to simulate Model interaction as a human.

Functions
---------

    
`main()`
:   The main function that runs.

Classes
-------

`HumanInterface()`
:   A class used to represent a human interactable way version of the
    information the model receives.
    
        Attributes:
            hand: The cards in the player's hand.
            table: The cards on the table.
            outs: The cards in the out pile.
            dank: The dank card.
            def_card: The card to defend against.
            state: The state of gameplay.
        
    
    Inits HumanInterface.

    ### Methods

    `get_play(self)`
    :   TODO(Bretley)
        
        Returns:
            TODO(Bretley)

    `parse_obs(self, obs)`
    :   Parses the observations into a human readable structure.
        
        Args:
            obs: The observations to parse.