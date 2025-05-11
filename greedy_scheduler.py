from data import days, time_slots


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
