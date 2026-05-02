# =============================================================================
# MINI-GAME: Дневник наблюдений «Ситуация → Реакция»
# =============================================================================

default emotion_diary_unlocked = False
default emotion_diary_entries = []
default diary_streak = 0

define diary_scenarios = {
    "meeting_lina": {
        "title": "Разговор с Линой у входа в школу",
        "bg": "bg school entrance morning",
        "narration": "Лина подошла с улыбкой, спросила, как дела. Ты ответила кратко, но она не ушла — осталась рядом, молча.",
        "body_sensations": {
            "heart_fast": "Сердце бьётся чуть чаще",
            "throat_tight": "Ком в горле",
            "shoulders_tense": "Плечи напряжены",
            "hands_cold": "Ладони прохладные",
            "breath_shallow": "Дыхание поверхностное",
            "warm_chest": "Тепло в груди, когда она рядом"
        },
        "emotion_options": ["anxiety", "joy", "sadness", "relief", "shame", "gratitude"],
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
                "narration": "Ты заговорила о расписании. Лина поддержала, но диалог стал более формальным. Возможно, в следующий раз будет сложнее начать разговор."
            }
        },
        "correct_emotion_hint": "gratitude",
        "reflection_prompt": "Что стало легче, когда ты назвала это чувство?"
    },
    "laughing_alone": {
        "title": "Все смеялись, а ты — нет",
        "bg": "bg classroom afternoon",
        "narration": "В классе кто-то рассказал шутку. Все засмеялись. Ты тоже улыбнулась уголками губ, но внутри — пустота.",
        "body_sensations": {
            "chest_hollow": "Ощущение пустоты в груди",
            "face_smile_auto": "Улыбка 'по привычке'",
            "detached": "Чувство, будто наблюдаешь со стороны",
            "tired": "Внезапная усталость",
            "throat_lump": "Лёгкий ком в горле"
        },
        "emotion_options": ["sadness", "anxiety", "shame", "loneliness", "numbness", "relief"],
        "reactions": {
            "acknowledge": {
                "text": "Мысленно признать: 'Сейчас мне одиноко — и это окей'",
                "outcome": "self_compassion",
                "effects": {"self_awareness": 10, "anxiety": -3, "empathy": 2},
                "narration": "Ты не стала ругать себя за 'неправильную' реакцию. Просто отметила: 'Да, сейчас так'. И от этого стало чуть легче дышать."
            },
            "force_laugh": {
                "text": "Посмеяться громче, чтобы 'вписаться'",
                "outcome": "masking",
                "effects": {"anxiety": 4, "self_awareness": -2},
                "narration": "Ты добавила смеха, но внутри — ещё больше отстранения. Как будто между тобой и миром стало тоньше стекло."
            },
            "excuse_leave": {
                "text": "Извиниться и выйти на минуту",
                "outcome": "self_care",
                "effects": {"self_awareness": 6, "anxiety": -1, "trust": 1},
                "narration": "Ты вышла в коридор, сделала три глубоких вдоха. Вернулась, когда стало чуть проще. Никто не спросил — и это тоже было нормально."
            }
        },
        "correct_emotion_hint": "numbness",
        "reflection_prompt": "Что помогло бы тебе в такой момент? (можно записать в дневник)"
    }
}

init python:
    def get_stat_color(val):
        if val > 0: return "#c0ffc0"
        elif val < 0: return "#ffc0c0"
        else: return "#e0e0ff"

# --- СКРИН: Выбор телесных ощущений ---
screen body_sensations_picker(sensations_dict, on_toggle):
    modal True
    tag menu
    
    frame:
        background Solid("#0f0f1ecc")
        xfill True yfill True
        
    frame:
        style "empty_frame"
        xalign 0.5 yalign 0.5
        xsize 750 ysize 550
        background Frame("gui/diary_frame.png", tile=False)
        
        default selected_sensations = []
        
        vbox:
            spacing 18
            xalign 0.5 yalign 0.5
            
            text "📝 Что ты замечаешь в теле?" style "game_title"
            text "Отметь всё, что откликается — даже если кажется 'мелочью'" style "subtitle" color "#aaa"
            
            viewport:
                mousewheel True
                scrollbars "vertical"
                xsize 650 ysize 300
                vbox:
                    spacing 6
                    for sid, stext in sensations_dict.items():
                        $ symbol = "☑" if sid in selected_sensations else "☐"
                        hbox:
                            spacing 10
                            textbutton "[symbol]":
                                action on_toggle(sid)
                                style "checkbox_btn"
                                text_color "#a0a0ff"
                                text_hover_color "#ffffff"
                                text_size 28
                            text "[stext]" style "sensation_text" yalign 0.5
            
            hbox:
                spacing 20
                text "Выбрано: [len(selected_sensations)]" style "counter_text"
                textbutton "✓ Далее":
                    action Return()
                    style "confirm_button"

# --- СКРИН: Выбор реакции ---
screen reaction_selector(reactions_dict, on_select):
    modal True
    tag menu
    
    frame:
        background Solid("#0f0f1ecc")
        xfill True yfill True
        
    frame:
        style "empty_frame"
        xalign 0.5 yalign 0.5
        xsize 800 ysize 600
        background Frame("gui/diary_frame.png", tile=False)
        
        default hovered_reaction = None
        
        vbox:
            spacing 20
            xalign 0.5 yalign 0.5
            
            text "Как ты можешь отреагировать?" style "game_title"
            text "Нет 'правильных' ответов — есть то, что сейчас ближе тебе" style "subtitle" color "#aaa"
            
            viewport:
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 12
                    for rid, rdata in reactions_dict.items():
                        textbutton "[rdata.text]":
                            action on_select(rid)
                            style "reaction_button"
                            hovered SetScreenVariable("hovered_reaction", rid)
                            text_color "#f0f0ff"
                            text_size 17
                            text_xalign 0.0
            
            if hovered_reaction:
                $ rinfo = reactions_dict[hovered_reaction]
                frame:
                    style "outcome_preview"
                    xalign 0.5
                    text "Возможный эффект:" style "preview_label"
                    for stat, value in rinfo.effects.items():
                        $ sign = "+" if value > 0 else ""
                        text "[stat]: [sign][value]" style "preview_stat" color get_stat_color(value)
            
            textbutton "⤷ Пропустить выбор":
                action Return("skipped")
                style "skip_button"
                xalign 0.5

