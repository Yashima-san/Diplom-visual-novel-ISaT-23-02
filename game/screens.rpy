################################################################################
## Инициализация
################################################################################

init offset = -1

init python:
    import time
    import json
    
    def get_last_save_info(user_id):
        """Получение информации о последнем сохранении пользователя"""
        result = {
            'time': "Нет сохранений",
            'chapter': "Нет данных"
        }
        last_time = 0
        last_chapter = "Нет данных"
        
        try:
            chapter_display = {
                "Глава Первая: Связь": "Глава 1",
                "Глава Вторая: Новые знакомства": "Глава 2",
                "Глава Третья: Испытание дружбой": "Глава 3",
            }
            
            # Проверяем все возможные слоты сохранений
            all_slots = []
            # Обычные слоты 1-9
            for i in range(1, 10):
                all_slots.append(str(i))
            # Автосохранения 1-9
            for i in range(1, 10):
                all_slots.append(f"auto-{i}")
            # Быстрое сохранение
            all_slots.append("quick-save")
            
            for slot_name in all_slots:
                if renpy.can_load(slot_name):
                    try:
                        save_json = renpy.json_load(renpy.slot_json_filename(slot_name))
                        if save_json and save_json.get("user_id") == user_id:
                            timestamp = save_json.get("_timestamp", 0)
                            if timestamp > last_time:
                                last_time = timestamp
                                if timestamp:
                                    try:
                                        time_str = time.strftime("%d.%m.%Y %H:%M", time.localtime(timestamp))
                                        result['time'] = time_str
                                    except:
                                        result['time'] = "Недавно"
                                
                                # Получаем название главы из сохранения
                                save_chapter = save_json.get("chapter", "")
                                if save_chapter:
                                    if save_chapter in chapter_display:
                                        last_chapter = chapter_display[save_chapter]
                                    else:
                                        # Пытаемся определить главу по содержимому
                                        if "Первая" in save_chapter or "Связь" in save_chapter:
                                            last_chapter = "Глава 1"
                                        elif "Вторая" in save_chapter or "Новые знакомства" in save_chapter:
                                            last_chapter = "Глава 2"
                                        elif "Третья" in save_chapter:
                                            last_chapter = "Глава 3"
                                        else:
                                            last_chapter = save_chapter[:20] + "..." if len(save_chapter) > 20 else save_chapter
                    except:
                        continue
            
            result['chapter'] = last_chapter
            
            # Если нашли сохранение, но глава не определилась, проверяем в БД
            if result['chapter'] == "Нет данных" and last_time > 0:
                if hasattr(db, 'get_user_progress'):
                    progress = db.get_user_progress(user_id)
                    if progress:
                        result['chapter'] = progress[-1] if progress else "Нет данных"
        except Exception as e:
            print(f"Ошибка в get_last_save_info: {e}")
        
        return result
    
    def get_user_progress(user_id):
        """Получение прогресса игрока по главам"""
        progress = []
        
        # Словарь для форматирования названий глав
        chapter_formats = {
            "Глава Первая: Связь": "Глава 1",
            "Глава Вторая: Новые знакомства": "Глава 2",
            "Глава Третья: Испытание дружбой": "Глава 3",
        }
        
        try:
            # Проверяем все сохранения в JSON
            all_slots = []
            for i in range(1, 10):
                all_slots.append(str(i))
            for i in range(1, 10):
                all_slots.append(f"auto-{i}")
            all_slots.append("quick-save")
            
            chapters_found = set()
            
            for slot_name in all_slots:
                if renpy.can_load(slot_name):
                    try:
                        save_json = renpy.json_load(renpy.slot_json_filename(slot_name))
                        if save_json and save_json.get("user_id") == user_id:
                            chapter = save_json.get("chapter", "")
                            if chapter:
                                if chapter in chapter_formats:
                                    chapters_found.add(chapter_formats[chapter])
                                else:
                                    # Пытаемся определить главу по содержимому
                                    if "Первая" in chapter or "Связь" in chapter:
                                        chapters_found.add("Глава 1")
                                    elif "Вторая" in chapter or "Новые знакомства" in chapter:
                                        chapters_found.add("Глава 2")
                                    elif "Третья" in chapter:
                                        chapters_found.add("Глава 3")
                    except:
                        continue
            
            # Преобразуем в список и сортируем
            chapter_order = {"Глава 1": 1, "Глава 2": 2, "Глава 3": 3}
            progress = sorted(list(chapters_found), key=lambda x: chapter_order.get(x, 0))
            
        except Exception as e:
            print(f"Ошибка в get_user_progress: {e}")
        
        return progress

################################################################################
## Стили
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)


###### Стили курсоров ######

