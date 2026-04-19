import pygame

import config

from level.level_data import LEVELS

from scenes.in_game import InGame
from scenes.scene import Scene

class MainMenu(Scene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.level_button = {}
        for level_index, data in LEVELS.items():
            x, y, width, height = data["level_button"]
            self.level_button[level_index] = pygame.Rect(x, y, width, height)
    
    def handle_interaction(self, interaction):
        if interaction.type == pygame.MOUSEBUTTONDOWN and interaction.button == 1:
            x, y = interaction.pos

            # Choose level
            for level_index, button in self.level_button.items():
                if button.collidepoint(x, y):
                    self.game_manager.change_scene(InGame(self.game_manager, level_index))
                    break
            
            # Encyclopedia

    def draw(self, surface):
        surface.fill(config.COLOR_BACKGROUND)

        for level_index, button in self.level_button.items():
            pygame.draw.rect(surface, (200, 50, 50), button, border_radius = 5)
            level_text = self.game_manager.font.render(str(level_index), True, (255, 255, 255))
            surface.blit(level_text, (button.centerx - level_text.get_width() / 2, button.centery - level_text.get_height() / 2))