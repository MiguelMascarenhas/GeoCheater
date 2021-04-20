import time
import config
import requests
from art import *
from seleniumwire import webdriver 
from geopy.geocoders import Nominatim

# Necessary to avoid weird 301 response from GeoGuessr
options = {
    'backend': 'mitmproxy'
}
driver = webdriver.Chrome(executable_path='chromedriver.exe',  seleniumwire_options=options)


def login():
    # Go to "Sign in" url
    driver.get('https://www.geoguessr.com/signin')
    time.sleep(2)
    
    # Enter email
    email_xpath = '/html/body/div[1]/div/main/div/div/div/div/div/form/div/div[1]/div[2]/input'
    driver.find_element_by_xpath(email_xpath).send_keys(config.EMAIL)
    password_xpath = '/html/body/div[1]/div/main/div/div/div/div/div/form/div/div[2]/div[2]/input'
    
    # Enter passowrd
    driver.find_element_by_xpath(password_xpath).send_keys(config.PASSWORD)
    login_button_xpath = '/html/body/div[1]/div/main/div/div/div/div/div/form/div/section/section[2]/div/div/button'
    
    # Click "Sign In" Button
    driver.find_element_by_xpath(login_button_xpath).click()


def interceptor(request):
    # Check if request is from google api
    if 'https://maps.googleapis.com/maps/api/js/GeoPhotoService.GetMetadata' in request.url:
        response = requests.get(request.url, allow_redirects=True)
        coordinates = parse_coordinates_from_response(str(response.content))
        return get_country_by_coordinates(coordinates)


def parse_coordinates_from_response(raw_content):
    # Dirty code to parse .js file respsonse from Google API
    first_relevant_byte = raw_content.find('Google') + 30
    relevant_info = str(raw_content[first_relevant_byte:first_relevant_byte+400])
    coordinates = str(relevant_info[:relevant_info.find(']')])
    return coordinates


# Offline Mode (feel free to test it)
def search_game():
    time.sleep(3)
    play_button_xpath = '//html/body/div[1]/div/main/div/div/div/section[3]/section/section[1]/article/div[2]/div/button'
    driver.find_element_by_xpath(play_button_xpath).click()
    time.sleep(5)
    play_button_xpath = '//html/body/div[1]/div/main/div/div/div/div/div/div/article/div[4]/button'
    driver.find_element_by_xpath(play_button_xpath).click()



def search_battle_royal():
    time.sleep(3)
    # Click "Battle Royal" Button
    play_button_xpath = '/html/body/div/div/main/div/div/div/section[1]/a/div/button'
    driver.find_element_by_xpath(play_button_xpath).click()
    time.sleep(5)
    
    # Click "Play" Button - if popup appears
    button_popup_xpath = '/html/body/div[1]/div/main/div[1]/div/div/div/div/div/div[2]/button'
    if driver.find_element_by_xpath(button_popup_xpath) != None:
        driver.find_element_by_xpath(button_popup_xpath).click()
    
    # Click "Country Battle"
    time.sleep(1)
    play_button_1_xpath = '/html/body/div/div/main/div/div/section/section[1]/div/div/div[1]/div[2]/button'
    driver.find_element_by_xpath(play_button_1_xpath).click()


def get_country_by_coordinates(coordinates):
    # Use Nominatim library to retrieve address based on coordinates
    geolocator = Nominatim(user_agent="'http")
    
    try:
        location = geolocator.reverse(coordinates, language='en')
        
        # Get country from complete address
        country = location.address.split(', ')[-1]
        print(text2art(country))
        return country
    except:
        print("")


# Function that gets executed when a requests is made
driver.request_interceptor = interceptor

# Login
login()

# Search Battle Royal
search_battle_royal()

# This is needed to keep seleniumwire execution (interceptor method)
value = input("SCRIPT ENDED\n")