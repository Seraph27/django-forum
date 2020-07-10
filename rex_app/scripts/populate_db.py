from rex_app.models import *
import bs4
import requests
import random 
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
def run():
	r = requests.get('https://www.mantelligence.com/random-questions-to-ask/')
	r.raise_for_status()
	html = bs4.BeautifulSoup(r.text)
	user = None
	try:
		user = User.objects.get(username='admin')		
	except ObjectDoesNotExist:
		user = User.objects.create_superuser('admin', 'admin@example.com', 'pass')
		UserAttribute.objects.create(user=user, background_color=Colors.BLUE)

	for i in range(5):

		Question.objects.create(text=html.select('.questions-to-ask')[random.randint(0,121)].getText(), asked_by=user)
	
	Question.objects.create(text='test question', asked_by=user)