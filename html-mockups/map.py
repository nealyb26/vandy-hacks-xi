import folium
from folium.plugins import MarkerCluster

# List of coordinates with names
# Get data post filter
nash_pairs = [
    ["Downtown Nashville", (36.1667, -86.7816)],
    ["Nashville Public Library", (36.1587, -86.7884)],
    ["The Parthenon", (36.1528, -86.7855)],
    ["Vanderbilt University", (36.1682, -86.7903)],
    ["The Gulch", (36.1420, -86.7803)],
    ["Music Row", (36.1565, -86.7894)],
    ["Nashville Zoo", (36.1536, -86.8037)],
    ["Tennessee State Capitol", (36.1692, -86.7854)],
    ["East Nashville", (36.1408, -86.7855)],
    ["Bellevue", (36.1794, -86.7746)], ["Bellevue2", (36.1790, -86.7756)], ["Bellevue3", (36.1790, -86.7756)]
]
coords = [item[1] for item in nash_pairs]

# Create a map object centered on me
vandy = [36.1627, -86.7816]
my_map = folium.Map(location=vandy, zoom_start=13, control_scale=True, )
#width =500, height = 500

# my location as star
my_loc = [36.144051, -86.800949]
folium.Marker(
    location=my_loc,
    icon=folium.Icon(icon='star', color='orange', prefix='fa'),  # Font Awesome star icon
    tooltip="My Location"
).add_to(my_map)


#add all stores - FIXME custom icon for each category w default as $
marker_cluster = MarkerCluster(
    spiderfyOnMaxZoom=True,  # Expand clusters when max zoom is reached
    maxClusterRadius=30,      # Set the maximum radius of clusters
    showCoverageOnHover=False,  # Optionally hide coverage on hover
    disableClusteringAtZoom=16  # Disable clustering at higher zoom levels (optional)
).add_to(my_map)


for name, (lat, lon) in nash_pairs:
    popup_html = f"<b>Deal:</b> DEAL<br/>"
    popup_html += f"<b>Store:</b> STORE<br/>"
    popup_html += f"<b>Address:</b> ADDRESS<br/>"
    popup_html += '<b><a href="{}" target="_blank">Link</a></b>'.format('LINK')
    popup_iframe = folium.IFrame(width=200, height=100, html=popup_html)

    # Create a marker with a green dollar sign icon
    marker = folium.Marker(
        location=[lat, lon],
        tooltip=name,  # Show the name always when hovering over the marker
        icon=folium.Icon(icon='dollar-sign', color='green', prefix='fa'),
        popup=folium.Popup(popup_iframe)
    )
    
    # Add the marker to the cluster
    marker.add_to(marker_cluster)

# Save the map to an HTML file
my_map.save("html-mockups/map.html")