################################################################################
## Система мессенджера
################################################################################

init python:
    import time as tm
    
    # Класс для сообщений в чате
    class ChatMessage:
        def __init__(self, character, text, time=None, is_user=False):
            self.character = character
            self.text = text
            self.is_user = is_user
            self.time = time or tm.strftime("%H:%M")
    
    # История переписки
    chat_history = []
    chat_mode_active = False
    chat_choices = []
    chat_choice_callback = None
    chat_choices_shown = False
    current_chat_partner = "Лина"
    chat_status = "В сети"
    chat_pause_active = False
    chat_in_callback = False
    chat_processing_choice = False  # Флаг для предотвращения множественных вызовов
    
    # Функция для добавления сообщения в историю
    def add_chat_message(character, text, is_user=False):
        chat_history.append(ChatMessage(character, text, is_user=is_user))
        if len(chat_history) > 50:
            chat_history.pop(0)
    
    # Функция для очистки чата
    def clear_chat():
        global chat_history
        chat_history = []
    
    # Название мессенджера
    MESSENGER_NAME = "Discordia"
    
    # Функция для показа вариантов ответа
    def show_chat_choices(choices, callback):
        global chat_choices, chat_choice_callback, chat_choices_shown, chat_mode_active
        chat_choices = choices
        chat_choice_callback = callback
        chat_choices_shown = True
        chat_mode_active = True
        
        # Скрываем стандартное диалоговое окно
        renpy.run(Hide("say"))
        
        # Показываем экран чата с вариантами
        renpy.show_screen("messenger_chat_with_choices", _layer="screens")
        renpy.restart_interaction()
    
    # Функция для выбора варианта
    def select_chat_choice(choice_text):
        global chat_choices, chat_choice_callback, chat_choices_shown, chat_in_callback, chat_processing_choice
        
        # Предотвращаем множественные вызовы
        if chat_processing_choice:
            return
        
        chat_processing_choice = True
        
        # Добавляем сообщение пользователя в историю
        user_name = persistent.user_name if persistent.user_name else "Вы"
        add_chat_message(user_name, choice_text, is_user=True)
        renpy.restart_interaction()
        
        # Сохраняем callback и очищаем перед вызовом
        callback = chat_choice_callback
        chat_choices = []
        chat_choice_callback = None
        chat_choices_shown = False
        
        # Устанавливаем флаг, что мы в callback
        chat_in_callback = True
        
        # Вызываем колбэк (он должен выполнить renpy.jump)
        if callback:
            callback(choice_text)
        
        # Сбрасываем флаги
        chat_in_callback = False
        chat_processing_choice = False
    
    # Функция для показа сообщения в чате (без паузы)
    def show_chat_message_now(character, text, is_user=False):
        """Показывает сообщение в чате без паузы"""
        global chat_mode_active
        
        # Добавляем в историю
        add_chat_message(character.name if hasattr(character, 'name') else character, text, is_user)
        
        # Показываем экран чата если он еще не показан
        if not chat_mode_active and not chat_choices_shown:
            chat_mode_active = True
            renpy.show_screen("messenger_chat", _layer="screens")
        
        # Обновляем экран
        renpy.restart_interaction()
    
    # Функция для показа сообщения в чате с паузой
    def show_chat_message(character, text, is_user=False):
        """Показывает сообщение в чате с паузой"""
        global chat_pause_active, chat_in_callback, chat_processing_choice
        
        # Если мы в callback или обрабатываем выбор, показываем без паузы
        if chat_in_callback or chat_processing_choice:
            show_chat_message_now(character, text, is_user)
            return
        
        # Предотвращаем рекурсию
        if chat_pause_active:
            show_chat_message_now(character, text, is_user)
            return
        
        chat_pause_active = True
        show_chat_message_now(character, text, is_user)
        renpy.pause(1.5)
        chat_pause_active = False
    
    # Функция для скрытия чата
    def hide_chat():
        global chat_mode_active, chat_choices_shown
        chat_mode_active = False
        chat_choices_shown = False
        renpy.hide_screen("messenger_chat")
        renpy.hide_screen("messenger_chat_with_choices")
        renpy.restart_interaction()
    
    # Класс для персонажей в чате
    class ChatCharacter:
        def __init__(self, name, color=None):
            self.name = name
            self.color = color
        
        def __call__(self, text):
            show_chat_message(self, text, is_user=False)
    
    # Класс для пользователя
    class UserChatCharacter:
        def __init__(self, name):
            self.name = name
        
        def __call__(self, text):
            show_chat_message(self, text, is_user=True)
    
    # Функция для отправки сообщения от пользователя
    def user_say(text):
        """Отправляет сообщение от имени пользователя"""
        if hasattr(persistent, 'user_name') and persistent.user_name:
            name = persistent.user_name
        else:
            name = "Вы"
        
        # Создаем временный объект для сообщения
        class TempUser:
            def __init__(self, name):
                self.name = name
        
        show_chat_message(TempUser(name), text, is_user=True)
    
    # Сохраняем оригинальных персонажей
    original_e = None
    original_user_char = None
    original_a = None
    original_t = None
    original_k = None
    original_lib = None
    
    def enable_chat_mode():
        """Включает режим чата для персонажей"""
        global original_e, original_user_char, original_a, original_t, original_k, original_lib
        global e, user_char, a, t, k, lib
        
        # Сохраняем оригиналы
        original_e = e
        original_user_char = user_char
        original_a = a
        original_t = t
        original_k = k
        original_lib = lib
        
        # Создаем чат-версии
        e = ChatCharacter("Лина")
        user_char = UserChatCharacter(persistent.user_name if persistent.user_name else "Вы")
        a = ChatCharacter("Алекс")
        t = ChatCharacter("Анна Сергеевна")
        k = ChatCharacter("Катя")
        lib = ChatCharacter("Библиотекарь")
        
        # Очищаем историю
        clear_chat()
    
    def enable_mobile_chat_mode():
        """Включает мобильный режим чата"""
        enable_chat_mode()
    
    def disable_chat_mode():
        """Выключает режим чата"""
        global original_e, original_user_char, original_a, original_t, original_k, original_lib
        global e, user_char, a, t, k, lib
        
        # Сначала скрываем чат
        hide_chat()
        
        # Восстанавливаем оригиналы
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
        
        # Очищаем историю
        clear_chat()


