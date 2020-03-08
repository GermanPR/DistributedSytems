import requests

#declare a session object

r = requests.get('https://api.postcodes.io/postcodes/DH11QW')

print(r.json())