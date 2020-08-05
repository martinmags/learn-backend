import httplib2, json

def getGeocodeLocation(inputString):
  google_api_key = "AIzaSyBLQ_YyWm61yxezenmV2t3d-xnYZ5XWZkk"
  locationString = inputString.replace(" ", "+")
  url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (locationString, google_api_key))
  h = httplib2.Http()
  response, content = h.request(url, 'GET')
  result = json.loads(content)
  latitude = result['results'][0]['geometry']['location']['lat']
  longitude = result['results'][0]['geometry']['location']['lng']
  return latitude, longitude

def findARestaurant(mealType, location):
  # Geocode the location
  restaurantLocation = getGeocodeLocation(location)
  # Search for restaurants
  foursquare_client_id = "LAR4IG2B1UEX3FWYOQCFK44RHADWQOJMFCQ0L5RVOAT2S0XN"
  foursquare_api_key = "TBOW0ORHL51UYCM0S3MCAQRG53B02ZHF1LTEZD12SBSFK3GA"
  foursquare_v = "20200511"
  foursquare_ll = "{},{}".format(restaurantLocation[0], restaurantLocation[1])
  url = 'https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=%s&ll=%s' % (foursquare_client_id, foursquare_api_key, foursquare_v, foursquare_ll)
  # Parse response and return one restaurant
  h = httplib2.Http()
  response, content = h.request(url, 'GET')
  result = json.loads(content)

  restaurant = ""
  for i in result['response']['venues']:
    restaurant = i
    if mealType in i['name']:
      restaurant = i
      break
      
  return restaurant

place1 = findARestaurant("Grill", "Brentwood CA")
print(place1)