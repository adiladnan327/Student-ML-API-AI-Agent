import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

MODEL_FILE = "student_model.pkl"

def train_model():
    data = pd.read_csv("students.csv")

    # X = input feature. Here, study hours.
    X = data[["hours"]]

    # y = output/target. Here, exam score.
    y = data["score"]

    model = LinearRegression()
    model.fit(X, y)

    joblib.dump(model, MODEL_FILE)
    print(f"Model trained and saved as {MODEL_FILE}")

if __name__ == "__main__":
    train_model()
