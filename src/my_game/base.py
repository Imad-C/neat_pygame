import pygame

from .settings import Settings, Colour

class Base:
    def __init__(self, game) -> None:
        self.game = game
        self.rect = pygame.Rect(0, (Settings.WIN_HEIGHT.value - Settings.WIN_HEIGHT.value/10), Settings.WIN_WIDTH.value, Settings.WIN_HEIGHT.value/10)


        self.h_grid_lines = []
        self.v_grid_lines = []
        self.get_grid()


    def get_grid(self):
        for line in range(0, int(Settings.WIN_HEIGHT.value/Settings.BLOCK_SIZE.value)):
            self.h_grid_lines.append(line*Settings.BLOCK_SIZE.value)
        for line in range(0, int(Settings.WIN_WIDTH.value/Settings.BLOCK_SIZE.value)):
            self.v_grid_lines.append(line*Settings.BLOCK_SIZE.value)

    
    def draw_grid(self):
        for line_pos in self.h_grid_lines:
            pygame.draw.line(self.game.transparent_surface, Colour.TRANSP_GRAY.value, (0, line_pos), (Settings.WIN_WIDTH.value, line_pos))
        for line_pos in self.v_grid_lines:
            pygame.draw.line(self.game.transparent_surface, Colour.TRANSP_GRAY.value, (line_pos, 0), (line_pos, Settings.WIN_HEIGHT.value))
        self.game.screen.blit(self.game.transparent_surface, (0, 0))

    
    def update(self):
        self.game.screen.fill(Colour.BLACK.value)
        self.draw_grid()
        pygame.draw.rect(self.game.screen, Colour.GRAY.value, self.rect)
