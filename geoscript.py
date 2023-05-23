import webbrowser
import requests
import platform
import os
import geocoder

sistema_operativo = platform.system()
version_sistema = platform.release()

print("Sistema Operativo:", sistema_operativo)
print("Versión:", version_sistema)


def obtener_direccion_ip():
    response = requests.get('https://api.ipify.org?format=json')
    data = response.json()
    return data['ip']


def geolocalizar_ip(ip):
    g = geocoder.ip(ip)
    if not g.ok:
        return "No se pudo encontrar la ubicación."
    else:
        return (g.latlng[0], g.latlng[1])


ip = obtener_direccion_ip()
print("Dirección IP:", ip)

coordenadas = geolocalizar_ip(ip)
print("Coordenadas geográficas:")
print("Latitud:", coordenadas[0])
print("Longitud:", coordenadas[1])

# Genera el contenido HTML para mostrar la información de geolocalización con un mapa
html_content = f'''
<html>
<head>
    <title>Geolocalización</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
    crossorigin=""/>
    <style>
        #map {{
            height: 400px;
        }}
    </style>
</head>
<body>
    <h1>Geolocalización</h1>
    <p>Sistema Operativo: {sistema_operativo}</p>
    <p>Versión: {version_sistema}</p>
    <p>Dirección IP: {ip}</p>
    <p>Coordenadas geográficas:</p>
    <p>Latitud: {coordenadas[0]}</p>
    <p>Longitud: {coordenadas[1]}</p>
    <div id="map"></div>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
    integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
    crossorigin=""></script>
    <script>
        var map = L.map('map').setView([{coordenadas[0]}, {coordenadas[1]}], 13);
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            maxZoom: 19,
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
        }}).addTo(map);
        L.marker([{coordenadas[0]}, {coordenadas[1]}]).addTo(map);
    </script>
</body>
</html>
'''

# Guarda el contenido HTML en un archivo
with open('geolocalizacion.html', 'w') as file:
    file.write(html_content)

# Abre el archivo HTML en el navegador web predeterminado
webbrowser.open('file://' + os.path.realpath('geolocalizacion.html'))
