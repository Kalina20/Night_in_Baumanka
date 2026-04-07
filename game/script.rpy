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

default bottle_counter = 0
default visited_cabinets = []
default ui_unlocked = False
default cabinet_scene_map = {}
default current_cabinet = None
default success_flag = False
default found_story_scene_2_item = False
default failed_story_scene_2_search = False
default story_scene_1_match_selected_left = None
default story_scene_1_match_selected_right = None
default story_scene_1_match_done = []
default story_scene_1_match_success = False
default story_scene_1_match_failed = False
default story_scene_8_chain_assignments = {}
default story_scene_8_chain_item_positions = {}
default story_scene_8_chain_failed = False
default story_scene_8_chain_success = False
default story_scene_8_chain_checked = False
default story_scene_8_formula_items = []
default story_scene_8_formula_player_x = 360
default story_scene_8_formula_score = 0
default story_scene_8_formula_mistakes = 0
default story_scene_8_formula_won = False
default story_scene_8_formula_lost = False
default story_scene_8_formula_ticks = 0
default story_scene_10_choice = None
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

    def story_scene_8_chain_start_positions():
        return {
            "lamp": (30, 360),
            "resistor": (215, 360),
            "source": (400, 360),
            "wire": (585, 360),
        }

    def story_scene_8_chain_item_label(item_id):
        labels = {
            "source": "источник",
            "wire": "провод",
            "resistor": "резистор",
            "lamp": "лампа",
        }
        return labels[item_id]

    def story_scene_8_chain_item_image(item_id):
        image_variants = {
            "source": ["images/source.png", "images/source.jpg", "images/battery.png", "images/battery.jpg"],
            "wire": ["images/wire.png", "images/wire.jpg"],
            "resistor": ["images/resistor.jpg", "images/resistor.png"],
            "lamp": ["images/lamp.png", "images/lamp.jpg"],
        }

        for image_path in image_variants[item_id]:
            if renpy.loadable(image_path):
                return image_path

        return None

    def story_scene_8_chain_slot_positions():
        return {
            "slot_0": (30, 120),
            "slot_1": (215, 120),
            "slot_2": (400, 120),
            "slot_3": (585, 120),
        }

    def reset_story_scene_8_chain_game():
        store.story_scene_8_chain_assignments = {
            "slot_0": None,
            "slot_1": None,
            "slot_2": None,
            "slot_3": None,
        }
        store.story_scene_8_chain_item_positions = story_scene_8_chain_start_positions()
        store.story_scene_8_chain_failed = False
        store.story_scene_8_chain_success = False
        store.story_scene_8_chain_checked = False

    def story_scene_8_chain_dragged(drags, drop):
        drag = drags[0]
        item_id = drag.drag_name
        assignments = store.story_scene_8_chain_assignments
        start_positions = story_scene_8_chain_start_positions()
        slot_positions = story_scene_8_chain_slot_positions()
        previous_slot = None

        if store.story_scene_8_chain_failed or store.story_scene_8_chain_success:
            return

        store.story_scene_8_chain_checked = False

        for slot_id, assigned_item in assignments.items():
            if assigned_item == item_id:
                previous_slot = slot_id
                assignments[slot_id] = None
                break

        if drop is None or drop.drag_name not in slot_positions:
            if previous_slot:
                store.story_scene_8_chain_assignments[previous_slot] = item_id
                store.story_scene_8_chain_item_positions[item_id] = slot_positions[previous_slot]
            else:
                store.story_scene_8_chain_item_positions[item_id] = start_positions[item_id]
            renpy.restart_interaction()
            return

        slot_id = drop.drag_name
        replaced_item = assignments.get(slot_id)

        if replaced_item and replaced_item != item_id:
            store.story_scene_8_chain_item_positions[replaced_item] = start_positions[replaced_item]

        assignments[slot_id] = item_id
        store.story_scene_8_chain_item_positions[item_id] = slot_positions[slot_id]

        renpy.restart_interaction()
        return

    def story_scene_8_check_chain():
        assignments = store.story_scene_8_chain_assignments
        correct_order = ["source", "wire", "resistor", "lamp"]

        if not all(assignments.values()):
            renpy.notify("Сначала расставь все элементы по местам.")
            return

        store.story_scene_8_chain_checked = True
        store.story_scene_8_chain_success = all(
            assignments["slot_%d" % index] == correct_order[index]
            for index in range(4)
        )
        store.story_scene_8_chain_failed = not store.story_scene_8_chain_success
        renpy.restart_interaction()

    def reset_story_scene_8_formula_game():
        store.story_scene_8_formula_items = []
        store.story_scene_8_formula_player_x = 760
        store.story_scene_8_formula_score = 0
        store.story_scene_8_formula_mistakes = 0
        store.story_scene_8_formula_won = False
        store.story_scene_8_formula_lost = False
        store.story_scene_8_formula_ticks = 0

    def story_scene_8_formula_move_left():
        if store.story_scene_8_formula_won or store.story_scene_8_formula_lost:
            return
        store.story_scene_8_formula_player_x = max(20, store.story_scene_8_formula_player_x - 120)
        renpy.restart_interaction()

    def story_scene_8_formula_move_right():
        if store.story_scene_8_formula_won or store.story_scene_8_formula_lost:
            return
        store.story_scene_8_formula_player_x = min(1460, store.story_scene_8_formula_player_x + 120)
        renpy.restart_interaction()

    def story_scene_8_formula_spawn():
        pool = [
            {"text": "F = ma", "correct": True},
            {"text": "U = IR", "correct": True},
            {"text": "E = mc^2", "correct": True},
            {"text": "P = UI", "correct": True},
            {"text": "p = mv", "correct": True},
            {"text": "A = Fs", "correct": True},
            {"text": "Q = I^2Rt", "correct": True},
            {"text": "F = mЯу", "correct": False},
            {"text": "U = картошка", "correct": False},
            {"text": "a = pain", "correct": False},
            {"text": "p = печенька", "correct": False},
            {"text": "E = anime", "correct": False},
            {"text": "I = nya", "correct": False},
            {"text": "R = рулет", "correct": False},
            {"text": "P = пельмени", "correct": False},
        ]
        item = renpy.random.choice(pool).copy()
        item["x"] = renpy.random.randint(20, 1460)
        item["y"] = 0
        store.story_scene_8_formula_items.append(item)

    def story_scene_8_formula_tick():
        if store.story_scene_8_formula_won or store.story_scene_8_formula_lost:
            return

        store.story_scene_8_formula_ticks += 1

        if store.story_scene_8_formula_ticks % 5 == 1:
            story_scene_8_formula_spawn()

        updated_items = []

        for item in store.story_scene_8_formula_items:
            item["y"] += 25

            caught = item["y"] >= 640 and abs(item["x"] - store.story_scene_8_formula_player_x) <= 120
            missed = item["y"] > 760

            if caught:
                if item["correct"]:
                    store.story_scene_8_formula_score += 1
                else:
                    store.story_scene_8_formula_mistakes += 1
                continue

            if missed:
                if item["correct"]:
                    store.story_scene_8_formula_mistakes += 1
                continue

            updated_items.append(item)

        store.story_scene_8_formula_items = updated_items

        if store.story_scene_8_formula_score >= 5:
            store.story_scene_8_formula_won = True
        elif store.story_scene_8_formula_mistakes >= 3:
            store.story_scene_8_formula_lost = True

        renpy.restart_interaction()

    def reset_story_scene_10_choice_game():
        store.story_scene_10_choice = None

    def story_scene_10_pick_choice(choice_id):
        store.story_scene_10_choice = choice_id
        renpy.restart_interaction()

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
            "images/or.jpg": "ИЛИ",
            "images/xor.jpg": "XOR",
            "images/imp.jpg": "->",
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
    play music "audio/Minecraft 1.mp3"
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
    "Но теперь им предстояло отпраздновать это знаменательное событие...и отпраздновать с огоньком, а, вернее сказать, 
    с ящиком {color=#f0fc05}Corona Extra{/color}..."
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
    play music "coridor.mp3"
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
    play music "coridor.mp3"
    show i normal at Position(xpos=0.1, ypos=1.0) 
    show a normal at Position(xpos=0.3, ypos=1.0) 
    show d normal at Position(xpos=0.6, ypos=1.0) 
    show k normal at Position(xpos=0.9, ypos=1.0) 
    $ ui_unlocked = True
    $ ensure_cabinet_scene_map()
    $ random_speaker = renpy.random.choice([i, a, d, k])
    $ renpy.say(random_speaker, "Ладно парни идем дальше!", advance=False)

# label scene_reset:
#     hide i normal
#     hide a normal
#     hide d normal
#     hide k normal
#     return

label show_beer(count):    
    python:
        positions = [(0.47, 0.55), (0.53, 0.55), (0.41, 0.55), (0.59, 0.55)]
        beer_count = min(count, len(positions))

        for index in range(beer_count + 1):
            if index == 0:
                renpy.show("bubble", at_list=[Transform(xalign=0.5, yalign=0.6, xzoom=0.45, yzoom=0.6)], tag="bubble_i")
            else:
                xpos, ypos = positions[index-1]
                renpy.show(
                    "beer",
                    at_list=[Transform(xalign=xpos, yalign=ypos, zoom=0.15)],
                    tag="beer_%d" % index,
                )
        renpy.with_statement(Dissolve(2.0))
    return

label finish_cabinet_scene:
    if current_cabinet and current_cabinet not in visited_cabinets:
        $ visited_cabinets.append(current_cabinet)
    if success_flag:
        $ bottle_counter += 2
    $ success_flag = False
    jump base_room

# История Лычкова (поздравляет с успешной защитой)
label story_scene_1:
    $ ui_unlocked = False
    scene expression Transform("images/doska.jpg", size=(1920, 1080))
    play music "Smeshariki_-_Meteority_OST_Kosmicheskaya_odisseya_(SkySound.cc).mp3"
    show lichkov normal at Position(xpos=0.84, ypos=1.0)
    p1 "Я все еще не верю, что мы действительно дошли до этого дня."
    p1 "Раз уж мы у доски, давай быстро проверим базу."
    p1 "Соедини каждый пример с правильным ответом."
    $ reset_story_scene_1_match_game()
    call screen story_scene_1_match_game
    if story_scene_1_match_success:
        p1 "Все верно. Значит, не зря мы столько лет сидели в этих аудиториях."
        $ success_flag = True
        call show_beer(2)
    else:
        p1 "Нет, так не пойдет. Тут не все совпало правильно."
    jump finish_cabinet_scene

# История Недаша (найти предмет)
label story_scene_2:
    $ ui_unlocked = False
    scene bg room
    play music "nedash_smeshariki.mp3"
    show i normal at Position(xpos=0.1, ypos=1.0)
    show a normal at Position(xpos=0.3, ypos=1.0)
    show d normal at Position(xpos=0.7, ypos=1.0)
    show k normal at Position(xpos=0.9, ypos=1.0)
    $ renpy.pause(1.0, hard=True)
    show nedash elder with Dissolve(2.0)
    $ renpy.pause(1.0, hard=True)
    p2 "Приветсвую вас, о юные дарования!"
    a "Вячеслав Михайлович?!"
    p2 "А кто же еще, ахахахахха! Поздравляю вас с успешной защитой, хвала фильтру Баттерворта! Вы действительно заслужили отдых."
    p2 "Должен сказать, я наслышан о вашей затее, но мне нужна ваша помощь. Понимаете, годы уже не те,
    и зрение мое меня подводит."
    p2 "Помогите мне отыскать запоминающее устройство с НИРСами студентов, и я укажу вам путь к жидкому золоту."
    $ found_story_scene_2_item = False
    $ failed_story_scene_2_search = False
    call screen story_scene_2_search
    if found_story_scene_2_item:
        p2 "Вот это я понимаю студенты! Сразу видно, что вы за киллометр можете углядеть самое правильное управленческое решение!"
        p2 "Что ж, значит защиты НИРСов пройдут по расписанию,
        а вы, ребятки, можете наслаждаться вечером. Держите!"
        call show_beer(2)
        d "Вам спасибо, Вячеслав Михайлович!"
        $ success_flag = True
    elif failed_story_scene_2_search:
        p2 "Не нашли... опять на кафедре будут ругаться. Ну, ребятки, что-то в сон меня потянуло, а вы идите,
        может, поможете кому-то помоложе."
    jump finish_cabinet_scene

# История Семенцова (чинит проводку)
label story_scene_3:
    $ ui_unlocked = False
    scene bg room
    play music "semens.mp3"
    show semens cyborg at Position(xpos=0.18, ypos=1.0)
    p3 "Тишина в корпусе какая-то слишком подозрительная."
    p3 "Такое чувство, будто здание ждет, когда мы сделаем следующий шаг."
    p3 "Ладно, тогда совсем простой вопрос."
    call screen story_scene_3_resistor_game
    p3 "Да, это резистор. Значит, базу ты еще помнишь."
    call show_beer(2)
    jump finish_cabinet_scene

# История Брызгалова (приседания)
label story_scene_4:    
    $ ui_unlocked = False
    scene bg room
    play music "brizg_smeshariki.mp3"
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
        p4 "Ой, чуть не забыл про подарочек...Вот, держите, и помните - 
        в алкоголе всегда нужно знать меру, иначе можно выпить меньше!"
        call show_beer(2)
        $ success_flag = True
    else:
        p4 "Не хватило совсем чуть-чуть. После такой защиты простительно, но в качестве домашнего задания
        даю вам 100 км на велосипеде по измайловскому парку!"
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
    p8 "Хотя, с другой стороны, если мы уже здесь, то давай проверим, кто из нас еще помнит физику."
    p8 "Лови только правильные формулы и не трогай всякий бред."
    $ reset_story_scene_8_formula_game()
    hide byankin happy
    call screen story_scene_8_formula_game
    show byankin happy
    if story_scene_8_formula_won:
        p8 "Вот это уже разговор. Формулы летят, а ты даже не моргнул."
    else:
        p8 "Нет, физика так не делается. Картошку в закон Ома мы пока не подставляем."
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
    p10 "Ладно, тогда выбери одну картинку."
    $ reset_story_scene_10_choice_game()
    call screen story_scene_10_choice_game
    p10 "Значит, ты выбрал вариант [story_scene_10_choice]. Запомню."
    jump finish_cabinet_scene

# История Выхованца (хочет чтобы проверили гост)
label story_scene_11:
    $ ui_unlocked = False
    scene bg room
    p11 "Я думала, что после защиты станет легче."
    p11 "Но кажется, самое важное начинается только сейчас."
    p11 "Для начала попробуем собрать хотя бы простую цепь."
    $ reset_story_scene_8_chain_game()
    call screen story_scene_8_chain_game
    if story_scene_8_chain_success:
        p11 "Да. Когда все стоит на своих местах, становится спокойнее."
    else:
        p11 "Нет, здесь пока нет нужного порядка."
    jump finish_cabinet_scene

# История Фёдорова (хз)
label story_scene_12:
    $ ui_unlocked = False
    scene bg room
    p12 "В этом месте слишком много совпадений, чтобы считать их случайностью."
    p12 "Если мы дошли сюда вместе, значит, назад дороги уже не будет."
    p12 "На столе что-то лежит. Нажми на записку."
    call screen story_scene_12_note
    call screen story_scene_12_note_text
    p12 "Значит, и правда кто-то оставил нам подсказку."
    jump finish_cabinet_scene

screen story_scene_8_formula_game():
    modal True
    zorder 1200

    if story_scene_8_formula_won or story_scene_8_formula_lost:
        timer 0.01 action Return()
    else:
        timer 0.35 repeat True action Function(story_scene_8_formula_tick)

    key "K_LEFT" action Function(story_scene_8_formula_move_left)
    key "K_RIGHT" action Function(story_scene_8_formula_move_right)
    key "a" action Function(story_scene_8_formula_move_left)
    key "d" action Function(story_scene_8_formula_move_right)

    add Solid("#10141cee")

    frame:
        xpos 0
        ypos 0
        xsize 1920
        ysize 1080
        background None
        padding (40, 30)

        text "Мини-игра: Поймай формулу":
            xalign 0.5
            ypos 10
            size 38
            color "#ffffff"
            outlines [(2, "#000000", 0, 0)]

        text "Лови только правильные формулы. Управление: A/D или стрелки.":
            xalign 0.5
            ypos 60
            size 24
            color "#dddddd"

        hbox:
            xpos 620
            ypos 105
            spacing 80

            text "Поймано: [story_scene_8_formula_score] / 5":
                size 28
                color "#7dff7d"

            text "Ошибки: [story_scene_8_formula_mistakes] / 3":
                size 28
                color "#ff8c8c"

        fixed:
            xpos 120
            ypos 170
            xsize 1680
            ysize 760

            add Solid("#1b2330")

            for item in story_scene_8_formula_items:
                frame:
                    xpos item["x"]
                    ypos item["y"]
                    xsize 160
                    ysize 56
                    background Solid("#3d6ec9dd")

                    text item["text"]:
                        align (0.5, 0.5)
                        size 24
                        color "#ffffff"
                        text_align 0.5

            frame:
                xpos story_scene_8_formula_player_x
                ypos 610
                xsize 240
                ysize 140
                background None

                add Transform("images/Alexey/alex bag.JPG", fit="contain", xsize=240, ysize=140, rotate=90):
                    align (0.5, 0.5)

screen story_scene_4_minigame():
    modal True
    zorder 1200

    $ state_text = "Положение: вниз" if story_scene_4_is_down else "Положение: вверх"
    $ state_color = "#6ec1ff" if story_scene_4_is_down else "#ffffff"
    $ down_bg = "#2b5cffaa" if story_scene_4_is_down else "#1d1d1daa"
    $ up_bg = "#2fa34aaa" if not story_scene_4_is_down else "#1d1d1daa"
    $ pose_image = "images/Ivan/van brizg 1.JPG" if story_scene_4_is_down else "images/Ivan/van brizg 2.JPG"

    if story_scene_4_minigame_won or story_scene_4_minigame_lost:
        timer 0.01 action Return()
    else:
        timer 1.0 repeat True action Function(story_scene_4_tick)

    key "K_s" action Function(story_scene_4_press_down)
    key "K_w" action Function(story_scene_4_press_up)
    key "s" action Function(story_scene_4_press_down)
    key "w" action Function(story_scene_4_press_up)

    add Transform(pose_image, fit="contain", xsize=700, ysize=980, rotate=90):
        xalign 0.24
        yalign 0.5

    frame:
        xpos 1130
        ypos 260
        xsize 760
        ysize 560
        background Solid("#111a")
        padding (34, 30)

        vbox:
            spacing 18
            xfill True

            text "":
                xalign 0.5
                size 36
                color "#ffffff"
                outlines [(2, "#000000", 0, 0)]

            text "Нажимай S, чтобы присесть, и W, чтобы встать. Нужно сделать 30 повторений за 30 секунд.":
                xalign 0.5
                text_align 0.5
                size 24
                color "#f0f0f0"

            hbox:
                spacing 55
                xalign 0.5

                vbox:
                    spacing 10
                    text "Осталось времени":
                        size 24
                        color "#cccccc"
                    text "[story_scene_4_time_left] сек":
                        size 38
                        color "#ffd54a"

                vbox:
                    spacing 10
                    text "Сделано приседаний":
                        size 24
                        color "#cccccc"
                    text "[story_scene_4_squats] / 30":
                        size 38
                        color "#7dff7d"

            bar value StaticValue(story_scene_4_squats, 30):
                xalign 0.5
                xmaximum 620
                ymaximum 28

            frame:
                xalign 0.5
                xsize 340
                ysize 100
                background Solid("#ffffff10")

                text state_text:
                    align (0.5, 0.5)
                    size 32
                    color state_color

            hbox:
                spacing 26
                xalign 0.5

                frame:
                    xsize 150
                    ysize 76
                    background Solid(down_bg)

                    text "S\nвниз":
                        align (0.5, 0.5)
                        text_align 0.5
                        size 28
                        color "#ffffff"

                frame:
                    xsize 150
                    ysize 76
                    background Solid(up_bg)

                    text "W\nвверх":
                        align (0.5, 0.5)
                        text_align 0.5
                        size 28
                        color "#ffffff"

