################################################################################
## ЭКРАН ОТЛАДКИ БАЗЫ ДАННЫХ
################################################################################

init python:
    import time

    def get_user_progress(user_id):
        """Получение прогресса игрока по главам"""
        progress = []
        if hasattr(persistent, 'user_data') and persistent.user_data:
            str_user_id = str(user_id)
            if 'save_progress' in persistent.user_data and str_user_id in persistent.user_data['save_progress']:
                for save in persistent.user_data['save_progress'][str_user_id]:
                    if 'chapter' in save and save['chapter'] not in progress:
                        progress.append(save['chapter'])
        
        if hasattr(db, 'sqlite_available') and db.sqlite_available:
            try:
                db.connect()
                db.cursor.execute('''SELECT DISTINCT chapter FROM save_progress_users WHERE user_ID = ?''', (user_id,))
                for row in db.cursor.fetchall():
                    chapter = row['chapter']
                    if chapter and chapter not in progress:
                        progress.append(chapter)
            except:
                pass
            finally:
                db.disconnect()
        
        return progress

    def get_player_metrics_from_saves(user_id):
        """Получение метрик игрока из сохранений"""
        metrics = {
            'ei_score': 0,
            'anxiety': 50,
            'trust': 30,
            'self_awareness': 0,
            'empathy': 0,
            'vocabulary': 0
        }
        
        try:
            latest_slot = None
            latest_time = 0
            for i in range(1, 10):
                slot_str = str(i)
                if renpy.can_load(slot_str):
                    try:
                        save_data = renpy.slot_json(slot_str)
                        if save_data:
                            timestamp = save_data.get('_timestamp', 0)
                            if timestamp > latest_time:
                                latest_time = timestamp
                                latest_slot = slot_str
                    except:
                        pass
            
            if latest_slot:
                try:
                    save_data = renpy.slot_json(latest_slot)
                    if save_data and 'player_state' in save_data:
                        state = save_data['player_state']
                        metrics['self_awareness'] = state.get('self_awareness', 0)
                        metrics['empathy'] = state.get('empathy', 0)
                        metrics['vocabulary'] = state.get('vocabulary', 0)
                        metrics['anxiety'] = state.get('anxiety', 50)
                        metrics['trust'] = state.get('trust', 30)
                        metrics['ei_score'] = int((metrics['self_awareness'] + metrics['empathy']) / 2)
                except:
                    pass
        except:
            pass
        
        return metrics

    def get_user_saves(user_id):
        """Получение списка сохранений пользователя"""
        saves = []
        try:
            for i in range(1, 10):
                slot_str = str(i)
                if renpy.can_load(slot_str):
                    try:
                        save_data = renpy.slot_json(slot_str)
                        if save_data:
                            save_user_id = save_data.get('user_id')
                            if save_user_id == user_id:
                                chapter = save_data.get('chapter', 'Неизвестная глава')
                                timestamp = save_data.get('_timestamp', 0)
                                if timestamp > 0:
                                    date_str = time.strftime('%d.%m.%Y %H:%M', time.localtime(timestamp))
                                else:
                                    date_str = 'Неизвестно'
                                saves.append({
                                    'slot': i,
                                    'chapter': chapter,
                                    'date': date_str,
                                    'timestamp': timestamp
                                })
                    except:
                        pass
        except:
            pass
        return sorted(saves, key=lambda x: x['timestamp'], reverse=True)

    def get_user_achievements_count(user_id):
        """Получение количества разблокированных достижений"""
        count = 0
        total = 0
        try:
            if hasattr(persistent, '_achievements') and isinstance(persistent._achievements, dict):
                for ach_id, unlocked in persistent._achievements.items():
                    total += 1
                    if unlocked:
                        count += 1
        except:
            pass
        return count, total

    def get_user_achievements_list(user_id):
        """Получение списка разблокированных достижений"""
        unlocked = []
        try:
            if hasattr(persistent, '_achievements') and isinstance(persistent._achievements, dict):
                for ach_id, unlocked_flag in persistent._achievements.items():
                    if unlocked_flag and ach_id in achievements:
                        unlocked.append(achievements[ach_id])
        except:
            pass
        return unlocked

    def get_user_gallery_progress(user_id):
        """Получение прогресса галереи"""
        unlocked = 0
        total = 0
        try:
            if hasattr(persistent, '_gallery_unlocks') and isinstance(persistent._gallery_unlocks, dict):
                if 'gallery_items' in globals():
                    for item in gallery_items:
                        total += 1
                        if item.is_unlocked():
                            unlocked += 1
        except:
            pass
        return unlocked, total

    def get_user_emotion_stats_count(user_id):
        """Получение статистики по эмоциям"""
        stats = {'total': 0, 'correct': 0, 'accuracy': 0}
        try:
            if hasattr(persistent, 'emotion_stats') and persistent.emotion_stats:
                str_id = str(user_id)
                if str_id in persistent.emotion_stats:
                    data = persistent.emotion_stats[str_id]
                    stats['total'] = data.get('total_attempts', 0)
                    stats['correct'] = data.get('correct_matches', 0)
                    if stats['total'] > 0:
                        stats['accuracy'] = int((stats['correct'] / stats['total']) * 100)
        except:
            pass
        return stats

    def custom_load_action(slot):
        """Загрузка сохранения с проверкой пользователя"""
        slot_str = str(slot)
        try:
            if renpy.can_load(slot_str):
                try:
                    save_data = renpy.slot_json(slot_str)
                    if save_data:
                        current_user_id = persistent.user_id if hasattr(persistent, 'user_id') else None
                        save_user_id = save_data.get("user_id")
                        if save_user_id is not None and save_user_id != current_user_id:
                            renpy.show_screen("confirm_user_switch", slot=slot)
                            return
                except:
                    pass
                renpy.load(slot_str)
            else:
                renpy.notify(f"Слот {slot} пуст")
        except Exception as e:
            renpy.notify(f"Ошибка загрузки: {str(e)}")

    def clear_database():
        """Очистка базы данных и всех сохранений"""
        persistent.user_data = {
            'users': {},
            'achievements': {},
            'save_progress': {},
            'next_id': 1
        }
        persistent._achievements = {}
        persistent._gallery_unlocks = {}
        persistent.emotion_stats = {}
        persistent.body_sensation_stats = {}
        persistent.reaction_stats = {}
        persistent.user_id = None
        persistent.user_name = ""
        
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
        
        try:
            for i in range(1, 10):
                renpy.unlink_save(str(i))
            for i in range(1, 10):
                renpy.unlink_save(f"auto-{i}")
            renpy.unlink_save("quick-save")
        except:
            pass
        
        renpy.notify("База данных и все сохранения очищены")
        return True

