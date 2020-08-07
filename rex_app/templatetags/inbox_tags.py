from django import template
from rex_app.models import *

register = template.Library()

@register.inclusion_tag('rex_app/tags/inbox/dm_list.html')
def show_dms(dms, user):
    other_person = None
    dm_list = {}
    for dm in dms:
        other_person = dm.to_user if user == dm.from_user else dm.from_user
        
        if other_person not in dm_list:
            dm_list[other_person] = []
        dm_list[other_person].append(dm)
        
    return {'dm_list': dm_list}