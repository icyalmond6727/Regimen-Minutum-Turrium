import pygame
import config

class InspectMenu:
    def __init__(self):
        self.dock_h = 100
        self.dock_rect = pygame.Rect(0, config.WINDOW_HEIGHT - self.dock_h, config.WINDOW_WIDTH, self.dock_h)

    def draw(self, surface, game_manager, selected_entity):
        if selected_entity is None:
            return
        
        pygame.draw.rect(surface, (20, 20, 25), self.dock_rect)
        pygame.draw.line(surface, (0, 255, 255), (0, config.WINDOW_HEIGHT - self.dock_h), (config.WINDOW_WIDTH, config.WINDOW_HEIGHT - self.dock_h), 2)

        e = selected_entity
        name_txt = game_manager.font.render(f"UNIT: {e.name.upper()}", True, (0, 255, 255))
        surface.blit(name_txt, (30, config.WINDOW_HEIGHT - 85))

        if hasattr(e, 'damage'):
            stats = f"DAMAGE: {e.current_damage} | RANGE: {e.current_range} | ATTACK SPEED: {e.current_attack_speed} | BULLET SPEED: {e.current_bullet_speed}"
            color = (100, 200, 255)
        else:
            hp_ratio = f"{int(e.current_health)}/{e.health}"
            stats = f"HP: {hp_ratio} | SPEED: {e.current_speed} | REWARD: {e.gold_yield}"
            color = (255, 100, 100)

        stats_txt = game_manager.font.render(stats, True, color)
        surface.blit(stats_txt, (30, config.WINDOW_HEIGHT - 50))