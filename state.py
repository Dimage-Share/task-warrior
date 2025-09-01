from enum import Enum, auto
from scene import Scene

class TopMenuFocus(Enum):
    COMMANDS = auto()
    PROJECTS = auto()

class GameState:
    def __init__(self, db, config):
        self.isRunning = True
        self.currentScene = Scene.TOP_MENU
        self.selectedIndices = {scene: 0 for scene in Scene}
        self.selectedIndices[Scene.TOP_MENU] = (0, 0)

        self.currentStrategy = 'null' #db.load_strategy()
        self.inputText = ""
        self.tasksToOrganize = []
        self.selectedTaskToOrganize = None
        
        self.scrollOffset = 0
        self.newScheduleData = { 'name': '', 'days': [False] * 7, 'time': '00:00' }
        self.scheduleList = []
        self.selectedSchedule = None
        self.upcomingSchedules = []
        
        self.topMenuOptions = config["menu"]["items"]
        self.strategyOptions = config["strategy_options"]
        self.organizeSubmenuOptions = ["おわった", "やめる"]
        
        self.daysOfWeek = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]
        self.confirmOptions = ["はい", "いいえ"]
        self.scheduleSubmenuOptions = ["へんしゅう", "さくじょ", "やめる"]

        self.topMenuFocus = TopMenuFocus.COMMANDS
        self.projectList = []
        self.projectListIndex = 0
        self.inboxTasks = []
        self.recentDiaryEntries = []
        self.motivationOptions = [
            "100%", "90%", "80%", "75%", "70%", "60%", "50%",
            "40%", "30%", "25%", "20%", "10%", "0%"
        ]
        self.motivationValue = 75
        self.userName = config.get("user_name", "けいた")
        self.completedTaskCount = 0
        self.todaysScheduleCount = 0