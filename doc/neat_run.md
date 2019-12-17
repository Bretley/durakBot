Module neat_run
===============
Uses NEAT genetic machine learning to teach a machine how to play Durak.

Contains the Worker class, which does the main program loop for the Durak
emulation. Main initializes the configuration for neat-python and sends it to
the Worker class, which uses a custom Gym environment to iterate through the
game until it reaches a completion state.

    Usage:

    python neat_run.py
    python neat_run.py --config=FILEPATH --restore=FILEPATH

Functions
---------

    
`eval_genomes(genome, config)`
:   Evaluates the fitness of a genome.
    
    Sends the genome and configuration to the Worker class so that the worker
    can calculate how fit a genome is to reproduce.
    
    Args:
        genome: The genome to be tested.
        config: The configuration specifications for NEAT.
    Returns:
        A float that represents the fitness of a genome. The higher the number
        the fitter it is and the more likely the genome is to reproduce.

    
`main(config_file, restore_file)`
:   The main function for the neat_run module.
    
    Loads in the NEAT configuration and creates the objects necessary for
    running the NEAT emulation.
    
    Args:
        config_file: The location of the configuration file.
        restore_file: The location of the restore point file.

Classes
-------

`Worker(genome, config)`
:   Evaluates the fitness of a genome.
    
    Attributes:
        genome: The genome to be tested.
        config: The configuration specifications for NEAT.
        env: The game environment.
    
    Inits Worker with NEAT genome and configuration data.
    
    Args:
        genome: The genome to be tested.
        config: The configuration specifications for NEAT.

    ### Methods

    `work(self)`
    :   Evaluates the fitness of a genome.
        
        Creates the main loop for the evaluation of fitness. Loads in the Durak
        environment, initializes it, takes the state data, and iterates through
        states until the environment says that the game is done.
        
        Returns:
            A float that represents the fitness of a genome. The higher the
            number the fitter it is and the more likely the genome is to
            reproduce.