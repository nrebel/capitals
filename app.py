from flask import Flask, render_template, request, jsonify
import pandas as pd
import folium
from capitals import find_city_with_most_closer_capitals, get_closer_foreign_capitals, create_map_with_arcs

app = Flask(__name__)

# Assuming that the CSV file is in the same directory as the script
file_path = 'resources/worldcities.csv'
world_cities = pd.read_csv(file_path)
countries = sorted(world_cities['country'].unique())

@app.route('/', methods=['GET'])
def index():    
    return render_template('index.html', countries=countries)

@app.route('/get_cities/<country>')
def get_cities(country):
    cities = sorted(world_cities[world_cities['country'] == country]['city'].unique())
    return jsonify(cities)

@app.route('/get_map', methods=['POST'])
def get_map():
    country = request.form['country']
    city = request.form.get('city', None)
    if city:
        # Get closer foreign capitals if a city is selected
        result = get_closer_foreign_capitals(city, country, file_path)
    else:
        # Get city with the most closer capitals if no city is selected
        result = find_city_with_most_closer_capitals(country, file_path)
    
    # Create the map
    map_data = {
        'city_data': {'city': result['city'], 'country': country},
        'closer_capitals': result['closer_capitals']
    }
    map = create_map_with_arcs(map_data, file_path)
    return map._repr_html_()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2222, debug=True)
