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
            return persistent._achievements.get(self.id, False)
    
    # Словарь для хранения всех достижений
    achievements = {}
    
    # Функция для регистрации достижения
    def register_achievement(id, name, description, icon="", hidden=False):
        achievements[id] = Achievement(id, name, description, icon, hidden)
    
    # Функция для разблокировки достижения
    def unlock_achievement(id):
        if id in achievements:
            if not persistent._achievements.get(id, False):
                persistent._achievements[id] = True
                if not achievements[id].hidden:
                    renpy.notify("Достижение разблокировано: " + achievements[id].name)
    
    # Функция для проверки, разблокировано ли достижение
    def is_achievement_unlocked(id):
        return persistent._achievements.get(id, False)
    
    # Инициализация persistent переменной для хранения достижений
    if not hasattr(persistent, '_achievements'):
        persistent._achievements = {}

# Регистрация достижений
init -1 python:
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
                
                text _("Разблокировано: [unlocked]/[total]") size 30
                text _("Прогресс: [unlocked*100/total]%") size 30
            
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
                                        
                                        text ach.name:
                                            style "achievement_name"
                                            color "#ffffff" if ach.is_unlocked() else gui.insensitive_color
                                        
                                        if ach.is_unlocked():
                                            text ach.description:
                                                style "achievement_description"
                                        else:
                                            if ach.hidden:
                                                text _("Скрытое достижение"):
                                                    style "achievement_description"
                                            else:
                                                text _("???"):

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
    color "#ffffff"
    outlines [(2, "#000000", 0, 0)]

style achievement_description:
    size 22
    font gui.interface_text_font
    color "#cccccc"
    outlines [(1, "#000000", 0, 0)]
