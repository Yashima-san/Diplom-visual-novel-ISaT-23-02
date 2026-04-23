################################################################################
## СИСТЕМА МЕССЕНДЖЕРА (УЛУЧШЕННЫЙ ДИЗАЙН С АНИМАЦИЕЙ)
################################################################################
init python:
    import time as tm
    from datetime import datetime, timedelta
    
    # Звуки для мессенджера (MP3 формат)
    MESSAGE_SEND_SOUND = "sounds/message_send.mp3"
    MESSAGE_RECEIVE_SOUND = "sounds/message_receive.mp3"
    
    # Класс для сообщений в чате
    class ChatMessage:
        def __init__(self, character, text, time=None, is_user=False, date=None):
            self.character = character
            self.text = text
            self.is_user = is_user
            self.time = time or "20:32"
            self.date = date
            self.animation_time = 0.0
            self.is_date_separator = False
    
    # История переписки
    chat_history = []
    chat_mode_active = False
    chat_choices = []
    chat_choice_callback = None
    chat_choices_shown = False
    current_chat_partner = "Лина"
    chat_status = "online"
    chat_waiting_for_response = False
    chat_pending_messages = []
    chat_processing_choice = False
    chat_in_callback = False
    message_animation_id = 0
    chat_screen_shown = False
    
    # Переменные для дат в чате
    chat_is_typing = False
    chat_should_auto_close = False
    chat_current_date = None
    pending_jump = None
    
    # Дата начала чата - 2 сентября 20:32
    CHAT_START_DATE = datetime(2024, 9, 2, 20, 32)
    chat_current_dt = CHAT_START_DATE
    
    # Функция для получения текущего времени чата
    def get_chat_time():
        return chat_current_dt.strftime("%H:%M")
    def get_chat_date():
        return chat_current_dt.strftime("%d.%m.%Y")
    def add_time_offset(minutes=0):
        global chat_current_dt
        chat_current_dt += timedelta(minutes=minutes)
    
    # Функция для добавления разделителя даты
    def add_date_separator_if_needed(new_date):
        if not chat_history:
            return True
        last_msg = chat_history[-1]
        if last_msg.date != new_date:
            return True
        return False
    def add_date_separator(date_str):
        separator = ChatMessage("", f"--- {date_str} ---", is_user=False, date=date_str)
        separator.is_date_separator = True
        chat_history.append(separator)
    
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
    
    # Функция для добавления сообщения в историю
    def add_chat_message(character, text, is_user=False, play_sound=True):
        global message_animation_id, chat_current_dt
        
        current_date_str = chat_current_dt.strftime("%d.%m.%Y")
        current_time_str = chat_current_dt.strftime("%H:%M")
        
        # Добавляем разделитель даты если нужно
        if add_date_separator_if_needed(current_date_str):
            add_date_separator(current_date_str)
        new_msg = ChatMessage(character, text, time=current_time_str, is_user=is_user, date=current_date_str)
        new_msg.animation_time = 0.0
        chat_history.append(new_msg)
        if len(chat_history) > 50:
            chat_history.pop(0)
        if play_sound:
            if is_user:
                play_chat_sound(MESSAGE_SEND_SOUND)
            else:
                play_chat_sound(MESSAGE_RECEIVE_SOUND)
        message_animation_id += 1
    
    # Функция для очистки чата
    def clear_chat():
        global chat_history, chat_current_dt
        chat_history = []
        chat_current_dt = CHAT_START_DATE
    MESSENGER_NAME = "Discordia"
    
    # Функция для показа вариантов ответа
    def show_chat_choices(choices, callback):
        global chat_choices, chat_choice_callback, chat_choices_shown, chat_mode_active, chat_screen_shown
        chat_choices = choices
        chat_choice_callback = callback
        chat_choices_shown = True
        chat_mode_active = True
        
        if not chat_screen_shown:
            chat_screen_shown = True
            renpy.show_screen("messenger_chat", _layer="screens")
            renpy.restart_interaction()
    
    # Функция для выбора варианта
    def select_chat_choice(choice_text):
        global chat_choices, chat_choice_callback, chat_choices_shown
        global chat_in_callback, chat_processing_choice, chat_waiting_for_response
        global pending_jump
        
        if chat_processing_choice:
            return
        chat_processing_choice = True
        
        user_name = persistent.user_name if persistent.user_name else "Вы"
        add_chat_message(user_name, choice_text, is_user=True, play_sound=True)
        
        # Скрываем варианты сразу после выбора
        chat_choices = []
        chat_choices_shown = False
        renpy.restart_interaction()
        
        callback = chat_choice_callback
        chat_choice_callback = None
        
        # Временно отключаем обработку чата, чтобы callback не конфликтовал
        chat_in_callback = True
        chat_waiting_for_response = True
        
        if callback:
            try:
                # Запускаем callback в новом контексте — это ключевое!
                renpy.call_in_new_context("_run_chat_callback", _args=(callback, choice_text))
            except Exception as e:
                print(f"Ошибка в callback: {e}")
                chat_processing_choice = False
                chat_in_callback = False
        else:
            chat_processing_choice = False
            chat_in_callback = False
            chat_waiting_for_response = False
    
    # Функция для показа сообщения в чате
    def show_chat_message(character, text, is_user=False, play_sound=True):
        global chat_mode_active, chat_screen_shown, chat_current_dt
        if hasattr(character, 'name'):
            char_name = character.name
        else:
            char_name = character
        
        # Добавляем задержку между сообщениями
        add_time_offset(1)
        add_chat_message(char_name, text, is_user, play_sound)
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
        chat_mode_active = False
        chat_choices_shown = False
        chat_waiting_for_response = False
        chat_pending_messages = []
        chat_screen_shown = False
        chat_is_typing = False
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
    
    original_e = None
    original_user_char = None
    original_a = None
    original_t = None
    original_k = None
    original_lib = None
    
    def enable_chat_mode():
        global original_e, original_user_char, original_a, original_t, original_k, original_lib
        global e, user_char, a, t, k, lib, chat_screen_shown, chat_current_dt, pending_jump
        
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
        # Сброс даты к 2 сентября 20:32
        chat_current_dt = CHAT_START_DATE
        pending_jump = None  # ← Сброс отложенного перехода
    
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
    
    def execute_pending_jump():
        global pending_jump
        if pending_jump:
            jump_target = pending_jump
            pending_jump = None
            renpy.jump(jump_target)
        return False

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

