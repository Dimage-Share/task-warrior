import pygame
from typing import TYPE_CHECKING
from scenes.scene_renderer import SceneRenderer

if TYPE_CHECKING:
    from ui import UIManager
    from state import GameState

class List(SceneRenderer):
    def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
        mainRect = pygame.Rect(50, 80, uiManager.screenWidth - 100, uiManager.screenHeight - 160)
        content_y_start = uiManager.showWindow(mainRect)
        content_x = mainRect.x + uiManager.padding + 12
        yOffset = content_y_start
        list_with_add_button = ["あたらしいよてい"] + state.scheduleList
        max_visible_items = 10
        if state.scrollOffset > 0: uiManager.showText("▲", mainRect.right - 30, mainRect.top + 10)
        if state.scrollOffset + max_visible_items < len(list_with_add_button): uiManager.showText("▼", mainRect.right - 30, mainRect.bottom - 30)
        visible_items = list_with_add_button[state.scrollOffset : state.scrollOffset + max_visible_items]

        for i, item in enumerate(visible_items):
            absolute_index = i + state.scrollOffset
            is_selected = absolute_index == state.selectedIndices[state.currentScene]
            
            if is_selected:
                uiManager.showCursor(content_x, yOffset + uiManager.fontSmall.get_height() / 2, is_cursor_visible)

            if isinstance(item, str):
                color = uiManager.colors['font_color'] if is_selected else uiManager.colors['inactive_color']
                uiManager.showText(f"＋ {item}", content_x + 40, yOffset, color=color)
            else:
                base_color = uiManager.colors['font_color'] if item['is_enabled'] else uiManager.colors['inactive_color']
                color = base_color if is_selected else uiManager.colors['inactive_color']
                days_map = state.daysOfWeek
                days_short = "".join([days_map[d][:1] for d, v in enumerate(item['days']) if v == '1'])
                schedule_text = f"{item['time_str']} [{days_short if days_short else '一回'}] {item['name']}"
                uiManager.showText(schedule_text, content_x + 40, yOffset, color=color, font=uiManager.fontSmall)
            
            yOffset += uiManager.fontSmall.get_height() + 15