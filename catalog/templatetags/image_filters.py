from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter
def add_border(image_url, border_color="black", border_width=5):
    return format_html('<img src="{}" style="border: {}px solid {};" />', image_url, border_width, border_color)