################################################################################
## ЭКРАН ОТЛАДКИ БАЗЫ ДАННЫХ
################################################################################

screen debug_database():
    tag menu
    use game_menu(_("Игроки"), scroll="viewport"):
        style_prefix "debug"
        
        vbox:
            spacing 15
            xfill True
            
            # ================================================================
            # ОДИН ФРЕЙМ СО ВСЕЙ ИНФОРМАЦИЕЙ
            # ================================================================
            frame:
                background Frame("gui/confirm_frame.png", 15, 15)
                xalign 0.5
                xysize (1200, 750)
                padding (20, 15)
                
                vbox:
                    spacing 15
                    xfill True
                    
                    text "Информация об игроках":
                        size 32
                        color gui.accent_color
                        xalign 0.5
                        outlines [(2, "#671a1a", 0, 0)]
                    
                    # Текущий игрок
                    frame:
                        background "#6f4427"
                        xsize 1100
                        xalign 0.5
                        padding (15, 12)
                        
                        hbox:
                            spacing 30
                            xalign 0.5
                            text "Текущий игрок:":
                                size 22
                                color "#cccccc"
                                outlines [(1, "#77472f", 0, 0)]
                            $ current_user_name = persistent.user_name if hasattr(persistent, 'user_name') and persistent.user_name else "Не задан"
                            $ current_user_id = persistent.user_id if hasattr(persistent, 'user_id') and persistent.user_id else "Не задан"
                            text "[current_user_name]":
                                size 22
                                color gui.accent_color
                                outlines [(1, "#77472f", 0, 0)]
                            text "(ID: [current_user_id])":
                                size 20
                                color "#cccccc"
                    
                    # Кнопки управления
                    hbox:
                        spacing 20
                        xalign 0.5
                        textbutton "Обновить":
                            action Show("debug_database")
                            background Frame("gui/button/choice_idle_background.png", 15, 15)
                            hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                            padding (25, 10)
                            xsize 320
                        textbutton "Очистить БД":
                            action Show("confirm_clear_db")
                            background Frame("gui/button/choice_idle_background.png", 15, 15)
                            hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                            padding (25, 10)
                            xsize 320
                    
                    # Разделитель
                    frame:
                        xsize 1000
                        ysize 4
                        xalign 0.5
                        background "#ac5032"
                    
                    # Заголовок списка
                    text "Все игроки (нажмите на строку для просмотра деталей):":
                        size 22
                        color gui.accent_color
                        xalign 0.5
                    
                    $ users = db.get_all_users() if hasattr(db, 'get_all_users') else []
                    
                    if users:
                        # Заголовки таблицы
                        frame:
                            background "#6f4427"
                            xsize 1100
                            padding (10, 10)
                            xalign 0.5
                            
                            hbox:
                                spacing 15
                                xfill True
                                
                                text "ID":
                                    size 18
                                    xsize 60
                                    text_align 0.5
                                    color "#cccccc"
                                    outlines [(1, "#77472f", 0, 0)]
                                text "Имя":
                                    size 18
                                    xsize 150
                                    text_align 0.5
                                    color "#cccccc"
                                    outlines [(1, "#77472f", 0, 0)]
                                text "Прогресс":
                                    size 18
                                    xsize 180
                                    text_align 0.5
                                    color "#cccccc"
                                    outlines [(1, "#77472f", 0, 0)]
                                text "Достиж.":
                                    size 18
                                    xsize 120
                                    text_align 0.5
                                    color "#cccccc"
                                    outlines [(1, "#77472f", 0, 0)]
                                text "Галерея":
                                    size 18
                                    xsize 120
                                    text_align 0.5
                                    color "#cccccc"
                                    outlines [(1, "#77472f", 0, 0)]
                                text "Сохранения":
                                    size 18
                                    xsize 200
                                    text_align 0.5
                                    color "#cccccc"
                                    outlines [(1, "#77472f", 0, 0)]
                                text "ЭИ":
                                    size 18
                                    xsize 100
                                    text_align 0.5
                                    color "#cccccc"
                                    outlines [(1, "#77472f", 0, 0)]
                        
                        # Список игроков
                        viewport:
                            ysize 350
                            xfill True
                            
                            vbox:
                                spacing 2
                                xfill True
                                
                                for user in users:
                                    $ user_id = user['user_ID']
                                    $ user_name = user['name']
                                    
                                    button:
                                        xsize 1100
                                        xalign 0.5
                                        action Show("user_details", user_id=user_id, user_name=user_name)
                                        background Frame("gui/frame.png", 10, 10)
                                        hover_background Solid("#3a2a1a")
                                        padding (10, 8)
                                        
                                        hbox:
                                            spacing 15
                                            xfill True
                                            
                                            # ID
                                            text "[user_id]":
                                                size 18
                                                xsize 60
                                                text_align 0.5
                                            
                                            # Имя
                                            text "[user_name]":
                                                size 18
                                                xsize 150
                                                text_align 0.5
                                            
                                            # Прогресс по главам
                                            $ progress = get_user_progress(user_id)
                                            $ total_chapters = 3
                                            $ completed = len(progress)
                                            $ progress_percent = int((completed / total_chapters) * 100)
                                            
                                            vbox:
                                                xsize 180
                                                text "Гл: [completed]/[total_chapters]":
                                                    size 16
                                                    xalign 0.5
                                                bar:
                                                    value progress_percent
                                                    range 100
                                                    xsize 160
                                                    ysize 12
                                                    left_bar "#4caf50"
                                                    right_bar "#3a3a3a"
                                                    xalign 0.5
                                            
                                            # Достижения
                                            $ ach_count, ach_total = get_user_achievements_count(user_id)
                                            text "[ach_count]/[ach_total]":
                                                size 18
                                                xsize 120
                                                text_align 0.5
                                            
                                            # Галерея
                                            $ gal_unlocked, gal_total = get_user_gallery_progress(user_id)
                                            text "[gal_unlocked]/[gal_total]":
                                                size 18
                                                xsize 120
                                                text_align 0.5
                                            
                                            # Сохранения
                                            $ saves = get_user_saves(user_id)
                                            $ save_text = str(len(saves)) if saves else "0"
                                            text "[save_text]":
                                                size 18
                                                xsize 200
                                                text_align 0.5
                                            
                                            # ЭИ
                                            $ metrics = get_player_metrics_from_saves(user_id)
                                            $ ei_score = metrics.get('ei_score', 0)
                                            
                                            if ei_score >= 50:
                                                $ ei_color_val = "#ffa052"
                                            else:
                                                $ ei_color_val = "#888888"
                                            
                                            text "[ei_score]%":
                                                size 18
                                                color ei_color_val
                                                xsize 100
                                                text_align 0.5
                    else:
                        text "Нет игроков в базе данных":
                            size 22
                            xalign 0.5

