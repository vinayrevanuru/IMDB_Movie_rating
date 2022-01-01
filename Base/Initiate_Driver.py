import selenium.webdriver
from selenium.webdriver import Firefox
# we have written two functions for starting and closing browser 
# this code needs to run before all the testcases are run 
from Library import ConfigReader #  init file in library should be created to import it as a module
# this returns the key from the Config file without hardcoding link

def startbrowser():
	global driver

	if ConfigReader.readConfigData('Details','Browser')=="Chrome" :
		PATH = "../Driver/chromedriver.exe"
		driver = selenium.webdriver.Chrome(executable_path=PATH)
	elif ConfigReader.readConfigData('Details','Browser')=="Firefox" :
		PATH = "../Driver/geckodriver.exe"
		driver = Firefox(executable_path=PATH)
	url = ConfigReader.readConfigData('Details','Application_URL')
	#driver.get(url)


	return driver

def closebrowser():
	driver.close()

# startbrowser()