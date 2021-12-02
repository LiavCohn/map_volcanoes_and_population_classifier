import folium
import pandas as pd

map = folium.Map(location = [38.58,-99.09], zoom_start=6, tiles="Stamen Terrain")



#load the data- volacons in the US
data = pd.read_csv("volcanoes.txt")
lat = list(data.LAT)
lon = list(data.LON)
elev = list(data.ELEV)
names = list(data.NAME)

def color_maker(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000<=elevation <3000:
        return 'orange'

    return 'red'


html = """ Volcano name: <br> <a href = "https://www.google.com/search?q=%%22%s%%22" target=_blank>%s</a><br>
       Height: %s m"""

#we have to groups that will contain different layers- one for the volcanoes and another for the population

feature_group_volcano = folium.FeatureGroup(name = "Volcanoes")
feature_group_pop = folium.FeatureGroup(name = "Population")

feature_group_pop.add_child(folium.GeoJson(data=open('world.json','r',encoding = 'utf-8-sig').read() ,
style_function = lambda x: {'fillColor'  : 'green' if x['properties']['POP2005'] < 15000000
else 'orange' if  15000000 <= x['properties']['POP2005'] < 50000000
else 'red '}))

for lat,lon,el,name in zip(lat,lon,elev,names):
    #add object to the Map
    iframe = folium.IFrame(html= html % (name,name,el), width=200, height=100) #this will be the popup
    feature_group_volcano.add_child(folium.CircleMarker(location= [lat,lon], radius = 6, popup= folium.Popup(iframe), fill_color=color_maker(el),color='grey',fill_opacity=0.7))


map.add_child(feature_group_pop)
map.add_child(feature_group_volcano)

#with LayerControl we can select different layers and dactivate them
map.add_child(folium.LayerControl())

map.save("map.html")
