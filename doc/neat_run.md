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

    
`eval_genomes(genomes, config)`
:   Evaluates the fitness of a genome.
    
    Args:
        genomes: The genomes to be tested.
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