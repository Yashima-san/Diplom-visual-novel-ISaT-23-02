screen debug_database():
    tag menu
    use game_menu(_("Отладка БД"), scroll="viewport"):
        style_prefix "debug"
        
        vbox:
            spacing 20
            
            text "Информация о базе данных" size 40 xalign 0.5
            
            hbox:
                spacing 50
                text "Текущий пользователь:" size 30
                $ current_user_name = persistent.user_name if hasattr(persistent, 'user_name') and persistent.user_name else "Не задан"
                $ current_user_id = persistent.user_id if hasattr(persistent, 'user_id') and persistent.user_id else "Не задан"
                text "[current_user_name] (ID: [current_user_id])" size 30
            
            null height 30
            
            # Кнопки управления
            hbox:
                spacing 20
                xalign 0.5
                textbutton "Обновить данные" action Show("debug_database")
                textbutton "Сбросить все достижения" action Function(reset_all_achievements)
                textbutton "Очистить БД" action Show("confirm_clear_db")
            
            null height 30
            
            # Список всех пользователей с прогрессом
            frame:
                xsize 1400
                padding (20, 20)
                vbox:
                    text "Все пользователи (нажмите на строку для просмотра деталей):" size 30
                    $ users = db.get_all_users() if hasattr(db, 'get_all_users') else []
                    if users:
                        # Заголовок таблицы
                        hbox:
                            spacing 20
                            text "ID" size 24 bold True xsize 80
                            text "Имя" size 24 bold True xsize 200
                            text "Прогресс (главы)" size 24 bold True xsize 400
                            text "Достижений" size 24 bold True xsize 150
                            text "Последнее сохранение" size 24 bold True xsize 300
                        
                        null height 10
                        
                        # Строки пользователей
                        for user in users:
                            $ user_id = user['user_ID']
                            $ user_name = user['name']
                            
                            # Получаем прогресс пользователя
                            $ user_progress = get_user_progress(user_id)
                            $ progress_text = ", ".join(user_progress) if user_progress else "Нет данных"
                            
                            # Получаем количество достижений
                            $ user_achievements = db.get_user_achievements(user_id) if hasattr(db, 'get_user_achievements') else []
                            $ ach_count = len(user_achievements)
                            
                            # Получаем время последнего сохранения
                            $ last_save = get_last_save_time(user_id)
                            
                            button:
                                style "debug_user_button"
                                action Show("user_details", user_id=user_id, user_name=user_name)
                                
                                hbox:
                                    spacing 20
                                    text "[user_id]" size 22 xsize 80
                                    text "[user_name]" size 22 xsize 200
                                    text "[progress_text]" size 22 xsize 400
                                    text "[ach_count]" size 22 xsize 150
                                    text "[last_save]" size 22 xsize 300
                    else:
                        text "Нет пользователей" size 24

# Экран детальной информации о пользователе
screen user_details(user_id, user_name):
    tag menu
    use game_menu(_("Детали пользователя: [user_name] (ID: [user_id])"), scroll="viewport"):
        vbox:
            spacing 20
            
            # Кнопка возврата
            textbutton "← Назад к списку" action Show("debug_database")
            
            null height 20
            
            # Информация о пользователе
            frame:
                xsize 1400
                padding (20, 20)
                vbox:
                    text "Информация о пользователе:" size 30
                    null height 10
                    text "Имя: [user_name]" size 24
                    text "ID: [user_id]" size 24
            
            null height 20
            
            # Прогресс прохождения
            frame:
                xsize 1400
                padding (20, 20)
                vbox:
                    text "Прогресс прохождения:" size 30
                    null height 10
                    $ progress = get_user_progress(user_id)
                    if progress:
                        for i, chapter in enumerate(progress):
                            text "• Глава [i+1]: [chapter]" size 24
                    else:
                        text "Нет данных о прогрессе" size 24
            
            null height 20
            
            # Достижения
            frame:
                xsize 1400
                padding (20, 20)
                vbox:
                    text "Достижения:" size 30
                    null height 10
                    $ achievements = db.get_user_achievements(user_id) if hasattr(db, 'get_user_achievements') else []
                    if achievements:
                        for ach in achievements:
                            $ ach_name = ach.get('achi_name', ach.get('name', 'Неизвестно'))
                            $ ach_desc = ach.get('description', '')
                            $ ach_time = ach.get('time_point', '')
                            text "• [ach_name]: [ach_desc] ([ach_time])" size 22
                    else:
                        text "Нет достижений" size 24
            
            null height 20
            
            # Кнопка загрузки
            textbutton "Загрузить игру за этого пользователя" action [Function(set_current_user, user_id, user_name), Start()]
            null height 10
            text "При загрузке игра начнется с сохраненным прогрессом пользователя" size 18 color "#808080"

