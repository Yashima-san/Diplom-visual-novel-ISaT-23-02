# Определения персонажей и изображений
define e = Character('Лина', color="#707ef6")
define user_char = Character("[persistent.user_name]", color="#ff9e5e")
define thought_user = Character("[persistent.user_name]", what_italic=True)
define narrator = Character(None, what_italic=True)
define a = Character('Алекс', color="#6b8e23")
define t = Character('Анна Сергеевна', color="#9370db")
define k = Character('Катя', color="#fe7d90")
define lib = Character('Библиотекарь', color="#a0522d")

define persistent.user_name = ""
define persistent.user_id = None
define persistent.user_data = None

default player_self_awareness = 0
default player_empathy = 0
default player_emotional_vocabulary = 0
default player_anxiety_level = 50
default player_trust_level = 30

default current_chapter = "Глава Первая: Связь"
default first_choice = 0
default second_choice = 0
default chapter2_choice_1 = 0
default chapter2_choice_2 = 0
default chapter2_choice_final = 0
default morning_choice = 0
default emotion_game_results = []
default emotion_game_completed = False
default rhythm_game_score = 0

################################################################################
## ФУНКЦИИ ДЛЯ РАБОТЫ С СОСТОЯНИЕМ ИГРОКА И ЗАГРУЗКИ
################################################################################
init python:
    import time
    import json
    import random
    from datetime import datetime, timedelta
    
    def update_player_state(self_awareness_change=0, empathy_change=0, 
                        vocabulary_change=0, anxiety_change=0, trust_change=0):
        store.player_self_awareness = max(0, min(100, store.player_self_awareness + self_awareness_change))
        store.player_empathy = max(0, min(100, store.player_empathy + empathy_change))
        store.player_emotional_vocabulary = max(0, min(100, store.player_emotional_vocabulary + vocabulary_change))
        store.player_anxiety_level = max(0, min(100, store.player_anxiety_level + anxiety_change))
        store.player_trust_level = max(0, min(100, store.player_trust_level + trust_change))
        
        if persistent.user_id:
            if not hasattr(persistent, 'player_states') or persistent.player_states is None:
                persistent.player_states = {}
            str_id = str(persistent.user_id)
            if str_id not in persistent.player_states:
                persistent.player_states[str_id] = []
            persistent.player_states[str_id].append({
                'timestamp': time.time(),
                'self_awareness': store.player_self_awareness,
                'empathy': store.player_empathy,
                'vocabulary': store.player_emotional_vocabulary,
                'anxiety': store.player_anxiety_level,
                'trust': store.player_trust_level
            })
            if len(persistent.player_states[str_id]) > 50:
                persistent.player_states[str_id] = persistent.player_states[str_id][-50:]

    def load_latest_save():
        latest_slot = None
        latest_time = 0
        slots_to_check = [str(i) for i in range(1, 10)] + \
                         [f"auto-{i}" for i in range(1, 10)] + \
                         ["quick-save"]
        
        for slot in slots_to_check:
            if renpy.can_load(slot):
                try:
                    save_json = renpy.json_load(renpy.slot_json_filename(slot))
                    if save_json:
                        timestamp = save_json.get("_timestamp", 0)
                        if timestamp > latest_time:
                            latest_time = timestamp
                            latest_slot = slot
                except:
                    pass
                    
        if latest_slot:
            renpy.load(latest_slot)
        else:
            renpy.notify("Нет сохранённой игры")

################################################################################
## ТРАНСФОРМАЦИИ
################################################################################
transform character_scale:
    zoom 0.28
    xalign 0.5
    yalign 1.0
transform character_scale_left:
    zoom 0.28
    xalign 0.25
    yalign 1.0
transform character_scale_right:
    zoom 0.28
    xalign 0.75
    yalign 1.0
transform character_scale_center:
    zoom 0.28
    xalign 0.5
    yalign 1.0
transform character_scale_center_soft_approach:
    zoom 0.28
    xalign 0.5
    yalign 1.0
    easein 1.2 zoom 0.31
    pause 0.1
    easeout 0.28
transform character_scale_fadein:
    zoom 0.28
    alpha 0.0
    linear 0.5 alpha 1.0
    xalign 0.5
    yalign 1.0

