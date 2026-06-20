################################################################################
## ИНИЦИАЛИЗАЦИЯ
################################################################################
init offset = -1

init python:
    import time
    import json
    import os

    # ========================================================================
    # ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
    # ========================================================================
    
    def safe_get_emotion_stats(user_id):
        try:
            if 'get_emotion_stats' in globals() and callable(get_emotion_stats):
                res = get_emotion_stats(user_id)
                if isinstance(res, dict):
                    return (
                        res.get('total_attempts', 0),
                        res.get('correct_matches', 0),
                        res.get('emotions_chosen', {})
                    )
        except:
            pass
        return (0, 0, {})

    def get_current_chapter_safe():
        try:
            if hasattr(store, 'current_chapter') and store.current_chapter:
                return store.current_chapter
        except:
            pass
        return "Глава Первая: Связь"
    
    def get_save_user_name(slot):
        try:
            slot_str = str(slot)
            if renpy.can_load(slot_str):
                save_json = renpy.json_load(renpy.slot_json_filename(slot_str))
                if save_json:
                    return save_json.get("user_name", "")
        except:
            pass
        return ""
    
    def get_save_chapter(slot):
        try:
            slot_str = str(slot)
            if renpy.can_load(slot_str):
                save_json = renpy.json_load(renpy.slot_json_filename(slot_str))
                if save_json:
                    chapter = save_json.get("chapter", "")
                    if "Первая" in chapter or "Связь" in chapter:
                        return "Глава 1"
                    elif "Вторая" in chapter or "Новые знакомства" in chapter:
                        return "Глава 2"
                    elif "Третья" in chapter:
                        return "Глава 3"
                    elif chapter:
                        return chapter[:20] + "..." if len(chapter) > 20 else chapter
        except:
            pass
        return ""

    # ========================================================================
    # СИСТЕМА СОХРАНЕНИЙ
    # ========================================================================
    
    def add_save_metadata(json_data):
        try:
            json_data["user_id"] = persistent.user_id if hasattr(persistent, 'user_id') else None
            json_data["user_name"] = persistent.user_name if hasattr(persistent, 'user_name') else ""
            json_data["chapter"] = get_current_chapter_safe()
            json_data["_timestamp"] = time.time()
            json_data["player_state"] = {
                "self_awareness": store.player_self_awareness if hasattr(store, 'player_self_awareness') else 0,
                "empathy": store.player_empathy if hasattr(store, 'player_empathy') else 0,
                "vocabulary": store.player_emotional_vocabulary if hasattr(store, 'player_emotional_vocabulary') else 0,
                "anxiety": store.player_anxiety_level if hasattr(store, 'player_anxiety_level') else 50,
                "trust": store.player_trust_level if hasattr(store, 'player_trust_level') else 30
            }
        except:
            pass
        return json_data

    if not hasattr(config, 'save_json_callbacks'):
        config.save_json_callbacks = []
    if add_save_metadata not in config.save_json_callbacks:
        config.save_json_callbacks.append(add_save_metadata)

    def custom_save_action(slot):
        try:
            renpy.save(str(slot))
            renpy.notify(f"Игра сохранена в слот {slot}")
            return True
        except Exception as e:
            renpy.notify(f"Ошибка сохранения: {str(e)}")
            return False

    def custom_load_action(slot):
        slot_str = str(slot)
        try:
            if renpy.can_load(slot_str):
                save_json = renpy.json_load(renpy.slot_json_filename(slot_str))
                current_user_id = persistent.user_id if hasattr(persistent, 'user_id') else None
                if save_json:
                    save_user_id = save_json.get("user_id")
                    if save_user_id is not None and save_user_id != current_user_id:
                        renpy.show_screen("confirm_user_switch", slot=slot)
                        return
                renpy.load(slot_str)
            else:
                renpy.notify(f"Слот {slot} пуст")
        except Exception as e:
            renpy.notify(f"Ошибка загрузки: {str(e)}")

    def load_latest_save():
        current_user_id = persistent.user_id if hasattr(persistent, 'user_id') else None
        
        latest_slot = None
        latest_time = 0
        slots_to_check = [str(i) for i in range(1, 10)] + [f"auto-{i}" for i in range(1, 10)] + ["quick-save"]
        
        for slot in slots_to_check:
            if renpy.can_load(slot):
                try:
                    save_json = renpy.json_load(renpy.slot_json_filename(slot))
                    if save_json:
                        save_user_id = save_json.get("user_id")
                        if save_user_id == current_user_id or current_user_id is None:
                            timestamp = save_json.get("_timestamp", 0)
                            if timestamp > latest_time:
                                latest_time = timestamp
                                latest_slot = slot
                except:
                    pass
                    
        if latest_slot:
            try:
                renpy.load(latest_slot)
            except Exception as e:
                renpy.notify(f"Ошибка загрузки: {str(e)}")
        else:
            renpy.notify("Нет сохранённой игры для текущего пользователя")

    def load_other_user_save(slot):
        try:
            slot_str = str(slot)
            if renpy.can_load(slot_str):
                save_json = renpy.json_load(renpy.slot_json_filename(slot_str))
                if save_json:
                    save_user_id = save_json.get("user_id")
                    save_user_name = save_json.get("user_name", "")
                    if save_user_id:
                        persistent.user_id = save_user_id
                        persistent.user_name = save_user_name
                        renpy.load(slot_str)
        except Exception as e:
            renpy.notify(f"Ошибка загрузки: {str(e)}")

    def delete_save(slot):
        try:
            renpy.unlink_save(str(slot))
            renpy.notify(f"Сохранение {slot} удалено")
        except Exception as e:
            renpy.notify(f"Ошибка удаления: {str(e)}")

