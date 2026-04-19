import pygame

import config

from scenes.scene import Scene

class PauseMenu(Scene):
    def __init__(self, game_manager, previous_scene):
        super().__init__(game_manager)
        self.previous_scene = previous_scene

        menu_width = 540
        menu_height = 250
        center_x, center_y = config.WINDOW_WIDTH / 2, config.WINDOW_HEIGHT / 2
        self.menu = pygame.Rect(center_x - menu_width / 2, center_y - menu_height / 2, menu_width, menu_height)
        self.button_left = pygame.Rect(self.menu.left + 40, self.menu.bottom - 80, 140, 50)
        self.button_middle = pygame.Rect(self.menu.left + 40 + 140 + 20, self.menu.bottom - 80, 140, 50)
        self.button_right = pygame.Rect(self.menu.left + 40 + (140 + 20) * 2, self.menu.bottom - 80, 140, 50)

    def handle_interaction(self, interaction):
        # Escape - Resume
        if interaction.type == pygame.KEYDOWN and interaction.key == pygame.K_ESCAPE:
            self.game_manager.change_scene(self.previous_scene)

        # Click
        elif interaction.type == pygame.MOUSEBUTTONDOWN and interaction.button == 1:
            x, y = interaction.pos

            # Restart
            if self.button_left.collidepoint(x, y):
                from scenes.in_game import InGame
                self.game_manager.change_scene(InGame(self.game_manager, self.previous_scene.level_index))

            # Main Menu
            elif self.button_middle.collidepoint(x, y):
                from scenes.main_menu import MainMenu
                self.game_manager.change_scene(MainMenu(self.game_manager))
            
            # Resume
            elif self.button_right.collidepoint(x, y):
                self.game_manager.change_scene(self.previous_scene)

    def update(self):
        pass

    def draw(self, surface):
        self.previous_scene.draw(surface)

        overlay = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        pygame.draw.rect(surface, (50, 50, 50), self.menu, border_radius = 10)
        pygame.draw.rect(surface, (200, 200, 200), self.menu, width = 3, border_radius = 10)

        title = self.game_manager.font.render("PAUSE", True, (255, 200, 0))
        surface.blit(title, (self.menu.centerx - title.get_width() / 2, self.menu.top + 40))

        pygame.draw.rect(surface, (100, 100, 100), self.button_left, border_radius = 5)
        text_left = self.game_manager.font.render("Restart", True, (255, 255, 255))
        surface.blit(text_left, (self.button_left.centerx - text_left.get_width() / 2, self.button_left.centery - text_left.get_height() / 2))

        pygame.draw.rect(surface, (100, 100, 100), self.button_middle, border_radius = 5)
        text_middle = self.game_manager.font.render("Main Menu", True, (255, 255, 255))
        surface.blit(text_middle, (self.button_middle.centerx - text_middle.get_width() / 2, self.button_middle.centery - text_middle.get_height() / 2))

        pygame.draw.rect(surface, (100, 100, 100), self.button_right, border_radius = 5)
        text_right = self.game_manager.font.render("Resume", True, (255, 255, 255))
        surface.blit(text_right, (self.button_right.centerx - text_right.get_width() / 2, self.button_right.centery - text_right.get_height() / 2))