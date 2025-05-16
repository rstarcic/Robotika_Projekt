# main.py
from classes import Professor
from data import (
    classrooms,
    professors,
    timetable_1,
    timetable_2,
    timetable_3,
    timetable_4,
    timetable_5,
)
from greedy_scheduler import greedy_schedule
from hill_climb_optimizer import hill_climb
from display import display_timetable
from html_and_csv_export import generate_html_single_table


def main():
    timetables = [timetable_1, timetable_2, timetable_3, timetable_4, timetable_5]
    for year in range(1, 6):
        prof_subj = []
        for prof in professors:
            relevant_subjects = [s for s in prof.subjects if year in s.year]
            if relevant_subjects:
                prof_subj.append(
                    Professor(prof.name, prof.available_times, relevant_subjects)
                )

        # Greedy zakazivanje
        greedy_schedule(prof_subj, classrooms, timetables[year - 1])

        print("\nPočetni raspored:")
        display_timetable(timetables[year - 1], classrooms)

        # Optimizacija rasporeda
        optimized_timetable = hill_climb(timetables[year - 1], classrooms, prof_subj)

        print("\nOptimizirani raspored:")
        display_timetable(optimized_timetable, classrooms)

        # Izvoz HTML-a
        html_content = generate_html_single_table(timetables[year - 1], classrooms)
        with open(f"{year}_godina_timetable.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Generiran HTML: {year}_godina_timetable.html")

        html_optimized = generate_html_single_table(optimized_timetable, classrooms)
        with open(
            f"{year}_godina_optimized_timetable.html", "w", encoding="utf-8"
        ) as f:
            f.write(html_optimized)
        print(f"Generiran HTML: {year}_godina_optimized_timetable.html")


if __name__ == "__main__":
    main()
