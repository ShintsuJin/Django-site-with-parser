from django import template
from ..models import Category
from django.db.models import *


register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def show_categories():
    return Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)



#@register.inclusion_tag('inc/_sidebar.html')
#def show_categories(arg1='Hello'):
#    categories = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)
#    return {'categories': categories, 'arg1': arg1}