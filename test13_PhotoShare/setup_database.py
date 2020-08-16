from photo_sqlite import exec

exec('''
CREATE TABLE files (
    file_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    filename TEXT,
    album_id INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT (DATETIME('now', 'localtime'))
)
''')

exec('''
CREATE TABLE albums (
    album_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    user_id TEXT,
    created_at TIMESTAMP DEFAULT (DATETIME('now', 'localtime'))
)
''')

print('ok')