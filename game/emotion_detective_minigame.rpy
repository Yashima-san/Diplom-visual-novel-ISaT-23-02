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

# --- СКРИН: Колесо эмоций для детектива ---
screen emotion_wheel_detective(correct_answer, on_confirm):
    modal True
    zorder 200
    add "#000000CC"
    
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
            
            text "Какую эмоцию ты замечаешь?" size 36 color gui.accent_color xalign 0.5 bold True
            text "Нажми на карточку, которая кажется наиболее точной" size 24 color "#cccccc" xalign 0.5
            
            null height 20
            
            grid 4 2:
                xalign 0.5
                spacing 15
                for key, data in emotion_database.items():
                    textbutton "[data.icon] [data[name]]":
                        action on_confirm(key)
                        xsize 220
                        ysize 70
                        background Frame("gui/button/choice_idle_background.png", 15, 15)
                        hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                        text_color data["color"]
                        text_hover_color "#ffffff"
                        text_size 18
                        text_bold True
                        hovered SetScreenVariable("hovered_emotion", key)
            
            if hovered_emotion:
                $ hint_data = emotion_database.get(hovered_emotion, {})
                frame:
                    background Frame("gui/frame.png", 10, 10)
                    padding (20, 15)
                    xfill True
                    vbox:
                        text "[hint_data.get('icon', '')] [hint_data.get('name', '')]" size 22 color hint_data.get("color", "#ffffff") bold True xalign 0.5
                        text "Возможные признаки:" size 18 color "#aaaaaa" xalign 0.5
                        for clue in hint_data.get("body_clues", []):
                            text "• [clue]" size 16 color "#cccccc" xalign 0.5
            
            hbox:
                spacing 20
                xalign 0.5
                textbutton "⤷ Пропустить (сюжет продолжится)":
                    action Return("skipped")
                    background Frame("gui/button/choice_idle_background.png", 15, 15)
                    hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                    padding (15, 10)
    
    key "K_ESCAPE" action Return("skipped")

# --- СКРИН: Подсказки по телесным маркерам ---
screen body_clues_selector(available_clues, on_select):
    modal True
    zorder 200
    add "#000000CC"
    
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
            
            text "Что ты замечаешь в её поведении?" size 32 color gui.accent_color xalign 0.5 bold True
            text "Выбери 1-2 наиболее ярких признака" size 24 color "#cccccc" xalign 0.5
            
            viewport:
                mousewheel True
                scrollbars "vertical"
                ysize 350
                vbox:
                    spacing 12
                    for clue_id, clue_text in available_clues.items():
                        $ is_selected = clue_id in selected_clues_list
                        textbutton ("☑ " if is_selected else "☐ ") + clue_text:
                            action Function(on_select, clue_id)
                            xfill True
                            background None
                            hover_background Solid("#2a2a4a")
                            padding (15, 10)
                            text_color "#e0e0ff"
                            text_size 18
                            text_xalign 0.0
            
            textbutton "✓ Готово":
                xalign 0.5
                action Return(selected_clues_list)
                background Frame("gui/button/choice_idle_background.png", 15, 15)
                hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                padding (20, 12)
                xsize 200
    
    key "K_ESCAPE" action Return([])

# --- ОСНОВНАЯ ЛОГИКА ---
label emotion_detective_minigame(scenario_id="library_conflict"):
    if not emotion_detective_unlocked:
        $ emotion_detective_unlocked = True
    
    $ current_scenario = {
        "id": scenario_id,
        "bg": "bg library",
        "character": "Катя",
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
            "wrong": "Это возможно, но давай присмотримся ещё: что говорит её тело? Иногда гнев — это лишь 'крышка' для более уязвимых чувств."
        }
    }
    
    scene expression current_scenario["bg"] with fade
    show katia neutral at character_scale with dissolve
    pause 1.0
    
    play music "music/reflective_ambient.ogg" fadein 2.0
    narrator "[current_scenario['situation']]"
    
    python:
        def toggle_clue(clue_id):
            if clue_id in selected_clues:
                selected_clues.remove(clue_id)
            else:
                selected_clues.append(clue_id)
    
    $ selected_clues = []
    call screen body_clues_selector(current_scenario["available_clues"], toggle_clue)
    $ selected_clues = _return
    
    $ good_clues = ["clue1", "clue2", "clue4", "clue5"]
    $ clue_quality = len([c for c in selected_clues if c in good_clues])
    
    call screen emotion_wheel_detective(current_scenario["correct_emotion"], Return)
    $ selected_emotion = _return
    
    if selected_emotion == "skipped":
        narrator "Ты решаешь пока не анализировать — и это тоже нормально. Иногда нужно просто дать себе время."
        $ detective_score += 1
        $ emotion_detective_completed = True
        return
    elif selected_emotion == current_scenario["correct_emotion"]:
        play sound "audio/ui_success.ogg"
        $ detective_score += 10
        $ update_player_state(self_awareness_change=3, empathy_change=2, vocabulary_change=3, anxiety_change=-2)
        
        show katia thoughtful at character_scale with dissolve
        narrator "[current_scenario['feedback']['correct']]"
        
        if clue_quality >= 2:
            narrator "Ты стала замечать больше нюансов. Это помогает понимать людей глубже."
            $ update_player_state(empathy_change=2)
    elif selected_emotion in ["anger", "disgust"] and current_scenario["correct_emotion"] == "anxiety":
        play sound "audio/ui_neutral.ogg"
        $ detective_score += 5
        narrator "[current_scenario['feedback']['partial']]"
        narrator "Попробуй в следующий раз спросить себя: 'А что может быть ПОД этой реакцией?'"
        $ update_player_state(self_awareness_change=2, vocabulary_change=2)
    else:
        play sound "audio/ui_soft_fail.ogg"
        narrator "[current_scenario['feedback']['wrong']]"
        narrator "Не переживай: распознавание эмоций — это навык. Он растёт с практикой."
        $ update_player_state(anxiety_change=2)
    
    $ emotion_detective_completed = True
    if not is_achievement_unlocked("detective_first_step"):
        $ unlock_achievement("detective_first_step")
        narrator "🏆 Достигнуто: 'Первый шаг к пониманию'"
    
    stop music fadeout 3.0
    return