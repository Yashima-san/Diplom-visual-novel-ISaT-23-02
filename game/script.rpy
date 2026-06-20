# Определения персонажей и изображений
define user_char = Character("[persistent.user_name]", color="#ff9e5e")
define thought_user = Character("[persistent.user_name]", what_italic=True)
define narrator = Character(None, what_italic=True)
define a = Character('Алекс', color="#6b8e23")
define k = Character('Катя', color="#fe7d90")
define e = Character('Лина', color="#707ef6")

define t = Character('Анна Сергеевна', color="#9370db")
define lib = Character('Библиотекарь', color="#a0522d")

# Persistent переменные
default persistent.user_name = ""
default persistent.user_id = None
default persistent.user_data = None

# Основные переменные игры
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
default library_choice = 0
default music_reaction = 0
default conflict_help_choice = 0

# НОВЫЕ ПЕРЕМЕННЫЕ ДЛЯ ОТСЛЕЖИВАНИЯ СОБЫТИЙ
default visited_music_room = False          # Были ли в музыкалке (слышали игру Алекса)
default heard_alex_play = False             # Слышали ли игру Алекса на гитаре
default after_music_invite_sent = False     # Отправляли ли предложение пойти в музыкалку снова
default conflict_known_from = None          # Откуда узнали о конфликте: "direct", "lina", None

# Переменные для сюжета
default heard_about_conflict = False
default conflict_version = 0
default helped_katya = False

# Статистика выборов
default choice_statistics = {
    "self_awareness_choices": 0,
    "empathy_choices": 0,
    "avoidance_choices": 0,
    "healthy_choices": 0,
    "total_choices": 0
}

################################################################################
## ФУНКЦИИ ДЛЯ РАБОТЫ С СОСТОЯНИЕМ ИГРОКА
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
        
        if self_awareness_change > 0:
            store.choice_statistics["self_awareness_choices"] += 1
        if empathy_change > 0:
            store.choice_statistics["empathy_choices"] += 1
        if anxiety_change > 0 and self_awareness_change == 0:
            store.choice_statistics["avoidance_choices"] += 1
        if trust_change > 0 and empathy_change > 0:
            store.choice_statistics["healthy_choices"] += 1
        store.choice_statistics["total_choices"] += 1
        
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
                'trust': store.player_trust_level,
                'choice_stats': dict(store.choice_statistics)
            })
            if len(persistent.player_states[str_id]) > 50:
                persistent.player_states[str_id] = persistent.player_states[str_id][-50:]

    def get_current_chapter_safe():
        try:
            if hasattr(store, 'current_chapter') and store.current_chapter:
                return store.current_chapter
        except:
            pass
        return "Глава Первая: Связь"

################################################################################
## ТРАНСФОРМАЦИИ ДЛЯ СПРАЙТОВ (ПЛАВНОЕ ПЕРЕМЕЩЕНИЕ)
################################################################################

# Базовый размер спрайтов (остаётся zoom 0.28)
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

# Плавное приближение (мягкое)
transform character_center_soft_approach:
    zoom 0.28
    xalign 0.5
    yalign 1.0
    easein 1.2 zoom 0.31
    pause 0.1
    easeout 0.5 zoom 0.28

# Плавное появление с боков (для говорящих персонажей)
transform character_speak_slide:
    zoom 0.28
    xalign 0.5
    yalign 1.0
    easein 0.3 xoffset 15
    pause 0.15
    easeout 0.3 xoffset 0

# Плавное появление с боков
transform character_slide_left:
    xalign -0.3
    yalign 1.0
    zoom 0.28
    easein 0.6 xalign 0.25

transform character_slide_right:
    xalign 1.3
    yalign 1.0
    zoom 0.28
    easein 0.6 xalign 0.75

transform character_slide_center:
    xalign -0.3
    yalign 1.0
    zoom 0.28
    easein 0.6 xalign 0.5

# Плавное приближение к персонажу (камера приближается)
transform character_zoom_in:
    zoom 0.28
    xalign 0.5
    yalign 1.0
    easein 1.0 zoom 0.35
    pause 1.0
    easeout 1.0 zoom 0.28

# Плавное отдаление от персонажа
transform character_zoom_out:
    zoom 0.28
    xalign 0.5
    yalign 1.0
    easein 1.0 zoom 0.22
    pause 0.5
    easeout 1.0 zoom 0.28

# Эффект столкновения (тряска)
transform character_collision(duration=0.6, intensity=8):
    zoom 0.28
    xalign 0.5
    yalign 1.0
    easein 0.1 xoffset intensity
    easein 0.1 xoffset -intensity
    easein 0.1 xoffset intensity * 0.6
    easein 0.1 xoffset -intensity * 0.6
    easein 0.1 xoffset intensity * 0.3
    easein 0.1 xoffset -intensity * 0.3
    easein 0.1 xoffset 0

# Эффект столкновения для левого персонажа
transform character_collision_left(duration=0.6, intensity=6):
    zoom 0.28
    xalign 0.25
    yalign 1.0
    easein 0.08 xoffset intensity
    easein 0.08 xoffset -intensity
    easein 0.08 xoffset intensity * 0.6
    easein 0.08 xoffset -intensity * 0.6
    easein 0.08 xoffset intensity * 0.3
    easein 0.08 xoffset -intensity * 0.3
    easein 0.08 xoffset 0