################################################################################
## ЭКРАН ДЕТАЛЬНОЙ ИНФОРМАЦИИ О ПОЛЬЗОВАТЕЛЕ (ВСЁ В ОДНОМ ФРЕЙМЕ)
################################################################################

screen user_details(user_id, user_name):
    tag menu
    
    $ title_text = "Детали игрока: " + user_name + " (ID: " + str(user_id) + ")"
    
    use game_menu(_(title_text), scroll="viewport"):
        vbox:
            spacing 15
            xfill True

            text "Статистика прохождения":
                        size 32
                        color gui.accent_color
                        xalign 0.5
                        outlines [(2, "#671a1a", 0, 0)]

            null height 5
            
            # ================================================================
            # ОДИН ФРЕЙМ СО ВСЕЙ ИНФОРМАЦИЕЙ
            # ================================================================
            frame:
                background Frame("gui/confirm_frame.png", 15, 15)
                xfill True
                padding (25, 20)
                
                vbox:
                    spacing 20
                    xfill True
                    
                    # ========================================================
                    # ПРОГРЕСС
                    # ========================================================
                    text "Прогресс по главам:":
                        size 28
                        color gui.accent_color
                        xalign 0.05
                        outlines [(1, "#671a1a", 0, 0)]
                    
                    $ progress = get_user_progress(user_id)
                    $ total_chapters = 3
                    $ completed = len(progress)
                    $ progress_percent = int((completed / total_chapters) * 100)
                    
                    text "[progress_percent]% глав пройдено ([completed]/[total_chapters])":
                        size 18
                        xalign 0.5
                    
                    bar:
                        value progress_percent
                        range 100
                        xsize 800
                        ysize 20
                        left_bar "#4caf50"
                        right_bar "#3a3a3a"
                        xalign 0.5
                    
                    if progress:
                        hbox:
                            spacing 15
                            xalign 0.5
                            for chapter in progress:
                                text "✓ [chapter]":
                                    size 16
                                    color "#4caf50"
                    
                    # Разделитель
                    frame:
                        xsize 900
                        ysize 4
                        xalign 0.5
                        background "#ac5032"
                    
                    # ========================================================
                    # ИНФОРМАЦИЯ ОБ ИГРОКЕ
                    # ========================================================
                    text "Информация об игроке:":
                        size 28
                        color gui.accent_color
                        xalign 0.05
                        outlines [(1, "#671a1a", 0, 0)]
                    
                    $ metrics = get_player_metrics_from_saves(user_id)
                    
                    grid 2 3:
                        spacing 15
                        xalign 0.5
                        
                        frame:
                            background "#3a2a1a"
                            padding (15, 10)
                            xsize 350
                            vbox:
                                spacing 5
                                text "Самопонимание:":
                                    size 18
                                    color "#cccccc"
                                    xalign 0.5
                                text "[metrics.get('self_awareness', 0)]%":
                                    size 24
                                    color "#c66b2f"
                                    xalign 0.5
                        
                        frame:
                            background "#3a2a1a"
                            padding (15, 10)
                            xsize 350
                            vbox:
                                spacing 5
                                text "Эмпатия:":
                                    size 18
                                    color "#cccccc"
                                    xalign 0.5
                                text "[metrics.get('empathy', 0)]%":
                                    size 24
                                    color "#c66b2f"
                                    xalign 0.5
                        
                        frame:
                            background "#3a2a1a"
                            padding (15, 10)
                            xsize 350
                            vbox:
                                spacing 5
                                text "Словарь эмоций:":
                                    size 18
                                    color "#cccccc"
                                    xalign 0.5
                                text "[metrics.get('vocabulary', 0)]%":
                                    size 24
                                    color "#c66b2f"
                                    xalign 0.5
                        
                        frame:
                            background "#3a2a1a"
                            padding (15, 10)
                            xsize 350
                            vbox:
                                spacing 5
                                text "Тревожность:":
                                    size 18
                                    color "#cccccc"
                                    xalign 0.5
                                text "[metrics.get('anxiety', 50)]%":
                                    size 24
                                    color "#ff6666"
                                    xalign 0.5
                        
                        frame:
                            background "#3a2a1a"
                            padding (15, 10)
                            xsize 350
                            vbox:
                                spacing 5
                                text "Доверие:":
                                    size 18
                                    color "#cccccc"
                                    xalign 0.5
                                text "[metrics.get('trust', 30)]%":
                                    size 24
                                    color "#4caf50"
                                    xalign 0.5
                        
                        frame:
                            background "#3a2a1a"
                            padding (15, 10)
                            xsize 350
                            vbox:
                                spacing 5
                                text "Эмоциональный интеллект:":
                                    size 18
                                    color "#cccccc"
                                    xalign 0.5
                                $ ei_score = metrics.get('ei_score', 0)
                                if ei_score >= 50:
                                    $ ei_color = "#ffaa66"
                                else:
                                    $ ei_color = "#888888"
                                text "[ei_score]%":
                                    size 24
                                    color ei_color
                                    xalign 0.5
                    
                    # Разделитель
                    frame:
                        xsize 900
                        ysize 4
                        xalign 0.5
                        background "#ac5032"
                    
                    # ========================================================
                    # ДОСТИЖЕНИЯ (только разблокированные)
                    # ========================================================
                    text "Достижения:":
                        size 28
                        color gui.accent_color
                        xalign 0.05
                        outlines [(1, "#671a1a", 0, 0)]
                    
                    $ ach_count, ach_total = get_user_achievements_count(user_id)
                    text "Разблокировано: [ach_count]/[ach_total]":
                        size 18
                        xalign 0.5
                    
                    $ unlocked_achievements = get_user_achievements_list(user_id)
                    
                    if unlocked_achievements:
                        hbox:
                            spacing 10
                            xalign 0.5
                            for ach in unlocked_achievements:
                                frame:
                                    background "#4caf50" + "33"
                                    padding (8, 5)
                                    xsize 250
                                    hbox:
                                        spacing 8
                                        text "🏆":
                                            size 20
                                        vbox:
                                            text ach.name:
                                                size 14
                                                color "#ffffff"
                                            text ach.description:
                                                size 11
                                                color "#cccccc"
                    else:
                        text "Нет разблокированных достижений":
                            size 16
                            xalign 0.5
                    
                    # Разделитель
                    frame:
                        xsize 900
                        ysize 4
                        xalign 0.5
                        background "#ac5032"
                    
                    # ========================================================
                    # ГАЛЕРЕЯ (только количество открытых)
                    # ========================================================
                    text "Галерея:":
                        size 28
                        color gui.accent_color
                        xalign 0.05
                        outlines [(1, "#671a1a", 0, 0)]
                    
                    $ gal_unlocked, gal_total = get_user_gallery_progress(user_id)
                    text "Открыто: [gal_unlocked]/[gal_total] картинок":
                        size 18
                        xalign 0.5
                    
                    # Разделитель
                    frame:
                        xsize 900
                        ysize 4
                        xalign 0.5
                        background "#ac5032"
                    
                    # ========================================================
                    # СОХРАНЕНИЯ
                    # ========================================================
                    text "Сохранения:":
                        size 28
                        color gui.accent_color
                        xalign 0.05
                        outlines [(1, "#671a1a", 0, 0)]
                    
                    $ saves = get_user_saves(user_id)
                    
                    if saves:
                        for save in saves:
                            frame:
                                background "#3a2a1a"
                                padding (10, 8)
                                xsize 1100
                                xalign 0.5
                                
                                hbox:
                                    spacing 20
                                    xfill True
                                    
                                    text "Слот [save['slot']]":
                                        size 16
                                        xsize 120
                                    
                                    text "[save['chapter']]":
                                        size 16
                                        xsize 300
                                    
                                    text "[save['date']]":
                                        size 16
                                        xsize 200
                                    
                                    textbutton "Загрузить":
                                        action [Function(custom_load_action, save['slot']), Hide("user_details")]
                                        background Frame("gui/button/choice_idle_background.png", 10, 10)
                                        hover_background Frame("gui/button/choice_hover_background_1.png", 10, 10)
                                        padding (10, 5)
                                        xsize 150
                    else:
                        text "Нет сохранений":
                            size 16
                            color "#888888"
                            xalign 0.5
            
            null height 15
            
            # ================================================================
            # КНОПКА ЗАКРЫТЬ
            # ================================================================
            textbutton "Закрыть":
                xalign 0.5
                action [Hide("user_details"), Show("debug_database")]
                background Frame("gui/button/choice_idle_background_0.png", 15, 15)
                hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                padding (25, 12)
                xsize 300
                text_style "stats_close_button_text"

