from classes import Classroom, Subject, Professor

classrooms = [
    Classroom("108", False),
    Classroom("109", False),
    Classroom("110", True),
    Classroom("132", False),
]

subjects = [
    Subject("Robotika - Predavanje"),
    Subject("Robotika - Vježbe"),
    Subject("NMDU - Predavanje"),
    Subject("NMDU - Vježbe"),
    Subject("ModSim - Predavanje"),
    Subject("ModSim - Vježbe"),
    Subject("APOI - Predavanje"),
    Subject("APOI - Vježbe"),
    Subject("IT management - Predavanje"),
    Subject("IT management - Vježbe"),
]

professors = [
    Professor(
        "Dr. Etinger",
        ["Thu 8-10", "Fri 8-10"],
        [subjects[8]],
    ),
    Professor("Dr. Sajina", ["Tue 8-10", "Fri 10-12"], [subjects[9]]),
    Professor(
        "Dr. Johnson",
        ["Mon 8-10", "Tue 14-16", "Wed 14-16"],
        [subjects[0], subjects[1]],
    ),
    Professor(
        "Dr. Lee",
        ["Tue 8-10", "Tue 10-12", "Wed 14-16", "Wed 10-12", "Tue 8-10", "Fri 10-12"],
        [subjects[2]],
    ),
    Professor(
        "Dr. Brown",
        ["Mon 8-10", "Mon 10-12"],
        [subjects[4], subjects[5]],
    ),
    Professor("Dr. White", ["Thu 8-10"], [subjects[1]]),
    Professor("Dr. McCalister", ["Tue 8-10"], [subjects[3]]),
]

days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
time_slots = ["8-10", "10-12", "14-16", "16-18", "18-20"]

timetable = {
    classroom.name: {day: {time_slot: None for time_slot in time_slots} for day in days}
    for classroom in classrooms
}
