# =============================================================================
# MINI-GAME: Эмоциональный детектив
# =============================================================================

default emotion_detective_unlocked = False
default emotion_detective_completed = False
default detective_score = 0
default detective_hints_used = 0

define emotion_database = {
    "joy": {"name": "Радость", "color": "#FFD700", "icon": "😊", "body_clues": ["улыбка", "лёгкость в теле", "блестящие глаза"]},
    "sadness": {"name": "Грусть", "color": "#6495ED", "icon": "😔", "body_clues": ["опущенные плечи", "тихий голос", "слёзы"]},
    "anger": {"name": "Гнев", "color": "#DC143C", "icon": "😠", "body_clues": ["сжатые кулаки", "напряжённые челюсти", "громкий голос"]},
    "fear": {"name": "Страх", "color": "#9370DB", "icon": "😨", "body_clues": ["дрожь", "учащённое дыхание", "холодные ладони"]},
    "surprise": {"name": "Удивление", "color": "#32CD32", "icon": "😲", "body_clues": ["широко открытые глаза", "приподнятые брови", "задержка дыхания"]},
    "disgust": {"name": "Отвращение", "color": "#8B4513", "icon": "🤢", "body_clues": ["морщинка на носу", "отстранение", "скрещённые руки"]},
    "shame": {"name": "Стыд", "color": "#B22222", "icon": "😳", "body_clues": ["опущенный взгляд", "покраснение", "желание спрятаться"]},
    "anxiety": {"name": "Тревога", "color": "#708090", "icon": "😰", "body_clues": ["ёкание в груди", "беспокойные движения", "ком в горле"]},
}

# --- СКРИН: Колесо эмоций ---
screen emotion_wheel_selector(correct_answer, on_confirm):
    modal True
    tag menu
    
    frame:
        background Solid("#1a1a2e")
        xfill True yfill True
        
    frame:
        style "empty_frame"
        xalign 0.5 yalign 0.5
        xsize 800 ysize 600
        background Frame("gui/confirm_frame.png", tile=False)
        
        vbox:
            spacing 15
            xalign 0.5 yalign 0.5
            
            text "Какую эмоцию ты замечаешь?" style "game_title"
            text "Нажми на карточку, которая кажется наиболее точной" style "subtitle" color "#aaa"
            
            default hovered_emotion = None
            
            grid 4 2:
                xalign 0.5
                spacing 10
                for key, data in emotion_database.items():
                    textbutton "[data.icon] [data.name]":
                        action on_confirm(key)
                        style "emotion_button"
                        hovered SetScreenVariable("hovered_emotion", key)
                        text_color data.color
                        text_hover_color "#ffffff"
                        text_size 16
                        text_bold True
            
            if hovered_emotion:
                $ hint_data = emotion_database[hovered_emotion]
                frame:
                    style "hint_frame"
                    xalign 0.5
                    vbox:
                        text "[hint_data.icon] [hint_data.name]" style "hint_title" color hint_data.color
                        text "Возможные признаки:" style "hint_label"
                        for clue in hint_data.body_clues:
                            text "• [clue]" style "hint_text"
            
            if config.developer or persistent.allow_skip_minigames:
                textbutton "⤷ Пропустить (сюжет продолжится)":
                    action Return("skipped")
                    style "skip_button"
                    xalign 0.5

# --- СКРИН: Подсказки по телесным маркерам ---
screen body_clues_selector(available_clues, on_select):
    modal True
    tag menu
    
    frame:
        background Solid("#1a1a2ecc")
        xfill True yfill True
        
    frame:
        style "empty_frame"
        xalign 0.5 yalign 0.5
        xsize 700 ysize 500
        background Frame("gui/confirm_frame.png", tile=False)
        
        vbox:
            spacing 20
            xalign 0.5 yalign 0.5
            
            text "Что ты замечаешь в её поведении?" style "game_title"
            text "Выбери 1-2 наиболее ярких признака" style "subtitle" color "#aaa"
            
            viewport:
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 8
                    for clue_id, clue_text in available_clues.items():
                        textbutton "□ [clue_text]":
                            action on_select(clue_id)
                            style "clue_button"
                            text_color "#e0e0ff"
                            text_size 18
                            text_xalign 0.0
            
            textbutton "✓ Готово":
                action Return()
                style "confirm_button"
                xalign 0.5

