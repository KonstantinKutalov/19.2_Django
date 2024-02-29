from django import template

register = template.Library()

@register.filter
def add_media_prefix(value):
    if value:
        if value.startswith('/media/'):
            return value  # Если да, просто возвращаем значение без изменений
        else:
            return f'/media/{value}'
    return '#'  # Если значение пустое, возвращаем #
