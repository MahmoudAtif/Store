from django import template
from shop.models import *

register = template.Library()

@register.simple_tag
def categorys_tags():
    return Category.objects.all()
