import joblib

# Load model and vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Get email from user
email = input("Enter Email Text: ")

# Convert to numbers
email_vector = vectorizer.transform([email])

# Predict
prediction = model.predict(email_vector)

print("\nPrediction:", prediction[0])