from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime, timedelta

app = Flask(__name__, static_folder=".", static_url_path="")

def build_schedule(subjects):
    today = datetime.today()
    schedule = []

    for sub in subjects:
        exam = datetime.strptime(sub['exam_date'], "%Y-%m-%d")
        days_left = max((exam - today).days, 1)

        sub['priority_score'] = (sub['difficulty'] * 2) + (10 / days_left)

    subjects.sort(key=lambda x: -x['priority_score'])

    current_day = today

    for sub in subjects:
        sessions = min(5, sub['difficulty'] + 1)

        for _ in range(sessions):
            schedule.append({
                "date": current_day.strftime("%Y-%m-%d"),
                "focus": sub['name'],
                "note": f"Revise + Practice {sub['name']}"
            })
            current_day += timedelta(days=1)

    return schedule


@app.route("/")
def home():
    return send_from_directory(".", "body.html")


@app.route("/api/schedule", methods=["POST"])
def schedule_api():
    data = request.json
    subjects = data.get("subjects", [])
    result = build_schedule(subjects)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
