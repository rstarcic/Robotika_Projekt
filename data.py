from classes import Classroom, Subject, Professor

classrooms = [
    Classroom("108", False),
    Classroom("109", False),
    Classroom("110", True),
    Classroom("132", False),
]

subjects = [
    # PRVA godina
    Subject("Diferencijalni i integralni račun", "Predavanje", [1]),  # 0
    Subject("Diferencijalni i integralni račun", "Vježbe", [1]),  # 1
    Subject("Logika i diskretna matematika", "Predavanje", [1]),  # 2
    Subject("Logika i diskretna matematika", "Vježbe", [1]),  # 3
    Subject("Multimedijalni sustavi", "Predavanje", [1]),  # 4
    Subject("Multimedijalni sustavi", "Vježbe", [1]),  # 5
    Subject("Osnove IKT", "Predavanje", [1]),  # 6
    Subject("Osnove IKT", "Vježbe", [1]),  # 7
    Subject("Osnove podatkovne znanosti", "Predavanje", [1]),  # 8
    Subject("Osnove podatkovne znanosti", "Vježbe", [1]),  # 9
    Subject("Programiranje", "Predavanje", [1]),  # 10
    Subject("Programiranje", "Vježbe", [1]),  # 11
    # DRUGA godina
    Subject("Baze podataka II", "Predavanje", [2]),  # 12
    Subject("Baze podataka II", "Vježbe", [2]),  # 13
    Subject("Mrežni sustavi", "Predavanje", [2]),  # 14
    Subject("Mrežni sustavi", "Vježbe", [2]),  # 15
    Subject("Statistika", "Predavanje", [2]),  # 16
    Subject("Statistika", "Vježbe", [2]),  # 17
    Subject("SPA", "Predavanje", [2]),  # 18
    Subject("SPA", "Vježbe", [2]),  # 19
    # TREĆA godina
    Subject("Operacijska istraživanja", "Predavanje", [3]),  # 20
    Subject("Operacijska istraživanja", "Vježbe", [3]),  # 21
    Subject("Praktikum", "Predavanje", [3]),  # 22
    Subject("Web aplikacije", "Predavanje", [3]),  # 23
    Subject("Web aplikacije", "Vježbe", [3]),  # 24
    Subject("Upravljanje poslovnim procesima", "Predavanje", [3]),  # 25
    Subject("Upravljanje poslovnim procesima", "Vježbe", [3]),  # 26
    # ČETVRTA godina
    Subject("IT management", "Predavanje", [4]),  # 27
    Subject("IT management", "Vježbe", [4]),  # 28
    Subject("Mobilne aplikacije", "Predavanje", [4]),  # 29
    Subject("Mobilne aplikacije", "Vježbe", [4]),  # 30
    Subject("Modeli računarstva", "Predavanje", [4]),  # 31
    Subject("Modeli računarstva", "Vježbe", [4]),  # 32
    Subject("Raspodijeljeni sustavi", "Predavanje", [4]),  # 33
    Subject("Raspodijeljeni sustavi", "Vježbe", [4]),  # 34
    # PETA godina
    Subject("Funkcijsko programiranje", "Predavanje", [5]),  # 35
    Subject("Funkcijsko programiranje", "Vježbe", [5]),  # 36
    Subject("Internet stvari", "Predavanje", [5]),  # 37
    Subject("Internet stvari", "Vježbe", [5]),  # 38
    Subject("Napredni algoritmi i strukture podataka", "Predavanje", [5]),  # 39
    Subject("Napredni algoritmi i strukture podataka", "Vježbe", [5]),  # 40
    Subject("Razvoj IT rješenja", "Predavanje", [5]),  # 41
    # IZBORNI
    Subject("Stručna praksa prijediplomski", "Praksa", [3], is_elective=True),  # 42
    Subject("Stručna praksa diplomski", "Praksa", [4, 5], is_elective=True),  # 43
    Subject("Upravljanje projektima", "Predavanje", [4, 5], is_elective=True),  # 44
    Subject("Upravljanje projektima", "Vježbe", [4, 5], is_elective=True),  # 45
    Subject(
        "Geoinformacijski sustavi", "Predavanje", [2, 3, 4], is_elective=True
    ),  # 46
    Subject("Osnove ekonomije", "Predavanje", [2], is_elective=True),  # 47
    Subject("Osnove ekonomije", "Predavanje", [2], is_elective=True),  # 48
    Subject(
        "Računovodstvo u virtualnom okruženju", "Predavanje", [4, 5], is_elective=True
    ),  # 49
    Subject(
        "Računovodstvo u virtualnom okruženju", "Vježbe", [4, 5], is_elective=True
    ),  # 50
    Subject(
        "Sustavi elektroničkog učenja", "Predavanje", [4, 5], is_elective=True
    ),  # 51
    Subject("Sustavi elektroničkog učenja", "Vježbe", [4, 5], is_elective=True),  # 52
    Subject("Robotika", "Predavanje", [4], is_elective=True),  # 53
    Subject("Robotika", "Vježbe", [4], is_elective=True),  # 54
    Subject("Blockchain aplikacije", "Predavanje", [4], is_elective=True),  # 55
    Subject("Forenzičko računovodstvo", "Predavanje", [4], is_elective=True),  # 56
    Subject("Forenzičko računovodstvo", "Vježbe", [4], is_elective=True),  # 57
    Subject(
        "Interakcija čovjeka i računala", "Predavanje", [4], is_elective=True
    ),  # 58
    Subject("Sustavi elektroničkog učenja", "Predavanje", [4], is_elective=True),  # 59
    Subject("Sustavi elektroničkog učenja", "Vježbe", [4], is_elective=True),  # 60
]