# Эффект столкновения для правого персонажа
transform character_collision_right(duration=0.6, intensity=6):
    zoom 0.28
    xalign 0.75
    yalign 1.0
    easein 0.08 xoffset -intensity
    easein 0.08 xoffset intensity
    easein 0.08 xoffset -intensity * 0.6
    easein 0.08 xoffset intensity * 0.6
    easein 0.08 xoffset -intensity * 0.3
    easein 0.08 xoffset intensity * 0.3
    easein 0.08 xoffset 0

# Плавное исчезновение со смещением
transform character_fade_left:
    alpha 1.0
    xalign 0.25
    yalign 1.0
    zoom 0.28
    easeout 0.5 alpha 0.0 xoffset -50

transform character_fade_right:
    alpha 1.0
    xalign 0.75
    yalign 1.0
    zoom 0.28
    easeout 0.5 alpha 0.0 xoffset 50

# Плавное появление с эффектом "взгляда"
transform character_appear_thoughtful:
    alpha 0.0
    zoom 0.26
    xalign 0.5
    yalign 1.0
    easein 0.8 alpha 1.0 zoom 0.28

# Плавное движение в центр из любого положения
transform character_move_to_center:
    zoom 0.28
    yalign 1.0
    easein 0.6 xalign 0.5

################################################################################
## ИЗОБРАЖЕНИЯ (спрайты и фоны)
################################################################################
# Персонажи
image lina neutral = ConditionSwitch("renpy.loadable('images/characters/lina_neutral.png')", "images/characters/lina_neutral.png", "True", "#707ef6")
image lina speak = ConditionSwitch("renpy.loadable('images/characters/lina_speak.png')", "images/characters/lina_speak.png", "True", "#707ef6")
image lina smile = ConditionSwitch("renpy.loadable('images/characters/lina_smile.png')", "images/characters/lina_smile.png", "True", "#707ef6")
image lina speaksmile = ConditionSwitch("renpy.loadable('images/characters/lina_speak_smile.png')", "images/characters/lina_speak_smile.png", "True", "#707ef6")
image lina sad = ConditionSwitch("renpy.loadable('images/characters/lina_sad.png')", "images/characters/lina_sad.png", "True", "#707ef6")

image alex neutral = ConditionSwitch("renpy.loadable('images/characters/alex_neutral.png')", "images/characters/alex_neutral.png", "True", "#6b8e23")
image alex speak = ConditionSwitch("renpy.loadable('images/characters/alex_speak.png')", "images/characters/alex_speak.png", "True", "#707ef6")
image alex smile = ConditionSwitch("renpy.loadable('images/characters/alex_smile.png')", "images/characters/alex_smile.png", "True", "#6b8e23")
image alex speaksmile = ConditionSwitch("renpy.loadable('images/characters/alex_speak_smile.png')", "images/characters/alex_speak_smile.png", "True", "#707ef6")
image alex sad = ConditionSwitch("renpy.loadable('images/characters/alex_sad.png')", "images/characters/alex_sad.png", "True", "#707ef6")

image katia neutral = ConditionSwitch("renpy.loadable('images/characters/katia_neutral.png')", "images/characters/katia_neutral.png", "True", "#fe7d90")
image katia speak = ConditionSwitch("renpy.loadable('images/characters/katia_speak.png')", "images/characters/katia_speak.png", "True", "#707ef6")
image katia smile = ConditionSwitch("renpy.loadable('images/characters/katia_smile.png')", "images/characters/katia_smile.png", "True", "#fe7d90")
image katia speaksmile = ConditionSwitch("renpy.loadable('images/characters/katia_speak_smile.png')", "images/characters/katia_speak_smile.png", "True", "#707ef6")
image katia sad = ConditionSwitch("renpy.loadable('images/characters/katia_sad.png')", "images/characters/katia_sad.png", "True", "#707ef6")

# image teacher neutral = ConditionSwitch("renpy.loadable('images/characters/teacher_neutral.png')", "images/characters/teacher_neutral.png", "True", "#9370db")
# image teacher kind = ConditionSwitch("renpy.loadable('images/characters/teacher_kind.png')", "images/characters/teacher_kind.png", "True", "#9370db")
# image librarian neutral = ConditionSwitch("renpy.loadable('images/characters/librarian_neutral.png')", "images/characters/librarian_neutral.png", "True", "#a0522d")
# image librarian kind = ConditionSwitch("renpy.loadable('images/characters/librarian_kind.png')", "images/characters/librarian_kind.png", "True", "#a0522d")

# Фоны
image bg night_room = ConditionSwitch("renpy.loadable('images/night_room.png')", "images/night_room.png", "True", "#000000")
image bg room_pk = ConditionSwitch("renpy.loadable('images/room_pk.png')", "images/room_pk.png", "True", "#2a2a2a")
image bg bg_room_pk_light = ConditionSwitch("renpy.loadable('images/room_pk_light.png')", "images/room_pk_light.png", "True", "#3a3a3a")
image bg school_entrance = ConditionSwitch("renpy.loadable('images/school_entrance.png')", "images/school_entrance.png", "True", "#4a4a4a")
image bg school_hallway = ConditionSwitch("renpy.loadable('images/school_hallway.png')", "images/school_hallway.png", "True", "#5c5c5c")
image bg kitchen = ConditionSwitch("renpy.loadable('images/kitchen.png')", "images/kitchen.png", "True", "#5a5a5a")
image bg street = ConditionSwitch("renpy.loadable('images/street.png')", "images/street.png", "True", "#6a6a6a")
image bg classroom = ConditionSwitch("renpy.loadable('images/classroom.png')", "images/classroom.png", "True", "#8a8a8a")
image bg music_room = ConditionSwitch("renpy.loadable('images/music_room.png')", "images/music_room.png", "True", "#9a9a9a")
image bg library = ConditionSwitch("renpy.loadable('images/library.png')", "images/library.png", "True", "#aaaaaa")
image cg room_evening = ConditionSwitch("renpy.loadable('images/cg/room_evening.png')", "images/cg/room_evening.png", "True", "#2b2b2b")

