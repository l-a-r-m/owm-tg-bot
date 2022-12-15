import requests
import json
import time
import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime


api_key = '############'

bot_token = '################'

chat_id = '##################'

location = 'Berlin, DE'

# get the weather data from openweathermap
def get_weather_data():
    # get the weather data from openweathermap
    response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=' + location + '&units=metric&&appid=' + api_key)
    # convert the response to json
    weather_data = response.json()
    # return the weather data
    return weather_data
# generate an image with the current weather
def generate_image(weather_data):
    # get the current temperature
    temperature = weather_data['main']['temp']
    # get the low and high temperatures for the day
    low = weather_data['main']['temp_min']
    high = weather_data['main']['temp_max']
    # get the current weather description
    description = weather_data['weather'][0]['description']
    # get the current weather icon
    icon = weather_data['weather'][0]['icon']
    # get the current date and time
    #date_time = datetime.now().strftime('%d/%m/%Y %H:%M')
    # create a new image
    image = Image.new('RGB', (400, 150), color = (0, 0, 0))
    # get a drawing context
    draw = ImageDraw.Draw(image)
    # get the weather icon
    response = requests.get('http://openweathermap.org/img/wn/' + icon + '@4x.png')
    # convert the response to an image
    icon_image = Image.open(BytesIO(response.content))
    # resize the image
    icon_image = icon_image.resize((200, 200), Image.Resampling.LANCZOS)
    # paste the image on the image
    image.paste(icon_image, (230, -30))
    # get a font
    font = ImageFont.truetype('Documents/python/openai/fonts/Roboto-Black.ttf', size=20)
    # draw the location
    draw.text((10, 10), location, fill=(255, 255, 255), font=font)
    # draw the temperature
    draw.text((10, 35), 'Temperature: ' + str(temperature) + '°C', fill=(255, 255, 255), font=font)
    # draw the low and high temperatures
    draw.text((10, 60), str(high) + '°C' + ' / ' +str(low) + '°C', fill=(255, 255, 255), font=font)
    # draw the weather description
    draw.text((10, 110), description, fill=(255, 255, 255), font=font)
    # draw the date and time
    #draw.text((10, 70), 'Date and Time: ' + date_time, fill=(255, 255, 255), font=font)
    # return the image
    return image
# upload the image to a telegram channel
def upload_image(image):
    # convert the image to bytes
    image_bytes = BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)
    # upload the image to the telegram channel
    response = requests.post('https://api.telegram.org/bot' + bot_token + '/sendPhoto?chat_id=' + chat_id, files={'photo': image_bytes})
    # print the response
    print(response.text)
# post the weather data every hour
while True:
    # get the weather data
    weather_data = get_weather_data()
    # generate an image with the current weather
    image = generate_image(weather_data)
    # upload the image to a telegram channel
    upload_image(image)
    # sleep for 15 minutes
    time.sleep(900)