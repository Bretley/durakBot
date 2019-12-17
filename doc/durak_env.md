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
    
    Inits DurakEnv with default data.

    ### Ancestors (in MRO)

    * gym.core.Env

    ### Methods

    `render(self, mode='human')`
    :   Will not be used.

    `reset(self)`
    :   Resets the game to the starting state.
        
        TODO more detail about what gets reset.

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