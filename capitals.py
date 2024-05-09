import pandas as pd
import numpy as np

import folium

def create_map_with_arcs(city_data, file_path):
    # Load data for coordinates
    world_cities = pd.read_csv(file_path)
    capitals = world_cities[world_cities['capital'] == 'primary'][['city', 'lat', 'lng', 'country']]
    target_city = world_cities[(world_cities['country'] == city_data['city_data']['country']) &
                               (world_cities['city'] == city_data['city_data']['city'])].iloc[0]
    own_capital = capitals[capitals['country'] == city_data['city_data']['country']].iloc[0]

    # Create map centered around the target city
    city_map = folium.Map(location=[target_city['lat'], target_city['lng']], zoom_start=4)

    # Add marker for the target city
    folium.Marker([target_city['lat'], target_city['lng']], 
                  popup=f"{city_data['city_data']['city']} (Own City)", 
                  icon=folium.Icon(color='green')).add_to(city_map)

    # Add marker for the own capital with different color arc
    folium.Marker([own_capital['lat'], own_capital['lng']], 
                  popup=f"{own_capital['city']} (Own Capital)", 
                  icon=folium.Icon(color='red')).add_to(city_map)

    # Draw an arc to own capital
    folium.PolyLine(locations=[[target_city['lat'], target_city['lng']], 
                               [own_capital['lat'], own_capital['lng']]], 
                    color="red", weight=2, tooltip=f"{haversine(target_city['lng'], target_city['lat'], own_capital['lng'], own_capital['lat']):.2f} km").add_to(city_map)

    # Draw arcs to closer capitals
    for capital in city_data['closer_capitals']:
        cap_info = capitals[capitals['city'] == capital[0]].iloc[0]
        folium.PolyLine(locations=[[target_city['lat'], target_city['lng']], [cap_info['lat'], cap_info['lng']]],
                        color="blue", weight=1, tooltip=f"{capital[1]:.2f} km").add_to(city_map)
        folium.Marker([cap_info['lat'], cap_info['lng']], 
                      popup=f"{cap_info['city']} ({cap_info['country']})", 
                      icon=folium.Icon(color='blue')).add_to(city_map)

    return city_map


# Haversine formula to calculate the distance between two points on the Earth
def haversine(lon1, lat1, lon2, lat2):
    R = 6371.0  # Radius of the Earth in kilometers
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])  # Convert degrees to radians
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c
    return distance

def find_city_with_most_closer_capitals(country, file_path):
    # Load data
    world_cities = pd.read_csv(file_path)
    # Filter capitals and cities in the specified country
    capitals = world_cities[world_cities['capital'] == 'primary'][['city', 'lat', 'lng', 'country']]
    country_cities = world_cities[world_cities['country'] == country][['city', 'lat', 'lng']]
    country_capital = capitals[capitals['country'] == country]
    
    results = []
    
    for index, city in country_cities.iterrows():
        city_capitals_distances = []
        own_capital_distance = haversine(city['lng'], city['lat'], country_capital.iloc[0]['lng'], country_capital.iloc[0]['lat'])
        
        for cap_index, capital in capitals.iterrows():
            if capital['country'] != country:  # Exclude own country's capital
                distance = haversine(city['lng'], city['lat'], capital['lng'], capital['lat'])
                city_capitals_distances.append((capital['city'], distance, capital['country']))
        
        # Count foreign capitals closer than the own capital
        closer_capitals = [(cap[0], cap[1], cap[2]) for cap in city_capitals_distances if cap[1] < own_capital_distance]
        results.append({
            'city': city['city'],
            'closer_capitals_count': len(closer_capitals),
            'closer_capitals': closer_capitals,
            'own_capital_distance': own_capital_distance
        })
    
    # Find the city with the maximum number of closer foreign capitals
    most_closer_capitals_city = max(results, key=lambda x: x['closer_capitals_count'])
    return most_closer_capitals_city

def get_closer_foreign_capitals(city, country, file_path):
    # Load the data
    world_cities = pd.read_csv(file_path)
    capitals = world_cities[world_cities['capital'] == 'primary'][['city', 'lat', 'lng', 'country']]
    
    # Find the specific city and the capital of the country
    specific_city = world_cities[(world_cities['country'] == country) & (world_cities['city'] == city)].iloc[0]
    own_capital = capitals[capitals['country'] == country].iloc[0]
    # Calculate the distance from the specific city to its own capital
    own_capital_distance = haversine(specific_city['lng'], specific_city['lat'], own_capital['lng'], own_capital['lat'])
    
    # Initialize an empty list to store closer foreign capitals
    closer_capitals = []
    
    # Calculate distances to all foreign capitals and filter
    for index, capital in capitals.iterrows():
        if capital['country'] != country:
            distance = haversine(specific_city['lng'], specific_city['lat'], capital['lng'], capital['lat'])
            if distance < own_capital_distance:
                closer_capitals.append((capital['city'], distance, capital['country']))
    
    # Sort capitals by distance
    closer_capitals.sort(key=lambda x: x[1])

    # Prepare the result in the requested format
    result = {
        'city': city,
        'closer_capitals_count': len(closer_capitals),
        'closer_capitals': closer_capitals,
        'own_capital_distance': own_capital_distance
    }
    
    return result

def find_city_with_most_closer_capitals_worldwide(file_path):
    world_cities = pd.read_csv(file_path)
    countries = world_cities['country'].unique()

    winning_city = []
    count = 0

    print(countries)
    for country in countries:
        print("processing country: ", country)
        res = find_city_with_most_closer_capitals(country, file_path)
        if res['closer_capitals_count'] > count:
            count = res['closer_capitals_count']
            winning_city = res
            print(f"City: ", winning_city['city'], " (", country, " distance to own capital: ", winning_city['own_capital_distance'], "km)")
            print("Number of closer foreign capitals:", winning_city['closer_capitals_count'])
            
    return winning_city
    

# Example usage
file_path = 'resources/worldcities.csv'  # Replace with the actual path to the CSV file
#country = 'Brazil'
#city = 'Mannheim'
#result = find_city_with_most_closer_capitals(country, file_path)
#result = get_closer_foreign_capitals(city, country, file_path)
result = find_city_with_most_closer_capitals_worldwide(file_path)

print(f"City: ", result['city'], " (distance to own capital: ", result['own_capital_distance'], "km)")
print("Number of closer foreign capitals:", result['closer_capitals_count'])
print("List of closer capitals and distances:")
for capital in result['closer_capitals']:
    print(f"{capital[0]} ({capital[2]}): {capital[1]:.2f} km")
    
map_data = {
    'city_data': {'city': result['city'], 'country': country},
    'closer_capitals': result['closer_capitals']
}

map = create_map_with_arcs(map_data, file_path=file_path)
map.show_in_browser()