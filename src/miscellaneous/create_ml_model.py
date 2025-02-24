"""
Machine learning is not covered in the module.
This is a simple example of how to create a model using the medal standings data.
`pip install scikit-learn` is required before you can run this code.
"""
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def train_and_save_model():
    """
    Train a model to predict Total based on Year and Team, and save it to a .pkl file.
    """
    # Read the data into a DataFrame
    para_excel = Path(__file__).parent.parent.joinpath("data", "paralympics.xlsx")
    cols = ["Year", "Rank", "Team", "Gold", "Silver", "Bronze", "Total"]
    data = pd.read_excel(para_excel, sheet_name="medal_standings", usecols=cols)

    # Drop rows with NaNs since the accuracy of the model is not the focus here
    data.dropna(inplace=True)

    # Features and target
    X = data[['Year', 'Team']]
    y = data['Total']

    # One-hot encode the 'Team' column
    preprocessor = ColumnTransformer(
        transformers=[
            ('team', OneHotEncoder(), ['Team'])
        ],
        remainder='passthrough'
    )

    # Create a pipeline with preprocessing and regression model
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    pipeline.fit(X_train, y_train)

    # Save the model to a .pkl file
    joblib.dump(pipeline, '../data/model.pkl')

    print("Model saved to model.pkl")


if __name__ == "__main__":
    # Train the model and save it
    train_and_save_model()