################################################################################
## ИЗОБРАЖЕНИЯ
################################################################################
image lina neutral = ConditionSwitch("renpy.loadable('images/characters/lina_neutral.png')", "images/characters/lina_neutral.png", "True", "images/characters/lina.png")
image lina speak = ConditionSwitch("renpy.loadable('images/characters/lina_speak.png')", "images/characters/lina_speak.png", "True", "images/characters/lina.png")
image lina smile = ConditionSwitch("renpy.loadable('images/characters/lina_smile.png')", "images/characters/lina_smile.png", "True", "images/characters/lina.png")
image alex neutral = ConditionSwitch("renpy.loadable('images/characters/alex_neutral.png')", "images/characters/alex_neutral.png", "True", "images/characters/alex_neutral.png")
image alex smile = ConditionSwitch("renpy.loadable('images/characters/alex_smile.png')", "images/characters/alex_smile.png", "True", "images/characters/alex_neutral.png")
image katia neutral = ConditionSwitch("renpy.loadable('images/characters/katia_neutral.png')", "images/characters/katia_neutral.png", "True", "images/characters/katia_neutral.png")
image katia smile = ConditionSwitch("renpy.loadable('images/characters/katia_smile.png')", "images/characters/katia_smile.png", "True", "images/characters/katia_neutral.png")
image teacher neutral = ConditionSwitch("renpy.loadable('images/characters/teacher_neutral.png')", "images/characters/teacher_neutral.png", "True", "images/characters/teacher_neutral.png")
image teacher kind = ConditionSwitch("renpy.loadable('images/characters/teacher_kind.png')", "images/characters/teacher_kind.png", "True", "images/characters/teacher_neutral.png")
image librarian neutral = ConditionSwitch("renpy.loadable('images/characters/librarian_neutral.png')", "images/characters/librarian_neutral.png", "True", "images/characters/librarian_neutral.png")
image librarian kind = ConditionSwitch("renpy.loadable('images/characters/librarian_kind.png')", "images/characters/librarian_kind.png", "True", "images/characters/librarian_neutral.png")
image bg night_room = ConditionSwitch("renpy.loadable('images/night_room.png')", "images/night_room.png", "True", "#000000")
image bg room_pk = ConditionSwitch("renpy.loadable('images/room_pk.png')", "images/room_pk.png", "True", "#2a2a2a")
image bg bg_room_pk_light = ConditionSwitch("renpy.loadable('images/room_pk_light.png')", "images/room_pk_light.png", "True", "#3a3a3a")
image bg school_entrance = ConditionSwitch("renpy.loadable('images/school_entrance.png')", "images/school_entrance.png", "True", "#4a4a4a")
image bg kitchen = ConditionSwitch("renpy.loadable('images/kitchen.png')", "images/kitchen.png", "True", "#5a5a5a")
image bg street = ConditionSwitch("renpy.loadable('images/street.png')", "images/street.png", "True", "#6a6a6a")
image bg classroom = ConditionSwitch("renpy.loadable('images/classroom.png')", "images/classroom.png", "True", "#8a8a8a")
image bg music_room = ConditionSwitch("renpy.loadable('images/music_room.png')", "images/music_room.png", "True", "#9a9a9a")
image bg library = ConditionSwitch("renpy.loadable('images/library.png')", "images/library.png", "True", "#aaaaaa")
image cg room_evening = ConditionSwitch("renpy.loadable('images/cg/room_evening.png')", "images/cg/room_evening.png", "True", "#2b2b2b")

################################################################################
## ЭКРАНЫ МИНИ-ИГР (ИСПРАВЛЕННЫЕ)
################################################################################

# Игра 1: Эмоциональный компас
screen emotion_selection_extended():
    modal True
    zorder 100
    
    # Исправлено: используем frame с background вместо add с xfill
    frame:
        background Solid("#1a1a2eee")
        xfill True
        yfill True
        
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            xmaximum 600
            
            text "Мини-игра: Эмоциональный Компас" size 30 color "#ffffff" xalign 0.5
            text "Опиши свое текущее состояние. Выбери основную эмоцию:" size 20 color "#cccccc" xalign 0.5
            
            grid 2 4:
                spacing 10
                xalign 0.5
                
                $ emotions_list = [
                    ("Радость", "joy"), ("Доверие", "trust"),
                    ("Страх", "fear"), ("Удивление", "surprise"),
                    ("Печаль", "sadness"), ("Отвращение", "disgust"),
                    ("Гнев", "anger"), ("Предвкушение", "anticipation")
                ]
                
                for emo_name, emo_id in emotions_list:
                    textbutton emo_name:
                        action Return(emo_id)
                        xminimum 150
                        background "#444444"
                        hover_background "#666666"
                        
            textbutton "Пропустить" action Return(None) xalign 0.5

