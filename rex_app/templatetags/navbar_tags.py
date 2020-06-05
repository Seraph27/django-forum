from django import template
from rex_app.models import *

register = template.Library()

@register.inclusion_tag('rex_app/tags/navbar/question_dropdown.html')
def show_question_dropdown():
    return {'questions': Question.objects.all()}