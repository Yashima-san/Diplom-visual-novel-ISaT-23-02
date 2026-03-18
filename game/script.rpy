# Определения персонажей и изображений
define e = Character('Лина', color="#707ef6")
define user_char = Character("[persistent.user_name]", color="#ff9e5e")
define thought_user = Character("[persistent.user_name]", what_italic=True)
define narrator = Character(None, what_italic=True)

# Добавляем новых персонажей для второй главы
define a = Character('Алекс', color="#6b8e23")
define t = Character('Анна Сергеевна', color="#9370db")
define k = Character('Катя', color="#fe7d90")
define lib = Character('Библиотекарь', color="#a0522d")

# Определяем persistent переменные
define persistent.user_name = ""
define persistent.user_id = None
define persistent.user_data = None
default current_chapter = "Глава Первая: Связь"
default first_choice = 0
default second_choice = 0
default chapter2_choice_1 = 0
default chapter2_choice_2 = 0
default chapter2_choice_final = 0
default morning_choice = 0

# Трансформация для масштабирования
transform character_scale:
    zoom 0.4
    xalign 0.5
    yalign 1.0

# ПРАВИЛЬНОЕ объявление изображений с проверкой существования
init python:
    def safe_image(path, default=None):
        if renpy.loadable(path):
            return path
        return default

# Объявление изображений персонажей
image lina neutral = ConditionSwitch(
    "renpy.loadable('images/characters/lina_neutral.png')", "images/characters/lina_neutral.png",
    "True", "images/characters/lina.png"
)
image lina speak = ConditionSwitch(
    "renpy.loadable('images/characters/lina_speak.png')", "images/characters/lina_speak.png",
    "True", "images/characters/lina.png"
)
image lina smile = ConditionSwitch(
    "renpy.loadable('images/characters/lina_smile.png')", "images/characters/lina_smile.png",
    "True", "images/characters/lina.png"
)

image alex neutral = ConditionSwitch(
    "renpy.loadable('images/characters/alex_neutral.png')", "images/characters/alex_neutral.png",
    "True", "images/characters/alex_neutral.png"
)
image alex smile = ConditionSwitch(
    "renpy.loadable('images/characters/alex_smile.png')", "images/characters/alex_smile.png",
    "True", "images/characters/alex_neutral.png"
)

image katia neutral = ConditionSwitch(
    "renpy.loadable('images/characters/katia_neutral.png')", "images/characters/katia_neutral.png",
    "True", "images/characters/katia_neutral.png"
)
image katia smile = ConditionSwitch(
    "renpy.loadable('images/characters/katia_smile.png')", "images/characters/katia_smile.png",
    "True", "images/characters/katia_neutral.png"
)

image teacher neutral = ConditionSwitch(
    "renpy.loadable('images/characters/teacher_neutral.png')", "images/characters/teacher_neutral.png",
    "True", "images/characters/teacher_neutral.png"
)
image teacher kind = ConditionSwitch(
    "renpy.loadable('images/characters/teacher_kind.png')", "images/characters/teacher_kind.png",
    "True", "images/characters/teacher_neutral.png"
)

image librarian neutral = ConditionSwitch(
    "renpy.loadable('images/characters/librarian_neutral.png')", "images/characters/librarian_neutral.png",
    "True", "images/characters/librarian_neutral.png"
)
image librarian kind = ConditionSwitch(
    "renpy.loadable('images/characters/librarian_kind.png')", "images/characters/librarian_kind.png",
    "True", "images/characters/librarian_neutral.png"
)

# Объявление изображений фона
image bg night_room = ConditionSwitch(
    "renpy.loadable('images/night_room.png')", "images/night_room.png",
    "True", "#000000"
)
image bg room_pk = ConditionSwitch(
    "renpy.loadable('images/room_pk.png')", "images/room_pk.png",
    "True", "#2a2a2a"
)
image bg bg_room_pk_light = ConditionSwitch(
    "renpy.loadable('images/room_pk_light.png')", "images/room_pk_light.png",
    "True", "#3a3a3a"
)
image bg school_entrance = ConditionSwitch(
    "renpy.loadable('images/school_entrance.png')", "images/school_entrance.png",
    "True", "#4a4a4a"
)
image bg kitchen = ConditionSwitch(
    "renpy.loadable('images/kitchen.png')", "images/kitchen.png",
    "True", "#5a5a5a"
)
image bg street = ConditionSwitch(
    "renpy.loadable('images/street.png')", "images/street.png",
    "True", "#6a6a6a"
)
image bg school_hallway = ConditionSwitch(
    "renpy.loadable('images/school_hallway.png')", "images/school_hallway.png",
    "True", "#7a7a7a"
)
image bg classroom = ConditionSwitch(
    "renpy.loadable('images/classroom.png')", "images/classroom.png",
    "True", "#8a8a8a"
)
image bg music_room = ConditionSwitch(
    "renpy.loadable('images/music_room.png')", "images/music_room.png",
    "True", "#9a9a9a"
)
image bg library = ConditionSwitch(
    "renpy.loadable('images/library.png')", "images/library.png",
    "True", "#aaaaaa"
)

# CG-арты
image cg room_evening = ConditionSwitch(
    "renpy.loadable('images/cg/room_evening.png')", "images/cg/room_evening.png",
    "True", "#2b2b2b"
)

####################################################################################

