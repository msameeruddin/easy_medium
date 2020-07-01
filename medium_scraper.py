from web_retriever import WebRetriever
from bs4 import BeautifulSoup

class MediumScraper(WebRetriever):
	def __init__(self):
		self.medium_url = 'https://medium.com/@{}'

	def get_article_cards(self, avatar_name):
		"""
		Get the HTML source of the url provided with avatar_name
		:param str avatar_name: Avatar name of the user
		:return ResultSet article_segments: Set of article sections
		"""
		if not avatar_name:
			return None

		data_url = self.medium_url.format(avatar_name)
		html_source = self.get_page_source(data_url=data_url)
		article_cards_soup = BeautifulSoup(html_source, features="lxml")

		common_anchors = article_cards_soup.find_all('a', href=True)
		common_titles = article_cards_soup.find_all('h1')
		
		article_segments = [
			(a.parent).parent 
			for a in common_anchors for ht in common_titles if str(ht.text) in str(a.h1)
		]

		return article_segments

	def get_article_titles(self, article_cards):
		"""
		Get the article titles in the form of a list
		:param ResultSet article_cards: List of card details of each article
		:return list article_titles: List of article titles
		"""
		if article_cards:
			article_titles = []
			for segment in article_cards:
				try:
					title_ = segment.h1.get_text(strip=True)
				except Exception as e:
					title_ = None
				article_titles.append(title_)
			return article_titles
		return []

	def get_article_hrefs(self, article_cards):
		"""
		Get the article links in the form of a list
		:param ResultSet article_cards: List of card details of each article
		:return list article_hrefs: List of article hrefs
		"""
		if article_cards:
			article_hrefs = []
			for segment in article_cards:
				try:
					segment_children = segment.find_all(recursive=False)
					anchor_div = segment_children[1]
					href_ = anchor_div.a['href'].split('?source')[0]
					href_ = 'https://medium.com' + href_ if 'https://' not in href_ else href_
				except Exception as e:
					href_ = None
				article_hrefs.append(href_)
			return article_hrefs
		return []

	def get_meta_time(self, article_cards):
		"""
		Get the article published dates in the form of list
		:param ResultSet article_cards: List of card details of each article
		:return list article_dates: List of article published date
		"""
		if article_cards:
			article_dates = []
			for segment in article_cards:
				try:
					meta_div = segment.div.div.div.find_all(recursive=False)[1]
					meta_span = meta_div.find_all(recursive=False)[1]
					meta_date, meta_time = meta_span.get_text().split(' · ')
					meta_date = meta_date.strip()
					meta_time = meta_time.strip()
				except Exception as e:
					meta_date = None
					meta_time = None
				article_dates.append(
					{
						'date_published' : meta_date, 
						'read_time' : meta_time
					}
				)
			return article_dates
		return []

	def get_article_publications(self, article_cards):
		"""
		Get the article pulication details in the form of list
		:param ResultSet article_cards: List of card details of each article
		:return list publications: List of article publications
		"""
		if article_cards:
			publications = []
			for segment in article_cards:
				try:
					meta_div = segment.div.div.div.find_all(recursive=False)[1]
					sub_meta_div = meta_div.find_all(recursive=False)[0]
					pub_text = sub_meta_div.get_text().split(' in ')[1]
				except Exception as e:
					pub_text = 'Self'
				publications.append(pub_text)
			return publications
		return []

	def get_article_images(self, article_cards):
		"""
		Get the article image src's in the form of list
		:param ResultSet article_cards: List of card details of each article
		:return list image_srcs: List of article images
		"""
		if article_cards:
			image_srcs = []
			for segment in article_cards:
				try:
					image_div = segment.find_all(recursive=False)[1]
					src = image_div.img['src'].split('?q')[0]
				except Exception as e:
					src = None
				image_srcs.append(src)
			return image_srcs
		return []

	def get_article_applauds(self, article_cards):
		"""
		Get the article applauds in the form of list
		:param ResultSet article_cards: List of card details of each article
		:return list article_applauds: List of article applauds
		"""
		if article_cards:
			article_applauds = []
			for segment in article_cards:
				try:
					applaud_div = segment.find_all(recursive=False)[2]
					story_applaud = int(applaud_div.h4.get_text(strip=True))
				except Exception as e:
					story_applaud = None
				article_applauds.append(story_applaud)
			return article_applauds
		return []

	def organize_response(self, avatar_name):
		"""
		Get the fetched data in an organized format preferably in the form of dict
		:param str avatar_name: Avatar name of the user
		:return dict medium_user: Fetched data in the form dict
		"""
		if not avatar_name:
			return {}

		article_segments = self.get_article_cards(avatar_name=avatar_name)
		article_titles = self.get_article_titles(article_cards=article_segments)
		article_hrefs = self.get_article_hrefs(article_cards=article_segments)
		article_publications = self.get_article_publications(article_cards=article_segments)
		article_meta_timings = self.get_meta_time(article_cards=article_segments)
		article_images = self.get_article_images(article_cards=article_segments)
		article_applauds = self.get_article_applauds(article_cards=article_segments)

		medium_dumped = [
			{
				'title' : article_titles[i], 
				'href' : article_hrefs[i], 
				'publication' : article_publications[i], 
				'meta_time_data' : article_meta_timings[i], 
				'image_src' : article_images[i],  
				'total_applauds' : article_applauds[i]
			}
			for i in range(len(article_segments))
		]
		medium_user = {avatar_name : medium_dumped}

		return medium_user






if __name__ == '__main__':
	import json
	import os

	os.chdir(os.getcwd() + '/tests')

	ms = MediumScraper()
	avatar_name = 'sameeruddinmohammed'
	medium_user = ms.organize_response(avatar_name=avatar_name)

	with open(avatar_name + '.json', 'w') as jw:
		json.dump(medium_user, jw, ensure_ascii=False, indent=2)

	print('over')

