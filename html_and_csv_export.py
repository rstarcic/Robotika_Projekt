from data import days, time_slots


def generate_html_single_table(timetable, classrooms):
    html = """
    <html>
    <head>
        <style>
            table { border-collapse: collapse; width: 100%; margin-bottom: 50px; }
            th, td { border: 1px solid black; padding: 8px; text-align: center; vertical-align: top; }
            th { background-color: #f2f2f2; }
            h1 { margin-top: 20px; }
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
        html += f"<tr><td>{time_slot}</td>"

        for day in days:
            cell_content = ""
            for classroom in classrooms:
                lecture = timetable[classroom.name][day][time_slot]
                if lecture and lecture["classroom"] == classroom.name:
                    subject = lecture["subject"]
                    professor = lecture["professor"]
                    classroom_name = classroom.name
                    cell_content += f"<strong>{classroom_name}</strong><br>{professor}<br>{subject}<br><br>"

            if cell_content == "":
                cell_content = "Empty"

            html += f"<td>{cell_content}</td>"
        html += "</tr>"

    html += """
        </table>
    </body>
    </html>
    """

    return html
