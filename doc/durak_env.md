Module durak_env
================
A Gym environment that mimics a game of Durak.

Contains the DurakEnv class, which is a child class of the gym.Env class.
Implements all of the functions necessary to play through a game of Durak and
train a machine learning model to play it.

Classes
-------

`DurakEnv()`
:   The environment that represents a game of Durak.
    
    TODO more detail about Durak.
    
    Attributes:
        action_space: The set of available actions.
        observation_space: The set of variables in the environment.
        game_started: Whether or not the game has been started.
        deck: Deck object containing cards.
        out_pile: List of cards that are out of the game.
        players: The number of players.
        turns: The number of turns taken so far.
        table: The cards on the current attack/defense.
        ranks: Hash table of ranks of cards in table.
        attack_count: Count of attacks this turn.
        state: String representing the state of the game DFA.
        dank: String representing the dank suit.
        table_card: Card at the bottom of the deck.
        opponent: Bot that plays against the Model.
        print_trace: TODO(Bretley) with capitalization and punctuation.
        model: Model object wrapper, mostly manages Model's hand.
    
    Inits DurakEnv.

    ### Ancestors (in MRO)

    * gym.core.Env

    ### Methods

    `legal_attack(self, attack)`
    :   Determines whether an attack is a legal action or not.
        
        Args:
            attack: The attack to check.
        
        Returns:
            Attack is legal if:
            Action < 36 or 108.
            Card matches ranks in table.
            Card is in hand.

    `render(self, mode='human')`
    :   Will not be used.

    `reset(self)`
    :   Resets the game to the starting state.

    `step(self, action)`
    :   Proceeds through a single step in the game.
        
        Goes from one state of the game to the next based on the input action
        that it receives and returns relevant information. TODO more detail.
        
        Args:
            action: The action to take on this step.
        Returns:
            A gym.space that represents the current state of the game.
            A float that represents the fitness of this genome.
            A bool that represents whether or not the game is done.
            A list that contains additional information that may be useful.

`Model()`
:   Model is a wrapper for the AI hand.
    
    Attributes:
        hand: TODO(Bretley)
    
    Inits Model.

    ### Methods

    `remove_card(self, card)`
    :   Removes a card from the model's hand.
        
        Args:
            card: The card to remove from the model's hand.

    `take(self, card)`
    :   Adds card to the model's hand.
        
        Args:
            card: The card to add to the hand.

    `take_table(self, cards)`
    :   Adds cards to the model's hand.
        
        Args:
        cards: The list of cards to add to the model's hand.