################################################################################
## Система мессенджера
################################################################################

init python:
    import time as tm
    import threading
    
    # Класс для сообщений в чате
    class ChatMessage:
        def __init__(self, character, text, time=None, is_user=False):
            self.character = character
            self.text = text
            self.is_user = is_user
            self.time = time or tm.strftime("%H:%M")
    
    # История переписки
    chat_history = []
    
    # Функция для добавления сообщения в историю
    def add_chat_message(character, text, is_user=False):
        chat_history.append(ChatMessage(character, text, is_user=is_user))
        # Ограничиваем историю последними 50 сообщениями
        if len(chat_history) > 50:
            chat_history.pop(0)
    
    # Функция для очистки чата
    def clear_chat():
        global chat_history
        chat_history = []
    
    # Название мессенджера
    MESSENGER_NAME = "Discordia"
    
    # Временное хранилище для вариантов ответа
    chat_choices = []
    chat_choice_callback = None
    chat_active = False  # Флаг активности чата
    chat_choices_shown = False  # Флаг, были ли показаны варианты
    current_chat_partner = "Лина"  # Имя персонажа для чата
    chat_status = "В сети"  # Статус чата
    
    # Функция для показа вариантов ответа в чате
    def show_chat_choices(choices, callback):
        global chat_choices, chat_choice_callback, chat_active, chat_choices_shown
        chat_choices = choices
        chat_choice_callback = callback
        chat_active = True
        chat_choices_shown = True
        renpy.show_screen("messenger_chat_with_choices", _layer="screens")
    
    # Функция для обработки выбора
    def select_chat_choice(choice_text):
        global chat_choices, chat_choice_callback, chat_active, chat_choices_shown
        if chat_choice_callback:
            # Добавляем сообщение пользователя в историю чата
            add_chat_message(persistent.user_name if persistent.user_name else "Вы", choice_text, is_user=True)
            # Вызываем callback с выбранным текстом
            chat_choice_callback(choice_text)
        # Очищаем варианты, но оставляем чат открытым
        chat_choices = []
        chat_choice_callback = None
        chat_choices_shown = False
        
    # Функция для закрытия чата
    def close_chat():
        global chat_active, chat_choices_shown
        chat_active = False
        chat_choices_shown = False
        renpy.hide_screen("messenger_chat_with_choices")
        renpy.hide_screen("mobile_messenger")
    
    # Функция для отправки сообщения от персонажа с задержкой
    def send_message_with_delay(character, text, delay=5.0):
        global chat_status
        
        # Меняем статус на "Печатает..."
        chat_status = "Печатает..."
        renpy.restart_interaction()
        
        # Ждем указанное количество секунд
        renpy.pause(delay)
        
        # Возвращаем статус "В сети"
        chat_status = "В сети"
        renpy.restart_interaction()
        
        # Отправляем сообщение
        char_name = character.name if hasattr(character, 'name') else str(character)
        add_chat_message(char_name, text, False)
        renpy.restart_interaction()

# ИСПРАВЛЕННЫЙ экран чата с вариантами ответа
screen messenger_chat_with_choices():
    # Важно: делаем экран модальным и с высоким zorder
    modal True
    zorder 200
    
    # Стилизованный фон под чат
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
                    
                    # Иконка мессенджера
                    text "💬" size 36 xpos 20 yalign 0.5
                    
                    # Название мессенджера
                    text MESSENGER_NAME:
                        style "messenger_title"
                        size 24
                        color "#ffffff"
                        bold True
                        xalign 0.5
                        yalign 0.5
                    
                    # Пустое место для баланса
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
                    
                    # ИСПРАВЛЕНО: Используем два разных текстовых элемента с условием показа
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
                                            xalign 0.0
                                            yalign 0.0
                                            line_spacing 5
                                            substitute False
                                        text msg.time:
                                            style "messenger_time"
                                            size 14
                                            color "#bbbbbb"
                                            xalign 1.0
                                            yalign 1.0
                                            substitute False
                        else:
                            # Сообщение другого персонажа (слева)
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
                                            substitute False
                                        text msg.text:
                                            style "messenger_message_text"
                                            size 22
                                            color "#000000"
                                            line_spacing 5
                                            substitute False
                                        text msg.time:
                                            style "messenger_time"
                                            size 14
                                            color "#888888"
                                            xalign 1.0
                                            substitute False
            
            # Разделитель
            frame:
                xfill True
                ysize 2
                background "#3b3b3b"
                ypadding 0
                margin (0, 5)
            
            # Панель ввода
            frame:
                style "input_panel"
                xfill True
                
                hbox:
                    xfill True
                    spacing 10
                    
                    frame:
                        style "input_field"
                        xfill True
                        xsize 800
                        
                        # ИСПРАВЛЕНО: Убираем left_margin, используем xpos для отступа
                        text "Введите текст...":
                            style "input_placeholder"
                            size 20
                            color "#888888"
                            xpos 15
                            yalign 0.5
            
            # Область с вариантами ответа (показываем только если есть варианты)
            if chat_choices:
                frame:
                    style "messenger_choices_area"
                    xfill True
                    ysize 200
                    
                    viewport:
                        ysize 180
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
                                        xalign 0.5
                                        yalign 0.5
                                        line_spacing 5
                                        substitute False

