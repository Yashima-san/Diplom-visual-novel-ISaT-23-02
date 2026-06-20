# =============================================================================
# MINI-GAME: Дневник наблюдений Ситуация - Реакция
# =============================================================================

default emotion_diary_unlocked = False
default emotion_diary_entries = []
default diary_streak = 0

init python:
    diary_scenarios = {
        "meeting_lina": {
            "title": "Разговор с Линой у входа в школу",
            "bg": "bg school_entrance",
            "characters": "lina smile",
            "character_position": "character_scale_center",
            "character_dialogue": "Как ты себя чувствуешь? Волнуешься?",
            "narration": "Что вы ощущаете?",
            "body_sensations": {
                "heart_fast": "Сердце бьётся чуть чаще",
                "throat_tight": "Ком в горле",
                "shoulders_tense": "Плечи напряжены",
                "hands_cold": "Ладони прохладные",
                "breath_shallow": "Дыхание поверхностное",
                "warm_chest": "Тепло в груди, когда она рядом"
            },
            "emotion_options": ["anxiety", "joy", "sadness", "shame", "trust"],
            "reactions": {
                "speak_up": {
                    "text": "Сказать: Мне немного неловко, но я рада тебя видеть",
                    "outcome": "healthy_boundary",
                    "effects": {"self_awareness": 8, "trust": 5, "anxiety": -2},
                    "narration": "Ты назвала своё чувство — и оно стало менее пугающим. Лина кивнула.",
                    "character_response": "Спасибо, что сказала. Я подожду, когда будет проще."
                },
                "smile_silent": {
                    "text": "Улыбнуться и промолчать",
                    "outcome": "suppression",
                    "effects": {"anxiety": 3, "empathy": -2, "self_awareness": -1},
                    "narration": "Ты улыбнулась, но внутри осталось напряжение. Лина, кажется, почувствовала это — её улыбка стала чуть осторожнее."
                },
                "change_topic": {
                    "text": "Быстро перевести тему на учёбу",
                    "outcome": "avoidance",
                    "effects": {"anxiety": 1, "trust": -3},
                    "narration": "Ты заговорила о расписании. Лина поддержала, но диалог стал более формальным."
                }
            },
            "correct_emotion_hint": "trust",
            "reflection_prompt": "Что стало легче, когда ты назвала это чувство?"
        }
    }
    
    def get_stat_color(val):
        if val > 0:
            return "#c0ffc0"
        elif val < 0:
            return "#ffc0c0"
        else:
            return "#e0e0ff"
    
    def save_body_sensation_stats(user_id, selected_sensations):
        try:
            if not hasattr(persistent, 'body_sensation_stats') or persistent.body_sensation_stats is None:
                persistent.body_sensation_stats = {}
            
            str_id = str(user_id)
            if str_id not in persistent.body_sensation_stats:
                persistent.body_sensation_stats[str_id] = {
                    'total_sessions': 0,
                    'sensations_chosen': {}
                }
            
            stats = persistent.body_sensation_stats[str_id]
            stats['total_sessions'] += 1
            
            for sensation in selected_sensations:
                if sensation not in stats['sensations_chosen']:
                    stats['sensations_chosen'][sensation] = 0
                stats['sensations_chosen'][sensation] += 1
        except:
            pass
    
    def save_reaction_stats(user_id, reaction_type):
        try:
            if not hasattr(persistent, 'reaction_stats') or persistent.reaction_stats is None:
                persistent.reaction_stats = {}
            
            str_id = str(user_id)
            if str_id not in persistent.reaction_stats:
                persistent.reaction_stats[str_id] = {
                    'total_reactions': 0,
                    'reactions': {}
                }
            
            stats = persistent.reaction_stats[str_id]
            stats['total_reactions'] += 1
            
            if reaction_type not in stats['reactions']:
                stats['reactions'][reaction_type] = 0
            stats['reactions'][reaction_type] += 1
        except:
            pass

