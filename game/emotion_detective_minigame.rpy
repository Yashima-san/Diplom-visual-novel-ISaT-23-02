# =============================================================================
# MINI-GAME: Эмоциональный детектив
# =============================================================================

default emotion_detective_unlocked = False
default emotion_detective_completed = False
default detective_score = 0
default detective_hints_used = 0

init python:
    emotion_database = {
        "joy": {"name": "Радость", "color": "#FFD700", "icon": "😊", "body_clues": ["улыбка", "лёгкость в теле", "блестящие глаза"]},
        "sadness": {"name": "Грусть", "color": "#6495ED", "icon": "😔", "body_clues": ["опущенные плечи", "тихий голос", "слёзы"]},
        "anger": {"name": "Гнев", "color": "#DC143C", "icon": "😠", "body_clues": ["сжатые кулаки", "напряжённые челюсти", "громкий голос"]},
        "fear": {"name": "Страх", "color": "#9370DB", "icon": "😨", "body_clues": ["дрожь", "учащённое дыхание", "холодные ладони"]},
        "surprise": {"name": "Удивление", "color": "#32CD32", "icon": "😲", "body_clues": ["широко открытые глаза", "приподнятые брови", "задержка дыхания"]},
        "disgust": {"name": "Отвращение", "color": "#8B4513", "icon": "🤢", "body_clues": ["морщинка на носу", "отстранение", "скрещённые руки"]},
        "shame": {"name": "Стыд", "color": "#B22222", "icon": "😳", "body_clues": ["опущенный взгляд", "покраснение", "желание спрятаться"]},
        "anxiety": {"name": "Тревога", "color": "#708090", "icon": "😰", "body_clues": ["ёкание в груди", "беспокойные движения", "ком в горле"]},
    }
    
    # Расширенная база сценариев для детектива
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
                "clue5": "Плечи напряжены, как будто готова отстраниться"
            },
            "feedback": {
                "correct": "Ты заметила: за резкостью часто скрывается тревога. Возможно, Катя боится, что её осудят.",
                "partial": "Ты на верном пути! Попробуй обратить внимание не только на действия, но и на мелкие детали — дрожь в руках, дыхание...",
                "wrong": "Это возможно, но давай присмотримся ещё: что говорит её тело? Иногда гнев — это лишь крышка для более уязвимых чувств."
            }
        },
        "help_katya": {
            "bg": "bg library",
            "character": "katia",
            "situation": "Катя сидит, опустив плечи. Голос дрожит, хотя она пытается говорить спокойно. Пальцы нервно теребят край книги. Она избегает смотреть в глаза. Её щёки слегка покраснели.",
            "correct_emotion": "shame",
            "available_clues": {
                "clue1": "Опущенные плечи и сгорбленная спина",
                "clue2": "Избегает зрительного контакта",
                "clue3": "Голос дрожит, но звучит тихо",
                "clue4": "Пальцы нервно теребят край книги",
                "clue5": "Щёки слегка покраснели",
                "clue6": "Короткие, нервные фразы",
                "clue7": "Желание 'сжаться', стать меньше"
            },
            "feedback": {
                "correct": "Ты права: за внешним гневом и раздражением часто скрывается стыд или страх. Катя стыдится своей реакции и того, что не справляется с ожиданиями родителей.",
                "partial": "Ты очень близка! Обрати внимание на то, как Катя пытается 'сжаться' — это может говорить о желании спрятаться. Какая эмоция заставляет нас хотеть стать невидимкой?",
                "wrong": "Возможно, это не совсем то. Подумай, что чувствует человек, который накричал на друга, а потом осознал это? Скорее всего, ему становится..."
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
                "clue4": "Нога слегка отбивает ритм",
                "clue5": "Периодически кусает губу"
            },
            "feedback": {
                "correct": "Ты верно заметила признаки тревоги! Даже когда человек улыбается, тело может выдавать истинные чувства.",
                "partial": "Хорошее наблюдение! Обрати внимание на микродвижения — что говорит тело, пока лицо улыбается?",
                "wrong": "Попробуй присмотреться к языку тела, а не только к выражению лица."
            }
        }
    }

