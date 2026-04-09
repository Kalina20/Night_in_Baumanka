define e = Character('Все', color="#c300ff")
define ee = Character('Все (кроме Вани)', color="#c300ff")
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
define pq = Character("???", color="#dddddd")

default bottle_counter = 0
default bottle_plus = 2
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

define credits_entries = [
    {
        "title": "Night in Baumanka",
        "subtitle": "Визуальная новелла",
        "text": "Спасибо вам за прохождение!",
        "image": "images/IMG_7369.JPG",
    },
    {
        "title": "Команда",
        "subtitle": "Два придурка",
        "text": "Сценарист: Калиниченко Алексей и Писарев Иван\nПрограммист: Писарев Иван и Алексей Калиниченко\nХудожник: Калиниченко Алексей и Писарев Иван\nГейдизайнер: Писарев Иван и Алексей Калиниченко",
        "image": "images/IMG_7632.JPG",
    },
    {
        "title": "Особые благодарности",
        "subtitle": "Двум придуркам",
        "text": "Перекосов Даниил и Горшков Константин",
        "image": "images/IMG_8454 (2).JPG",
    },
]

init python:
    def credits_entry_image(entry):
        image_path = entry.get("image")
        if image_path and renpy.loadable(image_path):
            return image_path
        return None

    def ensure_cabinet_scene_map():
        if cabinet_scene_map:
            return

        cabinets = ["420", "421", "422", "423", "424", "425", "426", "427", "428", "429", "430"]
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
        ]
        renpy.random.shuffle(scene_labels)
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
            {"text": "A = FS", "correct": True},
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
    scene black
    show text "Основано на реальных событиях" at truecenter
    with dissolve
    pause 2.0
    hide text
    with dissolve
    jump vvedenie

label vvedenie:
    scene bg room
    play music "audio/Minecraft 1.mp3"
    "Эта история началась много лет назад..."
    "Несколько влиятельных людей по счастливой случайности оказались в одном университете, и даже в одной группе..."
    "Они были настолько разными, что даже не могли представить, что у них может быть что-то общее..."
    show ivan normal at Position(xpos=0.1, ypos=1.0) with dissolve
    "Анимешник..."
    show alexey normal at Position(xpos=0.3, ypos=1.0) with dissolve
    "Футболист..."
    show daniil normal at Position(xpos=0.6, ypos=1.0) with dissolve
    "Нефор..."
    show kostik normal at Position(xpos=0.9, ypos=1.0) with dissolve
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
    scene expression Transform("images/rooms/kaf.JPG", size=(1920, 1080))
    play music "lil_krystalll_-_Air_Force_(SkySound.cc).mp3"
    show i laugh at Position(xpos=0.12, ypos=1.0)
    show a happy at Position(xpos=0.35, ypos=1.0)
    show d happy at Position(xpos=0.6, ypos=1.0)
    show k laugh at Position(xpos=0.85, ypos=1.0)
    d "Ну, парни, хряпнем!?"
    i "Хряпнем!"
    a "Хряпнем!"
    k "Хряпнем!"
    $ renpy.pause(1.0, hard=True)
    show expression Solid("#0008") as shkaf_darken onlayer master
    show empty_chest:
        xalign 0.5
        yalign 0.5
        zoom 0.7
        yoffset -100
    with dissolve
    $ renpy.pause()
    show i surprise at Position(xpos=0.1, ypos=1.0)
    show a surprise at Position(xpos=0.2, ypos=1.0)
    show d surprise at Position(xpos=0.8, ypos=1.0)
    show k surprise at Position(xpos=0.9, ypos=1.0)
    stop music fadeout 1.0
    i "Не понял юмора..."
    a "Приехали..."
    play music "DJ_FON_Muzyka_dlya_fona_-_Grustnaya_muzyka_bez_slov_dlya_fona_(SkySound.cc).mp3"
    hide empty_chest with dissolve
    hide shkaf_darken
    show i angry at Position(xpos=0.12, ypos=1.0)
    show a surprise at Position(xpos=0.35, ypos=1.0)
    show d angry at Position(xpos=0.6, ypos=1.0)
    show k sad at Position(xpos=0.85, ypos=1.0)
    i "Этот шкаф лет сто никто не открывал, как так вышло?!"
    d "Так не бывает, тут какие-то тюбики явно постарались!"
    show i sad 
    show k think
    k "Может, беский?"
    show d think
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
    show k angry
    show d angry
    k "У нас в Саратове за такие приколы ебучку сносят!"
    show i angry
    i "Кто бы это ни был, мы до него доберемся!"
    jump pre_base_room

label pre_base_room:
    scene expression Transform("images/rooms/koridor.JPG", size=(1920, 1080))
    play music "coridor.mp3"
    show i normal at Position(xpos=0.12, ypos=1.0) with dissolve
    show a angry at Position(xpos=0.35, ypos=1.0) with dissolve
    show d normal at Position(xpos=0.6, ypos=1.0) with dissolve
    show k angry at Position(xpos=0.85, ypos=1.0) with dissolve
    a "Давайте быстрее найдем этого *****, а то пиво стынет!"
    d "Как хорошо, что мы сделали приложение с картой ГЗ, и можно спокойно ориентироваться по этажу!"
    i "Пойдем?"
    show d map 2
    $ ui_unlocked = True
    d "Куда?" (advance=False)

label base_room:
    scene expression Transform("images/rooms/koridor.JPG", size=(1920, 1080))
    play music "coridor.mp3"
    show i normal at Position(xpos=0.12, ypos=1.0) 
    show a normal at Position(xpos=0.35, ypos=1.0) 
    show d map 2 at Position(xpos=0.6, ypos=1.0) 
    show k normal at Position(xpos=0.85, ypos=1.0) 
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