# Единый init python блок со всеми функциями
init python:
    import time
    import json
    
    # Сохраняем оригинальных персонажей
    original_e = e
    original_user_char = user_char
    original_thought_user = thought_user
    original_a = a
    original_t = t
    original_k = k
    original_lib = lib

    # Функция для перехода к следующей главе
    def continue_to_next_chapter(old_chapter, new_chapter_title, new_chapter_subtitle):
        """Только переходит к следующей главе, без сохранения"""
        store.current_chapter = new_chapter_title
        
        if "Вторая" in new_chapter_title or "Новые знакомства" in new_chapter_title:
            if renpy.has_label("chapter_two"):
                renpy.jump("chapter_two")
            else:
                renpy.notify("Глава в разработке")
                renpy.jump("main_menu")
        elif "Третья" in new_chapter_title or "Испытание" in new_chapter_title:
            if renpy.has_label("chapter_three"):
                renpy.jump("chapter_three")
            else:
                renpy.notify("Глава в разработке")
                renpy.jump("main_menu")
        else:
            if renpy.has_label("chapter_two"):
                renpy.jump("chapter_two")
            else:
                renpy.notify("Глава в разработке")
                renpy.jump("main_menu")

    def exit_to_main_menu(old_chapter):
        """Выходит в главное меню"""
        renpy.jump("main_menu")

    def auto_save_chapter_complete(chapter_name):
        """Автоматически сохраняет прогресс при завершении главы"""
        if "Первая" in chapter_name or "Связь" in chapter_name:
            if hasattr(persistent, 'user_id') and persistent.user_id and 'db' in globals() and hasattr(db, 'update_save_progress'):
                try:
                    db.update_save_progress(persistent.user_id, chapter_name)
                except:
                    pass
            
            try:
                unlock_achievement("chapter_one_complete")
            except:
                pass
            
            try:
                renpy.take_screenshot()
                slot_name = f"chapter1-complete-{int(time.time())}"
                renpy.save(slot_name, f"Автосохранение: {chapter_name}")
                
                try:
                    save_json = renpy.json_load(renpy.slot_json_filename(slot_name))
                    if save_json is None:
                        save_json = {}
                    save_json["chapter"] = chapter_name
                    if hasattr(persistent, 'user_id') and persistent.user_id is not None:
                        save_json["user_id"] = persistent.user_id
                    if hasattr(persistent, 'user_name') and persistent.user_name:
                        save_json["user_name"] = persistent.user_name
                    save_json["_timestamp"] = time.time()
                    
                    with open(renpy.slot_json_filename(slot_name), 'w', encoding='utf-8') as f:
                        json.dump(save_json, f, ensure_ascii=False, indent=2)
                except Exception as e:
                    print(f"Ошибка при сохранении JSON: {e}")
            except:
                pass
            
            renpy.notify("Глава завершена! Прогресс сохранен.")
        
        elif "Вторая" in chapter_name or "Новые знакомства" in chapter_name:
            if hasattr(persistent, 'user_id') and persistent.user_id and 'db' in globals() and hasattr(db, 'update_save_progress'):
                try:
                    db.update_save_progress(persistent.user_id, chapter_name)
                except:
                    pass
            
            try:
                unlock_achievement("chapter_two_complete")
            except:
                pass
            
            try:
                renpy.take_screenshot()
                slot_name = f"chapter2-complete-{int(time.time())}"
                renpy.save(slot_name, f"Автосохранение: {chapter_name}")
                
                try:
                    save_json = renpy.json_load(renpy.slot_json_filename(slot_name))
                    if save_json is None:
                        save_json = {}
                    save_json["chapter"] = chapter_name
                    if hasattr(persistent, 'user_id') and persistent.user_id is not None:
                        save_json["user_id"] = persistent.user_id
                    if hasattr(persistent, 'user_name') and persistent.user_name:
                        save_json["user_name"] = persistent.user_name
                    save_json["_timestamp"] = time.time()
                    
                    with open(renpy.slot_json_filename(slot_name), 'w', encoding='utf-8') as f:
                        json.dump(save_json, f, ensure_ascii=False, indent=2)
                except Exception as e:
                    print(f"Ошибка при сохранении JSON: {e}")
            except:
                pass
            
            renpy.notify("Глава завершена! Прогресс сохранен.")
        
        else:
            renpy.notify("Глава в разработке. Прогресс не сохранен.")

    def add_user_info_to_save(json_data):
        """Добавляет информацию о пользователе в JSON сохранения"""
        try:
            user_name = ""
            if hasattr(persistent, 'user_name') and persistent.user_name:
                user_name = persistent.user_name
            json_data["user_name"] = user_name
            
            user_id = None
            if hasattr(persistent, 'user_id') and persistent.user_id is not None:
                user_id = persistent.user_id
            json_data["user_id"] = user_id
            
            json_data["chapter"] = get_current_chapter_safe()
            json_data["_timestamp"] = time.time()
        except Exception:
            json_data["chapter"] = "Глава Первая: Связь"
            json_data["_timestamp"] = time.time()
        
        return json_data
    
    if hasattr(config, 'save_json_callbacks'):
        config.save_json_callbacks = []
        config.save_json_callbacks.append(add_user_info_to_save)
    
    def continue_game():
        """Показывает экран выбора пользователя для продолжения игры"""
        renpy.show_screen("select_user_screen")
        return
    
    def custom_file_action(slot):
        """Кастомное действие для загрузки с проверкой пользователя"""
        if not renpy.can_load(str(slot)):
            renpy.notify(f"Слот {slot} пуст")
            return
        
        try:
            save_json = renpy.json_load(renpy.slot_json_filename(str(slot)))
            current_user_id = None
            if hasattr(persistent, 'user_id') and persistent.user_id is not None:
                current_user_id = persistent.user_id
                
            if save_json and save_json.get("user_id") != current_user_id and save_json.get("user_id") is not None:
                renpy.show_screen("confirm_user_switch", slot=slot)
                return
        except:
            pass
        
        renpy.run(FileAction(slot))
    
    def load_other_user_save(slot):
        """Загружает сохранение другого пользователя и обновляет persistent"""
        try:
            save_json = renpy.json_load(renpy.slot_json_filename(str(slot)))
            if save_json:
                if hasattr(persistent, 'user_id'):
                    persistent.user_id = save_json.get("user_id")
                if hasattr(persistent, 'user_name'):
                    persistent.user_name = save_json.get("user_name", "")
        except:
            pass
        
        renpy.run(FileAction(slot))

    def custom_save_action(slot):
        """Кастомное действие для сохранения с информацией о пользователе и главе"""
        try:
            current_chapter = get_current_chapter_safe()
            
            renpy.take_screenshot()
            renpy.save(str(slot), f"Сохранение в слот {slot}")
            
            save_json = renpy.json_load(renpy.slot_json_filename(str(slot)))
            if save_json is None:
                save_json = {}
            
            if hasattr(persistent, 'user_id') and persistent.user_id is not None:
                save_json["user_id"] = persistent.user_id
            else:
                save_json["user_id"] = None
                
            if hasattr(persistent, 'user_name') and persistent.user_name:
                save_json["user_name"] = persistent.user_name
            else:
                save_json["user_name"] = ""
                
            save_json["chapter"] = current_chapter
            save_json["_timestamp"] = time.time()
            
            with open(renpy.slot_json_filename(str(slot)), 'w', encoding='utf-8') as f:
                json.dump(save_json, f, ensure_ascii=False, indent=2)
            
            if persistent.user_id and 'db' in globals() and hasattr(db, 'update_save_progress'):
                try:
                    db.update_save_progress(persistent.user_id, current_chapter)
                except:
                    pass
            
            renpy.notify(f"Игра сохранена в слот {slot}")
            
        except Exception as e:
            renpy.notify(f"Ошибка при сохранении: {str(e)}")
            print(f"Ошибка в custom_save_action: {e}")
    
    def load_last_save_for_user(user_id):
        """Загружает последнее сохранение для указанного пользователя"""
        saves = []
        
        try:
            all_slots = []
            for i in range(1, 10):
                all_slots.append(str(i))
            for i in range(1, 10):
                all_slots.append(f"auto-{i}")
            all_slots.append("quick-save")
            
            for slot_name in all_slots:
                if renpy.can_load(slot_name):
                    try:
                        save_json = renpy.json_load(renpy.slot_json_filename(slot_name))
                        if save_json and save_json.get("user_id") == user_id:
                            timestamp = save_json.get("_timestamp", 0)
                            saves.append((slot_name, timestamp))
                    except:
                        continue
        except Exception as e:
            print(f"Ошибка при поиске сохранений: {e}")
        
        saves.sort(key=lambda x: x[1], reverse=True)
        
        if saves:
            try:
                renpy.load(str(saves[0][0]))
                return True
            except Exception as e:
                print(f"Ошибка при загрузке: {e}")
                return False
        return False
    
    def get_current_chapter_safe():
        """Безопасно определяет текущую главу"""
        try:
            if hasattr(store, 'current_chapter') and store.current_chapter:
                return store.current_chapter
        except:
            pass
        
        return "Глава Первая: Связь"
    
    def set_current_user(user_id, user_name):
        """Установка текущего пользователя"""
        if hasattr(persistent, 'user_id'):
            persistent.user_id = user_id
        if hasattr(persistent, 'user_name'):
            persistent.user_name = user_name
        renpy.notify(f"Выбран игрок: {user_name}")

    # Глобальные callback-функции для чата
    def first_choice_callback(choice_text):
        global first_choice
        if "Привет! Да, готова" in choice_text:
            first_choice = 1
            unlock_achievement("first_choice")
        elif "Привет! Я тоже очень рада" in choice_text:
            first_choice = 2
            unlock_achievement("first_choice")
        elif "Привет! Я очень рада" in choice_text:
            first_choice = 3
            unlock_achievement("first_choice")
        
        renpy.jump("continue_chat_after_first")
    
    def second_choice_callback(choice_text):
        global second_choice
        if "Звучит здорово! Я согласна" in choice_text:
            second_choice = 11
        elif "Давай сначала посмотрим" in choice_text:
            second_choice = 12
        elif "Звучит здорово! Библиотека" in choice_text:
            second_choice = 21
        elif "Спасибо, Лина" in choice_text and "буду просто наблюдать" in choice_text:
            second_choice = 22
        elif "Спасибо, Лина! Ты лучшая!" in choice_text:
            second_choice = 31
        elif "Спасибо, Лина! Я очень ценю твою дружбу" in choice_text:
            second_choice = 32
        
        renpy.jump("end_chat_scene")
    
    def morning_choice_callback(choice_text):
        global morning_choice
        if "Спасибо, Лина! Я уже встаю" in choice_text:
            morning_choice = 1
        elif "Я тоже волнуюсь" in choice_text:
            morning_choice = 2
        elif "Увидимся у входа" in choice_text:
            morning_choice = 3
        
        renpy.jump("continue_morning")