# ============================================================================
# СКРИН: ВЫБОР ТЕЛЕСНЫХ ОЩУЩЕНИЙ
# ============================================================================
screen body_sensations_picker(sensations_dict):
    modal True
    zorder 200
    add "gui/overlay/confirm.png"
    
    default selected_sensations = []
    
    # ====== НАСТРОЙКИ ЭКРАНА ======
    python:
        # Размеры кнопок ощущений
        sensation_button_width = 650      # ← РЕГУЛИРУЙ ШИРИНУ КНОПОК ОЩУЩЕНИЙ
        sensation_button_height = 50      # ← РЕГУЛИРУЙ ВЫСОТУ КНОПОК ОЩУЩЕНИЙ
        sensation_button_text_size = 18   # ← РЕГУЛИРУЙ РАЗМЕР ШРИФТА ОЩУЩЕНИЙ
        
        # Размеры кнопки "Далее"
        next_button_width = 320           # ← РЕГУЛИРУЙ ШИРИНУ КНОПКИ "Далее"
        next_button_height = 50           # ← РЕГУЛИРУЙ ВЫСОТУ КНОПКИ "Далее"
        next_button_text_size = 20        # ← РЕГУЛИРУЙ РАЗМЕР ШРИФТА "Далее"
        
        # Размеры иконок
        checkbox_size = 24                # ← РЕГУЛИРУЙ РАЗМЕР ЧЕКБОКСОВ
        checkmark_size = 16               # ← РЕГУЛИРУЙ РАЗМЕР ГАЛОЧЕК
    
    frame:
        background Frame("gui/confirm_frame.png", 25, 25)
        padding (40, 40)
        xysize (800, 700)
        xalign 0.5
        yalign 0.5
        
        vbox:
            spacing 20
            xalign 0.5
            yalign 0.5
            
            text "Что ты замечаешь в теле?":
                size 32
                color gui.accent_color
                xalign 0.5
                outlines [(2, "#671a1a", 0, 0)]
            
            text "Отметь всё, что откликается — даже если кажется мелочью":
                size 22
                xalign 0.5
                outlines [(1, "#1a1a1a", 0, 0)]
            
            viewport:
                ysize 350
                vbox:
                    spacing 8
                    for sid, stext in sensations_dict.items():
                        $ is_selected = sid in selected_sensations
                        button:
                            xsize sensation_button_width
                            ysize sensation_button_height
                            xalign 0.5
                            action (SetScreenVariable("selected_sensations", selected_sensations + [sid]) if not is_selected else SetScreenVariable("selected_sensations", [s for s in selected_sensations if s != sid]))
                            background (Solid("#6f573f") if is_selected else Solid("#544635"))
                            hover_background Solid("#3f2626")
                            padding (15, 10)
                            
                            hbox:
                                spacing 10
                                xfill True
                                
                                if is_selected:
                                    text "☑":
                                        size checkbox_size
                                        color "#4caf50"
                                        yalign 0.5
                                else:
                                    text "☐":
                                        size checkbox_size
                                        color "#a0a0ff"
                                        yalign 0.5
                                
                                text "[stext]":
                                    size sensation_button_text_size
                                    color "#e0e0ff"
                                    yalign 0.5
                                
                                if is_selected:
                                    text "✓":
                                        size checkmark_size
                                        color "#4caf50"
                                        xalign 1.0
                                        yalign 0.5
            
            hbox:
                spacing 20
                xalign 0.5
                yalign 0.5
                
                text "Выбрано: [len(selected_sensations)]":
                    size 24
                    color "#b4744e"
                    outlines [(1, "#1a1a1a", 0, 0)]
                
                textbutton "Далее":
                    action Return(selected_sensations)
                    background Frame("gui/button/choice_idle_background.png", 15, 15)
                    hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                    padding (20, 10)
                    xsize next_button_width
                    ysize next_button_height
                    text_size next_button_text_size
    
    key "K_ESCAPE" action Return([])

# ============================================================================
# СКРИН: ВЫБОР РЕАКЦИИ
# ============================================================================

