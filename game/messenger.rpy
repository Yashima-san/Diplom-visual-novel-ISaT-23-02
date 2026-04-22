################################################################################
## СИСТЕМА МЕССЕНДЖЕРА (УЛУЧШЕННЫЙ ДИЗАЙН С АНИМАЦИЕЙ)
################################################################################

init python:
    import time as tm
    
    # Звуки для мессенджера (MP3 формат)
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
    
    # История переписки
    chat_history = []
    chat_mode_active = False
    chat_choices = []
    chat_choice_callback = None
    chat_choices_shown = False
    current_chat_partner = "Лина"
    chat_status = "В сети"
    chat_waiting_for_response = False
    chat_pending_messages = []
    chat_processing_choice = False
    chat_in_callback = False
    message_animation_id = 0
    chat_screen_shown = False  # Флаг для отслеживания состояния экрана чата
    
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
        global message_animation_id
        
        new_msg = ChatMessage(character, text, is_user=is_user)
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
        global chat_history
        chat_history = []
    
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
            renpy.show_screen("messenger_chat_with_choices", _layer="screens")
            renpy.restart_interaction()
    
    # Функция для выбора варианта
    def select_chat_choice(choice_text):
        global chat_choices, chat_choice_callback, chat_choices_shown
        global chat_in_callback, chat_processing_choice, chat_waiting_for_response
        
        if chat_processing_choice:
            return
        
        chat_processing_choice = True
        
        user_name = persistent.user_name if persistent.user_name else "Вы"
        add_chat_message(user_name, choice_text, is_user=True, play_sound=True)
        
        chat_choices = []
        chat_choices_shown = False
        
        renpy.restart_interaction()
        
        callback = chat_choice_callback
        chat_choice_callback = None
        chat_in_callback = True
        
        renpy.hide_screen("messenger_chat_with_choices")
        renpy.show_screen("messenger_chat", _layer="screens")
        renpy.restart_interaction()
        
        chat_waiting_for_response = True
        
        if callback:
            try:
                callback(choice_text)
            except Exception as e:
                print(f"Ошибка в callback: {e}")
        
        chat_in_callback = False
        chat_processing_choice = False
    
    # Функция для показа сообщения в чате
    def show_chat_message(character, text, is_user=False, play_sound=True):
        global chat_mode_active, chat_screen_shown
        
        if hasattr(character, 'name'):
            char_name = character.name
        else:
            char_name = character
        
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
        global chat_pending_messages, chat_screen_shown
        
        chat_mode_active = False
        chat_choices_shown = False
        chat_waiting_for_response = False
        chat_pending_messages = []
        chat_screen_shown = False
        renpy.hide_screen("messenger_chat")
        renpy.hide_screen("messenger_chat_with_choices")
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
        global e, user_char, a, t, k, lib, chat_screen_shown
        
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


################################################################################
## ЭКРАН ЧАТА (ОСНОВНОЙ)
################################################################################

