################################################################################
## Экран отладки базы данных
################################################################################

screen debug_database():
    tag menu
    use game_menu(_("Игроки"), scroll="viewport"):
        style_prefix "debug"
        
        vbox:
            spacing 20
            xfill True  # Растягиваем по ширине
            
            # Заголовок
            text "Информация об игроках" size 40 xalign 0.5 color gui.accent_color outlines [(2, "#a43c13", 0, 0)]
            
            # Информация о текущем пользователе
            frame:
                style "debug_info_frame"
                xalign 0.5
                xsize 1100
                padding (20, 15)
                
                hbox:
                    spacing 30
                    xalign 0.5
                    text "Текущий игрок:" size 28 color "#ffffff"
                    $ current_user_name = persistent.user_name if hasattr(persistent, 'user_name') and persistent.user_name else "Не задан"
                    $ current_user_id = persistent.user_id if hasattr(persistent, 'user_id') and persistent.user_id else "Не задан"
                    text "[current_user_name]" size 28 color gui.accent_color bold True
                    text "(ID: [current_user_id])" size 28 color "#cccccc"
            
            null height 10
            
            # Кнопки управления
            hbox:
                spacing 20
                xalign 0.5
                textbutton "🔄 Обновить" action Show("debug_database")
                textbutton "🏆 Сбросить достижения" action Function(reset_all_achievements)
                textbutton "🗑️ Очистить БД" action Show("confirm_clear_db")
            
            null height 20
            
            # Список всех пользователей с прогрессом
            frame:
                style "debug_table_frame"
                xsize 1380
                padding (20, 20)
                
                vbox:
                    spacing 15
                    xfill True
                    
                    text "Все игроки (нажмите на строку для просмотра деталей):" size 28 color gui.accent_color
                    
                    # ИСПРАВЛЕНО: получаем список пользователей ДО его использования
                    $ users = db.get_all_users() if hasattr(db, 'get_all_users') else []
                    
                    if users:
                        # Заголовок таблицы
                        frame:
                            style "debug_table_header"
                            xfill True
                            padding (10, 12)
                            
                            hbox:
                                spacing 20
                                xfill True
                                
                                # Заголовки столбцов с фиксированной шириной
                                text "ID" size 22 bold True color gui.accent_color xsize 80 text_align 0.5
                                text "Имя" size 22 bold True color gui.accent_color xsize 200 text_align 0.5
                                text "Прогресс (главы)" size 22 bold True color gui.accent_color xsize 400 text_align 0.5
                                text "Достижений" size 22 bold True color gui.accent_color xsize 150 text_align 0.5
                                text "Последнее сохранение" size 22 bold True color gui.accent_color xsize 300 text_align 0.5
                        
                        # Строки пользователей
                        vpgrid:
                            cols 1
                            spacing 4
                            yinitial 0.0
                            mousewheel True
                            draggable True
                            xadjustment None  # Запрет горизонтального скролла

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
                                
                                # Кнопка-строка с данными
                                button:
                                    style "debug_table_row"
                                    xfill True
                                    action Show("user_details", user_id=user_id, user_name=user_name)
                                    
                                    hbox:
                                        spacing 15
                                        xfill True
                                        
                                        # Данные с фиксированной шириной и выравниванием по центру
                                        text "[user_id]" size 22 color "#ffffff" xsize 80 text_align 0.5
                                        text "[user_name]" size 22 color "#ffffff" xsize 200 text_align 0.5
                                        text "[progress_text]" size 22 color "#ffffff" xsize 400 text_align 0.5
                                        text "[ach_count]" size 22 color "#ffffff" xsize 250 text_align 0.5
                                        text "[last_save]" size 22 color "#ffffff" xsize 80 text_align 0.5
                    else:
                        text "Нет пользователей в базе данных" size 24 xalign 0.5 color "#cccccc"

################################################################################
## Экран детальной информации о пользователе
################################################################################

