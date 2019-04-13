from selenium import webdriver
from threading import Lock

OVERRIDE_USERAGENT = 'general.useragent.override'
USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'

lock = Lock()

def start():
	global drivers
	profile = webdriver.FirefoxProfile()
	profile.set_preference(OVERRIDE_USERAGENT, USERAGENT)

	drivers = [None] * 3
	for i in range(len(drivers)):
		drivers[i] = webdriver.Firefox(profile)

def open_url(url, driver=-1):
		drivers[driver].get(url)

def get_source(driver=-1):
		return drivers[driver].page_source