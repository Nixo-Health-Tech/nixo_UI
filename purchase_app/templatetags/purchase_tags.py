from django import template
register = template.Library()

@register.filter
def get_credit_cost(products, key):
    for p in products:
        if p.slug == key:
            return p.meta.get('credit_cost', '—')
    return '—'
