import pygame
from typing import TYPE_CHECKING
from scenes.scene_renderer import SceneRenderer

if TYPE_CHECKING:
    from ui import UIManager
    from state import GameState

class Tasks(SceneRenderer):
    def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
        mainRect = pygame.Rect(50, 80, uiManager.screenWidth - 100, uiManager.screenHeight - 160)
        content_y_start = uiManager.showWindow(mainRect)
        content_x = mainRect.x + uiManager.padding + 12
        yOffset = content_y_start
        if not state.tasksToOrganize:
            uiManager.showText("せいりするタスクはまだありません。", content_x, yOffset)
            return
        line_height = uiManager.fontSmall.get_height() + 20
        max_visible_items = (mainRect.height - (uiManager.padding + 20) * 2) // line_height
        if state.scrollOffset > 0: uiManager.showText("▲", mainRect.right - 30, mainRect.top + 10)
        if state.scrollOffset + max_visible_items < len(state.tasksToOrganize): uiManager.showText("▼", mainRect.right - 30, mainRect.bottom - 30)
        visible_tasks = state.tasksToOrganize[state.scrollOffset : state.scrollOffset + max_visible_items]
        for i, task in enumerate(visible_tasks):
            absolute_index = i + state.scrollOffset
            taskText = f"[{task['status']}] {task['name']}"
            if task['project']: taskText += f" (#{task['project']})"
            color = uiManager.colors['font_color'] if absolute_index == state.selectedIndices[state.currentScene] else uiManager.colors['inactive_color']
            if absolute_index == state.selectedIndices[state.currentScene]: uiManager.showCursor(content_x, yOffset + uiManager.fontSmall.get_height() / 2, is_cursor_visible)
            uiManager.showText(taskText[:40], content_x + 40, yOffset, color=color, font=uiManager.fontSmall)
            yOffset += line_height