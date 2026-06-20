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
            current_user_id = persistent.user_id if hasattr(persistent, 'user_id') else None
            
            # Проверяем только слоты текущего игрока
            for i in range(1, 10):
                slot_str = str(i)
                if renpy.can_load(slot_str):
                    save_json = renpy.json_load(renpy.slot_json_filename(slot_str))
                    if save_json:
                        save_user_id = save_json.get('user_id')
                        # Загружаем только сохранения текущего игрока
                        if save_user_id == current_user_id or current_user_id is None:
                            timestamp = save_json.get('_timestamp', 0)
                            if timestamp > latest_time:
                                latest_time = timestamp
                                latest_slot = slot_str
            
            if latest_slot:
                save_json = renpy.json_load(renpy.slot_json_filename(latest_slot))
                if save_json and 'player_state' in save_json:
                    state = save_json['player_state']
                    metrics['self_awareness'] = state.get('self_awareness', 0)
                    metrics['empathy'] = state.get('empathy', 0)
                    metrics['vocabulary'] = state.get('vocabulary', 0)
                    metrics['anxiety'] = state.get('anxiety', 50)
                    metrics['trust'] = state.get('trust', 30)
                    metrics['ei_score'] = int((metrics['self_awareness'] + metrics['empathy']) / 2)
        except:
            pass
        
        return metrics

    def clear_database():
        """Полная очистка базы данных и всех сохранений"""
        # Вызываем новый метод очистки из database.rpy
        if 'db' in globals() and hasattr(db, 'clear_all_data'):
            db.clear_all_data()
        else:
            # Ручная очистка, если db недоступна
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
            persistent.player_states = {}
            
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
            spacing 20
            xfill True
            
            text "Информация об игроках":
                size 40
                color gui.accent_color
                xalign 0.5
                outlines [(2, "#671a1a", 0, 0)]
            
            frame:
                background Frame("gui/confirm_frame.png", 15, 15)
                xalign 0.5
                xsize 1200
                padding (20, 15)
                
                hbox:
                    spacing 30
                    xalign 0.5
                    text "Текущий игрок:":
                        size 26
                        outlines [(1, "#671a1a", 0, 0)]
                    $ current_user_name = persistent.user_name if hasattr(persistent, 'user_name') and persistent.user_name else "Не задан"
                    $ current_user_id = persistent.user_id if hasattr(persistent, 'user_id') and persistent.user_id else "Не задан"
                    text "[current_user_name]":
                        size 26
                        color gui.accent_color
                        outlines [(1, "#671a1a", 0, 0)]
                    text "(ID: [current_user_id])":
                        size 24
                        outlines [(1, "#671a1a", 0, 0)]
            
            null height 10
            
            hbox:
                spacing 20
                xalign 0.5
                textbutton "Обновить":
                    action Show("debug_database")
                    background Frame("gui/button/choice_idle_background.png", 15, 15)
                    hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                    padding (15, 8)
                textbutton "Очистить БД":
                    action Show("confirm_clear_db")
                    background Frame("gui/button/choice_idle_background.png", 15, 15)
                    hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                    padding (15, 8)
            
            null height 20
            
            frame:
                background Frame("gui/confirm_frame.png", 15, 15)
                xsize 1200
                xalign 0.5
                padding (20, 15)
                
                vbox:
                    spacing 15
                    xfill True
                    
                    text "Все игроки (нажмите на строку для просмотра деталей):":
                        size 26
                        color gui.accent_color
                        outlines [(1, "#671a1a", 0, 0)]
                    
                    $ users = db.get_all_users() if hasattr(db, 'get_all_users') else []
                    
                    if users:
                        frame:
                            background "#c66b2f"
                            xfill True
                            padding (10, 10)
                            
                            hbox:
                                spacing 20
                                xfill True
                                
                                text "ID":
                                    size 20
                                    xsize 80
                                    text_align 0.5
                                    outlines [(1, "#671a1a", 0, 0)]
                                text "Имя":
                                    size 20
                                    xsize 200
                                    text_align 0.5
                                    outlines [(1, "#671a1a", 0, 0)]
                                text "Прогресс":
                                    size 20
                                    xsize 250
                                    text_align 0.5
                                    outlines [(1, "#671a1a", 0, 0)]
                                text "ЭИ":
                                    size 20
                                    xsize 200
                                    text_align 0.5
                                    outlines [(1, "#671a1a", 0, 0)]
                                text "Статистика":
                                    size 20
                                    xsize 300
                                    text_align 0.5
                                    outlines [(1, "#671a1a", 0, 0)]
                        
                        viewport:
                            mousewheel True
                            ysize 400
                            vbox:
                                spacing 2
                                for user in users:
                                    $ user_id = user['user_ID']
                                    $ user_name = user['name']
                                    
                                    button:
                                        xfill True
                                        action Show("user_details", user_id=user_id, user_name=user_name)
                                        background Frame("gui/frame.png", 10, 10)
                                        hover_background Solid("#703f0e")
                                        padding (10, 8)
                                        
                                        hbox:
                                            spacing 20
                                            xfill True
                                            
                                            text "[user_id]":
                                                size 20
                                                xsize 80
                                                text_align 0.5
                                                outlines [(1, "#671a1a", 0, 0)]
                                            text "[user_name]":
                                                size 20
                                                xsize 200
                                                text_align 0.5
                                                outlines [(1, "#671a1a", 0, 0)]
                                            
                                            $ progress = get_user_progress(user_id)
                                            $ total_chapters = 3
                                            $ completed = len(progress)
                                            $ progress_percent = int((completed / total_chapters) * 100)
                                            
                                            vbox:
                                                xsize 250
                                                text "Глав: [completed]/[total_chapters]":
                                                    size 18
                                                    xalign 0.5
                                                    outlines [(1, "#671a1a", 0, 0)]
                                                bar:
                                                    value progress_percent
                                                    range 100
                                                    xsize 200
                                                    ysize 15
                                                    left_bar "#4caf50"
                                                    right_bar "#3a3a3a"
                                            
                                            $ metrics = get_player_metrics_from_saves(user_id)
                                            $ ei_score = metrics.get('ei_score', 0)
                                            
                                            if ei_score >= 50:
                                                $ ei_color_val = "#ffaa66"
                                            else:
                                                $ ei_color_val = "#888888"
                                            
                                            text "ЭИ: [ei_score]%":
                                                size 20
                                                color ei_color_val
                                                xsize 200
                                                text_align 0.5
                                                outlines [(1, "#671a1a", 0, 0)]
                                            
                                            if 'get_emotion_stats' in globals() and callable(get_emotion_stats):
                                                $ emotion_stats = get_emotion_stats(user_id)
                                            else:
                                                $ emotion_stats = {'total_attempts': 0, 'correct_matches': 0}
                                            $ total_attempts = emotion_stats.get('total_attempts', 0)
                                            $ correct = emotion_stats.get('correct_matches', 0)
                                            $ acc = int((correct / max(total_attempts, 1)) * 100)
                                            
                                            if acc >= 70:
                                                $ acc_color_val = "#4caf50"
                                            elif acc >= 40:
                                                $ acc_color_val = "#ffaa66"
                                            else:
                                                $ acc_color_val = "#888888"
                                            
                                            vbox:
                                                xsize 300
                                                text "Попыток: [total_attempts]":
                                                    size 18
                                                    outlines [(1, "#671a1a", 0, 0)]
                                                text "Точность: [acc]%":
                                                    size 18
                                                    color acc_color_val
                                                    outlines [(1, "#671a1a", 0, 0)]
                    else:
                        text "Нет игроков в базе данных":
                            size 22
                            xalign 0.5

