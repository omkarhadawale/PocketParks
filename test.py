from flask import Flask, render_template
import folium
import requests

app = Flask(__name__)

def get_zipcode_from_coordinates(latitude, longitude):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key=AIzaSyAO795cD8dqb2PwLEMOKS22MlrFfx19JB8'
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        for result in data['results']:
            for component in result['address_components']:
                if 'postal_code' in component['types']:
                    return int(component['long_name'])
    return None


    


def get_forestation_coordinates():
    data = requests.get("https://data.cityofnewyork.us/resource/4jyz-6b7u.json")
    data = data.json()
    coordinates_list = []
    for item in data:
        geometry = item.get('geometry')
        if geometry:
            
            longitude, latitude = map(float, geometry.replace('POINT (', '').replace(')', '').split())
            coordinates_list.append((latitude, longitude))

    return coordinates_list

def coordinates_belongs_to_zip():
    zip_codes =[10458, 10468,10453, 10468,10457, 10458,10451, 10452,10456,10451, 10454,10455,10474,10472, 10473,10029, 10035,10017, 10018, 10019,10020, 10022,11212, 11233, 11236,11224, 11229,10004,11435]
    all_coordinates = get_forestation_coordinates()
    required_coordinates = []
    for i in all_coordinates:
        if get_zipcode_from_coordinates(i[0],i[1]) in zip_codes:
            
            required_coordinates.append(i)
    return required_coordinates        



@app.route('/')
def index():
    # List of latitude and longitude points as tuples
    coordinates = coordinates_belongs_to_zip()
   
    
    # Create a Folium map centered at an initial point
    map_center = [sum([coord[0] for coord in coordinates]) / len(coordinates),
                  sum([coord[1] for coord in coordinates]) / len(coordinates)]
    my_map = folium.Map(location=map_center, zoom_start=5)

    # Add markers for each coordinate
    for coord in coordinates:
        folium.Marker(location=[coord[0], coord[1]]).add_to(my_map)

    # Save the map to an HTML file
    my_map.save('templates/map.html')

    # Render the template containing the map
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)
