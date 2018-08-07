from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re

import string
import itertools


driver = webdriver.Chrome()

csv_file = open('googleplaystore_alphabet.csv', 'w')
writer = csv.writer(csv_file)

csv_file = open('googleplaystore_alphabet_reviews.csv', 'w')
reviews_writer = csv.writer(csv_file)

writer.writerow(['App', 'Category', 'Rating', 'Reviews', 'Size', 'Installs', 'Type', 'Price', 'Content Rating', 'Genres', 'Last Updated', 'Current Ver', 'Android Ver'])

app_global_list = []

categories = {
			 'ART_AND_DESIGN':['Art & Design'], 
			 'AUTO_AND_VEHICLES': ['Auto & Vehicles'],
			 'BEAUTY' : ['Beauty'],
			 'BOOKS_AND_REFERENCE' :['Books & Reference'], 
			 'BUSINESS' :['Business'],
			 'COMICS': ['Comics'],
			 'COMMUNICATION':['Communication'],
			 'DATING':['Dating'], 
			 'EDUCATION':['Education'], 
			 'ENTERTAINMENT':['Entertainment'], 
			 'EVENTS':['Events'], 
			 'FINANCE':['Finance'], 
			 'FOOD_AND_DRINK' :['Food & Drink'], 
			 'HEALTH_AND_FITNESS': ['Health & Fitness'],
			 'HOUSE_AND_HOME':['House & Home'] , 
			 'LIBRARIES_AND_DEMO':['Libraries & Demo'],
			 'LIFESTYLE' :['Lifestyle'], 
			 'GAME' :['Action', 'Adventure', 'Arcade', 'Board', 'Card', 'Casino', 'Casual', 'Educational','Music', 
			 		'Puzzle', 'Racing', 'Role Playing', 'Simulation', 'Sports', 'Strategy', 'Trivia', 'Word'], 
			 'FAMILY': ['Family', 'Educational', 'Education', 'Pretend Play', 'Entertainment', 'Music & Video',
			 			'Creativity', 'Strategy', 'Brain Games', 'Genius Games', 'Simulation', 'Action & Adventure'
			 			'Word', 'Casual', 'Puzzle', 'Action & Adventure', 'Role Playing'],
			 'MEDICAL' :['Medical'],
			 'SOCIAL' : ['Social'],
			 'SHOPPING' : ['Shopping'],
			 'PHOTOGRAPHY' : ['Photography'],
			 'SPORTS' : ['Sports'],
			 'TRAVEL_AND_LOCAL' : ['Travel & Local'],
			 'TOOLS' : ['Tools'],
			 'PERSONALIZATION' : ['Personalization'],
			 'PRODUCTIVITY' : ['Productivity'],
			 'PARENTING' : ['Parenting'],
			 'WEATHER' : ['Weather'],
			 'VIDEO_PLAYERS' : ['Video Players & Editors'],
			 'NEWS_AND_MAGAZINES' : ['News & Magazines'],
			 'MAPS_AND_NAVIGATION' : ['Maps & Navigation']
			 }


def scroll_to_end():
	SCROLL_PAUSE_TIME = 4

	# Get scroll height
	last_height = driver.execute_script("return document.body.scrollHeight")

	while True:
		# Scroll down to bottom
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# Wait to load page
		time.sleep(SCROLL_PAUSE_TIME)

		# Calculate new scroll height and compare with last scroll height
		new_height = driver.execute_script("return document.body.scrollHeight")

		if new_height == last_height:
			break
		last_height = new_height


#print(search_input)

