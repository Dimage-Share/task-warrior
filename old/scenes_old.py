# import pygame
# import textwrap
# from typing import TYPE_CHECKING
# from state import TopMenuFocus

# if TYPE_CHECKING:
#     from ui import UIManager
#     from state import GameState

# class SceneRenderer:
#     def __init__(self, config):
#         self.config = config
#     def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
#         pass

# class TopMenuScene(SceneRenderer):
#     def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
#         menu_config = self.config.get("menu", {})
#         margin = menu_config.get("margin", {"left": 32, "top": 32, "right": 32, "bottom": 32})
#         col_margin = menu_config.get("column_margin", 220)
#         items = state.topMenuOptions
#         num_rows = len(items)
#         num_cols = len(items[0]) if num_rows > 0 else 0
        
#         row_padding = int(uiManager.font.get_height() * 1.2)
#         row_height = uiManager.font.get_height() + row_padding
        
#         cursor_offset = 30 
#         col_widths = [0] * num_cols
#         for r in range(num_rows):
#             for c in range(num_cols):
#                 option = items[r][c]
#                 if option:
#                     text_surf = uiManager.font.render(option, True, (0,0,0))
#                     col_widths[c] = max(col_widths[c], text_surf.get_width())

#         total_text_width = sum(col_widths)
#         total_gaps_width = (num_cols - 1) * col_margin
#         menu_content_width = cursor_offset + total_text_width + total_gaps_width
        
#         menu_width = margin["left"] + menu_content_width + margin["right"]
#         menu_height = margin["top"] + (num_rows - 1) * row_height + uiManager.font.get_height() + margin["bottom"]
        
#         menu_origin = menu_config.get("origin", {"x": 32, "y": 64})
#         menuRect = pygame.Rect(menu_origin['x'], menu_origin['y'], menu_width, menu_height)
#         content_start_y_commands = uiManager.showWindow(menuRect, "ねぶか")
#         content_start_x = menuRect.x + margin["left"]
#         text_start_x = content_start_x + cursor_offset
#         selected_row, selected_col = state.selectedIndices[state.currentScene]
#         for r, row_items in enumerate(items):
#             current_col_offset = 0
#             for c, option in enumerate(row_items):
#                 if option is None:
#                     current_col_offset += col_widths[c] + col_margin
#                     continue
                
#                 x_pos = text_start_x + current_col_offset
#                 y_pos = content_start_y_commands + r * row_height
#                 color = uiManager.colors['font_color'] if state.topMenuFocus == TopMenuFocus.COMMANDS else uiManager.colors['inactive_color']
#                 uiManager.showText(option, x_pos, y_pos, color=color)

#                 if r == selected_row and c == selected_col and state.topMenuFocus == TopMenuFocus.COMMANDS:
#                     uiManager.showCursor(x_pos - cursor_offset, y_pos + uiManager.font.get_height() // 2, is_cursor_visible)
                
#                 current_col_offset += col_widths[c] + col_margin
        
#         scheduleRect = pygame.Rect(menuRect.right + 20, menuRect.top, uiManager.screenWidth - menuRect.right - 40, menu_height)
#         uiManager.showWindow(scheduleRect, "つぎのよてい")
#         y_offset = scheduleRect.y + uiManager.padding + 40
#         if not state.upcomingSchedules:
#             uiManager.showText("とうろくされたよていはありません。", scheduleRect.x + uiManager.padding + 12, y_offset, font=uiManager.fontSmall)
#         else:
#             for schedule in state.upcomingSchedules:
#                 day_str = schedule['datetime'].strftime('%m/%d')
#                 time_str = schedule['datetime'].strftime('%H:%M')
#                 day_of_week = state.daysOfWeek[schedule['datetime'].weekday()][:1]
#                 display_text = f"{day_str}({day_of_week}) {time_str} {schedule['name']}"
#                 uiManager.showText(display_text, scheduleRect.x + uiManager.padding + 12, y_offset, font=uiManager.fontSmall)
#                 y_offset += 30
        
#         projectRect = pygame.Rect(menuRect.right + 20, scheduleRect.bottom + 20, uiManager.screenWidth - menuRect.right - 40, uiManager.screenHeight - scheduleRect.bottom - 100)
#         content_y_start_projects = uiManager.showWindow(projectRect, "プロジェクト")
#         y_offset = content_y_start_projects
#         if not state.projectList:
#             uiManager.showText("プロジェクトはまだありません。", projectRect.x + uiManager.padding + 12, y_offset, font=uiManager.fontSmall)
#         else:
#             for i, project_name in enumerate(state.projectList):
#                 color = uiManager.colors['font_color'] if state.topMenuFocus == TopMenuFocus.PROJECTS else uiManager.colors['inactive_color']
#                 uiManager.showText(project_name, projectRect.x + uiManager.padding + 42, y_offset, font=uiManager.fontSmall, color=color)
#                 if i == state.projectListIndex and state.topMenuFocus == TopMenuFocus.PROJECTS:
#                     uiManager.showCursor(projectRect.x + uiManager.padding + 12, y_offset + uiManager.fontSmall.get_height() // 2, is_cursor_visible)
#                 y_offset += 30

