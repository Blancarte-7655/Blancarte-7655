"""Dibuja data/contributions.json como un calendario animado (claro y oscuro).

Los cuadritos caen en diagonal, una sola vez, como una ola que llega a la orilla.
"""
import datetime as dt
import json
import os

from comun import DATA, MONO, TEMAS, esc, guardar, marco

MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
CEL, GAP = 12, 3
PASO = CEL + GAP
X0, Y0 = 46, 92  # esquina del primer cuadrito


def semanas(dias):
    """Acomoda los días en columnas de domingo a sábado, igual que GitHub."""
    cols, col = [], [None] * 7
    for d in dias:
        f = dt.date.fromisoformat(d["fecha"])
        fila = (f.weekday() + 1) % 7  # domingo = 0
        if fila == 0 and any(col):
            cols.append(col)
            col = [None] * 7
        col[fila] = {**d, "f": f}
    if any(col):
        cols.append(col)
    return cols


def svg(t, datos):
    c = TEMAS[t]
    cols = semanas(datos["dias"])[-53:]
    ancho = 860
    alto = Y0 + 7 * PASO + 40
    cuerpo = []
    cuerpo.append(
        f'<text x="20" y="56" font-family="{MONO}" font-size="12.5" fill="{c["prompt"]}">osvaldo@blancarte <tspan fill="{c["tenue"]}">~ $</tspan> <tspan fill="{c["tinta"]}">./contribuciones.sh</tspan></text>'
    )
    # meses arriba
    ultimo = None
    for i, col in enumerate(cols):
        dia = next((d for d in col if d), None)
        if dia and dia["f"].month != ultimo and dia["f"].day <= 7 and i < len(cols) - 1:
            cuerpo.append(
                f'<text x="{X0 + i * PASO}" y="{Y0 - 8}" font-family="{MONO}" font-size="10" fill="{c["tenue"]}">{MESES[dia["f"].month - 1]}</text>'
            )
            ultimo = dia["f"].month
    for fila, nom in ((1, "lun"), (3, "mié"), (5, "vie")):
        cuerpo.append(
            f'<text x="20" y="{Y0 + fila * PASO + 9.5}" font-family="{MONO}" font-size="10" fill="{c["tenue"]}">{nom}</text>'
        )
    # cuadritos
    for i, col in enumerate(cols):
        for fila, d in enumerate(col):
            if not d:
                continue
            retraso = (i + fila * 2) * 0.018
            tip = f'{d["cuenta"]} contribuciones · {d["f"].day} {MESES[d["f"].month - 1]} {d["f"].year}'
            cuerpo.append(
                f'<rect class="c" style="animation-delay:{retraso:.3f}s" x="{X0 + i * PASO}" y="{Y0 + fila * PASO}" width="{CEL}" height="{CEL}" rx="3" fill="{c["calor"][min(d["nivel"], 5)]}"><title>{esc(tip)}</title></rect>'
            )
    # pie: totales y leyenda
    s = datos["stats"]
    yp = Y0 + 7 * PASO + 30
    partes = [f'<tspan fill="{c["acento"]}" font-weight="700">{s["total"]:,}</tspan> contribuciones en el último año']
    partes.append(f'racha actual <tspan fill="{c["tinta"]}">{s["racha_actual"]} d</tspan>')
    partes.append(f'más larga <tspan fill="{c["tinta"]}">{s["racha_larga"]} d</tspan>')
    if s.get("mejor_dia"):
        partes.append(f'mejor día <tspan fill="{c["tinta"]}">{esc(s["mejor_dia"])}</tspan>')
    sepr = f' <tspan fill="{c["linea"]}">·</tspan> '
    cuerpo.append(
        f'<text class="pie" x="20" y="{yp}" font-family="{MONO}" font-size="11.5" fill="{c["suave"]}">{sepr.join(partes)}</text>'
    )
    lx = ancho - 20 - 6 * PASO - 70
    yp_pie = yp
    yp = 56
    ley = [f'<text x="{lx}" y="{yp}" font-family="{MONO}" font-size="10" fill="{c["tenue"]}">menos</text>']
    for k, col in enumerate(c["calor"]):
        ley.append(f'<rect x="{lx + 38 + k * PASO}" y="{yp - 10}" width="{CEL}" height="{CEL}" rx="3" fill="{col}"/>')
    ley.append(f'<text x="{lx + 42 + 6 * PASO}" y="{yp}" font-family="{MONO}" font-size="10" fill="{c["tenue"]}">más</text>')
    cuerpo.append(f'<g class="pie">{"".join(ley)}</g>')
    yp = yp_pie
    cuerpo.append(
        f'<text class="pie" x="20" y="{yp + 20}" font-family="{MONO}" font-size="9.5" fill="{c["tenue"]}">// se actualiza solo cada día · {esc(datos.get("actualizado", ""))}</text>'
    )
    estilo = (
        ".c{transform-box:fill-box;transform-origin:center;animation:cae .55s cubic-bezier(.2,.8,.2,1) both}"
        "@keyframes cae{from{opacity:0;transform:translateY(-7px) scale(.6)}to{opacity:1;transform:none}}"
        ".pie{animation:ap 1s 1.6s ease-out both}@keyframes ap{from{opacity:0}to{opacity:1}}"
    )
    return marco(t, ancho, alto, "contribuciones — blancarte", "\n".join(cuerpo), estilo)


def main():
    with open(os.path.join(DATA, "contributions.json"), encoding="utf-8") as f:
        datos = json.load(f)
    for t in TEMAS:
        guardar(f"contrib-{t}.svg", svg(t, datos))


if __name__ == "__main__":
    main()
