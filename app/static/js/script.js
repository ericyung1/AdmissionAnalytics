function toggleInput(id) {
    var input = document.getElementById(id + "-input");
    if (document.getElementById(id + "-checkbox").checked) {
        input.style.display = "block";
    } else {
        input.style.display = "none";
    }
}

document.querySelectorAll('.form__field').forEach(function(input) {
    input.addEventListener('focus', function() {
        var label = this.parentNode.parentNode.querySelector('label');
        if (label) {
            label.style.color = 'transparent';
            label.style.backgroundImage = 'linear-gradient(to right, #11998e, #38ef7d)';
            label.style.webkitBackgroundClip = 'text';
            label.style.fontWeight = '700'; /* Make the text bold */
        }
    });
    input.addEventListener('blur', function() {
        var label = this.parentNode.parentNode.querySelector('label');
        if (label) {
            label.style.color = '#fff';
            label.style.backgroundImage = 'none';
            label.style.fontWeight = 'normal'; /* Make the text normal weight */
        }
    });
});

document.getElementById('student-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Get the filled fields
    var form_data = new FormData(document.getElementById('student-form'));
    var filled_fields = Array.from(form_data.entries()).reduce((obj, [key, value]) => {
        if (value) obj[key] = value;  // Only include fields with values
        return obj;
    }, {});

    // Send a POST request to the /predict route
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(filled_fields)
    })
    .then(response => response.json())
    .then(data => {
        // Update the content of the prediction-result div
        document.getElementById('prediction-result').textContent = 'Prediction: ' + data.prediction;
    });
});
