import pygame
from typing import TYPE_CHECKING
from scenes.scene_renderer import SceneRenderer

if TYPE_CHECKING:
    from ui import UIManager
    from state import GameState

class ChooseStrategy(SceneRenderer):
    def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
        mainRect = pygame.Rect(50, 80, uiManager.screenWidth - 100, 300)
        content_y_start = uiManager.showWindow(mainRect)
        content_start_x = mainRect.x + uiManager.padding + 20
        for i, option in enumerate(state.strategyOptions):
            y = content_y_start + i * 50
            uiManager.showText(option, content_start_x + 40, y)
            if i == state.selectedIndices[state.currentScene]:
                uiManager.showCursor(content_start_x, y + 15, is_cursor_visible)