import pygame
from typing import TYPE_CHECKING
from scenes.scene_renderer import SceneRenderer
from .tasks import Tasks

if TYPE_CHECKING:
    from ui import UIManager
    from state import GameState

class Submenu(SceneRenderer):
    def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
        Tasks(self.config).show(uiManager, state, is_cursor_visible)
        overlay = pygame.Surface((uiManager.screenWidth, uiManager.screenHeight), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        uiManager.screen.blit(overlay, (0, 0))
        menuW, menuH = 200, 120
        menuRect = pygame.Rect((uiManager.screenWidth - menuW) // 2, (uiManager.screenHeight - menuH) // 2, menuW, menuH)
        content_y_start = uiManager.showWindow(menuRect)
        content_start_x = menuRect.x + uiManager.padding + 20
        for i, option in enumerate(state.organizeSubmenuOptions):
            y = content_y_start + i * 45
            uiManager.showText(option, content_start_x + 40, y)
            if i == state.selectedIndices[state.currentScene]: uiManager.showCursor(content_start_x, y + 15, is_cursor_visible)