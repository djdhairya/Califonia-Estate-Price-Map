import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from sklearn.datasets import fetch_california_housing
import folium
from folium import plugins

# Load the California housing dataset
data = fetch_california_housing(as_frame=True).frame

# Create the map centered at the mean latitude and longitude
m = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=6)

# Get min and max values for house value and average rooms
price_min, price_max = data['MedHouseVal'].min(), data['MedHouseVal'].max()
size_min, size_max = data['AveRooms'].min(), data['AveRooms'].max()

# Iterate through each row and plot the data
for _, row in data.iterrows():
    normalized_price = (row['MedHouseVal'] - price_min) / (price_max - price_min)
    color = plt.cm.RdYlGn(1 - normalized_price)

    normalized_rooms = (row['AveRooms'] - size_min) / (size_max - size_min)

    popup_info = f"""Medium House Value: ${row['MedHouseVal']:.2f}<br>
    Average Rooms: {row['AveRooms']:.2f}<br>
    Population: {row['Population']}<br>
    Median Income: {row['MedInc']:.2f}"""

    folium.CircleMarker(
        [row['Latitude'], row['Longitude']],
        radius=5 + 20 * normalized_rooms,
        color=mcolors.to_hex(color[:3]),
        fill=True,
        fill_color=mcolors.to_hex(color[:3]),
        fill_opacity=0.7,
        popup=folium.Popup(popup_info, max_width=300)
    ).add_to(m)

# Add a minimap
plugins.MiniMap().add_to(m)

# Save the map to an HTML file
m.save('California_Estate.html')