# --- ОСНОВНАЯ ЛОГИКА ---
label emotion_detective_minigame:
    if not emotion_detective_unlocked:
        $ emotion_detective_unlocked = True
    
    $ current_scenario = {
        "id": "library_conflict",
        "bg": "bg library evening",
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
    
    scene expression current_scenario.bg with fade
    show katya nervous at center with dissolve
    pause 1.0
    
    play music "music/reflective_ambient.ogg" fadein 2.0
    narrator "[current_scenario.situation]"
    
    $ selected_clues = []
    call screen body_clues_selector(
        available_clues=current_scenario.available_clues,
        on_select=SelectedField("selected_clues", toggle=True)
    )
    
    $ good_clues = ["clue1", "clue2", "clue4", "clue5"]
    $ clue_quality = len([c for c in selected_clues if c in good_clues])
    
    $ selected_emotion = None
    $ hovered_emotion = None
    
    call screen emotion_wheel_selector(
        correct_answer=current_scenario.correct_emotion,
        on_confirm=SetScreenVariable("selected_emotion")
    )
    
    if selected_emotion == "skipped":
        narrator "Ты решаешь пока не анализировать — и это тоже нормально. Иногда нужно просто дать себе время."
        $ detective_score += 1
        $ emotion_detective_completed = True
        return
    elif selected_emotion == current_scenario.correct_emotion:
        play sound "audio/ui_success.ogg"
        $ detective_score += 10
        $ emotional_vocabulary += 3
        $ empathy += 2
        $ self_awareness += 2
        
        show katya thoughtful at center with dissolve
        narrator "[current_scenario.feedback.correct]"
        
        if clue_quality >= 2:
            narrator "Ты стала замечать больше нюансов. Это помогает понимать людей глубже."
            $ empathy += 1
    elif selected_emotion in ["anger", "disgust"] and current_scenario.correct_emotion == "anxiety":
        play sound "audio/ui_neutral.ogg"
        $ detective_score += 5
        $ emotional_vocabulary += 1
        
        narrator "[current_scenario.feedback.partial]"
        narrator "Попробуй в следующий раз спросить себя: 'А что может быть ПОД этой реакцией?'"
    else:
        play sound "audio/ui_soft_fail.ogg"
        $ anxiety += 1
        
        narrator "[current_scenario.feedback.wrong]"
        narrator "Не переживай: распознавание эмоций — это навык. Он растёт с практикой."
    
    $ emotion_detective_completed = True
    $ persistent.achievements = persistent.achievements or []
    if "detective_first_step" not in persistent.achievements:
        $ persistent.achievements.append("detective_first_step")
        narrator "🏆 Достигнуто: 'Первый шаг к пониманию'"
    
    stop music fadeout 3.0
    return

# --- СТИЛИ ---
style emotion_button is button:
    xsize 180 ysize 70
    background Frame("gui/button_bg.png", tile=False)
    hover_background Frame("gui/button_hover.png", tile=False)
    padding (10, 5, 10, 5)

style clue_button is button:
    xsize 600
    background None
    hover_background Solid("#2a2a4a")
    padding (15, 10, 15, 10)

style hint_frame is frame:
    background Frame("gui/hint_box.png", tile=False)
    xsize 500
    padding (20, 15, 20, 15)

style hint_title is text:
    size 22
    bold True
    outlines [(2, "#00000080", 0, 0)]

style hint_label is text:
    size 16
    color "#aaa"
    yoffset 5

style hint_text is text:
    size 15
    color "#d0d0ff"
    yoffset 2