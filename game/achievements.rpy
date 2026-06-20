################################################################################
## Система достижений
################################################################################

init -1 python:
    import time
    from collections import deque
    
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
    
    # Очередь уведомлений
    notification_queue = deque()
    current_notifications = []
    NOTIFICATION_MAX_VISIBLE = 5
    
    class NotificationItem:
        def __init__(self, text, is_achievement=False, duration=3.0):
            self.text = text
            self.is_achievement = is_achievement
            self.duration = duration
            self.created_at = time.time()
            self.alpha = 1.0
    
    def show_notification_queue(text, is_achievement=False, duration=3.0):
        """Добавляет уведомление в очередь"""
        notification_queue.append(NotificationItem(text, is_achievement, duration))
        renpy.restart_interaction()
    
    def process_notification_queue():
        """Обрабатывает очередь уведомлений и показывает их"""
        global current_notifications, notification_queue
        
        current_time = time.time()
        
        # Удаляем старые уведомления
        current_notifications = [n for n in current_notifications if current_time - n.created_at < n.duration]
        
        # Добавляем новые уведомления, если есть место
        while len(current_notifications) < NOTIFICATION_MAX_VISIBLE and notification_queue:
            notif = notification_queue.popleft()
            notif.created_at = current_time
            current_notifications.append(notif)
        
        # Показываем уведомления через Ren'Py
        for i, notif in enumerate(current_notifications):
            # Формируем текст с иконкой для достижений
            display_text = notif.text
            if notif.is_achievement:
                display_text = "★ " + notif.text + " ★"
            
            # Показываем уведомление с задержкой для каждого
            renpy.show_screen("notify_queue", message=display_text, y_offset=i * 85, is_achievement=notif.is_achievement)
        
        # Очищаем старые уведомления из очереди отображения
        if len(current_notifications) > 0:
            return True
        return False
    
    # Функция для регистрации достижения
    def register_achievement(id, name, description, icon="", hidden=False):
        achievements[id] = Achievement(id, name, description, icon, hidden)
    
    # Функция для загрузки достижений из базы данных
    def load_achievements_from_db():
        if persistent.user_id and 'db' in globals() and hasattr(db, 'get_user_achievements'):
            try:
                db_achievements = db.get_user_achievements(persistent.user_id)
                for ach in db_achievements:
                    ach_name = ach.get('achi_name')
                    if ach_name:
                        # Ищем ID достижения по имени
                        for ach_id, ach_obj in achievements.items():
                            if ach_obj.name == ach_name:
                                if not isinstance(persistent._achievements, dict):
                                    persistent._achievements = {}
                                persistent._achievements[ach_id] = True
                                break
            except:
                pass
    
    # Функция для разблокировки достижения
    def unlock_achievement(id):
        if id in achievements:
            # Проверяем, что persistent._achievements - словарь
            if not isinstance(persistent._achievements, dict):
                old_data = persistent._achievements
                persistent._achievements = {}
                if isinstance(old_data, set):
                    for ach_id in old_data:
                        persistent._achievements[ach_id] = True
            
            if not persistent._achievements.get(id, False):
                persistent._achievements[id] = True
                
                # Показываем уведомление о достижении
                achievement_name = achievements[id].name
                achievement_desc = achievements[id].description
                notification_text = f"{achievement_name}"
                if achievement_desc:
                    notification_text = f"{notification_text}\n{achievement_desc}"
                
                show_notification_queue(notification_text, is_achievement=True, duration=4.0)
                
                # Сохраняем в базу данных
                if persistent.user_id and 'db' in globals() and hasattr(db, 'save_achievement'):
                    db.save_achievement(persistent.user_id, achievements[id].name, achievements[id].description)
    
    # Функция для проверки, разблокировано ли достижение
    def is_achievement_unlocked(id):
        # Проверяем, что persistent._achievements - словарь
        if not isinstance(persistent._achievements, dict):
            return False
        return persistent._achievements.get(id, False)
    
    # Функция для обычных уведомлений (не достижений)
    def notify_with_queue(message, duration=3.0):
        show_notification_queue(message, is_achievement=False, duration=duration)
    
    # Переопределяем стандартный notify
    original_notify = renpy.notify
    def custom_notify(message):
        notify_with_queue(message)
    renpy.notify = custom_notify
    
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

    # Регистрация существующих достижений
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
    
    # Новые достижения для эмоциональной мини-игры
    register_achievement(
        "emotion_beginner",
        "Юный эмоциональный детектив",
        "Впервые определил своё эмоциональное состояние"
    )
    
    register_achievement(
        "emotion_treasure_hunter",
        "Охотник за эмоциями",
        "Распознал тревогу"
    )
    
    register_achievement(
        "emotion_pioneer",
        "Первопроходец чувств",
        "Смог определить страх"
    )
    
    register_achievement(
        "emotion_explorer",
        "Исследователь эмоций",
        "Почувствовал предвкушение"
    )
    
    register_achievement(
        "emotion_seeker",
        "Искатель надежды",
        "Обнаружил в себе надежду"
    )
    
    # Достижения для дневника эмоций
    register_achievement(
        "diary_streak_3",
        "Три шага подряд",
        "Сделал три здоровых выбора в дневнике подряд"
    )
    
    register_achievement(
        "empathetic_listener",
        "Чуткий слушатель",
        "Помог Кате разобраться в своих чувствах"
    )
    
    register_achievement(
        "detective_first_step",
        "Первый шаг к пониманию",
        "Завершил первую миссию эмоционального детектива"
    )
    
    # Загружаем достижения из базы данных при старте
    load_achievements_from_db()

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