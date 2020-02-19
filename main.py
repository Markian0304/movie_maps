from geopy.geocoders import Nominatim
from helper import read_file, films
import pycountry
import time
import folium

year = int(input("P;ease enter year: "))
user_place = inp = input("Please enter your location (format: lat, long): ")
try:
    user_place = list(map(float, inp.split(', ')))
except Exception as ex:
    print('Incorrect data!')
    print(ex)
    exit()

geolocator = Nominatim(user_agent="Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36")

location = geolocator.reverse(user_place)

country = location.raw['address']['country']
code = location.raw['address']['country_code'].upper()
fcountry = pycountry.countries.get(alpha_2=code)
print(country)
print(fcountry.name)
print('Please wait...')

count = 0
#read file with movies
ls = read_file('locations.list')

#create map object
map = folium.Map(location=user_place, zoom_start = 5)

for i in films(ls, year, fcountry.name):
    try:
        print(i[0], '\n---------------------------')
        location = geolocator.geocode(i[1].strip())
        if location is None:
            print('None\n===========================')
        else:
            popup_text = f"{i[0]}\n({location.latitude}, {location.longitude})"
            folium.Marker(location=[location.latitude, location.longitude],
                          popup=popup_text,
                          icon=folium.Icon(color = 'green')).add_to(map)
            print((location.latitude, location.longitude),
                  location.address,
                  '\n=========================')
        count+=1
        if count % 20 == 0:
            time.sleep(4)
    except Exception as ex:
        print('Server timeout! ' + str(ex))
        time.sleep(5)

folium.Marker(location=user_place,
              popup="Place which user wrote.",
              icon=folium.Icon(color = 'orange')).add_to(map)        


map.save(f"{year}_movies_map_{fcountry.name}.html")

print(f"Finished. Please have look at the map {year}_movies_map_{fcountry.name}.html")
