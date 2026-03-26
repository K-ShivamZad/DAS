from flask import Flask, render_template, request, jsonify, flash, redirect, url_for

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = "super_secret_key_for_flash_messages" # Required for flash messages

# 1. Standard Web Route (Serves HTML)
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# 2. Form Handling Route
@app.route('/predict', methods=['POST'])
def predict_ui():
    try:
        # Extract data from the HTML form
        area = float(request.form['area'])
        bedrooms = int(request.form['bedrooms'])
        
        # Simulated Model Prediction logic
        # (In reality, you would use joblib to load the model you saved earlier: model.predict([[area, bedrooms]]))
        estimated_price = round((area * 0.05) + (bedrooms * 2.5), 2)
        
        # Flash a success message
        flash("Prediction generated successfully!")
        
        # Render the template again, passing the prediction variable via Jinja
        return render_template('index.html', prediction=estimated_price)
    
    except Exception as e:
        flash(f"Error: {str(e)}")
        return redirect(url_for('home'))

# 3. Creating an API with Query Parameters
# Try accessing: http://127.0.0.1:5000/api/v1/predict?area=2000&beds=4
@app.route('/api/v1/predict', methods=['GET'])
def predict_api():
    # Extract Query Parameters from the URL
    area = request.args.get('area', type=float)
    beds = request.args.get('beds', type=int)
    
    if area is None or beds is None:
        return jsonify({'error': 'Please provide both area and beds parameters.'}), 400
        
    # Simulated Prediction
    estimated_price = round((area * 0.05) + (beds * 2.5), 2)
    
    # APIs return JSON data, not HTML
    return jsonify({
        'status': 'success',
        'input': {'area_sqft': area, 'bedrooms': beds},
        'estimated_price_lakhs': estimated_price
    })

if __name__ == '__main__':
    # use_reloader=False is important when running inside certain IDE environments
    app.run(debug=True, port=5000, use_reloader=False)
