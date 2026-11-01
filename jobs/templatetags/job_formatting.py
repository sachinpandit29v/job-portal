from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()


@register.filter
def indian_currency(value):
    """Format a numeric amount with the Indian grouping convention."""
    if value is None or value == '':
        return ''

    try:
        amount = int(value)
    except (TypeError, ValueError):
        return value

    number = str(abs(amount))
    if len(number) > 3:
        last_three = number[-3:]
        remaining = number[:-3]
        groups = []
        while remaining:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        number = ','.join(groups + [last_three])

    sign = '-' if amount < 0 else ''
    return f'{sign}₹{number}'


@register.filter
def lpa(value):
    """Format an annual salary as lakhs per annum."""
    if value is None or value == '':
        return ''

    try:
        amount = Decimal(str(value)) / Decimal('100000')
    except (InvalidOperation, TypeError, ValueError):
        return value

    formatted = f'{amount:.2f}'.rstrip('0').rstrip('.')
    return f'₹{formatted} LPA'