################################################################################
## ФУНКЦИИ СОХРАНЕНИЯ И ПЕРЕХОДОВ
################################################################################
init python:
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
            json_data["choice_statistics"] = dict(store.choice_statistics)
        except Exception:
            json_data["chapter"] = "Глава Первая: Связь"
            json_data["_timestamp"] = time.time()
        return json_data
    
    if hasattr(config, 'save_json_callbacks'):
        config.save_json_callbacks = []
        config.save_json_callbacks.append(add_user_info_to_save)

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

################################################################################
## НАЧАЛО ИГРЫ
################################################################################
label start:
    # Показываем предупреждение
    $ show_warning = True
    while show_warning:
        call screen warning_screen
        if _return:
            $ show_warning = False

    $ current_chapter = "Глава Первая: Связь"
    $ player_self_awareness = 0
    $ player_empathy = 0
    $ player_emotional_vocabulary = 0
    $ player_anxiety_level = 50
    $ player_trust_level = 30
    $ choice_statistics = {"self_awareness_choices": 0, "empathy_choices": 0, "avoidance_choices": 0, "healthy_choices": 0, "total_choices": 0}
    $ helped_katya = False
    $ visited_music_room = False
    $ heard_alex_play = False
    $ after_music_invite_sent = False
    $ conflict_known_from = None
    
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
    
    narrator "Ты ничего не забыла, [persistent.user_name]?"
    narrator "Пора просыпаться..."
    
    scene black with fade
    show text "{size=80}Глава Первая{/size}\n{size=60}Связь{/size}" with dissolve
    pause 3.0
    scene black with dissolve

    if persistent.user_id and 'db' in globals() and hasattr(db, 'update_save_progress'):
        $ db.update_save_progress(persistent.user_id, "Глава Первая: Связь")
    
    $ unlock_achievement("wake_up")
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
    narrator "На стене висел постер с изображением аниме-персонажа."
    thought_user "Я научилась имитировать. Улыбаться, когда нужно. Но внутри – тишина."
    thought_user "Единственный, кто меня понимает – это моя интернет-подруга, Лина."
    
    show bg room_pk with dissolve
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
        $ show_chat_choices(["Звучит здорово! Я согласна на все! 👍", "Давай сначала посмотрим, как пройдет день. 🤔"], second_choice_callback)
        $ store.wait_for_chat()
    elif first_choice == 2:
        $ e("Ой, я понимаю! Но не переживай! Мы же вместе! 🤗")
        $ e("Я придумала, что мы можем ходить в библиотеку, там так тихо и уютно!")
        $ show_chat_choices(["Звучит здорово! Библиотека – отличная идея!", "Спасибо, Лина! Я пока буду просто наблюдать. 👀"], second_choice_callback)
        $ store.wait_for_chat()
    elif first_choice == 3:
        $ e("Ой, [persistent.user_name]! 🥺 Я так тронута!")
        $ e("Я тоже очень рада! И ты не волнуйся, я буду рядом! 💕")
        $ show_chat_choices(["Спасибо, Лина! Ты лучшая!", "Спасибо, Лина!"], second_choice_callback)
        $ store.wait_for_chat()
    
    pause 2.0
    $ disable_chat_mode()
    jump night_scene

label night_scene:
    stop music
    scene bg night_room with fade
    narrator "Ночь опустилась на город мягко."
    thought_user "Завтрашний день... Прыжок в неизвестность."
    thought_user "Психолог говорила, что важно анализировать свои состояния."
    narrator "[persistent.user_name] взяла в руки таблицу «Колесо эмоций»."
    
    call emotion_wheel_game("morning_school") from _call_emotion_wheel_game
    
    $ emotion_game_completed = True
    
    narrator "Засыпая, [persistent.user_name] думала только об одном…"
    thought_user "Скорее бы наступило утро..."
    scene black with fade
    pause 1.0
    jump morning_scene

