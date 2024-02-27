# app/views.py
from flask import Blueprint, render_template, request, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

# Create a Flask Blueprint which will define the view functions
bp = Blueprint('views', __name__)

# Define the base directory of your project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load the data
university_data = {
    "Washington University in St. Louis": pd.read_csv(os.path.join(BASE_DIR, 'data', 'washington_university_in_saint_louis.csv')),
    "Fontbonne University": pd.read_csv(os.path.join(BASE_DIR, 'data', 'fontbonne_university.csv')),
    "Saint Louis University": pd.read_csv(os.path.join(BASE_DIR, 'data', 'saint_louis_university.csv')),
}

# Preprocess the data
for university, df in university_data.items():
    # Compute the average AP and SAT II scores
    ap_columns = [col for col in df.columns if col.startswith('AP:')]
    sat2_columns = [col for col in df.columns if col.startswith('SAT II:')]
    df['Average AP Score'] = df[ap_columns].mean(axis=1)
    df['Average SAT II Score'] = df[sat2_columns].mean(axis=1)

    # Drop the original AP and SAT II columns
    df.drop(columns=ap_columns + sat2_columns, inplace=True)

# Train a model for each university
models = {}
for university, df in university_data.items():
    # Split the data into features (X)
    X = df

    # Standardize the features
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Train the model
    model = KMeans(n_clusters=2)  # You can adjust the number of clusters
    model.fit(X)

    # Store the model and scaler
    models[university] = (model, scaler)

@bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        form_data = request.form.to_dict()  # Convert the form data to a dictionary
        filled_fields = {k: v for k, v in form_data.items() if v}  # Remove empty fields

        # Print the filled fields
        for field, value in filled_fields.items():
            print(f"{field}: {value}")

    return render_template('index.html')

@bp.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract the fields from the POST request
        data = request.get_json()

        # Create a full feature vector with all features set to 0
        student_data_dict = {feature: [0] for feature in X.columns}

        # Update the feature vector with the user's input
        if data.get('gpa') is not None:
            student_data_dict['GPA'] = [float(data.get('gpa'))]
        if data.get('sat') is not None:
            student_data_dict['SAT'] = [float(data.get('sat'))]
        if data.get('act') is not None:
            student_data_dict['ACT'] = [float(data.get('act'))]
        if data.get('average_ap_score') is not None:
            student_data_dict['Average AP Score'] = [float(data.get('average_ap_score'))]
        if data.get('average_sat2_score') is not None:
            student_data_dict['Average SAT II Score'] = [float(data.get('average_sat2_score'))]

        # Get the model and scaler for the selected university
        model, scaler = models[data.get('university')]

        # Create a DataFrame for the student's data
        student_data = pd.DataFrame(student_data_dict)

        # Standardize the student's data
        student_data = scaler.transform(student_data)

        # Make a prediction
        prediction = model.predict(student_data)

        # Return the cluster that the student's data belongs to
        return jsonify({'prediction': prediction[0].tolist()})

    except Exception as e:
        print(str(e))  # print the exception to the terminal
        return jsonify({'error': str(e)}), 500