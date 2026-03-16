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
default current_chapter = "Глава Первая: Связь"  # Глобальная переменная для главы

# Объявление изображений персонажей
image lina neutral = "images/characters/lina.png"
image lina happy = "images/characters/lina_happy.png"
image lina smile = "images/characters/lina_smile.png"

image alex neutral = "images/characters/alex.png"
image alex smile = "images/characters/alex_smile.png"

image katia neutral = "images/characters/katia.png"
image katia smile = "images/characters/katia_smile.png"

image teacher neutral = "images/characters/teacher.png"
image teacher kind = "images/characters/teacher_kind.png"

image librarian neutral = "images/characters/librarian.png"
image librarian kind = "images/characters/librarian_kind.png"

# Объявление изображений фона
image bg room_evening = "images/room_evening.png"
image bg night_room = "images/night_room.png"
image bg room_pk = "images/room_pk.png"
image bg bg_room_pk_light = "images/room_pk_light.png"
image bg school_entrance = "images/school_entrance.png"
image bg kitchen = "images/kitchen.png"
image bg street = "images/street.png"
image bg school_hallway = "images/school_hallway.png"
image bg classroom = "images/classroom.png"
image bg music_room = "images/music_room.png"
image bg library = "images/library.png"


# Единый init python блок со всеми функциями
init python:
    import time
    import json

        # Функция для автоматического сохранения при завершении главы
    def auto_save_chapter_complete(chapter_name):
        """Автоматически сохраняет прогресс при завершении главы"""
        if hasattr(persistent, 'user_id') and persistent.user_id and 'db' in globals() and hasattr(db, 'update_save_progress'):
            try:
                db.update_save_progress(persistent.user_id, chapter_name)
            except:
                pass
        
        # Разблокируем достижение за прохождение главы
        try:
            if "Первая" in chapter_name or "Связь" in chapter_name:
                if 'unlock_achievement' in globals():
                    unlock_achievement("chapter_one_complete")
            elif "Вторая" in chapter_name or "Новые знакомства" in chapter_name:
                if 'unlock_achievement' in globals():
                    unlock_achievement("chapter_two_complete")
        except:
            pass
        
        # Делаем скриншот и сохраняем
        try:
            renpy.take_screenshot()
            slot_name = f"chapter-complete-{int(time.time())}"
            renpy.save(slot_name, f"Автосохранение: {chapter_name}")
            
            # Обновляем JSON с информацией о главе
            try:
                import json
                save_json = renpy.json_load(renpy.slot_json_filename(slot_name))
                if save_json:
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
        
        renpy.notify(f"Глава завершена! Прогресс сохранен.")
    
    # Функция для перехода к следующей главе (БЕЗ СОХРАНЕНИЯ)
    def continue_to_next_chapter(old_chapter, new_chapter_title, new_chapter_subtitle):
        """Только переходит к следующей главе, без сохранения (сохранение уже сделано)"""
        renpy.notify("Загружаем следующую главу...")
        
        # Обновляем текущую главу
        store.current_chapter = new_chapter_title
        
        # Определяем, на какую главу переходить
        if "Вторая" in new_chapter_title or "Новые знакомства" in new_chapter_title:
            # Проверяем, существует ли метка chapter_two
            if renpy.has_label("chapter_two"):
                renpy.jump("chapter_two")
            else:
                renpy.notify("Глава в разработке")
                renpy.run(MainMenu())
        elif "Третья" in new_chapter_title or "Испытание" in new_chapter_title:
            # Проверяем, существует ли метка chapter_three
            if renpy.has_label("chapter_three"):
                renpy.jump("chapter_three")
            else:
                renpy.notify("Глава в разработке")
                renpy.run(MainMenu())
        else:
            # По умолчанию пытаемся перейти к chapter_two
            if renpy.has_label("chapter_two"):
                renpy.jump("chapter_two")
            else:
                renpy.notify("Глава в разработке")
                renpy.run(MainMenu())
    
    # Функция для выхода в главное меню (с сохранением, хотя оно уже должно быть сделано)
    def exit_to_main_menu(old_chapter):
        """Сохраняет прогресс (на всякий случай) и выходит в главное меню"""
        # Проверяем, нужно ли сохранять (если вдруг автосохранение не сработало)
        if hasattr(persistent, 'user_id') and persistent.user_id and 'db' in globals() and hasattr(db, 'update_save_progress'):
            try:
                db.update_save_progress(persistent.user_id, old_chapter)
            except:
                pass
        
        renpy.notify("Возвращаемся в главное меню...")
        renpy.run(MainMenu())

    # Функция для сохранения информации о пользователе
    def save_user_info():
        """Сохраняет информацию о текущем пользователе в файл сохранения"""
        renpy.save_persistent()
        return
    
    # Функция для добавления информации о пользователе в JSON сохранения
    def add_user_info_to_save(json_data):
        """Добавляет информацию о пользователе в JSON сохранения"""
        try:
            # Безопасно получаем имя пользователя
            user_name = ""
            if hasattr(persistent, 'user_name') and persistent.user_name:
                user_name = persistent.user_name
            json_data["user_name"] = user_name
            
            # Безопасно получаем ID пользователя
            user_id = None
            if hasattr(persistent, 'user_id') and persistent.user_id is not None:
                user_id = persistent.user_id
            json_data["user_id"] = user_id
            
            json_data["chapter"] = get_current_chapter_safe()
            json_data["_timestamp"] = time.time()
        except Exception:
            # В случае любой ошибки, просто продолжаем с минимальными данными
            json_data["chapter"] = "Глава Первая: Связь"
            json_data["_timestamp"] = time.time()
        
        return json_data
    
    # Очищаем и добавляем функцию в колбэки
    if hasattr(config, 'save_json_callbacks'):
        config.save_json_callbacks = []
        config.save_json_callbacks.append(add_user_info_to_save)
    
    # Функция для сохранения прогресса пользователя
    def save_user_progress():
        """Сохраняет текущий прогресс пользователя"""
        if hasattr(persistent, 'user_id') and persistent.user_id:
            # Сохраняем в базу данных
            current_chapter = get_current_chapter_safe()
            if hasattr(db, 'update_save_progress'):
                try:
                    db.update_save_progress(persistent.user_id, current_chapter)
                except:
                    pass
            
            # Также сохраняем информацию в файл сохранения
            renpy.take_screenshot()
            renpy.save("quick-save", "Быстрое сохранение")
    
    # Функция continue_game
    def continue_game():
        """Показывает экран выбора пользователя для продолжения игры"""
        renpy.show_screen("select_user_screen")
        return
    
    # Функция custom_file_action
    def custom_file_action(slot):
        """Кастомное действие для загрузки с проверкой пользователя"""
        # Проверяем, существует ли сохранение
        if not renpy.can_load(str(slot)):
            return
        
        try:
            save_json = renpy.json_load(renpy.slot_json_filename(str(slot)))
            # Получаем текущий ID пользователя
            current_user_id = None
            if hasattr(persistent, 'user_id') and persistent.user_id is not None:
                current_user_id = persistent.user_id
                
            if save_json and save_json.get("user_id") != current_user_id and save_json.get("user_id") is not None:
                # Если сохранение принадлежит другому пользователю
                renpy.show_screen("confirm_user_switch", slot=slot)
                return
        except:
            pass
        
        # Используем FileAction для загрузки
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

    # Функция для кастомного действия сохранения
    def custom_save_action(slot):
        """Кастомное действие для сохранения с информацией о пользователе и главе"""
        # Получаем текущую главу
        current_chapter = get_current_chapter_safe()
        
        # Делаем скриншот
        renpy.take_screenshot()
        
        # Сохраняем с дополнительной информацией
        renpy.save(str(slot), f"Сохранение {slot}")
        
        # Обновляем информацию в JSON
        try:
            save_json = renpy.json_load(renpy.slot_json_filename(str(slot)))
            if save_json:
                # Сохраняем ID пользователя
                if hasattr(persistent, 'user_id') and persistent.user_id is not None:
                    save_json["user_id"] = persistent.user_id
                else:
                    save_json["user_id"] = None
                    
                # Сохраняем имя пользователя
                if hasattr(persistent, 'user_name') and persistent.user_name:
                    save_json["user_name"] = persistent.user_name
                else:
                    save_json["user_name"] = ""
                    
                save_json["chapter"] = current_chapter
                save_json["_timestamp"] = time.time()
                
                # Сохраняем обратно
                with open(renpy.slot_json_filename(str(slot)), 'w', encoding='utf-8') as f:
                    json.dump(save_json, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка при сохранении JSON: {e}")
        
        renpy.notify(f"Игра сохранена в слот {slot}")
    
    # ЕДИНСТВЕННАЯ функция для определения текущей главы
    def get_current_chapter_safe():
        """Безопасно определяет текущую главу, работает даже во время сохранения"""
        try:
            # Пробуем получить из глобальной переменной
            if hasattr(store, 'current_chapter') and store.current_chapter:
                return store.current_chapter
        except:
            pass
        
        # По умолчанию возвращаем первую главу
        return "Глава Первая: Связь"
    
        # Функция для сохранения прогресса и перехода к следующей главе
    def save_progress_and_continue(old_chapter, new_chapter_title, new_chapter_subtitle):
        """Сохраняет прогресс и запускает следующую главу"""
        if hasattr(persistent, 'user_id') and persistent.user_id and 'db' in globals() and hasattr(db, 'update_save_progress'):
            try:
                db.update_save_progress(persistent.user_id, old_chapter)
            except:
                pass
        
        # Разблокируем достижение за прохождение главы
        try:
            if "Первая" in old_chapter or "Связь" in old_chapter:
                if 'unlock_achievement' in globals():
                    unlock_achievement("chapter_one_complete")
            elif "Вторая" in old_chapter or "Новые знакомства" in old_chapter:
                if 'unlock_achievement' in globals():
                    unlock_achievement("chapter_two_complete")
        except:
            pass
        
        # Делаем скриншот и сохраняем
        try:
            renpy.take_screenshot()
            slot_name = f"chapter-{int(time.time())}"
            renpy.save(slot_name, f"Автосохранение после {old_chapter}")
            
            # Обновляем JSON с информацией о главе
            try:
                import json
                save_json = renpy.json_load(renpy.slot_json_filename(slot_name))
                if save_json:
                    save_json["chapter"] = old_chapter
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
        
        renpy.notify("Прогресс сохранен!")
        
        # Определяем, на какую главу переходить
        if "Вторая" in new_chapter_title or "Новые знакомства" in new_chapter_title:
            # Проверяем, существует ли метка chapter_two
            if renpy.has_label("chapter_two"):
                renpy.jump("chapter_two")
            else:
                renpy.notify("Глава в разработке")
                # Возвращаемся в главное меню, так как главы нет
                renpy.run(MainMenu())
        elif "Третья" in new_chapter_title or "Испытание" in new_chapter_title:
            # Проверяем, существует ли метка chapter_three
            if renpy.has_label("chapter_three"):
                renpy.jump("chapter_three")
            else:
                renpy.notify("Глава в разработке")
                # Возвращаемся в главное меню, так как главы нет
                renpy.run(MainMenu())
        else:
            # По умолчанию пытаемся перейти к chapter_two
            if renpy.has_label("chapter_two"):
                renpy.jump("chapter_two")
            else:
                renpy.notify("Глава в разработке")
                # Возвращаемся в главное меню, так как главы нет
                renpy.run(MainMenu())
    
    def save_progress_and_continue(old_chapter, new_chapter_title, new_chapter_subtitle):
        """(Устаревшая функция) - используйте continue_to_next_chapter после auto_save_chapter_complete"""
        # Просто вызываем переход без повторного сохранения
        continue_to_next_chapter(old_chapter, new_chapter_title, new_chapter_subtitle)
    
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
    
    def set_current_user(user_id, user_name):
        """Установка текущего пользователя"""
        if hasattr(persistent, 'user_id'):
            persistent.user_id = user_id
        if hasattr(persistent, 'user_name'):
            persistent.user_name = user_name
        renpy.notify(f"Выбран игрок: {user_name}")


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
    
    # Разблокировка элементов галереи
    $ unlock_gallery_item("room_evening")

    # Показываем фон
    scene bg room_evening at truecenter with fade

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
    thought_user "Педагогическая алекситимия. Это слово, которое мне сказала врач, когда я проходила повторную комиссию в больнице.{p}Оно звучит так… официально. Как диагноз. Как приговор."
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

    # Диалог с первым выбором
    show lina happy at center with dissolve
    e "Привет! Ты уже готова к завтрашнему дню?{p}Я так рада, что мы теперь будем учиться вместе!🥳{p}Я уже придумала, как мы будем проводить перемены! ✨✨✨"
    hide lina

    narrator "Слова Лины, написанные с такой непринужденной легкостью, казались [persistent.user_name] одновременно и утешительными, и пугающими."
    narrator "Радость Лины была искренней, это было видно даже по смайликам, которые она использовала."

    thought_user "Я хочу ответить ей также жизнерадостно.. Но у меня не получается. Мои пальцы замирают над клавишами."
    thought_user "Что я могу сказать?"

    menu first_choice:
        "Привет! Да, готова. Уже жду не дождусь!":
            $ choice_1 = 1
            user_char "Привет! Да, готова. Уже жду не дождусь! 😊"
            $ unlock_achievement("first_choice")
            jump after_first_choice_1
        
        "Привет! Я тоже очень рада! Немного волнуюсь, но уверена, что с тобой будет весело!":
            $ choice_1 = 2
            user_char "Привет! Я тоже очень рада!{p}Немного волнуюсь, но уверена, что с тобой будет весело! 😊"
            $ unlock_achievement("first_choice")
            jump after_first_choice_2
        
        "Привет! Я очень рада, что мы будем учиться вместе. Я немного волнуюсь, потому что это новая школа, но я уверена, что с тобой мне будет легче. Ты – мой самый лучший друг.":
            $ choice_1 = 3
            user_char "Привет! Я очень рада, что мы будем учиться вместе.{p}Я немного волнуюсь, потому что это новая школа, но я уверена, что с тобой мне будет легче. Ты – мой самый лучший друг. ❤️"
            $ unlock_achievement("first_choice")
            jump after_first_choice_3

label after_first_choice_1:
    narrator "[persistent.user_name] отправила сообщение. Сердце ее забилось чуть быстрее."
    narrator "Она почувствовала легкое разочарование в себе. Этот ответ был слишком поверхностным, слишком… обычным."
    narrator "Она знала, что Лина, скорее всего, не заметит подвоха, но сама [persistent.user_name] чувствовала себя так, будто снова спряталась за маской."

    show lina happy at center with dissolve
    e "Ура! Я так рада!"
    e "Я уже придумала, что мы можем пойти в кафе после уроков, если захочешь! Или в парк! Что скажешь?"
    hide lina

    narrator "Лина, как всегда, полна энергии и предложений."
    
    thought_user "Жаль что у меня так не получается, как у Лины…"
    
    narrator "Она хотела бы ответить с такой же легкостью, но ее внутренний мир был слишком запутан."
    
    menu second_choice_1:
        "Звучит здорово! Я согласна на все!":
            $ choice_2 = 11
            user_char "Звучит здорово! Я согласна на все!"
            
        "Давай сначала посмотрим, как пройдет день. Я немного устала сегодня.":
            $ choice_2 = 12
            user_char "Давай сначала посмотрим, как пройдет день. Я немного устала сегодня."
    
    jump night_scene

label after_first_choice_2:
    narrator "[persistent.user_name] отправила сообщение. Она почувствовала легкое облегчение. Это было лучше, чем простое \"да\". Признание волнения было шагом к открытости."

    show lina happy at center with dissolve
    e "Ой, я понимаю! Но не переживай! Мы же вместе! Я тебе помогу со всем разобраться, обещаю! А перемены…"
    e "Я придумала, что мы можем ходить в библиотеку, там так тихо и уютно, или можем искать самые интересные уголки школы! Ты как?"
    hide lina

    narrator "Лина не просто ответила, она предложила конкретные планы, пытаясь развеять любые сомнения [persistent.user_name]."
    narrator "Ее слова были полны заботы и желания сделать так, чтобы [persistent.user_name] чувствовала себя комфортно."
    
    menu second_choice_2:
        "Звучит здорово! Библиотека – отличная идея!":
            $ choice_2 = 21
            user_char "Звучит здорово! Библиотека – отличная идея!"
            
        "Спасибо, Лина! Мне очень приятно, что ты так заботишься. Библиотека – это хорошо, но я, наверное, пока буду просто наблюдать.":
            $ choice_2 = 22
            user_char "Спасибо, Лина! Мне очень приятно, что ты так заботишься. Библиотека – это хорошо, но я, наверное, пока буду просто наблюдать."
    
    jump night_scene

label after_first_choice_3:
    narrator "[persistent.user_name] отправила сообщение. Сердце ее колотилось в груди. Это было самое откровенное, что она могла написать. Она почувствовала, как по ее телу разливается тепло, смешанное с тревогой."

    thought_user "Что скажет Лина? Примет ли она эту частичку моей истинной сущности?"

    show lina happy at center with dissolve
    e "Ой, [persistent.user_name]! 🥺 Я так тронута! Спасибо тебе большое!"
    e "Я тоже очень рада, что мы будем вместе! И ты не волнуйся, я буду рядом! Мы все вместе преодолеем!"
    e "А перемены… Я придумала, что мы можем просто сидеть где-нибудь в тихом месте и разговаривать, или если ты захочешь, мы можем вместе изучать новые места в школе!"
    e "Главное, чтобы тебе было комфортно! Ты – мой самый лучший друг тоже!"
    hide lina

    narrator "Слова Лины были полны искренности и тепла. Она не только приняла признание [persistent.user_name], но и ответила взаимностью, показав, что ее дружба не зависит от того, насколько [persistent.user_name] открыта."
    narrator "Это было именно то, что нужно [persistent.user_name], чтобы почувствовать себя немного увереннее."
    
    menu second_choice_3:
        "Спасибо, Лина! Ты лучшая! Я уже чувствую себя спокойнее.":
            $ choice_2 = 31
            user_char "Спасибо, Лина! Ты лучшая! Я уже чувствую себя спокойнее."
            
        "Спасибо, Лина! Я очень ценю твою дружбу. И да, мне будет легче, если ты будешь рядом.":
            $ choice_2 = 32
            user_char "Спасибо, Лина! Я очень ценю твою дружбу. И да, мне будет легче, если ты будешь рядом."
    
    jump night_scene

label night_scene:
    stop music
    scene bg night_room with fade
    play sound "song/night_ambient.mp3" fadein 3.0
    
    narrator "Ночь опустилась на город мягко, как шелковое одеяло."
    narrator "[persistent.user_name] лежала в постели, уставившись в потолок, где плясали тени от уличного фонаря."
    narrator "Сообщения Лины все еще крутились в голове, теплые и поддерживающие."
    narrator "Засыпая, [persistent.user_name] думала только об одном…"

    thought_user "Завтрашний день в новой школе… Это не просто новый этап — это будет прыжок в неизвестность, где моя тревога может либо раствориться в дружбе с Линой, либо накрыть с головой."
    
    stop sound fadeout 3.0
    scene black with fade
    pause 1.0

label morning_scene:
    stop music
    scene bg room_evening with fade
    play music "song/Audio_soft_1.mp3" fadein 3.0
    
    narrator "Утро пришло слишком быстро. Солнце пробивалось сквозь шторы, окрашивая комнату в золотистый свет."
    narrator "[persistent.user_name] проснулась с тяжелым сердцем, но с решимостью. Она села на кровати, потянулась и бросила взгляд на телефон. Новое сообщение от Лины уже ждало."

    show lina happy at center with dissolve
    e "Доброе утро, [persistent.user_name]! 🌅 Уже проснулась?"
    e "Я собираюсь и так волнуюсь за тебя! Не забудь взять тетради и хорошее настроение. Увидимся у входа в школу? 😘"
    hide lina

    thought_user "Ее энтузиазм заразителен... Может, и мне удастся почувствовать то же самое? Я не хочу подвести ее."

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

    show lina happy at center with dissolve
    e "[persistent.user_name]! Привет!"
    e "Я так рада тебя видеть!{p}Ты не опоздала ни на секунду!"

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
    
    # АВТОМАТИЧЕСКОЕ СОХРАНЕНИЕ при завершении главы
    $ auto_save_chapter_complete("Глава Первая: Связь")
    
    # Показываем экран перехода (переход без дополнительного сохранения)
    $ renpy.show_screen("chapter_transition", "Глава Первая: Связь", "Глава Вторая: Новые знакомства", "Новые знакомства")
    $ renpy.pause(None)


################################################################################
## Глава Вторая: Новые знакомства
################################################################################

label chapter_two:
    # Устанавливаем текущую главу для безопасного определения
    $ current_chapter = "Глава Вторая: Новые знакомства"
    
    # Показываем заголовок главы
    scene black with fade
    show text "{size=80}Глава Вторая{/size}\n{size=60}Новые знакомства{/size}" with dissolve
    pause 3.0
    scene black with dissolve
    
    # Обновляем прогресс в базе данных
    if persistent.user_id and 'db' in globals() and hasattr(db, 'update_save_progress'):
        $ db.update_save_progress(persistent.user_id, "Глава Вторая: Новые знакомства")
    
    # Запускаем музыку для второй главы
    play music "song/Audio_soft_2.mp3" fadein 5.0
    $ renpy.music.set_volume(0.4, delay=5)
    
    # Школьный коридор - временно используем school_entrance вместо school_hallway
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
            user_char "Да, я сегодня первый день. Приятно познакомиться."
            
        "Эм... да. Я новенькая.":
            $ chapter2_choice_1 = 2
            user_char "Эм... да. Я новенькая."
        
        "Просто молча кивнуть":
            $ chapter2_choice_1 = 3
            narrator "[persistent.user_name] просто молча кивнула."
    
    a "Класс! Я Алекс. Если что-то нужно будет — обращайся. Я здесь уже второй год, все знаю!"
    
    show lina happy at left with move
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
    
    # Сцена на уроке
    scene bg classroom with fade
    
    narrator "Класс был светлым и просторным. Ученики уже рассаживались по местам, приветствуя друг друга."
    narrator "Учительница, женщина средних лет с добрыми глазами, жестом пригласила всех сесть."
    
    show teacher kind at center with dissolve
    
    t "Ребята, сегодня у нас новая ученица. Представься, пожалуйста."
    
    narrator "Все взгляды устремились на [persistent.user_name]. Она почувствовала, как щеки заливает румянец."
    
    thought_user "Так, спокойно. Я же готовилась к этому."
    
    user_char "Меня зовут [persistent.user_name]. Я... я надеюсь, мы подружимся."
    
    narrator "Кто-то из ребят одобрительно кивнул, кто-то улыбнулся. Одна девочка на последней парте с интересом рассматривала новенькую."
    
    t "Садись, [persistent.user_name]. А ты, Катя, покажешь нашей новой ученице, как у нас все устроено, хорошо?"
    
    show katia smile at left with moveinleft
    
    k "Конечно, Анна Сергеевна!"
    
    hide teacher
    
    narrator "Катя помахала [persistent.user_name] рукой, приглашая сесть рядом."
    narrator "[persistent.user_name] осторожно опустилась на стул, чувствуя, как внутри смешиваются страх и любопытство."
    
    thought_user "Катя... Она кажется дружелюбной. Может, сегодня не такой уж плохой день?"
    
    # Звонок с урока
    play sound "song/school_bell.mp3"
    pause 1.0
    
    scene bg school_entrance with fade
    
    narrator "Первая перемена пролетела незаметно. Катя оказалась очень разговорчивой и рассказывала о всех учителях и школьных традициях."
    
    show katia smile at left
    show lina happy at right
    
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
    
    narrator "Актовый зал оказался уютным помещением с мягкими креслами и стареньким пианино в углу."
    narrator "Несколько ребят уже настраивали инструменты. Алекс взял гитару и улыбнулся."
    
    show alex smile at center with dissolve
    a "Мы сейчас разучиваем новую песню. Хотите послушать?"
    hide alex
    
    narrator "[persistent.user_name] кивнула, чувствуя, как музыка начинает заполнять пространство."
    narrator "Мелодия была простой, но в ней чувствовалось что-то теплое и искреннее."
    
    thought_user "Музыка... Оказывается, она может передавать чувства без слов. Это удивительно."
    
    show lina happy at center with dissolve
    e "Тебе нравится, [persistent.user_name]?"
    
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
    
    narrator "Пока остальные пошли в актовый зал, [persistent.user_name] направилась в библиотеку."
    narrator "Здесь было тихо и спокойно, пахло старыми книгами и уютом."
    
    show librarian kind at center with dissolve
    
    lib "Здравствуй, дорогая! Ты новенькая? Хочешь что-то почитать?"
    
    thought_user "Библиотека... Здесь мне спокойно. Никто не требует быть общительной."
    
    user_char "Здравствуйте. Да, я бы хотела... может, что-то поспокойнее?"
    
    lib "О, тогда тебе точно понравится этот сборник рассказов о природе. Очень умиротворяющее чтение."
    hide librarian
    
    narrator "[persistent.user_name] взяла книгу и устроилась в уютном кресле у окна."
    narrator "Тишина обволакивала, давая возможность побыть наедине со своими мыслями."
    
    thought_user "Может, иногда лучше быть одной, чем чувствовать себя чужой в компании? Хотя... Лина и Катя... С ними, кажется, можно попробовать."
    
    jump chapter_two_end

label chapter_two_end:
    scene black with fade
    stop music fadeout 3.0
    stop sound fadeout 3.0
    
    show text "{size=80}Конец второй главы{/size}" with dissolve
    pause 2.0
    
    # АВТОМАТИЧЕСКОЕ СОХРАНЕНИЕ при завершении главы
    $ auto_save_chapter_complete("Глава Вторая: Новые знакомства")
    
    # Обновляем прогресс в базе данных (дополнительно)
    if persistent.user_id and 'db' in globals() and hasattr(db, 'update_save_progress'):
        $ db.update_save_progress(persistent.user_id, "Глава Вторая: Новые знакомства")
    
    # Разблокируем достижение за прохождение второй главы
    $ unlock_achievement("chapter_two_complete")
    
    # Показываем экран перехода (переход без дополнительного сохранения)
    $ renpy.show_screen("chapter_transition", "Глава Вторая: Новые знакомства", "Глава Третья: Испытание дружбой", "Испытание дружбой")
    $ renpy.pause(None)


label chapter_three:
    # Устанавливаем текущую главу для безопасного определения
    $ current_chapter = "Глава Третья: Испытание дружбой"
    
    # Показываем заголовок главы
    scene black with fade
    show text "{size=80}Глава Третья{/size}\n{size=60}Испытание дружбой{/size}" with dissolve
    pause 2.0
    
    # Обновляем прогресс в базе данных
    #if persistent.user_id and 'db' in globals() and hasattr(db, 'update_save_progress'):
    #    $ db.update_save_progress(persistent.user_id, "Глава Третья: Испытание дружбой")
    
    # Здесь будет код третьей главы
    # ...
    #
    # В конце третьей главы:
    #scene black with fade
    #show text "{size=80}Конец третьей главы{/size}" with dissolve
    #pause 2.0
    #
    # АВТОМАТИЧЕСКОЕ СОХРАНЕНИЕ при завершении главы
    #$ auto_save_chapter_complete("Глава Третья: Испытание дружбой")
    #
    # Разблокируем достижение
    #$ unlock_achievement("chapter_three_complete")
    #
    # Показываем экран перехода к следующей главе или финальный экран
    #$ renpy.show_screen("chapter_transition", "Глава Третья: Испытание дружбой", "Глава Четвертая", "Новые испытания")
    #$ renpy.pause(None)