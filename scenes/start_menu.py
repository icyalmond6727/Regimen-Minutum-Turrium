import pygame

import config

from scenes.main_menu import MainMenu
from scenes.scene import Scene

class StartMenu(Scene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
    
    def handle_interaction(self, interaction):
        if interaction.type == pygame.MOUSEBUTTONDOWN:
            self.game_manager.change_scene(MainMenu(self.game_manager))

    def draw(self, surface):
        surface.fill(config.COLOR_BACKGROUND)

        game_title = self.game_manager.font.render("REGIMEN MINUTUM TURRIUM", True, (255, 255, 255))
        surface.blit(game_title, (config.WINDOW_WIDTH / 2 - game_title.get_width() / 2, config.WINDOW_HEIGHT / 2 - game_title.get_height() / 2))

        instruction_text = self.game_manager.font.render("CLICK TO START", True, (200, 200, 200))
        surface.blit(instruction_text, (config.WINDOW_WIDTH / 2 - instruction_text.get_width() / 2, config.WINDOW_HEIGHT - 100))