label show_beer(count, offset = 0.0):    
    python:
        positions = [(0.47 + offset, 0.55), (0.53 + offset, 0.55), 
        (0.41 + offset, 0.55), (0.59 + offset, 0.55)]
        beer_count = min(count, len(positions))

        for index in range(beer_count + 1):
            if index == 0:
                renpy.show("bubble", at_list=[Transform(xalign=0.5 + offset + offset/2, yalign=0.6, xzoom=0.45, yzoom=0.6)], tag="bubble_i")
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
        $ bottle_counter += bottle_plus
        $ bottle_plus = 2
    $ success_flag = False
    if len(visited_cabinets) == 11:
        jump final
    else:
        # ИСПРАААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААВИТЬ
        jump base_room

# История Лычкова (ГОТОВО)
label story_scene_1:
    $ ui_unlocked = False
    scene expression Transform("images/rooms/Igor_igorevic.JPG", size=(1920, 1080))
    play music "Smeshariki_-_Meteority_OST_Kosmicheskaya_odisseya_(SkySound.cc).mp3"
    show i normal at Position(xpos=0.1, ypos=1.0)    
    show d normal at Position(xpos=0.3, ypos=1.0)
    show k normal at Position(xpos=0.2, ypos=1.0)
    show a normal at Position(xpos=0.4, ypos=1.0)
    $ renpy.pause(1.0, hard=True)
    show lichkov normal at Position(xpos=0.84, ypos=1.0)
    p1 "Ой, добрый день, ребята, как я рад вас видеть!"
    show i happy    
    show d happy 
    show k happy
    show a happy 
    k "(щепотом) Сейчас же час ночи, ну ладно..."
    e "Добрый день, Игорь Игоревич!"
    p1 "Еще раз поздравляю с успешной защитой!"
    p1 "Знаете, когда я шел в кабинет, я встретил очень умного человека, который передал мне ваши напитки."
    show a surprise
    a "Кто это был, Игорь Игоревич?!"
    p1 "К сожалению, не могу вам сказать :("
    p1 "И напитки, к сожалению, просто так я вам отдать не могу. Нужно провести защиту лабораторной работы!"
    show i sad    
    show d sad 
    show k sad
    show a sad 
    d "Только не самый сложный предмет на кафедре..."
    p1 "Для защиты вам нужно выполнить небольшое теоретическое задание!"
    p1 "Кто пойдет отвечать?"
    show i normal    
    show d normal 
    show k normal
    show a normal 
    a "На цу е фа, парни?"
    show d angry
    d "Нет я не пойду идите *****"
    show d mad
    show k laugh
    k "Игорь Игоревич, будет отвечать Даниил Перекосов!"
    p1 "Ну что, Даниил, приступим?)"
    $ reset_story_scene_1_match_game()
    hide i 
    hide a 
    hide k 
    show d mad at Position(xpos=0.19, ypos=1.0)
    call screen story_scene_1_match_game
    if story_scene_1_match_success:
        show d laugh
        p1 "Даниил, вы большой молодец! Очень рад, что мои студенты не забыли мой курс!"
        p1 "Держите вашу награду, ребята! Отличного отдыха!"
        e "Спасибо, Игорь Игоревич, всего доброго!"
        $ success_flag = True
        call show_beer(2)
        $ renpy.pause()
    else:
        show d sad
        p1 "Даниил, к сожалению, не большой одной попытки в день("
        d "Игорь Игоревич, может, есть задание по прологу?"
        p1 "Конечно есть, но уже в следующий раз."
        d "До свидания, Игорь Игоревич..."
        p1 "Хорошего дня!"
    jump finish_cabinet_scene

# История Недаша (ГОТОВО)
label story_scene_2:
    $ ui_unlocked = False
    scene expression Transform("images/rooms/nedish.JPG", size=(1920, 1080))
    play music "nedash_smeshariki.mp3"
    show i normal at Position(xpos=0.10, ypos=1.0)
    show a normal at Position(xpos=0.3, ypos=1.0)
    show d normal at Position(xpos=0.7, ypos=1.0)
    show k normal at Position(xpos=0.9, ypos=1.0)
    $ renpy.pause(1.0, hard=True)
    show nedash elder with Dissolve(2.0)
    $ renpy.pause(1.0, hard=True)
    p2 "Приветсвую вас, о юные дарования!"
    show i surprise    
    show d surprise 
    show k surprise
    show a surprise 
    a "Вячеслав Михайлович?!"
    p2 "А кто же еще, ахахахахха! Поздравляю вас с успешной защитой, хвала фильтру Баттерворта! Вы действительно заслужили отдых."
    p2 "Должен сказать, я наслышан о вашей затее, но мне нужна ваша помощь. Понимаете, годы уже не те,
    и зрение мое меня подводит."
    show i normal    
    show d normal 
    show k normal
    show a normal 
    i "Как мы можем вам помочь?"
    p2 "Помогите мне отыскать запоминающее устройство с НИРСами студентов, и я укажу вам путь к жидкому золоту."
    $ found_story_scene_2_item = False
    $ failed_story_scene_2_search = False
    call screen story_scene_2_search
    if found_story_scene_2_item:
        show i happy    
        show d happy 
        show k happy
        show a happy 
        p2 "Вот это я понимаю студенты! Сразу видно, что вы за киллометр можете углядеть самое правильное управленческое решение!"
        p2 "Что ж, значит защиты НИРСов пройдут по расписанию,
        а вы, ребятки, можете наслаждаться вечером. Держите!"
        call show_beer(2)
        d "Вам спасибо, Вячеслав Михайлович!"
        $ success_flag = True
        $ renpy.pause()
    elif failed_story_scene_2_search:
        show i sad    
        show d sad 
        show k sad
        show a sad 
        p2 "Не нашли... опять на кафедре будут ругаться. Ну, ребятки, что-то в сон меня потянуло, 
        а ваши напитки помогут мне лучше заснуть. А вы идите,
        может, поможете кому-то помоложе."
        d "Я тоже частенько пользуюсь этим снотворным!"
        p2 "Какой молодец!"
        
    jump finish_cabinet_scene

