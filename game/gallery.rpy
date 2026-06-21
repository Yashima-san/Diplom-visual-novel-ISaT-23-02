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
            # Если нет условия разблокировки - НЕ РАЗБЛОКИРОВАНО
            if self.unlock_condition is None:
                return False
            if not isinstance(persistent._gallery_unlocks, dict):
                return False
            return persistent._gallery_unlocks.get(self.unlock_condition, False)
    
    if not hasattr(persistent, '_gallery_unlocks') or persistent._gallery_unlocks is None:
        persistent._gallery_unlocks = {}
    else:
        if not isinstance(persistent._gallery_unlocks, dict):
            old_data = persistent._gallery_unlocks
            persistent._gallery_unlocks = {}
            if isinstance(old_data, set):
                for item_key in old_data:
                    persistent._gallery_unlocks[item_key] = True
    
    def unlock_gallery_item(key):
        if not isinstance(persistent._gallery_unlocks, dict):
            persistent._gallery_unlocks = {}
        persistent._gallery_unlocks[key] = True
    
    def image_exists(path):
        try:
            return renpy.loadable(path)
        except:
            return False
    
    # Функция для автоматической разблокировки элементов галереи при получении достижений
    def auto_unlock_gallery_on_achievement(achievement_id):
        """Автоматически разблокирует соответствующие элементы галереи при получении достижения"""
        # Сопоставление достижений с элементами галереи
        gallery_mapping = {
            "meet_lina": ["Лина"],
            "meet_alex": ["Алекс"],
            "meet_katya": ["Катя"],
            "meet_teacher": ["Анна Сергеевна"],
            "meet_librarian": ["Библиотекарь"],
            "room_pk_light": ["Комната (светлая)"],
            "music_room_visit": ["Музыкальная комната"],
            "library_visit": ["Библиотека"],
            "room_evening": ["Вечерняя комната"],
            "wake_up": ["Ночная комната"],
            "first_choice": ["Комната (дневная)"],
            "new_friends": ["Школа (вход)", "Школьный коридор", "Класс"],
            "emotion_beginner": ["Кухня", "Улица"]
        }
        
        if achievement_id in gallery_mapping:
            for item_name in gallery_mapping[achievement_id]:
                # Ищем элемент галереи по имени
                for item in gallery_items:
                    if item.name == item_name and item.unlock_condition:
                        unlock_gallery_item(item.unlock_condition)
                        break
    
    gallery_items = []
    
    # Персонажи - ВСЕ ТРЕБУЮТ РАЗБЛОКИРОВКИ
    gallery_items.append(GalleryItem(
        "Лина", 
        "images/characters/lina_neutral.png", 
        "characters",
        "meet_lina"
    ))
    
    gallery_items.append(GalleryItem(
        "Алекс", 
        "images/characters/alex_neutral.png", 
        "characters",
        "meet_alex"
    ))
    
    gallery_items.append(GalleryItem(
        "Катя", 
        "images/characters/katia_neutral.png", 
        "characters",
        "meet_katya"
    ))
    
    gallery_items.append(GalleryItem(
        "Анна Сергеевна", 
        "images/characters/teacher_neutral.png", 
        "characters",
        "meet_teacher"
    ))
    
    gallery_items.append(GalleryItem(
        "Библиотекарь", 
        "images/characters/librarian_neutral.png", 
        "characters",
        "meet_librarian"
    ))

    # Фоны - ВСЕ ТРЕБУЮТ РАЗБЛОКИРОВКИ
    gallery_items.append(GalleryItem(
        "Ночная комната", 
        "images/night_room.png",
        "backgrounds",
        "night_room"
    ))
    
    gallery_items.append(GalleryItem(
        "Комната (дневная)", 
        "images/room_pk.png",
        "backgrounds",
        "room_pk"
    ))
    
    gallery_items.append(GalleryItem(
        "Комната (светлая)", 
        "images/room_pk_light.png",
        "backgrounds",
        "room_pk_light"
    ))
    
    gallery_items.append(GalleryItem(
        "Кухня", 
        "images/kitchen.png",
        "backgrounds",
        "kitchen"
    ))
    
    gallery_items.append(GalleryItem(
        "Улица", 
        "images/street.png",
        "backgrounds",
        "street"
    ))
    
    gallery_items.append(GalleryItem(
        "Школа (вход)", 
        "images/school_entrance.png",
        "backgrounds",
        "school_entrance"
    ))
    
    gallery_items.append(GalleryItem(
        "Школьный коридор", 
        "images/school_hallway.png",
        "backgrounds",
        "school_hallway"
    ))
    
    gallery_items.append(GalleryItem(
        "Класс", 
        "images/classroom.png",
        "backgrounds",
        "classroom"
    ))
    
    gallery_items.append(GalleryItem(
        "Музыкальная комната", 
        "images/music_room.png",
        "backgrounds",
        "music_room_visit"
    ))
    
    gallery_items.append(GalleryItem(
        "Библиотека", 
        "images/library.png",
        "backgrounds",
        "library_visit"
    ))

    # CG-арты - ВСЕ ТРЕБУЮТ РАЗБЛОКИРОВКИ
    gallery_items.append(GalleryItem(
        "Вечерняя комната", 
        "images/cg/room_evening.png",
        "cg",
        "room_evening"
    ))

