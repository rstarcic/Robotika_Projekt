import random

class Subject:
    def __init__(self, name):
        self.name = name
        self.scheduled = False

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
    def __init__(self, name):
        self.name = name
        self.schedule = {} 

    def is_available(self, day, time_slot):
        return (day, time_slot) not in self.schedule

    def schedule_lecture(self, professor, day, time_slot, subject):
        self.schedule[(day, time_slot)] = (professor, subject)

    def __repr__(self):
        return f"Classroom {self.name}"

# napraviti podjelu na predavaonice i labose?-
classrooms = [
    Classroom('108'),
    Classroom('109'),
    Classroom('110')
]
#podjela na predavanja i vjezbe?-
subjects = [Subject('Robotika'), Subject('NMDU'), Subject('ModSim'), Subject('APOI')]

#napraviti suprotno - kada profesor nije slobodan - ako je moguće - ne moraju biti ispunjene
#svi profesori nisu dostupni u jednom terminu
professors = [
    Professor('Dr. Smith', ['Mon 8-10'], [subjects[0]]),
    Professor('Dr. Johnson', ['Mon 8-10'], [subjects[1]]),
    Professor('Dr. Lee', ['Mon 8-10'], [subjects[2]]),
    Professor('Dr. Brown', ['Mon 8-10', 'Mon 10-12'], [subjects[3]]),
]

days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
time_slots = ['8-10', '10-12', '14-16', '16-18', '18-20']

timetable = {classroom.name: {day:{time_slot: None for time_slot in time_slots}for day in days} for classroom in classrooms}

def greedy_schedule(professors, classrooms, timetable):
    for professor in professors:
        
        available_slots = sorted(professor.available_times, key=lambda x: x)
        
        for slot in available_slots:
            day, time_slot = slot.split(' ')
            
            for subject in professor.subjects:
                if subject.scheduled:
                    continue
                
                scheduled_for_this_slot = False  
                
                for classroom in classrooms:
                    if classroom.is_available(day, time_slot):
                        timetable[classroom.name][day][time_slot] = {'professor': professor.name, 
                                                     'classroom': classroom.name, 
                                                     'subject': subject.name}
                        classroom.schedule_lecture(professor, day, time_slot, subject)
                        professor.schedule_lecture(slot)
                        subject.scheduled = True
                        print(f"Scheduled {subject.name} with {professor.name} in {classroom.name} on {slot}")
                        scheduled_for_this_slot = True
                        break
                if not scheduled_for_this_slot:
                    print(f"No classroom available for {subject.name} at {day} {time_slot}. Trying next available time slot.")
                    
                    for next_slot in available_slots:
                        if next_slot > slot:  
                            next_day, next_time_slot = next_slot.split(' ')
                            print(f"Trying to schedule {subject.name} for {professor.name} at {next_day} {next_time_slot}")
                            
                        
                            for classroom in classrooms:
                                if classroom.is_available(next_day, next_time_slot):
                                    conflict_found = False
                                    
                                    for other_day in days:
                                        for other_time_slot in time_slots:
                                            if timetable[classroom.name][other_day][other_time_slot]:
                                                other_lecture = timetable[other_day][other_time_slot]
                                                if (other_lecture['classroom'] == classroom.name and
                                                    other_lecture['professor'] != professor.name):
                                                    conflict_found = True
                                                    break
                                                
                                                if other_lecture['subject'] == subject.name:
                                                    conflict_found = True
                                                    break
                                        if conflict_found:
                                            break

                                    if not conflict_found:
                                        timetable[classroom.name][next_day][next_time_slot] = {'professor': professor.name, 
                                                                              'classroom': classroom.name, 
                                                                              'subject': subject.name}
                                        classroom.schedule_lecture(professor, next_day, next_time_slot, subject)
                                        professor.schedule_lecture(next_slot)
                                        subject.scheduled = True
                                        print(f"Scheduled {subject.name} with {professor.name} in {classroom.name} on {next_slot}")
                                        scheduled_for_this_slot = True
                                        break
                            if scheduled_for_this_slot:
                                break
                if not scheduled_for_this_slot:
                    print(f"{subject.name} could not be scheduled for {professor.name}.")
                    
#Napraviti optimizaciju tako da ne postoje preklapanja među godinama? oce rec izborni kolegiji koje slusaju 1. i 2. godina npr. -
#Da sto vise predavanja bude u pocetku tjedna? ujutro? -
#Smanjiti broj predavanja u danu? -
#Ako se radi podjela predavanja/vjezbe - staviti da prvo idu predavanja pa vjezbe (vjezbe prate predavanja?)-

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
                                    if timetable[classroom.name][day1][time_slot1] and timetable[classroom.name][day2][time_slot2]:
                                        lecture1 = timetable[classroom.name][day1][time_slot1]
                                        lecture2 = timetable[classroom.name][day2][time_slot2]
                                        
                                        if lecture1['subject'] == lecture2['subject']:
                                            continue  

                                        if professor1.is_available(time_slot2) and professor2.is_available(time_slot1):
                                            swap_lectures(timetable, professor1, professor2, day1, time_slot1, day2, time_slot2)
                                            new_cost = calculate_cost(timetable)
                                            
                                            if new_cost < best_cost:
                                                best_timetable = {day: dict(time_slot) for day, time_slot in timetable.items()}
                                                best_cost = new_cost
                                                improved = True
                                                print(f"Improved Cost: {best_cost}")
                                            
                                            swap_lectures(timetable, professor1, professor2, day1, time_slot1, day2, time_slot2, undo=True)

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

def swap_lectures(timetable, professor1, professor2, day1, time_slot1, day2, time_slot2, undo=False):
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
                if lecture and lecture['classroom'] == classroom.name:
                    print(f"  {time_slot}: {lecture['subject']} by {lecture['professor']}")
                elif not lecture or lecture['classroom'] != classroom.name:
                    print(f"  {time_slot}: No lecture scheduled")

greedy_schedule(professors, classrooms, timetable)

print("\nInitial Timetable:")
display_timetable(timetable, classrooms)

optimized_timetable = hill_climb(timetable, classrooms, professors)

print("\nOptimized Timetable:")
display_timetable(optimized_timetable, classrooms)
