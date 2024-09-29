#python manage.py shell   
from deals.models import Post  # Import your Post model
object_data_arr = [] #product_name, location_name, address, info_text, score, post_date, location_lat, location_long
for item in Post.objects.all():
    object_data_arr.append(
        [item.product_name, item.location_name, item.location_street_address, item.info_text, item.score,
        item.post_date, item.location_lat, item.location_long]
    )
        

print(object_data_arr)


import folium
from folium.plugins import MarkerCluster
# Create a map object centered on me
vandy = [36.1446206, -86.8032659]
my_map = folium.Map(location=vandy, zoom_start=12, control_scale=True)

# my location as star
folium.Marker(
    location=vandy,
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

#product_name, location_name, address, info_text, score, post_date, location_lat, location_long
for object in object_data_arr:
    popup_html = f"<b>Deal:</b> {object[0]}<br/>"
    popup_html += f"<b>Store:</b> {object[1]}<br/>"
    popup_html += f"<b>Address:</b> {object[2]}<br/>"
    popup_html += f"<b>Info:</b> {object[3]}<br/>"
    popup_html += f"<b>Number Upvotes:</b> {object[4]}<br/>"
    popup_html += f"<b>Post Date:</b> {object[5].strftime('%B %d, %Y, %I:%M %p')}<br/>"
    #popup_html += '<b><a href="{}" target="_blank">Link</a></b>'.format('LINK')
    popup_iframe = folium.IFrame(width=370, height=150, html=popup_html)

    # Create a marker with a green dollar sign icon
    marker = folium.Marker(
        location=[object[6], object[7]],
        tooltip=object[0],  # Show the name always when hovering over the marker
        icon=folium.Icon(icon='dollar-sign', color='green', prefix='fa'),
        popup=folium.Popup(popup_iframe)
    )
    
    # Add the marker to the cluster
    marker.add_to(marker_cluster)

# Add custom JavaScript for the back button
'''my_map.get_root().html.add_child(folium.Element("""
    <div style="position: absolute; top: 80px; left: 10px; z-index: 1000;">
        <a class="dropdown-item" href="{% url 'deals:home' %}" 
                style="background-color: white; border: 2px solid #007bff; border-radius: 5px; padding: 5px; cursor: pointer;">
            Back
        </a>
    </div>
"""))'''

from django.urls import reverse
# Generate the URL for 'deals:home'
home_url = reverse('deals:home')
# Add the element to your map
my_map.get_root().html.add_child(folium.Element(f"""
    <div style="position: absolute; top: 80px; left: 10px; z-index: 1000;">
        <a class="dropdown-item" href="{home_url}" 
                style="background-color: white; border: 2px solid #007bff; border-radius: 5px; padding: 5px; cursor: pointer;">
            Back
        </a>
    </div>
"""))


# Save the map to an HTML file
my_map.save("./deals/templates/deals/map.html")