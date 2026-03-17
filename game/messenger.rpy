################################################################################
## Система мессенджера
################################################################################

init python:
    # Класс для сообщений в чате
    class ChatMessage:
        def __init__(self, character, text, time=None, is_user=False):
            self.character = character
            self.text = text
            self.is_user = is_user
            import time as tm
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
    
    # Название мессенджера (отсылка к Discord/Telegram)
    MESSENGER_NAME = "Discordia"  # Комбинация Discord и "дискордия" (разлад)
    # Альтернативные варианты:
    # MESSENGER_NAME = "ChatGram"  # Telegram + Chat
    # MESSENGER_NAME = "VibeChat"  # Современный вайб

# Экран чата-мессенджера
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
                    
                    # Кнопка закрытия (если нужна)
                    textbutton "✕" xpos 1100 yalign 0.5 action Hide("messenger_chat")
            
            # Область сообщений
            viewport:
                id "chat_viewport"
                ysize 540
                scrollbars "vertical"
                mousewheel True
                draggable True
                yinitial 1.0  # Всегда показываем последние сообщения
                
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
                                    text msg.character[0]:
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
                    
                    # Кнопка для загрузки истории (если нужно)
                    if len(chat_history) >= 50:
                        textbutton "Загрузить предыдущие сообщения":
                            style "messenger_load_button"
                            xalign 0.5
                            ypadding 10
                            action NullAction()
            
            # Поле ввода (для будущих интерактивных чатов)
            frame:
                style "messenger_input_area"
                xfill True
                
                hbox:
                    xfill True
                    spacing 10
                    
                    # Поле ввода (заглушка для неинтерактивных диалогов)
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

# Стили для мессенджера
style messenger_frame:
    background Frame("gui/frame.png", 25, 25, 25, 25)
    padding (0, 0)

style messenger_header:
    background "#2b2b2b"
    ysize 80
    padding (10, 10)

style messenger_title:
    font gui.interface_text_font
    outlines [(2, "#000000", 0, 0)]

style messenger_status:
    font gui.interface_text_font

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
    font gui.interface_text_font

style messenger_message_text:
    font gui.text_font

style messenger_time:
    font gui.interface_text_font

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

# Новая функция для отображения сообщений в чате
init python:
    def messenger_say(character, text, is_user=False):
        """Отображает сообщение в чате и в обычном режиме"""
        # Добавляем в историю чата
        add_chat_message(character.name if hasattr(character, 'name') else character, text, is_user)
        # Показываем экран чата
        renpy.show_screen("messenger_chat")
        # Ждем немного для отображения
        renpy.pause(0.5)
        # Показываем обычный диалог для озвучки и паузы
        character(text)
        # Скрываем чат
        renpy.hide_screen("messenger_chat")
    
    # Заменяем стандартные Character на обертки для чата
    class ChatCharacter:
        def __init__(self, original_char):
            self.original = original_char
            self.name = original_char.name if hasattr(original_char, 'name') else str(original_char)
        
        def __call__(self, text, **kwargs):
            messenger_say(self, text, is_user=False)
    
    class UserChatCharacter:
        def __init__(self, original_char):
            self.original = original_char
            self.name = "Вы"
        
        def __call__(self, text, **kwargs):
            messenger_say(self, text, is_user=True)
    
    # Функция для преобразования персонажей в чат-версии
    def enable_chat_mode():
        global e, user_char, thought_user
        # Создаем чат-версии персонажей
        chat_e = ChatCharacter(e)
        chat_user = UserChatCharacter(user_char)
        chat_thought = UserChatCharacter(thought_user)
        
        # Временно заменяем
        e = chat_e
        user_char = chat_user
        thought_user = chat_thought
        
        # Очищаем историю перед новой перепиской
        clear_chat()
    
    # Функция для отключения чат-режима
    def disable_chat_mode():
        global e, user_char, thought_user
        # Возвращаем оригинальные персонажи
        # (нужно сохранить их в отдельные переменные при старте)
        pass