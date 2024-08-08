from flask import Flask, request, jsonify, send_from_directory
import util
import os
from flask_cors import CORS

app = Flask(__name__, static_folder='client', static_url_path='', template_folder='client')
CORS(app)

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'app.html')

@app.route('/get_location_names/<city>', methods=['GET'])
def get_location_names(city):
    response = jsonify({
        'locations': util.get_location_names(city)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    data = request.get_json()

    if not all(k in data for k in ('city', 'area_sqft', 'location', 'bedrooms', 'bathrooms')):
        return jsonify({'error': 'Missing data'}), 400

    city = data['city']
    area_sqft = float(data['area_sqft'])
    location = data['location']
    bedrooms = int(data['bedrooms'])
    bathrooms = int(data['bathrooms'])

    response = jsonify({
        'estimated_price': util.get_estimated_price(city, location, area_sqft, bedrooms, bathrooms)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run(host='0.0.0.0', port=8000, debug=True)
