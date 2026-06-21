## Данный файл содержит настройки, способные изменить вашу игру.

## Основное
define config.name = _("За гранью чувств")
define gui.show_name = True
define config.version = "1.2"

define gui.about = _p("""
Игровой проект был сделан для обучения понимания чувств и личности человека.
""")

define build.name = "ZagranyuChuvstv"

## Звуки и музыка
define config.has_sound = True
define config.has_music = True
define config.has_voice = True

define config.main_menu_music = "song/Menu_audio_1.mp3"

## Переходы
define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.intra_transition = dissolve
define config.after_load_transition = None
define config.end_game_transition = None

## Управление окнами
define config.window = "auto"
define config.window_show_transition = Dissolve(0.2)
define config.window_hide_transition = Dissolve(0.2)

## Стандартные настройки
default preferences.text_cps = 65
default preferences.afm_time = 15

## Директория сохранений
define config.save_directory = "ZagranyuChuvstv-1762831903"

## Иконка
define config.window_icon = "gui/window_icon.png"

## Настройка Дистрибутива
init python:
    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)

    build.documentation('*.html')
    build.documentation('*.txt')