# Экран чата (простой, без вариантов)
screen messenger_chat():
    # Стилизованный фон под чат
    frame:
        style "messenger_frame"
        xalign 0.5
        yalign 0.5
        xsize 1200
        ysize 700
        
        vbox:
            # Шапка чата
            frame:
                style "messenger_header"
                xfill True
                
                hbox:
                    xfill True
                    
                    # Иконка мессенджера
                    text "💬" size 36 xpos 20 yalign 0.5
                    
                    # Название и статус
                    vbox:
                        xalign 0.5
                        yalign 0.5
                        text MESSENGER_NAME:
                            style "messenger_title"
                            size 24
                            color "#ffffff"
                            bold True
                        text "онлайн":
                            style "messenger_status"
                            size 16
                            color "#4caf50"
                    
                    # Кнопка закрытия
                    textbutton "✕" xpos 1100 yalign 0.5 action Function(hide_chat)
            
            # Область сообщений
            viewport:
                id "chat_viewport"
                ysize 540
                scrollbars "vertical"
                mousewheel True
                draggable True
                yinitial 1.0
                
                vbox:
                    spacing 10
                    xfill True
                    
                    # Отображаем все сообщения из истории
                    for msg in chat_history:
                        if msg.is_user:
                            # Сообщение пользователя (справа)
                            hbox:
                                xfill True
                                xalign 1.0
                                
                                frame:
                                    style "messenger_user_bubble"
                                    xmaximum 600
                                    
                                    vbox:
                                        text msg.text:
                                            style "messenger_message_text"
                                            size 22
                                            color "#ffffff"
                                        text msg.time:
                                            style "messenger_time"
                                            size 14
                                            color "#bbbbbb"
                                            xalign 1.0
                        else:
                            # Сообщение другого персонажа (слева)
                            hbox:
                                xfill True
                                
                                # Аватар персонажа
                                frame:
                                    style "messenger_avatar"
                                    xysize (50, 50)
                                    background "#c66b2f"
                                    
                                    # Первая буква имени как аватар
                                    $ initial = msg.character[0] if msg.character else "?"
                                    text initial:
                                        size 30
                                        color "#ffffff"
                                        xalign 0.5
                                        yalign 0.5
                                
                                frame:
                                    style "messenger_other_bubble"
                                    xmaximum 600
                                    
                                    vbox:
                                        text msg.character:
                                            style "messenger_name"
                                            size 18
                                            color "#ff9e5e"
                                            bold True
                                        text msg.text:
                                            style "messenger_message_text"
                                            size 22
                                            color "#000000"
                                        text msg.time:
                                            style "messenger_time"
                                            size 14
                                            color "#888888"
                                            xalign 1.0
            
            # Поле ввода (для будущих интерактивных чатов)
            frame:
                style "messenger_input_area"
                xfill True
                
                hbox:
                    xfill True
                    spacing 10
                    
                    # Поле ввода (заглушка)
                    frame:
                        style "messenger_input_field"
                        xfill True
                        ysize 60
                        
                        text "Введите сообщение..." size 20 color "#888888" xpos 20 yalign 0.5
                    
                    # Кнопка отправки (заглушка)
                    frame:
                        style "messenger_send_button"
                        xysize (60, 60)
                        background "#c66b2f"
                        
                        text "➤" size 30 color "#ffffff" xalign 0.5 yalign 0.5


