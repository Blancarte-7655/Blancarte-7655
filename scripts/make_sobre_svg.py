"""Une el retrato ASCII y la tarjeta neofetch en una sola imagen (sin bordes de tabla).

Uso:
  python scripts/make_sobre_svg.py              -> luna sobre el mar
  python scripts/make_sobre_svg.py foto.jpg     -> tu foto en ASCII
"""
import make_ascii_svg as ascii_
import make_info_card as info
from comun import TEMAS, guardar, marco

ANCHO, ALTO = 860, 408


def svg(t, renglones, comando, mov):
    c = TEMAS[t]
    a_cuerpo, a_estilo = ascii_.partes(t, renglones, comando, mov)
    i_cuerpo, i_estilo = info.partes(t)
    cuerpo = (
        f'{a_cuerpo}'
        f'<line x1="372" y1="58" x2="372" y2="{ALTO - 10}" stroke="{c["borde"]}"/>'
        f'<g transform="translate(372,0)">{i_cuerpo}</g>'
    )
    return marco(t, ANCHO, ALTO, "Sobre mí: retrato en ASCII y datos tipo neofetch", cuerpo, a_estilo + i_estilo)


if __name__ == "__main__":
    renglones, comando, mov = ascii_.generar()
    for t in TEMAS:
        guardar(f"sobre-{t}.svg", svg(t, renglones, comando, mov))
