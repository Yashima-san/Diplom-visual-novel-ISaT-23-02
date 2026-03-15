################################################################################
## Галерея
################################################################################

init python:
    class GalleryItem:
        def __init__(self, name, image, category, unlock_condition=None):
            self.name = name
            self.image = image
            self.category = category
            self.unlock_condition = unlock_condition
        
        def is_unlocked(self):
            if self.unlock_condition is None:
                return True
            # Проверяем, что persistent._gallery_unlocks - словарь
            if not isinstance(persistent._gallery_unlocks, dict):
                return False
            return persistent._gallery_unlocks.get(self.unlock_condition, False)
    
    # Инициализация persistent для галереи
    if not hasattr(persistent, '_gallery_unlocks') or persistent._gallery_unlocks is None:
        persistent._gallery_unlocks = {}
    else:
        # Если уже существует, но это не словарь, конвертируем или создаем новый
        if not isinstance(persistent._gallery_unlocks, dict):
            old_data = persistent._gallery_unlocks
            persistent._gallery_unlocks = {}
            # Если это было множество с разблокированными элементами
            if isinstance(old_data, set):
                for item_key in old_data:
                    persistent._gallery_unlocks[item_key] = True
    
    # Функция для разблокировки элемента галереи
    def unlock_gallery_item(key):
        # Проверяем, что persistent._gallery_unlocks - словарь
        if not isinstance(persistent._gallery_unlocks, dict):
            persistent._gallery_unlocks = {}
        persistent._gallery_unlocks[key] = True
    
    # Словарь для хранения элементов галереи
    gallery_items = []
    
    # Добавление элементов в галерею
    gallery_items.append(GalleryItem(
        "Лина", 
        "images/characters/lina.png", 
        "characters",
        "meet_lina"
    ))

    gallery_items.append(GalleryItem(
        "[persistent.user_name]", 
        "images/characters/user.png", 
        "characters",
        "meet_user"
    ))

    gallery_items.append(GalleryItem(
        "Комната вечером", 
        "images/room_evening.png",
        "backgrounds",
        "room_evening"
    ))
    
    gallery_items.append(GalleryItem(
        "Комната закат", 
        "images/room_pk_light.png",
        "backgrounds",
        "room_pk_light"
    ))
    
    gallery_items.append(GalleryItem(
        "Комната", 
        "images/room_pk.png",
        "backgrounds",
        "room_pk"
    ))
    
    gallery_items.append(GalleryItem(
        "Школа", 
        "images/school_entrance.png",
        "backgrounds",
        None
    ))
    
    gallery_items.append(GalleryItem(
        "Кухня", 
        "images/kitchen.png",
        "backgrounds",
        None
    ))
    
    gallery_items.append(GalleryItem(
        "Улица", 
        "images/street.png",
        "backgrounds",
        None
    ))
    
    gallery_items.append(GalleryItem(
        "Ночная комната", 
        "images/night_room.png",
        "backgrounds",
        None
    ))

    gallery_items.append(GalleryItem(
        "Ночная комната", 
        "images/cg/room_day.png",
        "cg",
        None
    ))

