import pygame
from typing import TYPE_CHECKING
from scenes.scene_renderer import SceneRenderer
from sqlite import SQLite


if TYPE_CHECKING:
    from ui import UIManager
    from state import GameState


class Task:
    def __init__(self, db: SQLite, id=0):
        self.db = db
        self.suggestions = {
            "priority": {"特急": 4, "高": 3, "中": 2, "低": 1},
            "dur": [
                "2分",
                "5分",
                "15分",
                "30分",
                "45分",
                "1H",
                "1.5H",
                "2H",
                "3H",
                "1d",
                "TBD",
            ],
            "projects": db.getList(
                f"select name from project where id > 1 order by name"
            ),
            "tags": db.getList(f"select distinct name from tag order by name"),
        }
        if id > 0:
            self.load(id)

    def load(self, id):
        pass

    def save(self):
        pass


class TaskEditor(SceneRenderer):
    def __init__(self, pconf: dict):
        conf = pconf["task_form"]
        self.conf = conf

        self.priorities = {v: k for k, v in conf["priorities"].items()}
        self.durations = conf["dur"]
        self.projects = []
        self.tasks = []
        self.loaded = False

    def show(self, uiManager: "UIManager", state: "GameState"):
        screen_rect = uiManager.screen.get_rect()
        form_height = screen_rect.height // 2 - 40
        form_rect = pygame.Rect(50, 50, screen_rect.width - 100, form_height)
        self.showForm(uiManager, state, form_rect)

    def showForm(
        self,
        uiManager: "UIManager",
        state: "GameState",
        area: pygame.Rect,
        is_cursor_visible: bool,
    ):
        uiManager.showWindow(area, "新規タスク登録")

        padding = uiManager.padding * 2
        x1 = area.x + padding
        content_x_right = area.centerx + padding / 2
        yy = area.y + 55  # ウィンドウタイトルの分をオフセット
        field_height = 40
        label_offset_y = -22

        form_data = state.form_data

        # --- 左列 ---
        col_width = area.width / 2 - padding * 1.5

        # タスク名
        uiManager.showText(
            "タスク名", x1, yy + label_offset_y, font=uiManager.fontSmall
        )
        name_rect = pygame.Rect(x1, yy, col_width, field_height)
        self.draw_text_input(
            uiManager,
            name_rect,
            form_data["name"],
            "task_name",
            state.active_widget,
            is_cursor_visible,
        )

        yy += field_height + 35
        # タグ
        uiManager.showText(
            "タグ (カンマ区切り)", x1, yy + label_offset_y, font=uiManager.fontSmall
        )
        tags_rect = pygame.Rect(x1, yy, col_width, field_height)
        self.draw_text_input(
            uiManager,
            tags_rect,
            form_data["tags"],
            "task_tags",
            state.active_widget,
            is_cursor_visible,
        )

        yy += field_height + 35
        # 内容
        uiManager.showText("内容", x1, yy + label_offset_y, font=uiManager.fontSmall)
        desc_height = area.bottom - yy - padding
        desc_rect = pygame.Rect(x1, yy, col_width, desc_height)
        self.draw_text_input(
            uiManager,
            desc_rect,
            form_data["description"],
            "task_description",
            state.active_widget,
            is_cursor_visible,
            is_multiline=True,
        )

        # --- 右列 ---
        yy = area.y + 55

        # 優先度 と 所要時間
        half_col_width = col_width / 2 - padding / 4
        uiManager.showText(
            "優先度", content_x_right, yy + label_offset_y, font=uiManager.fontSmall
        )
        priority_rect = pygame.Rect(content_x_right, yy, half_col_width, field_height)
        priority_text = self.priority_names.get(form_data["priority"], "未選択")
        self.draw_dropdown(
            uiManager,
            priority_rect,
            priority_text,
            "task_priority",
            state.active_widget,
        )

        duration_x = priority_rect.right + padding / 2
        uiManager.showText(
            "所要時間", duration_x, yy + label_offset_y, font=uiManager.fontSmall
        )
        duration_rect = pygame.Rect(duration_x, yy, half_col_width, field_height)
        self.draw_dropdown(
            uiManager,
            duration_rect,
            form_data["duration"],
            "task_duration",
            state.active_widget,
        )

        yy += field_height + 35
        # 期限
        uiManager.showText(
            "期限 (yyyy-MM-dd)",
            content_x_right,
            yy + label_offset_y,
            font=uiManager.fontSmall,
        )
        due_rect = pygame.Rect(content_x_right, yy, col_width, field_height)
        self.draw_text_input(
            uiManager,
            due_rect,
            form_data["dueto"],
            "task_dueto",
            state.active_widget,
            is_cursor_visible,
        )

        yy += field_height + 35
        # 対象プロジェクト
        uiManager.showText(
            "対象プロジェクト",
            content_x_right,
            yy + label_offset_y,
            font=uiManager.fontSmall,
        )
        project_rect = pygame.Rect(content_x_right, yy, col_width, field_height)
        project_name = next(
            (p["name"] for p in self.projects if p["id"] == form_data["project_id"]),
            "未選択",
        )
        self.draw_dropdown(
            uiManager, project_rect, project_name, "task_project", state.active_widget
        )

        yy += field_height + 25
        # 重要フラグ
        important_rect = pygame.Rect(content_x_right, yy, 24, 24)
        self.draw_checkbox(
            uiManager,
            important_rect,
            form_data["important"],
            "task_important",
            state.active_widget,
        )
        uiManager.showText(
            "重要フラグ",
            important_rect.right + 10,
            important_rect.centery - 14,
            font=uiManager.fontSmall,
        )

    def draw_text_input(
        self,
        uiManager,
        rect,
        text,
        widget_id,
        active_widget,
        is_cursor_visible,
        is_multiline=False,
    ):
        is_active = widget_id == active_widget
        # アクティブなウィジェットの背景色を変える
        bg_color = (
            uiManager.colors["window_white"]
            if is_active
            else uiManager.colors["background"]
        )
        text_color = (
            uiManager.colors["background"]
            if is_active
            else uiManager.colors["font_color"]
        )

        pygame.draw.rect(uiManager.screen, bg_color, rect, 0, 4)
        pygame.draw.rect(
            uiManager.screen, uiManager.colors["inactive_color"], rect, 1, 4
        )

        display_text = text
        if is_active and is_cursor_visible:
            display_text += "_"

        # テキストをクリッピングして描画
        uiManager.showText(
            display_text,
            rect.x + 10,
            rect.y + 8,
            color=text_color,
            rect_to_clip=rect.inflate(-20, -16),
        )

    def draw_dropdown(self, uiManager, rect, text, widget_id, active_widget):
        is_active = widget_id == active_widget
        bg_color = (
            uiManager.colors["window_white"]
            if is_active
            else uiManager.colors["background"]
        )
        text_color = (
            uiManager.colors["background"]
            if is_active
            else uiManager.colors["font_color"]
        )

        pygame.draw.rect(uiManager.screen, bg_color, rect, 0, 4)
        pygame.draw.rect(
            uiManager.screen, uiManager.colors["inactive_color"], rect, 1, 4
        )
        uiManager.showText(text, rect.x + 10, rect.y + 8, color=text_color)
        uiManager.showText("▼", rect.right - 25, rect.centery - 12, color=text_color)

    def draw_checkbox(self, uiManager, rect, is_checked, widget_id, active_widget):
        is_active = widget_id == active_widget
        border_color = (
            uiManager.colors["font_color"]
            if is_active
            else uiManager.colors["inactive_color"]
        )

        pygame.draw.rect(uiManager.screen, uiManager.colors["background"], rect, 0, 4)
        pygame.draw.rect(uiManager.screen, border_color, rect, 2, 4)
        if is_checked:
            check_color = uiManager.colors["motivation_100"]
            pygame.draw.line(
                uiManager.screen,
                check_color,
                (rect.left + 4, rect.centery),
                (rect.centerx - 1, rect.bottom - 5),
                3,
            )
            pygame.draw.line(
                uiManager.screen,
                check_color,
                (rect.centerx - 1, rect.bottom - 5),
                (rect.right - 4, rect.top + 5),
                3,
            )
