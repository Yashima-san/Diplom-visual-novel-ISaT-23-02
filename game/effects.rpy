################################################################################
## ЭФФЕКТЫ: ТРЯСКА, СТОЛКНОВЕНИЯ И ДРУГИЕ ВИЗУАЛЬНЫЕ ЭФФЕКТЫ
################################################################################

# Тряска экрана
transform screen_shake(intensity=5, duration=0.3):
    linear 0.05 xoffset intensity yoffset intensity
    linear 0.05 xoffset -intensity yoffset -intensity
    linear 0.05 xoffset intensity * 0.5 yoffset -intensity * 0.5
    linear 0.05 xoffset -intensity * 0.5 yoffset intensity * 0.5
    linear 0.05 xoffset intensity * 0.3 yoffset intensity * 0.3
    linear 0.05 xoffset 0 yoffset 0

# Мягкая тряска экрана (менее интенсивная)
transform screen_gentle_shake(intensity=3, duration=0.3):
    linear 0.05 xoffset intensity yoffset 0
    linear 0.05 xoffset -intensity yoffset 0
    linear 0.05 xoffset intensity * 0.5 yoffset 0
    linear 0.05 xoffset -intensity * 0.5 yoffset 0
    linear 0.1 xoffset 0 yoffset 0

# Функция для создания эффекта удара
init python:
    def play_hit_effect():
        renpy.with_statement(Shake((0, 0, 0, 0), 0.3, dist=10))
        renpy.play("sounds/hit.mp3", channel="sound")

# Использование в сценах:
# show expression "screen_shake" as shake
# with Shake((0, 0, 0, 0), 0.5, dist=15)