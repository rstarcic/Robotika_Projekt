from data import days, time_slots


def clean_professor_name(full_name):
    titles = [
        "prof. dr. sc. ",
        "izv. prof. dr. sc. ",
        "doc. dr. sc. ",
        "dr. sc. ",
        "mag. inf. ",
        "dipl. ing.",
        "izv.",
        "mr. sc.",
        "mag. edu. math.",
    ]
    for title in titles:
        full_name = full_name.replace(title, "")
    return full_name.strip()


def generate_html_single_table(
    timetable, classrooms, elective_names=None, year_number=1
):
    if elective_names is None:
        elective_names = set()

    classroom_names = sorted({c.name for c in classrooms})
    classroom_colors = [
        "#e6f7ff",
        "#d9fdd3",
        "#fff3cd",
        "#fce4ec",
        "#e1bee7",
        "#d1c4e9",
    ]
    day_translation = {
        "Mon": "Ponedjeljak",
        "Tue": "Utorak",
        "Wed": "Srijeda",
        "Thu": "Četvrtak",
        "Fri": "Petak",
    }

    html = f"""<!DOCTYPE html>
<html lang="hr">
<head>
    <meta charset="UTF-8">
    <title>Raspored za {year_number}. godinu (2024./2025.)</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f4;
            padding: 20px;
        }}

        h1, h2 {{
            text-align: center;
            margin: 0;
        }}

        h1 {{
            font-size: 28px;
            color: #333;
        }}

        h2 {{
            font-size: 18px;
            color: #777;
            margin-bottom: 20px;
        }}

        .controls {{
            text-align: center;
            margin: 20px 0;
        }}

        .controls button {{
            background-color: #494C4F;
            border: none;
            color: white;
            padding: 10px 16px;
            font-size: 14px;
            margin: 0 10px;
            border-radius: 6px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }}

        .controls button:hover {{
            background-color: #53595E;
        }}


        .legend {{
            display: flex;
            justify-content: center;
            gap: 16px;
            font-size: 14px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .box {{
            width: 18px;
            height: 18px;
            border-radius: 4px;
            border: 1px solid #ccc;
        }}

        .hidden {{ display: none; }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 0 8px rgba(0,0,0,0.1);
        }}

        th, td {{
            border: 1px solid #ccc;
            padding: 10px;
            text-align: center;
            vertical-align: top;
            font-size: 13px;
        }}

        th {{
            background-color: #eaeaea;
            color: #333;
        }}

        td div {{
            margin-bottom: 6px;
            padding: 6px;
            border-radius: 6px;
        }}

        td:hover {{
            background-color: #f0f8ff;
        }}

        .lecture.type-mode {{ background-color: #1e90ff; color: white; }}
        .exercise.type-mode {{ background-color: #00b894; color: white; }}
        .elective.type-mode {{ background-color: #f39c12; color: white; }}
        .elective.lecture.type-mode {{ background-color: #f1c40f; color: black; }}
        .elective.exercise.type-mode {{ background-color: #ffeccd; color: black; }}
    """

    # Boje po učionici
    for i, name in enumerate(classroom_names):
        color = classroom_colors[i % len(classroom_colors)]
        html += f".classroom-{name.replace(' ', '_')}.room-mode {{ background-color: {color}; }}\n"

    html += f"""
</style>
</head>
<body>
    <h1>Raspored za {year_number}. godinu</h1>
    <h2>Akademska godina 2024./2025.</h2>

    <div class="controls">
        <button onclick="setColorMode('type')"> Po tipu nastave</button>
        <button onclick="setColorMode('room')"> Po učionici</button>
    </div>

    <div class="legend" id="legend-type">
        <div class="legend-item"><div class="box" style="background:#1e90ff"></div> Predavanje</div>
        <div class="legend-item"><div class="box" style="background:#00b894"></div> Vježbe</div>
        <div class="legend-item"><div class="box" style="background:#f39c12"></div> Izborni kolegij</div>
        <div class="legend-item"><div class="box" style="background:#ffeccd"></div> Izborne vježbe</div>
    </div>

    <div class="legend hidden" id="legend-room">
    """

    for i, name in enumerate(classroom_names):
        color = classroom_colors[i % len(classroom_colors)]
        html += f'<div class="legend-item"><div class="box" style="background:{color}"></div> Učionica {name}</div>\n'

    html += "</div><table><tr><th>Vrijeme</th>"

    for day in days:
        html += f"<th>{day_translation.get(day, day)}</th>"

    html += "</tr>"

    for time_slot in time_slots:
        html += f"<tr><td><strong>{time_slot}</strong></td>"
        for day in days:
            cell_content = ""
            for classroom in classrooms:
                entry = timetable[classroom.name][day][time_slot]
                if entry and entry["classroom"] == classroom.name:
                    subject = entry["subject"]
                    subject_type = entry.get("subject_type", "")
                    professor = clean_professor_name(entry["professor"])
                    classroom_name = classroom.name.replace(" ", "_")

                    class_list = [f"classroom-{classroom_name}"]
                    if subject in elective_names:
                        class_list.append("elective")
                    if subject_type == "Predavanje":
                        class_list.append("lecture")
                    elif subject_type == "Vježbe":
                        class_list.append("exercise")

                    classes = " ".join(class_list)
                    cell_content += f"""
                    <div class="{classes} type-mode room-mode">
                        <strong>{subject}</strong><br>
                        {subject_type}<br>
                        {professor}<br>
                        {entry["classroom"]}
                    </div>
                    """
            if not cell_content:
                cell_content = "—"
            html += f"<td>{cell_content}</td>"
        html += "</tr>"

    html += """
    </table>
    <script>
        function setColorMode(mode) {
            document.querySelectorAll("td div").forEach(div => {
                div.classList.remove("type-mode", "room-mode");
                if (mode === "type") div.classList.add("type-mode");
                else div.classList.add("room-mode");
            });
            document.getElementById("legend-type").classList.toggle("hidden", mode !== "type");
            document.getElementById("legend-room").classList.toggle("hidden", mode !== "room");
        }

        window.onload = () => setColorMode("type");
    </script>
</body>
</html>
"""

    return html
