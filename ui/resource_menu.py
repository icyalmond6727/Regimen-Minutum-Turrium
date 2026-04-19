import pygame
import math
import config

class ResourceMenu:
    def __init__(self):
        self.hud_rect = pygame.Rect(10, 10, 160, 95)

    def draw(self, surface, game_manager, in_game_scene):
        pygame.draw.rect(surface, (40, 40, 45), self.hud_rect, border_radius = 8)
        pygame.draw.rect(surface, (100, 100, 110), self.hud_rect, width = 2, border_radius = 8)

        gold_txt = game_manager.font.render(f"GOLD: {in_game_scene.gold}", True, (255, 215, 0))
        lives_txt = game_manager.font.render(f"LIVES: {in_game_scene.lives}", True, (255, 50, 50))
        wave_txt = game_manager.font.render(f"WAVE: {in_game_scene.current_wave}/{in_game_scene.level.wave_count}", True, (255, 255, 255))
        
        surface.blit(gold_txt, (25, 15))
        surface.blit(lives_txt, (25, 45))
        surface.blit(wave_txt, (25, 75))

        btn = in_game_scene.wave_button
        pygame.draw.circle(surface, (0, 120, 180), btn.center, btn.width / 2)
        
        if in_game_scene.current_wave < in_game_scene.level.wave_count:
            if in_game_scene.wave_cooldown > 0:
                arc_rect = btn.inflate(12, 12)
                ratio = in_game_scene.wave_cooldown / in_game_scene.wave_interval
                start_angle = math.pi / 2
                stop_angle = math.pi / 2 + (2 * math.pi * ratio)
                pygame.draw.arc(surface, (0, 255, 255), arc_rect, start_angle, stop_angle, 4)
            else:
                pygame.draw.circle(surface, (200, 200, 200), btn.center, btn.width // 2, 2)
        
        cx, cy = btn.center
        play_icon = [(cx - 5, cy - 10), (cx - 5, cy + 10), (cx + 12, cy)]
        pygame.draw.polygon(surface, (255, 255, 255), play_icon)