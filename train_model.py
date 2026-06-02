import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

# Load dataset
data = pd.read_csv("dataset.csv")

# Convert text into numbers
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(data["text"])

# Labels
y = data["label"]

# Train model
model = MultinomialNB()
model.fit(X, y)

# Save model and vectorizer
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model Trained Successfully")
