# =============================================================================
# MINI-GAME: Дневник наблюдений «Ситуация → Реакция»
# =============================================================================

default emotion_diary_unlocked = False
default emotion_diary_entries = []
default diary_streak = 0

init python:
    diary_scenarios = {
        "meeting_lina": {
            "title": "Разговор с Линой у входа в школу",
            "bg": "bg school_entrance",
            "narration": "Лина подошла с улыбкой, спросила, как дела. Ты ответила кратко, но она не ушла — осталась рядом, молча.",
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
                    "text": "Сказать: 'Мне немного неловко, но я рада тебя видеть'",
                    "outcome": "healthy_boundary",
                    "effects": {"self_awareness": 8, "trust": 5, "anxiety": -2},
                    "narration": "Ты назвала своё чувство — и оно стало менее пугающим. Лина кивнула: 'Спасибо, что сказала. Я подожду, когда будет проще.'"
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

# --- СКРИН: Выбор телесных ощущений ---
screen body_sensations_picker(sensations_dict):
    modal True
    zorder 200
    add "#000000CC"
    
    default selected_sensations = []
    
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
            
            text "📝 Что ты замечаешь в теле?" size 32 color gui.accent_color xalign 0.5 bold True
            text "Отметь всё, что откликается — даже если кажется 'мелочью'" size 22 color "#cccccc" xalign 0.5
            
            viewport:
                mousewheel True
                scrollbars "vertical"
                ysize 350
                vbox:
                    spacing 8
                    for sid, stext in sensations_dict.items():
                        $ is_selected = sid in selected_sensations
                        hbox:
                            spacing 10
                            textbutton ("☑" if is_selected else "☐"):
                                action (SetScreenVariable("selected_sensations", selected_sensations + [sid]) if not is_selected else SetScreenVariable("selected_sensations", [s for s in selected_sensations if s != sid]))
                                xsize 50
                                background None
                                text_color "#a0a0ff"
                                text_hover_color "#ffffff"
                                text_size 28
                            text "[stext]" size 18 color "#e0e0ff" yalign 0.5
            
            hbox:
                spacing 20
                text "Выбрано: [len(selected_sensations)]" size 18 color "#aaaaaa"
                textbutton "✓ Далее":
                    action Return(selected_sensations)
                    background Frame("gui/button/choice_idle_background.png", 15, 15)
                    hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                    padding (20, 10)
                    xsize 150
    
    key "K_ESCAPE" action Return([])

# --- СКРИН: Выбор реакции ---
screen reaction_selector(reactions_dict):
    modal True
    zorder 200
    add "#000000CC"
    
    default hovered_reaction = None
    
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
            
            text "Как ты можешь отреагировать?" size 32 color gui.accent_color xalign 0.5 bold True
            text "Нет 'правильных' ответов — есть то, что сейчас ближе тебе" size 22 color "#cccccc" xalign 0.5
            
            viewport:
                mousewheel True
                scrollbars "vertical"
                ysize 350
                vbox:
                    spacing 12
                    for rid, rdata in reactions_dict.items():
                        textbutton "[rdata['text']]":
                            action Return(rid)
                            xfill True
                            background Frame("gui/reaction_btn.png", 15, 15)
                            hover_background Frame("gui/reaction_btn_hover.png", 15, 15)
                            padding (25, 15)
                            text_color "#f0f0ff"
                            text_size 17
                            text_xalign 0.0
                            hovered SetScreenVariable("hovered_reaction", rid)
            
            if hovered_reaction and hovered_reaction in reactions_dict:
                $ rinfo = reactions_dict[hovered_reaction]
                frame:
                    background Frame("gui/preview_box.png", 10, 10)
                    xfill True
                    padding (15, 12)
                    vbox:
                        text "Возможный эффект:" size 16 color "#aaaaaa" bold True
                        for stat, value in rinfo["effects"].items():
                            $ sign = "+" if value > 0 else ""
                            text "[stat]: [sign][value]" size 15 color get_stat_color(value)
            
            textbutton "⤷ Пропустить выбор":
                action Return("skipped")
                background Frame("gui/button/choice_idle_background.png", 15, 15)
                hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                padding (15, 10)
                xsize 200
                xalign 0.5
    
    key "K_ESCAPE" action Return("skipped")

# --- ОСНОВНАЯ ЛОГИКА ---
label emotion_diary_minigame(scenario_id="meeting_lina"):
    if not emotion_diary_unlocked:
        $ emotion_diary_unlocked = True
    
    $ scenario = diary_scenarios.get(scenario_id)
    if not scenario:
        narrator "⚠️ Сценарий '[scenario_id]' не найден. Возвращаемся к сюжету."
        return
    
    if scenario_id in emotion_diary_entries:
        narrator "Ты уже записывала этот момент в дневник."
        return
    
    scene expression scenario["bg"] with fade
    play music "music/diary_ambient.ogg" fadein 2.0
    narrator "[scenario['narration']]"
    pause 1.0
    
    call screen body_sensations_picker(scenario["body_sensations"])
    $ selected_sensations = _return
    
    if len(selected_sensations) >= 2:
        $ update_player_state(self_awareness_change=2)
    
    # Эмоциональная мини-игра
    call emotion_wheel_game("meeting_friend")
    
    call screen reaction_selector(scenario["reactions"])
    $ selected_reaction = _return
    
    if selected_reaction == "skipped":
        narrator "Ты пока не готова выбирать реакцию — и это тоже часть процесса."
        $ diary_streak = 0
    else:
        $ reaction_data = scenario["reactions"][selected_reaction]
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
        
        scene expression scenario["bg"] with dissolve
        narrator "[reaction_data['narration']]"
        
        if reaction_data["outcome"] in ["healthy_boundary", "self_compassion", "self_care"]:
            $ diary_streak += 1
            play sound "audio/ui_success.ogg"
            if diary_streak >= 3 and not is_achievement_unlocked("diary_streak_3"):
                $ unlock_achievement("diary_streak_3")
                narrator "🏆 Достигнуто: 'Три шага подряд'"
        else:
            $ diary_streak = 0
            play sound "audio/ui_neutral.ogg"
    
    narrator "[scenario['reflection_prompt']]"
    menu:
        "Записать в дневник (бонус к самопониманию)":
            $ update_player_state(self_awareness_change=3)
            $ emotion_diary_entries.append(scenario_id)
            narrator "Ты делаешь пометку. Возможно, позже это поможет увидеть закономерности."
        "Просто подумать":
            $ emotion_diary_entries.append(scenario_id)
            narrator "Ты обдумываешь это про себя. Иногда тишина — тоже ответ."
    
    stop music fadeout 3.0
    return