# Игра 2: Ритм Дружбы
screen rhythm_game_screen():
    modal True
    zorder 100
    
    # Фон
    add "bg music_room"
    
    # Интерфейс счета
    frame:
        background None
        pos (0.5, 0.1)
        anchor (0.5, 0.0)
        hbox:
            spacing 20
            text "Ритм Дружбы" size 40 color "#fff"
            text "Счет: [rhythm_game_score]" size 30 color "#ff9e5e"

    # Зона цели (Target) - исправлено использование border
    frame:
        pos (0.5, 0.8)
        anchor (0.5, 0.5)
        xsize 100
        ysize 100
        background Solid("#ffffff33")
        padding (2, 2, 2, 2) # Замена border
        
    # Инструкция и кнопка
    vbox:
        pos (0.5, 0.8)
        anchor (0.5, 0.5)
        spacing 20
        text "Нажми ПРОБЕЛ или кликни, когда круг совпадет с целью!" color "#fff" size 20 xalign 0.5
        
        textbutton "УДАР! (Пробел)" action Function(play_rhythm_hit) xalign 0.5 xminimum 200


################################################################################
## ЛОГИКА МИНИ-ИГР PYTHON
################################################################################
init python:
    rhythm_active = False
    rhythm_timer = None
    rhythm_target_time = 0
    rhythm_interval = 2.0

    def start_rhythm_game():
        store.rhythm_game_score = 0
        store.rhythm_active = True
        schedule_next_beat()
        renpy.show_screen("rhythm_game_screen")
        
    def schedule_next_beat():
        if not store.rhythm_active:
            return
        store.rhythm_target_time = time.time() + store.rhythm_interval

    def play_rhythm_hit():
        if not store.rhythm_active:
            return
        
        current_time = time.time()
        diff = abs(current_time - store.rhythm_target_time)
        
        if diff < 0.3:
            store.rhythm_game_score += 10
            renpy.notify("Отлично! +10")
        elif diff < 0.6:
            store.rhythm_game_score += 5
            renpy.notify("Неплохо! +5")
        else:
            renpy.notify("Мимо...")
            
        schedule_next_beat()

    def stop_rhythm_game():
        store.rhythm_active = False
        renpy.hide_screen("rhythm_game_screen")

################################################################################
## ФУНКЦИИ СОХРАНЕНИЯ И ПЕРЕХОДОВ
################################################################################
init python:
    def continue_to_next_chapter(old_chapter, new_chapter_title, new_chapter_subtitle):
        store.current_chapter = new_chapter_title
        if renpy.has_label("chapter_two"):
            renpy.jump("chapter_two")
        else:
            renpy.notify("Глава в разработке")
            renpy.jump("main_menu")

    def exit_to_main_menu(old_chapter):
        renpy.jump("main_menu")

    def auto_save_chapter_complete(chapter_name):
        if persistent.user_id and 'db' in globals() and hasattr(db, 'update_save_progress'):
            try:
                db.update_save_progress(persistent.user_id, chapter_name)
            except:
                pass
        try:
            unlock_achievement("chapter_one_complete")
        except:
            pass
        renpy.notify("Глава завершена! Прогресс сохранен.")

    def add_user_info_to_save(json_data):
        try:
            if hasattr(persistent, 'user_name') and persistent.user_name:
                json_data["user_name"] = persistent.user_name
            if hasattr(persistent, 'user_id') and persistent.user_id is not None:
                json_data["user_id"] = persistent.user_id
            json_data["chapter"] = get_current_chapter_safe()
            json_data["_timestamp"] = time.time()
            json_data["player_state"] = {
                "self_awareness": store.player_self_awareness,
                "empathy": store.player_empathy,
                "vocabulary": store.player_emotional_vocabulary,
                "anxiety": store.player_anxiety_level,
                "trust": store.player_trust_level
            }
        except Exception:
            json_data["chapter"] = "Глава Первая: Связь"
            json_data["_timestamp"] = time.time()
        return json_data
    
    if hasattr(config, 'save_json_callbacks'):
        config.save_json_callbacks = []
        config.save_json_callbacks.append(add_user_info_to_save)
    
    def get_current_chapter_safe():
        try:
            if hasattr(store, 'current_chapter') and store.current_chapter:
                return store.current_chapter
        except:
            pass
        return "Глава Первая: Связь"