# --- ОСНОВНАЯ ЛОГИКА ---
label emotion_diary_minigame(scenario_id="meeting_lina"):
    if not emotion_diary_unlocked:
        $ emotion_diary_unlocked = True
    
    $ scenario = diary_scenarios.get(scenario_id)
    if not scenario:
        narrator "⚠️ Сценарий '[scenario_id]' не найден. Возвращаемся к сюжету."
        return
    
    if scenario_id in emotion_diary_entries:
        narrator "Ты уже записывала этот момент в дневник. Хочешь перечитать?"
        menu:
            "Да, показать запись":
                call show_diary_entry(scenario_id)
                return
            "Нет, вернуться":
                return
    
    scene expression scenario.bg with fade
    play music "music/diary_ambient.ogg" fadein 2.0
    narrator "[scenario.narration]"
    pause 1.0
    
    $ selected_sensations = []
    call screen body_sensations_picker(
        sensations_dict=scenario.body_sensations,
        on_toggle=SelectedField("selected_sensations", toggle=True)
    )
    
    if len(selected_sensations) >= 2:
        $ self_awareness += 1
    
    $ selected_emotion = None
    $ available_emotions = {k: emotion_database[k] for k in scenario.emotion_options if k in emotion_database}
    
    call screen emotion_wheel_selector(
        correct_answer=scenario.correct_emotion_hint,
        on_confirm=SetScreenVariable("selected_emotion")
    )
    
    if selected_emotion and selected_emotion != "skipped":
        $ emotional_vocabulary += 2
        narrator "Ты записала: '[emotion_database[selected_emotion].name]'.\nПросто назвать чувство — уже шаг к тому, чтобы им управлять."
    
    $ selected_reaction = None
    $ hovered_reaction = None
    
    call screen reaction_selector(
        reactions_dict=scenario.reactions,
        on_select=SetScreenVariable("selected_reaction")
    )
    
    if selected_reaction == "skipped" or not selected_reaction:
        narrator "Ты пока не готова выбирать реакцию — и это тоже часть процесса."
        $ diary_streak = 0
    else:
        $ reaction_data = scenario.reactions[selected_reaction]
        # Исправлено: цикл Python внутри label требует блока python:
        python:
            for stat, value in reaction_data.effects.items():
                globals()[stat] = globals().get(stat, 0) + value
        
        scene expression scenario.bg with dissolve
        narrator "[reaction_data.narration]"
        
        if reaction_data.outcome in ["healthy_boundary", "self_compassion", "self_care"]:
            $ diary_streak += 1
            play sound "audio/ui_success.ogg"
            if diary_streak >= 3:
                narrator "🏆 Достигнуто: 'Три шага подряд'"
                $ persistent.achievements.append("diary_streak_3")
        else:
            $ diary_streak = 0
            play sound "audio/ui_neutral.ogg"
    
    narrator "[scenario.reflection_prompt]"
    menu:
        "Записать в дневник (бонус к самопониманию)":
            $ self_awareness += 3
            $ emotion_diary_entries.append(scenario_id)
            narrator "Ты делаешь пометку. Возможно, позже это поможет увидеть закономерности."
        "Просто подумать":
            $ emotion_diary_entries.append(scenario_id)
            narrator "Ты обдумываешь это про себя. Иногда тишина — тоже ответ."
    
    $ persistent.diary_completed = persistent.diary_completed or []
    if scenario_id not in persistent.diary_completed:
        $ persistent.diary_completed.append(scenario_id)
    
    stop music fadeout 3.0
    return

label show_diary_entry(scenario_id):
    $ scenario = diary_scenarios[scenario_id]
    scene expression scenario.bg with fade
    play music "music/diary_ambient.ogg" fadein 1.0
    narrator "📖 Твоя запись: '[scenario.title]'"
    narrator ""
    narrator "[scenario.narration]"
    
    if scenario_id in emotion_diary_entries:
        narrator ""
        $ sens_list = [scenario.body_sensations[s] for s in selected_sensations if s in scenario.body_sensations]
        narrator "Ты отметила в теле: [', '.join(sens_list) if sens_list else '—']"
        narrator "Назвала эмоцию: [emotion_database.get(selected_emotion, {}).get('name', '—') if 'selected_emotion' in globals() else '—']"
    
    narrator ""
    narrator "Эта запись — часть твоего пути. Ты растёшь."
    pause 2.0
    stop music fadeout 2.0
    return

# --- СТИЛИ ---
style checkbox_btn is button:
    xsize 40 ysize 40
    background None

style sensation_text is text:
    size 18
    color "#e0e0ff"
    yalign 0.5

style reaction_button is button:
    xsize 700 ysize 80
    background Frame("gui/reaction_btn.png", tile=False)
    hover_background Frame("gui/reaction_btn_hover.png", tile=False)
    padding (25, 15, 25, 15)

style outcome_preview is frame:
    background Frame("gui/preview_box.png", tile=False)
    xsize 400
    padding (15, 12, 15, 12)
    yoffset 10

style preview_label is text:
    size 16
    bold True
    color "#aaa"

style preview_stat is text:
    size 15