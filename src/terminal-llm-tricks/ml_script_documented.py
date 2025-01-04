import pickle

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load data from a CSV file.

    Args:
        filepath (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    data = pd.read_csv(filepath)
    return data


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform feature engineering on the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The DataFrame with new features.
    """
    # Example feature engineering steps
    df["age_squared"] = df["age"] ** 2
    df["income_log"] = np.log1p(df["income"])

    # Handle categorical variables
    categorical_cols = df.select_dtypes(include=["object"]).columns
    df = pd.get_dummies(df, columns=categorical_cols)

    return df


def preprocess_data(df: pd.DataFrame, target_column: str) -> tuple:
    """
    Preprocess the DataFrame and split it into training and testing sets.

    Args:
        df (pd.DataFrame): The input DataFrame.
        target_column (str): The target variable's name.

    Returns:
        tuple: Tuple containing:
            - X_train (np.ndarray): Training features.
            - X_test (np.ndarray): Testing features.
            - y_train (pd.Series): Training labels.
            - y_test (pd.Series): Testing labels.
            - scaler (StandardScaler): The fitted scaler object.
    """
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


def train_model(X_train: np.ndarray, y_train: pd.Series) -> RandomForestClassifier:
    """
    Train a Random Forest classifier.

    Args:
        X_train (np.ndarray): Training features.
        y_train (pd.Series): Training labels.

    Returns:
        RandomForestClassifier: The trained Random Forest model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model


def evaluate_model(
    model: RandomForestClassifier, X_test: np.ndarray, y_test: pd.Series
) -> tuple:
    """
    Evaluate the trained model on test data.

    Args:
        model (RandomForestClassifier): The trained Random Forest model.
        X_test (np.ndarray): Testing features.
        y_test (pd.Series): Testing labels.

    Returns:
        tuple: Tuple containing:
            - accuracy (float): The accuracy of the model.
            - report (str): The classification report as a string.
    """
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)

    print(f"Model Accuracy: {accuracy:.2f}")
    print("\nClassification Report:")
    print(report)

    return accuracy, report


def make_predictions(
    model: RandomForestClassifier, scaler: StandardScaler, new_data: pd.DataFrame
) -> np.ndarray:
    """
    Make predictions on new data using the trained model.

    Args:
        model (RandomForestClassifier): The trained Random Forest model.
        scaler (StandardScaler): The fitted scaler object.
        new_data (pd.DataFrame): New data to make predictions on.

    Returns:
        np.ndarray: Predicted labels for the new data.
    """
    # Ensure new_data has same features as training data
    new_data_scaled = scaler.transform(new_data)
    predictions = model.predict(new_data_scaled)
    return predictions


def save_model(model: RandomForestClassifier, filepath: str) -> None:
    """
    Save the trained model to a file.

    Args:
        model (RandomForestClassifier): The trained Random Forest model.
        filepath (str): The path where the model will be saved.
    """
    with open(filepath, "wb") as file:
        pickle.dump(model, file)


def load_saved_model(filepath: str) -> RandomForestClassifier:
    """
    Load a saved model from a file.

    Args:
        filepath (str): The path to the saved model file.

    Returns:
        RandomForestClassifier: The loaded Random Forest model.
    """
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