################################################################################
## СТИЛИ (ОРИГИНАЛЬНЫЕ)
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

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style quick_button:
    properties gui.button_properties("quick_button")

style choice_button:
    properties gui.button_properties("choice_button")
    
################################################################################
## ВНУТРИИГРОВЫЕ ЭКРАНЫ
################################################################################
screen say(who, what):
    zorder 1
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

style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height
    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)
    padding (25, 20, 25, 20)

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
    outlines [(2, "#1a1a1a", 0, 0)]

style say_dialogue:
    properties gui.text_properties("dialogue")
    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos
    adjust_spacing False
    line_spacing 5
    outlines [(1, "#1a1a1a", 0, 0)]

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

screen choice(items):
    style_prefix "choice"
    vbox:
        for i in items:
            textbutton i.caption action i.action

style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5
    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.text_properties("choice_button")
    outlines [(1, "#2a1a0a", 0, 0)]
    line_spacing 3

screen quick_menu():
    zorder 100
    if True:
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

style quick_menu:
    xalign 0.5
    yalign 0.97

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.text_properties("quick_button")
    
################################################################################
## ЭКРАНЫ ГЛАВНОГО И ИГРОВОГО МЕНЮ
################################################################################
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
        textbutton _("Статистика") action ShowMenu("player_stats_screen")
        if _in_replay:
            textbutton _("Завершить повтор") action EndReplay(confirm=True)
        elif not main_menu:
            textbutton _("Главное меню") action MainMenu()
        textbutton _("Об игре") action ShowMenu("about")
        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):
            textbutton _("Помощь") action ShowMenu("help")
        if renpy.variant("pc"):
            textbutton _("Выход") action Quit(confirm=not main_menu)

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.text_properties("navigation_button")

screen main_menu():
    tag menu
    add "gui/main_menu.png"
    python:
        has_saves = False
        current_user_id = persistent.user_id if hasattr(persistent, 'user_id') else None
        slots_to_check = [str(i) for i in range(1, 10)] + [f"auto-{i}" for i in range(1, 10)] + ["quick-save"]
        for slot in slots_to_check:
            if renpy.can_load(slot):
                try:
                    save_json = renpy.json_load(renpy.slot_json_filename(slot))
                    if save_json:
                        save_user_id = save_json.get("user_id")
                        if save_user_id == current_user_id or current_user_id is None:
                            has_saves = True
                            break
                except:
                    pass
    if gui.show_name:
        text "[config.name!t]":
            style "main_menu_title"
    text "Версия [config.version]":
        style "main_menu_version"
        at transform:
            alpha 0.5
    frame:
        style "main_menu_frame"
        xalign 0.5
        yalign 0.5
        xsize 500
        ysize 650
        background Frame("gui/choice_idle_background.png", 25, 25)
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 1
            if has_saves:
                textbutton _("Продолжить"):
                    style "main_menu_button"
                    action Function(load_latest_save)
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
    button:
        style "players_button"
        action ShowMenu("debug_database")

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
    background Frame("gui/button/choice_idle_background.png", 15, 15)
    hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)

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
    background Frame("gui/button/choice_idle_background_3.png", 15, 15)
    hover_background Frame("gui/button/choice_hover_background_2.png", 15, 15)
    padding (20, 20)

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