# История Семенцова (ГОТОВО)
label story_scene_3:
    $ ui_unlocked = False
    scene expression Transform("images/rooms/Igor_igorevic.JPG", size=(1920, 1080))
    play music "semens.mp3"
    show i normal at Position(xpos=0.1, ypos=1.0)
    show a normal at Position(xpos=0.25, ypos=1.0)
    show d normal at Position(xpos=0.40, ypos=1.0)
    show k normal at Position(xpos=0.55, ypos=1.0)
    show semens cyborg at Position(xpos=0.8, ypos=1.0)
    p3 "О, здарова, парни!"
    show i surprise  
    show a surprise   
    show d surprise 
    show k surprise    
    k "Здравствуйте, а что это на вас надето?.."
    p3 "Ох, долгая история. Кароче, ко мне пришел студент третьего курса, весь в слезах, представляете?"
    p3 "Он попросил у меня помощи с курсовой работой по схемотехнике..."
    show i normal  
    show a think   
    show d normal 
    show k normal  
    a "А научный руководитель случайно не Левиев?"
    p3 "Как ты понял?!"
    a "Было дело."
    show a normal
    p3 "Задание у него конечно интересное, но немножко сложноватое! Но, как видите, мы почти справились!
    Остался только мини-реактор!"
    p3 "Но, ребята, времени мало, поэтому действуем быстро! Кто пойдет отвечать?"
    show a happy
    a "Давайте я что ли."
    p3 "Алексей, мы и так виделись целое лето на втором курсе, дайте другим ребятам проявить себя!"
    show a sad
    p3 "Но учтите, задание будет не простым, курсовую работу все-таки делаем!"
    show i evil
    i "Ну пусть наш четырехглазый пойдет, он сказал что шарит в этой теме!"
    show k angry
    k "Я убью тебя..."
    show k happy
    k "Готов отвечать!"
    p3 "Тогда поехали!"
    hide i laugh
    hide a sad
    hide d normal
    show k think at Position(xpos=0.2, ypos=1.0)
    call screen story_scene_3_resistor_game
    show i happy at Position(xpos=0.1, ypos=1.0)
    show a happy at Position(xpos=0.25, ypos=1.0)
    show d happy at Position(xpos=0.40, ypos=1.0)
    show k happy at Position(xpos=0.55, ypos=1.0)
    p3 "Ничего себе, а ты разбираешься! Реально шаришь в этой теме."
    p3 "Ребята, вы не поверите, у нас и так на кафедре выпивки много, но сегодня заглянул очень важный человек и принес еще!"
    p3 "Он сказал, что это каких-то студентов, не ваше случайно?"
    e "Наше! Наше!"
    p3 "Ну, у нас уже места под осциллографы из-за бухла нет, поэтому забирайте все! Заслужили!"
    call show_beer(4)
    $ bottle_plus = 4
    $ success_flag = True
    $ renpy.pause()
    jump finish_cabinet_scene

# История Брызгалова (приседания)
label story_scene_4:    
    $ ui_unlocked = False
    scene expression Transform("images/rooms/brizgalov.JPG", size=(1920, 1080))
    play music "brizg_smeshariki.mp3"
    show i normal at Position(xpos=0.1, ypos=1.0)
    show a normal at Position(xpos=0.3, ypos=1.0)
    show d normal at Position(xpos=0.7, ypos=1.0)
    show k normal at Position(xpos=0.9, ypos=1.0)
    show brizg normal
    p4 "Физкульт-привет, спортсмены!"
    show i happy
    show a happy
    show d happy
    show k happy
    i "Спортсмены в строю! А что вы тут делаете?"
    p4 "Да я тут перед сном решил прокатиться на велосипеде, и не заметил, как доехал до главного здания!
    Решил передохнуть перед обратной дорогой, все-таки уже 100 километров проехал!"
    show d sad
    d "Я за прошлый год меньше пешком прошел..."
    show d happy
    p4 "И вот, пока отдыхал, студентку мою бывшую встретил! Сейчас вроде как у нас работает. Попросил у нее водички, а она мне
    помимо воды еще значит напитки дает, и сказала, что за ними скоро придут."
    show i surprise
    i "Ой, так это ж наше!"
    p4 "А она мне и наказала, что проверить вас надо будет! Хорошо, что недавно дневники самоподготовки просматривал, 
    и увидел, как Иван может за 30 секунд 200 раз присесть."
    show i laugh
    i "Давно это было, сейчас уже 300 могу!"
    p4 "Вот это настрой, ну тогда показывай! Понимаю, уже время позднее, поэтому планку немножко снизим."
    p4 "На старт, внимание, марш!"
    $ reset_story_scene_4_minigame()
    hide i normal
    hide a normal
    hide d normal
    hide k normal
    hide brizg normal
    call screen story_scene_4_minigame
    # show i normal at Position(xpos=0.1, ypos=1.0)
    # show a normal at Position(xpos=0.3, ypos=1.0)
    # show d normal at Position(xpos=0.7, ypos=1.0)
    # show k normal at Position(xpos=0.9, ypos=1.0)
    show brizg normal
    if story_scene_4_minigame_won:
        show i laugh at Position(xpos=0.1, ypos=1.0)
        show a happy at Position(xpos=0.3, ypos=1.0)
        show d laugh at Position(xpos=0.7, ypos=1.0)
        show k laugh at Position(xpos=0.9, ypos=1.0)
        p4 "Вот это темп. Сразу видно, что мои занятия не зря прошли! Молодец, молодец!"
        i "А приз спортсмену?"
        p4 "Ой, чуть не забыл! Да, старость не радость, одиннадцатый десяток пошел все-таки... Вот, держите, и помните - 
        в алкоголе всегда нужно знать меру, иначе можно выпить меньше!"
        i "Ура!"
        call show_beer(3, -0.35)
        $ bottle_plus = 3
        $ success_flag = True
        $ renpy.pause()
    else:
        show i sad at Position(xpos=0.1, ypos=1.0)
        show a sad at Position(xpos=0.3, ypos=1.0)
        show d sad at Position(xpos=0.7, ypos=1.0)
        show k sad at Position(xpos=0.9, ypos=1.0)
        p4 "Эх, не хватило совсем чуть-чуть. После такой защиты простительно, но в качестве домашнего задания
        даю вам 100 км на велосипеде по измайловскому парку, и чтоб потом дневник сдали!"
        i "Так точно, со следующей недели в зал ходить начну!"
        p4 "Вот это настрой!"
    jump finish_cabinet_scene