# Базовый стиль для всех кнопок с правильными курсорами
style button:
    properties gui.button_properties("button")
    mouse "default"                     # Обычное состояние
    hover_mouse "hover"                  # Наведение
    selected_mouse "click"              # Выбранное состояние
    selected_hover_mouse "click"          # Наведение на выбранном состоянии
    insensitive_mouse "default"           # Неактивное состояние

# Стили для курсоров (определяем их один раз)
init python:
    # Создаем курсоры если нужно (опционально)
    config.mouse = {
        "default": [ ("gui/cursor/default.png", 0, 0) ],
        "hover": [ ("gui/cursor/hover.png", 0, 0) ],
        "selected": [ ("gui/cursor/click.png", 0, 0) ],
        "selected_hover": [ ("gui/cursor/click.png", 0, 0) ],
        "insensitive": [ ("gui/cursor/default.png", 0, 0) ],
    }


# Для кнопок навигации
style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

# Для кнопок быстрого меню
style quick_button:
    properties gui.button_properties("quick_button")

# Для кнопок выбора
style choice_button:
    properties gui.button_properties("choice_button")

################################################################################
## Внутриигровые экраны
################################################################################

## Экран разговора #############################################################

screen say(who, what):
    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"

    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0

init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos 18 
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos

    adjust_spacing False

## Экран ввода #################################################################

screen input(prompt):
    style_prefix "input"
    window:

        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width

## Экран выбора ################################################################

screen choice(items):
    style_prefix "choice"
    vbox:
        for i in items:
            textbutton i.caption action i.action


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.text_properties("choice_button")

## Экран быстрого меню #########################################################

screen quick_menu():

    zorder 100

    # Убираем условие quick_menu или делаем его всегда True во время диалогов
    if True:  # Всегда показываем quick_menu

        hbox:
            style_prefix "quick"
            style "quick_menu"

            textbutton _("Назад") action Rollback()
            textbutton _("История") action ShowMenu('history')
            textbutton _("Пропуск") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Авто") action Preference("auto-forward", "toggle")
            textbutton _("Сохранить") action ShowMenu('save')
            textbutton _("Б.Сохр") action QuickSave()
            textbutton _("Б.Загр") action QuickLoad()
            textbutton _("Опции") action ShowMenu('preferences')


init python:
    config.overlay_screens.append("quick_menu")

# Убираем или комментируем эту строку, так как она не нужна
# default quick_menu = True

style quick_menu is hbox
style quick_button is default
style quick_button_text is button_text

style quick_menu:
    xalign 0.5
    yalign 0.97

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.text_properties("quick_button")

################################################################################
## Экраны Главного и Игрового меню
################################################################################

## Экран навигации #############################################################

screen navigation():
    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.8

        spacing gui.navigation_spacing

        if main_menu:

            textbutton _("Начать") action Start() 

        else:

            textbutton _("История") action ShowMenu("history")

            textbutton _("Сохранить") action ShowMenu("save")

        textbutton _("Загрузить") action ShowMenu("load")

        textbutton _("Настройки") action ShowMenu("preferences")

        if _in_replay:

            textbutton _("Завершить повтор") action EndReplay(confirm=True)

        elif not main_menu:

            textbutton _("Главное меню") action MainMenu()

        textbutton _("Об игре") action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

            textbutton _("Помощь") action ShowMenu("help")

        if renpy.variant("pc"):

            textbutton _("Выход") action Quit(confirm=not main_menu)


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.text_properties("navigation_button")


################################################################################
## Экран выбора пользователя для продолжения игры
################################################################################