# ИСПРАВЛЕННЫЙ экран чата для мобильного телефона
screen mobile_messenger():
    modal True
    zorder 200
    
    # Стилизованный фон под экран телефона
    frame:
        style "mobile_messenger_frame"
        xalign 0.5
        yalign 0.5
        xsize 800
        ysize 1400
        
        vbox:
            # Верхняя панель с временем и батареей
            frame:
                style "mobile_status_bar"
                xfill True
                
                hbox:
                    xfill True
                    
                    text "9:41" size 24 color "#ffffff" xalign 0.0
                    text "📶 🔋 100%" size 20 color "#ffffff" xalign 1.0
            
            # Шапка чата
            frame:
                style "mobile_chat_header"
                xfill True
                
                hbox:
                    xfill True
                    
                    text MESSENGER_NAME:
                        size 24
                        color "#ffffff"
                        bold True
                        xalign 0.5
                        yalign 0.5
            
            # Информация о собеседнике
            frame:
                style "mobile_chat_partner_info"
                xfill True
                
                hbox:
                    xalign 0.5
                    spacing 15
                    
                    frame:
                        style "mobile_contact_avatar"
                        xysize (60, 60)
                        background "#c66b2f"
                        text "Л" size 40 color "#ffffff" xalign 0.5 yalign 0.5
                    
                    vbox:
                        yalign 0.5
                        text "Лина" size 28 color "#ffffff" bold True
                        # ИСПРАВЛЕНО: Используем два разных текстовых элемента с условием показа
                        if chat_status == "В сети":
                            text "В сети":
                                size 18
                                color "#4caf50"
                                xalign 0.5
                        else:
                            text "Печатает...":
                                size 18
                                color "#ffaa00"
                                xalign 0.5
            
            # Область сообщений
            viewport:
                id "mobile_chat_viewport"
                ysize 800
                scrollbars "vertical"
                mousewheel True
                draggable True
                yinitial 1.0
                
                vbox:
                    spacing 15
                    xfill True
                    
                    # Отображаем все сообщения из истории
                    for msg in chat_history:
                        if msg.is_user:
                            # Сообщение пользователя (справа)
                            hbox:
                                xfill True
                                xalign 1.0
                                
                                frame:
                                    style "mobile_user_bubble"
                                    xmaximum 500
                                    
                                    vbox:
                                        text msg.text:
                                            style "mobile_message_text"
                                            size 24
                                            color "#ffffff"
                                            line_spacing 5
                                            substitute False
                                        text msg.time:
                                            style "mobile_time"
                                            size 16
                                            color "#bbbbbb"
                                            xalign 1.0
                                            substitute False
                        else:
                            # Сообщение Лины (слева)
                            hbox:
                                xfill True
                                
                                # Аватар Лины
                                frame:
                                    style "mobile_avatar"
                                    xysize (60, 60)
                                    background "#c66b2f"
                                    $ char_initial = msg.character[0] if msg.character else "?"
                                    text "[char_initial]":
                                        size 40
                                        color "#ffffff"
                                        xalign 0.5
                                        yalign 0.5
                                        substitute False
                                
                                frame:
                                    style "mobile_other_bubble"
                                    xmaximum 500
                                    
                                    vbox:
                                        text "Лина":
                                            style "mobile_name"
                                            size 20
                                            color "#ff9e5e"
                                            bold True
                                            substitute False
                                        text msg.text:
                                            style "mobile_message_text"
                                            size 24
                                            color "#000000"
                                            line_spacing 5
                                            substitute False
                                        text msg.time:
                                            style "mobile_time"
                                            size 16
                                            color "#888888"
                                            xalign 1.0
                                            substitute False
            
            # Разделитель
            frame:
                xfill True
                ysize 2
                background "#3b3b3b"
                ypadding 0
                margin (5, 5)
            
            # Панель ввода
            frame:
                style "mobile_input_panel"
                xfill True
                
                hbox:
                    xfill True
                    spacing 10
                    
                    frame:
                        style "mobile_input_field"
                        xfill True
                        
                        # ИСПРАВЛЕНО: Убираем left_margin, используем xpos для отступа
                        text "Введите текст...":
                            style "mobile_input_placeholder"
                            size 18
                            color "#888888"
                            xpos 15
                            yalign 0.5
            
            # Нижняя панель с вариантами ответа (показываем только если есть варианты)
            if chat_choices:
                frame:
                    style "mobile_input_area"
                    xfill True
                    
                    viewport:
                        ysize 150
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        
                        vbox:
                            spacing 8
                            xfill True
                            
                            for choice_text in chat_choices:
                                button:
                                    style "mobile_choice_button"
                                    xfill True
                                    action Function(select_chat_choice, choice_text)
                                    
                                    text choice_text:
                                        style "mobile_choice_text"
                                        size 20
                                        color "#2b2b2b"
                                        xalign 0.5
                                        yalign 0.5
                                        line_spacing 4
                                        substitute False

