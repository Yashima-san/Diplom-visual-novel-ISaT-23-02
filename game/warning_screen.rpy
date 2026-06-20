################################################################################
## ЭКРАН ПРЕДУПРЕЖДЕНИЯ
################################################################################
screen warning_screen():
    modal True
    zorder 200
    add "gui/overlay/confirm.png"
    
    frame:
        background Frame("gui/confirm_frame.png", 25, 25)
        xalign 0.5
        yalign 0.5
        xsize 700
        ysize 500
        padding (30, 30)
        
        vbox:
            spacing 25
            xalign 0.5
            yalign 0.5
            
            text "⚠️ ВНИМАНИЕ":
                size 40
                color "#ff4444"
                xalign 0.5
                outlines [(2, "#1a1a1a", 0, 0)]
            
            text "Эта игра содержит темы, связанные с эмоциональными переживаниями, тревогой и сложными социальными ситуациями.":
                size 22
                xalign 0.5
                text_align 0.5
                outlines [(1, "#1a1a1a", 0, 0)]
            
            text "Все персонажи и события являются вымышленными. Любое сходство с реальными людьми случайно.":
                size 20
                xalign 0.5
                text_align 0.5
                outlines [(1, "#1a1a1a", 0, 0)]
            
            text "Игра предназначена для аудитории старше 12 лет.":
                size 20
                xalign 0.5
                text_align 0.5
                outlines [(1, "#1a1a1a", 0, 0)]
            
            null height 10
            
            textbutton "Я понимаю и принимаю":
                xalign 0.5
                action Return(True)
                background Frame("gui/button/choice_idle_background_0.png", 15, 15)
                hover_background Frame("gui/button/choice_hover_background_1.png", 15, 15)
                padding (25, 12)
                xsize 350
                text_style "warning_accept_button_text"
    
    key "K_RETURN" action Return(True)

init -1 python:
    style.create("warning_accept_button_text", "button_text")
    style.warning_accept_button_text.color = "#b4744e"
    style.warning_accept_button_text.hover_color = "#ff9999"
    style.warning_accept_button_text.size = 24
    style.warning_accept_button_text.outlines = [(2, "#671a1a", 0, 0)]
    style.warning_accept_button_text.text_align = 0.5
    style.warning_accept_button_text.xalign = 0.5