# Экран чата с вариантами ответа
screen messenger_chat_with_choices():
    modal True
    zorder 200
    
    # Затемнение фона
    add "#00000080"
    
    frame:
        style "messenger_frame"
        xalign 0.5
        yalign 0.5
        xsize 1300
        ysize 900
        
        vbox:
            # Шапка мессенджера
            frame:
                style "messenger_header"
                xfill True
                
                hbox:
                    xfill True
                    
                    text "💬" size 36 xpos 20 yalign 0.5
                    
                    text MESSENGER_NAME:
                        style "messenger_title"
                        size 24
                        color "#ffffff"
                        bold True
                        xalign 0.5
                        yalign 0.5
                    
                    null width 50
            
            # Информация о собеседнике
            frame:
                style "chat_partner_info"
                xfill True
                
                vbox:
                    spacing 5
                    xalign 0.5
                    
                    text current_chat_partner:
                        style "chat_partner_name"
                        size 28
                        color "#ffffff"
                        bold True
                        xalign 0.5
                    
                    if chat_status == "В сети":
                        text "В сети":
                            style "chat_partner_status_online"
                            size 18
                            xalign 0.5
                    else:
                        text "Печатает...":
                            style "chat_partner_status_typing"
                            size 18
                            xalign 0.5
            
            # Область сообщений
            viewport:
                id "chat_viewport"
                ysize 450
                scrollbars "vertical"
                mousewheel True
                draggable True
                yinitial 1.0
                
                vbox:
                    spacing 15
                    xfill True
                    
                    for msg in chat_history:
                        if msg.is_user:
                            hbox:
                                xfill True
                                xalign 1.0
                                
                                frame:
                                    style "messenger_user_bubble"
                                    xmaximum 600
                                    
                                    vbox:
                                        text msg.text:
                                            style "messenger_message_text"
                                            size 22
                                            color "#ffffff"
                                            xalign 0.0
                                            line_spacing 5
                                        text msg.time:
                                            style "messenger_time"
                                            size 14
                                            color "#bbbbbb"
                                            xalign 1.0
                        else:
                            hbox:
                                xfill True
                                
                                frame:
                                    style "messenger_other_bubble"
                                    xmaximum 600
                                    
                                    vbox:
                                        text msg.character:
                                            style "messenger_name"
                                            size 18
                                            color "#ff9e5e"
                                            bold True
                                        text msg.text:
                                            style "messenger_message_text"
                                            size 22
                                            color "#000000"
                                            line_spacing 5
                                        text msg.time:
                                            style "messenger_time"
                                            size 14
                                            color "#888888"
                                            xalign 1.0
            
            # Разделитель
            frame:
                xfill True
                ysize 2
                background "#3b3b3b"
                ypadding 0
                margin (0, 5)
            
            # Область с вариантами ответа
            if chat_choices:
                frame:
                    style "messenger_choices_area"
                    xfill True
                    
                    viewport:
                        ysize 300
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        
                        vbox:
                            spacing 10
                            xfill True
                            
                            for choice_text in chat_choices:
                                button:
                                    style "messenger_choice_button"
                                    xfill True
                                    action Function(select_chat_choice, choice_text)
                                    
                                    text choice_text:
                                        style "messenger_choice_text"
                                        size 20
                                        color "#2b2b2b"