label morning_scene:
    stop music fadeout 1.0
    scene cg room_evening with fade
    play music "song/Audio_soft_1.mp3" fadein 3.0
    narrator "Утро 3 сентября."
    
    $ enable_chat_mode()
    $ e("Доброе утро, [persistent.user_name]! 🌅 Не забудь взять тетради и хорошее настроение 😘")
    
    $ show_chat_choices(["Спасибо, Лина! Я уже встаю. Увидимся у входа! ❤️", "Я тоже волнуюсь... Но спасибо, что ты рядом!", "Увидимся у входа в школу! 👋"], morning_choice_callback)
    
    $ store.wait_for_chat()
    pause 2.0
    $ disable_chat_mode()
    
    narrator "[persistent.user_name] начала собираться."
    scene bg kitchen with fade
    narrator "На кухне была записка от родителей: 'Удачи в новой школе! Мы в тебя верим!'"
    thought_user "Как всегда, коротко и по делу."
    stop music fadeout 2.0
    narrator "Она вышла из дома."
    scene bg street with fade
    play music "song/school_ambient.mp3" fadein 2.0
    play sound "sounds/footsteps.mp3" fadein 2.0
    narrator "Школа виднелась вдалеке."

    scene bg school_entrance with fade
    show lina smile at character_slide_center
    narrator "Лина махала ей рукой."
    show lina speaksmile at character_speak_slide
    e "[persistent.user_name]! Привет! Я так рада тебя видеть!"
    show lina smile at character_center_soft_approach
    play sound "sounds/hugs.mp3"
    narrator "Лина обняла [persistent.user_name]."
    stop sound

    e "Ну что, готова? Я тебе все покажу!"
    show lina speaksmile at character_speak_slide
    
    call emotion_diary_minigame("meeting_lina") from _call_emotion_diary_minigame
    
    hide lina
    scene black with fade
    stop music fadeout 3.0
    show text "{size=80}Конец первой главы{/size}" with dissolve
    pause 2.0
    hide text with dissolve
    pause 0.5
    $ auto_save_chapter_complete("Глава Первая: Связь")
    
    jump chapter_two

################################################################################
## ГЛАВА ВТОРАЯ: НОВЫЕ ЗНАКОМСТВА
################################################################################
label chapter_two:
    $ current_chapter = "Глава Вторая: Новые знакомства"
    $ heard_about_conflict = False
    $ conflict_version = 0
    $ helped_katya = False
    
    scene black with fade
    show text "{size=80}Глава Вторая{/size}\n{size=60}Новые знакомства{/size}" with dissolve
    pause 3.0
    scene black with dissolve
    
    play music "song/Audio_soft_2.mp3" fadein 5.0
    play sound "sounds/footsteps.mp3" fadein 2.0
    $ renpy.music.set_volume(0.4, delay=5)
    scene bg school_hallway with fade
    show lina smile at character_slide_left
    narrator "Лина вела [persistent.user_name] по коридорам."
    show lina speaksmile at character_speak_slide
    e "Смотри, это наша раздевалка! А тут спортзал."
    
    play sound "sounds/running.mp3" fadein 1.0
    narrator "Пока Лина объясняла где что находится, внезапно, из-за угла выскочил парень."
    stop sound fadeout 3.0
    play sound "sounds/conflict.mp3" fadein 1.0
    show lina neutral at character_collision_left
    show alex speak at character_collision_right
    stop sound fadeout 3.0
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
    
    show alex speaksmile at character_scale_right
    a "Класс! Я Алекс. Если что-то нужно — обращайся."
    show lina speaksmile at character_scale_left
    show alex smile at character_scale_right
    e "Алекс играет на гитаре!"
    show alex speak at character_scale_right
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
        show lina sad at character_scale_center
        e "Ну хотя бы на пару минут заглянем?"
        user_char "Ладно, уговорила."
        show lina smile at character_scale_center

    # --- РАЗВЕТВЛЕНИЕ: ИДЁМ В МУЗЫКАЛКУ ИЛИ НЕТ ---
    if chapter2_choice_2 != 2:
        jump music_room_visit
    else:
        jump music_room_visit

label music_room_visit:
    scene bg music_room with fade
    play music "song/gentle_guitar.mp3" fadein 3.0
    
    $ visited_music_room = True
    
    narrator "Актовый зал оказался уютным и светлым."
    show alex speaksmile at character_scale_center
    a "Мы сейчас разучиваем новую песню. Хотите послушать?"
    
    hide alex
    narrator "Алекс взял гитару и начал играть мелодичную композицию."
    narrator "Звуки гитары наполнили комнату теплом и уютом."
    stop music fadeout 2.0
    narrator "Музыка закончилась, и Алекс посмотрел на тебя с надеждой."
    
    $ heard_alex_play = True
    
    show alex smile at character_scale_center
    
    menu music_reaction_menu:
        "Это было красиво. Спасибо!":
            $ store.music_reaction = 1
            $ update_player_state(self_awareness_change=5, vocabulary_change=5, anxiety_change=-3)
            user_char "Это было красиво. Спасибо!"
            show alex speaksmile at character_scale_center
            a "Спасибо! Я очень рад, что тебе понравилось."
        "Мне понравилось, очень душевно.":
            $ store.music_reaction = 2
            $ update_player_state(empathy_change=5, trust_change=5)
            user_char "Мне понравилось, очень душевно."
            show alex speaksmile at character_scale_center
            a "Спасибо! Музыка помогает мне выражать то, что сложно сказать словами."
        "Интересно, но для меня это пока непривычно.":
            $ store.music_reaction = 3
            $ update_player_state(self_awareness_change=3, vocabulary_change=3)
            user_char "Интересно, но для меня это пока непривычно."
            show alex speaksmile at character_scale_center
            a "Понимаю. Но если захочешь послушать ещё — приходи, я всегда рад."
    
    show lina speaksmile at character_scale_left
    e "Ты здорово играешь, Алекс!"
    show alex speaksmile at character_scale_right
    show lina smile at character_scale_left
    a "Спасибо, Лина."
    
    # Лина уходит
    show lina speak at character_scale_left
    e "Извините, мне нужно забежать в учительскую. Я быстро!"
    show lina neutral at character_scale_left
    play sound "sounds/running.mp3" fadein 2.0
    hide lina with dissolve
    
    show alex speak at character_scale_center
    a "Давай тогда сходим в библиотеку, покажу тебе книге о музыке?"
    stop sound fadeout 3.0
    a "Если конечно ты хочешь."
    a "Ну как?"
    show alex neutral at character_scale_center
    # --- ВАРИАНТЫ ДАЛЬНЕЙШИХ ДЕЙСТВИЙ ---
    menu after_music_room_options:
        "Пойти с Алексом в библиотеку":
            $ library_choice = 1
            $ update_player_state(self_awareness_change=3)
            jump library_with_alex
            
        "Подождать Лину здесь, в музыкалке":
            $ library_choice = 2
            $ update_player_state(empathy_change=3)
            jump wait_for_lina_in_music_room