screen reaction_selector(reactions_dict):
    modal True
    zorder 200
    add "gui/overlay/confirm.png"
    
    default hovered_reaction = None
    
    # ====== НАСТРОЙКИ ЭКРАНА ======
    python:
        # Размеры кнопок реакций
        reaction_button_width = 820       # ← РЕГУЛИРУЙ ШИРИНУ КНОПОК РЕАКЦИЙ
        reaction_button_height = 80       # ← РЕГУЛИРУЙ ВЫСОТУ КНОПОК РЕАКЦИЙ
        reaction_button_text_size = 17    # ← РЕГУЛИРУЙ РАЗМЕР ШРИФТА РЕАКЦИЙ
        
        # Размеры текста эффектов
        effect_text_size = 14             # ← РЕГУЛИРУЙ РАЗМЕР ЭФФЕКТОВ
        
        # Размеры кнопки "Пропустить"
        skip_button_width = 200           # ← РЕГУЛИРУЙ ШИРИНУ КНОПКИ ПРОПУСКА
        skip_button_height = 50           # ← РЕГУЛИРУЙ ВЫСОТУ КНОПКИ ПРОПУСКА
        skip_button_text_size = 18        # ← РЕГУЛИРУЙ РАЗМЕР ШРИФТА ПРОПУСКА
    
    frame:
        background Frame("gui/confirm_frame.png", 25, 25)
        padding (40, 40)
        xysize (900, 800)
        xalign 0.5
        yalign 0.5
        
        vbox:
            spacing 20
            xalign 0.5
            yalign 0.5
            
            text "Как ты можешь отреагировать?":
                size 32
                color gui.accent_color
                xalign 0.5
                outlines [(2, "#671a1a", 0, 0)]
            
            text "Нет правильных ответов — есть то, что сейчас ближе тебе":
                size 22
                xalign 0.5
                outlines [(1, "#1a1a1a", 0, 0)]
            
            viewport:
                mousewheel True
                scrollbars "vertical"
                ysize 350
                vbox:
                    spacing 12
                    for rid, rdata in reactions_dict.items():
                        $ is_hovered = (hovered_reaction == rid)
                        button:
                            xsize reaction_button_width
                            ysize reaction_button_height
                            xalign 0.5
                            action Return(rid)
                            background (Solid("#6f573f") if is_hovered else Solid("#544635"))
                            hover_background Solid("#3f2626")
                            padding (25, 15)
                            hovered SetScreenVariable("hovered_reaction", rid)
                            unhovered SetScreenVariable("hovered_reaction", None)
                            
                            vbox:
                                spacing 5
                                text "[rdata['text']]":
                                    size reaction_button_text_size
                                    color "#f0f0ff"
                                    xalign 0.0
                                    outlines [(1, "#1a1a1a", 0, 0)]
                                
                                if is_hovered:
                                    $ rinfo = reactions_dict[rid]
                                    hbox:
                                        spacing 15
                                        for stat, value in rinfo["effects"].items():
                                            $ stat_name_ru = {
                                                "self_awareness": "Самопонимание",
                                                "empathy": "Эмпатия",
                                                "vocabulary": "Словарь",
                                                "anxiety": "Тревога",
                                                "trust": "Доверие"
                                            }.get(stat, stat)
                                            
                                            if value > 0:
                                                $ effect_text = f"{stat_name_ru}: +{value}"
                                                $ effect_color = "#c0ffc0"
                                            elif value < 0:
                                                $ effect_text = f"{stat_name_ru}: {value}"
                                                $ effect_color = "#ffc0c0"
                                            else:
                                                $ effect_text = f"{stat_name_ru}: 0"
                                                $ effect_color = "#e0e0ff"
                                            
                                            text "[effect_text]":
                                                size effect_text_size
                                                color effect_color
                                                outlines [(1, "#1a1a1a", 0, 0)]
            
            textbutton "Пропустить выбор":
                action Return("skipped")
                background Frame("gui/button/choice_idle_background.png", 15, 15)
                hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                padding (15, 10)
                xsize skip_button_width
                ysize skip_button_height
                text_size skip_button_text_size
                xalign 0.5
    
    key "K_ESCAPE" action Return("skipped")

# ============================================================================
# СКРИН: ВЫБОР ЭМОЦИИ ДЛЯ ДНЕВНИКА
# ============================================================================