################################################################################
## CALLBACK ФУНКЦИИ ДЛЯ ВЫБОРОВ
################################################################################
init python:
    def first_choice_callback(choice_text):
        if "Привет! Да, готова" in choice_text:
            store.first_choice = 1
            update_player_state(self_awareness_change=5, anxiety_change=-10, vocabulary_change=3)
        elif "Привет! Я тоже очень рада" in choice_text:
            store.first_choice = 2
            update_player_state(empathy_change=8, anxiety_change=-5, trust_change=5)
        elif "Привет! Я очень рада" in choice_text:
            store.first_choice = 3
            update_player_state(empathy_change=5, trust_change=10, anxiety_change=-8)
        return

    def second_choice_callback(choice_text):
        if "Звучит здорово! Я согласна" in choice_text:
            store.second_choice = 11
            update_player_state(trust_change=5, anxiety_change=-5, vocabulary_change=2)
        elif "Давай сначала посмотрим" in choice_text:
            store.second_choice = 12
            update_player_state(anxiety_change=5, trust_change=-3)
        elif "Звучит здорово! Библиотека" in choice_text:
            store.second_choice = 21
            update_player_state(self_awareness_change=5, vocabulary_change=5, anxiety_change=-3)
        elif "Спасибо, Лина" in choice_text and "буду просто наблюдать" in choice_text:
            store.second_choice = 22
            update_player_state(anxiety_change=10, trust_change=-5)
        elif "Спасибо, Лина! Ты лучшая!" in choice_text:
            store.second_choice = 31
            update_player_state(empathy_change=10, trust_change=10, anxiety_change=-10)
        elif "Спасибо, Лина! Я очень ценю твою дружбу" in choice_text:
            store.second_choice = 32
            update_player_state(empathy_change=8, trust_change=15, vocabulary_change=3)
        return

    def morning_choice_callback(choice_text):
        if "Спасибо, Лина! Я уже встаю" in choice_text:
            store.morning_choice = 1
            update_player_state(self_awareness_change=3, anxiety_change=-8, trust_change=3)
        elif "Я тоже волнуюсь" in choice_text:
            store.morning_choice = 2
            update_player_state(empathy_change=5, anxiety_change=5, trust_change=5)
        elif "Увидимся у входа" in choice_text:
            store.morning_choice = 3
            update_player_state(trust_change=5, anxiety_change=-5)
        return