# История Адамовой (ГОТОВО)
label story_scene_5:
    $ ui_unlocked = False
    scene expression Transform("images/rooms/adam_1.JPG", size=(1920, 1080))
    play music "saw.mp3"
    show i normal at Position(xpos=0.1, ypos=1.0)
    show a normal at Position(xpos=0.2, ypos=1.0)
    show d normal at Position(xpos=0.3, ypos=1.0)
    show k normal at Position(xpos=0.4, ypos=1.0)
    show expression Solid("#000000da") as shkaf_darken onlayer master
    i "Ой, а чего это тут свет выключен..."
    $ renpy.pause(5.0, hard=True)
    k "Кажется, я нашел выключатель, щас включу..."
    pq "Ну здравствуйте, мальчики"
    scene expression Transform("images/rooms/adam_2.JPG", size=(1920, 1080))
    show adamova normal at Position(xpos=0.7, ypos=1.0)
    hide shkaf_darken
    show i surprise at Position(xpos=0.1, ypos=1.0)
    show a surprise at Position(xpos=0.2, ypos=1.0)
    show d mad at Position(xpos=0.3, ypos=1.0)
    show k surprise at Position(xpos=0.4, ypos=1.0)
    e "Твою ма..."
    p5 "Я очень ждала вас! У меня есть кое-какие ваши вещи, но перед этим придется пройти мое жаркое испытан..."
    d "По съебам, мужики, оно того не стоит!"
    hide i
    hide a
    hide d
    hide k
    with Dissolve(2.0)
    # Здесь отдельная сцена в коридоре
    hide adamova normal
    scene bg corridor
    scene expression Transform("images/rooms/adam_3.JPG", size=(1920, 1080))
    show i sad at Position(xpos=0.12, ypos=1.0)
    show a sad at Position(xpos=0.35, ypos=1.0)
    show d sad at Position(xpos=0.7, ypos=1.0)
    show k sad at Position(xpos=0.9, ypos=1.0)
    d "Еще пару таких встреч, и я завязываю с пивом..."
    jump finish_cabinet_scene

# История Бабкина (ГОТОВО)
label story_scene_6:
    $ ui_unlocked = False
    scene expression Transform("images/rooms/babkin.JPG", size=(1920, 1080))
    play music "Smeshariki_-_Grustnaya_tema_OST_Babochka_(SkySound.cc).mp3"
    show i normal at Position(xpos=0.1, ypos=1.0)
    show d normal at Position(xpos=0.7, ypos=1.0)
    show a normal at Position(xpos=0.3, ypos=1.0)    
    show k normal at Position(xpos=0.9, ypos=1.0)
    show babkin normal
    e "..."
    show i laugh 
    show d laugh 
    show a think 
    show k laugh
    e "ПХАХАХАХАХАХАХХ!"
    show i normal 
    show d normal 
    show a normal 
    show k normal
    d "...Кхм, простите."
    p6 "Что смешного?"
    show d happy
    d "Да так, анекдот веселый вспомнили..."
    p6 "Все одновременно?"
    show d normal
    d "Ну да..."
    p6 "Ну ладно..."
    d "Мы тут за вещичками пришли, позволите?"
    p6 "Мне сказали их так просто не отдавать..."
    show i evil
    i "(шепотом) А что он сделает, собьет нас?"
    show i normal
    p6 "...Но мне впадлу что-то придумывать, поэтому забирайте."
    call show_beer(1, 0.35)
    $ success_flag = True
    $ bottle_plus = 1
    $ renpy.pause()
    show k angry
    k "А почему тут пустая бутылка?.."
    p6 "Горе запивал."
    d "Ну, мы пойдем..."
    p6 "..."
    hide i
    hide a
    hide d
    hide k
    with Dissolve(2.0)
    jump finish_cabinet_scene

