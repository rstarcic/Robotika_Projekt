from data import days, time_slots


def schedule_electives(professors, classrooms, timetables):
    elective_subjects = {}
    for prof in professors:
        for subj in prof.subjects:
            if subj.is_elective:
                elective_subjects.setdefault(subj.name, []).append((subj, prof))

    elective_slots = {year: set() for year in range(1, 6)}

    used_slots = set()

    for name, entries in elective_subjects.items():
        for subj, prof in entries:
            scheduled = False

            # Probaj prvo termine koje profesor želi
            preferred_slots = [
                slot
                for slot in prof.available_times
                if slot not in prof.scheduled_times
            ]

            # Ako nema definiranih termina, koristi sve termine u tjednu
            if not preferred_slots:
                print(
                    f"[Elective WARNING] '{name}' nema definiranih slobodnih termina za {prof.name}, pokušavam bilo koji..."
                )
                preferred_slots = [f"{d} {t}" for d in days for t in time_slots]

            for slot in preferred_slots:
                day, time_slot = slot.split()
                if (day, time_slot) in used_slots:
                    continue

                for classroom in classrooms:
                    if not classroom.is_available(day, time_slot):
                        continue

                    # Zakazivanje u sve godine kojima predmet pripada
                    can_schedule = True
                    for year in subj.year:
                        timetable = timetables[year - 1]
                        if timetable[classroom.name][day][time_slot] is not None:
                            can_schedule = False
                            break

                    if not can_schedule:
                        continue

                    for year in subj.year:
                        timetable = timetables[year - 1]
                        timetable[classroom.name][day][time_slot] = {
                            "professor": prof.name,
                            "classroom": classroom.name,
                            "subject": subj.name,
                            "subject_type": subj.type,
                        }

                    classroom.schedule_lecture(prof, day, time_slot, subj)
                    prof.schedule_lecture(slot)
                    subj.scheduled = True
                    for year in subj.year:
                        elective_slots[year].add((day, time_slot))

                    used_slots.add((day, time_slot))

                    print(f"[Elective] {name} scheduled at {slot} by {prof.name}")
                    scheduled = True
                    break  # prekini petlju po učionicama

                if scheduled:
                    break  # prekini petlju po terminima

            if not scheduled:
                print(
                    f"[Elective FAIL] Nije moguće zakazati '{name}' za profesora {prof.name}"
                )

    return elective_slots
