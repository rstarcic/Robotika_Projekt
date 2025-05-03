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


def sort_key(slot):
    day_order = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4}
    day_abbr, time_range = slot.split()
    start_hour = int(time_range.split("-")[0])
    return (day_order[day_abbr], start_hour)


def greedy_schedule(professors, classrooms, timetable):
    used_time_slots = set()
    for professor in professors:

        available_slots = sorted(professor.available_times, key=sort_key)
        for slot in available_slots:
            day, time_slot = slot.split(" ")

            if (day, time_slot) in used_time_slots:
                continue
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
                        classroom.schedule_lecture(professor, day, time_slot, subject)
                        professor.schedule_lecture(slot)
                        subject.scheduled = True
                        used_time_slots.add((day, time_slot))
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
                                                other_lecture = timetable[other_day][
                                                    other_time_slot
                                                ]
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
                                        used_time_slots.add((day, time_slot))
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
# Ako se radi podjela predavanja/vjezbe - staviti da prvo idu predavanja pa vjezbe (vjezbe prate predavanja?) done
def score_timetable(timetable, classrooms, professors):
    score = 0
    penalties = 0

    subject_slots = {}

    for classroom in classrooms:
        for (day, time_slot), (professor, subject) in classroom.schedule.items():
            if professor and subject:
                subject_slots[subject.name] = (day, time_slot, professor)

    for subject_name, (day, slot, professor) in subject_slots.items():
        slot_str = f"{day} {slot}"

        if slot_str not in professor.available_times:
            penalties += 15

    for subject in subject_slots:
        if "Vježbe" in subject:
            lecture_name = subject.replace("Vježbe", "Predavanje").strip()
            if lecture_name in subject_slots:
                lec_day, lec_slot, _ = subject_slots[lecture_name]
                ex_day, ex_slot, ex_prof = subject_slots[subject]

                if ex_prof is None:
                    continue

                lec_index = (days.index(lec_day), time_slots.index(lec_slot))
                ex_index = (days.index(ex_day), time_slots.index(ex_slot))

                if ex_index > lec_index:
                    score += 10
                else:
                    penalties += 10

                for prof in professors:
                    if (
                        prof.name == ex_prof.name
                        and f"{ex_day} {ex_slot}" not in prof.available_times
                    ):
                        penalties += 5
    return score - penalties


def clone_classrooms(classrooms):
    cloned = []
    for c in classrooms:
        new_classroom = Classroom(c.name, c.is_lab)
        new_classroom.schedule = {
            (day, time_slot): (
                Professor(p.name, p.available_times[:], p.subjects),
                subj,
            )
            for (day, time_slot), (p, subj) in c.schedule.items()
        }
        cloned.append(new_classroom)
    return cloned


def clone_timetable(classrooms):
    timetable = {
        c.name: {day: {slot: None for slot in time_slots} for day in days}
        for c in classrooms
    }
    for c in classrooms:
        for (day, slot), val in c.schedule.items():
            if val is None:
                continue
            prof, subj = val
            if prof is None or subj is None:
                continue
            timetable[c.name][day][slot] = {
                "professor": prof.name,
                "classroom": c.name,
                "subject": subj.name,
            }
    return timetable


def hill_climb(initial_timetable, classrooms, professors, max_iterations=1000):
    current_classrooms = clone_classrooms(classrooms)
    current_timetable = clone_timetable(current_classrooms)
    current_score = score_timetable(current_timetable, current_classrooms, professors)
    print("Original timetable score:", current_score)

    for _ in range(max_iterations):
        improved = False
        best_score = current_score
        best_classrooms = clone_classrooms(current_classrooms)

        for subject in [
            s for p in professors for s in p.subjects if "Vježbe" in s.name
        ]:
            lec_name = subject.name.replace("Vježbe", "Predavanje").strip()

            lec_time = None
            for c in current_classrooms:
                for (day, slot), (p, s) in c.schedule.items():
                    if s.name == lec_name:
                        lec_time = (day, slot)
                        break
                if lec_time:
                    break

            if not lec_time:
                continue

            lec_day_i = days.index(lec_time[0])
            lec_slot_i = time_slots.index(lec_time[1])
            ex_day, ex_slot, ex_prof, old_classroom = None, None, None, None

            for c in current_classrooms:
                for (d, s), (p, subj) in list(c.schedule.items()):
                    if subj.name == subject.name:
                        ex_day, ex_slot = d, s
                        ex_prof = p
                        old_classroom = c
                        del c.schedule[(d, s)]
                        break
                if ex_day:
                    break

            professor = ex_prof
            if professor is None:
                continue

            slot_moved = False
            for day_i in range(lec_day_i, len(days)):
                for slot_i in range(len(time_slots)):
                    if day_i == lec_day_i and slot_i <= lec_slot_i:
                        continue

                    new_day = days[day_i]
                    new_slot = time_slots[slot_i]
                    new_slot_str = f"{new_day} {new_slot}"

                    for classroom in current_classrooms:

                        if not classroom.is_lab or not classroom.is_available(
                            new_day, new_slot
                        ):
                            continue

                        classroom.schedule[(new_day, new_slot)] = (professor, subject)

                        new_timetable = clone_timetable(current_classrooms)
                        new_score = score_timetable(
                            new_timetable, current_classrooms, professors
                        )

                        if new_score > best_score:
                            for bc in best_classrooms:
                                if (ex_day, ex_slot) in bc.schedule:
                                    p, s = bc.schedule[(ex_day, ex_slot)]
                                    if s.name == subject.name:
                                        del bc.schedule[(ex_day, ex_slot)]
                                        break

                            best_score = new_score
                            best_classrooms = clone_classrooms(current_classrooms)
                            improved = True
                        else:
                            del classroom.schedule[(new_day, new_slot)]
                    if slot_moved:
                        break
                if slot_moved:
                    break

            if not slot_moved and ex_day:
                old_classroom.schedule[(ex_day, ex_slot)] = (professor, subject)

        if not improved:
            break

        current_classrooms = best_classrooms
        current_timetable = clone_timetable(current_classrooms)
        current_score = best_score
    print("New cost:", current_score)

    return current_timetable


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


html_content_timetable = generate_html_single_table(timetable, classrooms)

with open("timetable.html", "w", encoding="utf-8") as f:
    f.write(html_content_timetable)

print("HTML file generated: timetable.html")


html_content_optimized_timetable = generate_html_single_table(
    optimized_timetable, classrooms
)

with open("optimized_timetable.html", "w", encoding="utf-8") as f:
    f.write(html_content_optimized_timetable)

print("HTML file generated: optimized_timetable.html")
