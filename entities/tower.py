import pygame

import config

from entities.entity_data import TOWERS
import entities.projectile as projectile

import utils.math_processor as math_processor

class Tower:
    def __init__(self, name, x, y):
        self.__dict__.update(TOWERS[name])
        self.x = x
        self.y = y
        self.current_range = self.range
        self.current_damage = self.damage
        self.current_attack_speed = self.attack_speed
        self.current_bullet_speed = self.bullet_speed
        self.cooldown = 0
        self.target = None

    def update(self, enemies, projectiles, current_frame, event_heap):
        # Attack cooldown
        if (self.cooldown > 0):
            self.cooldown -= 1

        # Find target
        self.target = None
        for enemy in enemies:
            if math_processor.get_distance(self.x, self.y, enemy.x, enemy.y) <= self.current_range:
                if self.target is None or len(enemy.path) - enemy.path_index < len(self.target.path) - self.target.path_index:
                    self.target = enemy
        
        # Attack
        if self.target is not None and self.cooldown == 0:
            interception = math_processor.get_interception(self, self.target)
            if interception is not None:
                hit_x, hit_y, frames_to_hit = interception
                event_heap.push((current_frame + frames_to_hit, "damage", (self.target, self.current_damage)))
                projectiles.append(projectile.Projectile(self.current_bullet_speed, self.x, self.y, hit_x, hit_y))
                self.cooldown = self.current_attack_speed

    def draw(self, surface):
        # Draw tower
        pygame.draw.rect(surface, self.color, (self.x - self.width / 2, self.y - self.height / 2, self.width, self.height))
        
        # Draw range
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.current_range, 1)

        # Draw target line
        if self.target is not None:
            pygame.draw.line(surface, (155, 155, 155), (self.x, self.y), (self.target.x, self.target.y), 2)