# class DiaryInputScene(SceneRenderer):
#     def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
#         mainRect = pygame.Rect(50, 80, uiManager.screenWidth - 100, 150)
#         content_y_start = uiManager.showWindow(mainRect)
#         content_x = mainRect.x + uiManager.padding + 12
#         uiManager.showText("きょうのできごとをどうぞ", content_x, content_y_start, font=uiManager.fontSmall, color=uiManager.colors['inactive_color'])
#         inputRect = pygame.Rect(content_x, content_y_start + 35, mainRect.width - (uiManager.padding + 12) * 2, 40)
#         pygame.draw.rect(uiManager.screen, uiManager.colors['background'], inputRect)
#         uiManager.showText(state.inputText + "_", inputRect.x + 10, inputRect.y + 5)

# class InputTaskScene(SceneRenderer):
#     def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
#         mainRect = pygame.Rect(50, 80, uiManager.screenWidth - 100, 150)
#         content_y_start = uiManager.showWindow(mainRect)
#         content_x = mainRect.x + uiManager.padding + 12
#         uiManager.showText("（#プロジェクト名 でプロジェクト指定可）", content_x, content_y_start, font=uiManager.fontSmall, color=uiManager.colors['inactive_color'])
#         inputRect = pygame.Rect(content_x, content_y_start + 35, mainRect.width - (uiManager.padding + 12) * 2, 40)
#         pygame.draw.rect(uiManager.screen, uiManager.colors['background'], inputRect)
#         uiManager.showText(state.inputText + "_", inputRect.x + 10, inputRect.y + 5)

# class ChooseStrategyScene(SceneRenderer):
#     def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
#         mainRect = pygame.Rect(50, 80, uiManager.screenWidth - 100, 300)
#         content_y_start = uiManager.showWindow(mainRect)
#         content_start_x = mainRect.x + uiManager.padding + 20
#         for i, option in enumerate(state.strategyOptions):
#             y = content_y_start + i * 50
#             uiManager.showText(option, content_start_x + 40, y)
#             if i == state.selectedIndices[state.currentScene]:
#                 uiManager.showCursor(content_start_x, y + 15, is_cursor_visible)

# class MapViewScene(SceneRenderer):
#     def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
#         mainRect = pygame.Rect(50, 80, uiManager.screenWidth - 100, uiManager.screenHeight - 160)
#         content_y_start = uiManager.showWindow(mainRect)
#         content_x = mainRect.x + uiManager.padding + 12
#         uiManager.showText("マップはまだえがかれていない。", content_x, content_y_start)

# class OrganizeTasksScene(SceneRenderer):
#     def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
#         mainRect = pygame.Rect(50, 80, uiManager.screenWidth - 100, uiManager.screenHeight - 160)
#         content_y_start = uiManager.showWindow(mainRect)
#         content_x = mainRect.x + uiManager.padding + 12
#         yOffset = content_y_start
#         if not state.tasksToOrganize:
#             uiManager.showText("せいりするタスクはまだありません。", content_x, yOffset)
#             return
#         line_height = uiManager.fontSmall.get_height() + 20
#         max_visible_items = (mainRect.height - (uiManager.padding + 20) * 2) // line_height
#         if state.scrollOffset > 0: uiManager.showText("▲", mainRect.right - 30, mainRect.top + 10)
#         if state.scrollOffset + max_visible_items < len(state.tasksToOrganize): uiManager.showText("▼", mainRect.right - 30, mainRect.bottom - 30)
#         visible_tasks = state.tasksToOrganize[state.scrollOffset : state.scrollOffset + max_visible_items]
#         for i, task in enumerate(visible_tasks):
#             absolute_index = i + state.scrollOffset
#             taskText = f"[{task['status']}] {task['name']}"
#             if task['project']: taskText += f" (#{task['project']})"
#             color = uiManager.colors['font_color'] if absolute_index == state.selectedIndices[state.currentScene] else uiManager.colors['inactive_color']
#             if absolute_index == state.selectedIndices[state.currentScene]: uiManager.showCursor(content_x, yOffset + uiManager.fontSmall.get_height() / 2, is_cursor_visible)
#             uiManager.showText(taskText[:40], content_x + 40, yOffset, color=color, font=uiManager.fontSmall)
#             yOffset += line_height

