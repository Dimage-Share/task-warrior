import pygame
import re
from scene import Scene
from state import TopMenuFocus

class InputHandler:
    def handleEvents(self, gameState, db):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState.isRunning = False

            elif event.type == pygame.TEXTINPUT:
                is_text_input_scene = gameState.currentScene in [
                    Scene.INPUT_TASK, Scene.DIARY_INPUT,
                    Scene.SCHEDULE_INPUT_NAME, Scene.SCHEDULE_SELECT_TIME,
                    Scene.SCHEDULE_EDIT_NAME, Scene.SCHEDULE_EDIT_TIME
                ]
                if is_text_input_scene:
                    gameState.inputText += event.text

            elif event.type == pygame.KEYDOWN:
                is_text_input_scene = gameState.currentScene in [
                    Scene.INPUT_TASK, Scene.SCHEDULE_INPUT_NAME, 
                    Scene.SCHEDULE_SELECT_TIME, Scene.DIARY_INPUT,
                    Scene.SCHEDULE_EDIT_NAME, Scene.SCHEDULE_EDIT_TIME
                ]
                if event.key == pygame.K_ESCAPE or (event.key == pygame.K_a and not is_text_input_scene):
                    if is_text_input_scene:
                        pygame.key.stop_text_input()
                        pygame.key.set_repeat(500, 50)
                    
                    if gameState.currentScene == Scene.TOP_MENU and gameState.topMenuFocus == TopMenuFocus.PROJECTS:
                        gameState.topMenuFocus = TopMenuFocus.COMMANDS
                    elif gameState.currentScene != Scene.TOP_MENU:
                        gameState.currentScene = Scene.TOP_MENU
                    else:
                        gameState.isRunning = False
                    continue

                sceneName = gameState.currentScene.name.title().replace('_', '')
                handlerName = f"handleKey{sceneName}"
                handler = getattr(self, handlerName, None)
                if handler:
                    handler(event, gameState, db)
    
    def handleKeyTopMenu(self, event, state, db):
        if state.topMenuFocus == TopMenuFocus.COMMANDS:
            self.handleKeyTopMenuCommands(event, state, db)
        elif state.topMenuFocus == TopMenuFocus.PROJECTS:
            self.handleKeyTopMenuProjects(event, state, db)

    def handleKeyTopMenuCommands(self, event, state, db):
        row, col = state.selectedIndices[state.currentScene]
        menu = state.topMenuOptions
        num_rows = len(menu)
        new_row, new_col = row, col

        if event.key == pygame.K_UP: new_row = max(0, row - 1)
        elif event.key == pygame.K_DOWN: new_row = min(num_rows - 1, row + 1)
        elif event.key == pygame.K_LEFT: new_col = max(0, col - 1)
        elif event.key == pygame.K_RIGHT: new_col = min(len(menu[row]) - 1, col + 1)
        elif event.key == pygame.K_RETURN:
            menuItem = menu[row][col]
            if menuItem == "新しいタスク": 
                state.currentScene = Scene.INPUT_TASK; state.inputText = ""
                pygame.key.start_text_input(); pygame.key.set_repeat(0)
            elif menuItem == "さくせん": state.currentScene = Scene.CHOOSE_STRATEGY
            elif menuItem == "プロジェクト": state.topMenuFocus = TopMenuFocus.PROJECTS; state.projectList = []
            elif menuItem == "整理": state.currentScene = Scene.ORGANIZE_TASKS; state.tasksToOrganize = []
            elif menuItem == "予定": state.currentScene = Scene.SCHEDULE_LIST; state.scheduleList = []
            elif menuItem == "日記": 
                state.currentScene = Scene.DIARY_INPUT; state.inputText = ""
                pygame.key.start_text_input(); pygame.key.set_repeat(0)
            elif menuItem == "モチベーション": state.currentScene = Scene.MOTIVATION_VIEW
            return

        if menu[new_row][new_col] is None:
            if event.key == pygame.K_DOWN and col == 1: new_col = 0
            elif event.key == pygame.K_RIGHT and row == 3: new_col=col
            elif new_col < len(menu[new_row]) and menu[new_row][new_col] is None:
                new_col = col
        
        state.selectedIndices[state.currentScene] = (new_row, new_col)

    def handleKeyTopMenuProjects(self, event, state, db):
        if not state.projectList:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                state.topMenuFocus = TopMenuFocus.COMMANDS
            return

        if event.key == pygame.K_UP:
            state.projectListIndex = max(0, state.projectListIndex - 1)
        elif event.key == pygame.K_DOWN:
            state.projectListIndex = min(len(state.projectList) - 1, state.projectListIndex + 1)
        elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            state.topMenuFocus = TopMenuFocus.COMMANDS

    def handleKeyMotivationView(self, event, state, db):
        if event.key == pygame.K_UP:
            state.motivationValue = min(100, state.motivationValue + 5)
        elif event.key == pygame.K_DOWN:
            state.motivationValue = max(0, state.motivationValue - 5)
        elif event.key == pygame.K_RETURN:
            print(f"モチベーションを {state.motivationValue}% に設定しました。")
            state.currentScene = Scene.TOP_MENU
    
    def handleKeyDiaryInput(self, event, state, db):
        if event.key == pygame.K_RETURN:
            if state.inputText:
                db.addDiaryEntry(state.inputText)
                state.currentScene = Scene.TOP_MENU
                state.inputText = ""
                pygame.key.stop_text_input(); pygame.key.set_repeat(500, 50)
        elif event.key == pygame.K_BACKSPACE: state.inputText = state.inputText[:-1]
    
    def handleKeyInputTask(self, event, state, db):
        if event.key == pygame.K_RETURN:
            if state.inputText:
                text = state.inputText
                tags = re.findall(r'@(\w+)', text)
                task_name = re.sub(r'\s*@\w+\s*', ' ', text).strip()
                db.add_task_to_inbox(task_name, ",".join(tags))
                state.currentScene = Scene.TOP_MENU
                state.inputText = ""
                pygame.key.stop_text_input(); pygame.key.set_repeat(500, 50)
        elif event.key == pygame.K_BACKSPACE:
            state.inputText = state.inputText[:-1]

    def handleKeyChooseStrategy(self, event, state, db):
        if event.key == pygame.K_UP: state.selectedIndices[state.currentScene] = (state.selectedIndices[state.currentScene] - 1 + len(state.strategyOptions)) % len(state.strategyOptions)
        elif event.key == pygame.K_DOWN: state.selectedIndices[state.currentScene] = (state.selectedIndices[state.currentScene] + 1) % len(state.strategyOptions)
        elif event.key == pygame.K_RETURN:
            state.currentStrategy = state.strategyOptions[state.selectedIndices[state.currentScene]]
            db.save_strategy(state.currentStrategy)
            state.currentScene = Scene.TOP_MENU

    def handleKeyOrganizeTasks(self, event, state, db):
        if not state.tasksToOrganize: return
        max_visible_items = 10
        if event.key == pygame.K_UP:
            state.selectedIndices[state.currentScene] = max(0, state.selectedIndices[state.currentScene] - 1)
            if state.selectedIndices[state.currentScene] < state.scrollOffset:
                state.scrollOffset = state.selectedIndices[state.currentScene]
        elif event.key == pygame.K_DOWN:
            state.selectedIndices[state.currentScene] = min(len(state.tasksToOrganize) - 1, state.selectedIndices[state.currentScene] + 1)
            if state.selectedIndices[state.currentScene] >= state.scrollOffset + max_visible_items:
                state.scrollOffset = state.selectedIndices[state.currentScene] - max_visible_items + 1
        elif event.key == pygame.K_RETURN:
            state.selectedTaskToOrganize = state.tasksToOrganize[state.selectedIndices[state.currentScene]]
            state.currentScene = Scene.ORGANIZE_SUBMENU
            
    def handleKeyOrganizeSubmenu(self, event, state, db):
        if event.key == pygame.K_UP: state.selectedIndices[state.currentScene] = (state.selectedIndices[state.currentScene] - 1 + len(state.organizeSubmenuOptions)) % len(state.organizeSubmenuOptions)
        elif event.key == pygame.K_DOWN: state.selectedIndices[state.currentScene] = (state.selectedIndices[state.currentScene] + 1) % len(state.organizeSubmenuOptions)
        elif event.key == pygame.K_RETURN:
            action = state.organizeSubmenuOptions[state.selectedIndices[state.currentScene]]
            if action == "おわった": db.update_task_status(state.selectedTaskToOrganize['id'], 'done')
            state.currentScene = Scene.ORGANIZE_TASKS
            state.tasksToOrganize = []

    def handleKeyScheduleList(self, event, state, db):
        list_with_add_button = ["あたらしいよてい"] + state.scheduleList
        if not list_with_add_button: return
        max_visible_items = 10
        if event.key == pygame.K_UP:
            state.selectedIndices[state.currentScene] = max(0, state.selectedIndices[state.currentScene] - 1)
            if state.selectedIndices[state.currentScene] < state.scrollOffset:
                state.scrollOffset = state.selectedIndices[state.currentScene]
        elif event.key == pygame.K_DOWN:
            state.selectedIndices[state.currentScene] = min(len(list_with_add_button) - 1, state.selectedIndices[state.currentScene] + 1)
            if state.selectedIndices[state.currentScene] >= state.scrollOffset + max_visible_items:
                state.scrollOffset = state.selectedIndices[state.currentScene] - max_visible_items + 1
        elif event.key == pygame.K_RETURN:
            selectedIndex = state.selectedIndices[state.currentScene]
            if selectedIndex == 0:
                state.newScheduleData = {'name': '', 'days': [False] * 7, 'time': '00:00'}
                state.inputText = ""
                state.currentScene = Scene.SCHEDULE_INPUT_NAME
                pygame.key.start_text_input(); pygame.key.set_repeat(0)
            else:
                state.selectedSchedule = state.scheduleList[selectedIndex - 1]
                state.currentScene = Scene.SCHEDULE_SUBMENU
        elif event.key == pygame.K_SPACE:
            selectedIndex = state.selectedIndices[state.currentScene]
            if selectedIndex > 0:
                schedule_to_toggle = state.scheduleList[selectedIndex - 1]
                db.toggleScheduleStatus(schedule_to_toggle['id'])
                state.scheduleList = []
    
    def handleKeyScheduleSubmenu(self, event, state, db):
        if event.key == pygame.K_UP: state.selectedIndices[state.currentScene] = (state.selectedIndices[state.currentScene] - 1 + len(state.scheduleSubmenuOptions)) % len(state.scheduleSubmenuOptions)
        elif event.key == pygame.K_DOWN: state.selectedIndices[state.currentScene] = (state.selectedIndices[state.currentScene] + 1) % len(state.scheduleSubmenuOptions)
        elif event.key == pygame.K_RETURN:
            action = state.scheduleSubmenuOptions[state.selectedIndices[state.currentScene]]
            if action == "さくじょ":
                db.deleteSchedule(state.selectedSchedule['id'])
            elif action == "へんしゅう":
                state.newScheduleData['name'] = state.selectedSchedule['name']
                state.newScheduleData['time'] = state.selectedSchedule['time_str']
                state.newScheduleData['days'] = [day == '1' for day in state.selectedSchedule['days']]
                state.inputText = state.newScheduleData['name']
                state.currentScene = Scene.SCHEDULE_EDIT_NAME
                pygame.key.start_text_input(); pygame.key.set_repeat(0)
                return
            state.currentScene = Scene.SCHEDULE_LIST
            state.scheduleList = []
    
    def handleKeyScheduleInputName(self, event, state, db):
        if event.key == pygame.K_RETURN:
            if state.inputText:
                state.newScheduleData['name'] = state.inputText
                state.currentScene = Scene.SCHEDULE_SELECT_DAYS
                pygame.key.stop_text_input(); pygame.key.set_repeat(500, 50)
        elif event.key == pygame.K_BACKSPACE: state.inputText = state.inputText[:-1]

    def handleKeyScheduleSelectDays(self, event, state, db):
        options_count = len(state.daysOfWeek) + 1
        if event.key == pygame.K_UP: state.selectedIndices[state.currentScene] = (state.selectedIndices[state.currentScene] - 1 + options_count) % options_count
        elif event.key == pygame.K_DOWN: state.selectedIndices[state.currentScene] = (state.selectedIndices[state.currentScene] + 1) % options_count
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            selectedIndex = state.selectedIndices[state.currentScene]
            if selectedIndex < len(state.daysOfWeek):
                state.newScheduleData['days'][selectedIndex] = not state.newScheduleData['days'][selectedIndex]
            else:
                state.inputText = state.newScheduleData['time']
                state.currentScene = Scene.SCHEDULE_SELECT_TIME
                pygame.key.start_text_input(); pygame.key.set_repeat(0)
    
    def handleKeyScheduleSelectTime(self, event, state, db):
        if event.key == pygame.K_RETURN:
            if len(state.inputText) == 5 and state.inputText[2] == ':':
                state.newScheduleData['time'] = state.inputText
                state.currentScene = Scene.SCHEDULE_CONFIRM
                pygame.key.stop_text_input(); pygame.key.set_repeat(500, 50)
        elif event.key == pygame.K_BACKSPACE: state.inputText = state.inputText[:-1]

    def handleKeyScheduleConfirm(self, event, state, db):
        if event.key == pygame.K_UP: state.selectedIndices[state.currentScene] = (state.selectedIndices[state.currentScene] - 1 + len(state.confirmOptions)) % len(state.confirmOptions)
        elif event.key == pygame.K_DOWN: state.selectedIndices[state.currentScene] = (state.selectedIndices[state.currentScene] + 1) % len(state.confirmOptions)
        elif event.key == pygame.K_RETURN:
            selection = state.confirmOptions[state.selectedIndices[state.currentScene]]
            if selection == "はい":
                days_str = "".join(['1' if day else '0' for day in state.newScheduleData['days']])
                db.addSchedule(state.newScheduleData['name'], days_str, state.newScheduleData['time'])
                state.currentScene = Scene.TOP_MENU
            else: 
                state.currentScene = Scene.SCHEDULE_LIST
                state.scheduleList = []

    def handleKeyScheduleEditName(self, event, state, db):
        if event.key == pygame.K_RETURN:
            if state.inputText:
                state.newScheduleData['name'] = state.inputText
                state.currentScene = Scene.SCHEDULE_EDIT_DAYS
                pygame.key.stop_text_input(); pygame.key.set_repeat(500, 50)
        elif event.key == pygame.K_BACKSPACE: state.inputText = state.inputText[:-1]

    def handleKeyScheduleEditDays(self, event, state, db):
        options_count = len(state.daysOfWeek) + 1
        if event.key == pygame.K_UP: state.selectedIndices[state.currentScene] = (state.selectedIndices[state.currentScene] - 1 + options_count) % options_count
        elif event.key == pygame.K_DOWN: state.selectedIndices[state.currentScene] = (state.selectedIndices[state.currentScene] + 1) % options_count
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            selectedIndex = state.selectedIndices[state.currentScene]
            if selectedIndex < len(state.daysOfWeek):
                state.newScheduleData['days'][selectedIndex] = not state.newScheduleData['days'][selectedIndex]
            else:
                state.inputText = state.newScheduleData['time']
                state.currentScene = Scene.SCHEDULE_EDIT_TIME
                pygame.key.start_text_input(); pygame.key.set_repeat(0)

    def handleKeyScheduleEditTime(self, event, state, db):
        if event.key == pygame.K_RETURN:
            if len(state.inputText) == 5 and state.inputText[2] == ':':
                state.newScheduleData['time'] = state.inputText
                state.currentScene = Scene.SCHEDULE_EDIT_CONFIRM
                pygame.key.stop_text_input(); pygame.key.set_repeat(500, 50)
        elif event.key == pygame.K_BACKSPACE: state.inputText = state.inputText[:-1]

    def handleKeyScheduleEditConfirm(self, event, state, db):
        if event.key == pygame.K_UP: state.selectedIndices[state.currentScene] = (state.selectedIndices[state.currentScene] - 1 + len(state.confirmOptions)) % len(state.confirmOptions)
        elif event.key == pygame.K_DOWN: state.selectedIndices[state.currentScene] = (state.selectedIndices[state.currentScene] + 1) % len(state.confirmOptions)
        elif event.key == pygame.K_RETURN:
            selection = state.confirmOptions[state.selectedIndices[state.currentScene]]
            if selection == "はい":
                days_str = "".join(['1' if day else '0' for day in state.newScheduleData['days']])
                db.updateSchedule(state.selectedSchedule['id'], state.newScheduleData['name'], days_str, state.newScheduleData['time'])
            state.currentScene = Scene.SCHEDULE_LIST
            state.scheduleList = []