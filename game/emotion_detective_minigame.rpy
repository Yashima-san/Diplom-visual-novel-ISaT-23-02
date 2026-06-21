# =============================================================================
# MINI-GAME: Эмоциональный детектив
# =============================================================================

default emotion_detective_unlocked = False
default emotion_detective_completed = False
default detective_score = 0
default detective_hints_used = 0

init python:
    # Цветовая схема для эмоций (как у Плутчика, но с детективной атмосферой)
    emotion_database = {
        "joy": {"name": "Радость", "color": "#FFD700", "icon": "😊", "body_clues": ["улыбка", "лёгкость в теле", "блестящие глаза"]},
        "trust": {"name": "Доверие", "color": "#90EE90", "icon": "🤝", "body_clues": ["расслабленные плечи", "прямой взгляд", "открытая поза"]},
        "fear": {"name": "Страх", "color": "#9370DB", "icon": "😨", "body_clues": ["дрожь", "учащённое дыхание", "холодные ладони"]},
        "surprise": {"name": "Удивление", "color": "#32CD32", "icon": "😲", "body_clues": ["широко открытые глаза", "приподнятые брови", "задержка дыхания"]},
        "sadness": {"name": "Грусть", "color": "#6495ED", "icon": "😔", "body_clues": ["опущенные плечи", "тихий голос", "слёзы"]},
        "disgust": {"name": "Отвращение", "color": "#8B4513", "icon": "🤢", "body_clues": ["морщинка на носу", "отстранение", "скрещённые руки"]},
        "anger": {"name": "Гнев", "color": "#DC143C", "icon": "😠", "body_clues": ["сжатые кулаки", "напряжённые челюсти", "громкий голос"]},
        "anticipation": {"name": "Предвкушение", "color": "#FFA500", "icon": "🤔", "body_clues": ["блеск в глазах", "лёгкая улыбка", "наклон вперёд"]},
        "shame": {"name": "Стыд", "color": "#B22222", "icon": "😳", "body_clues": ["опущенный взгляд", "покраснение", "желание спрятаться"]},
        "anxiety": {"name": "Тревога", "color": "#708090", "icon": "😰", "body_clues": ["ёкание в груди", "беспокойные движения", "ком в горле"]},
    }
    
    detective_scenarios = {
        "library_conflict": {
            "bg": "bg library",
            "character": "katia",
            "situation": "Катя резко захлопнула учебник, когда подошёл Алекс. Она не смотрит на него, но пальцы нервно перебирают край страницы.",
            "correct_emotion": "anxiety",
            "available_clues": {
                "clue1": "Пальцы дрожат, перебирают бумагу",
                "clue2": "Избегает зрительного контакта",
                "clue3": "Громко хлопнула книгой",
                "clue4": "Дышит чуть чаще обычного",
                "clue5": "Плечи напряжены"
            },
            "correct_clues": ["clue1", "clue2", "clue4", "clue5"],
            "feedback": {
                "correct": "Ты заметила: за резкостью часто скрывается тревога.",
                "partial": "Ты на верном пути! Обрати внимание на мелкие детали — дрожь в руках, дыхание...",
                "wrong": "Присмотримся ещё: что говорит её тело?"
            }
        },
        "help_katya": {
            "bg": "bg library",
            "character": "katia",
            "situation": "Катя сидит, опустив плечи. Голос дрожит, хотя она пытается говорить спокойно. Пальцы нервно теребят край книги. Она избегает смотреть в глаза.",
            "correct_emotion": "shame",
            "available_clues": {
                "clue1": "Опущенные плечи",
                "clue2": "Избегает зрительного контакта",
                "clue3": "Голос дрожит",
                "clue4": "Пальцы теребят книгу",
                "clue5": "Щёки покраснели",
                "clue6": "Желание 'сжаться'"
            },
            "correct_clues": ["clue1", "clue2", "clue4", "clue5", "clue6"],
            "feedback": {
                "correct": "Ты права: за внешним гневом часто скрывается стыд.",
                "partial": "Ты близка! Обрати внимание на желание 'сжаться'.",
                "wrong": "Подумай, что чувствует человек, осознавший свою ошибку?"
            }
        },
        "school_morning": {
            "bg": "bg school_entrance",
            "character": "lina",
            "situation": "Лина улыбается, но ты замечаешь, что её улыбка не совсем искренняя. Она теребит край рюкзака и часто смотрит в сторону.",
            "correct_emotion": "anxiety",
            "available_clues": {
                "clue1": "Нервно теребит рюкзак",
                "clue2": "Улыбка не доходит до глаз",
                "clue3": "Часто смотрит по сторонам",
                "clue4": "Нога отбивает ритм",
                "clue5": "Кусает губу"
            },
            "correct_clues": ["clue1", "clue2", "clue3", "clue4", "clue5"],
            "feedback": {
                "correct": "Ты верно заметила признаки тревоги!",
                "partial": "Хорошее наблюдение! Обрати внимание на микродвижения.",
                "wrong": "Присмотрись к языку тела, а не только к лицу."
            }
        }
    }

