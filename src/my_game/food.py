import pygame
import random

from .settings import Settings, Colour

class FallingBase(pygame.sprite.Sprite):    
    def __init__(self, game, fall_speed=Settings.SPEED.value) -> None:
        super().__init__()
        self.game = game

        self.x = self.restrict_x()
        self.rect = pygame.Rect((self.x, 0), (Settings.BLOCK_SIZE.value, Settings.BLOCK_SIZE.value))

        self.colour = Colour.TRANSP_GRAY.value
        self.outline_colour = Colour.TRANSP_GRAY.value

        self.fall_speed = fall_speed
        self.fall_speed_counter = self.fall_speed

        self.collect_score = 0
        self.miss_score = 0
        self.miss_counter = 0


    def restrict_x(self):
        while True:
            x_pos = random.randint(0, Settings.WIN_WIDTH.value - Settings.BLOCK_SIZE.value)
            x_pos = Settings.BLOCK_SIZE.value*round(x_pos/Settings.BLOCK_SIZE.value)
            if x_pos != Settings.WIN_WIDTH.value/2:
                return x_pos
        

    def check_fall(self):
        if self.fall_speed_counter <= 0:
            self.fall_speed_counter = self.fall_speed
            return True
        else:
            self.fall_speed_counter -= 1
            return False

    
    def fall(self):
        if self.check_fall():
            self.rect.y += Settings.BLOCK_SIZE.value


    def kill_check(self):
        if self.rect.y >= Settings.WIN_HEIGHT.value - Settings.WIN_HEIGHT.value/10:
            return True


    def collision_check(self, player_rect):
        return bool(self.rect.colliderect(player_rect))


    def update(self):
        self.fall()
        pygame.draw.rect(self.game.screen, self.colour, self.rect)
        pygame.draw.rect(self.game.screen, self.outline_colour, self.rect, 2)


class Food(FallingBase):
    def __init__(self, game, fall_speed=Settings.SPEED.value/8) -> None:
        super().__init__(game, fall_speed)

        self.colour = Colour.GREEN.value
        self.outline_colour = Colour.LIGHT_GREEN.value

        self.collect_score = 10
        self.miss_score = -3
        self.miss_counter = 1
    
    def __str__(self):
        return f"Food at location ({self.rect.x}, {self.rect.y})"


class BadFood(FallingBase):
    def __init__(self, game, fall_speed=Settings.SPEED.value/4) -> None:
        super().__init__(game, fall_speed)

        self.colour = Colour.RED.value
        self.outline_colour = Colour.LIGHT_RED.value

        self.collect_score = -30

    def __str__(self):
        return f"BadFood at location ({self.rect.x}, {self.rect.y})"