import gym
import neat
import os

from src.durak_env import DurakEnv


class Worker:
    def __init__(self, genome, config):
        self.genome = genome
        self.config = config
        self.env = None

    def work(self):
        self.env = DurakEnv()
        self.env.reset()

        done = False

        while not done:
            actions = None
            _, _, done, _ = self.env.step(actions)

        fitness = 0
        return fitness


def eval_genomes(genome, config):
    worker = Worker(genome, config)
    return worker.work()


def main(config_file, restore_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    if restore_file is None:
        p = neat.Population(config)
    else:
        p = neat.Checkpointer.restore_checkpoint(restore_file)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(generation_interval=10, filename_prefix='../restores/neat-checkpoint-'))

    pe = neat.ParallelEvaluator(10, eval_genomes)

    winner = p.run(pe.evaluate)

    print(winner)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.normpath(os.path.join(local_dir, '..', 'config', '.NEAT'))
    restore_path = None  # os.path.normpath(os.path.join(local_dir, '..', 'restores', 'neat-checkpoint-1'))
    main(config_path, restore_path)
