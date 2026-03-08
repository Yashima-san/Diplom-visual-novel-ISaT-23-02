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
                text "[persistent.user_name] (ID: [persistent.user_id])" size 30
            
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
                    $ users = db.get_all_users()
                    for user in users:
                        text "ID: [user['user_ID']], Имя: [user['name']]" size 24
            
            null height 20
            
            # Достижения текущего пользователя
            frame:
                xsize 1200
                padding (20, 20)
                vbox:
                    text "Достижения пользователя [persistent.user_name]:" size 30
                    $ achievements = db.get_user_achievements(persistent.user_id)
                    if achievements:
                        for ach in achievements:
                            text "• [ach['achi_name']]: [ach['description']] ([ach['time_point']])" size 24
                    else:
                        text "Нет достижений" size 24

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