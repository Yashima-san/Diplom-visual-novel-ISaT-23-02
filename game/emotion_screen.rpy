################################################################################
## МИНИ-ИГРА: КОЛЕСО ЭМОЦИЙ РОБЕРТА ПЛУТЧИКА
################################################################################

init python:
    # База эмоций Плутчика (8 базовых эмоций)
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
    
    # Сценарии для мини-игры
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
        "meeting_friend": {
            "title": "Встреча с подругой",
            "situation": "Лина подходит к тебе с улыбкой и обнимает. Ты чувствуешь, как напряжение уходит. На душе становится тепло и спокойно.",
            "possible_emotions": ["joy", "trust", "sadness"],
            "best_emotion": "joy",
            "feedback": {
                "correct": "Верно! Радость от встречи с близким человеком — одно из самых тёплых чувств.",
                "partial": "Хороший вариант! А что ещё ты чувствуешь в этот момент?",
                "wrong": "Подумай ещё. Возможно, ты упускаешь что-то важное?"
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
        """Получение статистики по мини-игре"""
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
        """Сохранение статистики мини-игры"""
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
    
    def safe_get_emotion_stats(user_id):
        """Безопасное получение статистики для экранов"""
        try:
            stats = get_emotion_stats(user_id)
            return (stats.get('total_attempts', 0), stats.get('correct_matches', 0), stats.get('emotions_chosen', {}))
        except:
            return (0, 0, {})

################################################################################
## ЭКРАН МИНИ-ИГРЫ "КОЛЕСО ЭМОЦИЙ"
################################################################################

screen plutchik_wheel(scenario_data, scenario_id):
    modal True
    zorder 200
    add "#000000CC"
    
    default selected_emotion = None
    default show_hint = False
    default hint_text = ""
    
    # Получаем данные сценария
    python:
        title = scenario_data.get('title', 'Колесо эмоций')
        situation = scenario_data.get('situation', '')
        possible = scenario_data.get('possible_emotions', [])
        best_id = scenario_data.get('best_emotion', 'joy')
        best_name = plutchik_emotions.get(best_id, {}).get('name_ru', 'Радость')
    
    frame:
        background Frame("gui/confirm_frame.png", 25, 25)
        padding (40, 40)
        xysize (1400, 920)
        xalign 0.5
        yalign 0.5
        
        vbox:
            spacing 20
            xfill True
            
            # Заголовок
            text "🎡 [title]" size 38 color gui.accent_color xalign 0.5 bold True
            
            # Ситуация
            frame:
                background Frame("gui/frame.png", 15, 15)
                xfill True
                padding (25, 20)
                text "[situation]":
                    size 22
                    color "#ffffff"
                    text_align 0.0
                    xfill True
            
            # Основное содержимое
            hbox:
                spacing 30
                xfill True
                
                # Левая колонка - колесо эмоций
                vbox:
                    xsize 650
                    spacing 15
                    
                    text "Выбери эмоцию, которую ты сейчас чувствуешь:" size 22 color "#e0e0e0" xalign 0.5 bold True
                    
                    # Сетка эмоций 2x4 (базовые эмоции Плутчика)
                    grid 2 4:
                        spacing 20
                        xalign 0.5
                        
                        for emo_id, emo_data in plutchik_emotions.items():
                            $ emo_name = emo_data['name_ru']
                            $ emo_icon = emo_data['icon']
                            $ emo_color = emo_data['color']
                            
                            button:
                                xsize 280
                                ysize 90
                                action SetScreenVariable("selected_emotion", emo_id)
                                
                                frame:
                                    xfill True
                                    yfill True
                                    background (Solid(emo_color + "33") if selected_emotion == emo_id else Solid(emo_color + "11"))
                                    padding (10, 10)
                                    
                                    hbox:
                                        spacing 15
                                        xalign 0.5
                                        yalign 0.5
                                        
                                        text emo_icon size 42
                                        $ text_color_value = "#ffffff" if selected_emotion == emo_id else "#e0e0e0"
                                        text emo_name size 24 color text_color_value
                                        if selected_emotion == emo_id:
                                            text "✓" size 24 color "#4caf50"
                
                # Правая колонка - информация и кнопки
                vbox:
                    xsize 380
                    spacing 25
                    yalign 0.5
                    
                    # Информация о выбранной эмоции
                    if selected_emotion:
                        $ sel_data = plutchik_emotions.get(selected_emotion, {})
                        $ sel_name = sel_data.get('name_ru', '')
                        $ sel_icon = sel_data.get('icon', '❓')
                        $ sel_color = sel_data.get('color', '#ffffff')
                        $ sel_desc = sel_data.get('description', '')
                        $ opposite_id = sel_data.get('opposite', '')
                        $ opposite_name = plutchik_emotions.get(opposite_id, {}).get('name_ru', 'неизвестно')
                        
                        frame:
                            background Frame("gui/confirm_frame_1.png", 15, 15)
                            padding (20, 15)
                            xfill True
                            vbox:
                                spacing 12
                                text "Твой выбор:" size 20 color "#aaaaaa" xalign 0.5
                                text "[sel_icon] [sel_name]" size 36 color sel_color xalign 0.5 bold True
                                text "[sel_desc]" size 16 color "#cccccc" xalign 0.5 text_align 0.5
                                
                                null height 5
                                text "Противоположная эмоция:" size 16 color "#aaaaaa" xalign 0.5
                                text "[opposite_name]" size 20 color "#888888" xalign 0.5
                        
                        # Проверка правильности (в зависимости от сценария)
                        if selected_emotion == best_id:
                            text "✅ Точное попадание!" size 24 color "#4caf50" xalign 0.5 bold True
                        elif selected_emotion in possible:
                            text "🟡 Хороший вариант!" size 24 color "#ff9800" xalign 0.5 bold True
                        else:
                            text "❓ Возможно, стоит присмотреться к другим эмоциям" size 22 color "#ff5722" xalign 0.5
                    
                    # Кнопка подсказки
                    if show_hint:
                        frame:
                            background Frame("gui/frame.png", 10, 10)
                            padding (15, 12)
                            xfill True
                            text "[hint_text]" size 18 color "#aaaaaa" text_align 0.0
                        
                        textbutton "🙈 Скрыть подсказку":
                            xalign 0.5
                            action SetScreenVariable("show_hint", False)
                    else:
                        textbutton "📖 Показать подсказку":
                            xalign 0.5
                            action SetScreenVariable("show_hint", True)
                            hovered SetScreenVariable("hint_text", "Обрати внимание на свои телесные ощущения:\n• Как бьётся сердце?\n• Какое дыхание?\n• Что чувствуешь в теле?")
                    
                    null height 30
                    
                    hbox:
                        spacing 25
                        xalign 0.5
                        
                        if selected_emotion:
                            textbutton "✅ Подтвердить выбор":
                                background Frame("gui/button/choice_idle_background.png", 15, 15)
                                hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                                padding (15, 12)
                                xsize 220
                                action Return(selected_emotion)
                        else:
                            textbutton "✅ Подтвердить выбор":
                                background Frame("gui/button/choice_idle_background.png", 15, 15)
                                hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                                padding (15, 12)
                                xsize 220
                                action Return(None)
                                sensitive False
                        
                        textbutton "❌ Пропустить":
                            background Frame("gui/button/choice_idle_background.png", 15, 15)
                            hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                            padding (15, 12)
                            xsize 180
                            action Return("skip")
    
    # Клавиши управления
    key "K_ESCAPE" action Return("skip")
    key "game_menu" action Return("skip")
    key "K_RETURN" action Return(selected_emotion if selected_emotion else "skip")

################################################################################
## ФУНКЦИЯ ЗАПУСКА МИНИ-ИГРЫ
################################################################################

label emotion_wheel_game(scenario_id="morning_school"):
    """Вызов мини-игры Колесо эмоций Плутчика"""
    
    python:
        # Получаем сценарий
        scenario = emotion_scenarios.get(scenario_id, emotion_scenarios["morning_school"])
        
        # Показываем ситуацию (если не в режиме тишины)
        if not renpy.is_skipping():
            renpy.say(None, "📖 " + scenario.get('title', 'Эмоциональная ситуация'))
            renpy.say(None, scenario.get('situation', ''))
    
    # Запускаем экран выбора эмоции
    call screen plutchik_wheel(scenario, scenario_id)
    
    $ result = _return
    
    if result == "skip":
        $ update_player_state(self_awareness_change=2, vocabulary_change=1)
        $ save_emotion_stats(persistent.user_id, False, "skip")
        narrator "Ты решила пока не анализировать свои чувства. Это тоже нормально — иногда нужно просто побыть в тишине."
        return
    
    $ selected = result
    $ best = scenario.get('best_emotion', 'joy')
    $ possible = scenario.get('possible_emotions', [])
    $ selected_name = plutchik_emotions.get(selected, {}).get('name_ru', selected)
    
    # Получаем feedback в зависимости от правильности
    $ feedback_dict = scenario.get('feedback', {})
    
    # Проверка правильности
    if selected == best:
        $ is_correct = True
        $ feedback_text = feedback_dict.get('correct', "Ты верно определила эмоцию!")
        narrator "[feedback_text]"
        $ update_player_state(self_awareness_change=12, empathy_change=5, vocabulary_change=8, anxiety_change=-5)
    elif selected in possible:
        $ is_correct = True
        $ feedback_text = feedback_dict.get('partial', "Хороший вариант! Ты на верном пути.")
        narrator "[feedback_text]"
        $ update_player_state(self_awareness_change=8, empathy_change=3, vocabulary_change=5, anxiety_change=-3)
    else:
        $ is_correct = False
        $ feedback_text = feedback_dict.get('wrong', "Попробуй ещё раз. Прислушайся к своим ощущениям.")
        narrator "[feedback_text]"
        $ update_player_state(self_awareness_change=5, vocabulary_change=3, anxiety_change=2)
    
    # Сохраняем статистику
    $ save_emotion_stats(persistent.user_id, is_correct, selected)
    
    # Бонусная информация об эмоции
    $ emo = plutchik_emotions.get(selected, {})
    $ opposite = plutchik_emotions.get(emo.get('opposite', ''), {}).get('name_ru', 'неизвестно')
    narrator "💡 Знаешь ли ты? Эмоция «[selected_name]» противоположна эмоции «[opposite]». Понимание этого помогает лучше осознавать свои чувства."
    
    # Отмечаем прогресс в достижениях
    if persistent.user_id:
        $ stats = get_emotion_stats(persistent.user_id)
        if stats.get('total_attempts', 0) >= 1:
            $ unlock_achievement("emotion_beginner")
        if stats.get('correct_matches', 0) >= 3:
            $ unlock_achievement("emotion_treasure_hunter")
    
    return