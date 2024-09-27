from django import template

register = template.Library()

@register.filter
def setstatus(status):
    return "จองแล้ว" if status == "booked" else "ว่าง"
