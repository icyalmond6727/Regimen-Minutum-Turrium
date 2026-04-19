import pygame

from scenes.start_menu import StartMenu

class GameManager:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24, bold = True)
        self.current_scene = StartMenu(self)

    def change_scene(self, new_scene):
        self.current_scene = new_scene
    
    def handle_interaction(self, interaction):
        self.current_scene.handle_interaction(interaction)
    
    def update(self):
        self.current_scene.update()
    
    def draw(self, surface):
        self.current_scene.draw(surface)