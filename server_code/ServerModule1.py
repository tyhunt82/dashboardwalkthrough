import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
import random
#import psycopg2 
import anvil.http
  
@anvil.server.callable
def get_revenue():
  return app_tables.revenue.search()
 
@anvil.server.callable
def get_user_signups():
    # Connect and retrieve data from your existing database - example code below
    # conn = psycopg2.connect("host=db.myapp.com dbname=my_app user=postgres password=secret")
    # cur = conn.cursor()
    # cur.execute("""
    #    SELECT COUNT(*), DATE_TRUNC('week', signup_date) AS d
    #         FROM users
    #         WHERE signup_date > NOW() - INTERVAL '3 months'
    #         GROUP BY DATE_TRUNC('week', signup_date)
    #         ORDER BY d;
    #""")
    #return list(cur)
    
    # Here's some dummy data that you might return from your database, as an example
    return [{'signups': 120, 'date':datetime(2019, 6, 10, 0, 0)}, 
            {'signups': 180, 'date':datetime(2019, 6, 3, 0, 0)}, 
            {'signups': 150, 'date':datetime(2019, 5, 27, 0, 0)}]
    
@anvil.server.callable
def get_marketing_data():
  # Connect and retrieve data from your local machine or Jupyter Notebook using the Anvil Uplink

  # Here's a tutorial that explains how to connect to a Jupyter Notebook:
  # https://anvil.works/learn/tutorials/jupyter-notebook-to-web-app
  
  # Here's some dummy data that you might return using the Uplink, as an example:
  return [{'strategy':'Strategy A', 'count':200}, 
          {'strategy':'Strategy B', 'count':185}, 
          {'strategy':'Strategy C', 'count':175}]

@anvil.server.callable
def get_price_data():
  resp = anvil.http.request("https://api.unibit.ai/api/realtimestock/AAPL?AccessKey=demo",
                           json=True)
  # create a datetime object using date and minute data from the api
  return [{'price':x['price'], 'date':datetime.strptime((x['date']+ x['minute']), '%Y%m%d%H:%M:%S')} 
          for x in resp['Realtime Stock price']]


@anvil.server.callable
def get_weather_data(latitude, longitude):
  try:
    resp = anvil.http.request("https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&exclude=hourly,daily&appid=%s&units=imperial" 
        % (latitude, longitude, "43eda1fbcf0b07043eeeac93ae54e1e0"),
        json=True)
    # convert timestamp to datetime object
    time = datetime.fromtimestamp(resp['current']['dt'])
    # return time and temperature data
    return {
      'time':time, 
      'temp':resp['current']['temp']
    }
  except anvil.http.HttpError:
    # If we've exceeded our DarkSky quota, we return some random data for this example
    return {'time':datetime.now(), 'temp':65 + random.uniform(-3, +3)}
  
  
  