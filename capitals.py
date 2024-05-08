import pandas as pd
import numpy as np

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
            'closer_capitals': closer_capitals
        })
    
    # Find the city with the maximum number of closer foreign capitals
    most_closer_capitals_city = max(results, key=lambda x: x['closer_capitals_count'])
    return most_closer_capitals_city

# Example usage
file_path = 'resources/worldcities.csv'  # Replace with the actual path to the CSV file
country = 'Germany'
result = find_city_with_most_closer_capitals(country, file_path)
print("City:", result['city'])
print("Number of closer foreign capitals:", result['closer_capitals_count'])
print("List of closer capitals and distances:")
for capital in result['closer_capitals']:
    print(f"{capital[0]} ({capital[2]}): {capital[1]:.2f} km")
