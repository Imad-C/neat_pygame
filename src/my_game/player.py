import pygame

from .settings import Settings, Colour, Direction

class Player(pygame.sprite.Sprite):
    def __init__(self, game, move_speed=Settings.SPEED.value/16, move_allowed=True) -> None:
        super().__init__()
        self.game = game
        
        self.rect = pygame.Rect(
            (Settings.WIN_WIDTH.value/2, Settings.WIN_HEIGHT.value - Settings.WIN_HEIGHT.value/10 - Settings.BLOCK_SIZE.value),
            (Settings.BLOCK_SIZE.value, Settings.BLOCK_SIZE.value)
            )
        
        self.direction = Direction.NONE
        self.move_allowed = move_allowed

        self.move_speed = move_speed #16
        self.move_speed_counter = self.move_speed
    

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.direction = Direction.LEFT
        elif keys[pygame.K_d]:
            self.direction = Direction.RIGHT
        else:
            self.direction = Direction.NONE


    def check_move(self):
        if self.move_speed_counter <= 0:
            return True
        else:
            self.move_speed_counter -= 1
            return False

    
    def restrict_move(self):
        self.can_move = False
        self.move_speed_counter = self.move_speed


    def move(self):
        if self.check_move():
            if self.direction == Direction.RIGHT:
                self.rect.x += Settings.BLOCK_SIZE.value
                self.restrict_move()
            if self.direction == Direction.LEFT:
                self.rect.x -= Settings.BLOCK_SIZE.value
                self.restrict_move()
            if self.direction == Direction.NONE:
                pass
    

    def reset(self):
        self.rect.x = Settings.WIN_WIDTH.value/2


    def update(self):
        if self.move_allowed:
            self.get_input()
        self.move()
        pygame.draw.rect(self.game.screen, Colour.BLUE.value, self.rect)
        pygame.draw.rect(self.game.screen, Colour.LIGHT_BLUE.value, self.rect, 2) #outline