screen emotion_wheel_detective(correct_answer, on_confirm):
    modal True
    zorder 200
    add "gui/overlay/confirm.png"
    
    default hovered_emotion = None
    
    frame:
        background Frame("gui/confirm_frame.png", 25, 25)
        padding (40, 40)
        xysize (1200, 800)
        xalign 0.5
        yalign 0.5
        
        vbox:
            spacing 20
            xalign 0.5
            yalign 0.5
            
            text "Какую эмоцию ты замечаешь?":
                size 36
                color gui.accent_color
                xalign 0.5
                outlines [(2, "#1a1a1a", 0, 0)]
            text "Нажми на карточку, которая кажется наиболее точной":
                size 24
                xalign 0.5
            
            null height 20
            
            grid 4 2:
                xalign 0.5
                spacing 15
                for key, data in emotion_database.items():
                    button:
                        xsize 220
                        ysize 70
                        action on_confirm(key)
                        background Frame("gui/button/choice_idle_background.png", 15, 15)
                        hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                        hovered SetScreenVariable("hovered_emotion", key)
                        
                        text "[data['icon']] [data['name']]":
                            size 18
                            color data["color"]
                            # Убираем bold
                            xalign 0.5
                            yalign 0.5
            
            if hovered_emotion:
                $ hint_data = emotion_database.get(hovered_emotion, {})
                frame:
                    background Frame("gui/frame.png", 10, 10)
                    padding (20, 15)
                    xfill True
                    vbox:
                        text "[hint_data.get('icon', '')] [hint_data.get('name', '')]":
                            size 22
                            color hint_data.get("color", "#ffffff")
                            xalign 0.5
                        text "Возможные признаки:":
                            size 18
                            xalign 0.5
                        for clue in hint_data.get("body_clues", []):
                            text "• [clue]":
                                size 16
                                xalign 0.5
            
            hbox:
                spacing 20
                xalign 0.5
                textbutton "Пропустить (сюжет продолжится)":
                    action Return("skipped")
                    background Frame("gui/button/choice_idle_background.png", 15, 15)
                    hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                    padding (15, 10)
    
    key "K_ESCAPE" action Return("skipped")

screen body_clues_selector(available_clues, on_select):
    modal True
    zorder 200
    add "gui/overlay/confirm.png"
    
    default selected_clues_list = []
    
    frame:
        background Frame("gui/confirm_frame.png", 25, 25)
        padding (40, 40)
        xysize (800, 700)
        xalign 0.5
        yalign 0.5
        
        vbox:
            spacing 25
            xalign 0.5
            yalign 0.5
            
            text "Что ты замечаешь в её поведении?":
                size 32
                color gui.accent_color
                xalign 0.5
                bold True
            text "Выбери 1-2 наиболее ярких признака":
                size 24
                xalign 0.5
            
            viewport:
                mousewheel True
                scrollbars "vertical"
                ysize 350
                vbox:
                    spacing 12
                    for clue_id, clue_text in available_clues.items():
                        $ is_selected = clue_id in selected_clues_list
                        button:
                            xfill True
                            action Function(on_select, clue_id)
                            background (Solid("#6f573f") if is_selected else Solid("#544635"))
                            hover_background Solid("#3f2626")
                            padding (15, 10)
                            
                            hbox:
                                spacing 10
                                if is_selected:
                                    text "☑":
                                        size 20
                                        color "#4caf50"
                                else:
                                    text "☐":
                                        size 20
                                        color "#a0a0ff"
                                text "[clue_text]":
                                    size 18
                                    color "#e0e0ff"
                                    xalign 0.0
            
            textbutton "Готово":
                xalign 0.5
                action Return(selected_clues_list)
                background Frame("gui/button/choice_idle_background.png", 15, 15)
                hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                padding (20, 12)
                xsize 200
    
    key "K_ESCAPE" action Return([])