screen messenger_chat():
    zorder 150  # Высокий z-order, но ниже модальных окон (200)
    
    # Окно чата (под текстовым окном, yalign 0.2)
    frame:
        style "messenger_frame"
        xalign 0.5
        yalign 0.2
        xsize 950
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
                        xysize (35, 35)
                        background "#c66b2f"
                        
                        $ avatar_text = current_chat_partner[0] if current_chat_partner else "?"
                        text avatar_text:
                            size 20
                            color "#ffffff"
                            xalign 0.5
                            yalign 0.5
                    
                    vbox:
                        xfill True
                        spacing 2
                        yalign 0.5
                        
                        text current_chat_partner:
                            style "messenger_chat_name"
                            size 14
                            color "#ffffff"
                            bold True
                        
                        if chat_status == "В сети":
                            text "онлайн":
                                style "messenger_chat_status_online"
                                size 11
                                color "#4caf50"
            
            # Область сообщений
            viewport:
                id "chat_viewport"
                ysize 500
                scrollbars "vertical"
                mousewheel True
                draggable True
                yinitial 0.4
                
                vbox:
                    spacing 8
                    xfill True
                    
                    for msg in chat_history:
                        if msg.is_user:
                            hbox:
                                xfill True
                                xalign 1.0
                                at message_appear_right
                                
                                frame:
                                    style "messenger_user_bubble"
                                    xmaximum 450
                                    
                                    vbox:
                                        spacing 2
                                        text msg.text:
                                            style "messenger_message_text_user"
                                            size 16
                                            color "#ffffff"
                                        text msg.time:
                                            style "messenger_message_time_user"
                                            size 9
                                            color "#dddddd"
                                            xalign 1.0
                                
                                null width 10
                        else:
                            hbox:
                                xfill True
                                spacing 8
                                at message_appear_left
                                
                                frame:
                                    style "messenger_message_avatar"
                                    xysize (25, 25)
                                    background "#c66b2f"
                                    
                                    $ avatar_letter = msg.character[0] if msg.character else "?"
                                    text avatar_letter:
                                        size 14
                                        color "#ffffff"
                                        xalign 0.5
                                        yalign 0.5
                                
                                frame:
                                    style "messenger_other_bubble"
                                    xmaximum 450
                                    
                                    vbox:
                                        spacing 2
                                        text msg.character:
                                            style "messenger_message_name"
                                            size 11
                                            color "#c66b2f"
                                            bold True
                                        text msg.text:
                                            style "messenger_message_text_other"
                                            size 16
                                            color "#1a1a1a"
                                        text msg.time:
                                            style "messenger_message_time_other"
                                            size 9
                                            color "#999999"
                                            xalign 1.0
                                
                                null width 8
            
            # Индикатор набора текста
            if chat_waiting_for_response and not chat_choices_shown:
                frame:
                    style "messenger_typing_indicator"
                    xalign 0.0
                    
                    hbox:
                        spacing 5
                        text "✎" size 12 color "#c66b2f"
                        text "печатает..." size 11 color "#888888"


################################################################################
## ЭКРАН ЧАТА С ВАРИАНТАМИ ОТВЕТА
################################################################################

screen messenger_chat_with_choices():
    modal True
    zorder 200  # Высокий z-order для модального окна
    
    # НЕТ ЗАТЕМНЕНИЯ - удалено полностью
    
    frame:
        style "messenger_frame"
        xalign 0.5
        yalign 0.2
        xsize 950
        ysize 720
        
        vbox:
            # Шапка
            frame:
                style "messenger_header"
                xfill True
                
                hbox:
                    xfill True
                    spacing 12
                    
                    # Аватар
                    frame:
                        style "messenger_chat_avatar"
                        xysize (35, 35)
                        background "#c66b2f"
                        
                        $ avatar_text = current_chat_partner[0] if current_chat_partner else "?"
                        text avatar_text:
                            size 20
                            color "#ffffff"
                            xalign 0.5
                            yalign 0.5
                    
                    vbox:
                        xfill True
                        spacing 2
                        yalign 0.5
                        
                        text current_chat_partner:
                            style "messenger_chat_name"
                            size 14
                            color "#ffffff"
                            bold True
                            xalign 0.0
                        
                        if chat_status == "В сети":
                            text "онлайн":
                                style "messenger_chat_status_online"
                                size 11
                                color "#4caf50"
            
            # Область сообщений
            viewport:
                id "chat_viewport"
                ysize 450
                scrollbars "vertical"
                mousewheel True
                draggable True
                yinitial 0.4
                
                vbox:
                    spacing 8
                    xfill True
                    
                    for msg in chat_history:
                        if msg.is_user:
                            hbox:
                                xfill True
                                xalign 1.0
                                at message_appear_right
                                
                                frame:
                                    style "messenger_user_bubble"
                                    xmaximum 450
                                    
                                    vbox:
                                        spacing 2
                                        text msg.text:
                                            style "messenger_message_text_user"
                                            size 16
                                            color "#ffffff"
                                        text msg.time:
                                            style "messenger_message_time_user"
                                            size 9
                                            color "#dddddd"
                                            xalign 1.0
                                
                                null width 10
                        else:
                            hbox:
                                xfill True
                                spacing 8
                                at message_appear_left
                                
                                frame:
                                    style "messenger_message_avatar"
                                    xysize (25, 25)
                                    background "#c66b2f"
                                    
                                    $ avatar_letter = msg.character[0] if msg.character else "?"
                                    text avatar_letter:
                                        size 14
                                        color "#ffffff"
                                        xalign 0.5
                                        yalign 0.5
                                
                                frame:
                                    style "messenger_other_bubble"
                                    xmaximum 450
                                    
                                    vbox:
                                        spacing 2
                                        text msg.character:
                                            style "messenger_message_name"
                                            size 11
                                            color "#c66b2f"
                                            bold True
                                        text msg.text:
                                            style "messenger_message_text_other"
                                            size 16
                                            color "#1a1a1a"
                                        text msg.time:
                                            style "messenger_message_time_other"
                                            size 9
                                            color "#999999"
                                            xalign 1.0
                                
                                null width 8
            
            # Разделитель
            frame:
                xfill True
                ysize 1
                background "#e0e0e0"
                ypadding 0
            
            # Область с вариантами ответа
            if chat_choices:
                frame:
                    style "messenger_choices_area"
                    xfill True
                    
                    vbox:
                        spacing 6
                        xfill True
                        
                        text "ВЫБЕРИТЕ ОТВЕТ:" size 11 color "#999999" xalign 0.5 bold True
                        
                        for choice_text in chat_choices:
                            button:
                                style "messenger_choice_button"
                                xfill True
                                xalign 0.5
                                action Function(select_chat_choice, choice_text)
                                
                                text choice_text:
                                    style "messenger_choice_text"
                                    size 14
                                    color "#2b2b2b"
                                    xalign 0.5