# Экран галереи
screen gallery():
    tag menu
    
    default selected_category = "characters"
    
    use game_menu(_("Карточки")):
        vbox:
            spacing 20
            
            # Статистика галереи
            hbox:
                spacing 50
                xalign 0.45
                
                $ unlocked_count = len([item for item in gallery_items if item.is_unlocked()])
                $ total_count = len(gallery_items)
                $ progress_percent = (unlocked_count * 100 // total_count) if total_count > 0 else 0
                
                text _("Открыто: [unlocked_count]/[total_count]") size 28
                text _("Прогресс: [progress_percent]%") size 28
            
            null height 10
            
            hbox:
                spacing 10
                xalign 0.45
                
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
            
            $ category_items = [item for item in gallery_items if item.category == selected_category]
            
            if category_items:
                fixed:
                    ysize 650  # Фиксированная высота для прокрутки
                    
                    viewport:
                        yfill True
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        
                        vpgrid:
                            cols 3
                            spacing 40
                            yinitial 0.5
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
                                                
                                                $ image_exists = renpy.loadable(item.image) if item.image else False
                                                if image_exists:
                                                    # ИСПРАВЛЕНО: используем xysize с сохранением пропорций
                                                    add item.image:
                                                        xysize (300, 160)
                                                        fit "contain"
                                                        xalign 0.5
                                                        yalign 0.5
                                                else:
                                                    text "Изображение\nне найдено" size 20 xalign 0.5 yalign 0.5
                                                
                                                text item.name:
                                                    color "#ffffff"
                                                    size 20
                                                    font gui.interface_text_font
                                                    outlines [(2, "#671a1a", 0, 0)]
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
            
            text title:
                color "#ffffff"
                size 32
                font gui.interface_text_font
                outlines [(2, "#671a1a", 0, 0)]
                xalign 0.5
            
            $ image_exists = renpy.loadable(image) if image else False
            if image_exists:
                # ИСПРАВЛЕНО: используем xysize с сохранением пропорций для поп-апа
                add image:
                    xysize (1170, 620)
                    fit "contain"
                    xalign 0.5
                    yalign 0.5
            else:
                text "Изображение не найдено:\n[image]" size 30 xalign 0.5 yalign 0.5
            
            textbutton _("Закрыть"):
                xalign 0.5
                ypos 50
                background Frame("gui/button/choice_idle_background.png", 10, 10, 10, 10)
                hover_background Frame("gui/button/choice_hover_background_1.png", 10, 10, 10, 10)
                padding (30, 15)
                xsize 250
                action Hide("gallery_image_popup")
                text_style "gallery_close_button_text"
    
    key "game_menu" action Hide("gallery_image_popup")
    key "K_ESCAPE" action Hide("gallery_image_popup")

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