screen emotion_selector_diary(emotion_options_dict):
    modal True
    zorder 200
    add "gui/overlay/confirm.png"
    
    default selected_emotion = None
    
    # ====== НАСТРОЙКИ ЭКРАНА ======
    python:
        # Размеры кнопок эмоций
        emotion_button_width = 240       # ← РЕГУЛИРУЙ ШИРИНУ КНОПОК ЭМОЦИЙ
        emotion_button_height = 80       # ← РЕГУЛИРУЙ ВЫСОТУ КНОПОК ЭМОЦИЙ
        emotion_button_text_size = 22    # ← РЕГУЛИРУЙ РАЗМЕР ШРИФТА ЭМОЦИЙ
        
        # Размеры кнопок действий
        action_button_width = 320        # ← РЕГУЛИРУЙ ШИРИНУ КНОПОК ДЕЙСТВИЙ
        action_button_height = 50        # ← РЕГУЛИРУЙ ВЫСОТУ КНОПОК ДЕЙСТВИЙ
        action_button_text_size = 20     # ← РЕГУЛИРУЙ РАЗМЕР ШРИФТА ДЕЙСТВИЙ
        
        # Отступы в сетке
        grid_spacing = 30                # ← РЕГУЛИРУЙ ОТСТУП МЕЖДУ КНОПКАМИ
    
    frame:
        background Frame("gui/confirm_frame.png", 25, 25)
        padding (40, 40)
        xysize (900, 450)
        xalign 0.5
        yalign 0.5
        
        vbox:
            spacing 15
            xalign 0.5
            yalign 0.5
            
            text "Какую эмоцию ты испытываешь?":
                size 32
                color gui.accent_color
                xalign 0.5
                outlines [(2, "#671a1a", 0, 0)]
            
            grid 3 2:
                spacing grid_spacing
                xalign 0.5
                yalign 0.5
                for key, data in emotion_options_dict.items():
                    if selected_emotion == key:
                        $ bg_color = data["color"] + "77"
                    else:
                        $ bg_color = data["color"] + "22"
                    
                    button:
                        xsize emotion_button_width
                        ysize emotion_button_height
                        action SetScreenVariable("selected_emotion", key)
                        background Solid(bg_color)
                        hover_background Solid(data["color"] + "55")
                        
                        if selected_emotion == key:
                            text "[data['icon']] [data['name']] ✓":
                                size emotion_button_text_size
                                color data["color"]
                                xalign 0.5
                                yalign 0.5
                                outlines [(1, "#1a1a1a", 0, 0)]
                        else:
                            text "[data['icon']] [data['name']]":
                                size emotion_button_text_size
                                color data["color"]
                                xalign 0.5
                                yalign 0.5
                                outlines [(1, "#1a1a1a", 0, 0)]
            
            hbox:
                spacing 50
                xalign 0.5
                
                if selected_emotion is not None:
                    textbutton "Подтвердить":
                        action Return(selected_emotion)
                        background Frame("gui/button/choice_idle_background.png", 15, 15)
                        hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                        padding (15, 10)
                        xsize action_button_width
                        ysize action_button_height
                        text_size action_button_text_size
                else:
                    textbutton "Подтвердить":
                        action Return(None)
                        sensitive False
                        background Frame("gui/button/choice_idle_background.png", 15, 15)
                        hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                        padding (15, 10)
                        xsize action_button_width
                        ysize action_button_height
                        text_size action_button_text_size
                
                textbutton "Пропустить":
                    action Return(None)
                    background Frame("gui/button/choice_idle_background.png", 15, 15)
                    hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                    padding (15, 10)
                    xsize action_button_width
                    ysize action_button_height
                    text_size action_button_text_size
    
    key "K_ESCAPE" action Return(None)

# ============================================================================
# ОСНОВНАЯ ЛОГИКА МИНИ-ИГРЫ
# ============================================================================

