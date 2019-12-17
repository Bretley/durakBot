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
    
    Durak is a Russian/Slavic/Eastern European card game that
    exists somewhere in between War and Euchre. Rounds are played with
    attackers and defenders, the first to go out wins, and the trump 'dank'
    suit matters. It's a good blend of mechanics, strategy, and luck.
    
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
        print_trace: Whether or not to print trace of the game.
        first_shed: True if first shed of the turn, false otherwise.
        shed_so_far: Number of cards shed so far.
        allowed_to_shed: Total number of cards the Model could shed.
        model: Model object wrapper, mostly manages Model's hand.
    
    Inits DurakEnv.

    ### Ancestors (in MRO)

    * gym.core.Env

    ### Methods

    `legal_attack(self, move)`
    :   Determines whether an attack is a legal action or not.
        
        Args:
            move: The attack to check.
        
        Returns:
            Attack is legal if:
            Move < 36 or 108.
            Card matches ranks in table.
            Card is in hand.

    `legal_defense(self, move)`
    :   Determines whether a defense is a legal action or not.
        
        Args:
            move: The defense to check.
        
        Returns:
            True if defense is legal.
            Defense is legal if it is higher rank same suit,or any dank,
            or higher dank in the case that a dank was played.

    `legal_shed(self, move)`
    :   Determines whether a shed is a legal action or not.
        
        Args:
            move: The attack to check.
        
        Returns:
            Whether or not the shed is legal.
            'Done' is always a legal shed.
            Shed card is legal if card is in hand and rank matches table.

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