# Стили для мессенджера
style messenger_frame:
    background Frame("gui/frame.png", 25, 25, 25, 25)
    padding (0, 0)

style messenger_header:
    background "#2b2b2b"
    ysize 60
    padding (20, 10)

style messenger_title:
    font gui.interface_text_font
    outlines [(2, "#000000", 0, 0)]
    xalign 0.5
    yalign 0.5

style chat_partner_info:
    background "#363636"
    ysize 80
    padding (20, 10)
    xfill True

style chat_partner_name:
    font gui.interface_text_font
    outlines [(2, "#000000", 0, 0)]
    xalign 0.5

# ИСПРАВЛЕНО: Добавлены отдельные стили для статусов
style chat_partner_status_online:
    font gui.interface_text_font
    color "#4caf50"
    xalign 0.5

style chat_partner_status_typing:
    font gui.interface_text_font
    color "#ffaa00"
    xalign 0.5

style input_panel:
    background "#2b2b2b"
    ysize 70
    padding (15, 10)
    xfill True

style input_field:
    background "#3b3b3b"
    ysize 50
    xfill True

style input_placeholder:
    font gui.interface_text_font
    yalign 0.5

style messenger_user_bubble:
    background "#c66b2f"
    padding (20, 15)
    margin (10, 5, 30, 5)
    xalign 1.0

style messenger_other_bubble:
    background "#f0f0f0"
    padding (20, 15)
    margin (10, 5, 30, 5)

style messenger_name:
    font gui.interface_text_font

style messenger_message_text:
    font gui.text_font
    xalign 0.0
    yalign 0.0

style messenger_time:
    font gui.interface_text_font
    xalign 1.0
    yalign 1.0

style messenger_choices_area:
    background "#2b2b2b"
    ysize 200
    padding (15, 10)
    xfill True

style messenger_choice_button:
    background "gui/thoughtbubble.png"
    hover_background "gui/thoughtbubble_hover.png"
    padding (15, 10)
    xfill True
    xalign 0.5

style messenger_choice_text:
    hover_color "#ffffff"
    xalign 0.5
    yalign 0.5
    size 20
    line_spacing 5
    color "#2b2b2b"

# Стили для мобильного мессенджера
style mobile_messenger_frame:
    background "#1a1a1a"
    padding (0, 0)

style mobile_status_bar:
    background "#000000"
    ysize 60
    padding (20, 10)

style mobile_chat_header:
    background "#2b2b2b"
    ysize 60
    padding (10, 10)

style mobile_chat_partner_info:
    background "#363636"
    ysize 100
    padding (10, 10)

style mobile_contact_avatar:
    background "#c66b2f"
    xysize (60, 60)

style mobile_avatar:
    background "#c66b2f"
    xysize (60, 60)
    margin (10, 0, 5, 0)

style mobile_user_bubble:
    background "#c66b2f"
    padding (20, 15)
    margin (10, 5, 30, 5)
    xalign 1.0

style mobile_other_bubble:
    background "#f0f0f0"
    padding (20, 15)
    margin (10, 5, 30, 5)

style mobile_name:
    font gui.interface_text_font
    size 20
    color "#ff9e5e"

style mobile_message_text:
    font gui.text_font
    size 24
    xalign 0.0
    yalign 0.0

style mobile_time:
    font gui.interface_text_font
    size 16
    xalign 1.0
    yalign 1.0

style mobile_input_panel:
    background "#2b2b2b"
    ysize 60
    padding (10, 5)

style mobile_input_field:
    background "#3b3b3b"
    ysize 45
    xfill True

