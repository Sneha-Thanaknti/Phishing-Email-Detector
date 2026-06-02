from flask import Flask, render_template, request, Response
import joblib
import sqlite3

app = Flask(__name__)

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

@app.route("/", methods=["GET", "POST"])
def home():

    prediction = ""
    confidence = ""

    if request.method == "POST":

        email = request.form["email"]

        email_vector = vectorizer.transform([email])

        prediction = model.predict(email_vector)[0]

        probabilities = model.predict_proba(email_vector)
        confidence = round(max(probabilities[0]) * 100, 2)

        conn = sqlite3.connect("emails.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO scans(email, prediction, confidence) VALUES (?, ?, ?)",
            (email, prediction, confidence)
        )

        conn.commit()
        conn.close()

    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM scans ORDER BY id DESC")

    history = cursor.fetchall()

    total_scans = len(history)

    phishing_count = sum(
        1 for row in history if row[2] == "phishing"
    )

    safe_count = sum(
        1 for row in history if row[2] == "safe"
    )

    conn.close()

    return render_template(
        "index.html",
        prediction=prediction,
        confidence=confidence,
        history=history,
        total_scans=total_scans,
        phishing_count=phishing_count,
        safe_count=safe_count
    )
@app.route("/download")
def download():

    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, prediction, confidence FROM scans"
    )

    rows = cursor.fetchall()

    conn.close()

    csv_data = "ID,Prediction,Confidence\n"

    for row in rows:
        csv_data += f"{row[0]},{row[1]},{row[2]}\n"

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=scan_report.csv"
        }
    )

if __name__ == "__main__":
    app.run(debug=True)