# ============================================================================
# ПУТЬ 1: В БИБЛИОТЕКУ С АЛЕКСОМ (ПРЯМОЕ НАБЛЮДЕНИЕ КОНФЛИКТА)
# ============================================================================
label library_with_alex:
    scene bg library with fade
    show alex speaksmile at character_scale_center
    play sound "sounds/footsteps.mp3" fadein 2.0
    a "Вот мы и в библиотеке. Здесь так спокойно... Я часто сюда прихожу, когда хочу побыть один."
    narrator "Алекс подошёл к стеллажу и взял книгу по музыкальной теории."
    a "А ты любишь читать?"
    stop sound fadeout 1.0
    show alex smile at character_scale_center
    
    menu:
        "Да, люблю. Особенно когда хочу понять свои чувства.":
            $ update_player_state(self_awareness_change=5, vocabulary_change=3)
            user_char "Да, люблю. Особенно когда хочу понять свои чувства."
            show alex speaksmile at character_scale_center
            a "Это здорово. Книги действительно помогают разобраться в себе."
        "Не очень... Мне сложно сосредоточиться.":
            $ update_player_state(anxiety_change=3)
            user_char "Не очень... Мне сложно сосредоточиться."
            show alex speak at character_scale_center
            a "Понимаю. Иногда я тоже не могу усидеть на месте."
        "Иногда читаю, но больше люблю слушать музыку.":
            $ update_player_state(empathy_change=3)
            user_char "Иногда читаю, но больше люблю слушать музыку."
            show alex speaksmile at character_scale_center
            a "Музыка — это тоже язык чувств. Рад, что тебе понравилось."
    
    narrator "Вы мило поболтали о книгах и музыке. [persistent.user_name] решила немного оглядеться и начала осматривать стеллажи на соседнем ряду."
    narrator "Она была недалеко от Алекса, который что-то искал в книгах."
    narrator "[persistent.user_name] заметила как к Алекс начал разговаривать со старастой их класса."

    # Появляется Катя
    show alex neutral at character_scale_center
    show katia neutral at character_scale_right with dissolve
    katya "Алекс? Ты тоже здесь?"
    show alex speak at character_scale_center
    a "Да, ищу ноты. А ты что делаешь?"
    show alex neutral at character_scale_center

    katya "Готовлюсь к контрольной... Но у меня ничего не получается!"
    
    show katia sad at character_scale_right
    show alex speak at character_scale_center
    a "Может, я смогу помочь? Я неплохо разбираюсь в этих темах."
    katya "Нет! Не надо! Оставь меня!"
    show alex sad at character_scale_center
    a "Но я хочу помочь. Почему ты так реагируешь?"
    show katia speak at character_scale_right
    katya "Ты не понимаешь! Родители и так давят на меня, а тут ещё и ты со своей помощью!"
    show katia neutral at character_scale_right
    
    show alex sad at character_scale_left
    a "Извини... Я не хотел тебя обидеть."
    katya "Просто... просто оставь меня в покое, пожалуйста."
    
    hide alex with dissolve
    narrator "Алекс развернулся и ушёл, оставив Катю одну."
    
    show katia sad at character_scale_center
    katya "Почему всё так сложно..."
    
    $ heard_about_conflict = True
    $ conflict_known_from = "direct"
    
    jump help_katya_choice

# ============================================================================
# ПУТЬ 2: ЖДЁМ ЛИНУ В МУЗЫКАЛКЕ (УЗНАЁМ О КОНФЛИКТЕ ОТ ЛИНЫ)
# ============================================================================
label wait_for_lina_in_music_room:
    scene bg music_room with fade
    narrator "Ты осталась в музыкальной комнате, ожидая Лину."
    narrator "В тишине ты заметила, как спокойно и уютно здесь."
    thought_user "Интересно, что чувствует Алекс, когда играет? Радость? Спокойствие? Или что-то другое?"
    
    show lina speaksmile at character_scale_center
    e "[persistent.user_name]! Прости, что так долго. Учительница дала мне журнал отнести."
    
    user_char "Всё в порядке."

    show lina speak at character_scale_center
    e "Слушай, я только что видела Катю... Она шла в библиотеку и выглядела очень расстроенной."
    e "Кажется, она поругалась с Алексом. Он просто хотел помочь, а она накричала."
    user_char "Правда? Бедная Катя... Может, с ней что-то случилось?"
    e "Не знаю... Но мне кажется, ей нужна поддержка. Может, зайдём к ней?"
    show lina sad at character_scale_center
    
    $ heard_about_conflict = True
    $ conflict_known_from = "lina"
    
    menu go_to_katya_from_lina:
        "Да, давай проверим, как она":
            $ update_player_state(empathy_change=5)
            narrator "Вы с Линой направились в библиотеку."
            jump go_to_library_with_lina
            
        "Может, ей нужно побыть одной?":
            $ update_player_state(self_awareness_change=3)
            narrator "Ты решила, что Кате нужно время. Вы остались ждать в коридоре."
            narrator "Через несколько минут Катя вышла из библиотеки, вытирая глаза."
            jump meet_katya_after_conflict