################################################################################
## Глава Первая: Связь
################################################################################

label start:
    # Устанавливаем текущую главу для безопасного определения
    $ current_chapter = "Глава Первая: Связь"
    
    # Устанавливаем музыку главного меню
    play music config.main_menu_music fadein 5.0
    $ renpy.music.set_volume(0.1, delay=0)
    
    # Вызов экрана и получение имени
    $ entered_name = renpy.call_screen("input_name_screen")
    
    # Обработка введенного имени
    if entered_name is None or entered_name.strip() == "":
        $ player_name = "Настя"
    else:
        $ player_name = entered_name.strip()
    
    # Сохраняем имя в persistent для использования во всех персонажах
    $ persistent.user_name = player_name
    
    # Сохраняем имя пользователя в базу данных
    $ user_id = db.add_user(player_name) if 'db' in globals() and hasattr(db, 'add_user') else None
    
    # Сохраняем user_id в persistent
    $ persistent.user_id = user_id
    
    "Ты ничего не забыла, [persistent.user_name]?"
    "Пора просыпаться..."
    
    # Показываем заголовок главы
    scene black with fade
    show text "{size=80}Глава Первая{/size}\n{size=60}Связь{/size}" with dissolve
    pause 3.0
    scene black with dissolve

    # Обновляем прогресс в базе данных
    if persistent.user_id and 'db' in globals() and hasattr(db, 'update_save_progress'):
        $ db.update_save_progress(persistent.user_id, "Глава Первая: Связь")
    
    # Разблокировка первого достижения
    $ unlock_achievement("wake_up")
    
    # Разблокировка элементов галереи (CG-арт для вечерней комнаты)
    $ unlock_gallery_item("room_evening")

    # Показываем CG-арт (вечер)
    scene cg room_evening at truecenter with fade

    # Старт музыки
    stop music
    play music "song/Audio_soft_1.mp3" fadein 5.0
    $ renpy.music.set_volume(0.5, delay=5)

    # Повествование
    narrator "Солнечные лучи, пробиваясь сквозь неплотно задернутые шторы, рисовали на полу комнаты девочки причудливые узоры."
    narrator "Пылинки, словно крошечные танцоры, кружились в золотистых столбах света, создавая атмосферу умиротворения, которая, однако, не проникала в душу юной обитательницы этого пространства."
    narrator "Комната, аккуратно обставленная, но лишенная ярких акцентов, отражала ее внутренний мир – упорядоченный, но безжизненный."
    narrator "На столе, заваленном учебниками и тетрадями, стоял старенький ноутбук, его экран тускло мерцал, словно отражая невысказанные мысли."

    thought_user "Вечер... слишком долго спала...{p}Впрочем, как и всегда."
    thought_user "Не понимаю, почему люди так радуются щебетанию птиц. Это просто… звук. Как и все остальное."
    thought_user "Чувства. Эмоции. Слова, которые я слышу постоянно, но для меня – лишь набор звуков, лишенных смысла."
    thought_user "Алекситимия. Это слово, которое мне сказала врач, когда я проходила повторную комиссию в больнице.{p}Оно звучит так… официально. Как диагноз. Как приговор."
    thought_user "Родители, конечно, не поняли. Они и раньше не понимали. Я для них – просто ребенок, который должен учиться и вести себя хорошо."
    thought_user "А как вести себя хорошо, когда ты не понимаешь, что чувствуют другие?{p}Когда их улыбки кажутся мне масками, а слезы – просто мокрыми пятнами на лице?"

    show bg bg_room_pk_light with dissolve
    $ unlock_gallery_item("room_pk_light")

    narrator "На стене висел постер с изображением какого-то аниме-персонажа, его глаза, широко распахнутые, казалось, смотрели куда-то вдаль, в мир, полный ярких красок и бурных эмоций."
    narrator "[persistent.user_name] часто смотрела на него, пытаясь уловить хоть что-то, что могло бы помочь ей понять."
    narrator "Но даже в этом вымышленном мире, где все было преувеличено и гиперболизировано, она чувствовала себя чужой."

    thought_user "Я помню, как в детстве пыталась плакать, когда мне было больно."
    thought_user "Но слезы не шли.{p}Я просто чувствовала пустоту."
    thought_user "Родители говорили, что я просто капризничаю. Они не знали, что я не знаю, как это – чувствовать."
    thought_user "Я научилась имитировать. Улыбаться, когда нужно, кивать, когда говорят что-то важное.{p}Но внутри – ничего. Только тишина."
    thought_user "И эта тишина пугает меня больше всего. Она как бездна, в которую я могу упасть в любой момент."

    narrator "В углу комнаты стоял старый плюшевый медведь, его мех был истерт от бесчисленных объятий, которых он так и не получил."
    narrator "Он был единственным свидетелем ее детских игр, ее молчаливым слушателем."

    thought_user "Единственный, кто меня понимает – это моя интернет-подруга, Лина."

    thought_user "Мы познакомились в игре. Она рассказывала мне о своих проблемах, о своих радостях. Я слушала, пыталась что-то ответить. Иногда мне казалось, что я понимаю ее."
    thought_user "Но потом я вспоминала, что это лишь слова. Я не могла почувствовать ее боль или ее счастье."
    thought_user "Я просто анализировала информацию."
    thought_user "Лина – единственная, кто не считает меня странной. Или, может быть, считает, но ей все равно."
    thought_user "Она говорит, что я – особенная. Но я не хочу быть особенной."
    thought_user "Я хочу быть нормальной."
    thought_user "Хочу понимать, что происходит вокруг меня."

    narrator "На экране ноутбука появилось уведомление. Новое сообщение от Лины."
    narrator "[persistent.user_name] лениво начала подниматься со своей нагретой кровати и подошла ко столу, на котором находился ноутбук."
    narrator "Она медленно протянула руку к мышке, ее пальцы дрожали от легкого волнения."

    show bg room_pk with dissolve
    $ unlock_gallery_item("room_pk")

    thought_user "Новая школа. Новые люди. Родители думают, что это поможет. Может быть. Там учится Лина. Это хорошо. Хоть кто-то знакомый."
    thought_user "...Но… что, если я опять не смогу? Что, если я опять буду стоять в стороне, наблюдая, как другие смеются, общаются, живут? Я боюсь…"
    thought_user "Боюсь не справиться."
    thought_user "Боюсь снова почувствовать эту пустоту, когда все вокруг будут казаться мне чужими."
    thought_user "Но я должна."
    thought_user "Я должна попытаться. Я должна научиться понимать. И я должна встретиться со своими страхами. Даже если они кажутся мне такими же пустыми, как и я сама."

    narrator "[persistent.user_name] открыла окно чата."
    narrator "На экране появилось приветствие от Лины, яркое и жизнерадостное, словно солнечный луч, пробившийся сквозь тучи."

    # Включаем режим чата для этой сцены
    $ enable_chat_mode()

    # Лина отправляет сообщение
    $ e("Привет! Ты уже готова к завтрашнему дню? Я так рада, что мы теперь будем учиться вместе! 🥳 Я уже придумала, как мы будем проводить перемены! ✨✨✨")

    narrator "Слова Лины, написанные с такой непринужденной легкостью, казались [persistent.user_name] одновременно и утешительными, и пугающими."
    narrator "Радость Лины была искренней, это было видно даже по смайликам, которые она использовала."

    thought_user "Я хочу ответить ей также жизнерадостно.. Но у меня не получается. Мои пальцы замирают над клавишами."
    thought_user "Что я могу сказать?"

    # Показываем варианты ответа в чате
    $ show_chat_choices([
        "Привет! Да, готова. Уже жду не дождусь! 😊",
        "Привет! Я тоже очень рада! Немного волнуюсь, но уверена, что с тобой будет весело! 😊",
        "Привет! Я очень рада, что мы будем учиться вместе. Я немного волнуюсь, потому что это новая школа, но я уверена, что с тобой мне будет легче. Ты – мой самый лучший друг. ❤️"
    ], first_choice_callback)
    
    $ renpy.pause(None)

