from flask import Flask, render_template, request
import joblib

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

    return render_template(
        "index.html",
        prediction=prediction,
        confidence=confidence
    )

if __name__ == "__main__":
    app.run(debug=True)