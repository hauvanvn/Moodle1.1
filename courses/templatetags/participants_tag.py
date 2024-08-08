from django import template

register=template.Library()

@register.simple_tag
def subtraction(val, arg):
    return val - arg

@register.simple_tag
def compare_equal(val, arg):
    return val == arg

@register.simple_tag
def compare_moreRequal(val, arg):
    return val >= arg

@register.simple_tag
def compare_moreThan3(val, arg):
    return (int(val) - int(arg) <= 3) and (int(val) - int(arg) >= 0)