# class OrganizeSubmenuScene(SceneRenderer):
#     def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
#         OrganizeTasksScene(self.config).show(uiManager, state, is_cursor_visible)
#         overlay = pygame.Surface((uiManager.screenWidth, uiManager.screenHeight), pygame.SRCALPHA)
#         overlay.fill((0, 0, 0, 180))
#         uiManager.screen.blit(overlay, (0, 0))
#         menuW, menuH = 200, 120
#         menuRect = pygame.Rect((uiManager.screenWidth - menuW) // 2, (uiManager.screenHeight - menuH) // 2, menuW, menuH)
#         content_y_start = uiManager.showWindow(menuRect)
#         content_start_x = menuRect.x + uiManager.padding + 20
#         for i, option in enumerate(state.organizeSubmenuOptions):
#             y = content_y_start + i * 45
#             uiManager.showText(option, content_start_x + 40, y)
#             if i == state.selectedIndices[state.currentScene]: uiManager.showCursor(content_start_x, y + 15, is_cursor_visible)

# class ScheduleInputNameScene(SceneRenderer):
#     def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool, prompt="よていのなまえをにゅうりょく"):
#         mainRect = pygame.Rect(50, 80, uiManager.screenWidth - 100, 150)
#         content_y_start = uiManager.showWindow(mainRect)
#         content_x = mainRect.x + uiManager.padding + 12
#         uiManager.showText(prompt, content_x, content_y_start, font=uiManager.fontSmall)
#         inputRect = pygame.Rect(content_x, content_y_start + 35, mainRect.width - (uiManager.padding + 12) * 2, 40)
#         pygame.draw.rect(uiManager.screen, uiManager.colors['background'], inputRect)
#         uiManager.showText(state.inputText + "_", inputRect.x + 10, inputRect.y + 5)

# class ScheduleSelectDaysScene(SceneRenderer):
#     def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
#         mainRect = pygame.Rect(50, 80, uiManager.screenWidth - 100, 400)
#         content_y_start = uiManager.showWindow(mainRect)
#         content_x = mainRect.x + uiManager.padding + 20
#         yOffset = content_y_start
#         for i, day in enumerate(state.daysOfWeek):
#             checkbox = "[v]" if state.newScheduleData['days'][i] else "[ ]"
#             color = uiManager.colors['font_color'] if i == state.selectedIndices[state.currentScene] else uiManager.colors['inactive_color']
#             uiManager.showText(f"{checkbox} {day}", content_x + 40, yOffset, color=color)
#             if i == state.selectedIndices[state.currentScene]: uiManager.showCursor(content_x, yOffset + 15, is_cursor_visible)
#             yOffset += 40
#         color = uiManager.colors['font_color'] if len(state.daysOfWeek) == state.selectedIndices[state.currentScene] else uiManager.colors['inactive_color']
#         uiManager.showText("つぎへ", content_x + 40, yOffset + 20, color=color)
#         if len(state.daysOfWeek) == state.selectedIndices[state.currentScene]: uiManager.showCursor(content_x, yOffset + 20 + 15, is_cursor_visible)

# class ScheduleSelectTimeScene(SceneRenderer):
#     def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool, prompt="じこくをにゅうりょく (HH:MM)"):
#         mainRect = pygame.Rect(50, 80, uiManager.screenWidth - 100, 150)
#         content_y_start = uiManager.showWindow(mainRect)
#         content_x = mainRect.x + uiManager.padding + 12
#         uiManager.showText(prompt, content_x, content_y_start, font=uiManager.fontSmall)
#         inputRect = pygame.Rect(content_x, content_y_start + 35, mainRect.width - (uiManager.padding + 12) * 2, 40)
#         pygame.draw.rect(uiManager.screen, uiManager.colors['background'], inputRect)
#         uiManager.showText(state.inputText + "_", inputRect.x + 10, inputRect.y + 5)

