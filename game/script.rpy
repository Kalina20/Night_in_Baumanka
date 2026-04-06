define e = Character('я', color="#ffffff")
define i = Character('Иван Писарев', color="#db4010")
define a = Character('Алексей Калиниченко', color="#559d0d")
define d = Character('Даниил Перекосов', color="#8d9ce9")
define k = Character('Константин Горшков', color="#e4e815")

define p1 = Character("Лычков Игорь Игоревич", color="#dddddd")
define p2 = Character("Недашковский Вячеслав Михайлович", color="#dddddd")
define p3 = Character("Семенцов Станислав Григорьевич", color="#dddddd")
define p5 = Character("Адамова Арина Александровна", color="#dddddd")
define p10 = Character("Кадырбаева Анастасия Рустемовна", color="#dddddd")
define p6 = Character("Бабкин Павел Сергеевич", color="#dddddd")
define p4 = Character("Брызгалов Владимир Григорьевич", color="#dddddd")
define p8 = Character("Бянкин Валерий Михайлович", color="#dddddd")
define p9 = Character("Тихомирова Елизавета Алексеевна", color="#dddddd")
define p7 = Character("Левиев Дмитрий Олегович", color="#dddddd")
define p11 = Character("Выхованец Валерий Святославович", color="#dddddd")
define p12 = Character("Фёдоров Сергей Владимирович", color="#dddddd")

default room_exit_counter = 0
default visited_cabinets = []
default ui_unlocked = False
default cabinet_scene_map = {}
default current_cabinet = None
default found_story_scene_2_item = False
default failed_story_scene_2_search = False
default story_scene_1_match_selected_left = None
default story_scene_1_match_selected_right = None
default story_scene_1_match_done = []
default story_scene_1_match_success = False
default story_scene_1_match_failed = False
default story_scene_4_squats = 0
default story_scene_4_time_left = 30
default story_scene_4_is_down = False
default story_scene_4_minigame_won = False
default story_scene_4_minigame_lost = False

init python:
    def ensure_cabinet_scene_map():
        if cabinet_scene_map:
            return

        cabinets = ["420", "421", "422", "423", "424", "425", "426", "427", "428", "429", "430", "431"]
        scene_labels = [
            "story_scene_1",
            "story_scene_2",
            "story_scene_3",
            "story_scene_4",
            "story_scene_5",
            "story_scene_6",
            "story_scene_7",
            "story_scene_8",
            "story_scene_9",
            "story_scene_10",
            "story_scene_11",
            "story_scene_12",
        ]
        # renpy.random.shuffle(scene_labels) пока закометим для отладки
        store.cabinet_scene_map = dict(zip(cabinets, scene_labels))

    def reset_story_scene_4_minigame():
        store.story_scene_4_squats = 0
        store.story_scene_4_time_left = 30
        store.story_scene_4_is_down = False
        store.story_scene_4_minigame_won = False
        store.story_scene_4_minigame_lost = False

    def reset_story_scene_1_match_game():
        store.story_scene_1_match_selected_left = None
        store.story_scene_1_match_selected_right = None
        store.story_scene_1_match_done = []
        store.story_scene_1_match_success = False
        store.story_scene_1_match_failed = False

    def story_scene_1_select_left(item_id):
        if item_id in store.story_scene_1_match_done:
            return

        store.story_scene_1_match_selected_left = item_id

        if store.story_scene_1_match_selected_right is not None:
            story_scene_1_try_match()
        else:
            renpy.restart_interaction()

    def story_scene_1_select_right(item_id):
        if item_id in store.story_scene_1_match_done:
            return

        store.story_scene_1_match_selected_right = item_id

        if store.story_scene_1_match_selected_left is not None:
            story_scene_1_try_match()
        else:
            renpy.restart_interaction()

    def story_scene_1_try_match():
        correct_pairs = {
            "2 + 2": "4",
            "5 - 2": "3",
            "3 x 3": "9",
        }

        left = store.story_scene_1_match_selected_left
        right = store.story_scene_1_match_selected_right

        if left is None or right is None:
            return

        if correct_pairs.get(left) == right:
            if left not in store.story_scene_1_match_done:
                store.story_scene_1_match_done.append(left)
            if right not in store.story_scene_1_match_done:
                store.story_scene_1_match_done.append(right)

            if len(store.story_scene_1_match_done) == 6:
                store.story_scene_1_match_success = True
        else:
            store.story_scene_1_match_failed = True

        store.story_scene_1_match_selected_left = None
        store.story_scene_1_match_selected_right = None
        renpy.restart_interaction()

    def story_scene_4_press_down():
        if store.story_scene_4_minigame_won or store.story_scene_4_minigame_lost:
            return

        if not store.story_scene_4_is_down:
            store.story_scene_4_is_down = True
            renpy.restart_interaction()

    def story_scene_4_press_up():
        if store.story_scene_4_minigame_won or store.story_scene_4_minigame_lost:
            return

        if store.story_scene_4_is_down:
            store.story_scene_4_is_down = False
            store.story_scene_4_squats += 1

            if store.story_scene_4_squats >= 30:
                store.story_scene_4_minigame_won = True

            renpy.restart_interaction()

    def story_scene_4_tick():
        if store.story_scene_4_minigame_won or store.story_scene_4_minigame_lost:
            return

        store.story_scene_4_time_left -= 1

        if store.story_scene_4_time_left <= 0:
            store.story_scene_4_time_left = 0
            if store.story_scene_4_squats >= 30:
                store.story_scene_4_minigame_won = True
            else:
                store.story_scene_4_minigame_lost = True

        renpy.restart_interaction()

