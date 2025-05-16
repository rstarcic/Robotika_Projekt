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


def generate_html_single_table(timetable, classrooms):
    html = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 50px; }
            th, td { border: 1px solid #444; padding: 8px; text-align: center; vertical-align: top; font-size: 14px; }
            th { background-color: #f0f0f0; }
            h1 { margin-top: 20px; text-align: center; }
        </style>
        <title>College Timetable</title>
    </head>
    <body>
        <h1>College Timetable (All Classrooms)</h1>
        <table>
            <tr>
                <th>Time Slot</th>
    """

    # Zaglavlja dana
    for day in days:
        html += f"<th>{day}</th>"
    html += "</tr>"

    # Redovi za svaki timeslot
    for time_slot in time_slots:
        html += f"<tr><td><strong>{time_slot}</strong></td>"

        for day in days:
            cell_content = ""
            for classroom in classrooms:
                lecture = timetable[classroom.name][day][time_slot]
                if lecture and lecture["classroom"] == classroom.name:
                    subject = lecture["subject"]
                    subject_type = lecture.get("subject_type", "")
                    professor = clean_professor_name(lecture["professor"])
                    classroom_name = classroom.name

                    cell_content += (
                        f"<strong>{subject}</strong><br>"
                        f"{subject_type}<br>"
                        f"{professor}<br>"
                        f"{classroom_name}<br><br>"
                    )

            if cell_content == "":
                cell_content = "—"

            html += f"<td>{cell_content}</td>"
        html += "</tr>"

    html += """
        </table>
    </body>
    </html>
    """

    return html
