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
            
            # Кнопка обновления данных
            textbutton "Обновить данные" action Show("debug_database")
            
            null height 30
            
            # Список всех пользователей
            frame:
                xsize 1200
                padding (20, 20)
                vbox:
                    text "Все пользователи:" size 30
                    $ users = db.get_all_users() if hasattr(db, 'get_all_users') else []
                    if users:
                        for user in users:
                            text "ID: [user['user_ID']], Имя: [user['name']]" size 24
                    else:
                        text "Нет пользователей" size 24
            
            null height 20
            
            # Достижения текущего пользователя
            frame:
                xsize 1200
                padding (20, 20)
                vbox:
                    text "Достижения пользователя [current_user_name]:" size 30
                    if current_user_id != "Не задан" and current_user_id is not None:
                        $ achievements = db.get_user_achievements(current_user_id) if hasattr(db, 'get_user_achievements') else []
                        if achievements:
                            for ach in achievements:
                                text "• [ach.get('achi_name', '')]: [ach.get('description', '')] ([ach.get('time_point', '')])" size 24
                        else:
                            text "Нет достижений" size 24
                    else:
                        text "Пользователь не выбран" size 24

# Добавим кнопку в главное меню для доступа к отладке (опционально)
screen main_menu():
    tag menu
    add gui.main_menu_background
    
    frame:
        style "main_menu_frame"
        
        vbox:
            text "[config.name!t]":
                style "main_menu_title"
            
            text "Версия [config.version]":
                style "main_menu_version"
            
            null height 30
            
            # Стандартные кнопки главного меню
            textbutton _("Начать") action Start()
            textbutton _("Загрузить") action ShowMenu("load")
            textbutton _("Настройки") action ShowMenu("preferences")
            textbutton _("Достижения") action ShowMenu("achievements")
            textbutton _("Карточки") action ShowMenu("gallery")
            textbutton _("Отладка БД") action ShowMenu("debug_database")  # Добавлено
            textbutton _("Выход") action Quit(confirm=False)