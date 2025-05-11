# main.py
from classes import Professor
from data import classrooms, professors, timetable_1, timetable_2
from greedy_scheduler import greedy_schedule
from hill_climb_optimizer import hill_climb
from display import display_timetable
from html_and_csv_export import generate_html_single_table


def main():
    timetables=[timetable_1, timetable_2]
    for year in range(1,3):
        prof_subj=[]
        for prof in professors:
            if year in prof.subjects:
                prof_subj.append(Professor(prof.name, prof.available_times, prof.subjects[year]))
        
        # Greedy zakazivanje
        greedy_schedule(prof_subj, classrooms, timetables[year-1])

        print("\nPočetni raspored:")
        display_timetable(timetables[year-1], classrooms)

        # Optimizacija rasporeda
        optimized_timetable = hill_climb(timetables[year-1], classrooms, prof_subj)

        print("\nOptimizirani raspored:")
        display_timetable(optimized_timetable, classrooms)

        # Izvoz HTML-a
        html_content = generate_html_single_table(timetables[year-1], classrooms)
        with open(f"timetable_{year}.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Generiran HTML: timetable_{year}.html")

        html_optimized = generate_html_single_table(optimized_timetable, classrooms)
        with open(f"optimized_timetable_{year}.html", "w", encoding="utf-8") as f:
            f.write(html_optimized)
        print(f"Generiran HTML: optimized_timetable_{year}.html")

        #Izvoz csv
        with open(f"timetable_{year}.csv", 'w') as f:  
            for key, value in timetables[year-1].items():
                f.write(str([key, value]))
        
        with open(f"optimised_timetable_{year}.csv", 'w') as f:  
            for key, value in optimized_timetable.items():
                f.write(str([key, value]))
    

if __name__ == "__main__":
    main()