# Экран подтверждения очистки БД
screen confirm_clear_db():
    modal True
    zorder 200
    
    frame:
        style "confirm_frame"
        xalign 0.5
        yalign 0.5
        xsize 600
        ysize 300
        padding (30, 30)
        
        vbox:
            spacing 25
            xalign 0.5
            
            text "Очистить базу данных?":
                size 20
                color "#ff7171"
                xalign 0.5
            
            text "Все пользователи и их прогресс будут удалены!":
                size 20
                color "#ffffff"
                xalign 0.5
            
            hbox:
                spacing 50
                xalign 0.5
                
                textbutton "Да" action [Function(clear_database), Show("debug_database")]
                textbutton "Нет" action Hide("confirm_clear_db")

# Добавить функции для работы с данными
init python:
    import time
    
    def get_user_progress(user_id):
        """Получение прогресса пользователя по главам"""
        progress = []
        if hasattr(persistent, 'user_data') and persistent.user_data:
            str_user_id = str(user_id)
            if 'save_progress' in persistent.user_data and str_user_id in persistent.user_data['save_progress']:
                for save in persistent.user_data['save_progress'][str_user_id]:
                    if 'chapter' in save and save['chapter'] not in progress:
                        progress.append(save['chapter'])
        
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
                    if chapter not in progress:
                        progress.append(chapter)
            except:
                pass
            finally:
                db.disconnect()
        
        return progress
    
    def get_last_save_time(user_id):
        """Получение времени последнего сохранения"""
        last_time = "Нет данных"
        
        if hasattr(persistent, 'user_data') and persistent.user_data:
            str_user_id = str(user_id)
            if 'save_progress' in persistent.user_data and str_user_id in persistent.user_data['save_progress']:
                saves = persistent.user_data['save_progress'][str_user_id]
                if saves:
                    last_save = saves[-1].get('save_point', '')
                    if last_save:
                        try:
                            last_time = time.ctime(float(last_save)) if isinstance(last_save, (int, float)) else str(last_save)
                        except:
                            last_time = str(last_save)
        
        return last_time
    
    def set_current_user(user_id, user_name):
        """Установка текущего пользователя для загрузки"""
        persistent.user_id = user_id
        persistent.user_name = user_name
    
    def reset_all_achievements():
        """Сброс всех достижений"""
        persistent._achievements = {}
        renpy.notify("Все достижения сброшены")
    
    def clear_database():
        """Очистка базы данных"""
        # Очищаем persistent данные
        persistent.user_data = {
            'users': {},
            'achievements': {},
            'save_progress': {},
            'next_id': 1
        }
        persistent._achievements = {}
        persistent._gallery_unlocks = {}
        persistent.user_id = None
        persistent.user_name = ""
        
        # Очищаем SQLite если доступен
        if hasattr(db, 'sqlite_available') and db.sqlite_available:
            try:
                db.connect()
                db.cursor.execute("DELETE FROM users")
                db.cursor.execute("DELETE FROM save_progress_users")
                db.cursor.execute("DELETE FROM achievements")
                db.connection.commit()
            except:
                pass
            finally:
                db.disconnect()
        
        renpy.notify("База данных очищена")

## Стили для отладки
style debug_user_button:
    xsize 1380
    padding (10, 10)
    background "#333333"
    hover_background "#444444"
    margin (0, 2)