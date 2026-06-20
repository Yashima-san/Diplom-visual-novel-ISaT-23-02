## Основное
define config.name = _("За гранью чувств")
define gui.show_name = True
define config.version = "1.0"

define gui.about = _p("""
Игровой проект был сделан для обучения понимания чувств и личности человека.
""")

define build.name = "ZagranyuChuvstv"

## Звуки и музыка
define config.has_sound = True
define config.has_music = True
define config.has_voice = True

define config.main_menu_music = "song/Menu_audio_1.mp3"

## Переходы (увеличиваем длительность для комфортного чтения)
define config.enter_transition = Dissolve(0.5)
define config.exit_transition = Dissolve(0.5)
define config.intra_transition = Dissolve(0.3)
define config.after_load_transition = None
define config.end_game_transition = None

## Управление окнами
define config.window = "auto"
define config.window_show_transition = Dissolve(0.3)
define config.window_hide_transition = Dissolve(0.3)

## Стандартные настройки (МЕДЛЕННАЯ СКОРОСТЬ ТЕКСТА)
default preferences.text_cps = 20
default preferences.afm_time = 15
default preferences.afm_enable = False  # Авто-чтение выключено по умолчанию

## Отключаем анимацию атрибутов персонажей (иногда вызывает глюки)
define config.say_attribute_transition = None

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