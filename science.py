import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
import matplotlib.pyplot as plt
import seaborn as sns

# ... (Other imports for TF-IDF, RNNs, CNNs, etc. - add as needed) ...


def preprocess_data(data, target_column):
    """Preprocesses the data."""

    # Handle missing values (replace with mean for numerical features)
    for col in data.columns:
        if data[col].dtype in [np.number]:
            data[col].fillna(data[col].mean(), inplace=True)

    # Encode categorical features (if any)
    for col in data.select_dtypes(include=["object", "category"]).columns:
        if col != target_column:
            le = LabelEncoder()
            data[col] = le.fit_transform(data[col])

    # Normalize numerical features
    scaler = StandardScaler()
    numerical_features = data.select_dtypes(include=[np.number]).columns
    data[numerical_features] = scaler.fit_transform(data[numerical_features])

    return data


def train_and_evaluate_model(
    model, X_train, X_test, y_train, y_test, model_type="classification"
):
    """Trains and evaluates the model."""
    model.fit(X_train, y_train)

    if model_type == "classification":
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average="weighted")
        recall = recall_score(y_test, y_pred, average="weighted")
        f1 = f1_score(y_test, y_pred, average="weighted")

        return {
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1-Score": f1,
        }
    elif model_type == "regression":
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        return {"MSE": mse, "R-squared": r2}
    else:
        return {}


def data_science_page():
    """Streamlit app for the Data Science page."""
    st.title("Automated Machine Learning")

    # File uploader
    uploaded_file = st.file_uploader("Upload your dataset", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
        except Exception:
            data = pd.read_excel(uploaded_file)

        st.write("## Data Preview")
        st.write(data.head())

        # Target variable selection
        target_column = st.selectbox("Select Target Variable", data.columns)

        # Preprocess data
        data = preprocess_data(data, target_column)

        # Split data
        X = data.drop(target_column, axis=1)
        y = data[target_column]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Model Selection and Training
        st.write("## Model Selection and Training")
        model_type = st.selectbox(
            "Select Model Type", ["Classification", "Regression"]
        )

        if model_type == "Classification":
            selected_models = st.multiselect(
                "Select Models",
                ["Logistic Regression", "Random Forest", "Gradient Boosting"],
            )
            models = {
                "Logistic Regression": LogisticRegression(),
                "Random Forest": RandomForestClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(),
            }
        elif model_type == "Regression":
            selected_models = st.multiselect(
                "Select Models", ["Linear Regression"]
            )
            models = {"Linear Regression": LinearRegression()}
        else:
            selected_models = []
            models = {}

        if st.button("Run Models"):
            results = {}
            for model_name in selected_models:
                model = models[model_name]
                results[model_name] = train_and_evaluate_model(
                    model,
                    X_train,
                    X_test,
                    y_train,
                    y_test,
                    model_type=model_type.lower(),
                )

            st.write("## Results")
            if results:
                # Display results in ascending order of a chosen metric
                if model_type == "Classification":
                    # Sort by accuracy (you can change this to another metric)
                    sorted_results = sorted(
                        results.items(), key=lambda item: item[1]["Accuracy"]
                    )
                elif model_type == "Regression":
                    # Sort by R-squared (you can change this to another metric)
                    sorted_results = sorted(
                        results.items(), key=lambda item: item[1]["R-squared"]
                    )

                for model_name, metrics in sorted_results:
                    st.write(f"### {model_name}")
                    st.write(metrics)

                    # Confusion Matrix for Classification
                    if model_type == "Classification":
                        model = models[model_name]
                        y_pred = model.predict(X_test)
                        cm = confusion_matrix(y_test, y_pred)
                        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
                        disp.plot()
                        st.pyplot()

if __name__ == "__main__":
    data_science_page()