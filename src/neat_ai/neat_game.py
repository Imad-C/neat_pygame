import enum
import neat
import os
import pygame; pygame.init()
import random

from src.my_game import Base, Food, Player, Settings, Direction, MainGame

class GameInfo:
    def __init__(self, score, missed):
        self.score = score
        self.missed = missed


class NeatGame(MainGame):
    '''
    Gives additional funtionality to MainGame so it can be fed into NEAT, but can
    still be played manually by passing move_allowed=True
    '''
    def __init__(self, 
            win_width=Settings.WIN_WIDTH.value,
            win_height=Settings.WIN_HEIGHT.value,
            food_speed=Settings.SPEED.value/8,
            food_spawn_speed=Settings.SPEED.value*4,
            player_speed=Settings.SPEED.value/8,

            pop_no = 0
            ) -> None:
        super().__init__(
            win_width=win_width,
            win_height=win_height,
            food_speed=food_speed,
            food_spawn_speed=food_spawn_speed,
            player_speed=player_speed
        )
        
        self.player = Player(self, self.player_speed, move_allowed=False)
        self.pop_no = pop_no
    

    def move_player(self, player: Player, direction=Direction.NONE):
        '''
        Allow the game to move the player (so it can be controlled by NEAT)
        '''
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


    def get_game_state(self):
        '''
        Returns all vars that are inputs to NEAT
        ### Returns
        - Player x grid coordinate
        - Food x grid coordiante
        - Vertical distance between food and player (using grid coordinates)
        '''
        player_x = self.get_grid_coord(self.player.rect.x)
        player_y = self.get_grid_coord(self.player.rect.y)

        if self.food_instances: #if food exists
            food = self.food_instances[0]
            food_x = self.get_grid_coord(food.rect.x)
            food_y_distance = abs(player_y - self.get_grid_coord(food.rect.y))
        else: #if no food, assume food at center top of screen
            food_x = self.get_grid_coord(Settings.WIN_WIDTH.value/2)
            food_y_distance = self.get_grid_coord(Settings.WIN_HEIGHT.value)
        
        return player_x, food_x, food_y_distance


    def draw_game_state(self):
        '''
        Draws the game state
        '''
        player_x, food_x, food_y_dist = self.get_game_state()
        food_x_dist = abs(player_x - food_x)

        if self.food_instances:
            food: Food = self.food_instances[0]
            points = (
                (self.player.rect.x, self.player.rect.y),
                (food.rect.x, self.player.rect.y),
                (food.rect.x, food.rect.y)
                )
        else:
            points = (
                (self.player.rect.x, self.player.rect.y),
                (Settings.WIN_WIDTH.value/2, self.player.rect.y),
                (Settings.WIN_WIDTH.value/2, 0)
                )            
        
        food_x_dist_surface = self.font_small.render(f'{food_x_dist}', False, (0,200,0))
        self.screen.blit(
            food_x_dist_surface, #surface to draw on
            ((player_x + food_x) * Settings.BLOCK_SIZE.value / 2, #x coord of surface
             self.player.rect.y) #y coord of surface
             )
        
        food_y_dist_surface = self.font_small.render(f'{food_y_dist}', False, (0,200,0))
        self.screen.blit(
            food_y_dist_surface,
            (food_x * Settings.BLOCK_SIZE.value,
             (self.player.rect.y - food_y_dist * Settings.BLOCK_SIZE.value / 2))
             )
            
        pygame.draw.lines(self.screen, (0,200,0), False, points)
    

    def draw_game_info(self):
        super().draw_game_info()
        score_surface = self.font.render(f'PopNo.: {self.pop_no}', False, (0,200,0))
        self.screen.blit(score_surface, (Settings.BLOCK_SIZE.value, Settings.BLOCK_SIZE.value*3))
    
    
    def update(self):
        super().update()
        self.draw_game_state()

        pygame.display.flip()


    def loop(self):
        '''
        Updates the game within the NEAT loop which is 
        different to the main game loop called with the method update()
        '''
        self.move_player(self.player)
        self.spawn_food()
        self.update()

        self.clock.tick(Settings.SPEED.value)

        return GameInfo(self.score, self.missed)


    def reset(self):
        self.player.reset()
        self.food_spawn_counter = self.food_spawn_speed
        self.food_instances.clear()
        self.score = 0
        self.missed = 0


if __name__ == "__main__":
    NeatGame().run()