################################################################################
## ГЛАВА ПЕРВАЯ: СВЯЗЬ
################################################################################
label start:
    $ current_chapter = "Глава Первая: Связь"
    $ player_self_awareness = 0
    $ player_empathy = 0
    $ player_emotional_vocabulary = 0
    $ player_anxiety_level = 50
    $ player_trust_level = 30
    
    python:
        if not hasattr(persistent, 'player_states') or persistent.player_states is None:
            persistent.player_states = {}
    
    play music config.main_menu_music fadein 5.0
    $ renpy.music.set_volume(0.1, delay=0)
    
    if renpy.has_screen("input_name_screen"):
        $ entered_name = renpy.call_screen("input_name_screen")
    else:
        $ entered_name = renpy.input("Введите ваше имя:", length=20)
    
    if entered_name is None or entered_name.strip() == "":
        $ player_name = "Настя"
    else:
        $ player_name = entered_name.strip()
    
    $ persistent.user_name = player_name
    $ user_id = None
    if 'db' in globals() and hasattr(db, 'add_user'):
        $ user_id = db.add_user(player_name)
    $ persistent.user_id = user_id
    
    "Ты ничего не забыла, [persistent.user_name]?"
    "Пора просыпаться..."
    scene black with fade
    show text "{size=80}Глава Первая{/size}\n{size=60}Связь{/size}" with dissolve
    pause 3.0
    scene black with dissolve

    if persistent.user_id and 'db' in globals() and hasattr(db, 'update_save_progress'):
        $ db.update_save_progress(persistent.user_id, "Глава Первая: Связь")
    
    $ unlock_achievement("wake_up")
    $ unlock_gallery_item("room_evening")
    scene cg room_evening at truecenter with fade
    stop music
    play music "song/Audio_soft_1.mp3" fadein 5.0
    $ renpy.music.set_volume(0.5, delay=5)

    narrator "Солнечные лучи, пробиваясь сквозь неплотно задернутые шторы, рисовали на полу комнаты девочки причудливые узоры."
    narrator "Пылинки, словно крошечные танцоры, кружились в золотистых столбах света."
    narrator "Комната, аккуратно обставленная, но лишенная ярких акцентов, отражала ее внутренний мир – упорядоченный, но безжизненный."
    thought_user "Вечер... слишком долго спала... Впрочем, как и всегда."
    thought_user "Чувства. Эмоции. Слова, которые я слышу постоянно, но для меня – лишь набор звуков, лишенных смысла."
    thought_user "Алекситимия. Это слово, которое мне сказала врач. Оно звучит так… официально. Как диагноз."
    
    show bg bg_room_pk_light with dissolve
    $ unlock_gallery_item("room_pk_light")
    narrator "На стене висел постер с изображением аниме-персонажа."
    thought_user "Я научилась имитировать. Улыбаться, когда нужно. Но внутри – тишина."
    thought_user "Единственный, кто меня понимает – это моя интернет-подруга, Лина."
    
    show bg room_pk with dissolve
    $ unlock_gallery_item("room_pk")
    thought_user "Новая школа. Новые люди. Там учится Лина. Это хорошо."
    thought_user "Но я боюсь не справиться. Боюсь снова почувствовать эту пустоту."
    
    $ enable_chat_mode()
    $ e("Привет! Ты уже готова к завтрашнему дню? Я так рада, что мы теперь будем учиться вместе! 🥳")
    narrator "Слова Лины казались одновременно утешительными и пугающими."
    
    $ show_chat_choices([
        "Привет! Да, готова. Уже жду не дождусь! 😊",
        "Привет! Я тоже очень рада! Немного волнуюсь, но уверена, что с тобой будет весело! 😊",
        "Привет! Я очень рада, что мы будем учиться вместе. Ты – мой самый лучший друг. ❤️"
    ], first_choice_callback)
    $ store.wait_for_chat()

label continue_chat_after_first:
    if first_choice == 1:
        $ e("Ура! Я так рада!")
        $ e("Я уже придумала, что мы можем пойти в кафе после уроков! Что скажешь?")
        $ show_chat_choices(["Звучит здорово! Я согласна на все!", "Давай сначала посмотрим, как пройдет день."], second_choice_callback)
        $ store.wait_for_chat()
    elif first_choice == 2:
        $ e("Ой, я понимаю! Но не переживай! Мы же вместе!")
        $ e("Я придумала, что мы можем ходить в библиотеку, там так тихо и уютно!")
        $ show_chat_choices(["Звучит здорово! Библиотека – отличная идея!", "Спасибо, Лина! Я пока буду просто наблюдать."], second_choice_callback)
        $ store.wait_for_chat()
    elif first_choice == 3:
        $ e("Ой, [persistent.user_name]! 🥺 Я так тронута!")
        $ e("Я тоже очень рада! И ты не волнуйся, я буду рядом!")
        $ show_chat_choices(["Спасибо, Лина! Ты лучшая!", "Спасибо, Лина! Я очень ценю твою дружбу."], second_choice_callback)
        $ store.wait_for_chat()
    
    $ renpy.pause(7.0)
    $ disable_chat_mode()
    jump night_scene

label night_scene:
    stop music
    scene bg night_room with fade
    play sound "song/night_ambient.mp3" fadein 3.0
    narrator "Ночь опустилась на город мягко."
    thought_user "Завтрашний день... Прыжок в неизвестность."
    thought_user "Психолог говорила, что важно анализировать свои состояния."
    narrator "[persistent.user_name] взяла в руки таблицу «Колесо эмоций»."
    
    # ЗАПУСК МИНИ-ИГРЫ 1
    call screen emotion_selection_extended
    
    if _return:
        $ selected_emotion = _return
        if selected_emotion:
            thought_user "Я выбрала: [selected_emotion]. Это помогает структурировать хаос."
            $ update_player_state(self_awareness_change=10, vocabulary_change=8, anxiety_change=-5)
            $ emotion_game_completed = True
        else:
            thought_user "Я не смогла выбрать."
            $ update_player_state(anxiety_change=5)
    
    narrator "Засыпая, [persistent.user_name] думала только об одном…"
    thought_user "Скорее бы наступило утро..."
    stop sound fadeout 3.0
    scene black with fade
    pause 1.0
    jump morning_scene

