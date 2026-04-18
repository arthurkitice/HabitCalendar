import calendar

calendar.setfirstweekday(calendar.SUNDAY)

MESES_BR = (
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    )

def get_days(year, month):
    # Retorna uma lista de listas (semanas)
    # Ex: [[0, 0, 1, 2, 3, 4, 5], [6, 7, ...]]
    weeks = calendar.monthcalendar(year, month)
    
    return [day for week in weeks for day in week]

def get_month_name(month_number):
    if 1 <= month_number <= 12:
        return MESES_BR[month_number - 1]
    return "Mês inválido"

def get_reversed_days(month_number):
    if month_number == 2:
        starting_day = 29 if calendar.isleap(2026) else 28
    else:
        starting_day = 31 if month_number in [1, 3, 5, 7, 8, 10, 12] else 30
    return list(reversed(range(1, starting_day + 1)))