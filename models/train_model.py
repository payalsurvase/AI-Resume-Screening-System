import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
df = pd.read_csv("data/ai_resume_screening.csv")

# Convert text columns to numbers
encoder = LabelEncoder()

df["education_level"] = encoder.fit_transform(df["education_level"])
df["shortlisted"] = encoder.fit_transform(df["shortlisted"])

# Features
X = df.drop("shortlisted", axis=1)

# Target
y = df["shortlisted"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestClassifier(random_state=42)

model.fit(X_train, y_train)

# Prediction
pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, pred)

print("Accuracy:", round(accuracy * 100, 2), "%")

# Save model
joblib.dump(model, "models/resume_shortlist_model.pkl")

print("Model Saved Successfully!")