label continue_chat_after_first:
    if first_choice == 1:
        $ e("Ура! Я так рада!")
        $ e("Я уже придумала, что мы можем пойти в кафе после уроков, если захочешь! Или в парк! Что скажешь?")
        
        $ show_chat_choices([
            "Звучит здорово! Я согласна на все!",
            "Давай сначала посмотрим, как пройдет день. Я немного устала сегодня."
        ], second_choice_callback)
        $ renpy.pause(None)
    
    elif first_choice == 2:
        $ e("Ой, я понимаю! Но не переживай! Мы же вместе!")
        $ e("Я придумала, что мы можем ходить в библиотеку, там так тихо и уютно! Ты как?")
        
        $ show_chat_choices([
            "Звучит здорово! Библиотека – отличная идея!",
            "Спасибо, Лина! Я, наверное, пока буду просто наблюдать."
        ], second_choice_callback)
        $ renpy.pause(None)
    
    elif first_choice == 3:
        $ e("Ой, [persistent.user_name]! 🥺 Я так тронута!")
        $ e("Я тоже очень рада, что мы будем вместе! И ты не волнуйся, я буду рядом!")
        
        $ show_chat_choices([
            "Спасибо, Лина! Ты лучшая! Я уже чувствую себя спокойнее.",
            "Спасибо, Лина! Я очень ценю твою дружбу."
        ], second_choice_callback)
        $ renpy.pause(None)
    
    return