################################################################################
## ЭКРАН ОБ ИГРЕ
################################################################################
screen about():
    tag menu
    use game_menu(_("Об игре"), scroll="viewport"):
        style_prefix "about"
        vbox:
            label "[config.name!t]"
            text "Версия [config.version!t]\n"
            if gui.about:
                text "[gui.about!t]\n"
            text "Сделано с помощью {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"

style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text
style about_label_text:
    size gui.label_text_size
################################################################################
## ЭКРАН ПОМОЩИ
################################################################################
screen help():
    tag menu
    default device = "keyboard"
    use game_menu(_("Помощь"), scroll="viewport"):
        vbox:
            spacing 25
            
            text "Управление игрой":
                size 36
                color gui.accent_color
                xalign 0.5
                outlines [(2, "#671a1a", 0, 0)]
            
            null height 10
            
            frame:
                background Frame("gui/confirm_frame.png", 15, 15)
                xfill True
                padding (25, 25)
                
                vbox:
                    spacing 25
                    xfill True
                    
                    text "Клавиатура и мышь":
                        size 28
                        color gui.accent_color
                        xalign 0.05
                        outlines [(1, "#671a1a", 0, 0)]
                    
                    hbox:
                        spacing 20
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        text "Ввод/Продолжить:" size 24 xsize 300 yalign 0.5 text_align 0.0
                        text "ЛКМ, Пробел, Enter" size 24 color "#915d49" xsize 400
                    
                    hbox:
                        spacing 20
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        text "Пропустить диалог:" size 24 xsize 300 yalign 0.5 text_align 0.0
                        text "Нажмите кнопку 'Пропуск' в быстром меню" size 24 color "#915d49" xsize 400
                    
                    hbox:
                        spacing 20
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        text "Скрыть окно диалога:" size 24 xsize 300 yalign 0.5 text_align 0.0
                        text "ПКМ, H" size 24 color "#915d49" xsize 400
                    
                    hbox:
                        spacing 20
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        text "Сделать скриншот:" size 24 xsize 300 yalign 0.5 text_align 0.0
                        text "S" size 24 color "#915d49" xsize 400
                    
                    hbox:
                        spacing 20
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        text "Открыть меню:" size 24 xsize 300 yalign 0.5 text_align 0.0
                        text "Esc, ПКМ" size 24 color "#915d49" xsize 400
                    
                    hbox:
                        spacing 20
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        text "Быстрое сохранение:" size 24 xsize 300 yalign 0.5 text_align 0.0
                        text "F5" size 24 color "#915d49" xsize 400
                    
                    hbox:
                        spacing 20
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        text "Быстрая загрузка:" size 24 xsize 300 yalign 0.5 text_align 0.0
                        text "F8" size 24 color "#915d49" xsize 400
                    
                    hbox:
                        spacing 20
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        text "Громкость (+/-):" size 24 xsize 300 yalign 0.5 text_align 0.0
                        text "PageUp / PageDown" size 24 color "#915d49" xsize 400
                    
                    hbox:
                        spacing 20
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        text "Полноэкранный режим:" size 24 xsize 300 yalign 0.5 text_align 0.0
                        text "F11" size 24 color "#915d49" xsize 400
                    
                    null height 10
                    frame:
                        xsize 1000
                        ysize 4
                        xalign 0.5
                        background "#ac5032"
                    null height 10
                    
                    text "Советы":
                        size 28
                        color gui.accent_color
                        xalign 0.05
                        outlines [(1, "#671a1a", 0, 0)]
                    
                    text "• Обращай внимание на телесные ощущения персонажей — они помогут распознавать эмоции.":
                        size 22
                        xsize 1000
                        xalign 0.5
                        text_align 0.1
                    
                    text "• В мини-игре «Колесо эмоций» выбирай эмоцию, которая лучше всего описывает ситуацию.":
                        size 22
                        xsize 1000
                        xalign 0.5
                        text_align 0.1
                    
                    text "• Дневник наблюдений помогает развивать эмоциональный интеллект.":
                        size 22
                        xsize 1000
                        xalign 0.5
                        text_align 0.1
                    
                    text "• Твои решения влияют на отношения с персонажами и доступные достижения.":
                        size 22
                        xsize 1000
                        xalign 0.5
                        text_align 0.1
            
            null height 25
            
            textbutton "Закрыть":
                xalign 0.5
                background Frame("gui/button/choice_idle_background_0.png", 15, 15)
                hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                padding (35, 15)
                xsize 300
                action Return()
