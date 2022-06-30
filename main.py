import os
import discord
import requests

client = discord.Client()
my_secret = os.environ['TOKEN']
weather_secret = os.environ['open_weather_api_key']


# Get data from Open Weather API
def get_city_geo(c, w):
  url = "http://api.openweathermap.org/geo/1.0/direct"
  querystring = {"q":c,"limit":"1","appid":w}
  payload = ""
  response = requests.request("GET", url, data=payload, params=querystring)
  data = response.json()
  lat = data[0]["lat"]
  lon = data[0]["lon"]
  
  return get_weather(lat, lon)


def get_weather(lt, ln):
  url = "https://api.openweathermap.org/data/2.5/weather"
  querystring = {"lat":lt,"lon":ln,"units":"metric","appid":"9761e7fc685088f96d1501b8eabd19d6"}
  payload = ""
  response =  requests.request("GET", url, data=payload, params=querystring)
  data = response.json()
  description = data["weather"][0]["description"]
  temperature = data["main"]["temp"]
  country = data["name"]
  
  res = {
    "description": description,
    "temperature": temperature,
    "country": country
  }

  
  return res




@client.event
async def on_ready():
  print(f"{client.user} logged in now!")


@client.event
async def on_message(message):
  city = message.content
  
  if city[0] == ".":

    pass

  else:
    
    res = get_city_geo(city, weather_secret)
    await message.channel.send(f'Hey {message.author}, There are {res["description"]} in {res["country"]} and the temperature is {res["temperature"]} deg celcius.')
  



client.run(my_secret)
