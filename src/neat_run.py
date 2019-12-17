"""Uses NEAT genetic machine learning to teach a machine how to play Durak.

Contains the Worker class, which does the main program loop for the Durak
emulation. Main initializes the configuration for neat-python and sends it to
the Worker class, which uses a custom Gym environment to iterate through the
game until it reaches a completion state.

    Usage:

    python neat_run.py
    python neat_run.py --config=FILEPATH --restore=FILEPATH
"""

import argparse
import os

import neat

from src.durak_env import DurakEnv


class Worker:
    """Evaluates the fitness of a genome.

    Attributes:
        genome: The genome to be tested.
        config: The configuration specifications for NEAT.
        env: The game environment.
    """

    def __init__(self, genome, config):
        """Inits Worker with NEAT genome and configuration data.

        Args:
            genome: The genome to be tested.
            config: The configuration specifications for NEAT.
    """

        self.genome = genome
        self.config = config
        self.env = None

    def work(self):
        """Evaluates the fitness of a genome.

        Creates the main loop for the evaluation of fitness. Loads in the Durak
        environment, initializes it, takes the state data, and iterates through
        states until the environment says that the game is done.

        Returns:
            A float that represents the fitness of a genome. The higher the
            number the fitter it is and the more likely the genome is to
            reproduce.
        """

        # Loads in a default Durak state
        self.env = DurakEnv()
        self.env.reset()

        net = neat.nn.FeedForwardNetwork.create(self.genome, self.config)

        # Takes the first step to get an observation ofn the current state
        observation, _, _, _ = self.env.step(self.env.action_space.sample())
        reward = 0
        done = False
        info = None

        # Loops through the game until the game is finished or the machine makes an unforgivable mistake
        while not done:
            actions = net.activate(observation)
            observation, reward, done, info = self.env.step(actions)

        del info

        return reward


def eval_genomes(genome, config):
    """Evaluates the fitness of a genome.

    Sends the genome and configuration to the Worker class so that the worker
    can calculate how fit a genome is to reproduce.

    Args:
        genome: The genome to be tested.
        config: The configuration specifications for NEAT.
    Returns:
        A float that represents the fitness of a genome. The higher the number
        the fitter it is and the more likely the genome is to reproduce.
    """

    # Uses the worker class for simplicity
    worker = Worker(genome, config)
    return worker.work()


def main(config_file, restore_file):
    """The main function for the neat_run module.

    Loads in the NEAT configuration and creates the objects necessary for
    running the NEAT emulation.

    Args:
        config_file: The location of the configuration file.
        restore_file: The location of the restore point file.
    """

    # Loads configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    # Loads Restore file if it is specified
    if restore_file is None:
        population = neat.Population(config)
    else:
        population = neat.Checkpointer.restore_checkpoint(restore_file)

    # Creates reporters
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(generation_interval=10, filename_prefix='../restores/neat-checkpoint-'))

    # Runs the learning in parallel
    evaluator = neat.ParallelEvaluator(10, eval_genomes)
    winner = population.run(evaluator.evaluate)

    print(winner)


if __name__ == '__main__':
    # Reads in optional file specification arguments
    PARSER = argparse.ArgumentParser(description="Run NEAT on the Durak game.")
    PARSER.add_argument('--config', type=str, default="../config/.NEAT", required=False)
    PARSER.add_argument('--restore', type=str, default=None, required=False)
    ARGS = PARSER.parse_args()

    LOCAL_DIR = os.path.dirname(__file__)
    CONFIG_PATH = os.path.normpath(os.path.join(LOCAL_DIR, ARGS.config))

    if ARGS.restore is None:
        RESTORE_PATH = None
    else:
        RESTORE_PATH = os.path.normpath(os.path.join(LOCAL_DIR, ARGS.restore))

    main(CONFIG_PATH, RESTORE_PATH)
