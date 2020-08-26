# from .models import YourModel
from django import template
register = template.Library()

@register.simple_tag
def create_stack(stack):
    array = []
    for item in stack:
        array.append(item)
    return array

@register.simple_tag
def pop_item_from_stack(stack):
    return stack.pop(0)

@register.simple_tag
def push_item_onto_stack(stack, item):
    stack.insert(0, item)
    return stack
