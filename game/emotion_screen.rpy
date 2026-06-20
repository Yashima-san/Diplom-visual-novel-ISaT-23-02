################################################################################
## МИНИ-ИГРА: КОЛЕСО ЭМОЦИЙ РОБЕРТА ПЛУТЧИКА
################################################################################

init python:
    plutchik_emotions = {
        "joy": {
            "name": "Радость",
            "name_ru": "Радость",
            "color": "#FFD700",
            "icon": "😊",
            "intensity": 1,
            "opposite": "sadness",
            "description": "Чувство удовлетворения, счастья, восторга"
        },
        "trust": {
            "name": "Доверие",
            "name_ru": "Доверие",
            "color": "#90EE90",
            "icon": "🤝",
            "intensity": 1,
            "opposite": "disgust",
            "description": "Чувство безопасности, уверенности, открытости"
        },
        "fear": {
            "name": "Страх",
            "name_ru": "Страх",
            "color": "#9370DB",
            "icon": "😨",
            "intensity": 1,
            "opposite": "anger",
            "description": "Ожидание опасности, тревога, беспокойство"
        },
        "surprise": {
            "name": "Удивление",
            "name_ru": "Удивление",
            "color": "#32CD32",
            "icon": "😲",
            "intensity": 1,
            "opposite": "anticipation",
            "description": "Реакция на неожиданное событие"
        },
        "sadness": {
            "name": "Печаль",
            "name_ru": "Печаль",
            "color": "#6495ED",
            "icon": "😔",
            "intensity": 1,
            "opposite": "joy",
            "description": "Чувство потери, разочарования, тоски"
        },
        "disgust": {
            "name": "Отвращение",
            "name_ru": "Отвращение",
            "color": "#8B4513",
            "icon": "🤢",
            "intensity": 1,
            "opposite": "trust",
            "description": "Неприятие, отторжение чего-либо"
        },
        "anger": {
            "name": "Гнев",
            "name_ru": "Гнев",
            "color": "#DC143C",
            "icon": "😠",
            "intensity": 1,
            "opposite": "fear",
            "description": "Сильное возмущение, злость, раздражение"
        },
        "anticipation": {
            "name": "Предвкушение",
            "name_ru": "Предвкушение",
            "color": "#FFA500",
            "icon": "🤔",
            "intensity": 1,
            "opposite": "surprise",
            "description": "Ожидание будущего события, надежда"
        }
    }
    
    emotion_scenarios = {
        "morning_school": {
            "title": "Утро в новой школе",
            "situation": "Ты стоишь у входа в новую школу. Сердце бьётся чаще обычного. Ладони слегка влажные. Ты видишь, как ученики заходят внутрь, кто-то смеётся, кто-то серьёзно обсуждает что-то.",
            "possible_emotions": ["fear", "anticipation", "surprise"],
            "best_emotion": "anticipation",
            "feedback": {
                "correct": "Ты верно определила! Волнение перед новым — это нормально. Предвкушение помогает настроиться на позитивный лад.",
                "partial": "Интересный выбор! Но попробуй прислушаться к своим ощущениям — что именно ты чувствуешь?",
                "wrong": "Это эмоция, но возможно, сейчас ты испытываешь что-то другое. Прислушайся к своему телу."
            }
        },
        "first_lesson": {
            "title": "Первый урок",
            "situation": "Учительница объявляет, что будет проверочная работа. В классе воцаряется тишина. Твои мысли путаются, в животе появляется неприятное ощущение.",
            "possible_emotions": ["fear", "anger", "surprise"],
            "best_emotion": "fear",
            "feedback": {
                "correct": "Ты правильно распознала страх! Это естественная реакция на неожиданные испытания.",
                "partial": "Близко! Но какая эмоция сейчас преобладает?",
                "wrong": "Попробуй ещё раз. Прислушайся к сигналам своего тела."
            }
        }
    }
    
    def get_emotion_stats(user_id):
        try:
            if hasattr(persistent, 'emotion_stats') and persistent.emotion_stats:
                str_id = str(user_id)
                if str_id in persistent.emotion_stats:
                    stats = persistent.emotion_stats[str_id]
                    return {
                        'total_attempts': stats.get('total_attempts', 0),
                        'correct_matches': stats.get('correct_matches', 0),
                        'emotions_chosen': stats.get('emotions_chosen', {})
                    }
        except:
            pass
        return {'total_attempts': 0, 'correct_matches': 0, 'emotions_chosen': {}}
    
    def save_emotion_stats(user_id, is_correct, emotion_chosen):
        try:
            if not hasattr(persistent, 'emotion_stats') or persistent.emotion_stats is None:
                persistent.emotion_stats = {}
            
            str_id = str(user_id)
            if str_id not in persistent.emotion_stats:
                persistent.emotion_stats[str_id] = {
                    'total_attempts': 0,
                    'correct_matches': 0,
                    'emotions_chosen': {}
                }
            
            stats = persistent.emotion_stats[str_id]
            stats['total_attempts'] += 1
            
            if is_correct:
                stats['correct_matches'] += 1
            
            if emotion_chosen and emotion_chosen != "skip":
                if emotion_chosen not in stats['emotions_chosen']:
                    stats['emotions_chosen'][emotion_chosen] = 0
                stats['emotions_chosen'][emotion_chosen] += 1
        except:
            pass

