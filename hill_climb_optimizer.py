from data import days, time_slots
from classes import Classroom, Professor


# Napraviti optimizaciju tako da ne postoje preklapanja među godinama? oce rec izborni kolegiji koje slusaju 1. i 2. godina npr.
# Da sto vise predavanja bude u pocetku tjedna? ujutro?
# Smanjiti broj predavanja u danu?
# Da se sto vise predavanja stavi u istu predavaonu?
# Ako se radi podjela predavanja/vjezbe - staviti da prvo idu predavanja pa vjezbe (vjezbe prate predavanja?) done
def score_timetable(timetable, classrooms, professors, elective_slots):
    if elective_slots is None:
        elective_slots = set()
        print("bla", elective_slots)
    score = 0
    penalties = 0
    subject_slots = {}
    for classroom in classrooms:
        for (day, time_slot), (professor, subject) in classroom.schedule.items():
            if professor and subject:
                key = (subject.name, subject.type)
                subject_slots[key] = (day, time_slot, professor, subject)

                if (day, time_slot) in elective_slots:
                    print("bla", elective_slots)
                    if not subject.is_elective:
                        penalties += 1000  # Zabranjeno za obavezne
                    else:
                        score += 40  # Izborni u svom slotu – OK
                else:
                    score += 40  # Sve ostalo normalno boduj

    for (name, type_), (day, slot, professor, subject) in subject_slots.items():
        slot_str = f"{day} {slot}"

        if slot_str not in professor.available_times:
            penalties += 20
        else:
            score += 10

    for (name, type_), (ex_day, ex_slot, ex_prof, ex_subject) in subject_slots.items():
        if ex_subject.type == "Vježbe":
            lecture_key = (ex_subject.name, "Predavanje")
            if lecture_key in subject_slots:
                lec_day, lec_slot, lec_prof, lec_subject = subject_slots[lecture_key]

                lec_index = (days.index(lec_day), time_slots.index(lec_slot))
                ex_index = (days.index(ex_day), time_slots.index(ex_slot))

                if ex_index > lec_index:
                    score += 50  # Reward: vježbe come after predavanje
                else:
                    penalties += 40  # Penalty: bad order

                # Extra penalty if professor not available for vježbe
                ex_slot_str = f"{ex_day} {ex_slot}"
                if ex_slot_str not in ex_prof.available_times:
                    penalties += 5

    day_counts = {day: 0 for day in days}
    for (name, type_), (day, slot, professor, subject) in subject_slots.items():
        day_counts[day] += 1
    for day, count in day_counts.items():
        if count == 0:
            penalties += 5  # blaga kazna za prazan dan
        elif count == 1:
            score += 3  # ok, samo jedno predavanje
        elif count == 2:
            score += 6  # optimalno
        elif count == 3:
            score += 2  # još ok
        else:
            penalties += (count - 2) * 100  # jako penaliziraj pretrpane dane

    for (name, type_), (day, slot, professor, subject) in subject_slots.items():
        if slot == "8-10":
            score += 5
        elif slot == "10-12":
            score += 3
        elif slot == "14-16":
            penalties += 2
        elif slot in ["16-18", "18-20"]:
            penalties += 4

    return score - penalties


def clone_classrooms(classrooms):
    cloned = []
    for c in classrooms:
        new_classroom = Classroom(c.name, c.is_lab)
        new_classroom.schedule = {
            (day, time_slot): (
                Professor(p.name, p.available_times[:], list(p.subjects)),
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
                "subject_type": subj.type,
            }
    return timetable


def hill_climb(
    initial_timetable, classrooms, professors, elective_slots=None, max_iterations=1000
):
    current_classrooms = clone_classrooms(classrooms)
    current_timetable = clone_timetable(current_classrooms)
    current_score = score_timetable(
        current_timetable, current_classrooms, professors, elective_slots=elective_slots
    )
    print("Original timetable score:", current_score)

    if elective_slots is None:
        print("Prazni electives")
        elective_slots = set()
    else:
        print("LLL", elective_slots)

    for _ in range(max_iterations):
        improved = False
        best_score = current_score
        best_classrooms = clone_classrooms(current_classrooms)

        for subject in [
            s for p in professors for s in p.subjects if s.type == "Vježbe"
        ]:

            lec_time = None
            for c in current_classrooms:
                for (day, slot), (p, s) in c.schedule.items():
                    if s.name == subject.name and s.type == "Predavanje":
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
                    if subj.name == subject.name and subj.type == "Vježbe":
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

                    if (new_day, new_slot) in elective_slots:
                        continue

                    for classroom in current_classrooms:

                        if not classroom.is_lab or not classroom.is_available(
                            new_day, new_slot
                        ):
                            continue

                        professor_busy_elsewhere = any(
                            (new_day, new_slot) in c.schedule
                            and c.schedule[(new_day, new_slot)][0].name
                            == professor.name
                            for c in current_classrooms
                        )
                        if professor_busy_elsewhere:
                            continue
                        time_slot_occupied = any(
                            (new_day, new_slot) in c.schedule
                            for c in current_classrooms
                        )
                        if time_slot_occupied:
                            continue

                        classroom.schedule[(new_day, new_slot)] = (professor, subject)

                        new_timetable = clone_timetable(current_classrooms)
                        new_score = score_timetable(
                            new_timetable,
                            current_classrooms,
                            professors,
                            elective_slots=elective_slots,
                        )

                        if new_score > best_score:
                            for bc in best_classrooms:
                                if (ex_day, ex_slot) in bc.schedule:
                                    p, s = bc.schedule[(ex_day, ex_slot)]
                                    if s.name == subject.name and s.type == "Vježbe":
                                        del bc.schedule[(ex_day, ex_slot)]
                                        break

                            best_score = new_score
                            best_classrooms = clone_classrooms(current_classrooms)
                            improved = True
                            slot_moved = True
                        else:
                            del classroom.schedule[(new_day, new_slot)]
                    if slot_moved:
                        break
                if slot_moved:
                    break

            if not slot_moved and ex_day:
                old_classroom.schedule[(ex_day, ex_slot)] = (professor, subject)

        current_classrooms = best_classrooms
        current_timetable = clone_timetable(current_classrooms)
        current_score = best_score

        for c in current_classrooms:
            for lect in list(c.schedule.items()):
                this_year = False
                for professor in professors:
                    if lect[1][1] in professor.subjects:
                        this_year = True
                if not this_year and lect[0] in c.schedule.keys():
                    print("brisem", lect)
                    del c.schedule[lect[0]]

        current_timetable = clone_timetable(current_classrooms)
    print("New cost:", current_score)

    return current_timetable
