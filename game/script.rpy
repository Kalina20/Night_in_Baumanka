define e = Character('я', color="#ffffff")
define i = Character('Иван Писарев', color="#db4010")
define a = Character('Алексей Калиниченко', color="#559d0d")
define d = Character('Даниил Перекосов', color="#1c3ace")
define k = Character('Константин Горшков', color="#e4e815")

define p1 = Character("Иван Писарев", color="#db4010")
define p2 = Character("Алексей Калиниченко", color="#559d0d")
define p3 = Character("Даниил Перекосов", color="#1c3ace")
define p4 = Character("Константин Горшков", color="#e4e815")
define p5 = Character("Марина Лебедева", color="#ff8a65")
define p6 = Character("Егор Сафронов", color="#8bc34a")
define p7 = Character("Света Орлова", color="#4fc3f7")
define p8 = Character("Роман Власов", color="#ba68c8")
define p9 = Character("Нина Белова", color="#f06292")
define p10 = Character("Тимур Давыдов", color="#ffb74d")
define p11 = Character("Оля Жукова", color="#81c784")
define p12 = Character("Максим Громов", color="#90a4ae")

default room_exit_counter = 0
default visited_cabinets = []
default ui_unlocked = False
default room_assignments = {}

init python:
    # Each character carries all content needed for a room scene.
    characters_data = [
        {
            "id": 1,
            "speaker": p1,
            "image": "i normal",
            "lines": [
                "Я все еще не верю, что мы действительно дошли до этого дня.",
                "Кажется, в этих кабинетах спрятано больше историй, чем в наших чатах.",
            ],
        },
        {
            "id": 2,
            "speaker": p2,
            "image": "a normal",
            "lines": [
                "Если честно, я зашел сюда просто перевести дух.",
                "Но теперь уже хочется понять, кто еще бродит по этому этажу.",
            ],
        },
        {
            "id": 3,
            "speaker": p3,
            "image": "d normal",
            "lines": [
                "Тишина в корпусе какая-то слишком подозрительная.",
                "Такое чувство, будто здание ждет, когда мы сделаем следующий шаг.",
            ],
        },
        {
            "id": 4,
            "speaker": p4,
            "image": "k normal",
            "lines": [
                "Я бы не называл это обычной прогулкой после защиты.",
                "У этого вечера явно есть свой сценарий.",
            ],
        },
        {
            "id": 5,
            "speaker": p5,
            "image": None,
            "lines": [
                "Я оставила в одном из кабинетов записку, но уже не помню в каком.",
                "Если найдешь ее, не читай вслух, договорились?",
            ],
        },
        {
            "id": 6,
            "speaker": p6,
            "image": None,
            "lines": [
                "На этом этаже слишком хорошо слышны шаги.",
                "Иногда кажется, что за нами кто-то идет на полсекунды позже.",
            ],
        },
        {
            "id": 7,
            "speaker": p7,
            "image": None,
            "lines": [
                "Я всегда думала, что ночью универ выглядит романтичнее.",
                "Оказалось, ночью он выглядит так, будто знает о нас лишнее.",
            ],
        },
        {
            "id": 8,
            "speaker": p8,
            "image": None,
            "lines": [
                "Если открыть все кабинеты подряд, мы точно соберем полную картину.",
                "Главное, чтобы картина потом не собрала нас.",
            ],
        },
        {
            "id": 9,
            "speaker": p9,
            "image": None,
            "lines": [
                "Я запомнила этот коридор еще с первого курса.",
                "Только тогда он казался бесконечным, а сейчас — замкнутым.",
            ],
        },
        {
            "id": 10,
            "speaker": p10,
            "image": None,
            "lines": [
                "Хочешь совет? Не заходи в кабинет, если тебе уже не по себе.",
                "Обычно интуиция ошибается реже, чем расписание.",
            ],
        },
        {
            "id": 11,
            "speaker": p11,
            "image": None,
            "lines": [
                "Я думала, что после защиты станет легче.",
                "Но кажется, самое важное начинается только сейчас.",
            ],
        },
        {
            "id": 12,
            "speaker": p12,
            "image": None,
            "lines": [
                "В этом месте слишком много совпадений, чтобы считать их случайностью.",
                "Если мы дошли сюда вместе, значит, назад дороги уже не будет.",
            ],
        },
    ]

label start:
    python:
        rooms = ["420", "421", "422", "423", "424", "425", "426", "427", "428", "429", "430", "431"]
        people = characters_data[:]
        renpy.random.shuffle(people)
        room_assignments = dict(zip(rooms, people))

    jump vvedenie

label vvedenie:
    scene bg room
    play music "audio/Minecraft 1.mp3" fadein 1.0
    show i normal at Position(xpos=0.1, ypos=1.0)
    show a normal at Position(xpos=0.3, ypos=1.0)
    show d normal at Position(xpos=0.6, ypos=1.0)
    show k normal at Position(xpos=0.9, ypos=1.0)
    'И вот наша дружная компания сдала выпускные квалификационные работы на отлично'
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

label visit_room(room_id):
    scene bg room
    $ ui_unlocked = True
    $ person = room_assignments[room_id]

    if person["image"]:
        show expression person["image"]

    python:
        for line in person["lines"]:
            renpy.say(person["speaker"], line)

    if room_id not in visited_cabinets:
        $ visited_cabinets.append(room_id)

    $ room_exit_counter += 1
    jump base_room

label room_420:
    call visit_room("420")
    return

label room_421:
    call visit_room("421")
    return

label room_422:
    call visit_room("422")
    return

label room_423:
    call visit_room("423")
    return

label room_424:
    call visit_room("424")
    return

label room_425:
    call visit_room("425")
    return

label room_426:
    call visit_room("426")
    return

label room_427:
    call visit_room("427")
    return

label room_428:
    call visit_room("428")
    return

label room_429:
    call visit_room("429")
    return

label room_430:
    call visit_room("430")
    return

label room_431:
    call visit_room("431")
    return