################################################################################
## СТИЛИ ДЛЯ МЕССЕНДЖЕРА
################################################################################

style messenger_frame:
    background Frame("gui/frame.png", 12, 12, 12, 12)
    padding (0, 0)

style messenger_header:
    background "#2b2b2b"
    ysize 50
    padding (10, 6)

style messenger_close_button:
    background None
    hover_background None
    xsize 30
    ysize 30

style messenger_close_button_text:
    color "#ffffff"
    hover_color "#c66b2f"
    size 20
    yalign 0.5

style messenger_chat_avatar:
    background "#c66b2f"
    xysize (35, 35)

style messenger_chat_name:
    font "FOT-YurukaStd-UB.otf"
    outlines [(1, "#000000", 0, 0)]

style messenger_chat_status_online:
    font "FOT-YurukaStd-UB.otf"

style messenger_typing_indicator:
    background None
    padding (6, 3)

# Стили для сообщений пользователя
style messenger_user_bubble:
    background "#c66b2f"
    padding (10, 7)
    margin (6, 3, 10, 3)
    xalign 1.0

style messenger_message_text_user:
    font "LeticeaBumsteadCyrillic.otf"
    color "#ffffff"
    xalign 0.0

style messenger_message_time_user:
    font "FOT-YurukaStd-UB.otf"
    color "#dddddd"
    xalign 1.0

# Стили для сообщений собеседника
style messenger_other_bubble:
    background "#f0f0f0"
    padding (10, 7)
    margin (6, 3, 35, 3)

style messenger_message_avatar:
    background "#c66b2f"
    xysize (25, 25)

style messenger_message_name:
    font "FOT-YurukaStd-UB.otf"
    color "#c66b2f"

style messenger_message_text_other:
    font "LeticeaBumsteadCyrillic.otf"
    color "#1a1a1a"

style messenger_message_time_other:
    font "FOT-YurukaStd-UB.otf"
    color "#999999"
    xalign 1.0

# Стили для области выбора ответов
style messenger_choices_area:
    background "#f8f8f8"
    padding (12, 10)
    xfill True

style messenger_choice_button:
    background "gui/button/choice_var.png"
    hover_background "gui/button/choice_var_hover.png"
    padding (10, 8)
    xfill True
    xmaximum 900
    xalign 0.5

style messenger_choice_text:
    hover_color "#ffffff"
    xalign 0.5
    yalign 0.5
    size 14
    color "#2b2b2b"
    text_align 0.5