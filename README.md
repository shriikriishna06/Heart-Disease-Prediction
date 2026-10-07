# 🫀 Heart Risk Check

A simple web app that estimates the risk of heart disease from a few health details. It is built with Streamlit and powered by a machine learning classification model.

## About the project

Several classification models were trained and compared on a heart disease dataset. Logistic Regression gave the highest accuracy, so it was chosen as the final model for the app.

## How it works

1. You enter details such as age, blood pressure, cholesterol, max heart rate, ECG result and chest pain type.
2. The inputs are one-hot encoded, matched to the training columns and scaled.
3. The Logistic Regression model predicts whether the risk is higher or lower and shows a risk percentage.

## Inputs used

Age, Sex, Chest Pain Type, Resting BP, Cholesterol, Fasting Blood Sugar, Resting ECG, Max Heart Rate, Exercise-Induced Angina, Oldpeak (ST depression) and ST Slope.

## Tech stack

- Python
- Streamlit
- scikit-learn
- pandas and joblib
