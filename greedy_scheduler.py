from data import days, time_slots


def sort_key(slot):
    day_order = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4}
    day_abbr, time_range = slot.split()
    start_hour = int(time_range.split("-")[0])
    return (day_order[day_abbr], start_hour)


def greedy_schedule(professors, classrooms, timetable, elective_slots=None):

    used_time_slots = set()

    if elective_slots is None:
        elective_slots = set()

    for professor in professors:

        available_slots = sorted(professor.available_times, key=sort_key)
        for subject in professor.subjects:
            if subject.scheduled:
                continue

            scheduled_for_this_subject = False

            # Try preferred time slots first
            for slot in available_slots:
                day, time_slot = slot.split(" ")

                if (day, time_slot) in elective_slots:
                    continue  # skip slots used by electives
                if (day, time_slot) in used_time_slots:
                    continue
                if not professor.is_available(slot):
                    continue

                for classroom in classrooms:
                    if classroom.is_available(day, time_slot):
                        if subject.type == "Vježbe" and not classroom.is_lab:
                            continue
                        if subject.type == "Predavanje" and classroom.is_lab:
                            continue

                        timetable[classroom.name][day][time_slot] = {
                            "professor": professor.name,
                            "classroom": classroom.name,
                            "subject": subject.name,
                            "subject_type": subject.type,
                        }
                        classroom.schedule_lecture(
                            professor, day, time_slot, subject
                        )  # treba debugirati
                        professor.schedule_lecture(slot)
                        subject.scheduled = True
                        used_time_slots.add((day, time_slot))
                        print(
                            f"Scheduled {subject.name} with {professor.name} in {classroom.name} on {slot}"
                        )
                        scheduled_for_this_subject = True
                        break

                if scheduled_for_this_subject:
                    break

            # If not scheduled in preferred slots, find the first available slot anywhere
            if not scheduled_for_this_subject:
                print(
                    f"No available preferred time slot for {subject.name}. Trying any free slot..."
                )

                for day in days:
                    for time_slot in time_slots:
                        if (day, time_slot) in elective_slots:
                            continue
                        if (day, time_slot) in used_time_slots:
                            continue

                        for classroom in classrooms:
                            if not classroom.is_available(day, time_slot):
                                continue
                            if subject.type == "Vježbe" and not classroom.is_lab:
                                continue
                            if subject.type == "Predavanje" and classroom.is_lab:
                                continue

                            timetable[classroom.name][day][time_slot] = {
                                "professor": professor.name,
                                "classroom": classroom.name,
                                "subject": subject.name,
                                "subject_type": subject.type,
                            }
                            classroom.schedule_lecture(
                                professor, day, time_slot, subject
                            )
                            professor.schedule_lecture(f"{day} {time_slot}")
                            subject.scheduled = True
                            used_time_slots.add((day, time_slot))
                            print(
                                f"[Fallback] Scheduled {subject.name} with {professor.name} in {classroom.name} on {day} {time_slot}"
                            )
                            scheduled_for_this_subject = True
                            break

                        if scheduled_for_this_subject:
                            break
                    if scheduled_for_this_subject:
                        break

            if not scheduled_for_this_subject:
                print(f"{subject.name} could not be scheduled for {professor.name}.")