def f(num_app_elements,search_text_url):
	junk_apps = []

	print('inside f')
	for j in range(0,num_app_elements):

		driver.get(search_text_url)
		scroll_to_end()
		time.sleep(3)
		app_elements = driver.find_elements_by_xpath('//div[@class= "details"]/a[@class="title"]')
		

		try:
			app_id = app_elements[j].get_attribute('href')
		except:
			print('ERORR!!!! - Found in num_app_list but not the actual element')
			continue
		print(app_id)
		try: 
		#bogus app, link does not exist
			driver.get(app_id)
		except:
			junk_apps.append(app_id)
			continue

		print('************ CLICKED APP ' + str(j) + ' *****************')

		wait_app_details = WebDriverWait(driver, 5)
		temp = wait_app_details.until(EC.presence_of_all_elements_located((By.XPATH,
								'//span[@class="htlgb"]')))

		name = driver.find_element_by_xpath('//h1[@itemprop = "name"]/span').text

		try:
			total_reviews = driver.find_element_by_xpath('//span[@class="AYi5wd TBRnV"]/span[@class=""]').text
			total_reviews = int(total_reviews.replace(',',''))
		except:
			total_reviews = 0

		temp = driver.find_elements_by_xpath('//span[@class="T32cc UAO9ie"]/a')
		category_possibilities = [x.text for x in temp]
		print(category_possibilities)


		try:
			rating = driver.find_element_by_xpath('//div[@class="BHMmbe"]').text
			rating[1]
		except:
			rating = 'NaN'
		

		try:
			temp = driver.find_elements_by_xpath('//div[@class="hAyfc"]/div[text()="Updated"]/..//span[@class="htlgb"]')
			last_updated = temp[1].text
		except:
			last_updated = 'NaN'
		try:
			temp = driver.find_elements_by_xpath('//div[@class="hAyfc"]/div[text()="Size"]/..//span[@class="htlgb"]')
			size = temp[1].text
		except:
			size = 'NaN'

		try:
			temp = driver.find_elements_by_xpath('//div[@class="hAyfc"]/div[text()="Installs"]/..//span[@class="htlgb"]')
			installs = temp[1].text
		except:
			installs = 0
		try:
			temp = driver.find_element_by_xpath('//span[@class="oocvOe"]/button').get_attribute('aria-label')
			if 'Buy' in temp:
				paid_or_free = 'Paid'
				price = temp.split(' ')[0]
			else:
				paid_or_free = 'Free'
				price = 0
		except:
			paid_or_free = 'NaN'
		try:
			temp = driver.find_elements_by_xpath('//div[@class="hAyfc"]/div[text()="Current Version"]/..//span[@class="htlgb"]')
			current_version = temp[1].text
		except:
			current_version = 'NaN'
		try:
			temp = driver.find_elements_by_xpath('//div[@class="hAyfc"]/div[text()="Content Rating"]/..//span[@class="htlgb"]')
			content_rating = temp[0].text.split('\n')[0]
		except:
			content_rating = 'NaN'
		try:
			temp = driver.find_elements_by_xpath('//div[@class="hAyfc"]/div[text()="Requires Android"]/..//span[@class="htlgb"]')
			android_req = temp[1].text
		except:
			android_req = 'NaN'

		app_dict={}
		
		if name in app_global_list: #removing duplicates
			#print('DUPLICATE')
			continue
		else:
			#print('NEW APP')
			app_global_list.append(name)


			try:
				#because transaltion will return error if there are special icons present in the name
				transalted_name = translator.translate(name).text
				app_dict['app'] = transalted_name
				print(transalted_name)

			except:
				app_dict['app'] = name
				print(name)

			# CSV HEADERS
			#['App', 'Category', 'Rating', 'Reviews', 'Size', 'Installs', 'Content Rating', 'Last Updated', 'Current Ver', 'Android Ver']
			temp = driver.find_elements_by_xpath('//span[@class="T32cc UAO9ie"]/a')
			category_possibilities = [x.text for x in temp]

			for category in category_possibilities:
				for key_category in categories:
					if category in categories[key_category]:
						app_dict['category'] = key_category

			app_dict['rating'] = rating
			app_dict['total_reviews'] = total_reviews
			app_dict['size'] = size
			app_dict['installs'] = installs
			app_dict['type'] = paid_or_free
			app_dict['price'] = price
			app_dict['content_rating'] = content_rating
			app_dict['genres'] = ";".join(category_possibilities[1:])
			app_dict['last_updated'] = last_updated
			app_dict['current_version'] = current_version
			app_dict['android_req'] = android_req
			#app_dict['support'] = support

			writer.writerow(app_dict.values())
			print('total_reviews = ', total_reviews)
			print( '=' * 50)
			if total_reviews > 100:
				# 'clicking READ ALL REVIEWS'
				try:
					read_all_reviews = driver.find_element_by_xpath('//div[@class="XnFhVd"]/div[@role="button"]')
					get_reviews(read_all_reviews, name)
				except:
					pass

		time.sleep(2)
def get_reviews(read_all_reviews, name):
	#time.sleep(3)
	read_all_reviews.click()
	time.sleep(5)
	scroll_to_end()
	time.sleep(7)
	
	try:
		reviews_elements = driver.find_elements_by_xpath('//div[@jsmodel="y8Aajc"]')
		print('Reviews found = ' , len(reviews_elements)) 
		review_count = 0

		for review in reviews_elements:
			if review_count == 100:
				break
			try:
				full_button = review.find_element_by_xpath('.//button[@jsname="gxjVle"]')
				full_button.click()
			except:
				pass
			text = review.find_element_by_xpath('.//div[@class="UD7Dzf"]').text
			
			if text != '':
				print(text)
				review_dict = {}
				review_dict['name'] = name
				review_dict['text'] = text
				reviews_writer.writerow(review_dict.values())
				review_count = review_count + 1
			else:
				# skip writing empty reviews
				pass
	except:
		pass



url = "https://play.google.com/store/apps"
driver.get(url)
search_input = driver.find_element_by_css_selector('#gbqfq')

alphabets = list(string.ascii_lowercase)

for i in range(1, 4):
	permutations = list(itertools.permutations(alphabets, i))
	for tup in permutations:
		search_text = ''.join(tup)
		print( '^^^^^^ SEARCH STRING : ' + search_text + ' ^^^^^^^^^ ')
		try:
			search_input.send_keys(search_text)
			search_input.send_keys(Keys.ENTER)
			time.sleep(2)
			search_text_url = driver.current_url
			scroll_to_end()
			time.sleep(3)
			num_app_elements = len(driver.find_elements_by_xpath('//div[@class= "details"]/a[@class="title"]'))
			print("Number of apps = " , num_app_elements)
			
			f(num_app_elements,search_text_url)
		except:
			#no results found for permuation search_text
			pass

		driver.get(search_text_url)
		search_input = driver.find_element_by_css_selector('#gbqfq')
		search_input.clear()
		time.sleep(2)

driver.close()
