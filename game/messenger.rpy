################################################################################
## СИСТЕМА МЕССЕНДЖЕРА (УЛУЧШЕННЫЙ ДИЗАЙН С АНИМАЦИЕЙ)
################################################################################

init python:
    import time as tm
    import math
    
    # Звуки для мессенджера
    MESSAGE_SEND_SOUND = "sounds/message_send.mp3"
    MESSAGE_RECEIVE_SOUND = "sounds/message_receive.mp3"
    
    # Класс для сообщений в чате
    class ChatMessage:
        def __init__(self, character, text, time=None, is_user=False):
            self.character = character
            self.text = text
            self.is_user = is_user
            self.time = time or tm.strftime("%H:%M")
            self.animation_time = 0.0
            self.read = False
    
    # Глобальные переменные состояния чата
    chat_history = []
    chat_mode_active = False
    chat_choices = []
    chat_choice_callback = None
    chat_choices_shown = False
    current_chat_partner = "Лина"
    chat_status = "online"
    chat_is_typing = False
    chat_typing_timer = None
    chat_auto_close_timer = None
    chat_waiting_for_response = False
    chat_pending_messages = []
    chat_processing_choice = False
    chat_in_callback = False
    message_animation_id = 0
    chat_screen_shown = False
    chat_should_close = False
    
    # Функция для проверки существования звукового файла
    def sound_exists(sound_file):
        try:
            return renpy.loadable(sound_file)
        except:
            return False
    
    # Функция для безопасного воспроизведения звука
    def play_chat_sound(sound_file):
        if sound_exists(sound_file):
            renpy.play(sound_file, channel="sound")
        else:
            alt_paths = [
                "audio/" + sound_file.split("/")[-1],
                "game/" + sound_file,
                sound_file.split("/")[-1]
            ]
            for alt_path in alt_paths:
                if sound_exists(alt_path):
                    renpy.play(alt_path, channel="sound")
                    return
    
    # Функция для расчета времени печати на основе длины сообщения
    def calculate_typing_time(text):
        """Расчет времени печати: базовая задержка 1.5 сек + 0.07 сек на символ"""
        base_time = 1.5
        char_time = len(text) * 0.05
        return min(base_time + char_time, 4.0)  # Максимум 4 секунды
    
    # Функция для показа индикатора печати
    def show_typing_indicator(duration=2.0):
        global chat_is_typing, chat_status
        
        old_status = chat_status
        chat_status = "typing"
        chat_is_typing = True
        
        # Обновляем экран
        if chat_screen_shown:
            renpy.restart_interaction()
        
        # Устанавливаем таймер для скрытия индикатора
        def hide_typing():
            global chat_is_typing, chat_status
            chat_is_typing = False
            chat_status = "online"
            if chat_screen_shown:
                renpy.restart_interaction()
        
        renpy.invoke_in_time(duration, hide_typing)
    
    # Функция для автоматического закрытия чата
    def start_auto_close(delay=3.0):
        global chat_auto_close_timer, chat_should_close
        
        def close_chat():
            global chat_should_close, chat_mode_active, chat_screen_shown
            if not chat_choices_shown and not chat_waiting_for_response:
                chat_should_close = True
                hide_chat()
        
        renpy.invoke_in_time(delay, close_chat)
    
    # Функция для добавления сообщения в историю
    def add_chat_message(character, text, is_user=False, play_sound=True):
        global message_animation_id, chat_waiting_for_response
        
        # Скрываем индикатор печати если он активен
        if not is_user and chat_is_typing:
            global chat_status
            chat_is_typing = False
            chat_status = "online"
        
        new_msg = ChatMessage(character, text, is_user=is_user)
        new_msg.animation_time = 0.0
        chat_history.append(new_msg)
        
        # Ограничиваем историю
        if len(chat_history) > 50:
            chat_history.pop(0)
        
        # Воспроизводим звук
        if play_sound:
            if is_user:
                play_chat_sound(MESSAGE_SEND_SOUND)
            else:
                play_chat_sound(MESSAGE_RECEIVE_SOUND)
        
        message_animation_id += 1
        
        # Автопрокрутка вниз
        if chat_screen_shown:
            renpy.restart_interaction()
    
    # Функция для очистки чата
    def clear_chat():
        global chat_history
        chat_history = []
    
    MESSENGER_NAME = "Discordia"
    
    # Функция для показа вариантов ответа (теперь варианты по центру)
    def show_chat_choices(choices, callback):
        global chat_choices, chat_choice_callback, chat_choices_shown, chat_mode_active
        global chat_screen_shown, chat_auto_close_timer, chat_should_close
        
        # Отменяем авто-закрытие если было
        chat_should_close = False
        chat_choices = choices
        chat_choice_callback = callback
        chat_choices_shown = True
        chat_mode_active = True
        chat_waiting_for_response = True
        
        if not chat_screen_shown:
            chat_screen_shown = True
            renpy.show_screen("messenger_chat", _layer="screens")
            renpy.restart_interaction()
    
    # Функция для выбора варианта
    def select_chat_choice(choice_text):
        global chat_choices, chat_choice_callback, chat_choices_shown
        global chat_in_callback, chat_processing_choice, chat_waiting_for_response
        global chat_auto_close_timer, chat_should_close
        
        if chat_processing_choice:
            return
        
        chat_processing_choice = True
        
        # Отменяем авто-закрытие
        chat_should_close = False
        
        # Получаем имя пользователя
        user_name = persistent.user_name if persistent.user_name else "Вы"
        
        # Добавляем сообщение пользователя
        add_chat_message(user_name, choice_text, is_user=True, play_sound=True)
        
        # Скрываем варианты ответов
        chat_choices = []
        chat_choices_shown = False
        chat_waiting_for_response = False
        
        renpy.restart_interaction()
        
        # Вызываем callback
        callback = chat_choice_callback
        chat_choice_callback = None
        chat_in_callback = True
        
        if callback:
            try:
                callback(choice_text)
            except Exception as e:
                print(f"Ошибка в callback: {e}")
        
        chat_in_callback = False
        chat_processing_choice = False
        
        # Запускаем таймер авто-закрытия чата
        start_auto_close(3.0)
    
    # Функция для показа сообщения в чате
    def show_chat_message(character, text, is_user=False, play_sound=True):
        global chat_mode_active, chat_screen_shown, chat_auto_close_timer, chat_should_close
        
        # Отменяем авто-закрытие при новом сообщении
        chat_should_close = False
        
        # Определяем имя персонажа
        if hasattr(character, 'name'):
            char_name = character.name
        else:
            char_name = character
        
        # Показываем индикатор печати перед сообщением (если сообщение не от пользователя)
        if not is_user and not chat_is_typing:
            typing_time = calculate_typing_time(text)
            show_typing_indicator(typing_time)
            # Ждем завершения печати
            renpy.pause(typing_time)
        
        # Добавляем сообщение
        add_chat_message(char_name, text, is_user, play_sound)
        
        # Активируем режим чата если нужно
        if not chat_mode_active and not chat_choices_shown:
            chat_mode_active = True
            if not chat_screen_shown:
                chat_screen_shown = True
                renpy.show_screen("messenger_chat", _layer="screens")
            renpy.restart_interaction()
    
    # Функция для отправки нескольких сообщений с задержкой
    def send_messages_with_delay(messages, delay=2.0):
        global chat_waiting_for_response, chat_pending_messages
        
        chat_pending_messages = []
        for msg in messages:
            character = msg[0]
            text = msg[1]
            is_user = msg[2] if len(msg) > 2 else False
            chat_pending_messages.append((character, text, is_user, delay))
        
        chat_waiting_for_response = True
        renpy.call_in_new_context("_process_message_queue")
    
    # Функция для скрытия чата
    def hide_chat():
        global chat_mode_active, chat_choices_shown, chat_waiting_for_response
        global chat_pending_messages, chat_screen_shown, chat_is_typing
        global chat_status, chat_auto_close_timer, chat_should_close
        
        chat_mode_active = False
        chat_choices_shown = False
        chat_waiting_for_response = False
        chat_pending_messages = []
        chat_screen_shown = False
        chat_is_typing = False
        chat_status = "online"
        chat_should_close = False
        renpy.hide_screen("messenger_chat")
        renpy.restart_interaction()
    
    # Класс для персонажей в чате
    class ChatCharacter:
        def __init__(self, name, color=None, avatar_letter=None):
            self.name = name
            self.color = color
            self.avatar_letter = avatar_letter or name[0] if name else "?"
        
        def __call__(self, text, play_sound=True):
            show_chat_message(self, text, is_user=False, play_sound=play_sound)
    
    # Класс для пользователя
    class UserChatCharacter:
        def __init__(self, name):
            self.name = name
            self.avatar_letter = name[0] if name else "?"
        
        def __call__(self, text, play_sound=True):
            show_chat_message(self, text, is_user=True, play_sound=play_sound)
    
    # Сохраняем оригинальных персонажей
    original_e = None
    original_user_char = None
    original_a = None
    original_t = None
    original_k = None
    original_lib = None
    
    def enable_chat_mode():
        global original_e, original_user_char, original_a, original_t, original_k, original_lib
        global e, user_char, a, t, k, lib, chat_screen_shown, chat_status
        
        original_e = e
        original_user_char = user_char
        original_a = a
        original_t = t
        original_k = k
        original_lib = lib
        
        e = ChatCharacter("Лина", avatar_letter="Л")
        user_char = UserChatCharacter(persistent.user_name if persistent.user_name else "Вы")
        a = ChatCharacter("Алекс", avatar_letter="А")
        t = ChatCharacter("Анна Сергеевна", avatar_letter="А")
        k = ChatCharacter("Катя", avatar_letter="К")
        lib = ChatCharacter("Библиотекарь", avatar_letter="Б")
        
        clear_chat()
        chat_screen_shown = False
        chat_status = "online"
        chat_is_typing = False
    
    def disable_chat_mode():
        global original_e, original_user_char, original_a, original_t, original_k, original_lib
        global e, user_char, a, t, k, lib
        
        hide_chat()
        
        if original_e:
            e = original_e
        if original_user_char:
            user_char = original_user_char
        if original_a:
            a = original_a
        if original_t:
            t = original_t
        if original_k:
            k = original_k
        if original_lib:
            lib = original_lib
        
        clear_chat()


