# app/views.py
from flask import Blueprint, render_template, request, jsonify

# Create a Flask Blueprint which will define the view functions
bp = Blueprint('views', __name__)

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
    # Extract data from POST request
    data = request.get_json()
    # Perform prediction using data
    # prediction = perform_prediction(data)  # You'll need to implement this
    # Return prediction result as JSON
    return jsonify({'prediction': 'Your prediction result here'})
