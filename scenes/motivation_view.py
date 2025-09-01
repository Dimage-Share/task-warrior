import pygame
from typing import TYPE_CHECKING
from scenes.scene_renderer import SceneRenderer
from .top_menu import TopMenu

if TYPE_CHECKING:
    from ui import UIManager
    from state import GameState


class MotivationView(SceneRenderer):
    def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
        TopMenu(self.config).show(uiManager, state, is_cursor_visible)

        overlay = pygame.Surface((uiManager.screenWidth, uiManager.screenHeight), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        uiManager.screen.blit(overlay, (0, 0))

        mainRect = pygame.Rect(50, 80, uiManager.screenWidth - 100, uiManager.screenHeight - 160)
        uiManager.showWindow(mainRect)

        color_100 = pygame.Color("#ff4500")
        color_0 = pygame.Color("#87cefa")
        
        value = state.motivationValue
        ratio = value / 100.0
        
        interpolated_color = color_0.lerp(color_100, ratio)

        try:
            large_font_size = int(uiManager.screenHeight / 5)
            large_font = pygame.font.Font(self.config["font"]["path"], large_font_size)
        except Exception:
            large_font = uiManager.font

        text_to_show = f"{value}%"
        text_surf = large_font.render(text_to_show, True, interpolated_color)
        text_rect = text_surf.get_rect(center=mainRect.center)

        uiManager.screen.blit(text_surf, text_rect)

        cursor_x = text_rect.left - 40
        cursor_y = text_rect.centery
        uiManager.showCursor(cursor_x, cursor_y, is_cursor_visible)