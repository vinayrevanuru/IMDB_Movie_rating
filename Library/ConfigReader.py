from configparser import ConfigParser
# reading config file
def readConfigData(section, key):
    config = ConfigParser()
    config.read("../ConfigurationFiles/Config.ini")
    return config.get(section, key)

# print(readConfigData('Details','Application_URL'))
# running the method and checking if it returns what we want

def read_urls(genre,val):
    url="https://www.imdb.com/search/title/?genres="+genre+"&start="+str(val)
    return url