# =============================================================================
# ОСНОВНАЯ МИНИ-ИГРА
# =============================================================================
label emotion_detective_minigame(scenario_id="library_conflict"):
    if not emotion_detective_unlocked:
        $ emotion_detective_unlocked = True
    
    # Получаем сценарий из базы
    python:
        if scenario_id in detective_scenarios:
            current_scenario = detective_scenarios[scenario_id]
        else:
            current_scenario = detective_scenarios["library_conflict"]
    
    scene expression current_scenario["bg"] with fade
    
    # Показываем персонажа в зависимости от сценария
    if current_scenario["character"] == "Катя":
        show katia sad at character_scale_center with dissolve
    elif current_scenario["character"] == "Лина":
        show lina neutral at character_scale_center with dissolve
    else:
        show katia sad at character_scale_center with dissolve
    
    pause 1.0
    
    "[current_scenario['situation']]"
    
    python:
        def toggle_clue(clue_id):
            if clue_id in selected_clues:
                selected_clues.remove(clue_id)
            else:
                selected_clues.append(clue_id)
    
    $ selected_clues = []
    call screen body_clues_selector(current_scenario["available_clues"], toggle_clue)
    $ selected_clues = _return
    
    # Определяем хорошие подсказки для текущего сценария
    $ good_clues = list(current_scenario["available_clues"].keys())
    $ clue_quality = len([c for c in selected_clues if c in good_clues])
    
    call screen emotion_wheel_detective(current_scenario["correct_emotion"], Return)
    $ selected_emotion = _return
    
    if selected_emotion == "skipped":
        narrator "Ты решаешь пока не анализировать — и это тоже нормально. Иногда нужно просто дать себе время."
        $ detective_score += 1
        $ emotion_detective_completed = True
        return
    elif selected_emotion == current_scenario["correct_emotion"]:
        $ detective_score += 10
        $ update_player_state(self_awareness_change=5, empathy_change=5, vocabulary_change=5, anxiety_change=-3)
        
        if current_scenario["character"] == "Катя":
            show katia neutral at character_scale_center with dissolve
        else:
            show lina smile at character_scale_center with dissolve
        
        narrator "[current_scenario['feedback']['correct']]"
        
        if clue_quality >= 3:
            narrator "Ты заметила несколько важных сигналов. Твоя внимательность к деталям помогает лучше понимать людей."
            $ update_player_state(empathy_change=3)
            
        # Достижения для разных сценариев
        if scenario_id == "help_katya" and not is_achievement_unlocked("empathetic_listener"):
            $ unlock_achievement("empathetic_listener")
            narrator "★ Достижение разблокировано: Чуткий слушатель"
        elif scenario_id == "library_conflict" and not is_achievement_unlocked("emotion_treasure_hunter"):
            $ unlock_achievement("emotion_treasure_hunter")
            
    elif selected_emotion in ["anger", "disgust", "sadness"] and current_scenario["correct_emotion"] in ["anxiety", "shame"]:
        $ detective_score += 5
        narrator "[current_scenario['feedback']['partial']]"
        $ update_player_state(self_awareness_change=3, vocabulary_change=3)
    else:
        $ detective_score += 2
        narrator "[current_scenario['feedback']['wrong']]"
        narrator "Не переживай: распознавание эмоций — это навык. Он растёт с практикой. Важно, что ты пытаешься."
        $ update_player_state(anxiety_change=2, vocabulary_change=2)
    
    $ emotion_detective_completed = True
    
    if not is_achievement_unlocked("detective_first_step"):
        $ unlock_achievement("detective_first_step")
        narrator "Достигнуто: Первый шаг к пониманию!"
    
    return