# История Левиева (ГОТОВО)
label story_scene_7:
    $ ui_unlocked = False
    scene expression Transform("images/rooms/leviev.JPG", size=(1920, 1080))
    play music "Dota_2_OST_-_Main_menu_1_(SkySound.cc).mp3"
    show i normal at Position(xpos=0.1, ypos=1.0)
    show d normal at Position(xpos=0.3, ypos=1.0)
    show a think at Position(xpos=0.2, ypos=1.0)    
    show k normal at Position(xpos=0.4, ypos=1.0)
    a "Чем тут воняет?.."
    play sound "audio/pudge_ult_half.mp3"
    $ renpy.pause(1.0, hard=True)
    show leviev normal at Position(xpos=0.7, ypos=1.0) with Dissolve(2.0) 
    $ renpy.pause(1.0, hard=True)
    show i surprise
    show d surprise
    show a surprise    
    show k surprise
    p7 "О, свежее мясо!"
    p7 "Мне тут моя подруга по несчастью передала кое-что, видимо, ваше. Еще добавила, чтобы прост так не отдавал, ХЭ!"
    show i sad
    show d sad
    show a sad
    show k sad
    a "Видно уже не наше..."
    p7 "Ох, Алексей, ваша работа в свое время произвела на меня впечатление! Значит, в этот раз будем строить ракету!"
    
    p7 "Ну, Алексей, подходите на защиту!"
    show k surprise
    k "(шепотом) Мужики, я кажется что-то вижу..."
    show a think at Position(xpos=0.1, ypos=1.0) 
    show leviev normal at Position(xpos=0.80, ypos=1.0)
    show shema at Transform(xalign=0.40, yalign=0.40, zoom=0.5)
    hide i 
    hide d
    hide k
    # Звук хука и картинка
    p7 "Ну вот значит, небольшая часть нашей схемы, давайте чуть подробнее ее разберем."
    a "А, ну тут все понятно!"    
    show k ctrl 1 at Position(xpos=0.1, ypos=1.0)
    p7 "Тогда рассказывайте!"
    show k ctrl 2 at Position(xpos=0.15, ypos=1.0)
    a "Нууу, тут у нас трехфазовый двуступенчатый резистор..."
    show k ctrl 1 at Position(xpos=0.20, ypos=1.0)
    p7 "Дальше-дальше!"
    show k ctrl 2 at Position(xpos=0.25, ypos=1.0)    
    a "Ээээм, еще я тут вижу адронный коллайдер с обратной связью..."
    show k ctrl 1 at Position(xpos=0.30, ypos=1.0)
    p7 "А зачем обратная связь?"
    show k ctrl 2 at Position(xpos=0.35, ypos=1.0)
    a "А, ну это же очевидно!"
    show k ctrl 1 at Position(xpos=0.40, ypos=1.0)
    p7 "Ваша правда...А как можно улучшить схему?"
    show k ctrl 2 at Position(xpos=0.45, ypos=1.0)
    a "Ну, есть несколько вариантов, но, на мой взгляд, самый логичный - добавить гравитационный разлом к восьмому выходу микросхемы!"
    show k ctrl 1 at Position(xpos=0.50, ypos=1.0)
    p7 "Интересное решение, интересное!"
    show k laugh
    k "Мужики я залутался!"
    call show_beer(2)
    $ success_flag = True
    $ renpy.pause()
    show a surprise
    a "Бежим! Только не попадитесь под хук!"
    hide a 
    hide k
    with Dissolve(2.0)
    jump finish_cabinet_scene

# История Бянкина (ГОТОВО)
label story_scene_8:
    $ ui_unlocked = False
    scene expression Transform("images/rooms/biankin.JPG", size=(1920, 1080))
    play music "Smeshariki_-_Nauchnaya_tema_OST_Pedagogicheskaya_poema_(SkySound.cc).mp3"
    show byankin normal
    show i normal at Position(xpos=0.12, ypos=1.0)
    show a normal at Position(xpos=0.25, ypos=1.0)
    show d normal at Position(xpos=0.8, ypos=1.0)
    show k normal at Position(xpos=0.9, ypos=1.0)
    p8 "Ох, студенты, здравствуйте, вы как раз вовремя!"
    show i surprise
    show a surprise
    show d surprise
    show k surprise
    i "Валерий Михайхлович, что здесь происходит?!"
    p8 "Ох, провожу эксперимент для новой лабораторной работы!"
    show i think
    show a think
    show d think
    show k think
    k "Новой лабораторной работы?.."
    p8 "Да, по синтезу нового элемента!"
    show i surprise
    show a surprise
    show d surprise
    show k surprise
    d "Чего-чего?!"
    p8 "Вы, ребята, очень кстати, ведь мне нужна ваша помощь!"
    a "Но что нам надо делать?!"
    p8 "Атомное ядро пока не стабильно, но, применив наши знания в области физики, мы сможем стабилизировать его и сотворить чудо!"
    show d sad
    d "Какие знания..."
    p8 "Студенты, вспомините все, чему я вас учил, и ловите только правильные формулы!"
    $ reset_story_scene_8_formula_game()
    hide i surprise 
    hide a surprise
    hide d sad
    hide k surprise
    hide byankin normal
    call screen story_scene_8_formula_game
    show i normal at Position(xpos=0.12, ypos=1.0)
    show a normal at Position(xpos=0.25, ypos=1.0)
    show d normal at Position(xpos=0.8, ypos=1.0)
    show k normal at Position(xpos=0.9, ypos=1.0)
    if story_scene_8_formula_won:
        show byankin happy
        show i happy at Position(xpos=0.12, ypos=1.0)
        show a happy at Position(xpos=0.25, ypos=1.0)
        show d happy at Position(xpos=0.8, ypos=1.0)
        show k happy at Position(xpos=0.9, ypos=1.0)
        p8 "Кажется, получилось... Мы создали Бянкиниум!" 
        e "Феноменально..."       
        p8 "Что ж, ребята, вы оказались хорошими студентами, а хорошие студенты заслуживают награды!"
        call show_beer(3)
        $ success_flag = True
        $ bottle_plus = 3
        $ renpy.pause()
    else:
        show byankin normal
        show i sad at Position(xpos=0.12, ypos=1.0)
        show a sad at Position(xpos=0.25, ypos=1.0)
        show d sad at Position(xpos=0.8, ypos=1.0)
        show k sad at Position(xpos=0.9, ypos=1.0)
        p8 "Эх, плохие вы студенты! И чем вы только на моих лекциях занимались... Придется все самому делать, а вы уходите!"
    jump finish_cabinet_scene