label start:
    $ ensure_cabinet_scene_map()
    jump vvedenie

label vvedenie:
    scene bg room
    play music "audio/Minecraft 1.mp3" fadein 1.0
    "Эта история началась много лет назад..."
    "Несколько влиятельных людей по счастливой случайности оказались в одном университете, и даже в одной группе..."
    "Они были настолько разными, что даже не могли представить, что у них может быть что-то общее..."
    show i normal at Position(xpos=0.1, ypos=1.0) with dissolve
    "Анимешник..."
    show a normal at Position(xpos=0.3, ypos=1.0) with dissolve
    "Футболист..."
    show d normal at Position(xpos=0.6, ypos=1.0) with dissolve
    "Нефор..."
    show k normal at Position(xpos=0.9, ypos=1.0) with dissolve
    "Саратовец..."
    "Но, несмотря на все различия, они стали друзьями..."
    "Их называли {color=#ff5555}Ремонт{/color}..."
    "Никто уже и не скажет, откуда взялось это название, но оно прочно закрепилось за ними..."
    "На пути {color=#ff5555}Ремонта{/color} возникало много препятствий, но они всегда поддерживали друг друга и находили выход из любой ситуации..."
    "Они чертили, кодили, плавали, выпивали, расстраивались и радовались вместе..."
    "И, после стольких лет, они наконец дошли до финиша и успешно защитили свои выпускные квалификационные работы!"
    "Но теперь им предстояло отпраздновать это знаменательное событие...и отпраздновать с огоньком, а, вернее сказать, с ящиком Corona Extra..."
    "...Прямо в стенах их родного университета!"
    "План был надеждый, как швейцарские часы - аккуратно пронести бутылки в рюкзаках, 
    спрятать их в неприметном шкафу, а ночью, когда универститет будет пуст, начать вечеринку..."
    "...И вот часы пробили полночь..."
    jump shkaf_transition

