################################################################################
## Система достижений
################################################################################

init -1 python:
    class Achievement:
        def __init__(self, id, name, description, icon="", hidden=False):
            self.id = id
            self.name = name
            self.description = description
            self.icon = icon
            self.hidden = hidden
        
        def is_unlocked(self):
            if not isinstance(persistent._achievements, dict):
                return False
            return persistent._achievements.get(self.id, False)
    
    # Словарь для хранения всех достижений
    achievements = {}
    
    # Функция для регистрации достижения
    def register_achievement(id, name, description, icon="", hidden=False):
        achievements[id] = Achievement(id, name, description, icon, hidden)
    
    # Функция для разблокировки достижения
    def unlock_achievement(id):
        if id in achievements:
            # Проверяем, что persistent._achievements - словарь
            if not isinstance(persistent._achievements, dict):
                # Конвертируем set в dict, если нужно
                old_data = persistent._achievements
                persistent._achievements = {}
                # Если это было множество с разблокированными достижениями
                if isinstance(old_data, set):
                    for ach_id in old_data:
                        persistent._achievements[ach_id] = True
            
            if not persistent._achievements.get(id, False):
                persistent._achievements[id] = True
                if not achievements[id].hidden:
                    renpy.notify("Достижение разблокировано: " + achievements[id].name)
                
                # Сохраняем в базу данных
                if persistent.user_id and 'db' in globals() and hasattr(db, 'save_achievement'):
                    db.save_achievement(persistent.user_id, achievements[id].name, achievements[id].description)
    
    # Функция для проверки, разблокировано ли достижение
    def is_achievement_unlocked(id):
        # Проверяем, что persistent._achievements - словарь
        if not isinstance(persistent._achievements, dict):
            return False
        return persistent._achievements.get(id, False)
    
    # Инициализация persistent переменной для хранения достижений
    if not hasattr(persistent, '_achievements'):
        persistent._achievements = {}  # Словарь вместо множества
    else:
        # Если уже существует, но это не словарь, конвертируем
        if not isinstance(persistent._achievements, dict):
            old_data = persistent._achievements
            persistent._achievements = {}
            # Если это было множество с разблокированными достижениями
            if isinstance(old_data, set):
                for ach_id in old_data:
                    persistent._achievements[ach_id] = True

# Регистрация достижений
init -1 python:
    # Существующие достижения
    register_achievement(
        "wake_up",
        "Проснулась?",
        "Добро пожаловать в игру. Приятной игры!"
    )
    
    register_achievement(
        "first_choice",
        "Ваш выбор",
        "Первый важный выбор в игре"
    )
    
    register_achievement(
        "meet_alex",
        "Знакомство с Алексом",
        "Вы познакомились с Алексом - школьным активистом"
    )
    
    register_achievement(
        "meet_katya",
        "Знакомство с Катей",
        "Вы познакомились с Катей - участницей театрального кружка"
    )
    
    register_achievement(
        "meet_teacher",
        "Знакомство с учителем",
        "Вы познакомились с Анной Сергеевной - классным руководителем"
    )
    
    register_achievement(
        "meet_librarian",
        "Знакомство с библиотекарем",
        "Вы познакомились с библиотекарем - хранительницей знаний"
    )
    
    register_achievement(
        "music_room_visit",
        "В мире музыки",
        "Вы посетили музыкальную комнату и открыли для себя новый мир"
    )
    
    register_achievement(
        "library_visit",
        "В мире книг",
        "Вы нашли уютное место в библиотеке"
    )
    
    register_achievement(
        "sociable_choice",
        "Общительная натура",
        "Вы выбрали общительный вариант ответа"
    )
    
    register_achievement(
        "shy_choice",
        "Застенчивая натура",
        "Вы выбрали застенчивый вариант ответа"
    )
    
    register_achievement(
        "balanced_choice",
        "Золотая середина",
        "Вы нашли баланс между общительностью и застенчивостью"
    )
    
    register_achievement(
        "new_friends",
        "Новые друзья",
        "Вы завели новых друзей в новой школе"
    )
    
    register_achievement(
        "chapter_one_complete",
        "Глава 1 пройдена",
        "Вы завершили первую главу"
    )
    
    # Новые достижения для второй главы
    register_achievement(
        "chapter_two_complete",
        "Глава 2 пройдена",
        "Вы завершили вторую главу"
    )
# Экран достижений
screen achievements():
    tag menu
    
    use game_menu(_("Достижения"), scroll="viewport"):
        style_prefix "achievements"
        
        vbox:
            spacing 20
            
            # Статистика
            hbox:
                spacing 50
                xalign 0.5
                
                $ unlocked = len([a for a in achievements.values() if a.is_unlocked()])
                $ total = len(achievements)
                $ progress_percent = (unlocked * 100 // total) if total > 0 else 0
                
                text _("Разблокировано: [unlocked]/[total]") size 30
                text _("Прогресс: [progress_percent]%") size 30
            
            null height 30
            
            # Список достижений
            vpgrid:
                cols 1
                spacing 15
                yinitial 0.0
                mousewheel True
                draggable True
                
                for ach in sorted(achievements.values(), key=lambda a: (not a.is_unlocked(), a.id)):
                    if ach.is_unlocked() or not ach.hidden:
                        button:
                            style "achievement_button"
                            
                            frame:
                                style "achievement_frame"
                                background (gui.accent_color if ach.is_unlocked() else gui.insensitive_color)
                                
                                hbox:
                                    spacing 20
                                    
                                    # Иконка
                                    frame:
                                        xysize (80, 80)
                                        background None
                                        if ach.is_unlocked():
                                            text "🏆" size 60 xalign 0.5 yalign 0.5
                                        else:
                                            text "❓" size 60 xalign 0.5 yalign 0.5
                                    
                                    # Информация
                                    vbox:
                                        yalign 0.5
                                        spacing 5
                                        
                                        if ach.is_unlocked():
                                            text ach.name:
                                                style "achievement_name"
                                                color "#ffffff"
                                        else:
                                            text ach.name:
                                                style "achievement_name"
                                                color gui.insensitive_color
                                        
                                        if ach.is_unlocked():
                                            text ach.description:
                                                style "achievement_description"
                                        else:
                                            if ach.hidden:
                                                text _("Скрытое достижение"):
                                                    style "achievement_description"
                                            else:
                                                text _("???"):
                                                    style "achievement_description"

## Стили для достижений
style achievements_vbox:
    xsize 1400
    xalign 0.5

style achievement_button:
    xsize 1200
    xalign 0.5
    padding (0, 0)

style achievement_frame:
    padding (20, 20)
    background None

style achievement_name:
    size 28
    font gui.interface_text_font
    outlines [(2, "#000000", 0, 0)]

style achievement_description:
    size 22
    font gui.interface_text_font
    color "#cccccc"
    outlines [(1, "#000000", 0, 0)]