# =============================================================================
# 🔧 НОВЫЙ ЛЕЙБЛ: безопасное выполнение колбэка из чата
# =============================================================================
label _run_chat_callback:
    python:
        callback, choice_text = _args
        try:
            callback(choice_text)
        except Exception as e:
            print(f"Ошибка при выполнении чат-колбэка: {e}")
        finally:
            # После выполнения колбэка — скрываем чат и сбрасываем флаги
            hide_chat()
            global chat_processing_choice, chat_in_callback, chat_waiting_for_response
            chat_processing_choice = False
            chat_in_callback = False
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
    
    # Вычисляем высоту области сообщений
    $ chat_viewport_height = 380 if chat_choices_shown else 480
    
    # Определяем статусную строку
    $ status_text = "В сети" if chat_status == "online" else "печатает..."
    $ status_color = "#4caf50" if chat_status == "online" else "#ff9800"
  
    # Таймер для автоматического скрытия индикатора печати
    if chat_is_typing:
        timer 2.0 action [SetVariable('chat_is_typing', False), SetVariable('chat_status', 'online'), Function(renpy.restart_interaction)] repeat False
    # Таймер для автоматического закрытия чата
    if chat_should_auto_close and not chat_choices_shown and not chat_waiting_for_response and chat_mode_active:
        timer 3.0 action Function(hide_chat) repeat False
    # Таймер для выполнения отложенного перехода
    timer 0.5 action Function(execute_pending_jump) repeat True
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
                        
                        # Статус
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
                yinitial 1.0
                vbox:
                    spacing 10
                    xfill True
                    for msg in chat_history:
                        if hasattr(msg, 'is_date_separator') and msg.is_date_separator:
                            # Разделитель даты
                            frame:
                                style "messenger_date_separator"
                                xfill True
                                xalign 0.5
                                background None
                                text msg.text:
                                    style "messenger_date_text"
                                    size 11
                                    color "#888888"
                                    xalign 0.5
                        elif msg.is_user:
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
            # Разделитель
            if chat_choices_shown:
                frame:
                    xfill True
                    ysize 2
                    background "#e0e0e0"
            
            # Нижний отсек с вариантами ответов
            if chat_choices_shown and chat_choices:
                frame:
                    style "messenger_choices_container"
                    xfill True
                    vbox:
                        spacing 12
                        xalign 0.5
                        xfill True
                        # Заголовок
                        hbox:
                            spacing 10
                            xalign 0.5
                            text "💬":
                                size 16
                            text "ВЫБЕРИТЕ ОТВЕТ":
                                size 12
                                color "#2f5ac6"
                                bold True
                        
                        # Кнопки вариантов ответов
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
    ysize 220
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
style messenger_date_separator:
    padding (10, 5)
    xfill True
style messenger_date_text:
    font "FOT-YurukaStd-UB.otf"
    color "#888888"
    italic True