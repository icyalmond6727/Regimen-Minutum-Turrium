import math
import pygame

import config

from core.event_heap import EventHeap

from entities.enemy import Enemy
from entities.entity_data import TOWERS
from entities.tower import Tower

from level.level_builder import Level_Builder

from scenes.defeat_menu import DefeatMenu
from scenes.scene import Scene
from scenes.pause_menu import PauseMenu
from scenes.victory_menu import VictoryMenu

from ui.inspect_menu import InspectMenu
from ui.resource_menu import ResourceMenu
from ui.tower_menu import TowerMenu

import utils.math_processor as math_processor
from utils.quick_sort import quick_sort

class InGame(Scene):
    def __init__(self, game_manager, level_index):
        super().__init__(game_manager)
        self.level = Level_Builder(level_index)
        self.level_index = level_index

        self.enemies = []
        self.towers = []
        self.projectiles = []
        self.event_heap = EventHeap()
        self.gold = self.level.starting_gold
        self.lives = self.level.starting_lives
        self.current_wave = 0
        self.current_frame = 0

        self.wave_button = pygame.Rect(170, 10, 50, 50)
        self.wave_cooldown = self.wave_interval = 0

        self.tower_menu = None
        self.inspect_menu = InspectMenu()
        self.resource_menu = ResourceMenu()

        self.selected_entity = None
    
    def spawn_enemy(self, path_index, enemy_name):
        new_enemy = Enemy(enemy_name, self.level.path_tile_centers[path_index])
        self.enemies.append(new_enemy)

    def start_wave(self):
        if self.current_wave >= len(self.level.waves):
            return

        spawn_time = self.current_frame
        for action in self.level.waves[self.current_wave]:
            type = action[0]
            
            if type == "spawn":
                _, path_index, enemy_name, enemy_count, interval = action
                for _ in range(enemy_count):
                    spawn_time += interval
                    self.event_heap.push((spawn_time, "spawn", (path_index, enemy_name)))
                    
            elif type == "delay":
                _, frames = action
                spawn_time += frames

        self.current_wave += 1
        
        self.wave_interval = (spawn_time - self.current_frame) + (config.FPS * 2)
        self.wave_cooldown = self.wave_interval
    
    def handle_interaction(self, interaction):
        # Escape - Pause
        if interaction.type == pygame.KEYDOWN and interaction.key == pygame.K_ESCAPE:
            self.game_manager.change_scene(PauseMenu(self.game_manager, self))
        
        # Click
        elif interaction.type == pygame.MOUSEBUTTONDOWN and interaction.button == 1:
            x, y = interaction.pos

            # Start wave
            if math_processor.get_distance(x, y, self.wave_button.centerx, self.wave_button.centery) <= self.wave_button.width / 2:
                if self.current_wave < self.level.wave_count and self.wave_cooldown == 0:
                    self.start_wave()
                return

            # Build tower
            keep_menu = False
            if self.tower_menu is not None:
                choice = self.tower_menu.handle_click(x, y)
                if choice in TOWERS:
                    cost = TOWERS[choice]["gold_cost"]
                    if self.gold >= cost:
                        self.gold -= cost
                        new_tower = Tower(choice, self.tower_menu.build_tile_center[0], self.tower_menu.build_tile_center[1])
                        self.towers.append(new_tower)
                        self.level.build_tiles.remove(self.tower_menu.build_tile)
                        self.tower_menu = None
                    else:
                        keep_menu = True
                        print("Not enough gold!")
                elif choice == "close":
                    self.tower_menu = None
            if not keep_menu:
                new_build = False
                for build_tile in self.level.build_tiles:
                    build_tile_center = math_processor.get_tile_center(build_tile[0], build_tile[1], config.TILE_SIZE)
                    if math_processor.get_distance(x, y, build_tile_center[0], build_tile_center[1]) <= config.TILE_SIZE / 2:
                        # Phát hiện click trúng ô đất -> Khởi tạo Menu vòng tròn!
                        self.tower_menu = TowerMenu(build_tile, build_tile_center)
                        new_build = True
                        break
                if not new_build: 
                    self.tower_menu = None
            
            # Inspect towers/enemies
            entity_found = False
            for tower in self.towers:
                if math_processor.get_distance(x, y, tower.x, tower.y) <= tower.width / 2:
                    self.selected_entity = tower
                    entity_found = True
                    break
            if not entity_found:
                for enemy in self.enemies:
                    if math_processor.get_distance(x, y, enemy.x, enemy.y) <= enemy.width / 2:
                        self.selected_entity = enemy
                        entity_found = True
                        break
            if not entity_found:
                self.selected_entity = None

    def update(self):
        self.current_frame += 1
        if self.wave_cooldown > 0:
            self.wave_cooldown -= 1

        self.event_heap.process_events(self.current_frame, self)
        
        for i in range(len(self.enemies) - 1, -1, -1):
            self.enemies[i].update()
            if self.enemies[i].killed:
                self.gold += self.enemies[i].gold_yield
                self.enemies[i], self.enemies[-1] = self.enemies[-1], self.enemies[i]
                self.enemies.pop()
            elif self.enemies[i].ended:
                if self.lives > 0:
                    self.lives -= self.enemies[i].lives_penalty
                self.enemies[i], self.enemies[-1] = self.enemies[-1], self.enemies[i]
                self.enemies.pop()
        
        for i in range(len(self.projectiles) - 1, -1, -1):
            self.projectiles[i].update()
            if self.projectiles[i].ended:
                self.projectiles[i], self.projectiles[-1] = self.projectiles[-1], self.projectiles[i]
                self.projectiles.pop()

        for tower in self.towers:
            tower.update(self.enemies, self.projectiles, self.current_frame, self.event_heap)

        if self.lives <= 0:
            defeat_frame = self.current_frame + config.FPS
            self.event_heap.push((defeat_frame, "defeat", ()))
        if self.current_wave == self.level.wave_count and len(self.enemies) == 0 and self.event_heap.is_empty():
            victory_frame = self.current_frame + config.FPS * 3
            self.event_heap.push((victory_frame, "victory", ()))

    def draw(self, surface):
        surface.fill(config.COLOR_BACKGROUND)
        for x in range(0, config.WINDOW_WIDTH, config.TILE_SIZE):
            pygame.draw.line(surface, config.COLOR_GRID, (x, 0), (x, config.WINDOW_HEIGHT))
        for y in range(0, config.WINDOW_HEIGHT, config.TILE_SIZE):
            pygame.draw.line(surface, config.COLOR_GRID, (0, y), (config.WINDOW_WIDTH, y))

        self.level.draw(surface)
        for tower in self.towers:
            tower.draw(surface)
        sorted_enemies = quick_sort(self.enemies, key = lambda e: -e.distance_left)
        for enemy in sorted_enemies:
            enemy.draw(surface)
        for projectile in self.projectiles:
            projectile.draw(surface)

        self.resource_menu.draw(surface, self.game_manager, self)
        self.inspect_menu.draw(surface, self.game_manager, self.selected_entity)
        
        if self.tower_menu is not None:
            self.tower_menu.draw(surface)