screen user_details(user_id, user_name):
    tag menu
    
    # Создаем заголовок без интерполяции
    $ title_text = "Детали пользователя: " + user_name + " (ID: " + str(user_id) + ")"
    
    use game_menu(_(title_text), scroll="viewport"):
        style_prefix "debug"
        
        vbox:
            spacing 20
            xfill True
            
            # Кнопка возврата
            button:
                style "debug_back_button"
                xalign 0.0
                action Show("debug_database")
                
                hbox:
                    spacing 8
                    text "⬅️" size 28
                    text "Назад к списку игроков" size 28
            
            null height 10
            
            # Информация о пользователе
            frame:
                style "debug_detail_frame"
                xfill True
                padding (25, 20)
                
                vbox:
                    spacing 15
                    xfill True
                    
                    text "📋 Информация об игроке" size 30 color gui.accent_color
                    
                    grid 2 2:
                        spacing 20
                        xalign 0.0
                        
                        # Левая колонка - метки
                        text "ID:" size 24 color "#5e5e5e" xalign 1.0 
                        text "Имя:" size 24 color "#5e5e5e" xalign 1.1
                        
                        # Правая колонка - значения
                        text "[user_id]" size 24 color gui.accent_color xalign 1.0
                        text "[user_name]" size 24 color gui.accent_color xalign 1.1
            
            null height 10
            
            # Прогресс прохождения
            frame:
                style "debug_detail_frame"
                xfill True
                padding (25, 20)
                
                vbox:
                    spacing 15
                    xfill True
                    
                    text "📖 Прогресс прохождения" size 30 color gui.accent_color
                    
                    $ progress = get_user_progress(user_id)
                    if progress:
                        vpgrid:
                            cols 1
                            spacing 10
                            yinitial 0.0
                            mousewheel True
                            draggable True
                            xadjustment None  # Запрет горизонтального скролла

                            for i, chapter in enumerate(progress):
                                hbox:
                                    spacing 15
                                    xfill True
                                    text "Глава [i+1]:" size 22 color "#939393" xsize 80 xpos 10
                                    text "[chapter]" size 22 color "#5e5e5e" xpos 90
                                    text "✅" size 24 xpos 200
                    else:
                        text "Нет данных о прогрессе" size 22 color "#939393" italic True
            
            null height 10
            
            # Достижения
            frame:
                style "debug_detail_frame"
                xfill True
                padding (25, 20)
                
                vbox:
                    spacing 15
                    xfill True
                    
                    text "🏆 Достижения" size 30 color gui.accent_color
                    
                    $ achievements = db.get_user_achievements(user_id) if hasattr(db, 'get_user_achievements') else []
                    if achievements:
                        vpgrid:
                            cols 1
                            spacing 10
                            yinitial 0.0
                            mousewheel True
                            draggable True
                            xadjustment None  # Запрет горизонтального скролла

                            for ach in achievements:
                                $ ach_name = ach.get('achi_name', ach.get('name', 'Неизвестно'))
                                $ ach_desc = ach.get('description', '')
                                $ ach_time = ach.get('time_point', '')
                                
                                frame:
                                    style "debug_achievement_item"
                                    xfill True
                                    padding (15, 10)
                                    
                                    vbox:
                                        spacing 5
                                        xfill True
                                        hbox:
                                            spacing 10
                                            text "🏅" size 22
                                            text "[ach_name]" size 22 color gui.accent_color
                                        text "[ach_desc]" size 18 color "#ffffff"
                                        text "[ach_time]" size 16 color "#434343" italic True
                    else:
                        text "Нет достижений" size 22 color "#ffffff" italic True
            
            null height 20
            

################################################################################
## Экран подтверждения очистки БД
################################################################################

