import pickle

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def run_ml_pipeline(
    data_filepath, target_column, model_save_path="model.pkl", new_data=None
):
    data = pd.read_csv(data_filepath)
    df = data.copy()
    df["age_squared"] = df["age"] ** 2
    df["income_log"] = np.log1p(df["income"])
    categorical_cols = df.select_dtypes(include=["object"]).columns
    df = pd.get_dummies(df, columns=categorical_cols)
    X = df.drop(target_column, axis=1)
    y = df[target_column]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    predictions = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)
    print(f"Model Accuracy: {accuracy:.2f}")
    print("\nClassification Report:")
    print(report)
    with open(model_save_path, "wb") as file:
        pickle.dump(model, file)
    if new_data is not None:
        new_data_scaled = scaler.transform(new_data)
        return model.predict(new_data_scaled)
    return model, scaler, accuracy, report


if __name__ == "__main__":
    try:
        run_ml_pipeline("your_data.csv", "target_column")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
