"""
TODO
"""

import argparse
import os

import neat

from src.durak_env import DurakEnv


class Worker:
    """
    TODO
    """

    def __init__(self, genome, config):
        """
        TODO
        """

        self.genome = genome
        self.config = config
        self.env = None

    def work(self):
        """
        TODO
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
    """
    TODO
    """

    # Use the worker class for simplicity
    worker = Worker(genome, config)
    return worker.work()


def main(config_file, restore_file):
    """
    TODO
    """

    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    # Load Restore file if it is specified
    if restore_file is None:
        population = neat.Population(config)
    else:
        population = neat.Checkpointer.restore_checkpoint(restore_file)

    # Create reporters
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(generation_interval=10, filename_prefix='../restores/neat-checkpoint-'))

    # Run the learning in parallel
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