# История Кадырбаевой (ГОТОВО)
label story_scene_9:
    $ ui_unlocked = False
    scene expression Transform("images/rooms/kaderbaeva.JPG", size=(1920, 1080))
    play music "kadira_smeshariki.mp3"
    show i normal at Position(xpos=0.12, ypos=1.0)
    show a think at Position(xpos=0.25, ypos=1.0)
    show d normal at Position(xpos=0.8, ypos=1.0)
    show k normal at Position(xpos=0.9, ypos=1.0)
    a "У меня плохое предчувствие..."
    $ renpy.pause(1.0, hard=True)
    show kadira normal at Position(xpos=0.50, ypos=1.0) with Dissolve(2.0)
    $ renpy.pause(1.0, hard=True)
    show a surprise
    a "Это че за аниме?!"
    show i evil
    show d surprise
    show k surprise
    p10 "Ребята, привет! ♥"
    show i laugh
    i "Охаё!"
    show a sad
    a "Не матерись, пожалуйста."
    show i sad
    i "Извини..."
    show i happy
    show a normal
    show d normal
    show k happy
    p10 "Мальчики, я так рада вас видеть! Я уже думала, что вы не придете!"
    i "А как вы узнали?"
    p10 "Ой, а ко мне забегала моя {color=#dce800}★{/color} преподавательница {color=#dce800}★{/color}, и предупредила о вашем скором прибытии! Еще и гостинцы оставила! ☺︎"
    p10 "...Но сказала вам просто так их не отдавать... 😔"
    p10 "Мальчики, должна вам признаться, мне нужна ваша помощь... 👉👈"
    show i laugh
    i "Поможем, чем сможем, Анастасия Рустемовна! 😎"
    p10 "Понимаете, в последнее время, когда я захожу на кафедру и вижу наших преподавателей, сердце стучит как бешеное! 🥺"
    show i think
    i "Не может быть..."
    p10 "Кажется, я влюбилась в одного из них, но не могу понять, в кого же именно! 😳"
    p10 "Кто-нибудь из вас сможет мне помочь?.. Пожалуйста? 🙏"
    show i laugh
    i "Я разберусь, я в таких делах мастер!"
    show i angry
    show a think
    show d laugh
    show k laugh
    ee "Пхахахахахах"
    show i happy
    p10 "Спасибо-спасибо! 🥰 Тогда подскажешь, в кого из них я могла влюбиться? 💖"
    hide a
    hide d
    hide k
    show kadira normal at Position(xpos=0.84, ypos=1.0)
    show i think at Position(xpos=0.18, ypos=1.0)
    $ reset_story_scene_10_choice_game()
    call screen story_scene_10_choice_game
    if story_scene_10_choice == "3":
        show kadira at Position(xpos=0.50, ypos=1.0)
        p10 "Ты выбрал его... Значит, ты действительно меня понимаешь. 💞"
        show i laugh
        i "Я же говорил я в любви толк знаю!"
        p10 "Как же я рада! ✨ Ну все, в следующий раз, когда его увижу, точно-точно признаюсь в своих чувствах! 🤩"
        p10 "А это вам, мальчики! Спасибо, что помогли навести порядок в моем сердце! 😘"
        call show_beer(2)
        $ success_flag = True
        i "Удачи тебе, подруга!"
        $ renpy.pause() 
    else:
        show kadira  at Position(xpos=0.50, ypos=1.0)
        p10 "Мне кажется, ты не совсем меня понял... 😢"
        show i sad
        i "Неужели я посмотрел недостаточно романтиких аниме?!"
        p10 "Простите, мальчики, мне нужно побыть одной... 😔"
    jump finish_cabinet_scene
        

# История Выхованца (ГОТОВО)
label story_scene_10:
    $ ui_unlocked = False
    scene expression Transform("images/rooms/vihovanic.JPG", size=(1920, 1080))
    play music "Smeshariki_-_Krosh_OST_Skamejka_(SkySound.cc).mp3"
    show i normal at Position(xpos=0.12, ypos=1.0)
    show a normal at Position(xpos=0.25, ypos=1.0)
    show d normal at Position(xpos=0.40, ypos=1.0)
    show k normal at Position(xpos=0.55, ypos=1.0)
    $ renpy.pause(1.0, hard=True)
    show vikh normal at Position(xpos=0.80, ypos=1.0) with Dissolve(2.0)
    $ renpy.pause(1.0, hard=True)
    p11 "ГОСТЫ, ГОСТЫ, ПОКАЖИТЕ МНЕ ГОСТЫ!"
    show i surprise
    show a surprise 
    show d surprise 
    show k surprise
    e "АААААААА"
    p11 "НЕТ ВРЕМЕНИ ОБЪЯСНЯТЬ, МНЕ СРОЧНО НУЖНО ПРОВЕРИТЬ КАКОЙ-НИБУДЬ ОТЧЕТ НА СООТВЕТСТВИЕ ГОСТУ!"
    p11 "ВОТ, РЕШИТЕ ЗАДАЧКУ, А ОТЧЕТ НА ПОЧТУ СКИНИТЕ! Я СМОТРЮ ИХ КАЖДЫЙ ЧЕТВЕРГ В 20:31!"
    $ reset_story_scene_8_chain_game()
    call screen story_scene_8_chain_game
    if story_scene_8_chain_success:
        p11 "ЛАДНО, ЗАСЧИТЫВАЮ! И ЗАБЕРИТЕ ОТСЮДА СВОИ БУТЫЛКИ, У НИХ НА ЭТИКЕТКАХ ШРИФТ НЕ ПО ГОСТУ!"
        call show_beer(3)
        $ bottle_plus = 3
        $ success_flag = True
        $ renpy.pause() 
    else:
        show i sad
        show a sad 
        show d sad 
        show k sad
        p11 "ВЫ ЧТО ТУТ, ВСЕ НА ПИТОНЕ ПИШИТЕ?! А НУ ПОШЛИ ВОН! ГОСТ САМ СЕБЯ НЕ ПРОВЕРИТ!"
    jump finish_cabinet_scene

