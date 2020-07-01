import requests
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class WebRetriever(object):
	def __init__(self):
		pass

	def get_headers(self):
		headers = {
			'authority': 'medium.com',
			'pragma': 'no-cache',
			'cache-control': 'no-cache',
			'dnt': '1',
			'upgrade-insecure-requests': '1',
			'user-agent': 'Mozilla/70.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'sec-fetch-site': 'same-origin',
			'sec-fetch-user': '?1',
			'sec-fetch-mode': 'navigate',
			'sec-fetch-dest': 'document',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
		}
		return headers

	def get_page_source(self, data_url):
		"""
		Get the source of the web page
		:param str data_url: URL of the page
		:return bytes page_source: HTML source of the page
		"""
		if not data_url:
			return None

		response = requests.get(
			url=data_url, 
			verify=True, 
			headers=self.get_headers()
		)
		page_source = response.text

		return page_source

	def get_driver_essentials(self, headless):
		"""
		Get the driver essentials - executable_path and options
		:param bool headless: Headless browser to scrape the data (Chrome is used)
		:return tuple - (driver_path, options):
		"""
		driver_path = os.getcwd() + '/chromedriver'
		options = Options()

		if headless:
			options.add_argument("--headless")
		options.add_argument("--no-sandbox")
		options.add_argument("--remote-debugging-port=9222")
		options.add_argument("--disable-dev-shm-usage")
		options.add_argument("--disable-notifications")

		return driver_path, options

	def js_source_retriever(self, data_url, headless=True):
		"""
		Returns the source of the webpage after rendering JS
		:param str data_url: Link of the webpage
		:return page_content: Source code of the webpage
		"""
		driver_path, options = self.get_driver_essentials(headless=headless)
		driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
		driver.get(url=data_url)
		# driver.implicitly_wait(time_to_wait=5)
		time.sleep(0.75)
		
		page_content = driver.page_source

		driver.close()
		driver.quit()
		
		return page_content
