import pickle

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_data(filepath):
    data = pd.read_csv(filepath)
    return data


def feature_engineering(df):
    # Example feature engineering steps
    df["age_squared"] = df["age"] ** 2
    df["income_log"] = np.log1p(df["income"])

    # Handle categorical variables
    categorical_cols = df.select_dtypes(include=["object"]).columns
    df = pd.get_dummies(df, columns=categorical_cols)

    return df


def preprocess_data(df, target_column):
    # Split features and target
    X = df.drop(target_column, axis=1)
    y = df[target_column]

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler


def train_model(X_train, y_train):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)

    print(f"Model Accuracy: {accuracy:.2f}")
    print("\nClassification Report:")
    print(report)

    return accuracy, report


def make_predictions(model, scaler, new_data):
    # Ensure new_data has same features as training data
    new_data_scaled = scaler.transform(new_data)
    predictions = model.predict(new_data_scaled)
    return predictions


def save_model(model, filepath):
    with open(filepath, "wb") as file:
        pickle.dump(model, file)


def load_saved_model(filepath):
    with open(filepath, "rb") as file:
        model = pickle.load(file)
    return model


# Example usage
if __name__ == "__main__":
    # Sample workflow
    try:
        # Load and prepare data
        data = load_data("your_data.csv")
        processed_data = feature_engineering(data)

        # Preprocess and split data
        X_train, X_test, y_train, y_test, scaler = preprocess_data(
            processed_data, "target_column"
        )

        # Train and evaluate model
        model = train_model(X_train, y_train)
        accuracy, report = evaluate_model(model, X_test, y_test)

        # Save model
        save_model(model, "model.pkl")

        # Make predictions on new data
        new_data = pd.DataFrame()  # Your new data here
        predictions = make_predictions(model, scaler, new_data)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
