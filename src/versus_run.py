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
import random

import neat

# pylint: disable=import-error
from durak_env import DurakEnv
from versus_evaluator import VersusEvaluator


class Worker:
    """A worker for multi-threaded evolution.

    Attributes:
        genome: The genome to be tested.
        config: The configuration specifications for NEAT.
        env: The Durak environment.
    """

    def __init__(self, genome_a, genome_b, config):
        """Inits a worker with a genome and the config.
        """
        self.genome_a = genome_a
        self.genome_b = genome_b
        self.config = config
        self.env = DurakEnv()
        self.net_a = neat.nn.FeedForwardNetwork.create(self.genome_a, self.config)
        self.net_b = neat.nn.FeedForwardNetwork.create(self.genome_b, self.config)

    def work(self):
        """Evaluates the fitness of a genome.

        Returns:
            A float that represents the fitness of a genome. The higher the number
            the fitter it is and the more likely the genome is to reproduce.
        """

        # Loads in a default Durak state.
        self.env.reset()

        # Takes the first step to get an observation ofn the current state.
        observation, _, _, info = self.env.step(self.env.action_space.sample())
        total_reward_a = 0
        total_reward_b = 0
        done = False
        reward = 0.
        num_games = 30
        # Loops through the game until the game is finished or the machine makes an unforgivable mistake.
        for _ in range(num_games):
            i = -1
            while not done:
                i += 1
                if info['player1']:
                    actions = self.net_a.activate(observation)
                    observation, reward, done, info = self.env.step(actions)
                else:
                    actions = self.net_a.activate(observation)
                    observation, reward, done, info = self.env.step(actions)

            if info['player1']:
                total_reward_a += reward
            else:
                total_reward_b += reward

            if int(random.random() * 1000) == 1:
                print(info, reward)

            self.env.reset()

        return total_reward_a / num_games, total_reward_b / num_games


def eval_genomes(genome_a, genome_b, config):
    """Evaluates the fitness of a genome by sending it to the worker.

    Args:
        genome_a: The first genome to be tested.
        genome_b: The second genome to be tested.
        config: The configuration specifications for NEAT.
    Returns:
        A float that represents the fitness of a genome. The higher the number
        the fitter it is and the more likely the genome is to reproduce.
    """

    worker = Worker(genome_a, genome_b, config)
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

    # Loads Restore file if it is specified.
    if restore_file is None:
        population = neat.Population(config)
    else:
        population = neat.Checkpointer.restore_checkpoint(restore_file)

    # Creates reporters.
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(generation_interval=500, filename_prefix='../restores/neat-checkpoint-'))

    # Runs the learning in parallel.
    evaluator = VersusEvaluator(8, eval_genomes)
    winner = population.run(evaluator.evaluate)

    print(winner)


if __name__ == '__main__':
    # Reads in optional file specification arguments.
    PARSER = argparse.ArgumentParser(description="Run NEAT on the Durak game.")
    PARSER.add_argument('--config', type=str, default="../config/.NEAT", required=False)
    PARSER.add_argument('--restore', type=str, default=None, required=False)
    ARGS = PARSER.parse_args()

    LOCAL_DIR = os.path.dirname(__file__)
    CONFIG_PATH = os.path.normpath(os.path.join(LOCAL_DIR, ARGS.config))

    if ARGS.restore is None:
        RESTORE_PATH = None
    else:
        RESTORE_PATH = os.path.normpath(os.path.join(LOCAL_DIR, "../restores/neat-checkpoint-" + str(ARGS.restore)))

    main(CONFIG_PATH, RESTORE_PATH)
