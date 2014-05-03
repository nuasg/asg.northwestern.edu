from django import template

register = template.Library()

def darken_part(part):
    return hex(int(int(part, 16) / 1.5))[2:].rjust(2, '0')

@register.filter
def darken(color):
    parts = [color[1:3], color[3:5], color[5:]]
    new_color = ''.join([darken_part(part) for part in parts])
    return '#' + new_color