################################################################################
## ЭКРАН НАСТРОЕК (ОПЦИЙ)
################################################################################
screen preferences():
    tag menu
    use game_menu(_("Настройки"), scroll="viewport"):
        vbox:
            spacing 25
            xfill True
            
            text "Настройки игры":
                size 36
                color gui.accent_color
                xalign 0.5
                outlines [(2, "#671a1a", 0, 0)]
            
            null height 10
            
            # ОДИН ОБЩИЙ ФРЕЙМ ДЛЯ ВСЕХ НАСТРОЕК
            frame:
                background Frame("gui/confirm_frame.png", 15, 15)
                xfill True
                padding (25, 20)
                
                vbox:
                    spacing 25
                    xfill True
                    
                    # ============================================
                    # ГРАФИКА И ЗВУК
                    # ============================================
                    text "Графика и звук":
                        size 28
                        color gui.accent_color
                        xalign 0.05
                        outlines [(1, "#671a1a", 0, 0)]
                    
                    hbox:
                        spacing 30
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        
                        text "Режим экрана:":
                            size 24
                            xsize 280
                            yalign 0.5
                            text_align 0.0
                        
                        textbutton "Оконный":
                            action Preference("display", "window")
                            xsize 180
                            text_align 0.5
                        
                        textbutton "Полный":
                            action Preference("display", "fullscreen")
                            xsize 180
                            text_align 0.5
                    
                    null height 5
                    
                    hbox:
                        spacing 30
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        
                        text "Громкость музыки:":
                            size 24
                            xsize 280
                            yalign 0.5
                            text_align 0.0
                        
                        bar:
                            value Preference("music volume")
                            xsize 500
                            ysize 25
                            xalign 0.0
                    
                    hbox:
                        spacing 30
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        
                        text "Громкость звуков:":
                            size 24
                            xsize 280
                            yalign 0.5
                            text_align 0.0
                        
                        bar:
                            value Preference("sound volume")
                            xsize 500
                            ysize 25
                            xalign 0.0
                    
                    hbox:
                        spacing 30
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        
                        text "Громкость голоса:":
                            size 24
                            xsize 280
                            yalign 0.5
                            text_align 0.0
                        
                        bar:
                            value Preference("voice volume")
                            xsize 500
                            ysize 25
                            xalign 0.0
                    
                    # Разделитель
                    null height 10
                    frame:
                        xsize 1000
                        ysize 4
                        xalign 0.5
                        background "#ac5032"
                    null height 10
                    
                    # ============================================
                    # ТЕКСТ И УПРАВЛЕНИЕ
                    # ============================================
                    text "Текст и управление":
                        size 28
                        color gui.accent_color
                        xalign 0.05
                        outlines [(1, "#671a1a", 0, 0)]
                    
                    hbox:
                        spacing 30
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        
                        text "Скорость текста:":
                            size 24
                            xsize 280
                            yalign 0.5
                            text_align 0.0
                        
                        bar:
                            value Preference("text speed")
                            xsize 500
                            ysize 25
                            xalign 0.0
                        
                        # ОТОБРАЖЕНИЕ ЦЕЛОГО ЧИСЛА (без десятичных)
                        $ text_speed = int(preferences.text_cps)
                        text "[text_speed]":
                            size 20
                            xsize 80
                            yalign 0.5
                            text_align 0.5
                            color "#b4744e"
                    
                    hbox:
                        spacing 30
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        
                        text "Авто-чтение:":
                            size 24
                            xsize 280
                            yalign 0.5
                            text_align 0.0
                        
                        bar:
                            value Preference("auto-forward time")
                            xsize 500
                            ysize 25
                            xalign 0.0
                        
                        # Отображение времени авто-чтения с одним знаком после запятой
                        $ auto_time = preferences.afm_time
                        text "[auto_time:.1f] сек/символ":
                            size 20
                            xsize 120
                            yalign 0.5
                            text_align 0.5
                            color "#b4744e"
                    
                    null height 5
                    
                    hbox:
                        spacing 30
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        
                        text "Пропуск:":
                            size 24
                            xsize 280
                            yalign 0.5
                            text_align 0.0
                        
                        textbutton "Непрочитанный":
                            action Preference("skip", "seen")
                            xsize 180
                            text_align 0.5
                        
                        textbutton "Весь текст":
                            action Preference("skip", "all")
                            xsize 180
                            text_align 0.5
                    
                    hbox:
                        spacing 30
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        
                        text "После выбора:":
                            size 24
                            xsize 280
                            yalign 0.5
                            text_align 0.0
                        
                        textbutton "Останавливать":
                            action Preference("after choices", "stop")
                            xsize 180
                            text_align 0.5
                        
                        textbutton "Продолжать":
                            action Preference("after choices", "skip")
                            xsize 180
                            text_align 0.5
                    
                    # Разделитель
                    null height 10
                    frame:
                        xsize 1000
                        ysize 4
                        xalign 0.5
                        background "#ac5032"
                    null height 10
                    
                    # ============================================
                    # СИСТЕМА
                    # ============================================
                    text "Система":
                        size 28
                        color gui.accent_color
                        xalign 0.05
                        outlines [(1, "#671a1a", 0, 0)]
                    
                    hbox:
                        spacing 30
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        
                        text "Язык:":
                            size 24
                            xsize 280
                            yalign 0.5
                            text_align 0.0
                        
                        textbutton "Русский":
                            action Language(None)
                            xsize 180
                            text_align 0.5
                        
                        textbutton "English":
                            action Language("english")
                            xsize 180
                            text_align 0.5
                    
                    null height 5
                    
                    hbox:
                        spacing 30
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        
                        text "Сброс настроек:":
                            size 24
                            xsize 280
                            yalign 0.5
                            text_align 0.0
                        
                        textbutton "Сбросить всё":
                            action Preference("reset")
                            xsize 500
                            text_align 0.5
            
            null height 15
            
            textbutton "Закрыть":
                xalign 0.5
                background Frame("gui/button/choice_idle_background_0.png", 15, 15)
                hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                padding (35, 15)
                xsize 300
                action Return()