label shkaf_transition:
    scene bg cabinet_with_beer
    show i normal at Position(xpos=0.1, ypos=1.0)
    show a normal at Position(xpos=0.2, ypos=1.0)
    show d normal at Position(xpos=0.3, ypos=1.0)
    show k normal at Position(xpos=0.4, ypos=1.0)
    d "Ну, парни, хряпнем!"
    i "Хряпнем!"
    a "Хряпнем!"
    k "Хряпнем!"
    show expression Solid("#0008") as shkaf_darken onlayer master
    show empty_chest:
        xalign 0.5
        yalign 0.5
        zoom 0.7
        yoffset -100
    with dissolve
    $ renpy.pause()
    i "Не понял юмора..."
    a "Приехали..."
    hide empty_chest with dissolve
    hide shkaf_darken
    i "Этот шкаф лет сто никто не открывал, как так вышло?!"
    d "Так не бывает, тут какие-то тюбики явно постарались!"
    k "Может, беский?"
    d "Может и он..."
    a "Эй, тут какая-то записка, кажется, с русскими буквами."
    show expression Solid("#0008") as shkaf_darken onlayer master
    show letter:
        xalign 0.5
        yalign 0.5
        zoom 0.7
        yoffset -100
    with dissolve
    $ renpy.pause()
    a "Прочтите кто-нибудь!"
    $ renpy.pause()
    hide letter with dissolve
    hide shkaf_darken
    k "У нас в Саратове за такие приколы ебучку сносят!"
    i "Кто бы это ни был, мы до него доберемся!"
    jump pre_base_room

label pre_base_room:
    scene bg corridor
    show i normal at Position(xpos=0.1, ypos=1.0) with dissolve
    show a normal at Position(xpos=0.3, ypos=1.0) with dissolve
    show d normal at Position(xpos=0.6, ypos=1.0) with dissolve
    show k normal at Position(xpos=0.9, ypos=1.0) with dissolve
    a "Давайте быстрее найдем этого *****, а то пиво стынет!"
    k "Как хорошо, что мы сделали приложение с картой ГЗ, и можно спокойно ориентироваться по этажу!"
    i "Пойдем?"
    $ ui_unlocked = True
    d "Куда?" (advance=False)

label base_room:
    scene bg corridor
    show i normal at Position(xpos=0.1, ypos=1.0) 
    show a normal at Position(xpos=0.3, ypos=1.0) 
    show d normal at Position(xpos=0.6, ypos=1.0) 
    show k normal at Position(xpos=0.9, ypos=1.0) 
    $ ui_unlocked = True
    $ ensure_cabinet_scene_map()
    $ random_speaker = renpy.random.choice([i, a, d, k])
    $ renpy.say(random_speaker, "Ладно парни идем дальше", advance=False)

# label scene_reset:
#     hide i normal
#     hide a normal
#     hide d normal
#     hide k normal
#     return

label finish_cabinet_scene:
    if current_cabinet and current_cabinet not in visited_cabinets:
        $ visited_cabinets.append(current_cabinet)

    $ room_exit_counter += 1
    jump base_room

# История Лычкова (поздравляет с успешной защитой)
label story_scene_1:
    $ ui_unlocked = False
    scene expression Transform("images/doska.jpg", size=(1920, 1080))
    show lichkov normal at Position(xpos=0.84, ypos=1.0)
    p1 "Я все еще не верю, что мы действительно дошли до этого дня."
    p1 "Раз уж мы у доски, давай быстро проверим базу."
    p1 "Соедини каждый пример с правильным ответом."
    $ reset_story_scene_1_match_game()
    call screen story_scene_1_match_game
    if story_scene_1_match_success:
        p1 "Все верно. Значит, не зря мы столько лет сидели в этих аудиториях."
    else:
        p1 "Нет, так не пойдет. Тут не все совпало правильно."
    jump finish_cabinet_scene

# История Недаша (отмечает 200 летие)
label story_scene_2:
    $ ui_unlocked = False
    scene bg room
    show nedash elder
    p2 "Если честно, я зашел сюда просто перевести дух."
    $ found_story_scene_2_item = False
    $ failed_story_scene_2_search = False
    call screen story_scene_2_search
    if found_story_scene_2_item:
        p2 "Нашел. Значит, здесь действительно кто-то был до нас."
    elif failed_story_scene_2_search:
        p2 "Не нашли... Значит, я либо ошибся, либо мы упустили что-то важное."
    p2 "Но теперь уже хочется понять, кто еще бродит по этому этажу."
    jump finish_cabinet_scene

