import pygame
from datetime import datetime
from typing import TYPE_CHECKING
from scene import Scene 
from scenes import (
    TopMenu, InputTask, ChooseStrategy, MapView, DiaryInput, MotivationView,
    OrganizeTasks, OrganizeSubmenu, 
    ScheduleList, ScheduleSubmenu,
    ScheduleCreateName, ScheduleCreateDays, ScheduleCreateTime, ScheduleCreateConfirm,
    ScheduleEditName, ScheduleEditDays, ScheduleEditTime, ScheduleEditConfirm
)

if TYPE_CHECKING:
    from state import GameState

class UIManager:
    def __init__(self, screen, fonts, colors, padding, header_config, footer_config, config, cursor_config):
        self.screen = screen
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        self.font = fonts['default']
        self.fontSmall = fonts['small']
        self.colors = colors
        self.padding = padding
        self.headerConfig = header_config
        self.footerConfig = footer_config
        self.config = config
        self.cursorConfig = cursor_config
        self.daysOfWeekJp = ("日", "月", "火", "水", "木", "金", "土")

        self.headerMessages = {
            Scene.TOP_MENU: "冒険を始める",
            Scene.INPUT_TASK: "新しいタスク",
            Scene.CHOOSE_STRATEGY: "さくせん",
            Scene.PROJECT: "マップ",
            Scene.ORGANIZE_TASKS: "タスクの整理",
            Scene.ORGANIZE_SUBMENU: "アクション",
            Scene.SCHEDULE_LIST: "予定の管理",
            Scene.SCHEDULE_INPUT_NAME: "新しい予定",
            Scene.SCHEDULE_SELECT_DAYS: "繰返し設定",
            Scene.SCHEDULE_SELECT_TIME: "時刻設定 (HH:MM)",
            Scene.SCHEDULE_CONFIRM: "この内容で登録しますか?",
            Scene.SCHEDULE_SUBMENU: "予定の編集・削除",
            Scene.SCHEDULE_EDIT_NAME: "予定の編集",
            Scene.SCHEDULE_EDIT_DAYS: "繰返し設定の編集",
            Scene.SCHEDULE_EDIT_TIME: "時刻設定の編集",
            Scene.SCHEDULE_EDIT_CONFIRM: "この内容で更新しますか?",
            Scene.DIARY_INPUT: "日記",
            Scene.MOTIVATION_VIEW: "モチベーション",
        }

        self.sceneRenderers = {
            Scene.TOP_MENU: TopMenu(self.config),
            Scene.INPUT_TASK: InputTask(self.config),
            Scene.CHOOSE_STRATEGY: ChooseStrategy(self.config),
            Scene.PROJECT: MapView(self.config),
            Scene.ORGANIZE_TASKS: OrganizeTasks(self.config),
            Scene.ORGANIZE_SUBMENU: OrganizeSubmenu(self.config),
            Scene.SCHEDULE_LIST: ScheduleList(self.config),
            Scene.SCHEDULE_SUBMENU: ScheduleSubmenu(self.config),
            Scene.SCHEDULE_INPUT_NAME: ScheduleCreateName(self.config),
            Scene.SCHEDULE_SELECT_DAYS: ScheduleCreateDays(self.config),
            Scene.SCHEDULE_SELECT_TIME: ScheduleCreateTime(self.config),
            Scene.SCHEDULE_CONFIRM: ScheduleCreateConfirm(self.config),
            Scene.SCHEDULE_EDIT_NAME: ScheduleEditName(self.config),
            Scene.SCHEDULE_EDIT_DAYS: ScheduleEditDays(self.config),
            Scene.SCHEDULE_EDIT_TIME: ScheduleEditTime(self.config),
            Scene.SCHEDULE_EDIT_CONFIRM: ScheduleEditConfirm(self.config),
            Scene.DIARY_INPUT: DiaryInput(self.config),
            Scene.MOTIVATION_VIEW: MotivationView(self.config),
        }

    def showElements(self, gameState: 'GameState', is_cursor_visible: bool):
        self.screen.fill(self.colors["background"])
        self.showHeader(gameState.currentScene)
        # self.showFooter(gameState.currentStrategy)
        self.showStatusBar(gameState)
        renderer = self.sceneRenderers.get(gameState.currentScene)
        if renderer: renderer.show(self, gameState, is_cursor_visible)
        pygame.display.flip()

    def showWindow(self, rect, title="", border_color=None):
        inner_rect = rect.inflate(-self.padding, -self.padding)
        pygame.draw.rect(self.screen, self.colors["window_blue"], inner_rect)
        
        border_c = border_color if border_color is not None else self.colors["window_white"]
        pygame.draw.rect(self.screen, border_c, rect, 4)

        content_y_start = rect.y + self.padding
        if title:
            title_surf = self.font.render(title, True, self.colors["font_color"], self.colors["window_blue"])
            title_rect = title_surf.get_rect(centerx=rect.centerx, y=rect.y - self.font.get_height() // 2)
            self.screen.blit(title_surf, title_rect)
            content_y_start = title_rect.bottom + self.padding
        
        return content_y_start
    
    def showText(self, text, x, y, color=None, font=None):
        font = font or self.font
        color = color or self.colors["font_color"]
        surf = font.render(text, True, color)
        self.screen.blit(surf, (x, y))
        return 280

    def showCursor(self, x, y, is_visible: bool):
        if not is_visible:
            return
            
        width = self.cursorConfig.get("width", 24)
        height = self.cursorConfig.get("height", 24)
        half_height = height / 2
        points = [(x, y - half_height), (x + width, y), (x, y + half_height)]
        pygame.draw.polygon(self.screen, self.colors["window_white"], points)

    def showHeader(self, currentScene):
        rect_config = self.headerConfig.get("rect", {"x": 16, "y": 16})
        height = 50
        width = self.screenWidth - (rect_config["x"] * 2)
        headerRect = pygame.Rect(rect_config["x"], rect_config["y"], width, height)
        self.showWindow(headerRect)
        now = datetime.now()
        day_of_week = self.daysOfWeekJp[int(now.strftime("%w"))]
        time_str = now.strftime(f"%Y/%m/%d({day_of_week}) %H:%M:%S")
        message = self.headerMessages.get(currentScene, "GTD Quest")
        y_pos = headerRect.centery - self.font.get_height() // 2
        msg_surf = self.font.render(message, True, self.colors["font_color"])
        time_surf = self.font.render(time_str, True, self.colors["font_color"])
        self.screen.blit(msg_surf, (headerRect.x + self.padding + 4, y_pos))
        self.screen.blit(time_surf, (headerRect.right - time_surf.get_width() - self.padding - 4, y_pos))

    def _showStatusItem(self, value, x, y):
        self.showText(value, x, y)
        return self.showText(str(value), x, y)
        
    def _showMotivation(self, x, y, gameState: 'GameState'):
        label_width = self.showText("モチベーション", x, y)
        
        bar_x = x + label_width + 20
        bar_y = y + self.font.get_height() // 2 - 5
        bar_width = 100
        bar_height = 10
        color_100 = pygame.Color(self.colors["motivation_100"])
        color_0 = pygame.Color(self.colors["motivation_0"])
        
        for i in range(bar_width):
            ratio = i / bar_width
            color = color_0.lerp(color_100, ratio)
            pygame.draw.line(self.screen, color, (bar_x + i, bar_y), (bar_x + i, bar_y + bar_height))

        indicator_x = bar_x + (gameState.motivationValue / 100) * bar_width
        triangle_size = 8
        dy = 4
        points = [
            (indicator_x - triangle_size / 2, bar_y - triangle_size / 2 - dy),
            (indicator_x + triangle_size / 2, bar_y - triangle_size / 2 - dy),
            (indicator_x, bar_y + triangle_size / 2 - dy)
        ]
        pygame.draw.polygon(self.screen, color_100, points)

        percent_width = self.showText(f"{str(gameState.motivationValue)}%", bar_x + bar_width + 10, y)
        return (bar_x + bar_width + 10 + percent_width) - x

    def showStatusBar(self, gameState: 'GameState'):
        rect_config = self.footerConfig.get("rect", {"x": 16, "y": 16})
        height = 100
        width = self.screenWidth - (rect_config["x"] * 2)
        y_pos = self.screenHeight - height - rect_config["y"]
        statusRect = pygame.Rect(rect_config["x"], y_pos, width, height)
        
        pygame.draw.line(self.screen, self.colors["window_white"], (statusRect.left, statusRect.y), (statusRect.right, statusRect.y), 2)

        #
        #   1段目
        #
        xx = statusRect.x + self.padding
        yy = statusRect.y + self.padding
        xx += self._showStatusItem(f"完了タスク {gameState.completedTaskCount}", xx, yy)
        xx += self._showStatusItem(f"今日の残作業 {gameState.todaysScheduleCount}", xx, yy)
        xx += self._showMotivation(xx, yy, gameState)
        
        #
        #   2段目
        #
        xx = statusRect.x + self.padding
        yy += 48
        self.showText(f"さくせん: {gameState.currentStrategy}", xx, yy)
        