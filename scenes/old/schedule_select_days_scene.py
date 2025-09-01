import pygame
from typing import TYPE_CHECKING
from .scene_renderer import SceneRenderer

if TYPE_CHECKING:
    from ui import UIManager
    from state import GameState


class ScheduleSelectDaysScene(SceneRenderer):
    def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
        mainRect = pygame.Rect(50, 80, uiManager.screenWidth - 100, 400)
        content_y_start = uiManager.showWindow(mainRect)
        content_x = mainRect.x + uiManager.padding + 20
        yOffset = content_y_start
        for i, day in enumerate(state.daysOfWeek):
            checkbox = "[v]" if state.newScheduleData['days'][i] else "[ ]"
            color = uiManager.colors['font_color'] if i == state.selectedIndices[state.currentScene] else uiManager.colors['inactive_color']
            uiManager.showText(f"{checkbox} {day}", content_x + 40, yOffset, color=color)
            if i == state.selectedIndices[state.currentScene]: uiManager.showCursor(content_x, yOffset + 15, is_cursor_visible)
            yOffset += 40
        color = uiManager.colors['font_color'] if len(state.daysOfWeek) == state.selectedIndices[state.currentScene] else uiManager.colors['inactive_color']
        uiManager.showText("つぎへ", content_x + 40, yOffset + 20, color=color)
        if len(state.daysOfWeek) == state.selectedIndices[state.currentScene]: uiManager.showCursor(content_x, yOffset + 20 + 15, is_cursor_visible)
