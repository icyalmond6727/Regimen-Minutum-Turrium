import math
import pygame

import config
import entities.entity_data as entity_data

class TowerMenu:
    def __init__(self, build_tile, build_tile_center):
        self.build_tile = build_tile
        self.build_tile_center = build_tile_center
        
        self.buttons = {} 
        self.tower_options = ["Pulse Blaster", "Railgun Sentinel"] 
        
        radius = config.TILE_SIZE * 0.3
        button_sz = 40

        for i, tower_name in enumerate(self.tower_options):
            angle = math.radians(i * (360 / len(self.tower_options)) - 90)
            
            button_x = self.build_tile_center[0] + radius * math.cos(angle)
            button_y = self.build_tile_center[1] + radius * math.sin(angle)
            
            self.buttons[tower_name] = pygame.Rect(int(button_x - button_sz / 2), int(button_y - button_sz / 2), button_sz, button_sz)

    def draw(self, surface):
        for name, rect in self.buttons.items():
            pygame.draw.rect(surface, (100, 100, 100), rect, border_radius = 5)
            icon_rect = rect.inflate(-10, -10)
            pygame.draw.rect(surface, entity_data.TOWERS[name]["color"], icon_rect, border_radius = 5)
    
    def handle_click(self, x, y):
        for name, rect in self.buttons.items():
            if rect.collidepoint(x, y):
                return name
        return "close"