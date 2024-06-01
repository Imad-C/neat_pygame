import enum
from math import hypot
import os
import pygame; pygame.init()
import random

from src.my_game import Base, Food, Player, Settings, Direction


class MainGame:
    def __init__(self, 
            win_width=Settings.WIN_WIDTH.value,
            win_height=Settings.WIN_HEIGHT.value,
            food_speed=Settings.SPEED.value/8,
            food_spawn_speed=Settings.SPEED.value*4,
            player_speed=Settings.SPEED.value/8
            ) -> None:
        
        #speed of gameplay
        self.food_speed = food_speed
        self.food_spawn_speed = food_spawn_speed
        self.food_spawn_counter = self.food_spawn_speed
        self.player_speed = player_speed

        #init display
        self.win_width = win_width
        self.win_height = win_height
        self.screen = pygame.display.set_mode((self.win_width, self.win_height))
        self.transparent_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)

        pygame.display.set_caption('Game Name')
        self.font = pygame.font.SysFont("monospace", 30)
        self.font_small = pygame.font.SysFont("monospace", 15)
        self.clock = pygame.time.Clock()

        #track game info
        self.score = 0
        self.missed = 0

        self.base = Base(self)
        self.player = Player(self, self.player_speed)
        self.food_instances = []

    
    def spawn_food(self):
        self.food_spawn_counter -= 1
        if self.food_spawn_counter <= 0:
            self.food_instances.append(Food(self, self.food_speed))
            self.food_spawn_counter = self.food_spawn_speed

    
    def update_food(self):
        for food in self.food_instances:
            food.update()
            if food.collision_check(self.player):
                self.score += food.collect_score #update score
                self.food_instances.remove(food)
            elif food.kill_check():
                self.score += self.get_perc_score(food) + food.miss_score
                self.missed += food.miss_counter
                self.food_instances.remove(food)
    

    def move_player(self, player: Player, direction=Direction.NONE):
        if player.check_move():
            if direction == Direction.LEFT:
                player.rect.x -= Settings.BLOCK_SIZE.value
                player.restrict_move()
            if direction == Direction.RIGHT:
                player.rect.x += Settings.BLOCK_SIZE.value
                player.restrict_move()  
            if direction == Direction.NONE:
                pass   
        else: pass

    
    def get_perc_score(self, food: Food):
        '''
        Calculates a score percentage based on distance between player and food
        ### Parameters
        - food being destroyed 
        '''
        distance = abs(self.get_grid_coord(self.player.rect.x) - self.get_grid_coord(food.rect.x))
        if distance >= 10:
            # print(f'distance: {distance}, score: 0, game_score: {self.score}')
            return 0
        elif 0 < distance < 10:
            # print(f'distance: {distance}, score: {food.collect_score - distance}, game_score: {self.score}')
            return food.collect_score - distance
        else: 
            # print(f'distance: {distance}, score: {food.collect_score} ,game_score: {self.score}')
            return food.collect_score


    def get_grid_coord(self, coord):
        '''
        Takes a pixel coordinate and converts it into a grid coordinate
        ### Parameters
        - pixel coordinate
        '''
        return round(coord/Settings.BLOCK_SIZE.value)
    

    def draw_game_info(self):
        score_surface = self.font.render(f'score : {self.score}', False, (0,200,0))
        self.screen.blit(score_surface, (Settings.BLOCK_SIZE.value, Settings.BLOCK_SIZE.value))

        missed_surface = self.font.render(f'missed: {self.missed}', False, (0,200,0))
        self.screen.blit(missed_surface, (Settings.BLOCK_SIZE.value, Settings.BLOCK_SIZE.value*2))

    
    def update(self):
        self.base.update()
        self.player.update()
        self.spawn_food()
        self.update_food()
        self.draw_game_info()

        pygame.display.flip()


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); os.sys.exit()
            
            self.move_player(self.player)
            self.spawn_food()
            self.update()

            self.clock.tick(Settings.SPEED.value)
    

if __name__ == "__main__":
    MainGame().run()