import requests
from bs4 import BeautifulSoup
import re

url_page1 = 'https://www.whitehouse.gov/briefing-room/press-briefings/'
url_page_other_pages = 'https://www.whitehouse.gov/briefing-room/press-briefings/page/'

# url_page1 = 'https://www.whitehouse.gov/briefing-room/speeches-remarks/'
# url_page_other_pages = 'https://www.whitehouse.gov/briefing-room/speeches-remarks/page/'

current_page = 1
pages_to_check = 1
articles_to_check = []
word_to_search_for = ' clear '
secondary_to_search_for = 'very'
occurances = []
chars_surrounding = 40

while current_page <= pages_to_check:
	#print(current_page)

	if current_page == 1:
		response = requests.get(url_page1)
	else:
		response = requests.get(url_page_other_pages + f'{current_page}/')

	html = response.text

	soup = BeautifulSoup(html,'html.parser')

	articles = soup.find_all('a', class_='news-item__title')

	for article in articles:
		articles_to_check.append(article['href'])
	current_page = current_page + 1

print(f'{len(articles_to_check)} Articles')

for articles_to_check in articles_to_check:
	print(articles_to_check)
	article_html = requests.get(articles_to_check)
	soup = BeautifulSoup(article_html.text,'html.parser')
	for br in soup.find_all('br'):
  		br.decompose()		
	transcript = soup.find_all('p', class_='')
	for p in transcript:
		all_occurances = [m.start() for m in re.finditer(word_to_search_for, p.text)]
		if len(all_occurances):
			for occurance in all_occurances:
				this_occurance = p.text[occurance-chars_surrounding:occurance+chars_surrounding+len(word_to_search_for)]
				this_occurance = this_occurance.replace(u'\xa0', u' ')
				secondary_array = [m.start() for m in re.finditer(secondary_to_search_for, this_occurance)]
				occurances.append(this_occurance + f' -- [{len(secondary_array)}] -- {soup.title.text}')

for occurance in occurances:
	print(occurance)