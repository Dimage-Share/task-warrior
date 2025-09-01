import sqlite3, os


class SQLite:
    def __init__(self, path, schema_file="./scripts/create_tables.sql"):
        exist = os.path.isfile(path)
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.path = path
        self.cursor = self.conn.cursor()
        # preset
        if not exist:
            self.preset(schema_file)

    def preset(self, schema_file):
        with open(schema_file, "r", encoding="utf-8") as file:
            content = file.read()
        self.cursor.executescript(content)
        self.conn.commit()
        print(f"{self.path} initialized.")

    def close(self):
        if self.conn:
            self.conn.close()

    def getList(self, cmd):
        pass

    def getTable(self, cmd):
        pass

    def getValue(self, cmd):
        pass

    def getInt(self, cmd):
        pass

    def executeNonQuery(self, cmd):
        pass

    # def getRecentDiaryEntries(self, limit=5):
    #     query = """
    #         SELECT
    #             content,
    #             strftime('%Y-%m-%d', created_at) ||
    #             '(' ||
    #             CASE strftime('%w', created_at)
    #                 WHEN '0' THEN '日'
    #                 WHEN '1' THEN '月'
    #                 WHEN '2' THEN '火'
    #                 WHEN '3' THEN '水'
    #                 WHEN '4' THEN '木'
    #                 WHEN '5' THEN '金'
    #                 WHEN '6' THEN '土'
    #             END ||
    #             ') ' ||
    #             strftime('%H:%M', created_at) AS formatted_date
    #         FROM
    #             diary_entries
    #         ORDER BY
    #             created_at DESC
    #         LIMIT ?
    #     """
    #     self.cursor.execute(query, (limit,))
    #     return self.cursor.fetchall()

    # def getTaskCount(self, status: str):
    #     self.cursor.execute("SELECT COUNT(*) as count FROM tasks WHERE status = ?", (status,))
    #     result = self.cursor.fetchone()
    #     return result['count'] if result else 0

    # def getTodaysScheduleCount(self):
    #     now = datetime.now()
    #     weekday = now.weekday()
    #     time_now_str = now.strftime('%H:%M')
    #     weekday_pattern_index = weekday + 1
    #     query = f"""
    #         SELECT COUNT(*) as count FROM schedules
    #         WHERE is_enabled = 1
    #         AND SUBSTR(days, ?, 1) = '1'
    #         AND time_str >= ?
    #     """
    #     self.cursor.execute(query, (weekday_pattern_index, time_now_str))
    #     result = self.cursor.fetchone()
    #     return result['count'] if result else 0

    # def getProjectList(self):
    #     self.cursor.execute("SELECT DISTINCT project FROM tasks WHERE project IS NOT NULL ORDER BY project")
    #     return [row['project'] for row in self.cursor.fetchall()]

    # def toggleScheduleStatus(self, schedule_id):
    #     self.cursor.execute("UPDATE schedules SET is_enabled = NOT is_enabled WHERE id = ?", (schedule_id,))
    #     self.conn.commit()

    # def updateSchedule(self, schedule_id, name, days, time_str):
    #     self.cursor.execute(
    #         "UPDATE schedules SET name = ?, days = ?, time_str = ? WHERE id = ?",
    #         (name, days, time_str, schedule_id)
    #     )
    #     self.conn.commit()

    # def deleteSchedule(self, schedule_id):
    #     self.cursor.execute("DELETE FROM schedules WHERE id = ?", (schedule_id,))
    #     self.conn.commit()

    # def addDiaryEntry(self, content):
    #     self.cursor.execute("INSERT INTO diary_entries (content) VALUES (?)", (content,))
    #     self.conn.commit()

    # def addSchedule(self, name, days, time_str):
    #     self.cursor.execute("INSERT INTO schedules (name, days, time_str) VALUES (?, ?, ?)",(name, days, time_str))
    #     self.conn.commit()

    # def getAllEnabledSchedules(self):
    #     self.cursor.execute("SELECT * FROM schedules WHERE is_enabled = 1 ORDER BY time_str, name")
    #     return self.cursor.fetchall()

    # def save_strategy(self, strategy):
    #     self.cursor.execute("INSERT OR REPLACE INTO app_state (key, value) VALUES ('current_strategy', ?)",(strategy,))
    #     self.conn.commit()

    # def load_strategy(self):
    #     self.cursor.execute("SELECT value FROM app_state WHERE key = 'current_strategy'")
    #     result = self.cursor.fetchone()
    #     return result['value'] if result else "なし"

    # def add_task_to_inbox(self, name, tags):
    #     project = None
    #     if '#' in name:
    #         parts = name.split('#', 1)[1].split(' ', 1)
    #         project = parts[0]
    #         name = parts[1].strip() if len(parts) > 1 else "名称未設定タスク"
    #     with self._connect() as conn:
    #         self.cursor.execute("INSERT INTO tasks (name, project, status, tags) VALUES (?, ?, 'inbox', ?)",(name, project, tags))
    #         self.conn.commit()

    # def get_tasks(self, status=None):
    #     if status:
    #         self.cursor.execute("SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC", (status,))
    #     else:
    #         self.cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    #     return self.cursor.fetchall()

    # def get_tasks_by_project(self):
    #     self.cursor.execute("SELECT DISTINCT project FROM tasks WHERE project IS NOT NULL AND status != 'done'")
    #     projects = [row['project'] for row in self.cursor.fetchall()]
    #     result = {}
    #     for proj in projects:
    #         self.cursor.execute("SELECT * FROM tasks WHERE project = ? AND status != 'done' ORDER BY created_at", (proj,))
    #         result[proj] = self.cursor.fetchall()
    #     return result

    # def update_task_status(self, task_id, new_status):
    #     self.cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
    #     self.conn.commit()