screen select_user_screen():
    modal True
    zorder 200
    
    style_prefix "select_user"
    
    add "gui/overlay/confirm.png"
    
    frame:
        style "select_user_frame"
        xalign 0.5
        yalign 0.5
        xsize 1200
        ysize 900
        padding (70, 70)
        
        vbox:
            spacing 20
            xfill True
            
            text "Выберите пользователя для продолжения:":
                size 32
                color "#ffffff"
                font gui.interface_text_font
                xalign 0.5
                yalign 0.5
            
            null height 10
            
            # Получаем список всех пользователей
            $ users = db.get_all_users() if hasattr(db, 'get_all_users') else []
            
            if users:
                # Заголовок таблицы
                frame:
                    style "select_user_header"
                    xfill True
                    padding (10, 12)
                    
                    hbox:
                        spacing 20
                        xfill True
                        
                        text "Имя" size 22 color "#ffffff" xsize 200 text_align 0.5
                        text "Сохранение" size 22 color "#ffffff" xsize 400 text_align 0.5
                        text "Прогресс" size 22 color "#ffffff" xsize 250 text_align 0.5
                        text "Достижений" size 22 color "#ffffff" xsize 150 text_align 0.5
                
                # Список пользователей
                viewport:
                    ysize 350
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    
                    vbox:
                        spacing 5
                        xfill True
                        
                        for user in users:
                            $ user_id = user['user_ID']
                            $ user_name = user['name']
                            
                            # Получаем информацию о последнем сохранении
                            $ last_save_info = get_last_save_info(user_id)
                            $ last_save_time = last_save_info['time']
                            $ last_save_chapter = last_save_info['chapter']
                            
                            # Получаем прогресс пользователя (все пройденные главы)
                            $ user_progress = get_user_progress(user_id)
                            $ progress_text = ", ".join(user_progress) if user_progress else "Нет данных"
                            
                            # Получаем количество достижений
                            $ user_achievements = db.get_user_achievements(user_id) if hasattr(db, 'get_user_achievements') else []
                            $ ach_count = len(user_achievements)
                            
                            # Кнопка выбора пользователя
                            button:
                                style "select_user_row"
                                xfill True
                                action [Function(set_current_user, user_id, user_name), Function(load_last_save_for_user, user_id), Hide("select_user_screen")]
                                
                                hbox:
                                    spacing 20
                                    xfill True
                                    
                                    text "[user_name]" size 22 color "#ffffff" xsize 200 text_align 0.5
                                    text "[last_save_time]" size 22 color "#ffffff" xsize 400 text_align 0.5
                                    text "[progress_text]" size 22 color "#ffffff" xsize 250 text_align 0.5
                                    text "[ach_count]" size 22 color "#ffffff" xsize 150 text_align 0.5
            else:
                # Сообщение когда нет пользователей
                vbox:
                    spacing 30
                    xalign 0.5
                    yalign 0.5
                    
                    text "Нет сохраненных игроков" size 28 xalign 0.5 color "#656565"
                    text "Начните новую игру, чтобы создать сохранение" size 22 xalign 0.5 color "#737373"
                    
                    null height 20
            
            null height 20
            
            # Кнопки действий
            hbox:
                spacing 5
                xalign 0.5
                yalign 0.1
                
                # Кнопка для начала новой игры прямо отсюда
                textbutton "Начать новую игру" style "select_user_button" action [Start(), Hide("select_user_screen")]
                
                textbutton "Отмена" style "select_user_button" action Hide("select_user_screen")
    
    key "game_menu" action Hide("select_user_screen")
    key "K_ESCAPE" action Hide("select_user_screen")

# Стили для экрана выбора пользователя
style select_user_frame:
    background Frame("gui/confirm_frame.png", 25, 25, 25, 25)
    padding (30, 30)

style select_user_header:
    background "#c66b2f"
    xfill True

style select_user_header_text:
    color "#ffffff"
    size 22

style select_user_row:
    background "#d9874d"
    hover_background "#97321b"
    xfill True
    padding (10, 8)
    margin (0, 2)

style select_user_button:
    padding (5, 5)
    xsize 350

style select_user_button_text:
    color "#ffffff"
    hover_color "#fb906d"
    outlines[(2, "#671a1a", 0, 0)]
    size 22
    font gui.interface_text_font
    text_align 0.5


init python:
    def get_user_last_chapter(user_id):
        """Получение последней главы пользователя"""
        last_chapter = None
        last_time = 0
        
        try:
            # Проверяем сохранения в файлах
            for i in range(1, 10):
                if renpy.can_load(str(i)):
                    try:
                        save_json = renpy.json_load(renpy.slot_json_filename(str(i)))
                        if save_json and save_json.get("user_id") == user_id:
                            timestamp = save_json.get("_timestamp", 0)
                            if timestamp > last_time:
                                last_time = timestamp
                                # Пытаемся получить название главы из сохранения
                                last_chapter = save_json.get("chapter", "Глава 1")
                    except:
                        continue
            
            # Если не нашли в сохранениях, проверяем в БД
            if not last_chapter and hasattr(db, 'sqlite_available') and db.sqlite_available:
                try:
                    db.connect()
                    db.cursor.execute('''
                        SELECT chapter FROM save_progress_users 
                        WHERE user_ID = ? ORDER BY save_point DESC LIMIT 1
                    ''', (user_id,))
                    row = db.cursor.fetchone()
                    if row:
                        last_chapter = row['chapter']
                except:
                    pass
                finally:
                    db.disconnect()
            
            # Если все еще нет, проверяем в persistent
            if not last_chapter and hasattr(persistent, 'user_data') and persistent.user_data:
                str_user_id = str(user_id)
                if 'save_progress' in persistent.user_data and str_user_id in persistent.user_data['save_progress']:
                    saves = persistent.user_data['save_progress'][str_user_id]
                    if saves:
                        last_chapter = saves[-1].get('chapter', 'Глава 1')
        except:
            pass
        
        return last_chapter if last_chapter else "Нет сохранений"
    
    def load_last_save_or_start():
        """Загружает последнее сохранение или начинает новую игру"""
        if persistent.user_id and load_last_save_for_user(persistent.user_id):
            return
        else:
            # Если нет сохранений, начинаем новую игру
            renpy.call_in_new_context("start")

    def set_current_user(user_id, user_name):
        """Установка текущего пользователя"""
        persistent.user_id = user_id
        persistent.user_name = user_name
        renpy.notify(f"Выбран игрок: {user_name}")


