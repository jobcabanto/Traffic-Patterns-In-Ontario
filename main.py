
import googlemaps, pandas as pd
from datetime import datetime
from database import DatabaseManagement

dbConnect, dbCursor = DatabaseManagement.connect()

class GoogleMapsData(object):

    def __init__(self):

      # Read off API key from Google Maps Platform stored in text file for best security practice
      
      apiFile, balanceRead = open("gmpAPI.txt", "r"), open("balanceSheet.txt", "r")
      self.apiKey, self.balance, self.requestCounter = apiFile.read(), float(balanceRead.read()), 0
      self.maps = googlemaps.Client(self.apiKey)

    def extract(self, frequency = 25, models = ["best_guess", "pessimistic", "optimistic"], epoch = 1694347200):

      start, end = "place_id:ChIJ1XEjSqNvK4gRMnRwdYfd9GA", "place_id:ChIJlWE7SDypKk0RPHN_Iz2kdvw" # Place IDs from Google (Milton to Orillia respectively)
      insert = """INSERT INTO gmpDatabase (Day_Of_Week, Date, Local_Time, Origin, Destination, Travel_Time, Distance, Transportation, Traffic_Model) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
      
      for i in range(frequency):
        for j in range(len(models)):
          departureTime = epoch + (1800 * i) # UTC | GMT
          weekday = datetime.fromtimestamp(departureTime).strftime('%A')
          date = datetime.fromtimestamp(departureTime).strftime('%B %d, %Y')
          time = datetime.fromtimestamp(departureTime).strftime('%I:%M%p')
          distance = self.maps.directions(origin = start, destination = end, alternatives = True, departure_time = departureTime, traffic_model = models[j])
          distanceInKm = (distance[0]['legs'][0]['distance']['text'])
          durationInHrs = (distance[0]['legs'][0]['duration_in_traffic']['text'])
          # print(distance)
          # print(f"\n{distanceInKm}")
          print(durationInHrs)

            # Insert and commit data into database

          dbCursor.execute(insert, (weekday, date, time, "Milton, Ontario, Canada", "Orillia, Ontario, Canada", durationInHrs, distanceInKm, "driving", models[j]))
          dbConnect.commit()

      self.requestCounter = frequency * len(models)
      self.usage()

    def export(self):
        
      # Transform data into .csv file to eventually transform into .xlsx file for Tableau takeover
      # Extract traffic data from Google Maps Platform (12-hour frequency/month = $45 -> 3000 rows of data)

      db_df = pd.read_sql_query("SELECT * FROM gmpDatabase", dbConnect)
      db_df.to_csv("trafficData.csv", index = False)
      print("File has been exported.")

    def usage(self):
      self.balance -= self.requestCounter * 0.015
      editBalance = open("balanceSheet.txt", "w")
      editBalance.write(f"{(round(self.balance, 3))}")
      editBalance.close()
      print(f"\nCurrent Balance: ${round(self.balance, 3)}\n\nRemember: One request costs $0.015 so use your requests wisely!")

session = GoogleMapsData()
session.export() # | Clear database before running.
# session.export()

# ________________________________________________________________________________________________________________________________________________________________ #

# https://jsfiddle.net/o6rmjyzc/3/
# https://mapstyle.withgoogle.com/ (Retro/Night Mode)

"""

function initMap() {
	
  const styledMapType = new google.maps.StyledMapType(
    [ insert code from mapstyle.withgoogle.com/
],
    { name: "Styled Map" }
  );
  
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 13,
    center: { lat: 43.19273341808923, lng: -79.85823834104112 },
  });
  const trafficLayer = new google.maps.TrafficLayer();
	
  map.mapTypes.set("styled_map", styledMapType);
  map.setMapTypeId("styled_map");
  trafficLayer.setMap(map);
  
}

window.initMap = initMap;

"""