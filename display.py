from data import days, time_slots


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
