import random


class Subject:
    def __init__(self, name):
        self.name = name
        self.scheduled = False
        # self.year = year

    def __repr__(self):
        return self.name


class Professor:
    def __init__(self, name, available_times, subjects):
        self.name = name
        self.available_times = available_times
        self.scheduled_times = []
        self.subjects = subjects

    def is_available(self, slot):
        return slot in self.available_times and slot not in self.scheduled_times

    def schedule_lecture(self, slot):
        self.scheduled_times.append(slot)

    def __repr__(self):
        return f"Professor {self.name}"


class Classroom:
    def __init__(self, name, is_lab):
        self.name = name
        self.schedule = {}
        self.is_lab = is_lab

    def is_available(self, day, time_slot):
        return (day, time_slot) not in self.schedule

    def schedule_lecture(self, professor, day, time_slot, subject):
        self.schedule[(day, time_slot)] = (professor, subject)

    def __repr__(self):
        return f"Classroom {self.name}"


# napraviti podjelu na predavaonice i labose? - done
classrooms = [
    Classroom("108", False),
    Classroom("109", False),
    Classroom("110", True),
    Classroom("132", False),
]
# podjela na predavanja i vjezbe? - done
subjects = [
    Subject("Robotika - Predavanje"),
    Subject("Robotika - Vježbe"),
    Subject("NMDU - Predavanje"),
    Subject("NMDU - Vježbe"),
    Subject("ModSim - Predavanje"),
    Subject("ModSim - Vježbe"),
    Subject("APOI - Predavanje"),
    Subject("APOI - Vježbe"),
]


professors = [
    Professor(
        "Dr. Johnson",
        ["Mon 8-10", "Tue 14-16", "Wed 14-16"],
        [subjects[0], subjects[1]],
    ),
    Professor("Dr. Lee", ["Mon 8-10"], [subjects[2]]),
    Professor(
        "Dr. Brown",
        ["Mon 8-10", "Mon 10-12"],
        [subjects[4], subjects[5]],
    ),
    # Professor("Dr. White", ["Thu 8-10"], [subjects[1]]),
    Professor("Dr. McCalister", ["Wed 8-10"], [subjects[3]]),
    # Professor("Dr. Taylor",["Thu 8-10", "Fri 10-12"],[subjects_vjezbe[0], subjects_vjezbe[3]],),
]

days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
time_slots = ["8-10", "10-12", "14-16", "16-18", "18-20"]

timetable = {
    classroom.name: {day: {time_slot: None for time_slot in time_slots} for day in days}
    for classroom in classrooms
}


def greedy_schedule(professors, classrooms, timetable):
    for phase in ["Predavanje", "Vježbe"]:
        for professor in professors:

            available_slots = sorted(professor.available_times, key=lambda x: x)

            for slot in available_slots:
                day, time_slot = slot.split(" ")

                for subject in professor.subjects:
                    if subject.scheduled:
                        continue
                    if not professor.is_available(slot):
                        continue

                    scheduled_for_this_slot = False

                    for classroom in classrooms:
                        if classroom.is_available(day, time_slot):
                            if classroom.is_available(day, time_slot):
                                if "Vježbe" in subject.name and not classroom.is_lab:
                                    continue
                                if not "Vježbe" in subject.name and classroom.is_lab:
                                    continue

                            timetable[classroom.name][day][time_slot] = {
                                "professor": professor.name,
                                "classroom": classroom.name,
                                "subject": subject.name,
                            }
                            classroom.schedule_lecture(
                                professor, day, time_slot, subject
                            )
                            professor.schedule_lecture(slot)
                            subject.scheduled = True
                            print(
                                f"Scheduled {subject.name} with {professor.name} in {classroom.name} on {slot}"
                            )
                            scheduled_for_this_slot = True
                            break
                    if not scheduled_for_this_slot:
                        print(
                            f"No classroom available for {subject.name} at {day} {time_slot}. Trying next available time slot."
                        )

                        for next_slot in available_slots:
                            if next_slot > slot:
                                next_day, next_time_slot = next_slot.split(" ")
                                print(
                                    f"Trying to schedule {subject.name} for {professor.name} at {next_day} {next_time_slot}"
                                )

                                for classroom in classrooms:
                                    if classroom.is_available(next_day, next_time_slot):
                                        conflict_found = False

                                        for other_day in days:
                                            for other_time_slot in time_slots:
                                                if timetable[classroom.name][other_day][
                                                    other_time_slot
                                                ]:
                                                    other_lecture = timetable[
                                                        other_day
                                                    ][other_time_slot]
                                                    if (
                                                        other_lecture["classroom"]
                                                        == classroom.name
                                                        and other_lecture["professor"]
                                                        != professor.name
                                                    ):
                                                        conflict_found = True
                                                        break

                                                    if (
                                                        other_lecture["subject"]
                                                        == subject.name
                                                    ):
                                                        conflict_found = True
                                                        break
                                            if conflict_found:
                                                break

                                        if not conflict_found:
                                            timetable[classroom.name][next_day][
                                                next_time_slot
                                            ] = {
                                                "professor": professor.name,
                                                "classroom": classroom.name,
                                                "subject": subject.name,
                                            }
                                            classroom.schedule_lecture(
                                                professor,
                                                next_day,
                                                next_time_slot,
                                                subject,
                                            )
                                            professor.schedule_lecture(next_slot)
                                            subject.scheduled = True
                                            print(
                                                f"Scheduled {subject.name} with {professor.name} in {classroom.name} on {next_slot}"
                                            )
                                            scheduled_for_this_slot = True
                                            break
                                if scheduled_for_this_slot:
                                    break
                    if not scheduled_for_this_slot:
                        print(
                            f"{subject.name} could not be scheduled for {professor.name}."
                        )


