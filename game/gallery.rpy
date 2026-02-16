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
    
    # CG-арты можно добавить позже
    # gallery_items.append(GalleryItem("CG Название", "images/cg/example.png", "cg", "cg_unlock_key"))

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
                xalign 0.5
                
                textbutton _("Персонажи"):
                    style "gallery_tab_button"
                    action SetScreenVariable("selected_category", "characters")
                    selected (selected_category == "characters")
                
                textbutton _("Фоны"):
                    style "gallery_tab_button"
                    action SetScreenVariable("selected_category", "backgrounds")
                    selected (selected_category == "backgrounds")
                
                textbutton _("CG-арты"):
                    style "gallery_tab_button"
                    action SetScreenVariable("selected_category", "cg")
                    selected (selected_category == "cg")
            
            null height 10
            
            # Галерея изображений
            $ category_items = [item for item in gallery_items if item.category == selected_category]
            
            if category_items:
                vpgrid:
                    cols 3
                    spacing 30
                    yinitial 0.0
                    mousewheel True
                    draggable True
                    
                    for item in category_items:
                        button:
                            style "gallery_item_button"
                            
                            if item.is_unlocked():
                                frame:
                                    xysize (360, 250)
                                    background "#333333"
                                    
                                    vbox:
                                        # Миниатюра
                                        add Transform(item.image, zoom=0.5, xalign=0.5, yalign=0.5) xysize (340, 200)
                                        
                                        # Название
                                        text item.name:
                                            style "gallery_item_name"
                                            xalign 0.5
                                            yalign 0.5
                            
                            else:
                                frame:
                                    xysize (340, 250)
                                    background "#222222"
                                    
                                    vbox:
                                        text "🔒" size 100 xalign 0.6 yalign 1.0
                                        text _("Не разблокировано"):
                                            style "gallery_locked_text"
                                            xalign 0.5
                                            yalign 1.0
                            
                            # Действие при клике
                            if item.is_unlocked():
                                action Show("gallery_image_popup", image=item.image, title=item.name)
            else:
                text _("В этой категории пока нет изображений.") xalign 0.5

# Всплывающее окно для просмотра изображения
screen gallery_image_popup(image, title):
    modal True
    zorder 200
    
    frame:
        style "gallery_popup_frame"
        xysize (1600, 820)
        xalign 0.5
        yalign 0.5
        
        vbox:
            # Заголовок
            text title:
                style "gallery_popup_title"
                xalign 0.5
            
            # Изображение
            add Transform(image, zoom=0.8, xalign=0.5, yalign=0.5) ysize 700
            
            # Кнопка закрытия
            textbutton _("Закрыть"):
                style "gallery_close_button"
                xalign 0.5
                action Hide("gallery_image_popup")
    
    # Закрытие по клику вне окна
    key "game_menu" action Hide("gallery_image_popup")

# Стили для галереи
style gallery_tab_button:
    background Frame("gui/button/choice_idle_background.png", 10, 10, 10, 10)
    hover_background Frame("gui/button/choice_hover_background_1.png", 10, 10, 10, 10)
    selected_background Frame("gui/button/choice_hover_background_1.png", 10, 10, 10, 10)
    padding (20, 10)
    xysize (200, 50)
    mouse "hover"
    hover_mouse "hover"

style gallery_tab_button_text:
    color "#ffffff"
    hover_color "#FF7B4E"
    selected_color "#FF7B4E"
    size 24
    outlines [(2, "#000000", 0, 0)]
    text_align 0.5

style gallery_item_button:
    xysize (350, 250)
    padding (0, 0)
    background None

style gallery_item_name:
    size 20
    color "#ffffff"
    font gui.interface_text_font
    outlines [(1, "#000000", 0, 0)]
    xalign 0.5

style gallery_locked_text:
    size 18
    color "#808080"
    font gui.interface_text_font
    xalign 0.5
    yalign 1.0

style gallery_popup_frame:
    background Frame("gui/confirm_frame.png", 25, 25, 25, 25)
    padding (15, 15)

style gallery_popup_title:
    size 32
    color "#ffffff"
    font gui.interface_text_font
    outlines [(2, "#000000", 0, 0)]

style gallery_close_button:
    background Frame("gui/button/choice_idle_background.png", 10, 10, 10, 10)
    hover_background Frame("gui/button/choice_hover_background_1.png", 10, 10, 10, 10)
    padding (30, 10)
    xsize 200

style gallery_close_button_text:
    color "#ffffff"
    hover_color "#FF7B4E"
    size 24
    outlines [(2, "#000000", 0, 0)]
    text_align 0.5