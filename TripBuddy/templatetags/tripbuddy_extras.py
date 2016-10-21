from django import template

register = template.Library()

@register.filter
def appendzero(value):
	value = str(value)
	for i in range(len(value)):
		if value[i] == '.':
			break
	if (i == len(value)):
		return value + '.00'
	if(len(value) - i == 2):
		return value + '0'