label end_chat_scene:
    $ disable_chat_mode()
    jump night_scene

label night_scene:
    stop music
    scene bg night_room with fade
    play sound "song/night_ambient.mp3" fadein 3.0
    
    narrator "Ночь опустилась на город мягко, как шелковое одеяло."
    narrator "[persistent.user_name] лежала в постели, уставившись в потолок, где плясали тени от уличного фонаря."
    narrator "Сообщения Лины все еще крутились в голове, теплые и поддерживающие."
    
    thought_user "Завтрашний день в новой школе… Это не просто новый этап — это будет прыжок в неизвестность, где моя тревога может либо раствориться в дружбе с Линой, либо накрыть с головой."
    
    thought_user "Хотя… может, стоит прямо сейчас чем-то заняться? Отвлечься от этих мыслей."
    thought_user "Психолог говорила, что важно анализировать свои состояния. Дала то самое задание — расширять эмоциональный словарь."
    
    narrator "[persistent.user_name] села на кровати и посмотрела на стол, где лежала распечатанная таблица чувств."
    
    thought_user "«Колесо эмоций» Роберта Плутчика. Нужно носить с собой и в моменты дискомфорта пытаться подобрать точное слово."
    thought_user "Может, попробовать прямо сейчас? Описать то, что я чувствую перед завтрашним днём..."
    
    narrator "Она подошла к столу, включила настольную лампу и взяла в руки таблицу с разноцветным кругом, разделённым на множество сегментов."
    
    show table_emotions at truecenter with dissolve
    $ renpy.pause(2.0)
    hide table_emotions with dissolve
    
    thought_user "В центре — базовые эмоции: радость, доверие, страх, удивление, печаль, отвращение, гнев, предвкушение."
    thought_user "А дальше — оттенки. Например, страх может переходить в тревогу, беспокойство, робость…"
    
    
    # Мини-игра: выбор эмоции
    call screen emotion_selection
    
    # После выбора продолжаем
    if _return:
        $ selected_emotion = _return[0]
        $ emotion_description = _return[1]
        
        thought_user "[selected_emotion]... Да, пожалуй, это самое точное слово."
        thought_user "[emotion_description]"
        
        if selected_emotion == "Тревога":
            $ unlock_achievement("emotion_treasure_hunter")
            thought_user "Интересно, получается, я смогла определить своё состояние. Может, это задание действительно работает?"
        elif selected_emotion == "Страх":
            $ unlock_achievement("emotion_pioneer")
            thought_user "Страх — это нормально, говорила психолог. Главное — не позволять ему парализовать тебя."
        elif selected_emotion == "Предвкушение":
            $ unlock_achievement("emotion_explorer")
            thought_user "Предвкушение… Оно больше похоже на смесь радости и надежды. Может, я действительно жду чего-то хорошего?"
        elif selected_emotion == "Надежда":
            $ unlock_achievement("emotion_seeker")
            thought_user "Надежда. Тёплое слово. Может, не всё так плохо?"
        else:
            $ unlock_achievement("emotion_beginner")
            thought_user "Записала в дневник наблюдений. Завтра расскажу психологу."
    
    thought_user "Засыпая, [persistent.user_name] думала только об одном…"
    thought_user "Завтрашний день в новой школе… Это не просто новый этап — это будет прыжок в неизвестность, где моя тревога может либо раствориться в дружбе с Линой, либо накрыть с головой."
    
    stop sound fadeout 3.0
    scene black with fade
    pause 1.0

