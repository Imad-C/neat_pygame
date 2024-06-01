import neat
import os
from pathlib import Path
import pickle
import pygame
import shutil

from src.my_game import Settings, Direction
from src.neat_ai import NeatGame

NORMAL_SPEED = {
    'food_speed': Settings.SPEED.value/4,
    'food_spawn_speed': Settings.SPEED.value*4,
    'player_speed': Settings.SPEED.value/8,
}

FAST_SPEED = {
    'food_speed': Settings.SPEED.value/32,
    'food_spawn_speed': Settings.SPEED.value*1.6,
    'player_speed': Settings.SPEED.value/64,
}

LOCAL_DIR = os.path.dirname(__file__)

class NeatGameAI():
    '''
    Every member of the population plays NeatGame every generation, this class
    allows it to do so
    '''
    def __init__(self, game_speed_dict):
        self.game = NeatGame(
            food_speed=game_speed_dict['food_speed'],
            food_spawn_speed=game_speed_dict['food_spawn_speed'],
            player_speed=game_speed_dict['player_speed']
            )
        
        self.player = self.game.player
    

    def test_ai(self, genome, config):
        '''
        Takes a trained nueral net (genome) and configuration to play the game
        '''
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        run = True
        while run: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT: run = False #pygame.quit(); os.sys.exit()
            
            output = net.activate(self.game.get_game_state())
            decision = output.index(max(output)) 
            if decision == 1:
                self.game.move_player(self.player, Direction.LEFT)
            elif decision == 2:
                self.game.move_player(self.player, Direction.RIGHT)
            else: # i.e. decision = 0
                self.game.move_player(self.player, Direction.NONE)

            game_info = self.game.loop()

        pygame.quit()


    def train_ai(self, genome, config):
        '''
        Takes a genome and config to play the game, 
        once game is over, assigns a fitness based on performance
        '''

        #generate new based on genome
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        run = True
        while run: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT: quit()

            #creates an output based on inputs (game_state)
            output = net.activate(self.game.get_game_state()) 
            #decide by taking max of output probabilities
            decision = output.index(max(output)) 
            if decision == 1:
                self.game.move_player(self.player, Direction.LEFT)
            elif decision == 2:
                self.game.move_player(self.player, Direction.RIGHT)
            else: #i.e. decision = 0
                self.game.move_player(self.player, Direction.NONE)

            #go to next loop
            game_info = self.game.loop()

            if any([
                self.lose_condition(
                    genome, game_info, game_info.missed >= 6),
                self.lose_condition(
                    genome, game_info, game_info.score >= 1000),
                self.lose_condition(
                    genome, game_info, self.player.rect.x <= 0, cost=50),
                self.lose_condition(
                    genome, game_info, self.player.rect.x >= Settings.WIN_WIDTH.value, cost=50)
                ]):
                break


    def lose_condition(self, genome, game_info, condition, cost=0):
        if condition:
            self.calculate_fitness(genome, game_info, cost)
            return True
        else: return False


    def calculate_fitness(self, genome, game_info, cost=0):
        genome.fitness += game_info.score
        genome.fitness -= cost


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        #initialise genome fitness to 0
        genome.fitness = 0 
        game: NeatGameAI = NeatGameAI(FAST_SPEED)
        #updating pop number
        game.game.pop_no = genome_id % 50 #this number is pop size
        game.train_ai(genome, config) 


def move_checkpoint(
        source=os.getcwd(),
        relative_destination='neat_outputs',
        file_name='neat-checkpoint-'
        ):
    
    path = os.path.join(LOCAL_DIR, relative_destination)
 
    for _, _, files in os.walk(source):
        for file in files:
            if file_name in str(file):
                try:
                    shutil.move(os.path.join(source, file),
                                os.path.join(path, file))
                except: pass


def run_neat(config, checkpoint: str=None):
    '''
    Takes a config and creates a population, evaluates each member of the population 
    by running it through the game, repeats for number passed in 'run' method. Size 
    of population is detirmined in the config.
    '''

    #initialising population, or using existing checkpoint
    if checkpoint:
        checkpoint_path = os.path.join(LOCAL_DIR, 'neat_outputs/' + checkpoint)
        pop = neat.Checkpointer.restore_checkpoint(checkpoint_path)

    else:
        pop = neat.Population(config) 

    # #adding reporter output
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(
        generation_interval=1, filename_prefix='neat-checkpoint-')) 


    winner = pop.run(eval_genomes, 30) #winner is best genome
    with open("best.pickle", 'wb') as f:
        pickle.dump(winner, f)

    #moving all checkpoints and best.pickle
    move_checkpoint()      
    move_checkpoint(file_name='best')


def test_ai(config, winner_name: str):
    winner_path = os.path.join(LOCAL_DIR, 'neat_outputs/' + winner_name)
    with open(winner_path + '.pickle', 'rb') as f:
        winner = pickle.load(f)

    game = NeatGameAI(NORMAL_SPEED)
    game.test_ai(winner, config)


if __name__ == "__main__":
    config_path = os.path.join(LOCAL_DIR, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    
    run_neat(config)
    # test_ai(config, 'best')