# Стили для мессенджера
style messenger_frame:
    background Frame("gui/frame.png", 25, 25, 25, 25)
    padding (0, 0)

style messenger_header:
    background "#2b2b2b"
    ysize 80
    padding (10, 10)

style messenger_title:
    font "FOT-YurukaStd-UB.otf"
    outlines [(2, "#000000", 0, 0)]

style messenger_status:
    font "FOT-YurukaStd-UB.otf"

style messenger_user_bubble:
    background "#c66b2f"
    padding (15, 10)
    margin (10, 5, 50, 5)
    xalign 1.0

style messenger_other_bubble:
    background "#f0f0f0"
    padding (15, 10)
    margin (10, 5, 50, 5)

style messenger_avatar:
    background "#c66b2f"
    xysize (50, 50)
    xalign 0.0

style messenger_name:
    font "FOT-YurukaStd-UB.otf"

style messenger_message_text:
    font "LeticeaBumsteadCyrillic.otf"

style messenger_time:
    font "FOT-YurukaStd-UB.otf"

style messenger_input_area:
    background "#2b2b2b"
    ysize 80
    padding (20, 10)

style messenger_input_field:
    background "#3b3b3b"
    ysize 60
    xfill True

style messenger_send_button:
    ysize 60
    xsize 60
    hover_background "#ff9e5e"

style messenger_load_button:
    background Frame("gui/button/choice_idle_background.png", 10, 10, 10, 10)
    hover_background Frame("gui/button/choice_hover_background_1.png", 10, 10, 10, 10)
    padding (20, 5)
    xalign 0.5

# Стили для экрана с вариантами
style chat_partner_info:
    background "#363636"
    ysize 80
    padding (20, 10)
    xfill True

style chat_partner_name:
    font "FOT-YurukaStd-UB.otf"
    outlines [(2, "#000000", 0, 0)]
    xalign 0.5

style chat_partner_status_online:
    font "FOT-YurukaStd-UB.otf"
    color "#4caf50"
    xalign 0.5

style chat_partner_status_typing:
    font "FOT-YurukaStd-UB.otf"
    color "#ffaa00"
    xalign 0.5

style messenger_choices_area:
    background "#2b2b2b"
    padding (15, 10)
    xfill True

style messenger_choice_button:
    background "gui/button/choice_var.png"
    hover_background "gui/button/choice_var_hover.png"
    padding (15, 10)
    xfill True
    xmaximum 1250
    xalign 0.5

style messenger_choice_text:
    hover_color "#ffffff"
    xalign 0.5
    yalign 0.5
    size 20
    line_spacing 5
    color "#2b2b2b"
    layout "subtitle"
    text_align 0.5