label morning_scene:
    stop music
    scene cg room_evening with fade
    play music "song/Audio_soft_1.mp3" fadein 3.0
    
    narrator "Утро пришло слишком быстро. Солнце пробивалось сквозь шторы, окрашивая комнату в золотистый свет."
    narrator "[persistent.user_name] проснулась с тяжелым сердцем, но с решимостью. Она села на кровати, потянулась и бросила взгляд на телефон."

    $ enable_chat_mode()
    
    $ e("Доброе утро, [persistent.user_name]! 🌅")
    $ e("Уже проснулась? Я сейчас собираюсь в школу и так волнуюсь за тебя! 🥺")
    $ e("Не забудь взять тетради и хорошее настроение 😘")
    
    thought_user "Ее энтузиазм заразителен... Может, и мне удастся почувствовать то же самое? Я не хочу подвести ее."
    
    $ show_chat_choices([
        "Спасибо, Лина! Я уже встаю. Увидимся у входа! ❤️",
        "Я тоже волнуюсь... Но спасибо, что ты рядом!",
        "Увидимся у входа в школу! Я постараюсь не опоздать 😊"
    ], morning_choice_callback)
    
    $ renpy.pause(None)

label continue_morning:
    $ disable_chat_mode()
    
    narrator "[persistent.user_name] улыбнулась, чувствуя себя немного увереннее."
    
    narrator "[persistent.user_name] улыбнулась уголком губ и начала собираться."
    narrator "Комната, обычно такая уютная, теперь казалась полем битвы: рюкзак валялся на полу, полный случайных вещей — старых учебников из прошлой школы, пачки карандашей и даже любимой записной книжки, куда она иногда черкала свои мысли."
    narrator "Она методично складывала все необходимое: свежие тетради, ручки, бутылку воды."
    narrator "Руки слегка дрожали, когда она выбирала одежду — простую голубую рубашку с короткими рукавами, синюю теннисную юбку и черные колготки, ничего вычурного, чтобы не привлекать лишнего внимания."
    narrator "В зеркале отразилось ее лицо: бледное, с легкими тенями под глазами от бессонной ночи. [persistent.user_name] прошептала себе, поправляя волосы."

    thought_user "Ты справишься!"
    thought_user "По крайней мере я на это очень сильно надеюсь… Сомнений у меня как всегда очень много…"

    scene bg kitchen with fade
    
    narrator "Спустившись на кухню, [persistent.user_name] увидела на столе тарелку с бутербродами, накрытую пищевой пленкой."
    narrator "Рядом стояла кружка с недопитым чаем и лежала записка, приклеенная к холодильнику ярким магнитом в виде яблока."

    narrator "\"Дорогая, мы с папой уехали рано. Завтрак на столе. Удачи в новой школе! Мы в тебя верим!\""

    thought_user "Как всегда, коротко и по делу. Но, наверное, это и есть их способ показать заботу…."

    narrator "[persistent.user_name] взяла один бутерброд и откусила маленький кусочек. Аппетита не было совсем. Она допила чай, стараясь не думать о том, что ее ждет."
    narrator "Вздохнув, она взяла рюкзак и вышла из дома. Новый день, новая школа, новая жизнь."

    scene bg street with fade
    play sound "song/footsteps.mp3" fadein 2.0
    
    narrator "Воздух был свежим, с легким запахом росы и еще не растаявшего ночного холодка. Улица, обычно оживленная, сейчас была почти пуста, лишь редкие прохожие спешили по своим делам."
    narrator "Каждый шаг [persistent.user_name] отдавался эхом в тишине, подчеркивая ее одиночество."
    narrator "Она шла, стараясь дышать ровно, но грудь сжималась от предвкушения."
    narrator "Школа виднелась вдалеке, большое, незнакомое здание, которое казалось одновременно манящим и пугающим."

    thought_user "Вот оно."
    thought_user "Сердце колотится как сумасшедшее."
    thought_user "Лина сказала, что будет ждать у входа. Надеюсь, я ее узнаю. Или она меня."
    thought_user "Как же глупо я себя чувствую, так волноваться из-за встречи с подругой…"

    scene bg school_entrance with fade
    stop sound fadeout 2.0
    play sound "song/school_ambient.mp3" fadein 3.0
    
    narrator "Подойдя ближе, [persistent.user_name] увидела у массивных дверей школы несколько учеников. Они смеялись, разговаривали, казались такими уверенными в себе."
    narrator "[persistent.user_name] замедлила шаг, пытаясь разглядеть среди них знакомое лицо. И вдруг она увидела ее."
    narrator "Лина, с яркой улыбкой и развевающимися на ветру волосами, махала ей рукой."

    thought_user "Она здесь. И она меня видит. Это уже что-то."

    narrator "[persistent.user_name] почувствовала, как напряжение немного отступает. Она ускорила шаг, направляясь к Лине."

    show lina speak at center with dissolve
    e "[persistent.user_name]! Привет!"
    e "Я так рада тебя видеть! Ты не опоздала ни на секунду!"

    narrator "Лина обняла [persistent.user_name] крепко, словно старую подругу. Это объятие было таким искренним и теплым, что [persistent.user_name] почувствовала, как последние остатки страха начинают таять."

    thought_user "Привет… я тебя тоже рада видеть.."
    thought_user "Она настоящая. И она меня приняла. Может, этот прыжок в неизвестность не так уж и страшен."

    narrator "Они стояли так несколько мгновений, а затем Лина отстранилась, ее глаза сияли."

    e "Ну что, готова к первому дню? Я тебе все покажу! И познакомлю с моими друзьями."
    e "Они такие же сумасшедшие, как и я, так что не бойся!"
    hide lina

    narrator "[persistent.user_name] посмотрела на Лину и заторможенно кивнула."
    thought_user "Возможно, сегодняшний день действительно станет не прыжком в неизвестность, а шагом навстречу чему-то новому и хорошему."

    thought_user "Я справлюсь. Когда Лина рядом со мной…"

    play sound "song/school_bell.mp3"
    pause 2.0
    
    narrator "Прозвенел школьный звонок, призывая учеников на первый урок."
    narrator "Голоса учеников нарастали, заполняя школьный двор."
    narrator "Лина взяла [persistent.user_name] за руку и повела к входу."

    scene black with fade
    stop sound fadeout 3.0
    stop music fadeout 3.0
    
    show text "{size=80}Конец первой главы{/size}" with dissolve
    pause 2.0
    hide text with dissolve
    pause 0.5
    
    $ auto_save_chapter_complete("Глава Первая: Связь")
    
    $ result = renpy.call_screen("chapter_transition", "Глава Первая: Связь", "Глава Вторая: Новые знакомства", "Новые знакомства")
    
    if result[0] == "continue":
        $ continue_to_next_chapter(result[1], result[2], result[3])
    else:
        $ exit_to_main_menu(result[1])
    
    return


