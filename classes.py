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