# ============================================================================
# ЭКРАН КОЛЕСА ЭМОЦИЙ С РЕГУЛИРУЕМЫМИ ПАРАМЕТРАМИ
# ============================================================================
screen plutchik_wheel(scenario_data, scenario_id):
    modal True
    zorder 200
    add "gui/overlay/confirm.png"
    
    default selected_emotion = None
    default show_hint = False
    default hint_text = ""
    
    # ====== НАСТРОЙКИ ЭКРАНА ======
    python:
        # Размеры кнопок эмоций
        emotion_button_width = 250      # ← РЕГУЛИРУЙ ШИРИНУ КНОПОК
        emotion_button_height = 70      # ← РЕГУЛИРУЙ ВЫСОТУ КНОПОК
        emotion_button_text_size = 22   # ← РЕГУЛИРУЙ РАЗМЕР ШРИФТА КНОПОК
        
        # Размеры кнопок действий
        action_button_width = 320       # ← РЕГУЛИРУЙ ШИРИНУ КНОПОК ДЕЙСТВИЙ
        action_button_height = 60       # ← РЕГУЛИРУЙ ВЫСОТУ КНОПОК ДЕЙСТВИЙ
        action_button_text_size = 20    # ← РЕГУЛИРУЙ РАЗМЕР ШРИФТА КНОПОК ДЕЙСТВИЙ
        
        title = scenario_data.get('title', 'Колесо эмоций')
        situation = scenario_data.get('situation', '')
        possible = scenario_data.get('possible_emotions', [])
        best_id = scenario_data.get('best_emotion', 'joy')
    
    frame:
        background Frame("gui/confirm_frame.png", 25, 25)
        padding (30, 30)
        xysize (1200, 800)
        xalign 0.5
        yalign 0.5
        
        vbox:
            spacing 15
            xfill True
            
            text title:
                size 34
                color gui.accent_color
                xalign 0.5
                outlines [(2, "#671a1a", 0, 0)]
            
            frame:
                background Frame("gui/frame.png", 15, 15)
                xsize 1000
                padding (20, 15)
                xalign 0.5
                yalign 0.5
                text situation:
                    size 20
                    text_align 0.0
                    xfill True
            
            null height 15
            
            # ====== БЛОК С ЭМОЦИЯМИ ======
            hbox:
                spacing 25
                xfill True
                
                # ЛЕВАЯ ЧАСТЬ: КНОПКИ ЭМОЦИЙ
                vbox:
                    xsize 600
                    spacing 10
                    
                    text "Выбери эмоцию, которую ты сейчас чувствуешь:":
                        size 20
                        xalign 0.5
                        outlines [(1, "#1a1a1a", 0, 0)]
                    
                    # Сетка эмоций (2 строки x 4 колонки)
                    grid 2 4:
                        spacing 15
                        xalign 0.5
                        
                        for emo_id, emo_data in plutchik_emotions.items():
                            $ emo_name = emo_data['name_ru']
                            $ emo_icon = emo_data['icon']
                            $ emo_color = emo_data['color']
                            
                            if selected_emotion == emo_id:
                                $ btn_bg = Solid(emo_color + "55")
                                $ check_mark = " ✓"
                                $ text_color_value = "#ffffff"
                            else:
                                $ btn_bg = Solid(emo_color + "22")
                                $ check_mark = ""
                                $ text_color_value = "#e0e0e0"
                            
                            button:
                                xsize emotion_button_width
                                ysize emotion_button_height
                                action SetScreenVariable("selected_emotion", emo_id)
                                background btn_bg
                                hover_background Solid(emo_color + "77")
                                
                                frame:
                                    xfill True
                                    yfill True
                                    background None
                                    padding (10, 10)
                                    text "[emo_icon] [emo_name][check_mark]":
                                        size emotion_button_text_size
                                        color text_color_value
                                        xalign 0.5
                                        yalign 0.5
                                        outlines [(1, "#1a1a1a", 0, 0)]
                
                # ПРАВАЯ ЧАСТЬ: ИНФОРМАЦИЯ О ВЫБРАННОЙ ЭМОЦИИ
                vbox:
                    xsize 400
                    spacing 15
                    yalign 0.5
                    
                    if selected_emotion:
                        $ sel_data = plutchik_emotions.get(selected_emotion, {})
                        $ sel_name = sel_data.get('name_ru', '')
                        $ sel_icon = sel_data.get('icon', '?')
                        $ sel_color = sel_data.get('color', '#ffffff')
                        $ sel_desc = sel_data.get('description', '')
                        $ opposite_id = sel_data.get('opposite', '')
                        $ opposite_name = plutchik_emotions.get(opposite_id, {}).get('name_ru', 'неизвестно')
                        
                        frame:
                            background Frame("gui/overlay/confirm.png", 15, 15)
                            padding (15, 12)
                            xfill True
                            xalign 0.5
                            vbox:
                                spacing 8
                                xalign 0.5
                                text "Твой выбор:":
                                    size 18
                                    xalign 0.5
                                    outlines [(1, "#1a1a1a", 0, 0)]
                                text "[sel_icon] [sel_name]":
                                    size 32
                                    color sel_color
                                    xalign 0.5
                                    outlines [(2, "#1a1a1a", 0, 0)]
                                text "[sel_desc]":
                                    size 15
                                    xalign 0.5
                                    text_align 0.5
                                text "Противоположная эмоция: [opposite_name]":
                                    size 14
                                    xalign 0.5
                        
                        if selected_emotion == best_id:
                            text "Точное попадание!":
                                size 20
                                color "#4caf50"
                                xalign 0.5
                                outlines [(1, "#216717", 0, 0)]
                        elif selected_emotion in possible:
                            text "Хороший вариант!":
                                size 20
                                color "#ff9800"
                                xalign 0.5
                                outlines [(1, "#9f691e", 0, 0)]

                        else:
                            text "Возможно, стоит присмотреться к другим эмоциям":
                                size 20
                                color "#ff5722"
                                xalign 0.5
                                outlines [(1, "#923a1c", 0, 0)]

                    
                    # Кнопка подсказки
                    if show_hint:
                        frame:
                            background Frame("gui/frame.png", 10, 10)
                            padding (12, 10)
                            xfill True
                            xalign 0.5
                            text "[hint_text]":
                                size 16
                                text_align 0.0
                        
                        textbutton "Скрыть подсказку":
                            xalign 0.5
                            action SetScreenVariable("show_hint", False)
                            background Frame("gui/button/choice_idle_background.png", 15, 15)
                            hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                            padding (12, 8)
                            xsize action_button_width
                            text_size action_button_text_size
                    else:
                        textbutton "Показать подсказку":
                            xalign 0.5
                            action SetScreenVariable("show_hint", True)
                            hovered SetScreenVariable("hint_text", "Обрати внимание на свои телесные ощущения:\n• Как бьётся сердце?\n• Какое дыхание?\n• Что чувствуешь в теле?")
                            background Frame("gui/button/choice_idle_background.png", 15, 15)
                            hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                            padding (12, 8)
                            xsize action_button_width
                            text_size action_button_text_size
            
            # ====== ОТДЕЛЬНЫЙ БЛОК С КНОПКАМИ ДЕЙСТВИЙ ======
            null height 70
            vbox:
                spacing 50
                xfill True

                hbox:
                    spacing 20
                    xalign 0.5
                    
                    if selected_emotion:
                        textbutton "Подтвердить выбор":
                            background Frame("gui/button/choice_idle_background.png", 15, 15)
                            hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                            padding (40, 10)
                            xsize action_button_width
                            ysize action_button_height
                            text_size action_button_text_size
                            action Return(selected_emotion)
                    else:
                        textbutton "Подтвердить выбор":
                            background Frame("gui/button/choice_idle_background.png", 15, 15)
                            hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                            padding (40, 10)
                            xsize action_button_width
                            ysize action_button_height
                            text_size action_button_text_size
                            action Return(None)
                            sensitive False
                    
                    textbutton "Пропустить":
                        background Frame("gui/button/choice_idle_background.png", 15, 15)
                        hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                        padding (15, 10)
                        xsize action_button_width
                        ysize action_button_height
                        text_size action_button_text_size
                        action Return("skip")
    
    key "K_ESCAPE" action Return("skip")
    key "game_menu" action Return("skip")