screen confirm_clear_db():
    modal True
    zorder 200
    
    style_prefix "confirm"
    
    add "gui/overlay/confirm.png"
    
    frame:
        style "debug_confirm_frame"
        xalign 0.5
        yalign 0.5
        xsize 450
        ysize 500
        padding (30, 30)
        
        vbox:
            spacing 25
            xalign 0.5
            yalign 0.5
            
            text "⚠️ ОЧИСТКА БАЗЫ ДАННЫХ ⚠️":
                size 24
                color "#ff7171"
                xalign 0.5
                text_align 0.5
                outlines [(2, "#a84343", 0, 0)]
            
            text "Все пользователи и их прогресс будут безвозвратно удалены!":
                size 18
                color "#ffffff"
                xalign 0.5
                text_align 0.5
                outlines [(2, "#855133", 0, 0)]
            
            null height 10
            
            hbox:
                spacing 10
                xalign 0.5
                
                textbutton "Да, очистить" style "debug_confirm_button_danger" action [Function(clear_database), Show("debug_database")]
                textbutton "Нет, отмена" style "debug_confirm_button_cancel" action Hide("confirm_clear_db")

################################################################################
## Функции для работы с данными
################################################################################

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
                            if isinstance(last_save, (int, float)):
                                last_time = time.strftime("%d.%m.%Y %H:%M", time.localtime(float(last_save)))
                            else:
                                last_time = str(last_save)
                        except:
                            last_time = str(last_save)
        
        return last_time
    
    def reset_all_achievements():
        """Сброс всех достижений"""
        persistent._achievements = {}
        renpy.notify("✅ Все достижения сброшены")
    
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
        
        renpy.notify("🗑️ База данных полностью очищена")

################################################################################
## Стили для отладки
################################################################################

style debug_info_frame:
    background Frame("gui/frame.png", 15, 15, 15, 15)
    xmaximum 1000

style debug_table_frame:
    background Frame("gui/frame.png", 15, 15, 15, 15)

style debug_table_header:
    background "#ffa46f"
    xfill True

style debug_table_row:
    background "#ffbc95"
    hover_background "#b8754d"
    selected_background "#ffd8c1"
    xfill True
    padding (10, 8)
    margin (0, 2)

style debug_detail_frame:
    background Frame("gui/frame.png", 15, 15, 15, 15)

style debug_achievement_item:
    background Frame("gui/confirm_frame_1.png", 15, 15, 15, 15)
    xfill True
    margin (0, 2)

style debug_action_frame:
    background Frame("gui/confirm_frame.png", 15, 15, 15, 15)

style debug_action_button:
    padding (30, 15)
    xsize 500
    xalign 0.5

style debug_action_button_text:
    color "#ffffff"
    hover_color gui.hover_color
    size 22
    font gui.interface_text_font
    outlines [(2, "#602e14", 0, 0)]
    text_align 0.5

style debug_back_button:
    background None
    hover_background None
    padding (10, 5)

style debug_back_button_text:
    color "#494949"
    hover_color gui.hover_color
    size 24
    font gui.interface_text_font
    outlines [(1, "#855133", 0, 0)]

style debug_confirm_frame:
    background Frame("gui/choice_idle_background_0.png", 25, 25, 25, 25)
    padding (25, 25)

style debug_confirm_button_danger:
    background Frame("gui/button/choice_idle_background.png", 15, 15, 15, 15)
    hover_background Frame("gui/button/choice_hover_background.png", 15, 15, 15, 15)
    padding (50, 10)
    xsize 200

style debug_confirm_button_danger_text:
    color "#ff8d67"
    hover_color "#ffffff"
    size 14
    font gui.interface_text_font
    text_align 0.5

style debug_confirm_button_cancel:
    background Frame("gui/button/choice_idle_background.png", 15, 15, 15, 15)
    hover_background Frame("gui/button/choice_hover_background.png", 15, 15, 15, 15)
    padding (50, 10)
    xsize 200

style debug_confirm_button_cancel_text:
    color "#ff8d67"
    hover_color "#ffffff"
    size 14
    font gui.interface_text_font
    text_align 0.5