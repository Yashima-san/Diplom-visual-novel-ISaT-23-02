################################################################################
## База данных SQLite
################################################################################

init -2 python:
    # Попытка импорта sqlite3 с обработкой ошибки
    import sys
    import os
    import time
    
    # Инициализация persistent переменных
    if not hasattr(persistent, 'user_data') or persistent.user_data is None:
        persistent.user_data = {
            'users': {},
            'achievements': {},
            'save_progress': {},
            'next_id': 1
        }
    
    # Проверяем наличие sqlite3
    try:
        import sqlite3
        sqlite_available = True
    except ImportError:
        sqlite_available = False
        renpy.notify("Внимание: Модуль sqlite3 не найден. Данные будут сохраняться только в файлах сохранений Ren'Py.")
    
    class Database:
        def __init__(self):
            self.db_path = None
            self.connection = None
            self.cursor = None
            self.sqlite_available = sqlite_available
            
            if self.sqlite_available:
                self.init_database()
            else:
                # Создаем альтернативное хранилище в виде словаря
                self.memory_storage = {
                    'users': {},
                    'achievements': {},
                    'save_progress': {}
                }
                self.next_user_id = 1
        
        def init_database(self):
            """Инициализация базы данных и создание таблиц"""
            if not self.sqlite_available:
                return
                
            try:
                # Путь к файлу базы данных в папке game
                self.db_path = os.path.join(renpy.config.gamedir, "game_data.sqlite")
                self.connect()
                
                # Создание таблицы users
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
                        save_point TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Создание таблицы achievements
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS achievements (
                        achi_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_ID INTEGER NOT NULL,
                        achi_name VARCHAR(50) NOT NULL,
                        description VARCHAR(120),
                        time_point TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                        last_release_date DATE
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
                self.sqlite_available = False
            finally:
                self.disconnect()
        
        def connect(self):
            """Установка соединения с базой данных"""
            if not self.sqlite_available:
                return
            try:
                self.connection = sqlite3.connect(self.db_path)
                self.connection.row_factory = sqlite3.Row
                self.cursor = self.connection.cursor()
            except Exception as e:
                renpy.notify(f"Ошибка подключения к БД: {str(e)}")
                self.sqlite_available = False
        
        def disconnect(self):
            """Закрытие соединения с базой данных"""
            if self.sqlite_available and self.cursor:
                self.cursor.close()
            if self.sqlite_available and self.connection:
                self.connection.close()
        
        def add_user(self, user_name):
            """Добавление нового пользователя"""
            # Проверяем, есть ли уже пользователь в persistent
            if hasattr(persistent, 'user_data') and persistent.user_data and 'users' in persistent.user_data:
                for user_id, data in persistent.user_data['users'].items():
                    if data.get('name') == user_name:
                        return int(user_id)
            
            if self.sqlite_available:
                return self._add_user_sqlite(user_name)
            else:
                return self._add_user_memory(user_name)
        
        def _add_user_sqlite(self, user_name):
            """Добавление пользователя в SQLite"""
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
                    
                    # Добавляем запись о начале игры
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
        
        def _add_user_memory(self, user_name):
            """Добавление пользователя в память (альтернативное хранилище)"""
            # Инициализируем persistent.user_data если его нет
            if not hasattr(persistent, 'user_data') or persistent.user_data is None:
                persistent.user_data = {
                    'users': {},
                    'achievements': {},
                    'save_progress': {},
                    'next_id': 1
                }
            
            # Проверяем существующего пользователя
            if 'users' in persistent.user_data:
                for user_id, data in persistent.user_data['users'].items():
                    if data.get('name') == user_name:
                        return int(user_id)
            
            # Создаем нового пользователя
            user_id = persistent.user_data.get('next_id', 1)
            if 'users' not in persistent.user_data:
                persistent.user_data['users'] = {}
            
            persistent.user_data['users'][str(user_id)] = {
                'name': user_name,
                'created_at': time.time()
            }
            
            # Добавляем прогресс
            if 'save_progress' not in persistent.user_data:
                persistent.user_data['save_progress'] = {}
            
            if str(user_id) not in persistent.user_data['save_progress']:
                persistent.user_data['save_progress'][str(user_id)] = []
            
            persistent.user_data['save_progress'][str(user_id)].append({
                'chapter': "Глава 1: Связь",
                'save_point': time.time()
            })
            
            persistent.user_data['next_id'] = user_id + 1
            
            return user_id
        
        def get_user_id(self, user_name):
            """Получение ID пользователя по имени"""
            if self.sqlite_available:
                return self._get_user_id_sqlite(user_name)
            else:
                return self._get_user_id_memory(user_name)
        
        def _get_user_id_sqlite(self, user_name):
            """Получение ID из SQLite"""
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
        
        def _get_user_id_memory(self, user_name):
            """Получение ID из памяти"""
            if hasattr(persistent, 'user_data') and persistent.user_data and 'users' in persistent.user_data:
                for user_id, data in persistent.user_data['users'].items():
                    if data.get('name') == user_name:
                        return int(user_id)
            return None
        
        def save_achievement(self, user_id, achievement_name, description=""):
            """Сохранение достижения"""
            if self.sqlite_available:
                self._save_achievement_sqlite(user_id, achievement_name, description)
            else:
                self._save_achievement_memory(user_id, achievement_name, description)
        
        def _save_achievement_sqlite(self, user_id, achievement_name, description):
            """Сохранение достижения в SQLite"""
            try:
                self.connect()
                self.cursor.execute('''
                    INSERT INTO achievements (user_ID, achi_name, description)
                    VALUES (?, ?, ?)
                ''', (user_id, achievement_name, description));
                self.connection.commit()
            except Exception as e:
                renpy.notify(f"Ошибка при сохранении достижения: {str(e)}")
            finally:
                self.disconnect()
        
        def _save_achievement_memory(self, user_id, achievement_name, description):
            """Сохранение достижения в память"""
            if not hasattr(persistent, 'user_data') or persistent.user_data is None:
                persistent.user_data = {
                    'users': {},
                    'achievements': {},
                    'save_progress': {},
                    'next_id': 1
                }
            
            if 'achievements' not in persistent.user_data:
                persistent.user_data['achievements'] = {}
            
            str_user_id = str(user_id)
            if str_user_id not in persistent.user_data['achievements']:
                persistent.user_data['achievements'][str_user_id] = []
            
            # Проверяем, не было ли уже такого достижения
            for ach in persistent.user_data['achievements'][str_user_id]:
                if ach.get('name') == achievement_name:
                    return
            
            persistent.user_data['achievements'][str_user_id].append({
                'name': achievement_name,
                'description': description,
                'time_point': time.time()
            })
        
        def update_save_progress(self, user_id, chapter):
            """Обновление прогресса сохранения"""
            if self.sqlite_available:
                self._update_save_progress_sqlite(user_id, chapter)
            else:
                self._update_save_progress_memory(user_id, chapter)
        
        def _update_save_progress_sqlite(self, user_id, chapter):
            """Обновление прогресса в SQLite"""
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
        
        def _update_save_progress_memory(self, user_id, chapter):
            """Обновление прогресса в памяти"""
            if not hasattr(persistent, 'user_data') or persistent.user_data is None:
                persistent.user_data = {}
            
            if 'save_progress' not in persistent.user_data:
                persistent.user_data['save_progress'] = {}
            
            str_user_id = str(user_id)
            if str_user_id not in persistent.user_data['save_progress']:
                persistent.user_data['save_progress'][str_user_id] = []
            
            persistent.user_data['save_progress'][str_user_id].append({
                'chapter': chapter,
                'save_point': time.time()
            })
        
        # В database.rpy, обновите метод get_all_users

        def get_all_users(self):
            """Получение всех пользователей"""
            if self.sqlite_available:
                return self._get_all_users_sqlite()
            else:
                return self._get_all_users_memory()
        
        def _get_all_users_memory(self):
            """Получение пользователей из памяти"""
            users = []
            if hasattr(persistent, 'user_data') and persistent.user_data and 'users' in persistent.user_data:
                for user_id, data in persistent.user_data['users'].items():
                    users.append({
                        'user_ID': int(user_id),
                        'name': data.get('name', '')
                    })
            return users
        
        def _get_all_users_sqlite(self):
            """Получение пользователей из SQLite"""
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
            if self.sqlite_available:
                return self._get_user_achievements_sqlite(user_id)
            else:
                return self._get_user_achievements_memory(user_id)
        
        def _get_user_achievements_sqlite(self, user_id):
            """Получение достижений из SQLite"""
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
        
        def _get_user_achievements_memory(self, user_id):
            """Получение достижений из памяти"""
            achievements = []
            if hasattr(persistent, 'user_data') and persistent.user_data and 'achievements' in persistent.user_data:
                str_user_id = str(user_id)
                if str_user_id in persistent.user_data['achievements']:
                    for ach in persistent.user_data['achievements'][str_user_id]:
                        achievements.append({
                            'achi_name': ach.get('name', ''),
                            'description': ach.get('description', ''),
                            'time_point': ach.get('time_point', '')
                        })
            return achievements

        def get_user_progress(user_id):
            """Получение прогресса пользователя по главам"""
            progress = []
            
            # Словарь для форматирования названий глав
            chapter_formats = {
                "Глава Первая: Связь": "Глава 1 - Связь",
                "Глава Вторая: Новые знакомства": "Глава 2 - Новые знакомства",
                "Глава Третья: Испытание дружбой": "Глава 3 - Испытание дружбой",
            }
            
            # Получаем прогресс из persistent
            if hasattr(persistent, 'user_data') and persistent.user_data:
                str_user_id = str(user_id)
                if 'save_progress' in persistent.user_data and str_user_id in persistent.user_data['save_progress']:
                    for save in persistent.user_data['save_progress'][str_user_id]:
                        chapter = save.get('chapter', '')
                        if chapter and chapter not in progress:
                            # Форматируем название главы
                            formatted_chapter = chapter_formats.get(chapter, chapter)
                            progress.append(formatted_chapter)
            
            # Если используем SQLite
            if hasattr(db, 'sqlite_available') and db.sqlite_available:
                try:
                    db.connect()
                    db.cursor.execute('''
                        SELECT DISTINCT chapter FROM save_progress_users 
                        WHERE user_ID = ? ORDER BY save_point
                    ''', (user_id,))
                    for row in db.cursor.fetchall():
                        chapter = row['chapter']
                        if chapter and chapter not in progress:
                            formatted_chapter = chapter_formats.get(chapter, chapter)
                            progress.append(formatted_chapter)
                except:
                    pass
                finally:
                    db.disconnect()
        
            return progress
    
    # Глобальный экземпляр базы данных
    db = Database()

# Инициализация версии игры
init -1 python:
    def init_game_version():
        if db.sqlite_available:
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