# =============================================================================
# ОСНОВНОЙ ЭКРАН МИНИ-ИГРЫ (ЕДИНЫЙ СТИЛЬ)
# =============================================================================
screen emotion_detective_game(scenario):
    modal True
    zorder 200
    add "gui/overlay/confirm.png"
    
    # Переменные состояния
    default selected_clues = []
    default max_clues = 2
    default selected_emotion = None
    default hovered_emotion = None
    default game_step = "clues"  # "clues" или "emotion"
    
    # Данные сценария
    python:
        situation = scenario.get('situation', '')
        available_clues = scenario.get('available_clues', {})
        correct_emotion = scenario.get('correct_emotion', 'joy')
        character = scenario.get('character', '')
        
        # Формируем список эмоций для отображения
        emotion_keys = list(emotion_database.keys())
        if correct_emotion not in emotion_keys:
            emotion_keys.append(correct_emotion)
    
    frame:
        background Frame("gui/confirm_frame.png", 25, 25)
        padding (30, 30)
        xysize (1200, 750)
        xalign 0.5
        yalign 0.5
        
        vbox:
            spacing 15
            xfill True
            
            # Заголовок
            text "🔍 Эмоциональный детектив" size 34 color gui.accent_color xalign 0.5 outlines [(2, "#671a1a", 0, 0)]
            
            # Ситуация
            frame:
                background Frame("gui/frame.png", 10, 10)
                padding (20, 15)
                xsize 950
                xalign 0.5
                text "[situation]":
                    size 20
                    text_align 0.0
                    xfill True
            
            null height 25
            
            # ================================================================
            # ШАГ 1: ВЫБОР ПОДСКАЗОК
            # ================================================================
            if game_step == "clues":
                vbox:
                    spacing 15
                    xfill True
                    
                    text "Выбери до 2 наиболее ярких признаков:":
                        size 24
                        color gui.accent_color
                        xalign 0.5
                        outlines [(1, "#671a1a", 0, 0)]
                    
                    # Счетчик
                    frame:
                        background Frame("gui/frame.png", 10, 10)
                        padding (10, 6)
                        xsize 400
                        xalign 0.5
                        text "Выбрано [len(selected_clues)] / [max_clues]" size 20 color "#b4744e" xalign 0.5
                    
                    # Сетка подсказок
                    grid 2 3:
                        spacing 15
                        xalign 0.5
                        for clue_id, clue_text in list(available_clues.items())[:6]:
                            $ is_selected = clue_id in selected_clues
                            $ can_select = len(selected_clues) < max_clues
                            button:
                                xsize 350
                                ysize 60
                                action (
                                    SetScreenVariable("selected_clues", selected_clues + [clue_id]) 
                                    if not is_selected and can_select 
                                    else SetScreenVariable("selected_clues", [c for c in selected_clues if c != clue_id])
                                )
                                background (Solid("#a58c74") if is_selected else Solid("#544635"))
                                hover_background Solid("#3f2626")
                                
                                hbox:
                                    spacing 10
                                    xalign 0.5
                                    yalign 0.5
                                    if is_selected:
                                        text "✓" size 20 color "#4caf50"
                                    text "[clue_text]" size 18 color "#e0e0ff" xalign 0.5
                    
                    null height 30

                    # Кнопка продолжения
                    if len(selected_clues) > 0:
                        textbutton "Продолжить":
                            xalign 0.5
                            action SetScreenVariable("game_step", "emotion")
                            background Frame("gui/button/choice_idle_background.png", 15, 15)
                            hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                            padding (30, 12)
                            xsize 320
                    else:
                        textbutton "Продолжить":
                            xalign 0.5
                            sensitive False
                            background Frame("gui/button/choice_idle_background.png", 15, 15)
                            hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                            padding (30, 12)
                            xsize 320
            
            # ================================================================
            # ШАГ 2: ВЫБОР ЭМОЦИИ
            # ================================================================
            else:
                vbox:
                    spacing 15
                    xfill True
                    
                    text "Какую эмоцию ты замечаешь?":
                        size 28
                        color gui.accent_color
                        xalign 0.5
                        outlines [(1, "#671a1a", 0, 0)]
                    
                    # Колесо эмоций (круговая раскладка 3x4)
                    grid 5 2:
                        spacing 12
                        xalign 0.5
                        for key in emotion_keys[:12]:
                            $ data = emotion_database.get(key, {})
                            $ emo_name = data.get('name', key)
                            $ emo_color = data.get('color', '#888888')
                            $ emo_icon = data.get('icon', '?')
                            $ is_selected = (selected_emotion == key)
                            
                            button:
                                xsize 180
                                ysize 70
                                action SetScreenVariable("selected_emotion", key)
                                hovered SetScreenVariable("hovered_emotion", key)
                                unhovered SetScreenVariable("hovered_emotion", None)
                                background Solid(emo_color + "44")
                                hover_background Solid(emo_color + "77")
                                if is_selected:
                                    background Solid(emo_color + "88")
                                    hover_background Solid(emo_color + "99")
                                
                                text "[emo_icon] [emo_name]" + (" ✓" if is_selected else ""):
                                    size 16
                                    color emo_color
                                    xalign 0.5
                                    yalign 0.5
                                    outlines [(1, "#1a1a1a", 0, 0)]
                    
                    # Информация о выбранной эмоции
                    if hovered_emotion or selected_emotion:
                        $ show_key = hovered_emotion or selected_emotion
                        $ show_data = emotion_database.get(show_key, {})
                        frame:
                            background Frame("gui/frame.png", 10, 10)
                            padding (15, 10)
                            xysize(1100, 50)
                            xalign 0.5
                            hbox:
                                spacing 20
                                xalign 0.5
                                text "[show_data.get('icon', '')] [show_data.get('name', '')]":
                                    size 22
                                    color show_data.get('color', '#ffffff')
                                text "• " + " • ".join(show_data.get('body_clues', [])[:2]):
                                    size 22
                    
                    null height 30
                    
                    hbox:
                        spacing 30
                        xalign 0.5
                        
                        textbutton "Назад":
                            action SetScreenVariable("game_step", "clues")
                            background Frame("gui/button/choice_idle_background.png", 15, 15)
                            hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                            padding (20, 12)
                            xsize 320
                        
                        if selected_emotion:
                            textbutton "Готово":
                                action Return({
                                    "clues": selected_clues,
                                    "emotion": selected_emotion
                                })
                                background Frame("gui/button/choice_idle_background.png", 15, 15)
                                hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                                padding (20, 12)
                                xsize 320
                        else:
                            textbutton "Готово":
                                sensitive False
                                background Frame("gui/button/choice_idle_background.png", 15, 15)
                                hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                                padding (20, 12)
                                xsize 250
            
            # Кнопка пропуска (всегда доступна)
            textbutton "Пропустить":
                xalign 0.5
                action Return({"clues": [], "emotion": "skipped"})
                background Frame("gui/button/choice_idle_background.png", 15, 15)
                hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                padding (20, 12)
                xsize 320
    
    key "K_ESCAPE" action Return({"clues": [], "emotion": "skipped"})
