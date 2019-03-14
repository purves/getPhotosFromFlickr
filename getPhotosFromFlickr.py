from configparser import ConfigParser
import urllib
from pprint import pprint
from loguru import logger
import flickrapi
import os

logger.add(".//output//logs//logs_{time}.log", format="{level}: {message}")
# get flickr authentication details from config file
CONFIG_FILE = './/config//config.ini'
config = ConfigParser()
config.read(CONFIG_FILE)

api_key = config.get("flickr", "api_key")
api_secret = config.get("flickr", "api_secret")
flickr = flickrapi.FlickrAPI(api_key, api_secret)  # , format='parsed-json')
logger.info("Flickr API details: " + api_key + "//" + api_secret)

# make sure to return the date uploaded,
# date taken as well as the URL of the original image
extras = 'url_o,date_taken,date_upload'

count = 0
userID = config.get("query", "user_id")
start_date = config.get("query", "start_date")
logger.info("Query: userID=" + userID + " startDate=" + start_date)
directory = ".//output//photos//" + userID + "//"

SAVE_PHOTOS = config.getboolean("behaviour", "save_photos")
logger.info("Save Photos: " + str(SAVE_PHOTOS))

# for each photo, loop through it and download the original size.
for photo in flickr.walk(user_id=userID,
                         min_upload_date=start_date,
                         extras=extras):

    # keep track of how many have been saved
    count = count + 1

    # write out the photo details
    # logger.debug(str(count) + " --> " + photo.get('id') +
    #             ":" + photo.get('title'))

    # get the url of the original photo
    url = photo.get('url_o')

    # take the filename from the url
    # and route the file to the photos sub directory
    filename = str(count) + "_" + url[url.rfind("/")+1:]

    logger.debug(" " + str(count) + " > " + url + " > " + directory + filename)

    # get the original picture and write it to a file
    if SAVE_PHOTOS:
        if not os.path.exists(directory):
            os.makedirs(directory)
        urllib.request.urlretrieve(url, directory + filename)

# confirm download is complete and how many were saved
logger.info("Processed # photos: " + str(count))