label emotion_wheel_game(scenario_id="morning_school"):
    python:
        scenario = emotion_scenarios.get(scenario_id, emotion_scenarios["morning_school"])
    
    call screen plutchik_wheel(scenario, scenario_id)
    $ result = _return
    
    if result == "skip":
        $ update_player_state(self_awareness_change=2, vocabulary_change=1)
        $ save_emotion_stats(persistent.user_id, False, "skip")
        return
    
    $ selected = result
    $ best = scenario.get('best_emotion', 'joy')
    $ possible = scenario.get('possible_emotions', [])
    $ selected_name = plutchik_emotions.get(selected, {}).get('name_ru', selected)
    
    if selected == best:
        $ is_correct = True
        $ feedback_text = scenario.get('feedback', {}).get('correct', "Ты верно определила эмоцию!")
        narrator "[feedback_text]"
        $ update_player_state(self_awareness_change=12, empathy_change=5, vocabulary_change=8, anxiety_change=-5)
    elif selected in possible:
        $ is_correct = True
        $ feedback_text = scenario.get('feedback', {}).get('partial', "Хороший вариант! Ты на верном пути.")
        narrator "[feedback_text]"
        $ update_player_state(self_awareness_change=8, empathy_change=3, vocabulary_change=5, anxiety_change=-3)
    else:
        $ is_correct = False
        $ feedback_text = scenario.get('feedback', {}).get('wrong', "Попробуй ещё раз. Прислушайся к своим ощущениям.")
        narrator "[feedback_text]"
        $ update_player_state(self_awareness_change=5, vocabulary_change=3, anxiety_change=2)
    
    $ save_emotion_stats(persistent.user_id, is_correct, selected)
    
    return