# Экран галереи
screen gallery():
    tag menu
    
    default selected_category = "characters"
    
    use game_menu(_("Карточки")):
        vbox:
            spacing 20
            
            # Вкладки категорий
            hbox:
                spacing 10
                xalign 0.6
                
                textbutton _("Персонажи"):
                    action SetScreenVariable("selected_category", "characters")
                    selected (selected_category == "characters")
                
                textbutton _("Фоны"):
                    action SetScreenVariable("selected_category", "backgrounds")
                    selected (selected_category == "backgrounds")
                
                textbutton _("CG-арты"):
                    action SetScreenVariable("selected_category", "cg")
                    selected (selected_category == "cg")
            
            null height 10
            
            # Галерея изображений
            $ category_items = [item for item in gallery_items if item.category == selected_category]
            
            if category_items:
                vpgrid:
                    cols 3
                    spacing 40
                    yinitial 0.5
                    mousewheel True
                    draggable True
                    xpos 50
                    
                    for item in category_items:
                        if item.is_unlocked():
                            button:
                                xysize (350, 250)
                                background None
                                action Show("gallery_image_popup", image=item.image, title=item.name)
                                
                                frame:
                                    xysize (360, 250)
                                    background Frame("gui/confirm_frame.png", 0, 0, 0, 0)
                                    
                                    vbox:
                                        xalign 0.5
                                        yalign 0.5
                                        
                                        # Проверяем существование файла перед отображением
                                        $ image_exists = renpy.loadable(item.image) if item.image else False
                                        if image_exists:
                                            add Transform(item.image, zoom=0.2, xalign=0.5, yalign=0.5) xysize (300, 160)
                                        else:
                                            text "Изображение\nне найдено" size 20 xalign 0.5 yalign 0.5
                                        
                                        # Название
                                        text item.name:
                                            color "#ffffff"
                                            size 20
                                            font gui.interface_text_font
                                            outlines [(2, "#5e1414", 0, 0)]
                                            xalign 0.5
                                            yalign 0.2
                        else:
                            button:
                                xysize (350, 250)
                                background None
                                
                                frame:
                                    xysize (340, 250)
                                    background Frame("gui/confirm_frame.png", 0, 0)

                                    vbox:
                                        xalign 0.5
                                        yalign 0.3

                                        text "🔒" size 80 xalign 0.5 yalign 1.0
                                        text _("Не разблокировано"):
                                            color "#8f4e36"
                                            size 18
                                            font gui.interface_text_font
                                            xalign 0.5
                                            yalign 0.45
            else:
                text _("В этой категории пока нет изображений.") xalign 0.5

# Всплывающее окно для просмотра изображения
screen gallery_image_popup(image, title):
    modal True
    zorder 200
    add "gui/overlay/confirm.png"
    
    frame:
        background Frame("gui/confirm_frame.png", 25, 25)
        padding (35, 35)
        xysize (1600, 920)
        xalign 0.5
        yalign 0.5
        
        vbox:
            xalign 0.5
            yalign 0.5
            
            # Заголовок
            text title:
                color "#ffffff"
                size 32
                font gui.interface_text_font
                outlines [(2, "#711b1b", 0, 0)]
                xalign 0.5
            
            # Изображение
            $ image_exists = renpy.loadable(image) if image else False
            if image_exists:
                add Transform(image, zoom=0.8, xalign=0.5, yalign=0.5) xsize 1170 ysize 620
            else:
                text "Изображение не найдено:\n[image]" size 30 xalign 0.5 yalign 0.5
            
            # Кнопка закрытия
            textbutton _("Закрыть"):
                xalign 0.5
                ypos 50
                background Frame("gui/button/choice_idle_background.png", 10, 10, 10, 10)
                hover_background Frame("gui/button/choice_hover_background_1.png", 10, 10, 10, 10)
                padding (30, 10)
                xsize 250
                action Hide("gallery_image_popup")
                text_style "gallery_close_button_text"
    
    # Закрытие по клику вне окна
    key "game_menu" action Hide("gallery_image_popup")

# Стили для галереи
style gallery_tab_button:
    background Frame("gui/button/choice_idle_background.png", 10, 10, 10, 10)
    hover_background Frame("gui/button/choice_hover_background_1.png", 10, 10, 10, 10)
    selected_background Frame("gui/button/choice_hover_background_1.png", 10, 10, 10, 10)
    padding (20, 10)
    xysize (200, 50)

style gallery_tab_button_text:
    color "#ffffff"
    hover_color "#FF7B4E"
    selected_color "#FF7B4E"
    size 24
    outlines [(2, "#671a1a", 0, 0)]
    text_align 0.5

style gallery_close_button_text:
    color "#ffffff"
    hover_color "#FF7B4E"
    size 24
    outlines [(2, "#671a1a", 0, 0)]
    text_align 0.5