## Экран главного меню #########################################################

screen main_menu():
    
    tag menu

    # Фон из папки gui
    add "gui/main_menu.png"
    
    # Название игры сверху по центру
    if gui.show_name:
        text "[config.name!t]":
            style "main_menu_title"
    
    # Версия игры в нижнем левом углу
    text "Версия [config.version]":
        style "main_menu_version"
        at transform:
            alpha 0.5
    
    # Центрированное меню на стикере
    frame:
        style "main_menu_frame"
        xalign 0.5
        yalign 0.5
        xsize 500
        ysize 650
        
        # Фон для рамки - стикер
        background Frame("gui/choice_idle_background.png", 25, 25, 25, 25)
        
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 1
            
            # Кнопки меню
            textbutton _("Продолжить"):
                style "main_menu_button"
                action Function(continue_game)
            
            textbutton _("Начать игру"):
                style "main_menu_button"
                action Start()
            
            textbutton _("Загрузить"):
                style "main_menu_button"
                action ShowMenu("load")
            
            textbutton _("Карточки"):
                style "main_menu_button"
                action ShowMenu("gallery")
            
            textbutton _("Достижения"):
                style "main_menu_button"
                action ShowMenu("achievements")
            
            textbutton _("Настройки"):
                style "main_menu_button"
                action ShowMenu("preferences")
            
            textbutton _("Выход"):
                style "main_menu_button"
                action Quit(confirm=True)
    
    # Кнопка "Игроки" слева от стикера
    button:
        style "players_button"
        action ShowMenu("debug_database")

## Стили для главного меню
style main_menu_title:
    color "#ffffff"
    size gui.title_text_size
    font gui.interface_text_font
    xalign 0.5
    yalign 0.1
    textalign 0.5
    layout "subtitle"
    outlines [(5, "#a43c13", 0, 0)]

style main_menu_version:
    color "#ffffff"
    size gui.interface_text_size
    font gui.interface_text_font
    xalign 0.02
    yalign 0.98
    textalign 0.0
    outlines [(2, "#000000", 0, 0)]

style main_menu_frame:
    xalign 0.5
    yalign 0.5
    xsize 500
    ysize 650
    background None

style main_menu_button:
    xalign 0.5
    padding (20, 15)
    xsize 400
    ysize None
    margin (0, 5)
    background Frame("gui/button/choice_idle_background.png", 15, 15, 15, 15)
    hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15, 15, 15)

style main_menu_button_text:
    color "#ffffff"
    hover_color "#fb906d"
    selected_color "#da6037"
    size 18
    font gui.interface_text_font
    outlines [(2, "#b64520", 0, 0)]
    text_align 0.5
    xalign 0.5

style players_button:
    xpos 0.22
    ypos 0.55
    xsize 295
    ysize 139
    background Frame("gui/button/choice_idle_background_3.png", 15, 15, 15, 15)
    hover_background Frame("gui/button/choice_hover_background_2.png", 15, 15, 15, 15)
    padding (20, 20)



## Экран игрового меню #########################################################

screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):
    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:

            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True
                        edgescroll (300, 500)
                        
                        xadjustment None
                        side_yfill True

                        vbox:
                            spacing spacing
                            xfill True
                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True
                        
                        xadjustment None
                        side_yfill True
                        spacing spacing
                        transclude

                else:
                    transclude

    use navigation

    textbutton _("Вернуться"):
        style "return_button"
        action Return()

    label title


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 45
    top_padding 180
    background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize 420
    yfill True

style game_menu_content_frame:
    left_margin 100
    right_margin 40
    top_margin 15

style game_menu_viewport:
    xsize 1340

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 15

style game_menu_label:
    xpos 65
    ysize 180

style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -45


## Экран Об игре ###############################################################

