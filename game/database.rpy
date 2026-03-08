################################################################################
## База данных SQLite
################################################################################

init -2 python:
    import sqlite3
    import os
    
    class Database:
        def __init__(self):
            # Путь к файлу базы данных
            self.db_path = os.path.join(config.basedir, "game_data.sqlite")
            self.connection = None
            self.cursor = None
            self.init_database()
        
        def init_database(self):
            """Инициализация базы данных и создание таблиц"""
            try:
                self.connect()
                
                # Создание таблицы users в соответствии с ER-диаграммой
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        user_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR(45) NOT NULL
                    )
                ''')
                
                # Создание таблицы save_progress_users
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS save_progress_users (
                        save_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_ID INTEGER NOT NULL,
                        chapter CHAR(15),
                        save_point TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_ID) REFERENCES users(user_ID)
                    )
                ''')
                
                # Создание таблицы achievements
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS achievements (
                        achi_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_ID INTEGER NOT NULL,
                        achi_name VARCHAR(50) NOT NULL,
                        description VARCHAR(120),
                        time_point TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_ID) REFERENCES users(user_ID)
                    )
                ''')
                
                # Создание таблицы game_versions
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS game_versions (
                        game_version_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        release_date DATE
                    )
                ''')
                
                # Создание таблицы update_version
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS update_version (
                        update_version_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        game_version_ID INTEGER NOT NULL,
                        last_release_date DATE,
                        FOREIGN KEY (game_version_ID) REFERENCES game_versions(game_version_ID)
                    )
                ''')
                
                # Создание индексов для оптимизации
                self.cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_user_id ON save_progress_users(user_ID)
                ''')
                
                self.cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_achievement_user ON achievements(user_ID)
                ''')
                
                self.cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_update_version ON update_version(game_version_ID)
                ''')
                
                self.connection.commit()
                
            except Exception as e:
                renpy.notify(f"Ошибка инициализации БД: {str(e)}")
            finally:
                self.disconnect()
        
        def connect(self):
            """Установка соединения с базой данных"""
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
        
        def disconnect(self):
            """Закрытие соединения с базой данных"""
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        
        def add_user(self, user_name):
            """Добавление нового пользователя в таблицу users"""
            user_id = None
            try:
                self.connect()
                
                # Проверяем, существует ли уже пользователь с таким именем
                self.cursor.execute(
                    "SELECT user_ID FROM users WHERE name = ?",
                    (user_name,)
                )
                existing_user = self.cursor.fetchone()
                
                if existing_user:
                    user_id = existing_user['user_ID']
                else:
                    # Добавляем нового пользователя
                    self.cursor.execute(
                        "INSERT INTO users (name) VALUES (?)",
                        (user_name,)
                    )
                    self.connection.commit()
                    user_id = self.cursor.lastrowid
                    
                    # Добавляем запись о начале игры в save_progress_users
                    self.cursor.execute(
                        "INSERT INTO save_progress_users (user_ID, chapter) VALUES (?, ?)",
                        (user_id, "Глава 1: Связь")
                    )
                    self.connection.commit()
                
            except Exception as e:
                renpy.notify(f"Ошибка при добавлении пользователя: {str(e)}")
            finally:
                self.disconnect()
            
            return user_id
        
        def get_user_id(self, user_name):
            """Получение ID пользователя по имени"""
            user_id = None
            try:
                self.connect()
                self.cursor.execute(
                    "SELECT user_ID FROM users WHERE name = ?",
                    (user_name,)
                )
                result = self.cursor.fetchone()
                if result:
                    user_id = result['user_ID']
            except Exception as e:
                renpy.notify(f"Ошибка при получении ID пользователя: {str(e)}")
            finally:
                self.disconnect()
            
            return user_id
        
        def save_achievement(self, user_id, achievement_name, description=""):
            """Сохранение достижения в базу данных"""
            try:
                self.connect()
                self.cursor.execute('''
                    INSERT INTO achievements (user_ID, achi_name, description)
                    VALUES (?, ?, ?)
                ''', (user_id, achievement_name, description))
                self.connection.commit()
            except Exception as e:
                renpy.notify(f"Ошибка при сохранении достижения: {str(e)}")
            finally:
                self.disconnect()
        
        def update_save_progress(self, user_id, chapter):
            """Обновление прогресса сохранения"""
            try:
                self.connect()
                self.cursor.execute('''
                    INSERT INTO save_progress_users (user_ID, chapter)
                    VALUES (?, ?)
                ''', (user_id, chapter))
                self.connection.commit()
            except Exception as e:
                renpy.notify(f"Ошибка при обновлении прогресса: {str(e)}")
            finally:
                self.disconnect()
        
        def get_all_users(self):
            """Получение всех пользователей (для отладки)"""
            users = []
            try:
                self.connect()
                self.cursor.execute("SELECT * FROM users ORDER BY user_ID")
                for row in self.cursor.fetchall():
                    users.append(dict(row))
            except Exception as e:
                renpy.notify(f"Ошибка при получении пользователей: {str(e)}")
            finally:
                self.disconnect()
            return users
        
        def get_user_achievements(self, user_id):
            """Получение всех достижений пользователя"""
            achievements = []
            try:
                self.connect()
                self.cursor.execute('''
                    SELECT * FROM achievements 
                    WHERE user_ID = ? 
                    ORDER BY time_point DESC
                ''', (user_id,))
                for row in self.cursor.fetchall():
                    achievements.append(dict(row))
            except Exception as e:
                renpy.notify(f"Ошибка при получении достижений: {str(e)}")
            finally:
                self.disconnect()
            return achievements
    
    # Глобальный экземпляр базы данных
    db = Database()

# Инициализация версии игры
init -1 python:
    def init_game_version():
        try:
            db.connect()
            # Проверяем, есть ли уже запись о версии
            db.cursor.execute("SELECT * FROM game_versions")
            if not db.cursor.fetchone():
                # Добавляем текущую версию
                db.cursor.execute(
                    "INSERT INTO game_versions (release_date) VALUES (date('now'))"
                )
                game_version_id = db.cursor.lastrowid
                
                # Добавляем запись об обновлении
                db.cursor.execute(
                    "INSERT INTO update_version (game_version_ID, last_release_date) VALUES (?, date('now'))",
                    (game_version_id,)
                )
                db.connection.commit()
        except Exception as e:
            renpy.notify(f"Ошибка при инициализации версии: {str(e)}")
        finally:
            db.disconnect()
    
    # Вызываем инициализацию версии
    init_game_version()