import requests

# #declare a session object

r = requests.get('https://api.postcodes.io/postcodes/DH13DE')

# print(r.json())
# import requests, urllib3, json
# from urllib.parse import quote,urlencode
# postcode = "DH1 1QW"
# params = {"api_key": "iddqd"}

# #conn = httplib2.HTTPSConnection("api.ideal-postcodes.co.uk:443")
# r = requests.get('https://api.ideal-postcodes.co.uk/v1/postcodes/%s?%s' % (quote(postcode), urlencode(params)))
print(r.json()['status'])
# addresses = json.load(r)['result']