################################################################################
## Глава Вторая: Новые знакомства
################################################################################

label chapter_two:
    $ current_chapter = "Глава Вторая: Новые знакомства"
    
    scene black with fade
    show text "{size=80}Глава Вторая{/size}\n{size=60}Новые знакомства{/size}" with dissolve
    pause 3.0
    scene black with dissolve
    
    if persistent.user_id and 'db' in globals() and hasattr(db, 'update_save_progress'):
        $ db.update_save_progress(persistent.user_id, "Глава Вторая: Новые знакомства")
    
    play music "song/Audio_soft_2.mp3" fadein 5.0
    $ renpy.music.set_volume(0.4, delay=5)
    
    scene bg school_entrance with fade
    play sound "song/school_ambient.mp3" fadein 3.0
    
    narrator "Лина уверенно вела [persistent.user_name] по длинным школьным коридорам."
    narrator "Стены были увешаны яркими плакатами, объявлениями о кружках и секциях, фотографиями улыбающихся учеников."
    narrator "[persistent.user_name] чувствовала, как на нее обрушивается калейдоскоп новых впечатлений."
    
    thought_user "Здесь так шумно... Столько людей. Как Лина может ориентироваться во всем этом?"
    
    e "Смотри, это наша раздевалка! А тут спортзал. О, а вот и столовая, здесь готовят потрясающие булочки с корицей!"
    
    narrator "Лина тараторила без остановки, показывая все уголки школы."
    narrator "Вдруг из-за угла выскочил парень с взъерошенными волосами и чуть не сбил их с ног."
    
    show alex smile at center with dissolve
    
    narrator "Он ловко увернулся и улыбнулся."
    
    a "Ой, простите! Я совсем вас не заметил. Вы новенькая?"
    
    narrator "Парень с любопытством посмотрел на [persistent.user_name]."
    
    thought_user "Он обращается ко мне? Что ответить?"
    
    menu second_chapter_first_choice:
        "Да, я сегодня первый день. Приятно познакомиться.":
            $ chapter2_choice_1 = 1
            $ unlock_achievement("sociable_choice")
            user_char "Да, я сегодня первый день. Приятно познакомиться."
            
        "Эм... да. Я новенькая.":
            $ chapter2_choice_1 = 2
            $ unlock_achievement("shy_choice")
            user_char "Эм... да. Я новенькая."
        
        "Просто молча кивнуть":
            $ chapter2_choice_1 = 3
            $ unlock_achievement("balanced_choice")
            narrator "[persistent.user_name] просто молча кивнула."
    
    a "Класс! Я Алекс. Если что-то нужно будет — обращайся. Я здесь уже второй год, все знаю!"
    $ unlock_achievement("meet_alex")

    show lina speak at left with move
    show alex smile at right
    
    e "Алекс — наш школьный активист! Он во всех мероприятиях участвует. А еще играет на гитаре."
    
    a "Лина, ну зачем ты сразу все секреты выдаешь?"
    
    narrator "Алекс засмеялся, и [persistent.user_name] почувствовала, как напряжение потихоньку отпускает."
    
    a "Слушай, а вы на большую перемену в музыкалку не хотите сходить? Мы там с ребятами репетируем. Будет весело!"
    
    thought_user "Музыка... Я никогда особо не слушала музыку. Но Лина, кажется, заинтересовалась."
    
    e "Ой, можно? Я давно хотела послушать, как вы играете!"
    
    narrator "Лина вопросительно посмотрела на [persistent.user_name]."
    
    menu second_chapter_second_choice:
        "Давай сходим. Интересно посмотреть.":
            $ chapter2_choice_2 = 1
            user_char "Давай сходим. Интересно посмотреть."
            
        "Не знаю... Я не очень люблю шумные компании.":
            $ chapter2_choice_2 = 2
            user_char "Не знаю... Я не очень люблю шумные компании."
        
        "Если Лина хочет, то я тоже пойду.":
            $ chapter2_choice_2 = 3
            user_char "Если Лина хочет, то я тоже пойду."
    
    if chapter2_choice_2 == 2:
        e "Ну хотя бы на пару минут заглянем? Если не понравится — сразу уйдем, обещаю!"
        narrator "Лина мягко, но настойчиво уговаривала подругу."
        narrator "[persistent.user_name] вздохнула."
        user_char "Ладно, уговорила. Ненадолго."
    else:
        a "Отлично! Тогда жду вас после третьего урока. Актовый зал, не забудьте!"
    
    hide alex
    hide lina
    
    narrator "Прозвенел звонок на урок, и Лина с [persistent.user_name] поспешили в класс."
    
    scene bg classroom with fade
    
    narrator "Класс был светлым и просторным. Ученики уже рассаживались по местам, приветствуя друг друга."
    narrator "Учительница, женщина средних лет с добрыми глазами, жестом пригласила всех сесть."
    
    show teacher kind at center with dissolve
    
    t "Ребята, сегодня у нас новая ученица. Представься, пожалуйста."
    $ unlock_achievement("meet_teacher")

    narrator "Все взгляды устремились на [persistent.user_name]. Она почувствовала, как щеки заливает румянец."
    
    thought_user "Так, спокойно. Я же готовилась к этому."
    
    user_char "Меня зовут [persistent.user_name]. Я... я надеюсь, мы подружимся."
    
    narrator "Кто-то из ребят одобрительно кивнул, кто-то улыбнулся. Одна девочка на последней парте с интересом рассматривала новенькую."
    
    t "Садись, [persistent.user_name]. А ты, Катя, покажешь нашей новой ученице, как у нас все устроено, хорошо?"
    
    show katia smile at left with moveinleft
    
    k "Конечно, Анна Сергеевна!"
    $ unlock_achievement("meet_katya")

    hide teacher
    
    narrator "Катя помахала [persistent.user_name] рукой, приглашая сесть рядом."
    narrator "[persistent.user_name] осторожно опустилась на стул, чувствуя, как внутри смешиваются страх и любопытство."
    
    thought_user "Катя... Она кажется дружелюбной. Может, сегодня не такой уж плохой день?"
    
    play sound "song/school_bell.mp3"
    pause 1.0
    
    scene bg school_entrance with fade
    
    narrator "Первая перемена пролетела незаметно. Катя оказалась очень разговорчивой и рассказывала о всех учителях и школьных традициях."
    
    show katia speak at left
    show lina smile at right
    
    k "А еще у нас есть театральный кружок! Я там состою. Если хочешь, приходи посмотреть!"
    
    e "Ой, точно! [persistent.user_name], это же отличная идея! Ты ведь любишь читать, может, и играть понравится?"
    
    thought_user "Играть? На сцене? Перед всеми? Это звучит пугающе... но и заманчиво одновременно."
    
    narrator "К ним подошел Алекс."
    
    show alex smile at center
    
    a "Ну что, идете? Перемена большая, самое время для музыки!"
    
    menu second_chapter_final_choice:
        "Идем! Я хочу послушать.":
            $ chapter2_choice_final = 1
            user_char "Идем! Я хочу послушать."
            jump music_room_scene
            
        "Может, в другой раз? Я немного устала.":
            $ chapter2_choice_final = 2
            user_char "Может, в другой раз? Я немного устала."
            jump library_scene
        
        "А можно мы с Катей тоже придем?":
            $ chapter2_choice_final = 3
            user_char "А можно мы с Катей тоже придем?"
            k "Ой, а можно? Я тоже очень хочу!"
            a "Конечно! Чем больше, тем веселее!"
            jump music_room_scene