################################################################################
## ЭКРАН ДЕТАЛЬНОЙ ИНФОРМАЦИИ О ПОЛЬЗОВАТЕЛЕ
################################################################################

screen user_details(user_id, user_name):
    tag menu
    
    $ title_text = "Детали игрока: " + user_name + " (ID: " + str(user_id) + ")"
    
    use game_menu(_(title_text), scroll="viewport"):
        vbox:
            spacing 20
            xfill True
            
            button:
                action Show("debug_database")
                background None
                hover_background None
                padding (10, 5)
                
                hbox:
                    spacing 8
                    text "<--":
                        size 28
                        outlines [(1, "#671a1a", 0, 0)]
                    text "Назад к списку игроков":
                        size 26
                        hover_color gui.hover_color
                        outlines [(1, "#671a1a", 0, 0)]
            
            null height 10
            
            python:
                if hasattr(persistent, 'user_data') and persistent.user_data:
                    str_id = str(user_id)
                    save_progress = persistent.user_data.get('save_progress', {}).get(str_id, [])
                    completed_chapters = len(set([s.get('chapter', '') for s in save_progress if s.get('chapter')]))
                else:
                    completed_chapters = 0
                total_chapters = 3
                progress_percent = int((completed_chapters / total_chapters) * 100)
            
            frame:
                background Frame("gui/confirm_frame.png", 15, 15)
                xfill True
                padding (25, 20)
                
                vbox:
                    spacing 15
                    
                    text "Прогресс игрока:":
                        size 26
                        color gui.accent_color
                        outlines [(1, "#671a1a", 0, 0)]
                    
                    text "[progress_percent]% глав пройдено":
                        size 20
                        xalign 0.5
                    bar:
                        value progress_percent
                        range 100
                        xsize 800
                        ysize 25
                        left_bar "#4caf50"
                        right_bar "#3a3a3a"
                        xalign 0.5
            
            null height 10
            
            frame:
                background Frame("gui/confirm_frame.png", 15, 15)
                xfill True
                padding (25, 20)
                
                vbox:
                    spacing 15
                    
                    text "Информация об игроке:":
                        size 26
                        color gui.accent_color
                        outlines [(1, "#671a1a", 0, 0)]
                    
                    $ metrics = get_player_metrics_from_saves(user_id)
                    
                    vbox:
                        spacing 10
                        
                        hbox:
                            spacing 30
                            xalign 0.5
                            text "Самопонимание:":
                                size 20
                            text "[metrics.get('self_awareness', 0)]%":
                                size 20
                                color "#c66b2f"
                                outlines [(1, "#1a1a1a", 0, 0)]
                        
                        hbox:
                            spacing 30
                            xalign 0.5
                            text "Эмпатия:":
                                size 20
                            text "[metrics.get('empathy', 0)]%":
                                size 20
                                color "#c66b2f"
                                outlines [(1, "#1a1a1a", 0, 0)]
                        
                        hbox:
                            spacing 30
                            xalign 0.5
                            text "Словарь эмоций:":
                                size 20
                            text "[metrics.get('vocabulary', 0)]%":
                                size 20
                                color "#c66b2f"
                                outlines [(1, "#1a1a1a", 0, 0)]
                        
                        hbox:
                            spacing 30
                            xalign 0.5
                            text "Тревожность:":
                                size 20
                            text "[metrics.get('anxiety', 50)]%":
                                size 20
                                color "#ff6666"
                                outlines [(1, "#1a1a1a", 0, 0)]
                        
                        hbox:
                            spacing 30
                            xalign 0.5
                            text "Доверие:":
                                size 20
                            text "[metrics.get('trust', 30)]%":
                                size 20
                                color "#4caf50"
                                outlines [(1, "#1a1a1a", 0, 0)]
            
            null height 10
            
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
        xsize 600
        ysize 450
        padding (30, 30)
        
        vbox:
            spacing 25
            xalign 0.5
            yalign 0.5
            
            text "ВНИМАНИЕ!":
                size 40
                color "#ff4444"
                xalign 0.5
                bold True
                outlines [(2, "#1a1a1a", 0, 0)]
            
            text "Вы уверены, что хотите очистить базу данных?":
                size 22
                xalign 0.5
                text_align 0.5
            
            text "Это действие НЕОБРАТИМО!":
                size 20
                color "#ff4444"
                xalign 0.5
                bold True
                outlines [(1, "#1a1a1a", 0, 0)]
            
            text "Будут удалены: все игроки, достижения, прогресс, сохранения и открытые изображения.":
                size 18
                xalign 0.5
                text_align 0.5
                color "#ffaa66"
            null height 10
            
            hbox:
                spacing 30
                xalign 0.5
                
                textbutton "ДА, ОЧИСТИТЬ":
                    action [Function(clear_database), Hide("confirm_clear_db"), Show("debug_database")]
                    background Frame("gui/button/choice_idle_background.png", 15, 15)
                    hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                    padding (15, 10)
                    xsize 180
                
                textbutton "ОТМЕНА":
                    action Hide("confirm_clear_db")
                    background Frame("gui/button/choice_idle_background.png", 15, 15)
                    hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                    padding (15, 10)
                    xsize 180
    
    key "K_ESCAPE" action Hide("confirm_clear_db")
    key "game_menu" action Hide("confirm_clear_db")

style stats_close_button_text:
    color "#ffffff"
    hover_color "#ff9999"
    size 24
    text_align 0.5
    outlines [(1, "#1a1a1a", 0, 0)]