label _process_message_queue:
    python:
        messages = chat_pending_messages.copy()
        chat_pending_messages = []
    
    python:
        for msg in messages:
            character, text, is_user, delay = msg
            show_chat_message(character, text, is_user, play_sound=True)
            renpy.pause(delay)
        
        chat_waiting_for_response = False
    return


################################################################################
## ТРАНСФОРМАЦИИ ДЛЯ АНИМАЦИИ
################################################################################

transform message_appear_left:
    alpha 0.0
    xoffset -50
    linear 0.2 alpha 1.0 xoffset 0

transform message_appear_right:
    alpha 0.0
    xoffset 50
    linear 0.2 alpha 1.0 xoffset 0

transform choice_button_appear:
    alpha 0.0
    yoffset 20
    linear 0.15 alpha 1.0 yoffset 0


################################################################################
## ЭКРАН ЧАТА
################################################################################

screen messenger_chat():
    zorder 150
    
    # Вычисляем высоту области сообщений в зависимости от наличия вариантов
    $ chat_viewport_height = 350 if chat_choices_shown else 450
    
    # Определяем статусную строку
    $ status_text = "В сети" if chat_status == "online" else "печатает..."
    $ status_color = "#4caf50" if chat_status == "online" else "#ff9800"
    
    frame:
        style "messenger_frame"
        xalign 0.5
        yalign 0.2
        xsize 850
        ysize 720
        
        vbox:
            # Шапка чата
            frame:
                style "messenger_header"
                xfill True
                
                hbox:
                    xfill True
                    spacing 12
                    
                    # Аватар
                    frame:
                        style "messenger_chat_avatar"
                        xysize (40, 40)
                        background "#2f6bc6"
                        
                        $ avatar_text = current_chat_partner[0] if current_chat_partner else "?"
                        text avatar_text:
                            size 22
                            color "#ffffff"
                            xalign 0.5
                            yalign 0.5
                    
                    vbox:
                        xfill True
                        spacing 2
                        yalign 0.5
                        
                        text current_chat_partner:
                            style "messenger_chat_name"
                            size 16
                            color "#ffffff"
                            bold True
                        
                        # Статус (меняется между "В сети" и "печатает...")
                        text status_text:
                            style "messenger_chat_status"
                            size 11
                            color status_color
            
            # Область сообщений
            viewport:
                id "chat_viewport"
                ysize chat_viewport_height
                scrollbars "vertical"
                mousewheel True
                draggable True
                yinitial 1.0  # Всегда показываем последние сообщения
                
                vbox:
                    spacing 10
                    xfill True
                    
                    for msg in chat_history:
                        if msg.is_user:
                            # Сообщение пользователя (справа)
                            hbox:
                                xfill True
                                xalign 1.0
                                at message_appear_right
                                
                                frame:
                                    style "messenger_user_bubble"
                                    xmaximum 480
                                    
                                    vbox:
                                        spacing 3
                                        text msg.text:
                                            style "messenger_message_text_user"
                                            size 15
                                            color "#ffffff"
                                        text msg.time:
                                            style "messenger_message_time_user"
                                            size 9
                                            color "#dddddd"
                                            xalign 1.0
                                
                                null width 10
                        else:
                            # Сообщение другого пользователя (слева)
                            hbox:
                                xfill True
                                spacing 8
                                at message_appear_left
                                
                                frame:
                                    style "messenger_message_avatar"
                                    xysize (28, 28)
                                    background "#2f6bc6"
                                    
                                    $ avatar_letter = msg.character[0] if msg.character else "?"
                                    text avatar_letter:
                                        size 14
                                        color "#ffffff"
                                        xalign 0.5
                                        yalign 0.5
                                
                                frame:
                                    style "messenger_other_bubble"
                                    xmaximum 480
                                    
                                    vbox:
                                        spacing 3
                                        text msg.character:
                                            style "messenger_message_name"
                                            size 10
                                            color "#2f6bc6"
                                            bold True
                                        text msg.text:
                                            style "messenger_message_text_other"
                                            size 15
                                            color "#1a1a1a"
                                        text msg.time:
                                            style "messenger_message_time_other"
                                            size 9
                                            color "#999999"
                                            xalign 1.0
                                
                                null width 8
            
            # Разделитель (показываем только если есть варианты ответов)
            if chat_choices_shown:
                frame:
                    xfill True
                    ysize 2
                    background "#e0e0e0"
                    ypadding 3
            
            # Нижний отсек с вариантами ответов (по центру)
            if chat_choices_shown and chat_choices:
                frame:
                    style "messenger_choices_container"
                    xfill True
                    yalign 0.5
                    
                    vbox:
                        spacing 12
                        xalign 0.5
                        xfill True
                        
                        # Заголовок с иконкой
                        hbox:
                            spacing 10
                            xalign 0.5
                            
                            text "💬":
                                size 16
                            text "ВЫБЕРИТЕ ОТВЕТ":
                                size 12
                                color "#2f5ac6"
                                bold True
                        
                        # Кнопки вариантов ответов (по центру)
                        for choice_text in chat_choices:
                            button:
                                style "messenger_choice_button"
                                xsize 500
                                xalign 0.5
                                at choice_button_appear
                                action Function(select_chat_choice, choice_text)
                                
                                text choice_text:
                                    style "messenger_choice_text"
                                    size 13
                                    color "#2b2b2b"
                                    xalign 0.5
                                    yalign 0.5


