from flask import Flask, render_template, request, jsonify
import pandas as pd
import folium
from capitals import find_city_with_most_closer_capitals, get_closer_foreign_capitals, create_map_with_arcs

from flask import Flask, render_template, request, jsonify
import pandas as pd
import folium
import json
from flask_sqlalchemy import SQLAlchemy
from models import db, CountryMap, CityMap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///capitals.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

file_path = 'resources/worldcities.csv'
world_cities = pd.read_csv(file_path)
countries = sorted(world_cities['country'].unique())

with app.app_context():
    db.create_all()  # Create database tables based on models if not exist

def get_or_create_data(country, city=None):
    if city:
        map_data = CityMap.query.filter_by(country=country, city=city).first()
    else:
        map_data = CountryMap.query.filter_by(country=country).first()
    
    if map_data:
        data = json.loads(map_data.data)
    else:
        if city:
            data = get_closer_foreign_capitals(city, country, file_path)
        else:
            data = find_city_with_most_closer_capitals(country, file_path)

        json_data = json.dumps({
            'city': data['city'],
            'closer_capitals': data['closer_capitals'],
            'city_data': {'country': country, 'city': data['city']}
        })

        if city:
            new_entry = CityMap(country=country, city=city, data=json_data)
        else:
            new_entry = CountryMap(country=country, city_with_most_capitals=data['city'], data=json_data)
        db.session.add(new_entry)
        db.session.commit()

    return data

@app.route('/', methods=['GET'])
def index():    
    return render_template('index.html', countries=countries)

@app.route('/stored-countries')
def stored_countries():
    return render_template('stored_countries.html')

@app.route('/get_cities/<country>')
def get_cities(country):
    cities = sorted(world_cities[world_cities['country'] == country]['city'].unique())
    return jsonify(cities)

@app.route('/get_map', methods=['POST'])
def get_map():
    country = request.form['country']
    city = request.form.get('city', None)
    data = get_or_create_data(country, city)

    map_data = {
        'city_data': {'city': data['city'], 'country': country},
        'closer_capitals': data['closer_capitals']
    }
    map = create_map_with_arcs(map_data, file_path)
    map_html = map._repr_html_()

    # Prepare data for displaying information about closer capitals
    info_data = {
        'selected_city': data['city'],
        'closer_capitals': data['closer_capitals']
    }
    
    return jsonify({'map': map_html, 'info': info_data})

@app.route('/list_countries')
def list_countries():
    entries = CountryMap.query.order_by(CountryMap.country).all()
    countries_info = {}
    for entry in entries:
        countries_info.setdefault(entry.country, []).append({
            'city_with_most_capitals': entry.city_with_most_capitals,
            'data': entry.data  # Ensure this data is in a JSON-serializable format
        })
    return jsonify(countries_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111, debug=True)
