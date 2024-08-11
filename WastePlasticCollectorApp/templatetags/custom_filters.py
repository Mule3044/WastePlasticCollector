from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def star_rating(value):
    try:
        value = float(value)
    except (ValueError, TypeError):
        return ''

    full_stars = int(value)
    half_star = 1 if (value - full_stars) >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star

    stars = '<i class="fas fa-star gold"></i>' * full_stars
    if half_star:
        stars += '<i class="fas fa-star-half-alt gold"></i>'
    stars += '<i class="far fa-star"></i>' * empty_stars

    return stars