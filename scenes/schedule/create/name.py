import pygame
from typing import TYPE_CHECKING
from scenes.scene_renderer import SceneRenderer

if TYPE_CHECKING:
    from ui import UIManager
    from state import GameState

class Name(SceneRenderer):
    def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool, prompt="よていのなまえをにゅうりょく"):
        mainRect = pygame.Rect(50, 80, uiManager.screenWidth - 100, 150)
        content_y_start = uiManager.showWindow(mainRect)
        content_x = mainRect.x + uiManager.padding + 12
        uiManager.showText(prompt, content_x, content_y_start, font=uiManager.fontSmall)
        inputRect = pygame.Rect(content_x, content_y_start + 35, mainRect.width - (uiManager.padding + 12) * 2, 40)
        pygame.draw.rect(uiManager.screen, uiManager.colors['background'], inputRect)
        uiManager.showText(state.inputText + "_", inputRect.x + 10, inputRect.y + 5)