# ============================================================================
# ПОМОЩЬ КАТЕ (ПРЯМОЕ НАБЛЮДЕНИЕ)
# ============================================================================
label help_katya_choice:
    show katia sad at character_scale_center
    
    menu:
        "Подойти к Кате и поговорить (помочь разобраться)":
            $ update_player_state(empathy_change=3, trust_change=2)
            $ helped_katya = True
            jump talk_to_katya_with_minigame
            
        "Дать ей время побыть одной":
            $ update_player_state(self_awareness_change=3, empathy_change=2)
            $ helped_katya = False
            narrator "Ты решила не вмешиваться. Иногда людям нужно побыть наедине со своими мыслями."
            narrator "Ты тихо села в кресло с книгой, но краем глаза всё равно поглядывала на Катю."
            jump observe_katya_direct

# ============================================================================
# РАЗГОВОР С КАТЕЙ С ИСПОЛЬЗОВАНИЕМ МИНИ-ИГРЫ "ЭМОЦИОНАЛЬНЫЙ ДЕТЕКТИВ"
# ============================================================================
label talk_to_katya_with_minigame:
    scene bg library with fade
    show katia sad at character_scale_center
    
    user_char "Катя... Ты в порядке? Может, поговорим?"
    
    katya "А? Да... Всё нормально. Просто..."
    show katia speak at character_scale_center
    katya "Ты, наверное, слышала? Я накричала на Алекса."
    show katia sad at character_scale_center

    user_char "Я не хочу лезть не в своё дело, но если хочешь поговорить..."
    
    narrator "Ты вспомнила упражнения по распознаванию эмоций, которые практиковала..."
    narrator "Попробуй понять, что на самом деле чувствует Катя."
    
    # Вызов мини-игры Эмоциональный детектив со специальным сценарием
    call emotion_detective_minigame("help_katya") from _call_emotion_detective_minigame
    
    # После мини-игры проверяем успех
    if detective_score >= 10:
        jump successful_help_katya
    elif detective_score >= 5:
        jump partial_help_katya
    else:
        jump less_successful_help_katya

# ============================================================================
# УСПЕШНАЯ ПОМОЩЬ КАТЕ
# ============================================================================
label successful_help_katya:
    show katia neutral at character_scale_center
    
    user_char "Катя... Мне кажется, ты не злишься на Алекса на самом деле. Ты просто... устала от давления и стыдишься того, что не справляешься?"
    
    katya "Откуда ты... Откуда ты знаешь?"
    
    user_char "Я вижу. Ты опускаешь плечи, будто хочешь стать меньше. И избегаешь смотреть в глаза."

    show katia speak at character_scale_center
    katya "Ты права... Родители требуют только отличных оценок. А я чувствую, что если получу четвёрку — подведу их."
    katya "Алекс пришёл со своей помощью, а я... я просто сорвалась. Мне так стыдно."
    show katia sad at character_scale_center

    user_char "Понимаю. Иногда помощь может казаться давлением. Но Алекс искренне хотел поддержать тебя."

    show katia speaksmile at character_scale_center
    katya "Знаю... Я поговорю с ним. Извинюсь."
    katya "Спасибо тебе. Ты очень внимательная. Не каждый умеет так... замечать."
    show katia smile at character_scale_center

    user_char "Я учусь этому. Рада, что смогла помочь."
    
    $ update_player_state(empathy_change=10, trust_change=8, self_awareness_change=5, vocabulary_change=5)
    
    jump after_conflict_with_help

# ============================================================================
# ЧАСТИЧНО УСПЕШНАЯ ПОМОЩЬ
# ============================================================================
label partial_help_katya:
    show katia neutral at character_scale_center
    
    user_char "Катя... Кажется, ты не столько злишься, сколько переживаешь из-за чего-то. Может, давление родителей?"
    
    show katia speak at character_scale_center
    katya "Ты... отчасти права. Да, мне сейчас непросто."
    show katia sad at character_scale_center
    katya "Но я пока не готова говорить об этом подробно. Извини."
    
    user_char "Понимаю. Просто знай, что я рядом, если захочешь поговорить."

    show katia speaksmile at character_scale_center
    katya "Спасибо... Это много значит."
    show katia sad at character_scale_center
    
    $ update_player_state(empathy_change=5, trust_change=4, self_awareness_change=3)
    
    jump after_conflict_with_help