# =============================================================================
# ОСНОВНАЯ ЛОГИКА МИНИ-ИГРЫ
# =============================================================================
label emotion_detective_minigame(scenario_id="library_conflict"):
    if not emotion_detective_unlocked:
        $ emotion_detective_unlocked = True
    
    python:
        if scenario_id in detective_scenarios:
            current_scenario = detective_scenarios[scenario_id]
        else:
            current_scenario = detective_scenarios["library_conflict"]
    
    scene expression current_scenario["bg"] with fade
    
    if current_scenario["character"] == "katia":
        show katia sad at character_scale with dissolve
    elif current_scenario["character"] == "lina":
        show lina neutral at character_scale with dissolve
    else:
        show katia sad at character_scale with dissolve
    
    pause 0.5
    
    call screen emotion_detective_game(current_scenario)
    $ result = _return
    
    $ selected_clues = result.get("clues", [])
    $ selected_emotion = result.get("emotion", "skipped")
    
    if selected_emotion == "skipped":
        narrator "Ты решаешь пока не анализировать — и это тоже нормально."
        $ detective_score += 1
        $ emotion_detective_completed = True
        $ update_player_state(self_awareness_change=2, vocabulary_change=2)
        return
    
    # Оценка
    $ correct_clues = current_scenario.get("correct_clues", [])
    $ correct_emotion = current_scenario.get("correct_emotion", "joy")
    
    $ correct_selected = len([c for c in selected_clues if c in correct_clues])
    $ total_selected = len(selected_clues)
    $ clue_accuracy = (correct_selected / max(total_selected, 1)) * 100 if total_selected > 0 else 0
    $ emotion_correct = (selected_emotion == correct_emotion)
    
    if emotion_correct:
        $ detective_score += 10
        
        if clue_accuracy >= 80:
            $ detective_score += 5
            $ update_player_state(self_awareness_change=8, empathy_change=8, vocabulary_change=5, anxiety_change=-5)
            narrator "Ты отлично заметила ключевые сигналы! Твоя внимательность впечатляет."
        elif clue_accuracy >= 50:
            $ detective_score += 3
            $ update_player_state(self_awareness_change=5, empathy_change=5, vocabulary_change=3, anxiety_change=-3)
            narrator "Ты заметила несколько важных сигналов. Это хороший шаг к пониманию."
        else:
            $ update_player_state(self_awareness_change=3, empathy_change=3, vocabulary_change=2, anxiety_change=-2)
            narrator "Ты правильно определила эмоцию! В следующий раз попробуй заметить больше телесных сигналов."
        
        if current_scenario["character"] == "katia":
            show katia neutral at character_scale with dissolve
        else:
            show lina smile at character_scale with dissolve
        
        narrator "[current_scenario['feedback']['correct']]"
            
        if scenario_id == "help_katya" and not is_achievement_unlocked("empathetic_listener"):
            $ unlock_achievement("empathetic_listener")
            narrator "★ Достижение: Чуткий слушатель"
        elif scenario_id == "library_conflict" and not is_achievement_unlocked("emotion_treasure_hunter"):
            $ unlock_achievement("emotion_treasure_hunter")
            
    elif selected_emotion in ["anger", "disgust", "sadness"] and correct_emotion in ["anxiety", "shame"]:
        $ detective_score += 5
        
        if clue_accuracy >= 60:
            $ update_player_state(self_awareness_change=5, empathy_change=3, vocabulary_change=4, anxiety_change=-2)
            narrator "Ты хорошо заметила телесные сигналы!"
        else:
            $ update_player_state(self_awareness_change=3, vocabulary_change=3)
        
        narrator "[current_scenario['feedback']['partial']]"
    else:
        $ detective_score += 2
        $ update_player_state(anxiety_change=2, vocabulary_change=2)
        narrator "[current_scenario['feedback']['wrong']]"
        narrator "Не переживай: распознавание эмоций — это навык. Он растёт с практикой."
    
    $ emotion_detective_completed = True
    
    if not is_achievement_unlocked("detective_first_step"):
        $ unlock_achievement("detective_first_step")
        narrator "Достигнуто: Первый шаг к пониманию"
    
    return