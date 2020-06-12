from rex_app.models import *
import bs4
import requests
import random 

def run():
	r = requests.get('https://www.mantelligence.com/random-questions-to-ask/')
	r.raise_for_status()
	html = bs4.BeautifulSoup(r.text)

	for i in range(5):
		Question.objects.create(text=html.select('.questions-to-ask')[random.randint(0,121)].getText())
	
	Question.objects.create(text='test question')