label music_room_scene:
    hide alex
    hide katia
    hide lina
    
    scene bg music_room with fade
    play music "song/gentle_guitar.mp3" fadein 3.0
    $ unlock_achievement("music_room_visit")

    narrator "Актовый зал оказался уютным помещением с мягкими креслами и стареньким пианино в углу."
    narrator "Несколько ребят уже настраивали инструменты. Алекс взял гитару и улыбнулся."
    
    show alex smile at center with dissolve
    a "Мы сейчас разучиваем новую песню. Хотите послушать?"
    hide alex
    
    narrator "[persistent.user_name] кивнула, чувствуя, как музыка начинает заполнять пространство."
    narrator "Мелодия была простой, но в ней чувствовалось что-то теплое и искреннее."
    
    thought_user "Музыка... Оказывается, она может передавать чувства без слов. Это удивительно."
    
    show lina speak at center with dissolve
    e "Тебе нравится, [persistent.user_name]?"

    show lina smile at center with dissolve

    user_char "Да... очень. Это... это красиво."
    
    narrator "Алекс довольно улыбнулся и продолжил играть."
    narrator "В этот момент [persistent.user_name] поняла, что, возможно, мир эмоций не так уж недоступен для нее."
    narrator "Нужно просто найти правильный ключ."
    hide lina
    
    jump chapter_two_end

label library_scene:
    hide alex
    hide katia
    hide lina
    
    scene bg library with fade
    $ unlock_achievement("library_visit")
    
    narrator "Пока остальные пошли в актовый зал, [persistent.user_name] направилась в библиотеку."
    narrator "Здесь было тихо и спокойно, пахло старыми книгами и уютом."
    
    show librarian kind at center with dissolve
    
    lib "Здравствуй, дорогая! Ты новенькая? Хочешь что-то почитать?"
    $ unlock_achievement("meet_librarian")

    thought_user "Библиотека... Здесь мне спокойно. Никто не требует быть общительной."
    
    user_char "Здравствуйте. Да, я бы хотела... может, что-то поспокойнее?"
    
    lib "О, тогда тебе точно понравится этот сборник рассказов о природе. Очень умиротворяющее чтение."
    hide librarian
    
    narrator "[persistent.user_name] взяла книгу и устроилась в уютном кресле у окна."
    narrator "Тишина обволакивала, давая возможность побыть наедине со своими мыслями."
    
    thought_user "Может, иногда лучше быть одной, чем чувствовать себя чужой в компании? Хотя... Лина и Катя... С ними, кажется, можно попробовать."
    $ unlock_achievement("new_friends")
    
    jump chapter_two_end

label chapter_two_end:
    scene black with fade
    stop music fadeout 3.0
    stop sound fadeout 3.0
    
    show text "{size=80}Конец второй главы{/size}" with dissolve
    pause 2.0
    hide text with dissolve
    pause 0.5
    
    $ auto_save_chapter_complete("Глава Вторая: Новые знакомства")
    
    if persistent.user_id and 'db' in globals() and hasattr(db, 'update_save_progress'):
        $ db.update_save_progress(persistent.user_id, "Глава Вторая: Новые знакомства")
    
    $ result = renpy.call_screen("chapter_transition", "Глава Вторая: Новые знакомства", "Глава Третья: Испытание дружбой", "Испытание дружбой")
    
    if result[0] == "continue":
        $ continue_to_next_chapter(result[1], result[2], result[3])
    else:
        $ exit_to_main_menu(result[1])
    
    return


label chapter_three:
    $ current_chapter = "Глава Третья: Испытание дружбой"
    
    scene black with fade
    show text "{size=80}Глава Третья{/size}\n{size=60}Испытание дружбой{/size}" with dissolve
    pause 3.0
    scene black with dissolve
    
    "Глава в разработке"
    
    return