label morning_scene:
    stop music
    scene cg room_evening with fade
    play music "song/Audio_soft_1.mp3" fadein 3.0
    narrator "Утро 3 сентября."
    $ enable_chat_mode()
    $ e("Доброе утро, [persistent.user_name]! 🌅 Не забудь взять тетради и хорошее настроение 😘")
    
    $ show_chat_choices(["Спасибо, Лина! Я уже встаю. Увидимся у входа! ❤️", "Я тоже волнуюсь... Но спасибо, что ты рядом!", "Увидимся у входа в школу!"], morning_choice_callback)
    $ store.wait_for_chat()
    $ renpy.pause(7.0)
    $ disable_chat_mode()
    return

label continue_morning:
    narrator "[persistent.user_name] начала собираться."
    scene bg kitchen with fade
    narrator "На кухне была записка от родителей: \"Удачи в новой школе! Мы в тебя верим!\""
    thought_user "Как всегда, коротко и по делу."
    stop music fadeout 2.0
    narrator "Она вышла из дома."
    scene bg street with fade
    play music "song/school_ambient.mp3" fadein 2.0
    narrator "Школа виднелась вдалеке."
    scene bg school_entrance with fade
    show lina smile at character_scale_fadein
    narrator "Лина махала ей рукой."
    show lina speak at character_scale
    e "[persistent.user_name]! Привет! Я так рада тебя видеть!"
    show lina smile at character_scale_center_soft_approach
    narrator "Лина обняла [persistent.user_name]."
    e "Ну что, готова? Я тебе все покажу!"
    hide lina
    play sound "song/school_bell.mp3"
    pause 2.0
    narrator "Прозвенел звонок."
    scene black with fade
    stop music fadeout 3.0
    stop sound fadeout 3.0
    show text "{size=80}Конец первой главы{/size}" with dissolve
    pause 2.0
    hide text with dissolve
    pause 0.5
    $ auto_save_chapter_complete("Глава Первая: Связь")
    # Переход ко второй главе
    jump chapter_two
    return

################################################################################
## ГЛАВА ВТОРАЯ: НОВЫЕ ЗНАКОМСТВА
################################################################################
label chapter_two:
    $ current_chapter = "Глава Вторая: Новые знакомства"
    scene black with fade
    show text "{size=80}Глава Вторая{/size}\n{size=60}Новые знакомства{/size}" with dissolve
    pause 3.0
    scene black with dissolve
    
    play music "song/Audio_soft_2.mp3" fadein 5.0
    $ renpy.music.set_volume(0.4, delay=5)
    scene bg school_entrance with fade
    narrator "Лина вела [persistent.user_name] по коридорам."
    show lina speak at character_scale
    e "Смотри, это наша раздевалка! А тут спортзал."
    narrator "Из-за угла выскочил парень."
    show alex smile at character_scale
    a "Ой, простите! Вы новенькая?"
    
    menu second_chapter_first_choice:
        "Да, я сегодня первый день. Приятно познакомиться.":
            $ chapter2_choice_1 = 1
            $ update_player_state(self_awareness_change=3, trust_change=5, anxiety_change=-3)
            user_char "Да, я сегодня первый день. Приятно познакомиться."
        "Эм... да. Я новенькая.":
            $ chapter2_choice_1 = 2
            $ update_player_state(anxiety_change=3, trust_change=-2)
            user_char "Эм... да. Я новенькая."
        "Просто молча кивнуть":
            $ chapter2_choice_1 = 3
            $ update_player_state(self_awareness_change=2, vocabulary_change=2)
            narrator "[persistent.user_name] просто молча кивнула."
            
    a "Класс! Я Алекс. Если что-то нужно — обращайся."
    show lina speak at character_scale_left
    show alex smile at character_scale_right
    e "Алекс играет на гитаре!"
    a "Слушай, а вы на большую перемену в музыкалку не хотите сходить?"
    
    menu second_chapter_second_choice:
        "Давай сходим. Интересно посмотреть.":
            $ chapter2_choice_2 = 1
            $ update_player_state(self_awareness_change=5, vocabulary_change=3)
            user_char "Давай сходим. Интересно посмотреть."
        "Не знаю... Я не очень люблю шумные компании.":
            $ chapter2_choice_2 = 2
            $ update_player_state(anxiety_change=5)
            user_char "Не знаю... Я не очень люблю шумные компании."
        "Если Лина хочет, то я тоже пойду.":
            $ chapter2_choice_2 = 3
            $ update_player_state(empathy_change=5, trust_change=5)
            user_char "Если Лина хочет, то я тоже пойду."

    if chapter2_choice_2 == 2:
        e "Ну хотя бы на пару минут заглянем?"
        user_char "Ладно, уговорила."

    hide alex
    hide lina
    narrator "Прозвенел звонок на урок."
    scene bg classroom with fade
    show teacher kind at character_scale
    t "Ребята, сегодня у нас новая ученица. Представься, пожалуйста."
    user_char "Меня зовут [persistent.user_name]. Я надеюсь, мы подружимся."
    t "Садись. Катя, покажешь нашей новой ученице всё?"
    show katia smile at character_scale_left
    k "Конечно, Анна Сергеевна!"
    hide teacher
    narrator "Катя помахала рукой."
    
    # Перемена
    scene bg school_entrance with fade
    show katia speak at character_scale_left
    show lina smile at character_scale_right
    k "У нас есть театральный кружок!"
    e "Ой, точно! [persistent.user_name], это же отличная идея!"
    show alex smile at character_scale_center
    a "Ну что, идете в музыкалку?"
    
    menu second_chapter_final_choice:
        "Идем! Я хочу послушать.":
            $ chapter2_choice_final = 1
            $ update_player_state(self_awareness_change=5, vocabulary_change=5, anxiety_change=-5)
            jump music_room_scene
        "Может, в другой раз? Я немного устала.":
            $ chapter2_choice_final = 2
            $ update_player_state(self_awareness_change=3, vocabulary_change=3)
            jump library_scene
        "А можно мы с Катей тоже придем?":
            $ chapter2_choice_final = 3
            $ update_player_state(empathy_change=8, trust_change=5)
            k "Ой, а можно? Я тоже очень хочу!"
            a "Конечно!"
            jump music_room_scene