screen about():
    tag menu

    use game_menu(_("Об игре"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Версия [config.version!t]\n")

            if gui.about:
                text "[gui.about!t]\n"

            text _("Сделано с помощью {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Экраны загрузки и сохранения ################################################

screen save():
    tag menu
    use file_slots_with_user(_("Сохранить"), is_save=True)

screen load():
    tag menu
    use file_slots_with_user(_("Загрузить"), is_save=False)

screen file_slots_with_user(title, is_save=True):
    default page_name_value = FilePageNameInputValue(pattern=_("{} страница"), auto=_("Автосохранения"), quick=_("Быстрые сохранения"))
    
    # Отображаем информацию о текущем пользователе
    frame:
        style "user_info_frame"
        xalign 0.5
        yalign 0.05
        xsize 600
        padding (15, 10)
        
        hbox:
            spacing 10
            xalign 0.5
            text "Игрок:" size 24 color "#ffffff"
            text "[persistent.user_name]" size 24 color "#ff832b" bold True
            if persistent.user_id:
                text "(ID: [persistent.user_id])" size 18 color "#cccccc"
    
    use game_menu(title):
        fixed:
            yoffset 80
            
            order_reverse True
            
            button:
                style "page_label"
                
                key_events True
                xalign 0.5
                action page_name_value.Toggle()
                
                input:
                    style "page_label_text"
                    value page_name_value
            
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"
                
                xalign 0.5
                yalign 0.5
                
                spacing gui.slot_spacing
                
                for i in range(gui.file_slot_cols * gui.file_slot_rows):
                    
                    $ slot = i + 1
                    
                    button:
                        # Разные действия для сохранения и загрузки
                        if is_save:
                            action Function(custom_save_action, slot)
                        else:
                            action Function(custom_file_action, slot)
                        
                        has vbox
                        
                        add FileScreenshot(slot) xalign 0.5
                        
                        text FileTime(slot, format=_("{#file_time}%A, %d %B %Y, %H:%M"), empty=_("Пустой слот")):
                            style "slot_time_text"
                        
                        text FileSaveName(slot):
                            style "slot_name_text"
                        
                        # Добавляем информацию о пользователе в слот
                        $ save_user = FileJson(slot, "user_name", empty="")
                        if save_user:
                            text "Игрок: [save_user]":
                                style "slot_user_text"
                        
                        # Добавляем информацию о главе в слот
                        $ save_chapter = FileJson(slot, "chapter", empty="")
                        if save_chapter:
                            # Сокращаем название главы для отображения
                            if "Первая" in save_chapter or "Связь" in save_chapter:
                                $ display_chapter = "Глава 1"
                            elif "Вторая" in save_chapter or "Новые знакомства" in save_chapter:
                                $ display_chapter = "Глава 2"
                            elif "Третья" in save_chapter:
                                $ display_chapter = "Глава 3"
                            else:
                                $ display_chapter = save_chapter[:20] + "..." if len(save_chapter) > 20 else save_chapter
                            
                            text "Глава: [display_chapter]":
                                style "slot_chapter_text"
                        
                        key "save_delete" action FileDelete(slot)
            
            vbox:
                style_prefix "page"
                
                xalign 0.5
                yalign 1.0
                
                hbox:
                    xalign 0.5
                    
                    spacing gui.page_spacing
                    
                    textbutton _("<") action FilePagePrevious()
                    key "save_page_prev" action FilePagePrevious()
                    
                    if config.has_autosave:
                        textbutton _("{#auto_page}А") action FilePage("auto")
                    
                    if config.has_quicksave:
                        textbutton _("{#quick_page}Б") action FilePage("quick")
                    
                    for page in range(1, 10):
                        textbutton "[page]" action FilePage(page)
                    
                    textbutton _(">") action FilePageNext()
                    key "save_page_next" action FilePageNext()
                
                if config.has_sync:
                    if CurrentScreenName() == "save":
                        textbutton _("Загрузить Sync"):
                            action UploadSync()
                            xalign 0.5
                    else:
                        textbutton _("Скачать Sync"):
                            action DownloadSync()
                            xalign 0.5

style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 75
    ypadding 5
    xalign 0.5

style page_label_text:
    textalign 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.text_properties("slot_button")

style user_info_frame:
    background Frame("gui/frame.png", 15, 15, 15, 15)
    xalign 0.5
    yalign 0.05
    xsize 600
    padding (15, 10)

style slot_user_text:
    size 16
    color "#ff832b"
    font gui.interface_text_font
    xalign 0.5

# Стиль для текста главы в слоте
style slot_chapter_text:
    size 16
    color "#ff9e5e"
    font gui.interface_text_font
    xalign 0.5


## Экран настроек ##############################################################

screen preferences():
    tag menu

    use game_menu(_("Настройки"), scroll="viewport"):

        vbox:
            # Первая строка - режим экрана и пропуск
            hbox:
                spacing 100  # Добавляем расстояние между колонками
                
                if renpy.variant("pc") or renpy.variant("web"):
                    vbox:
                        style_prefix "radio"
                        label _("Режим экрана")
                        textbutton _("Оконный") action Preference("display", "window")
                        textbutton _("Полный") action Preference("display", "fullscreen")
                
                vbox:
                    style_prefix "check"
                    label _("Пропуск")
                    textbutton _("Всего текста") action Preference("skip", "toggle")
                    textbutton _("После выборов") action Preference("after choices", "toggle")
                    textbutton _("Переходов") action InvertSelected(Preference("transitions", "toggle"))

            null height (4 * gui.pref_spacing)

            # Вторая строка - слайдеры в две колонки
            hbox:
                style_prefix "slider"
                spacing 100  # Расстояние между колонками
                
                # Левая колонка
                vbox:
                    xsize 300  # Фиксированная ширина для левой колонки
                    
                    label _("Скорость текста")
                    bar value Preference("text speed")
                    
                    label _("Скорость авточтения")
                    bar value Preference("auto-forward time")
                
                # Правая колонка
                vbox:
                    xsize 400  # Фиксированная ширина для правой колонки
                    
                    if config.has_music:
                        label _("Громкость музыки")
                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:
                        label _("Громкость звуков")
                        hbox:
                            bar value Preference("sound volume")
                            if config.sample_sound:
                                textbutton _("Тест") action Play("sound", config.sample_sound)

                    if config.has_voice:
                        label _("Громкость голоса")
                        hbox:
                            bar value Preference("voice volume")
                            if config.sample_voice:
                                textbutton _("Тест") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing
                        textbutton _("Без звука"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 3

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 338

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.text_properties("check_button")

style slider_slider:
    xsize 525

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 15

style slider_button_text:
    properties gui.text_properties("slider_button")

style slider_vbox:
    xsize 675


## Экран истории ###############################################################

screen history():
    tag menu

    predict False

    use game_menu(_("История"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0, spacing=gui.history_spacing):

        style_prefix "history"

        for h in _history_list:

            window:

                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute False

                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("История диалогов пуста.")


define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## Экран помощи ################################################################

screen help():
    tag menu

    default device = "keyboard"

    use game_menu(_("Помощь"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing 23

            hbox:

                textbutton _("Клавиатура") action SetScreenVariable("device", "keyboard")
                textbutton _("Мышь") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("Геймпад") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help


screen keyboard_help():

    hbox:
        label _("Enter")
        text _("Прохождение диалогов, активация интерфейса.")

    hbox:
        label _("Пробел")
        text _("Прохождение диалогов без возможности делать выбор.")

    hbox:
        label _("Стрелки")
        text _("Навигация по интерфейсу.")

    hbox:
        label _("Esc")
        text _("Вход в игровое меню.")

    hbox:
        label _("Ctrl")
        text _("Пропускает диалоги, пока зажат.")

    hbox:
        label _("Tab")
        text _("Включает режим пропуска.")

    hbox:
        label _("Page Up")
        text _("Откат назад по сюжету игры.")

    hbox:
        label _("Page Down")
        text _("Откатывает предыдущее действие вперёд.")

    hbox:
        label "H"
        text _("Скрывает интерфейс пользователя.")

    hbox:
        label "S"
        text _("Делает снимок экрана.")

    hbox:
        label "V"
        text _("Включает поддерживаемый {a=https://www.renpy.org/l/voicing}синтезатор речи{/a}.")

    hbox:
        label "Shift+A"
        text _("Открывает меню специальных возможностей.")


screen mouse_help():

    hbox:
        label _("Левый клик")
        text _("Прохождение диалогов, активация интерфейса.")

    hbox:
        label _("Клик колёсиком")
        text _("Скрывает интерфейс пользователя.")

    hbox:
        label _("Правый клик")
        text _("Вход в игровое меню.")

    hbox:
        label _("Колёсико вверх")
        text _("Откат назад по сюжету игры.")

    hbox:
        label _("Колёсико вниз")
        text _("Откатывает предыдущее действие вперёд.")


screen gamepad_help():

    hbox:
        label _("Правый триггер\nA/Нижняя кнопка")
        text _("Прохождение диалогов, активация интерфейса.")

    hbox:
        label _("Левый Триггер\nЛевый Бампер")
        text _("Откат назад по сюжету игры.")

    hbox:
        label _("Правый бампер")
        text _("Откатывает предыдущее действие вперёд.")

    hbox:
        label _("Крестовина, Стики")
        text _("Навигация по интерфейсу.")

    hbox:
        label _("Старт, Гид, B/Правая кнопка")
        text _("Вход в игровое меню.")

    hbox:
        label _("Y/Верхняя кнопка")
        text _("Скрывает интерфейс пользователя.")

    textbutton _("Калибровка") action GamepadCalibrate()


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 12

style help_button_text:
    properties gui.text_properties("help_button")

style help_label:
    xsize 375
    right_padding 30

style help_label_text:
    size gui.text_size
    xalign 1.0
    textalign 1.0


################################################################################
## Дополнительные экраны
################################################################################

## Экран подтверждения #########################################################

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 75
            xysize (600, 450)

            label _(message):
                style "confirm_prompt"
                xalign 0.5
                yalign 0.5

            hbox:
                xalign 0.5
                spacing 120

                textbutton _("Да") action yes_action
                textbutton _("Нет") action no_action

    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    textalign 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.text_properties("confirm_button")


## Экран индикатора пропуска ###################################################

screen skip_indicator():
    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 9

            text _("Пропускаю")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    font "DejaVuSans.ttf"


## Экран уведомлений ###########################################################

screen notify(message):
    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")


## Экран NVL ###################################################################

screen nvl(dialogue, items=None):
    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):
    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    textalign gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    textalign gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    textalign gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.text_properties("nvl_button")


## Пузырьковый экран ###########################################################

screen bubble(who, what):
    style_prefix "bubble"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "bubble_namebox"

                text who:
                    id "who"

        text what:
            id "what"

        default ctc = None
        showif ctc:
            add ctc

style bubble_window is empty
style bubble_namebox is empty
style bubble_who is default
style bubble_what is default

style bubble_window:
    xpadding 30
    top_padding 5
    bottom_padding 5

style bubble_namebox:
    xalign 0.5

style bubble_who:
    xalign 0.5
    textalign 0.5
    color "#000"

style bubble_what:
    align (0.5, 0.5)
    text_align 0.5
    layout "subtitle"
    color "#000"

define bubble.frame = Frame("gui/bubble.png", 55, 55, 55, 95)
define bubble.thoughtframe = Frame("gui/thoughtbubble.png", 55, 55, 55, 55)

define bubble.properties = {
    "bottom_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "bottom_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "top_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "top_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "thought" : {
        "window_background" : bubble.thoughtframe,
    }
}

define bubble.expand_area = {
    "bottom_left" : (0, 0, 0, 22),
    "bottom_right" : (0, 0, 0, 22),
    "top_left" : (0, 22, 0, 0),
    "top_right" : (0, 22, 0, 0),
    "thought" : (0, 0, 0, 0),
}



################################################################################
## Мобильные варианты
################################################################################

style pref_vbox:
    variant "medium"
    xsize 675

screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu:

        hbox:
            style "quick_menu"
            style_prefix "quick"

            textbutton _("Назад") action Rollback()
            textbutton _("Пропуск") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Авто") action Preference("auto-forward", "toggle")
            textbutton _("Меню") action ShowMenu()


style window:
    variant "small"
    background "gui/phone/textbox.png"

style radio_button:
    variant "small"
    foreground "gui/phone/button/radio_[prefix_]foreground.png"

style check_button:
    variant "small"
    foreground "gui/phone/button/check_[prefix_]foreground.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_navigation_frame:
    variant "small"
    xsize 510

style game_menu_content_frame:
    variant "small"
    top_margin 0

style game_menu_viewport:
    variant "small"
    xsize 1305

style pref_vbox:
    variant "small"
    xsize 600

style bar:
    variant "small"
    ysize gui.bar_size
    left_bar Frame("gui/phone/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/phone/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    variant "small"
    xsize gui.bar_size
    top_bar Frame("gui/phone/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/phone/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    variant "small"
    ysize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    variant "small"
    xsize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    variant "small"
    ysize gui.slider_size
    base_bar Frame("gui/phone/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/horizontal_[prefix_]thumb.png"

style vslider:
    variant "small"
    xsize gui.slider_size
    base_bar Frame("gui/phone/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/vertical_[prefix_]thumb.png"

style slider_vbox:
    variant "small"
    xsize None

style slider_slider:
    variant "small"
    xsize 900

###########################################################################
###########################################################################

# Экран для ввода имени
screen input_name_screen():
    modal True
    
    # Затемненный фон
    add "#00000080"
    
    # Создаем переменную для хранения введенного текста
    default input_name = ""
    
    frame:
        style "input_frame"
        xalign 0.5
        yalign 0.5
        xsize 600
        ysize 350
        padding (30, 30)
        
        vbox:
            spacing 25
            xalign 0.5
            
            text "Как тебя зовут?":
                size 36
                color "#ff7171"
                font gui.interface_text_font
                xalign 0.5
                outlines [(2, "#a83c1f", 0, 0)]
            
            # Поле ввода с закругленными углами
            frame:
                style "input_field_frame"
                xysize (550, 60)
                xalign 0.5
                
                input:
                    id "name_input"
                    value ScreenVariableInputValue("input_name")
                    length 20
                    pixel_width 400
                    color "#ffffff"
                    font gui.interface_text_font
                    size 32
                    xalign 0.5
                    yalign 0.5
            
            # Кнопка для подтверждения
            textbutton "Продолжить":
                xalign 0.5
                style "input_confirm_button"
                action Return(input_name)
            
            text "Нажмите ENTER, чтобы продолжить":
                size 20
                color "#ff9083"
                font gui.interface_text_font
                xalign 0.5
                outlines [(2, "#de5d21", 0, 0)]
    
    key "K_RETURN" action Return(input_name)

init -1 python:
    # Добавляем стили для экрана ввода имени
    style.create("input_frame", "default")
    style.input_frame.background = Frame("gui/frame.png", 25, 25, 25, 25)
    style.input_frame.xalign = 0.5
    style.input_frame.yalign = 0.5
    
    style.create("input_field_frame", "default")
    style.input_field_frame.background = Frame("gui/button/choice_idle_background_1.png", 15, 15, 15, 15)
    style.input_field_frame.xysize = (500, 60)
    
    style.create("input_confirm_button", "button")
    style.input_confirm_button.background = Frame("gui/button/choice_idle_background_0.png", 15, 15, 15, 15)
    style.input_confirm_button.hover_background = Frame("gui/button/choice_hover_background_1.png", 15, 15, 15, 15)
    style.input_confirm_button.xsize = 450
    style.input_confirm_button.padding = (20, 10)
    
    style.create("input_confirm_button_text", "button_text")
    style.input_confirm_button_text.color = "#ffbf92"
    style.input_confirm_button_text.hover_color = "#ffffff"
    style.input_confirm_button_text.size = 24
    style.input_confirm_button_text.outlines = [(2, "#ff832b", 0, 0)]
    style.input_confirm_button_text.text_align = 0.5
    style.input_confirm_button_text.xalign = 0.5

################################################################################
## Экран перехода между главами
################################################################################

screen chapter_transition(old_chapter, new_chapter_title, new_chapter_subtitle):
    modal True
    zorder 200
    
    style_prefix "chapter_transition"
    
    # Затемненный фон
    add "#000000CC"
    
    frame:
        style "chapter_transition_frame"
        xalign 0.5
        yalign 0.5
        xsize 850
        ysize 550
        
        vbox:
            spacing 25
            xalign 0.5
            yalign 0.5
            
            text "Глава завершена" size 40 color "#ffffff" outlines [(3, "#671a1a", 0, 0)] xalign 0.5
            
            if old_chapter:
                text "[old_chapter]" size 30 color "#ffb995" outlines [(2, "#671a1a", 0, 0)] xalign 0.5
            
            null height 20
            
            text "Прогресс уже сохранен" size 28 color "#5e5e5e" xalign 0.5
            
            text "Вы можете продолжить или вернуться в меню" size 22 color "#888888" xalign 0.5
            
            null height 30
            
            # Проверяем, существует ли следующая глава
            $ next_chapter_exists = False
            if "Вторая" in new_chapter_title or "Новые знакомства" in new_chapter_title:
                $ next_chapter_exists = renpy.has_label("chapter_two")
            elif "Третья" in new_chapter_title or "Испытание" in new_chapter_title:
                $ next_chapter_exists = renpy.has_label("chapter_three")
            
            if next_chapter_exists:
                # Если глава существует, показываем обе кнопки
                hbox:
                    spacing 30
                    xalign 0.5
                    
                    textbutton "Да, продолжить":
                        style "chapter_transition_button"
                        action [Return(("continue", old_chapter, new_chapter_title, new_chapter_subtitle))]
                    
                    textbutton "Нет, выйти в главное меню":
                        style "chapter_transition_button"
                        action [Return(("exit", old_chapter))]
            else:
                # Если глава в разработке, показываем только одну кнопку
                textbutton "Выйти в главное меню":
                    style "chapter_transition_button"
                    xalign 0.5
                    action [Return(("exit", old_chapter))]
    
    key "K_RETURN" action If(next_chapter_exists, 
        true=Return(("continue", old_chapter, new_chapter_title, new_chapter_subtitle)), 
        false=Return(("exit", old_chapter)))
    key "K_ESCAPE" action Return(("exit", old_chapter))

## Стили для экрана перехода
style chapter_transition_frame:
    background Frame("gui/confirm_frame.png", 25, 25, 25, 25)
    padding (40, 40)

style chapter_transition_button:
    background Frame("gui/button/choice_idle_background.png", 15, 15, 15, 15)
    hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15, 15, 15)
    padding (30, 15)
    xsize 380

style chapter_transition_button_text:
    color "#ffffff"
    hover_color "#ff9e5e"
    outlines [(2, "#671a1a",0, 0)]
    size 18
    font gui.interface_text_font
    text_align 0.5