# История Семенцова (чинит проводку)
label story_scene_3:
    $ ui_unlocked = False
    scene bg room
    show semens cyborg
    p3 "Тишина в корпусе какая-то слишком подозрительная."
    p3 "Такое чувство, будто здание ждет, когда мы сделаем следующий шаг."
    jump finish_cabinet_scene

# История Брызгалова (качается)
label story_scene_4:
    $ ui_unlocked = False
    scene bg room
    show brizg normal
    p4 "Я бы не называл это обычной прогулкой после защиты."
    p4 "У этого вечера явно есть свой сценарий."
    p4 "Раз уж зашли так далеко, покажи, как умеешь приседать."
    p4 "У тебя 30 секунд и 30 повторений. S - вниз, W - вверх."
    $ reset_story_scene_4_minigame()
    hide brizg normal
    call screen story_scene_4_minigame
    show brizg normal
    if story_scene_4_minigame_won:
        p4 "Вот это темп. Сразу видно: к ночному забегу по Бауманке ты готов."
    else:
        p4 "Не хватило совсем чуть-чуть. После такой защиты простительно."
    jump finish_cabinet_scene

# История Адамовой (желает доминировать)
label story_scene_5:
    $ ui_unlocked = False
    scene bg room
    show adamova normal
    p5 "Я оставила в одном из кабинетов записку, но уже не помню в каком."
    p5 "Если найдешь ее, не читай вслух, договорились?"
    jump finish_cabinet_scene

# История Бабкина (не может стереть с доски "бабкин пидарас")
label story_scene_6:
    $ ui_unlocked = False
    scene bg room
    show babkin normal
    p6 "На этом этаже слишком хорошо слышны шаги."
    p6 "Иногда кажется, что за нами кто-то идет на полсекунды позже."
    jump finish_cabinet_scene

# История Левиева (хочет кушать)
label story_scene_7:
    $ ui_unlocked = False
    scene bg room
    show leviev normal
    p7 "Я всегда думала, что ночью универ выглядит романтичнее."
    p7 "Оказалось, ночью он выглядит так, будто знает о нас лишнее."
    jump finish_cabinet_scene

# История Бянкина (синетзирует элемент)
label story_scene_8:
    $ ui_unlocked = False
    scene bg room
    show byankin normal
    p8 "Если открыть все кабинеты подряд, мы точно соберем полную картину."
    p8 "Главное, чтобы картина потом не собрала нас."
    show byankin happy
    p8 "Хотя, с другой стороны, если мы уже здесь, то может быть"
    jump finish_cabinet_scene

# История Тихомировой (нашла куртку на кафедре)
label story_scene_9:
    $ ui_unlocked = False
    scene bg room
    show tishka normal:
        zoom 0.9
        xalign 0.5
        yalign 0.5
    p9 "Я запомнила этот коридор еще с первого курса."
    p9 "Только тогда он казался бесконечным, а сейчас замкнутым."
    jump finish_cabinet_scene

# История Кадырбаевой (хочет написать фанфик)
label story_scene_10:
    $ ui_unlocked = False
    scene bg room
    show kadira normal
    p10 "Хочешь совет? Не заходи в кабинет, если тебе уже не по себе."
    p10 "Обычно интуиция ошибается реже, чем расписание."
    jump finish_cabinet_scene

# История Выхованца (хочет чтобы проверили гост)
label story_scene_11:
    $ ui_unlocked = False
    scene bg room
    p11 "Я думала, что после защиты станет легче."
    p11 "Но кажется, самое важное начинается только сейчас."
    jump finish_cabinet_scene

# История Фёдорова (хз)
label story_scene_12:
    $ ui_unlocked = False
    scene bg room
    p12 "В этом месте слишком много совпадений, чтобы считать их случайностью."
    p12 "Если мы дошли сюда вместе, значит, назад дороги уже не будет."
    jump finish_cabinet_scene

