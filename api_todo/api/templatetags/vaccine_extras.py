from django import template

register = template.Library()

@register.filter
def humanize_days(days):
    """Converte dias em texto amigável (Meses/Anos)"""
    try:
        days = int(days)
    except:
        return days

    if days == 0:
        return "Ao nascer"
    elif days < 30:
        return f"{days} dias"
    elif days < 365:
        months = days // 30
        return f"{months} Meses"
    else:
        years = days // 365
        return f"{years} Anos"