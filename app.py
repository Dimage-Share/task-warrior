import pygame
import sys
import json
from datetime import datetime, timedelta
from sqlite import SQLite
from scene import Scene
from state import GameState
from ui import UIManager
from input_handler import InputHandler


class App:
    def __init__(self, config):
        self.config = config

        self.db = SQLite(config["database"]["path"])

        pygame.init()
        screen_size = (config["screen"]["width"], config["screen"]["height"])
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("GTD Quest")
        self.clock = pygame.time.Clock()

        pygame.key.set_repeat(500, 50)

        self.cursor_blink_timer = 0
        self.is_cursor_visible = True

        try:
            fonts = {
                "default": pygame.font.Font(
                    config["font"]["path"], config["font"]["size"]
                ),
                "small": pygame.font.Font(
                    config["font"]["path"], config["font"]["size"] - 8
                ),
            }
        except FileNotFoundError:
            print(f"Font file not found: {config['font']['path']}")
            sys.exit()

        colors = {k: tuple(v) for k, v in config["colors"].items()}
        padding = config.get("padding", 8)
        header_config = config.get("header", {})
        footer_config = config.get("footer", {})
        menu_config = config.get("menu", {})
        cursor_config = config.get("cursor", {})

        self.gameState = GameState(self.db, config)
        self.uiManager = UIManager(
            self.screen,
            fonts,
            colors,
            padding,
            header_config,
            footer_config,
            config,
            cursor_config,
        )
        self.inputHandler = InputHandler()

    def run(self):
        while self.gameState.isRunning:
            delta_time = self.clock.tick(60) / 1000.0

            self.inputHandler.handleEvents(self.gameState, self.db)
            self.updateState(delta_time)
            self.uiManager.showElements(self.gameState, self.is_cursor_visible)

        pygame.quit()
        sys.exit()

    def updateState(self, delta_time):
        self.cursor_blink_timer += delta_time
        if self.cursor_blink_timer >= 0.5:
            self.cursor_blink_timer = 0
            self.is_cursor_visible = not self.is_cursor_visible

        if self.gameState.currentScene == Scene.TOP_MENU:
            if not self.gameState.upcomingSchedules:
                self.gameState.upcomingSchedules = self.getUpcomingSchedules()
            if not self.gameState.projectList:
                self.gameState.projectList = []  # self.db.getProjectList()
            if not self.gameState.inboxTasks:
                self.gameState.inboxTasks = []  # self.db.get_tasks(status='inbox')

        if (
            self.gameState.currentScene == Scene.ORGANIZE_TASKS
            and not self.gameState.tasksToOrganize
        ):
            self.gameState.tasksToOrganize = (
                []
            )  # self.db.get_tasks(status='inbox') + self.db.get_tasks(status='wip')

        if (
            self.gameState.currentScene == Scene.SCHEDULE_LIST
            and not self.gameState.scheduleList
        ):
            self.gameState.scheduleList = []  # self.db.getAllEnabledSchedules()

        if (
            self.gameState.currentScene == Scene.DIARY_INPUT
            and not self.gameState.recentDiaryEntries
        ):
            self.gameState.recentDiaryEntries = []  # self.db.getRecentDiaryEntries()

        self.gameState.db = self.db

    def getUpcomingSchedules(self, limit=5):
        now = datetime.now()
        schedules = []  # self.db.getAllEnabledSchedules()
        upcoming = []

        for i in range(7):
            check_date = now + timedelta(days=i)
            weekday = check_date.weekday()

            for schedule in schedules:
                if schedule["days"][weekday] == "1":
                    schedule_time_str = schedule["time_str"]
                    schedule_datetime = datetime.strptime(
                        f"{check_date.strftime('%Y-%m-%d')} {schedule_time_str}",
                        "%Y-%m-%d %H:%M",
                    )

                    if schedule_datetime >= now:
                        upcoming.append(
                            {"datetime": schedule_datetime, "name": schedule["name"]}
                        )

        upcoming.sort(key=lambda x: x["datetime"])
        return upcoming[:limit]
