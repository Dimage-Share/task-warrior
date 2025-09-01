-- projectテーブルの作成
-- id=1は'inbox'として予約済み
CREATE TABLE
    IF NOT EXISTS project (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );

-- taskテーブルの作成
-- project_idはprojectテーブルのidを参照する外部キー
CREATE TABLE
    IF NOT EXISTS task (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        priority INTEGER DEFAULT 0,
        dur INTEGER DEFAULT 0,
        important INTEGER DEFAULT 0,
        dueto TEXT,
        project_id INTEGER,
        created_on TEXT NOT NULL,
        FOREIGN KEY (project_id) REFERENCES project (id)
    );

-- tagテーブルの作成
CREATE TABLE
    IF NOT EXISTS tag (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );

-- ntagテーブル（中間テーブル）の作成
-- taskとtagを多対多で関連付ける
-- task_idとtag_idの組み合わせでユニークになるようにする
CREATE TABLE
    IF NOT EXISTS ntag (
        task_id INTEGER,
        tag_id INTEGER,
        PRIMARY KEY (task_id, tag_id),
        FOREIGN KEY (task_id) REFERENCES task (id) ON DELETE CASCADE,
        FOREIGN KEY (tag_id) REFERENCES tag (id) ON DELETE CASCADE
    );

-- 初期データとしてinboxプロジェクトを挿入
-- 既にid=1が存在する場合は何もしない
INSERT
OR IGNORE INTO project (id, name)
VALUES
    (1, 'inbox');

CREATE TABLE
    IF NOT EXISTS priority (id INTEGER, name INTEGER);