################################################################################
## ЭКРАН ПОДТВЕРЖДЕНИЯ ОЧИСТКИ БД
################################################################################

screen confirm_clear_db():
    modal True
    zorder 200
    add "gui/overlay/confirm.png"
    
    frame:
        background Frame("gui/confirm_frame.png", 25, 25)
        xalign 0.5
        yalign 0.5
        xysize (720, 450)
        padding (30, 30)
        
        vbox:
            spacing 25
            xalign 0.5
            yalign 0.5
            
            text "ВНИМАНИЕ!":
                size 40
                color "#ff4444"
                xalign 0.5
                outlines [(1, "#641f1f", 0, 0)]
            
            text "Вы уверены, что хотите очистить базу данных?":
                size 22
                xalign 0.5
                text_align 0.5
            
            text "Это действие НЕОБРАТИМО!":
                size 20
                color "#ff4444"
                xalign 0.5
            
            null height 20
            
            hbox:
                spacing 30
                xalign 0.5
                
                textbutton "Да, очистить":
                    action [Function(clear_database), Hide("confirm_clear_db"), Show("debug_database")]
                    background Frame("gui/button/choice_idle_background.png", 15, 15)
                    hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                    padding (25, 15)
                    xsize 320
                
                textbutton "Отмена":
                    action Hide("confirm_clear_db")
                    background Frame("gui/button/choice_idle_background.png", 15, 15)
                    hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                    padding (25, 15)
                    xsize 320
    
    key "K_ESCAPE" action Hide("confirm_clear_db")
    key "game_menu" action Hide("confirm_clear_db")

style stats_close_button_text:
    color "#ffffff"
    hover_color "#ff9999"
    size 24
    text_align 0.5
    outlines [(1, "#1a1a1a", 0, 0)]