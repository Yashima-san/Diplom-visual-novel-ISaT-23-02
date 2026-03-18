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
    
    def add_chat_message(character, text, is_user=False):
        chat_history.append(ChatMessage(character, text, is_user=is_user))
        if len(chat_history) > 50:
            chat_history.pop(0)
    
    def clear_chat():
        global chat_history
        chat_history = []
    
    MESSENGER_NAME = "Discordia"
    
    chat_choices = []
    chat_choice_callback = None
    chat_active = False
    chat_choices_shown = False
    current_chat_partner = "Лина"
    chat_status = "В сети"
    
    def show_chat_choices(choices, callback):
        global chat_choices, chat_choice_callback, chat_active, chat_choices_shown
        chat_choices = choices
        chat_choice_callback = callback
        chat_active = True
        chat_choices_shown = True
        renpy.show_screen("messenger_chat_with_choices", _layer="screens")
    
    def select_chat_choice(choice_text):
        global chat_choices, chat_choice_callback, chat_active, chat_choices_shown
        if chat_choice_callback:
            user_name = persistent.user_name if persistent.user_name else "Вы"
            add_chat_message(user_name, choice_text, is_user=True)
            chat_choice_callback(choice_text)
        chat_choices = []
        chat_choice_callback = None
        chat_choices_shown = False
        
    def close_chat():
        global chat_active, chat_choices_shown
        chat_active = False
        chat_choices_shown = False
        renpy.hide_screen("messenger_chat_with_choices")
        renpy.hide_screen("mobile_messenger")
    
    def send_message_with_delay(character, text, delay=2.0):
        global chat_status
        
        chat_status = "Печатает..."
        renpy.restart_interaction()
        
        renpy.pause(delay)
        
        chat_status = "В сети"
        renpy.restart_interaction()
        
        char_name = character.name if hasattr(character, 'name') else str(character)
        add_chat_message(char_name, text, False)
        renpy.restart_interaction()

# ИСПРАВЛЕННЫЙ экран чата с вариантами ответа
screen messenger_chat_with_choices():
    modal True
    zorder 200
    
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

# ИСПРАВЛЕННЫЙ мобильный экран чата
screen mobile_messenger():
    modal True
    zorder 200
    
    frame:
        style "mobile_messenger_frame"
        xalign 0.5
        yalign 0.5
        xsize 800
        ysize 1400
        
        vbox:
            frame:
                style "mobile_status_bar"
                xfill True
                
                hbox:
                    xfill True
                    
                    text "9:41" size 24 color "#ffffff" xalign 0.0
                    text "📶 🔋 100%" size 20 color "#ffffff" xalign 1.0
            
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
                    
                    for msg in chat_history:
                        if msg.is_user:
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
                                        text msg.time:
                                            style "mobile_time"
                                            size 16
                                            color "#bbbbbb"
                                            xalign 1.0
                        else:
                            hbox:
                                xfill True
                                
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
                                
                                frame:
                                    style "mobile_other_bubble"
                                    xmaximum 500
                                    
                                    vbox:
                                        text "Лина":
                                            style "mobile_name"
                                            size 20
                                            color "#ff9e5e"
                                            bold True
                                        text msg.text:
                                            style "mobile_message_text"
                                            size 24
                                            color "#000000"
                                            line_spacing 5
                                        text msg.time:
                                            style "mobile_time"
                                            size 16
                                            color "#888888"
                                            xalign 1.0
            
            frame:
                xfill True
                ysize 2
                background "#3b3b3b"
                ypadding 0
                margin (5, 5)
            
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

# Функции для работы с чатом
init python:
    def chat_send(character, text, delay=2.0):
        global chat_status, current_chat_partner
        
        current_chat_partner = character.name if hasattr(character, 'name') else str(character)
        
        renpy.show_screen("messenger_chat_with_choices", _layer="screens")
        renpy.pause(0.2)
        
        send_message_with_delay(character, text, delay)
    
    def mobile_chat_send(character, text, delay=2.0):
        global chat_status, current_chat_partner
        
        current_chat_partner = character.name if hasattr(character, 'name') else str(character)
        
        renpy.show_screen("mobile_messenger", _layer="screens")
        renpy.pause(0.2)
        
        send_message_with_delay(character, text, delay)
    
    class ChatCharacter:
        def __init__(self, original_char):
            self.original = original_char
            self.name = original_char.name if hasattr(original_char, 'name') else str(original_char)
        
        def __call__(self, text, delay=2.0, **kwargs):
            chat_send(self, text, delay)
    
    class MobileChatCharacter:
        def __init__(self, original_char):
            self.original = original_char
            self.name = original_char.name if hasattr(original_char, 'name') else str(original_char)
        
        def __call__(self, text, delay=2.0, **kwargs):
            mobile_chat_send(self, text, delay)
    
    def enable_chat_mode():
        global e, a, t, k, lib, chat_status, chat_history
        global original_e, original_a, original_t, original_k, original_lib
        
        original_e = e
        original_a = a
        original_t = t
        original_k = k
        original_lib = lib
        
        e = ChatCharacter(original_e)
        a = ChatCharacter(original_a)
        t = ChatCharacter(original_t)
        k = ChatCharacter(original_k)
        lib = ChatCharacter(original_lib)
        
        clear_chat()
        chat_status = "В сети"
        
        renpy.run(Hide("say"))
    
    def enable_mobile_chat_mode():
        global e, a, t, k, lib, chat_status, chat_history
        global original_e, original_a, original_t, original_k, original_lib
        
        original_e = e
        original_a = a
        original_t = t
        original_k = k
        original_lib = lib
        
        e = MobileChatCharacter(original_e)
        a = MobileChatCharacter(original_a)
        t = MobileChatCharacter(original_t)
        k = MobileChatCharacter(original_k)
        lib = MobileChatCharacter(original_lib)
        
        clear_chat()
        chat_status = "В сети"
        
        renpy.run(Hide("say"))
    
    def disable_chat_mode():
        global e, a, t, k, lib, chat_status
        global original_e, original_a, original_t, original_k, original_lib
        
        e = original_e
        a = original_a
        t = original_t
        k = original_k
        lib = original_lib
        
        close_chat()
        clear_chat()
        chat_status = "В сети"
        
        renpy.run(Show("say"))