label music_room_scene:
    hide alex
    hide katia
    hide lina
    scene bg music_room with fade
    play music "song/gentle_guitar.mp3" fadein 3.0
    narrator "Актовый зал оказался уютным."
    show alex smile at character_scale
    a "Мы сейчас разучиваем новую песню. Хотите послушать?"
    hide alex
    narrator "Алекс начал играть и предложил попробовать отбить ритм."
    
    # ЗАПУСК МИНИ-ИГРЫ 2
    $ start_rhythm_game()
    
    $ beats_count = 0
    while beats_count < 5:
        $ renpy.pause(2.0)
        $ beats_count += 1
    
    $ stop_rhythm_game()
    
    if rhythm_game_score >= 30:
        narrator "У тебя отлично получилось! Алекс довольно заулыбался."
        $ update_player_state(empathy_change=10, trust_change=10, self_awareness_change=5)
    elif rhythm_game_score > 0:
        narrator "Неплохо для начала."
        $ update_player_state(empathy_change=5, trust_change=5)
    else:
        narrator "Ты сбивалась, но Алекс не обратил внимания."
        $ update_player_state(anxiety_change=5)

    show lina speak at character_scale
    e "Тебе нравится, [persistent.user_name]?"
    show lina smile at character_scale
    user_char "Да... очень. Это красиво."
    hide lina
    jump chapter_two_end

label library_scene:
    hide alex
    hide katia
    hide lina
    scene bg library with fade
    narrator "В библиотеке было тихо."
    show librarian kind at character_scale
    lib "Здравствуй, дорогая! Хочешь что-то почитать?"
    user_char "Здравствуйте. Да, я бы хотела... что-то поспокойнее?"
    lib "Тогда тебе понравится этот сборник рассказов о природе."
    hide librarian
    narrator "[persistent.user_name] устроилась в кресле."
    $ update_player_state(trust_change=10, empathy_change=5)
    jump chapter_two_end

label chapter_two_end:
    scene black with fade
    stop music fadeout 3.0
    show text "{size=80}Конец второй главы{/size}" with dissolve
    pause 2.0
    hide text with dissolve
    pause 0.5
    $ auto_save_chapter_complete("Глава Вторая: Новые знакомства")
    
    # Заглушка для перехода к 3 главе
    "Глава Третья: В разработке..."
    return