################################################################################
## ЭКРАН ИСТОРИИ
################################################################################
screen history():
    tag menu
    predict False
    use game_menu(_("История"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0):
        style_prefix "history"
        
        for h in _history_list:
            window:
                style "history_window"
                has fixed:
                    if h.who:
                        label h.who:
                            style "history_name"
                            substitute False
                            if "color" in h.who_args:
                                text_color h.who_args["color"]
                    $ what_text = h.what
                    text "[what_text!t]" style "history_text"
        if not _history_list:
            label _("История пуста.")

style history_window is empty
style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text
style history_text is gui_text
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
    text_align gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    text_align gui.history_text_xalign

################################################################################
## ЭКРАНЫ ЗАГРУЗКИ И СОХРАНЕНИЯ
################################################################################
screen save():
    tag menu
    use file_slots_with_user(_("Сохранить"), is_save=True)

screen load():
    tag menu
    use file_slots_with_user(_("Загрузить"), is_save=False)

screen file_slots_with_user(title, is_save=True):
    default page_name_value = FilePageNameInputValue(pattern=_("{} страница"), auto=_("Автосохранения"), quick=_("Быстрые сохранения"))
    
    use game_menu(title):
        fixed:
            yoffset 80
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
                    $ slot_exists = renpy.can_load(str(slot))
                    button:
                        if is_save:
                            action Function(custom_save_action, slot)
                        elif slot_exists:
                            action Function(custom_load_action, slot)
                        else:
                            action NullAction()
                        has vbox
                        frame:
                            xysize (config.thumbnail_width, config.thumbnail_height)
                            background Frame("gui/confirm_frame.png", 15, 15)
                            if slot_exists:
                                $ thumbnail = FileScreenshot(slot)
                                if thumbnail:
                                    add thumbnail xalign 0.5 yalign 0.5
                                else:
                                    text "Нет\nскриншота":
                                        size 20
                                        xalign 0.5
                                        yalign 0.5
                                        color "#666666"
                            else:
                                text "Пустой\nслот":
                                    size 20
                                    xalign 0.5
                                    yalign 0.5
                                    color "#666666"
                        $ file_time = FileTime(slot, format=_("{#file_time}%d.%m.%Y %H:%M"), empty=_("Пустой слот"))
                        if file_time:
                            text "[file_time]":
                                style "slot_time_text"
                        $ file_name = FileSaveName(slot)
                        if file_name:
                            text "[file_name]":
                                style "slot_name_text"
                        $ save_user = get_save_user_name(slot)
                        if save_user:
                            text "Игрок: [save_user]":
                                style "slot_user_text"
                        $ save_chapter = get_save_chapter(slot)
                        if save_chapter:
                            text "Глава: [save_chapter]":
                                style "slot_chapter_text"
                        if slot_exists and not is_save:
                            key "save_delete" action Function(delete_save, slot)
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

################################################################################
## ЭКРАН СТАТИСТИКИ ИГРОКА - ОДИН ФРЕЙМ
################################################################################
screen player_stats_screen():
    tag menu
    use game_menu(_("Статистика игрока"), scroll="viewport"):
        vbox:
            spacing 25
            xfill True
            
            text "Твой эмоциональный интеллект":
                size 36
                color gui.accent_color
                xalign 0.5
                outlines [(2, "#671a1a", 0, 0)]
            
            null height 10
            
            # ОДИН ОБЩИЙ ФРЕЙМ ДЛЯ ВСЕЙ СТАТИСТИКИ
            frame:
                background Frame("gui/confirm_frame.png", 15, 15)
                xfill True
                padding (25, 20)
                
                vbox:
                    spacing 25
                    xfill True
                    
                    # ============================================
                    # ОСНОВНЫЕ ПОКАЗАТЕЛИ
                    # ============================================
                    text "Основные показатели":
                        size 28
                        color gui.accent_color
                        xalign 0.05
                        outlines [(1, "#671a1a", 0, 0)]
                    
                    # Понимание своих эмоций
                    hbox:
                        spacing 30
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        
                        text "Понимание своих эмоций:":
                            size 24
                            xsize 400
                            yalign 0.5
                            text_align 0.0
                        
                        bar:
                            value player_self_awareness
                            range 100
                            xsize 500
                            ysize 30
                            left_bar "#c66b2f"
                            right_bar "#3a3a3a"
                            xalign 0.0
                        
                        text "[player_self_awareness]%":
                            size 20
                            xsize 80
                            yalign 0.5
                            text_align 0.5
                    
                    # Понимание чужих эмоций (эмпатия)
                    hbox:
                        spacing 30
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        
                        text "Понимание чужих эмоций (эмпатия):":
                            size 24
                            xsize 400
                            yalign 0.5
                            text_align 0.0
                        
                        bar:
                            value player_empathy
                            range 100
                            xsize 500
                            ysize 30
                            left_bar "#c66b2f"
                            right_bar "#3a3a3a"
                            xalign 0.0
                        
                        text "[player_empathy]%":
                            size 20
                            xsize 80
                            yalign 0.5
                            text_align 0.5
                    
                    # Эмоциональный словарь
                    hbox:
                        spacing 30
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        
                        text "Эмоциональный словарь:":
                            size 24
                            xsize 400
                            yalign 0.5
                            text_align 0.0
                        
                        bar:
                            value player_emotional_vocabulary
                            range 100
                            xsize 500
                            ysize 30
                            left_bar "#c66b2f"
                            right_bar "#3a3a3a"
                            xalign 0.0
                        
                        text "[player_emotional_vocabulary]%":
                            size 20
                            xsize 80
                            yalign 0.5
                            text_align 0.5
                    
                    # Уровень тревожности
                    hbox:
                        spacing 30
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        
                        text "Уровень тревожности:":
                            size 24
                            xsize 400
                            yalign 0.5
                            text_align 0.0
                        
                        bar:
                            value player_anxiety_level
                            range 100
                            xsize 500
                            ysize 30
                            left_bar "#ff6666"
                            right_bar "#3a3a3a"
                            xalign 0.0
                        
                        text "[player_anxiety_level]%":
                            size 20
                            xsize 80
                            yalign 0.5
                            text_align 0.5
                    
                    # Уровень доверия
                    hbox:
                        spacing 30
                        xfill True
                        xalign 0.5
                        xmaximum 1100
                        
                        text "Уровень доверия:":
                            size 24
                            xsize 400
                            yalign 0.5
                            text_align 0.0
                        
                        bar:
                            value player_trust_level
                            range 100
                            xsize 500
                            ysize 30
                            left_bar "#4caf50"
                            right_bar "#3a3a3a"
                            xalign 0.0
                        
                        text "[player_trust_level]%":
                            size 20
                            xsize 80
                            yalign 0.5
                            text_align 0.5
                    
                    # Разделитель
                    null height 10
                    frame:
                        xsize 1000
                        ysize 4
                        xalign 0.5
                        background "#ac5032"
                    null height 10
                    
                    # ============================================
                    # СТАТИСТИКА МИНИ-ИГРЫ
                    # ============================================
                    if persistent.user_id:
                        $ stats_total_attempts, stats_correct_matches, stats_emotions_chosen = safe_get_emotion_stats(persistent.user_id)
                        
                        text "Статистика мини-игры «Колесо эмоций»:":
                            size 28
                            color gui.accent_color
                            xalign 0.05
                            outlines [(1, "#671a1a", 0, 0)]
                        
                        hbox:
                            spacing 50
                            xfill True
                            xalign 0.5
                            xmaximum 1100
                            
                            vbox:
                                xalign 0.5
                                spacing 5
                                
                                text "Всего попыток:":
                                    size 22
                                    text_align 0.5
                                    xalign 0.5
                                
                                text "[stats_total_attempts]":
                                    size 28
                                    color "#c66b2f"
                                    xalign 0.5
                                    text_align 0.5
                            
                            vbox:
                                xalign 0.5
                                spacing 5
                                
                                text "Правильных ответов:":
                                    size 22
                                    text_align 0.5
                                    xalign 0.5
                                
                                text "[stats_correct_matches]":
                                    size 28
                                    color "#4caf50"
                                    xalign 0.5
                                    text_align 0.5
                            
                            vbox:
                                xalign 0.5
                                spacing 5
                                
                                text "Точность:":
                                    size 22
                                    text_align 0.5
                                    xalign 0.5
                                
                                $ accuracy = int((stats_correct_matches / max(stats_total_attempts, 1)) * 100)
                                text "[accuracy]%":
                                    size 28
                                    color "#ffaa00"
                                    xalign 0.5
                                    text_align 0.5
                        
                        if stats_emotions_chosen:
                            null height 10
                            
                            text "Частота выбора эмоций:":
                                size 22
                                xalign 0.05
                            
                            $ sorted_emotions = sorted(stats_emotions_chosen.items(), key=lambda x: x[1], reverse=True)[:5]
                            
                            # Отображение эмоций в виде списка
                            for emotion, count in sorted_emotions:
                                hbox:
                                    spacing 30
                                    xfill True
                                    xalign 0.5
                                    xmaximum 1100
                                    
                                    text "• [emotion]:":
                                        size 20
                                        color "#b4744e"
                                        xsize 300
                                        text_align 0.0
                                    
                                    # Мини-бар для визуализации частоты
                                    $ max_count = sorted_emotions[0][1] if sorted_emotions else 1
                                    $ bar_width = int((count / max_count) * 300)
                                    
                                    frame:
                                        xsize 300
                                        ysize 20
                                        
                                        frame:
                                            xsize bar_width
                                            ysize 20
                                            background "#c66b2f"
                                    
                                    text "[count] раз":
                                        size 20
                                        color "#b4744e"
                                        xsize 100
                                        text_align 0.5
                    else:
                        text "Нет данных для статистики":
                            size 22
                            color "#844646"
                            xalign 0.5
            
            null height 15
            
            textbutton "Закрыть":
                xalign 0.5
                background Frame("gui/button/choice_idle_background_0.png", 15, 15)
                hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                padding (35, 15)
                xsize 300
                action Return()

################################################################################
## ЭКРАН ДЛЯ ВВОДА ИМЕНИ (ОРИГИНАЛЬНЫЙ СТИЛЬ)
################################################################################
screen input_name_screen():
    modal True
    default input_name = ""
    frame:
        style "input_frame"
        xalign 0.5
        yalign 0.5
        xsize 600
        ysize 400
        padding (30, 30)
        vbox:
            spacing 25
            xalign 0.5
            text "Как тебя зовут?":
                size 36
                color "#ce5454"
                font gui.interface_text_font
                xalign 0.5
                outlines [(2, "#a83c1f", 0, 0)]
            frame:
                style "input_field_frame"
                xysize (540, 70)
                xalign 0.5
                background Frame("gui/button/choice_idle_background_1.png", 15, 15)
                input:
                    id "name_input"
                    value ScreenVariableInputValue("input_name")
                    length 20
                    color "#ffffff"
                    font gui.interface_text_font
                    size 32
                    xalign 0.5
                    yalign 0.5
            textbutton "Продолжить":
                xalign 0.5
                style "input_confirm_button"
                action Return(input_name)
            text "Нажмите ENTER, чтобы продолжить":
                size 18
                color "#ca6358"
                font gui.interface_text_font
                xalign 0.5

        key "K_RETURN" action Return(input_name)
    key "K_ESCAPE" action Return("")

init -1 python:
    style.create("input_frame", "default")
    style.input_frame.background = Frame("gui/confirm_frame.png", 25, 25)
    style.input_frame.xalign = 0.5
    style.input_frame.yalign = 0.5
    style.create("input_field_frame", "default")
    style.input_field_frame.background = Frame("gui/button/choice_idle_background_1.png", 15, 15)
    style.input_field_frame.xysize = (500, 60)
    style.create("input_confirm_button", "button")
    style.input_confirm_button.background = Frame("gui/button/choice_idle_background_0.png", 15, 15)
    style.input_confirm_button.hover_background = Frame("gui/button/choice_hover_background_1.png", 15, 15)
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
## ЭКРАН ПОДТВЕРЖДЕНИЯ ПЕРЕКЛЮЧЕНИЯ ПОЛЬЗОВАТЕЛЯ
################################################################################
screen confirm_user_switch(slot):
    modal True
    zorder 200
    add "gui/overlay/confirm.png"
    frame:
        style "confirm_frame"
        xalign 0.5
        yalign 0.5
        xsize 600
        ysize 400
        vbox:
            spacing 25
            xalign 0.5
            yalign 0.5
            text "ВНИМАНИЕ":
                size 36
                color "#ff7171"
                xalign 0.5
            text "Это сохранение принадлежит другому игроку.":
                size 24
                xalign 0.5
                text_align 0.5
            text "Загрузка переключит текущего пользователя.":
                size 24
                xalign 0.5
                text_align 0.5
            null height 20
            hbox:
                spacing 30
                xalign 0.5
                textbutton "Загрузить":
                    action [Function(load_other_user_save, slot), Hide("confirm_user_switch")]
                    background Frame("gui/button/choice_idle_background.png", 15, 15)
                    hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                    padding (15, 10)
                textbutton "Отмена":
                    action Hide("confirm_user_switch")
                    background Frame("gui/button/choice_idle_background.png", 15, 15)
                    hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                    padding (15, 10)
    key "K_ESCAPE" action Hide("confirm_user_switch")
    key "game_menu" action Hide("confirm_user_switch")

################################################################################
## СТИЛИ ДЛЯ СЛОТОВ СОХРАНЕНИЯ
################################################################################
style slot_time_text:
    color "#c66b2f"
    size 16
    font gui.interface_text_font
    xalign 0.5
    outlines [(1, "#1a1a1a", 0, 0)]

style slot_name_text:
    color "#ffffff"
    size 18
    font gui.interface_text_font
    xalign 0.5
    outlines [(1, "#1a1a1a", 0, 0)]

style slot_user_text:
    color "#aaaaaa"
    size 14
    font gui.interface_text_font
    xalign 0.5

style slot_chapter_text:
    color "#ffaa66"
    size 14
    font gui.interface_text_font
    xalign 0.5

style page_label:
    xpadding 10
    ypadding 5
    xalign 0.5

style page_label_text:
    size 24
    color gui.accent_color
    outlines [(1, "#671a1a", 0, 0)]

style confirm_frame:
    background Frame("gui/confirm_frame.png", 25, 25)
    padding (30, 30)
    xalign 0.5
    yalign 0.5
    xsize 600
    ysize 400