# ============================================================================
# МЕНЕЕ УСПЕШНАЯ ПОМОЩЬ
# ============================================================================
label less_successful_help_katya:
    show katia neutral at character_scale_center
    
    user_char "Катя... Всё наладится. Не переживай так."
    show katia sad at character_scale_center
    katya "Спасибо... но ты не совсем понимаешь."
    show katia speak at character_scale_left
    katya "Ладно, мне пора. Увидимся."
    
    hide katia with dissolve
    narrator "Катя быстро ушла, оставив тебя с чувством, что ты могла бы сделать больше."
    
    $ update_player_state(empathy_change=2, anxiety_change=3)
    
    jump after_conflict_without_help

# ============================================================================
# НАБЛЮДЕНИЕ ЗА КАТЕЙ (БЕЗ АКТИВНОЙ ПОМОЩИ)
# ============================================================================
label observe_katya_direct:
    narrator "Через несколько минут Катя глубоко вздохнула и вытерла глаза."
    
    show katia speak at character_scale_center
    katya "Эй... Ты здесь?"
    show katia neutral at character_scale_center
    user_char "Да, просто читаю."
    show katia speak at character_scale_center
    katya "Ты... не хочешь спросить, что случилось?"
    show katia sad at character_scale_center

    menu:
        "Если хочешь рассказать — я послушаю":
            $ update_player_state(empathy_change=5, trust_change=8)
            $ helped_katya = True
            user_char "Я не хочу давить. Если захочешь поделиться — я рядом."
            show katia speaksmile at character_scale_center
            katya "Ты очень добрая... Спасибо."
            katya "Просто у меня давление от родителей. Они ждут от меня идеальных результатов."
            katya "Алекс... он просто оказался не в то время не в том месте."
            show katia sad at character_scale_center
            narrator "Ты задумалась, что чувствует Катя на самом деле..."
            call emotion_wheel_game("simple_empathy") from _call_emotion_wheel_game_1
            
            jump after_conflict_with_help
            
        "Извини, я не хочу вмешиваться":
            $ update_player_state(anxiety_change=3)
            $ helped_katya = False
            user_char "Извини, я не очень хороша в таких разговорах..."
            show katia speaksmile at character_scale_center
            katya "Понимаю... Извини, что отвлекла."
            show katia sad at character_scale_center
            jump after_conflict_without_help

# ============================================================================
# ПУТЬ С ЛИНОЙ (ПОСЛЕ ТОГО КАК ЛИНА РАССКАЗАЛА)
# ============================================================================
label go_to_library_with_lina:
    scene bg library with fade
    show katia sad at character_scale_center
    
    katya "Ой, вы здесь... Извините, если я выгляжу странно."
    show lina speak at character_scale_left
    e "Всё в порядке, Катя. Ты как?"
    show katia speaksmile at character_scale_center
    show lina neutral at character_scale_left
    katya "Уже лучше... Простите, что вы видели меня в таком состоянии."
    show katia smile at character_scale_center
    show lina speaksmile at character_scale_left
    user_char "Ничего страшного. Если захочешь поговорить — мы рядом."
    show katia speaksmile at character_scale_center
    show lina smile at character_scale_left
    katya "Спасибо... Вы очень добры."
    show katia smile at character_scale_center
    show lina smile at character_scale_left
    
    menu help_katya_with_lina:
        "Попробовать поговорить с Катей (помочь разобраться)":
            $ helped_katya = True
            jump talk_to_katya_with_minigame
        "Оставить Катю, пусть отдохнёт":
            $ helped_katya = False
            jump after_conflict_without_help

# ============================================================================
# ВСТРЕЧА С КАТЕЙ ПОСЛЕ КОНФЛИКТА (ЕСЛИ НЕ ПОШЛИ В БИБЛИОТЕКУ)
# ============================================================================
label meet_katya_after_conflict:
    scene bg school_entrance with fade
    show katia speak at character_scale_center
    
    katya "Ой, вы здесь... Извините, если я выгляжу странно."
    show katia neutral at character_scale_center
    show lina speak at character_scale_left
    e "Всё в порядке, Катя. Ты как?"
    show katia speaksmile at character_scale_center
    show lina sad at character_scale_left
    katya "Уже лучше... Простите, что вы видели меня в таком состоянии."
    show katia sad at character_scale_center
    show lina smile at character_scale_left
    user_char "Ничего страшного. Если захочешь поговорить — мы рядом."
    show katia speaksmile at character_scale_center
    katya "Спасибо... Вы очень добры."
    show katia smile at character_scale_center
    
    $ update_player_state(empathy_change=3, trust_change=3)
    $ heard_about_conflict = True
    
    jump after_conflict_skip_help

# ============================================================================
# ЗАВЕРШЕНИЕ КОНФЛИКТА (С ПОМОЩЬЮ)
# ============================================================================
label after_conflict_with_help:
    narrator "Разговор помог немного разрядить обстановку."
    
    if player_empathy >= 20:
        narrator "Катя немного улыбнулась и поблагодарила тебя за поддержку."
        $ update_player_state(trust_change=5)
    
    if helped_katya:
        narrator "Вы обменялись телефонами, и Катя сказала, что будет рада новой подруге."
        if not is_achievement_unlocked("new_friends"):
            $ unlock_achievement("new_friends")
    
    jump after_conflict_end

# ============================================================================
# ЗАВЕРШЕНИЕ КОНФЛИКТА (БЕЗ ПОМОЩИ)
# ============================================================================
label after_conflict_without_help:
    narrator "Ты решила не вмешиваться глубоко, но Катя всё равно оценила твоё присутствие."
    narrator "Иногда просто быть рядом — уже достаточно."
    
    jump after_conflict_end

