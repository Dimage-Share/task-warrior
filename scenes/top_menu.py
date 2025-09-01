import pygame
from typing import TYPE_CHECKING
from state import TopMenuFocus
from scenes.scene_renderer import SceneRenderer
from scene import Scene

if TYPE_CHECKING:
    from ui import UIManager
    from state import GameState


class TopMenu(SceneRenderer):
    def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
        color_100 = pygame.Color("#ff4500")
        color_0 = pygame.Color("#87cefa")
        ratio = state.motivationValue / 100.0
        border_color = color_0.lerp(color_100, ratio)

        menu_rect, menu_height = self._showCommands(uiManager, state, is_cursor_visible, border_color)
        schedule_rect = self._showUpcomingSchedules(uiManager, state, menu_rect, menu_height, border_color)
        self._showProjects(uiManager, state, is_cursor_visible, menu_rect, schedule_rect, border_color)
        self._showInbox(uiManager, state, menu_rect, border_color)

    def _showCommands(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool, border_color):
        menu_config = self.config.get("menu", {})
        margin = menu_config.get("margin", {"left": 32, "top": 32, "right": 32, "bottom": 32})
        col_margin = menu_config.get("column_margin", 220)
        items = state.topMenuOptions
        num_rows = len(items)
        num_cols = len(items[0]) if num_rows > 0 else 0
        
        row_padding = int(uiManager.font.get_height() * 0.2)
        row_height = uiManager.font.get_height() + row_padding
        
        cursor_offset = 30 
        col_widths = [0] * num_cols
        for r in range(num_rows):
            for c in range(num_cols):
                option = items[r][c]
                if option:
                    text_surf = uiManager.font.render(option, True, (0,0,0))
                    col_widths[c] = max(col_widths[c], text_surf.get_width())

        total_text_width = sum(col_widths)
        total_gaps_width = (num_cols - 1) * col_margin
        menu_content_width = cursor_offset + total_text_width + total_gaps_width
        
        menu_width = margin["left"] + menu_content_width + margin["right"]
        menu_height = margin["top"] + (num_rows - 1) * row_height + uiManager.font.get_height() + margin["bottom"]
        
        menu_origin = menu_config.get("origin", {"x": 32, "y": 64})
        menuRect = pygame.Rect(menu_origin['x'], menu_origin['y'], menu_width, menu_height)
        content_start_y_commands = uiManager.showWindow(menuRect, "ねぶか", border_color=border_color)

        content_start_x = menuRect.x + margin["left"]
        text_start_x = content_start_x + cursor_offset
        
        selected_row, selected_col = state.selectedIndices[Scene.TOP_MENU]

        for r, row_items in enumerate(items):
            current_col_offset = 0
            for c, option in enumerate(row_items):
                if option is None:
                    current_col_offset += col_widths[c] + col_margin
                    continue
                
                x_pos = text_start_x + current_col_offset
                y_pos = content_start_y_commands + r * row_height
                
                color = uiManager.colors['font_color'] if state.topMenuFocus == TopMenuFocus.COMMANDS else uiManager.colors['inactive_color']
                uiManager.showText(option, x_pos, y_pos, color=color)

                if r == selected_row and c == selected_col and state.topMenuFocus == TopMenuFocus.COMMANDS:
                    uiManager.showCursor(x_pos - cursor_offset, y_pos + uiManager.font.get_height() // 2, is_cursor_visible)
                
                current_col_offset += col_widths[c] + col_margin
        
        return menuRect, menu_height

    def _showUpcomingSchedules(self, uiManager: 'UIManager', state: 'GameState', menuRect, menu_height, border_color):
        scheduleRect = pygame.Rect(menuRect.right + 20, menuRect.top, uiManager.screenWidth - menuRect.right - 40, menu_height)
        uiManager.showWindow(scheduleRect, "つぎのよてい", border_color=border_color)
        
        y_offset = scheduleRect.y + uiManager.padding + 40
        if not state.upcomingSchedules:
            uiManager.showText("とうろくされたよていはありません。", scheduleRect.x + uiManager.padding + 12, y_offset, font=uiManager.fontSmall)
        else:
            for schedule in state.upcomingSchedules:
                day_str = schedule['datetime'].strftime('%m/%d')
                time_str = schedule['datetime'].strftime('%H:%M')
                day_of_week = state.daysOfWeek[schedule['datetime'].weekday()][:1]
                
                display_text = f"{day_str}({day_of_week}) {time_str} {schedule['name']}"
                uiManager.showText(display_text, scheduleRect.x + uiManager.padding + 12, y_offset, font=uiManager.fontSmall)
                y_offset += 30
        return scheduleRect

    def _showProjects(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool, menuRect, scheduleRect, border_color):
        projectRect = pygame.Rect(menuRect.right + 20, scheduleRect.bottom + 20, uiManager.screenWidth - menuRect.right - 40, uiManager.screenHeight - scheduleRect.bottom - 144)
        content_y_start_projects = uiManager.showWindow(projectRect, "プロジェクト", border_color=border_color)
        y_offset = content_y_start_projects
        if not state.projectList:
            uiManager.showText("プロジェクトはまだありません。", projectRect.x + uiManager.padding + 12, y_offset, font=uiManager.fontSmall)
        else:
            for i, project_name in enumerate(state.projectList):
                color = uiManager.colors['font_color'] if state.topMenuFocus == TopMenuFocus.PROJECTS else uiManager.colors['inactive_color']
                uiManager.showText(project_name, projectRect.x + uiManager.padding + 42, y_offset, font=uiManager.fontSmall, color=color)
                if i == state.projectListIndex and state.topMenuFocus == TopMenuFocus.PROJECTS:
                    uiManager.showCursor(projectRect.x + uiManager.padding + 12, y_offset + uiManager.fontSmall.get_height() // 2, is_cursor_visible)
                y_offset += 30

    def _showInbox(self, uiManager: 'UIManager', state: 'GameState', menuRect, border_color):
        inboxRect = pygame.Rect(menuRect.left, menuRect.bottom + 20, menuRect.width, uiManager.screenHeight - menuRect.bottom - 144)
        content_y_start_inbox = uiManager.showWindow(inboxRect, "Inbox", border_color=border_color)
        y_offset = content_y_start_inbox
        if not state.inboxTasks:
            uiManager.showText("Inboxはからっぽです。", inboxRect.x + uiManager.padding + 12, y_offset, font=uiManager.fontSmall)
        else:
            for task in state.inboxTasks:
                uiManager.showText(f"・{task['name']}", inboxRect.x + uiManager.padding + 12, y_offset, font=uiManager.fontSmall)
                y_offset += 30