################################################################################
## СТИЛИ ДЛЯ МЕССЕНДЖЕРА
################################################################################

style messenger_frame:
    background Frame("gui/frame.png", 12, 12, 12, 12)
    padding (0, 0)

style messenger_header:
    background "#2b2b2b"
    ysize 55
    padding (12, 8)

style messenger_chat_avatar:
    background "#2f52c6"
    xysize (40, 40)

style messenger_chat_name:
    font "FOT-YurukaStd-UB.otf"
    outlines [(1, "#000000", 0, 0)]

style messenger_chat_status:
    font "FOT-YurukaStd-UB.otf"

style messenger_user_bubble:
    background "#2f3ec6"
    padding (12, 8)
    margin (6, 3, 12, 3)
    xalign 1.0

style messenger_message_text_user:
    font "LeticeaBumsteadCyrillic.otf"
    color "#ffffff"
    xalign 0.0

style messenger_message_time_user:
    font "FOT-YurukaStd-UB.otf"
    color "#dddddd"
    xalign 1.0

style messenger_other_bubble:
    background "#f0f0f0"
    padding (12, 8)
    margin (6, 3, 35, 3)

style messenger_message_avatar:
    background "#2f4bc6"
    xysize (28, 28)

style messenger_message_name:
    font "FOT-YurukaStd-UB.otf"
    color "#2f3ec6"

style messenger_message_text_other:
    font "LeticeaBumsteadCyrillic.otf"
    color "#1a1a1a"

style messenger_message_time_other:
    font "FOT-YurukaStd-UB.otf"
    color "#999999"
    xalign 1.0

style messenger_choices_container:
    background "#f5f7ff"
    padding (20, 15)
    ysize 230
    xfill True

style messenger_choice_button:
    background "#e8e8e8"
    hover_background "#c0c0c0"
    selected_background "#a0a0a0"
    padding (14, 10)
    xsize 500
    xalign 0.5

style messenger_choice_text:
    hover_color "#ffffff"
    selected_color "#ffffff"
    xalign 0.5
    yalign 0.5
    size 13
    color "#2b2b2b"
    text_align 0.5