# class ScheduleConfirmScene(SceneRenderer):
#     def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
#         mainRect = pygame.Rect(50, 80, uiManager.screenWidth - 100, 400)
#         content_y_start = uiManager.showWindow(mainRect)
#         content_x = mainRect.x + uiManager.padding + 20
#         yOffset = content_y_start
#         uiManager.showText(f"なまえ: {state.newScheduleData['name']}", content_x, yOffset)
#         yOffset += 40
#         days_str = " ".join([state.daysOfWeek[i][:1] for i, v in enumerate(state.newScheduleData['days']) if v])
#         uiManager.showText(f"ようび: {days_str if days_str else 'なし'}", content_x, yOffset)
#         yOffset += 40
#         uiManager.showText(f"じこく: {state.newScheduleData['time']}", content_x, yOffset)
#         yOffset += 80
#         for i, option in enumerate(state.confirmOptions):
#             color = uiManager.colors['font_color'] if i == state.selectedIndices[state.currentScene] else uiManager.colors['inactive_color']
#             uiManager.showText(option, content_x + 40, yOffset + i * 50, color=color)
#             if i == state.selectedIndices[state.currentScene]: uiManager.showCursor(content_x, yOffset + i * 50 + 15, is_cursor_visible)

# class ScheduleListScene(SceneRenderer):
#     def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
#         mainRect = pygame.Rect(50, 80, uiManager.screenWidth - 100, uiManager.screenHeight - 160)
#         content_y_start = uiManager.showWindow(mainRect)
#         content_x = mainRect.x + uiManager.padding + 12
#         yOffset = content_y_start
#         list_with_add_button = ["あたらしいよてい"] + state.scheduleList
#         max_visible_items = 10
#         if state.scrollOffset > 0: uiManager.showText("▲", mainRect.right - 30, mainRect.top + 10)
#         if state.scrollOffset + max_visible_items < len(list_with_add_button): uiManager.showText("▼", mainRect.right - 30, mainRect.bottom - 30)
#         visible_items = list_with_add_button[state.scrollOffset : state.scrollOffset + max_visible_items]

#         for i, item in enumerate(visible_items):
#             absolute_index = i + state.scrollOffset
#             is_selected = absolute_index == state.selectedIndices[state.currentScene]
            
#             if is_selected:
#                 uiManager.showCursor(content_x, yOffset + uiManager.fontSmall.get_height() / 2, is_cursor_visible)

#             if isinstance(item, str):
#                 color = uiManager.colors['font_color'] if is_selected else uiManager.colors['inactive_color']
#                 uiManager.showText(f"＋ {item}", content_x + 40, yOffset, color=color)
#             else:
#                 base_color = uiManager.colors['font_color'] if item['is_enabled'] else uiManager.colors['inactive_color']
#                 color = base_color if is_selected else uiManager.colors['inactive_color']
#                 days_map = state.daysOfWeek
#                 days_short = "".join([days_map[d][:1] for d, v in enumerate(item['days']) if v == '1'])
#                 schedule_text = f"{item['time_str']} [{days_short if days_short else '一回'}] {item['name']}"
#                 uiManager.showText(schedule_text, content_x + 40, yOffset, color=color, font=uiManager.fontSmall)
            
#             yOffset += uiManager.fontSmall.get_height() + 15
            
# class ScheduleSubmenuScene(SceneRenderer):
#     def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
#         ScheduleListScene(self.config).show(uiManager, state, is_cursor_visible)
#         overlay = pygame.Surface((uiManager.screenWidth, uiManager.screenHeight), pygame.SRCALPHA)
#         overlay.fill((0, 0, 0, 180))
#         uiManager.screen.blit(overlay, (0, 0))
#         menuW, menuH = 300, 200
#         menuRect = pygame.Rect((uiManager.screenWidth - menuW) // 2, (uiManager.screenHeight - menuH) // 2, menuW, menuH)
#         content_y_start = uiManager.showWindow(menuRect, "このよていをどうしますか？")
#         content_start_x = menuRect.x + uiManager.padding + 20
#         for i, option in enumerate(state.scheduleSubmenuOptions):
#             y = content_y_start + i * 45
#             uiManager.showText(option, content_start_x + 40, y)
#             if i == state.selectedIndices[state.currentScene]: uiManager.showCursor(content_start_x, y + 15, is_cursor_visible)

# class ScheduleEditNameScene(SceneRenderer):
#     def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
#         ScheduleInputNameScene(self.config).show(uiManager, state, is_cursor_visible, prompt="よていのなまえをへんしゅう")

# class ScheduleEditDaysScene(SceneRenderer):
#     def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
#         ScheduleSelectDaysScene(self.config).show(uiManager, state, is_cursor_visible)

# class ScheduleEditTimeScene(SceneRenderer):
#     def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
#         ScheduleSelectTimeScene(self.config).show(uiManager, state, is_cursor_visible, prompt="じこくをへんしゅう (HH:MM)")

# class ScheduleEditConfirmScene(SceneRenderer):
#     def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
#         ScheduleConfirmScene(self.config).show(uiManager, state, is_cursor_visible)