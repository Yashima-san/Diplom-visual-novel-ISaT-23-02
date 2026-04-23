################################################################################
## МИНИ-ИГРА: КОЛЕСО ЭМОЦИЙ
################################################################################

screen emotion_selection_extended():
    modal True
    zorder 200
    add "#000000CC"
    
    default selected_emotions = []
    
    frame:
        background Frame("gui/confirm_frame.png", 25, 25)
        padding (40, 40)
        xysize (1400, 850)
        xalign 0.5
        yalign 0.5
        
        vbox:
            spacing 20
            xfill True
            
            text "Колесо эмоций Роберта Плутчика" size 32 color gui.accent_color xalign 0.5
            
            text "Выбери эмоции, которые ты сейчас испытываешь:" size 24 xalign 0.5
            
            null height 10
            
            viewport:
                ysize 500
                scrollbars "vertical"
                mousewheel True
                draggable True
                
                grid 3 3:
                    spacing 20
                    xalign 0.5
                    
                    # Базовые эмоции
                    for emotion in ["Радость", "Доверие", "Страх", "Удивление", "Печаль", "Отвращение", "Гнев", "Предвкушение"]:
                        button:
                            style "emotion_button"
                            xsize 350
                            action ToggleScreenVariable("selected_emotions", emotion)
                            
                            if emotion in selected_emotions:
                                frame:
                                    style "emotion_button_selected"
                                    xfill True
                                    text emotion size 24 xalign 0.5 yalign 0.5
                            else:
                                frame:
                                    style "emotion_button_idle"
                                    xfill True
                                    text emotion size 24 xalign 0.5 yalign 0.5
            
            null height 20
            
            hbox:
                spacing 30
                xalign 0.5
                
                textbutton "Подтвердить":
                    style "emotion_confirm_button"
                    action Return(selected_emotions)
                
                textbutton "Отмена":
                    style "emotion_confirm_button"
                    action Return([])
    
    key "K_ESCAPE" action Return([])

style emotion_button:
    xsize 350
    ysize 80
    padding (0, 0)

style emotion_button_idle:
    background Frame("gui/button/choice_idle_background_0.png", 15, 15)
    padding (20, 20)

style emotion_button_selected:
    background Frame("gui/button/choice_hover_background_1.png", 15, 15)
    padding (20, 20)

style emotion_confirm_button:
    background Frame("gui/button/choice_idle_background.png", 15, 15)
    hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
    padding (20, 10)
    xsize 200

style emotion_confirm_button_text:
    color "#ffffff"
    hover_color "#ff9999"
    size 22
    text_align 0.5