# ============================================================================
# ЗАВЕРШЕНИЕ БЕЗ ВМЕШАТЕЛЬСТВА
# ============================================================================
label after_conflict_skip_help:
    narrator "Катя поблагодарила вас за внимание и ушла, сказав, что ей нужно побыть одной."
    
    jump after_conflict_end

# ============================================================================
# ОБЩЕЕ ЗАВЕРШЕНИЕ ГЛАВЫ 2
# ============================================================================
label after_conflict_end:
    hide katia with dissolve
    scene bg school_entrance with fade
    
    show lina smile at character_scale_left
    show alex smile at character_scale_right
    
    # --- ЛОГИКА ПОВТОРНОГО ПОСЕЩЕНИЯ МУЗЫКАЛКИ ---
    if visited_music_room and not after_music_invite_sent:
        show alex speaksmile at character_scale_right
        a "Слушайте, я как раз новую мелодию доделал. Хотите послушать?"
        show alex smile at character_scale_right

        menu repeat_music_visit:
            "С удовольствием! (Пойти в музыкалку)":
                $ after_music_invite_sent = True
                jump repeat_music_room_visit
            "В другой раз, сейчас просто погуляем":
                jump final_chapter2_scene
    elif not visited_music_room:
        show alex speaksmile at character_scale_right
        a "А вы не хотите зайти в музыкалку? Я мог бы сыграть для вас."
        show alex smile at character_scale_right

        menu first_music_suggestion:
            "Давай, сходим!":
                $ visited_music_room = True
                $ heard_alex_play = True
                jump music_room_first_visit_from_end
            "В другой раз, сейчас просто погуляем":
                jump final_chapter2_scene
    else:
        jump final_chapter2_scene

# ============================================================================
# ПОВТОРНОЕ ПОСЕЩЕНИЕ МУЗЫКАЛКИ (НОВАЯ МЕЛОДИЯ)
# ============================================================================
label repeat_music_room_visit:
    scene bg music_room with fade
    play music "song/gentle_guitar.mp3" fadein 2.0
    
    narrator "Вы снова в музыкальной комнате. Алекс берёт гитару."
    show alex speaksmile at character_scale_center
    
    a "Эта мелодия... она о том, как иногда сложно найти слова, но музыка говорит сама за себя."
    show alex speaksmile at character_scale_center
    stop music fadeout 1.0

    jump final_chapter2_scene

# ============================================================================
# ПЕРВОЕ ПОСЕЩЕНИЕ МУЗЫКАЛКИ В КОНЦЕ ГЛАВЫ
# ============================================================================
label music_room_first_visit_from_end:
    scene bg music_room with fade
    play music "song/gentle_guitar.mp3" fadein 3.0
    
    narrator "Вы заходите в музыкальную комнату. Алекс садится с гитарой."
    show alex sad at character_scale_center
    
    a "Я немного волнуюсь, но надеюсь, вам понравится."
    show alex smile at character_scale_right

    narrator "Алекс начинает играть красивую, вдохновляющую мелодию."
    narrator "Звуки гитары наполняют комнату теплом, и ты чувствуешь, как напряжение уходит."
    
    menu first_music_reaction:
        "Это потрясающе! Спасибо":
            $ update_player_state(self_awareness_change=5, anxiety_change=-5)
            user_char "Это потрясающе! Спасибо тебе."
            show alex speaksmile at character_scale_right
            a "Я очень рад, что тебе понравилось!"
            show alex smile at character_scale_right
        "Очень душевно...":
            $ update_player_state(empathy_change=5, trust_change=3)
            user_char "Очень душевно... Спасибо."
            show alex speaksmile at character_scale_right
            a "Музыка помогает мне выражать чувства. Рад, что ты это чувствуешь."
            show alex smile at character_scale_right
        "Красивая мелодия":
            $ update_player_state(vocabulary_change=3)
            user_char "Красивая мелодия."
            show alex speaksmile at character_scale_right
            a "Спасибо! Приходи ещё, у меня есть ещё несколько песен."
            show alex smile at character_scale_right
    
    jump final_chapter2_scene

# ============================================================================
# ФИНАЛЬНАЯ СЦЕНА ГЛАВЫ 2
# ============================================================================
label final_chapter2_scene:
    play music "song/school_ambient.mp3" fadein 3.0
    scene bg school_entrance with fade
    
    show lina speaksmile at character_scale_left
    show alex smile at character_scale_right
    
    e "Сегодня был отличный день! Правда, [persistent.user_name]?"
    show lina smile at character_scale_left
    show alex speaksmile at character_scale_right
    a "Да, здорово, что мы подружились."
    show alex smile at character_scale_right
    
    user_char "Мне было очень приятно провести с вами время."
    
    narrator "День подходил к концу, и ты чувствовала, как что-то внутри меняется..."
    thought_user "Сегодня я сделала первый шаг. Не знаю, правильный ли, но я попробовала."
    thought_user "Возможно, у меня получится. Возможно, я смогу научиться понимать не только других, но и себя."
    
    scene black with fade
    stop music fadeout 3.0
    show text "{size=80}Конец второй главы{/size}" with dissolve
    pause 2.0
    hide text with dissolve
    pause 0.5
    $ auto_save_chapter_complete("Глава Вторая: Новые знакомства")
    
    narrator "Глава Третья: В разработке..."
    return