# Napraviti optimizaciju tako da ne postoje preklapanja među godinama? oce rec izborni kolegiji koje slusaju 1. i 2. godina npr.
# Da sto vise predavanja bude u pocetku tjedna? ujutro?
# Smanjiti broj predavanja u danu?
# Da se sto vise predavanja stavi u istu predavaonu?
# Ako se radi podjela predavanja/vjezbe - staviti da prvo idu predavanja pa vjezbe (vjezbe prate predavanja?)


def hill_climb(timetable, classrooms, professors):
    current_cost = calculate_cost(timetable)
    print(f"Initial Cost: {current_cost}")

    improved = True
    while improved:
        improved = False
        best_timetable = {day: dict(time_slot) for day, time_slot in timetable.items()}

        best_cost = current_cost

        for professor1 in professors:
            for professor2 in professors:
                if professor1 == professor2:
                    continue

                for day1 in days:
                    for time_slot1 in time_slots:
                        for day2 in days:
                            for time_slot2 in time_slots:
                                for classroom in classrooms:
                                    if (
                                        timetable[classroom.name][day1][time_slot1]
                                        and timetable[classroom.name][day2][time_slot2]
                                    ):
                                        lecture1 = timetable[classroom.name][day1][
                                            time_slot1
                                        ]
                                        lecture2 = timetable[classroom.name][day2][
                                            time_slot2
                                        ]

                                        if lecture1["subject"] == lecture2["subject"]:
                                            continue

                                        if professor1.is_available(
                                            time_slot2
                                        ) and professor2.is_available(time_slot1):
                                            swap_lectures(
                                                timetable,
                                                professor1,
                                                professor2,
                                                day1,
                                                time_slot1,
                                                day2,
                                                time_slot2,
                                            )
                                            new_cost = calculate_cost(timetable)

                                            if new_cost < best_cost:
                                                best_timetable = {
                                                    day: dict(time_slot)
                                                    for day, time_slot in timetable.items()
                                                }
                                                best_cost = new_cost
                                                improved = True
                                                print(f"Improved Cost: {best_cost}")

                                            swap_lectures(
                                                timetable,
                                                professor1,
                                                professor2,
                                                day1,
                                                time_slot1,
                                                day2,
                                                time_slot2,
                                                undo=True,
                                            )

        timetable = best_timetable
        current_cost = best_cost

    print(f"Optimized Cost: {current_cost}")
    return timetable


def calculate_cost(timetable):
    unassigned_lectures = 0

    for classroom in classrooms:
        for day in days:
            for time_slot in time_slots:
                if not timetable[classroom.name][day][time_slot]:
                    unassigned_lectures += 1

    return unassigned_lectures


def swap_lectures(
    timetable, professor1, professor2, day1, time_slot1, day2, time_slot2, undo=False
):
    lecture1 = timetable[day1][time_slot1]
    lecture2 = timetable[day2][time_slot2]

    if undo:
        timetable[day1][time_slot1] = lecture1
        timetable[day2][time_slot2] = lecture2
    else:
        timetable[day1][time_slot1] = lecture2
        timetable[day2][time_slot2] = lecture1


def display_timetable(timetable, classrooms):
    print("\nCollege Timetable:")
    for classroom in classrooms:
        print(f"\n{classroom.name}:")
        for day in days:
            print(day)
            for time_slot in time_slots:
                lecture = timetable[classroom.name][day][time_slot]
                if lecture and lecture["classroom"] == classroom.name:
                    print(
                        f"  {time_slot}: {lecture['subject']} by {lecture['professor']}"
                    )
                elif not lecture or lecture["classroom"] != classroom.name:
                    print(f"  {time_slot}: No lecture scheduled")


greedy_schedule(professors, classrooms, timetable)

print("\nInitial Timetable:")
display_timetable(timetable, classrooms)

optimized_timetable = hill_climb(timetable, classrooms, professors)

print("\nOptimized Timetable:")
display_timetable(optimized_timetable, classrooms)


def generate_html_single_table(timetable, classrooms):
    html = """
    <html>
    <head>
        <style>
            table { border-collapse: collapse; width: 100%; margin-bottom: 50px; }
            th, td { border: 1px solid black; padding: 8px; text-align: center; vertical-align: top; }
            th { background-color: #f2f2f2; }
            h1 { margin-top: 20px; }
        </style>
        <title>College Timetable</title>
    </head>
    <body>
        <h1>College Timetable (All Classrooms)</h1>
        <table>
            <tr>
                <th>Time Slot</th>
    """

    # Zaglavlja dana
    for day in days:
        html += f"<th>{day}</th>"
    html += "</tr>"

    # Redovi za svaki timeslot
    for time_slot in time_slots:
        html += f"<tr><td>{time_slot}</td>"

        for day in days:
            cell_content = ""
            for classroom in classrooms:
                lecture = timetable[classroom.name][day][time_slot]
                if lecture and lecture["classroom"] == classroom.name:
                    subject = lecture["subject"]
                    professor = lecture["professor"]
                    classroom_name = classroom.name
                    # Složimo tekst za jednu učionicu
                    cell_content += f"<strong>{classroom_name}</strong><br>{professor}<br>{subject}<br><br>"

            if cell_content == "":
                cell_content = "Empty"

            html += f"<td>{cell_content}</td>"
        html += "</tr>"

    html += """
        </table>
    </body>
    </html>
    """

    return html


html_content = generate_html_single_table(timetable, classrooms)

with open("timetable.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML file generated: timetable.html")
