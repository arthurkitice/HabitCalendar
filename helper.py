import calendar
import cairosvg
import io
from PIL import Image
import customtkinter as ctk

calendar.setfirstweekday(calendar.SUNDAY)

MESES_BR = (
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    )

def carregar_icone_svg(caminho_arquivo, tamanho_icone):
    # Multiplicamos o tamanho desejado por 4 para garantir nitidez 
    largura_render = tamanho_icone[0] * 4
    altura_render = tamanho_icone[1] * 4

    png_bytes = cairosvg.svg2png(
        url=caminho_arquivo, 
        output_width=largura_render, 
        output_height=altura_render
    )
    
    imagem_memoria = io.BytesIO(png_bytes)
    imagem_pillow = Image.open(imagem_memoria)
    
    return ctk.CTkImage(light_image=imagem_pillow, dark_image=imagem_pillow, size=tamanho_icone)

def get_days(year, month):
    # Retorna uma lista de listas (semanas)
    # Ex: [[0, 0, 1, 2, 3, 4, 5], [6, 7, ...]]
    weeks = calendar.monthcalendar(year, month)
    
    return [day for week in weeks for day in week]

def get_reversed_days(month_number, year):
    if month_number == 2:
        starting_day = 29 if calendar.isleap(year) else 28
    else:
        starting_day = 31 if month_number in [1, 3, 5, 7, 8, 10, 12] else 30
    return list(reversed(range(1, starting_day + 1)))

def format_month_text(checked_days: int) -> str:
    """Formata o texto de estatísticas para os botões dos meses."""
    if checked_days == 0:
        return " "
    elif checked_days == 1:
        return "1 marcação"
    return f"{checked_days} marcações"

def format_year_text(checked_days: int) -> str:
    """Formata o texto de estatísticas para o cabeçalho do ano."""
    if checked_days == 0:
        return "Sem marcações"
    elif checked_days == 1:
        return "Uma marcação"
    return f"{checked_days} marcações"