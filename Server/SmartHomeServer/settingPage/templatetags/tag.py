from django import template

register = template.Library()

@register.simple_tag
def label_heading(label):
    return label.split('|')[0]

@register.simple_tag
def label_without_heading(label_tag):
    label_heading = str(label_tag)[str(label_tag).index('>')+1:str(label_tag).index('|')-len(str(label_tag))+1]
    return str(label_tag).replace(label_heading, '', 1)