professors = [
    Professor(
        "izv. prof. dr. sc. Valter Boljunčić",
        ["Mon 10-12", "Wed 10-12"],
        [subjects[0], subjects[1]],
    ),
    Professor(
        "doc. dr. sc. Siniša Miličić",
        ["Wed 8-10", "Thu 10-12"],
        [
            subjects[2],
            subjects[8],
            subjects[22],
            subjects[35],
            subjects[36],
        ],
    ),
    Professor(
        "mag. edu. math. Tea Šumberac",
        ["Thu 8-10", "Fri 8-10"],
        [subjects[3]],
    ),
    Professor(
        "izv. prof. dr. sc. Darko Etinger",
        ["Thu 8-10", "Fri 10-12", "Mon 10-12"],
        [subjects[4], subjects[6], subjects[25], subjects[27], subjects[58]],
    ),
    Professor(
        "izv. prof. dr. sc. Željka Tomasović",
        ["Thu 8-10", "Thu 14-16"],
        [subjects[5]],
    ),
    Professor(
        "mag. inf. Romeo Šajina",
        ["Thu 8-10", "Thu 14-16", "Tue 14-16"],
        [subjects[7], subjects[13]],
    ),
    Professor(
        "mag. inf. Robert Šajina",
        ["Thu 8-10", "Thu 8-10"],
        [subjects[11]],
    ),
    Professor(
        "izv. prof. dr. sc. Snježana Babić",
        ["Tue 8-10", "Wed 14-16"],
        [subjects[28], subjects[41], subjects[51], subjects[59], subjects[60]],
    ),
    Professor(
        "doc. dr. sc. Ivan Lorencin",
        ["Tue 14-16", "Fri 10-12"],
        [
            subjects[9],
            subjects[14],
            subjects[42],
            subjects[43],
            subjects[53],
            subjects[54],
        ],
    ),
    Professor(
        "doc. dr. sc. Goran Oreški",
        ["Mon 14-16", "Wed 10-12"],
        [subjects[12]],
    ),
    Professor(
        "dipl. ing. Dalibor Fonović",
        ["Mon 10-12", "Wed 8-10"],
        [
            subjects[15],
            subjects[38],
        ],
    ),
    Professor(
        "dr. sc. Darko Brborović",
        ["Mon 10-12", "Wed 8-10"],
        [
            subjects[16],
            subjects[17],
            subjects[31],
            subjects[32],
        ],
    ),
    Professor(
        "izv. prof. dr. sc. Tihomir Orehovački",
        ["Mon 10-12", "Wed 8-10"],
        [
            subjects[10],
            subjects[18],
            subjects[39],
        ],
    ),
    Professor(
        "mr. sc. Igor Škorić",
        ["Mon 10-12", "Wed 8-10"],
        [
            subjects[19],
            subjects[40],
        ],
    ),
    Professor(
        "doc. dr. sc. Katarina Kostelić",
        ["Mon 10-12", "Wed 8-10"],
        [subjects[20], subjects[21], subjects[52]],
    ),
    Professor(
        "doc. dr. sc. Nikola Tanković",
        ["Mon 10-12", "Wed 8-10"],
        [
            subjects[23],
            subjects[24],
            subjects[33],
            subjects[34],
            subjects[55],
        ],
    ),
    Professor(
        "mag. inf. Lorena Jeger",
        ["Mon 10-12", "Wed 8-10"],
        [
            subjects[26],
            subjects[28],
        ],
    ),
    Professor(
        "izv. prof. dr. sc. Siniša Sovilj",
        ["Mon 10-12", "Wed 8-10"],
        [
            subjects[29],
            subjects[30],
            subjects[37],
        ],
    ),
    Professor(
        "dipl. ing. Gordan Krčelić",
        ["Mon 10-12", "Wed 8-10"],
        [subjects[44], subjects[45]],
    ),
    Professor(
        "dr. sc. Boris Blagonić",
        ["Mon 10-12", "Wed 8-10"],
        [subjects[46]],
    ),
    Professor(
        "izv. prof. dr. sc. Dean Sinković",
        ["Mon 10-12", "Wed 8-10"],
        [subjects[47], subjects[48]],
    ),
    Professor(
        "prof. dr. sc. Robert Zenzerović",
        ["Mon 10-12", "Wed 8-10"],
        [
            subjects[49],
            subjects[50],
            subjects[56],
            subjects[57],
        ],
    ),
]


days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
time_slots = ["8-10", "10-12", "14-16", "16-18", "18-20"]

timetable_1 = {
    classroom.name: {day: {time_slot: None for time_slot in time_slots} for day in days}
    for classroom in classrooms
}


timetable_2 = {
    classroom.name: {day: {time_slot: None for time_slot in time_slots} for day in days}
    for classroom in classrooms
}

timetable_3 = {
    classroom.name: {day: {time_slot: None for time_slot in time_slots} for day in days}
    for classroom in classrooms
}


timetable_4 = {
    classroom.name: {day: {time_slot: None for time_slot in time_slots} for day in days}
    for classroom in classrooms
}

timetable_5 = {
    classroom.name: {day: {time_slot: None for time_slot in time_slots} for day in days}
    for classroom in classrooms
}
