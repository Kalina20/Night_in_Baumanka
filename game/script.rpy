define e = Character('я', color="#c8ffc8")
define p1 = Character("1", color="#ffd966")
define p2 = Character("2", color="#ffd966")
define p3 = Character("3", color="#ffd966")
define p4 = Character("4", color="#ffd966")
define p5 = Character("5", color="#ffd966")
define p6 = Character("6", color="#ffd966")
define p7 = Character("7", color="#ffd966")
define p8 = Character("8", color="#ffd966")
define p9 = Character("9", color="#ffd966")
define p10 = Character("10", color="#ffd966")
define p11 = Character("11", color="#ffd966")
define p12 = Character("12", color="#ffd966")

default room_exit_counter = 0
default visited_cabinets = []
default ui_unlocked = False
default room_assignments = {}

label start:
    python:
        rooms = ["420", "421", "422", "423", "424", "425", "426", "427", "428", "429", "430", "431"]
        people = [
            (p1, "Я персонаж номер 1."),
            (p2, "Я персонаж номер 2."),
            (p3, "Я персонаж номер 3."),
            (p4, "Я персонаж номер 4."),
            (p5, "Я персонаж номер 5."),
            (p6, "Я персонаж номер 6."),
            (p7, "Я персонаж номер 7."),
            (p8, "Я персонаж номер 8."),
            (p9, "Я персонаж номер 9."),
            (p10, "Я персонаж номер 10."),
            (p11, "Я персонаж номер 11."),
            (p12, "Я персонаж номер 12."),
        ]
        renpy.random.shuffle(people)
        room_assignments = dict(zip(rooms, people))

    jump vvedenie

label vvedenie:
    scene bg room
    e 'Введение'
    jump shkaf_transition

label shkaf_transition:
    scene bg room
    e 'шкаф'
    jump base_room

label base_room:
    scene bg room
    $ ui_unlocked = True
    e 'Комната'
    $ renpy.pause()
    jump base_room

label room_420:
    scene bg room
    $ ui_unlocked = True
    $ speaker, line = room_assignments["420"]
    $ renpy.say(speaker, line)
    if "420" not in visited_cabinets:
        $ visited_cabinets.append("420")
    $ room_exit_counter += 1
    jump base_room

label room_421:
    scene bg room
    $ ui_unlocked = True
    $ speaker, line = room_assignments["421"]
    $ renpy.say(speaker, line)
    if "421" not in visited_cabinets:
        $ visited_cabinets.append("421")
    $ room_exit_counter += 1
    jump base_room

label room_422:
    scene bg room
    $ ui_unlocked = True
    $ speaker, line = room_assignments["422"]
    $ renpy.say(speaker, line)
    if "422" not in visited_cabinets:
        $ visited_cabinets.append("422")
    $ room_exit_counter += 1
    jump base_room

label room_423:
    scene bg room
    $ ui_unlocked = True
    $ speaker, line = room_assignments["423"]
    $ renpy.say(speaker, line)
    if "423" not in visited_cabinets:
        $ visited_cabinets.append("423")
    $ room_exit_counter += 1
    jump base_room

label room_424:
    scene bg room
    $ ui_unlocked = True
    $ speaker, line = room_assignments["424"]
    $ renpy.say(speaker, line)
    if "424" not in visited_cabinets:
        $ visited_cabinets.append("424")
    $ room_exit_counter += 1
    jump base_room

label room_425:
    scene bg room
    $ ui_unlocked = True
    $ speaker, line = room_assignments["425"]
    $ renpy.say(speaker, line)
    if "425" not in visited_cabinets:
        $ visited_cabinets.append("425")
    $ room_exit_counter += 1
    jump base_room

label room_426:
    scene bg room
    $ ui_unlocked = True
    $ speaker, line = room_assignments["426"]
    $ renpy.say(speaker, line)
    if "426" not in visited_cabinets:
        $ visited_cabinets.append("426")
    $ room_exit_counter += 1
    jump base_room

label room_427:
    scene bg room
    $ ui_unlocked = True
    $ speaker, line = room_assignments["427"]
    $ renpy.say(speaker, line)
    if "427" not in visited_cabinets:
        $ visited_cabinets.append("427")
    $ room_exit_counter += 1
    jump base_room

label room_428:
    scene bg room
    $ ui_unlocked = True
    $ speaker, line = room_assignments["428"]
    $ renpy.say(speaker, line)
    if "428" not in visited_cabinets:
        $ visited_cabinets.append("428")
    $ room_exit_counter += 1
    jump base_room

label room_429:
    scene bg room
    $ ui_unlocked = True
    $ speaker, line = room_assignments["429"]
    $ renpy.say(speaker, line)
    if "429" not in visited_cabinets:
        $ visited_cabinets.append("429")
    $ room_exit_counter += 1
    jump base_room

label room_430:
    scene bg room
    $ ui_unlocked = True
    $ speaker, line = room_assignments["430"]
    $ renpy.say(speaker, line)
    if "430" not in visited_cabinets:
        $ visited_cabinets.append("430")
    $ room_exit_counter += 1
    jump base_room

label room_431:
    scene bg room
    $ ui_unlocked = True
    $ speaker, line = room_assignments["431"]
    $ renpy.say(speaker, line)
    if "431" not in visited_cabinets:
        $ visited_cabinets.append("431")
    $ room_exit_counter += 1
    jump base_room
