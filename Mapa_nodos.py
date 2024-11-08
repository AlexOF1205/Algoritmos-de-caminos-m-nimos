import osmnx as ox
import folium

lugar = "Xalapa, Veracruz"
Grafico = ox.graph_from_place(lugar, network_type="drive", simplify=True)
nodo_central = [19.5416, -96.9109]
N = folium.Map(location=nodo_central, zoom_start=13)

for node, data in Grafico.nodes(data=True):
    folium.CircleMarker(
        location=(data['y'], data['x']),
        radius=3,
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.7,
        popup=str(node)
    ).add_to(N)

N.save("xalapa_nodo.html")

