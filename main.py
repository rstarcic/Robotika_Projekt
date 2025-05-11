# main.py

from data import classrooms, professors, timetable
from greedy_scheduler import greedy_schedule
from hill_climb_optimizer import hill_climb
from display import display_timetable
from html_and_csv_export import generate_html_single_table


def main():
    # Greedy zakazivanje
    greedy_schedule(professors, classrooms, timetable)

    print("\nPočetni raspored:")
    display_timetable(timetable, classrooms)

    # Optimizacija rasporeda
    optimized_timetable = hill_climb(timetable, classrooms, professors)

    print("\nOptimizirani raspored:")
    display_timetable(optimized_timetable, classrooms)

    # Izvoz HTML-a
    html_content = generate_html_single_table(timetable, classrooms)
    with open("timetable.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Generiran HTML: timetable.html")

    html_optimized = generate_html_single_table(optimized_timetable, classrooms)
    with open("optimized_timetable.html", "w", encoding="utf-8") as f:
        f.write(html_optimized)
    print("Generiran HTML: optimized_timetable.html")


if __name__ == "__main__":
    main()
