from data import days, time_slots


def schedule_electives(professors, classrooms, timetables):
    elective_subjects = {}
    for prof in professors:
        for subj in prof.subjects:
            if subj.is_elective:
                elective_subjects.setdefault(subj.name, []).append((subj, prof))

    elective_slots = set()
    used_slots = set()

    for name, entries in elective_subjects.items():
        prof_availabilities = [set(p.available_times) for (_, p) in entries]
        common_slots = set.intersection(*prof_availabilities)

        for slot in sorted(common_slots):
            day, time_slot = slot.split()
            if (day, time_slot) in used_slots:
                continue

            # Check that no professor has another scheduled time
            if any(slot in p.scheduled_times for (_, p) in entries):
                continue

            for classroom in classrooms:
                if not classroom.is_available(day, time_slot):
                    continue

                scheduled = False
                for subj, prof in entries:
                    for year in subj.year:
                        timetable = timetables[year - 1]
                        if timetable[classroom.name][day][time_slot] is not None:
                            break
                        timetable[classroom.name][day][time_slot] = {
                            "professor": prof.name,
                            "classroom": classroom.name,
                            "subject": subj.name,
                            "subject_type": subj.type,
                        }
                    classroom.schedule_lecture(prof, day, time_slot, subj)
                    prof.schedule_lecture(slot)
                    subj.scheduled = True

                used_slots.add((day, time_slot))
                elective_slots.add((day, time_slot))
                print(f"[Elective] {name} scheduled at {slot}")
                scheduled = True
                break

            if scheduled:
                break

    return elective_slots
