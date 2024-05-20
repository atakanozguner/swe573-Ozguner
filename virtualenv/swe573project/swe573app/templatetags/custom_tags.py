from django import template
import json

register = template.Library()


@register.filter
def dictget(d, k):
    return d.get(k)


@register.filter
def parse_json(json_string):
    return json.loads(json_string)
