import pygame
from typing import TYPE_CHECKING
from scenes.scene_renderer import SceneRenderer

if TYPE_CHECKING:
    from ui import UIManager
    from state import GameState

class Confirm(SceneRenderer):
    def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
        mainRect = pygame.Rect(50, 80, uiManager.screenWidth - 100, 400)
        content_y_start = uiManager.showWindow(mainRect)
        content_x = mainRect.x + uiManager.padding + 20
        yOffset = content_y_start
        uiManager.showText(f"なまえ: {state.newScheduleData['name']}", content_x, yOffset)
        yOffset += 40
        days_str = " ".join([state.daysOfWeek[i][:1] for i, v in enumerate(state.newScheduleData['days']) if v])
        uiManager.showText(f"ようび: {days_str if days_str else 'なし'}", content_x, yOffset)
        yOffset += 40
        uiManager.showText(f"じこく: {state.newScheduleData['time']}", content_x, yOffset)
        yOffset += 80
        for i, option in enumerate(state.confirmOptions):
            color = uiManager.colors['font_color'] if i == state.selectedIndices[state.currentScene] else uiManager.colors['inactive_color']
            uiManager.showText(option, content_x + 40, yOffset + i * 50, color=color)
            if i == state.selectedIndices[state.currentScene]: uiManager.showCursor(content_x, yOffset + i * 50 + 15, is_cursor_visible)