label emotion_diary_minigame(scenario_id="meeting_lina"):
    if not emotion_diary_unlocked:
        $ emotion_diary_unlocked = True
    
    $ scenario = diary_scenarios.get(scenario_id)
    if not scenario:
        narrator "Сценарий не найден. Возвращаемся к сюжету."
        return
    
    if scenario_id in emotion_diary_entries:
        narrator "Ты уже записывала этот момент в дневник."
        return
    
    # Показываем фон
    scene expression scenario["bg"] with fade
    
    # Показываем персонажа, если он указан
    if "characters" in scenario and scenario["characters"]:
        $ char_image = scenario["characters"]
        $ char_position = scenario.get("character_position", "character_scale_center")
        
        # Показываем персонажа с нужной трансформацией
        if char_position == "character_scale_center":
            show expression char_image at character_scale_center with dissolve
        elif char_position == "character_scale_left":
            show expression char_image at character_scale_left with dissolve
        elif char_position == "character_scale_right":
            show expression char_image at character_scale_right with dissolve
        elif char_position == "character_slide_center":
            show expression char_image at character_slide_center with dissolve
        elif char_position == "character_slide_left":
            show expression char_image at character_slide_left with dissolve
        elif char_position == "character_slide_right":
            show expression char_image at character_slide_right with dissolve
        else:
            show expression char_image at character_scale_center with dissolve
    
    # Диалог персонажа
    if "character_dialogue" in scenario and scenario["character_dialogue"]:
        e "[scenario['character_dialogue']]"
    
    # Наррация
    narrator "[scenario['narration']]"
    pause 0.5
    
    # Выбор телесных ощущений
    call screen body_sensations_picker(scenario["body_sensations"])
    $ selected_sensations = _return
    
    if selected_sensations and persistent.user_id:
        $ save_body_sensation_stats(persistent.user_id, selected_sensations)
    
    if len(selected_sensations) >= 2:
        $ update_player_state(self_awareness_change=2)
        narrator "Ты заметила несколько телесных сигналов! Это важный шаг к пониманию себя."
    
    # Выбор эмоции
    $ emotion_options_dict = {}
    python:
        for emo_id in scenario.get("emotion_options", []):
            if emo_id in plutchik_emotions:
                emotion_options_dict[emo_id] = {
                    "name": plutchik_emotions[emo_id]["name_ru"],
                    "icon": plutchik_emotions[emo_id]["icon"],
                    "color": plutchik_emotions[emo_id]["color"]
                }
    
    call screen emotion_selector_diary(emotion_options_dict)
    $ selected_emotion = _return
    
    if selected_emotion:
        $ selected_emotion_name = plutchik_emotions.get(selected_emotion, {}).get('name_ru', selected_emotion)
        narrator "Ты записала: [selected_emotion_name]. Просто назвать чувство — уже шаг к тому, чтобы им управлять."
        $ update_player_state(vocabulary_change=2)
    
    # Выбор реакции
    call screen reaction_selector(scenario["reactions"])
    $ selected_reaction = _return
    
    if selected_reaction == "skipped" or not selected_reaction:
        narrator "Ты пока не готова выбирать реакцию — и это тоже часть процесса."
        $ diary_streak = 0
    else:
        $ reaction_data = scenario["reactions"][selected_reaction]
        
        if persistent.user_id:
            $ reaction_type = reaction_data.get('outcome', 'unknown')
            $ save_reaction_stats(persistent.user_id, reaction_type)
        
        python:
            for stat, value in reaction_data["effects"].items():
                if stat == "self_awareness":
                    store.player_self_awareness = max(0, min(100, store.player_self_awareness + value))
                elif stat == "empathy":
                    store.player_empathy = max(0, min(100, store.player_empathy + value))
                elif stat == "vocabulary":
                    store.player_emotional_vocabulary = max(0, min(100, store.player_emotional_vocabulary + value))
                elif stat == "anxiety":
                    store.player_anxiety_level = max(0, min(100, store.player_anxiety_level + value))
                elif stat == "trust":
                    store.player_trust_level = max(0, min(100, store.player_trust_level + value))
        
        # Показываем результат
        scene expression scenario["bg"] with dissolve
        
        # Показываем персонажа снова
        if "characters" in scenario and scenario["characters"]:
            $ char_image = scenario["characters"]
            $ char_position = scenario.get("character_position", "character_scale_center")
            
            if char_position == "character_scale_center":
                show expression char_image at character_scale_center with dissolve
            elif char_position == "character_scale_left":
                show expression char_image at character_scale_left with dissolve
            elif char_position == "character_scale_right":
                show expression char_image at character_scale_right with dissolve
            else:
                show expression char_image at character_scale_center with dissolve
        
        narrator "[reaction_data['narration']]"
        
        # Ответ персонажа, если есть
        if "character_response" in reaction_data and reaction_data["character_response"]:
            e "[reaction_data['character_response']]"
        
        if reaction_data["outcome"] in ["healthy_boundary", "self_compassion", "self_care"]:
            $ diary_streak += 1
            if diary_streak >= 3 and not is_achievement_unlocked("diary_streak_3"):
                $ unlock_achievement("diary_streak_3")
                narrator "Достигнуто: Три шага подряд"
        else:
            $ diary_streak = 0
    
    narrator "[scenario['reflection_prompt']]"
    
    menu:
        "Записать в дневник (бонус к самопониманию)":
            $ update_player_state(self_awareness_change=3)
            $ emotion_diary_entries.append(scenario_id)
            narrator "Ты делаешь пометку. Возможно, позже это поможет увидеть закономерности."
        
        "Просто подумать":
            $ emotion_diary_entries.append(scenario_id)
            narrator "Ты обдумываешь это про себя. Иногда тишина — тоже ответ."
    
    # Скрываем персонажа
    if "characters" in scenario and scenario["characters"]:
        hide expression char_image with dissolve
    
    return