# История Фёдорова (ГОТОВО)
label story_scene_11:
    $ ui_unlocked = False
    scene expression Transform("images/rooms/fedorov.JPG", size=(1920, 1080))
    play music "Smeshariki_-_Maskarad_OST_Maskarad_(SkySound.cc).mp3"    
    show i normal at Position(xpos=0.1, ypos=1.0)
    show a normal at Position(xpos=0.25, ypos=1.0)
    show d normal at Position(xpos=0.40, ypos=1.0)
    show k normal at Position(xpos=0.55, ypos=1.0)
    i "Никого..."
    a "Ну хоть немного отдохнем."
    d "О, тут опять записка какая-то..."
    call screen story_scene_12_note
    call screen story_scene_12_note_text
    show i laugh
    show a happy 
    show d happy
    show k happy
    d "Фартануло ебать!"
    call show_beer(2)
    $ success_flag = True
    $ renpy.pause()
    i "Забираем!"
    jump finish_cabinet_scene

# История Тихомировой (нашла куртку на кафедре)
label final:
    scene expression Transform("images/rooms/koridor.JPG", size=(1920, 1080))
    play music "coridor.mp3"
    show i normal at Position(xpos=0.12, ypos=1.0) 
    show a normal at Position(xpos=0.35, ypos=1.0) 
    show d map 2 at Position(xpos=0.6, ypos=1.0) 
    show k normal at Position(xpos=0.85, ypos=1.0) 
    d "Кажется, мы прошлись по всем кабинетам."
    show d normal
    i "Значит, пришло время вернуться на кафедру."
    a "Как думаете, {color=#ff5555}она{/color} нас ждет?"
    k "Я в этом уверен."
    hide i
    hide a
    hide d
    hide k
    with Dissolve(2.0)  
    scene expression Transform("images/rooms/kaf.JPG", size=(1920, 1080))
    play music "Linkin_Park_-_What_I_ve_Done_Instrumental_(SkySound.cc).mp3"
    show i normal at Position(xpos=0.10, ypos=1.0) 
    show a normal at Position(xpos=0.25, ypos=1.0) 
    show d normal at Position(xpos=0.75, ypos=1.0) 
    show k normal at Position(xpos=0.90, ypos=1.0)
    with Dissolve (2.0)
    $ renpy.pause(5.0, hard=True)
    pq "Что ж, кажется, это приключение подходит к концу..."
    show tishka normal with Dissolve(2.0)
        # zoom 0.9
        # xalign 0.5
        # yalign 0.5
    p9 "...И только от вас зависит, счастливый ли это будет конец."
    show i happy
    show a happy
    show d happy
    show k happy
    e "Добрый вечер, Елизавета Алексеевна!"
    show i normal
    show a normal
    show d normal
    show k normal
    p9 "Должна сказать, ваш план был хорош..."
    show i sad
    show a think
    show d sad
    show k sad
    p9 "...Если бы вы только не засунули ваши напитки в мой кафедральный шкаф."
    show i normal
    show a normal
    show d normal
    show k normal
    p9 "Я просто не могла не оценить такую наглость, и решила устроить вам финальную лабораторную работу!"
    p9 "А теперь пришло время защиты! Всё собрали?"
    # ИСПРАААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААВИТЬ
    # $ bottle_counter = 15
    if bottle_counter >= 16:
        jump final_good
    else:
        jump final_bad
    # call credits_scene
    # return

label show_beer_final():    
    python:
        positions = [(0.03, 0.55), (0.07, 0.55),
(0.11, 0.55), (0.15, 0.55), (0.19, 0.55), (0.23, 0.55),
(0.27, 0.55), (0.31, 0.55), (0.35, 0.55), (0.39, 0.55),
(0.43, 0.55), (0.47, 0.55), (0.51, 0.55), (0.55, 0.55),
(0.59, 0.55), (0.63, 0.55), (0.67, 0.55), (0.71, 0.55),
(0.75, 0.55), (0.79, 0.55), (0.83, 0.55), (0.87, 0.55), (0.91, 0.55), (0.95, 0.55),]
        for index in range(bottle_counter):            
            xpos, ypos = positions[index]
            renpy.show(
                "beer",
                at_list=[Transform(xalign=xpos, yalign=ypos, zoom=0.15)],
                tag="beer_%d" % index,
            )
            renpy.with_statement(Dissolve(0.5))        
    return

label final_good:
    show i happy
    show a happy
    show d happy
    show k happy
    e "Всё, Елизавета Алексеевна!"
    p9 "Ха, все-таки не зря я вас не отчислила! Лабораторная работа принимается!"
    e "Ура!"
    p9 "И, так как вы уже защитили свои дипломы, то ,технически, вы больше не студенты..."
    p9 "А значит, можете спокойно праздновать у нас на кафедре, не боясь отчисления!"
    e "УРА!"
    p9 "А я позову коллег, и мы пропустим пару стопочек на кафедре ИУ4, Семенцов всех приглашает! Счастливо!"
    e "До свидания, Елизавета Алексеевна!"
    stop music
    hide tishka normal
    with Dissolve(2.0) 
    $ renpy.pause(2.0, hard=True)
    show i laugh at Position(xpos=0.15, ypos=1.0)
    show a at Position(xpos=0.35, ypos=1.0)
    show d at Position(xpos=0.65, ypos=1.0) 
    show k at Position(xpos=0.85, ypos=1.0) 
    i "Ну, теперь-то мы хряпнем?"
    play music "lil_krystalll_-_Air_Force_(SkySound.cc).mp3"
    a "Открывай уже!"
    show d mad
    d "Я уже больше не могу терпеть!"
    show d laugh
    show k laugh
    k "А у меня еще водка в портфеле!"
    call show_beer_final()
    e "ЗА НАС, ЗА {color=#ff5555}РЕМОНТ{/color}!"
    call credits_scene