style mobile_input_placeholder:
    font gui.interface_text_font
    size 18
    yalign 0.5

style mobile_input_area:
    background "#2b2b2b"
    ysize 170
    padding (10, 8)

style mobile_choice_button:
    background "gui/thoughtbubble.png"
    hover_background "gui/thoughtbubble_hover.png"
    padding (12, 8)
    xfill True
    xalign 0.5

style mobile_choice_text:
    hover_color "#ffffff"
    xalign 0.5
    yalign 0.5
    size 20
    line_spacing 4
    color "#2b2b2b"

# Функции для работы с чатом
init python:
    def chat_send(character, text, delay=5.0):
        """Отправляет сообщение от персонажа в чат с задержкой"""
        global chat_status, current_chat_partner
        
        # Устанавливаем имя собеседника
        current_chat_partner = character.name if hasattr(character, 'name') else str(character)
        
        # Показываем экран чата
        renpy.show_screen("messenger_chat_with_choices", _layer="screens")
        renpy.pause(0.2)
        
        # Отправляем сообщение с задержкой
        send_message_with_delay(character, text, delay)
    
    def mobile_chat_send(character, text, delay=5.0):
        """Отправляет сообщение в мобильный чат с задержкой"""
        global chat_status, current_chat_partner
        
        # Устанавливаем имя собеседника
        current_chat_partner = character.name if hasattr(character, 'name') else str(character)
        
        # Показываем экран чата
        renpy.show_screen("mobile_messenger", _layer="screens")
        renpy.pause(0.2)
        
        # Отправляем сообщение с задержкой
        send_message_with_delay(character, text, delay)
    
    # Класс для чат-персонажей
    class ChatCharacter:
        def __init__(self, original_char):
            self.original = original_char
            self.name = original_char.name if hasattr(original_char, 'name') else str(original_char)
        
        def __call__(self, text, delay=5.0, **kwargs):
            # Отправляем сообщение в чат с задержкой
            chat_send(self, text, delay)
    
    # Класс для мобильного чата
    class MobileChatCharacter:
        def __init__(self, original_char):
            self.original = original_char
            self.name = original_char.name if hasattr(original_char, 'name') else str(original_char)
        
        def __call__(self, text, delay=5.0, **kwargs):
            # Отправляем сообщение в мобильный чат с задержкой
            mobile_chat_send(self, text, delay)
    
    # Функция для включения режима чата
    def enable_chat_mode():
        global e, a, t, k, lib, chat_status, chat_history
        global original_e, original_a, original_t, original_k, original_lib
        
        # Сохраняем оригинальных персонажей
        original_e = e
        original_a = a
        original_t = t
        original_k = k
        original_lib = lib
        
        # Создаем чат-версии персонажей
        e = ChatCharacter(original_e)
        a = ChatCharacter(original_a)
        t = ChatCharacter(original_t)
        k = ChatCharacter(original_k)
        lib = ChatCharacter(original_lib)
        
        # Очищаем историю перед новой перепиской
        clear_chat()
        
        # Устанавливаем статус
        chat_status = "В сети"
        
        # Скрываем обычное диалоговое окно
        renpy.run(Hide("say"))
    
    # Функция для включения мобильного режима чата
    def enable_mobile_chat_mode():
        global e, a, t, k, lib, chat_status, chat_history
        global original_e, original_a, original_t, original_k, original_lib
        
        # Сохраняем оригинальных персонажей
        original_e = e
        original_a = a
        original_t = t
        original_k = k
        original_lib = lib
        
        # Создаем мобильные чат-версии персонажей
        e = MobileChatCharacter(original_e)
        a = MobileChatCharacter(original_a)
        t = MobileChatCharacter(original_t)
        k = MobileChatCharacter(original_k)
        lib = MobileChatCharacter(original_lib)
        
        # Очищаем историю перед новой перепиской
        clear_chat()
        
        # Устанавливаем статус
        chat_status = "В сети"
        
        # Скрываем обычное диалоговое окно
        renpy.run(Hide("say"))
    
    # Функция для отключения режима чата
    def disable_chat_mode():
        global e, a, t, k, lib, chat_status
        global original_e, original_a, original_t, original_k, original_lib
        
        # Возвращаем оригинальные персонажи
        e = original_e
        a = original_a
        t = original_t
        k = original_k
        lib = original_lib
        
        # Закрываем чат
        close_chat()
        
        # Очищаем историю
        clear_chat()
        
        # Сбрасываем статус
        chat_status = "В сети"
        
        # Показываем обычное диалоговое окно
        renpy.run(Show("say"))