label final_bad:
    d "Нуууу, не совсем..."
    show i sad
    show a sad
    show d sad
    show k sad 
    p9 "И это всё? Ребят, да тут даже на тройку не тянет..."
    p9 "Боюсь, с такими неутешительными результатами зачесть лабораторную работу я вам не могу."
    p9 "А без лабораторной работы я не могу вам разрешить остаться на кафедре!"
    d "Ну, мы пойдем тогда..."
    p9 "Бывайте!"
    hide i
    hide a
    hide d
    hide k
    with Dissolve(2.0)     
    scene expression Transform("images/IMG_4434.JPG", size=(1920, 1080))
    play music "DJ_FON_Muzyka_dlya_fona_-_Grustnaya_muzyka_bez_slov_dlya_fona_(SkySound.cc).mp3"
    show i sad at Position(xpos=0.15, ypos=1.0)
    show a sad at Position(xpos=0.35, ypos=1.0)
    show d sad at Position(xpos=0.65, ypos=1.0) 
    show k sad at Position(xpos=0.85, ypos=1.0) 
    with Dissolve(2.0)
    a "Ну, в Свободу?"
    d "Поехли..."
    i "Это провал, господа..."
    k "Блять я заплакал..."
    call credits_scene


label credits_scene:
    scene black
    with Dissolve(5.0)
    # stop music fadeout 1.0
    call screen credits_screen
    return

transform credits_fadein:
    alpha 0.0
    linear 2.0 alpha 1.0

screen credits_screen():
    tag credits
    modal True

    fixed at credits_fadein:
        add Solid("#0c1018")

        frame:
            xpos 0
            ypos 0
            xsize 1920
            ysize 1080
            background None
            padding (60, 40)

            vbox:
                spacing 24
                xfill True

                hbox:
                    xfill True

                    vbox:
                        spacing 6

                        text "КОНЕЦ":
                            size 56
                            color "#f6f0dd"

                        text "":
                            size 24
                            color "#c8d2e0"

                    textbutton "Закрыть":
                        xalign 1.0
                        action MainMenu()

                viewport:
                    mousewheel True
                    draggable True
                    scrollbars "vertical"
                    side_yfill True
                    xsize 1800
                    ysize 860

                    vbox:
                        spacing 30
                        xfill True

                        null height 10

                        for entry in credits_entries:
                            frame:
                                xfill True
                                background Solid("#172030dd")
                                padding (28, 28)

                                hbox:
                                    spacing 28
                                    xfill True

                                    if credits_entry_image(entry):
                                        add Transform(
                                            credits_entry_image(entry),
                                            fit="contain",
                                            xsize=520,
                                            ysize=290,
                                        )
                                    else:
                                        frame:
                                            xsize 520
                                            ysize 290
                                            background Solid("#243147")

                                            text "IMAGE\n520 x 290":
                                                align (0.5, 0.5)
                                                text_align 0.5
                                                size 32
                                                color "#f6f0dd"

                                    vbox:
                                        spacing 12
                                        xmaximum 1120

                                        text "[entry['title']]":
                                            size 42
                                            color "#f6f0dd"

                                        if entry.get("subtitle"):
                                            text "[entry['subtitle']]":
                                                size 24
                                                color "#86b5ff"

                                        if entry.get("text"):
                                            text "[entry['text']]":
                                                size 28
                                                color "#d7deea"

                        null height 40

screen story_scene_8_formula_game():
    modal True
    zorder 1200

    if story_scene_8_formula_won or story_scene_8_formula_lost:
        timer 0.01 action Return()
    else:
        timer 0.35 repeat True action Function(story_scene_8_formula_tick)

    key "K_LEFT" action Function(story_scene_8_formula_move_left)
    key "K_RIGHT" action Function(story_scene_8_formula_move_right)

    add Solid("#10141cee")

    frame:
        xpos 0
        ypos 0
        xsize 1920
        ysize 1080
        background None
        padding (40, 30)

        text "Поймай формулу":
            xalign 0.5
            ypos 10
            size 38
            color "#ffffff"
            outlines [(2, "#000000", 0, 0)]

        text "Лови только правильные формулы. Управление: стрелочки вправо и влево.":
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

                add Transform("images/Alexey/a bag.png", fit="contain", xsize=240, ysize=140, rotate=0):
                    align (0.5, 0.5)

screen story_scene_4_minigame():
    modal True
    zorder 1200

    $ state_text = "Положение: вниз" if story_scene_4_is_down else "Положение: вверх"
    $ state_color = "#6ec1ff" if story_scene_4_is_down else "#ffffff"
    $ down_bg = "#2b5cffaa" if story_scene_4_is_down else "#1d1d1daa"
    $ up_bg = "#2fa34aaa" if not story_scene_4_is_down else "#1d1d1daa"
    $ pose_image = "images/Ivan/i brizg 1.png" if story_scene_4_is_down else "images/Ivan/i brizg 2.png"

    if story_scene_4_minigame_won or story_scene_4_minigame_lost:
        timer 0.01 action Return()
    else:
        timer 1.0 repeat True action Function(story_scene_4_tick)

    key "K_s" action Function(story_scene_4_press_down)
    key "K_w" action Function(story_scene_4_press_up)
    key "s" action Function(story_scene_4_press_down)
    key "w" action Function(story_scene_4_press_up)

    add Transform(pose_image, fit="contain", xsize=700, ysize=980, rotate=360):
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

