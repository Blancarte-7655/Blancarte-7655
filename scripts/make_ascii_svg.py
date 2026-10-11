"""Retrato ASCII que se "imprime" renglón por renglón (claro y oscuro).

Uso:
  python scripts/make_ascii_svg.py              -> dibuja la luna sobre el mar (por defecto)
  python scripts/make_ascii_svg.py foto.jpg     -> usa tu foto (mejor de frente y con buena luz)
"""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from comun import MONO, TEMAS, guardar, marco

ANCHO, ALTO = 370, 408
COLS, FILAS = 58, 34
CW, LH = 5.85, 10.4          # ancho de letra y alto de renglón
RAMPA = " .`:-=+*cs#%@"      # claro (vacío) -> oscuro (lleno)


def escena_luna():
    """Luna con cráteres, estrellas y mar con reflejo. Blanco = vacío."""
    w, h = 900, 900
    im = Image.new("L", (w, h), 255)
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(7)
    for _ in range(26):  # estrellas
        x, y = rng.integers(20, w - 20), rng.integers(20, 470)
        r = rng.choice([4, 5, 7])
        d.ellipse([x - r, y - r, x + r, y + r], fill=int(rng.integers(30, 120)))
    cx, cy, R = 560, 240, 175  # luna
    yy, xx = np.mgrid[0:h, 0:w]
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    arr = np.array(im, dtype=float)
    luna = dist < R
    # sombreado: más lleno al centro-izquierda, borde suave
    som = 25 + 70 * (np.clip(((xx - cx) + (yy - cy) * .4) / R, -1, 1) + 1) / 2
    arr[luna] = som[luna]
    for (ax, ay, ar, tono) in [(500, 190, 38, 120), (610, 300, 30, 110), (585, 175, 20, 95), (520, 300, 24, 105), (640, 220, 14, 95)]:
        cr = np.sqrt((xx - ax) ** 2 + (yy - ay) ** 2) < ar
        arr[cr & luna] = tono
    halo = (dist >= R) & (dist < R + 40)
    arr[halo] = np.minimum(arr[halo], 200 + (dist[halo] - R) * 1.4)
    # mar: líneas de ola cada vez más juntas hacia el horizonte
    hor = 560
    mar = Image.fromarray(np.clip(arr, 0, 255).astype("uint8"))
    dm = ImageDraw.Draw(mar)
    k = 0
    while True:
        yb = hor + 18 + 9 * k ** 1.45
        if yb > h - 10:
            break
        prof = (yb - hor) / (h - hor)
        amp, lam = 4 + 10 * prof, 60 + 120 * prof
        fase = rng.uniform(0, 6)
        pts = [(x, yb + amp * np.sin(x / lam * 6.28 + fase)) for x in range(0, w + 10, 8)]
        # cortar la línea en tramos para que parezca espuma suave
        for j in range(0, len(pts) - 1):
            if np.sin(j * .23 + fase * 3) > -.2:
                dm.line([pts[j], pts[j + 1]], fill=int(150 - 70 * prof), width=int(4 + 4 * prof))
        k += 1
    arr = np.array(mar, dtype=float)
    # reflejo de la luna
    for y in range(hor, h):
        anc = 40 + (y - hor) * .35
        for x in range(int(cx - anc), int(cx + anc)):
            if np.sin(y * .45 + x * .03) > .1:
                arr[y, x] = min(arr[y, x], 40 + abs(x - cx) / anc * 90 + (y - hor) * .12)
    arr[hor:hor + 5, :] = np.minimum(arr[hor:hor + 5, :], 90)
    return Image.fromarray(np.clip(arr, 0, 255).astype("uint8")).filter(ImageFilter.GaussianBlur(2))


def preparar_foto(ruta):
    import cv2
    im = Image.open(ruta).convert("RGB")
    try:  # quitar fondo si tienes rembg instalado
        from rembg import remove
        rgba = remove(im)
        blanco = Image.new("RGB", rgba.size, "white")
        blanco.paste(rgba, mask=rgba.split()[3])
        im = blanco
    except ImportError:
        pass
    gris = np.array(im.convert("L"))
    gris = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8)).apply(gris)
    return Image.fromarray(gris)


def a_texto(img):
    peq = np.array(img.resize((COLS, FILAS), Image.LANCZOS), dtype=float) / 255
    idx = ((1 - peq) * (len(RAMPA) - 1)).round().astype(int)
    return ["".join(RAMPA[i] for i in fila) for fila in idx]


def svg(t, renglones, comando):
    c = TEMAS[t]
    x0, y0 = 16, 78
    W = COLS * CW
    out = [f'<text x="20" y="56" font-family="{MONO}" font-size="12.5" fill="{c["prompt"]}">osvaldo@blancarte <tspan fill="{c["tenue"]}">~ $</tspan> <tspan fill="{c["tinta"]}">{comando}</tspan></text>']
    defs = []
    for i, r in enumerate(renglones):
        if not r.strip():
            continue
        b = 0.4 + i * 0.07
        y = y0 + i * LH
        defs.append(
            f'<clipPath id="r{i}"><rect x="{x0}" y="{y - LH + 2}" width="0" height="{LH}">'
            f'<animate attributeName="width" from="0" to="{W:.1f}" begin="{b:.2f}s" dur=".32s" fill="freeze"/></rect></clipPath>'
        )
        txt = r.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        out.append(
            f'<text clip-path="url(#r{i})" x="{x0}" y="{y}" textLength="{W:.1f}" lengthAdjust="spacingAndGlyphs" xml:space="preserve" font-family="{MONO}" font-size="9.6" fill="{c["ascii"]}">{txt}</text>'
        )
        out.append(
            f'<rect x="{x0}" y="{y - LH + 2}" width="6" height="{LH - 1}" fill="{c["acento"]}" opacity="0">'
            f'<animate attributeName="x" from="{x0}" to="{x0 + W:.1f}" begin="{b:.2f}s" dur=".32s" fill="freeze"/>'
            f'<animate attributeName="opacity" values="1;1;0" keyTimes="0;.95;1" begin="{b:.2f}s" dur=".33s" fill="freeze"/></rect>'
        )
    cuerpo = f'<defs>{"".join(defs)}</defs>' + "\n".join(out)
    return marco(t, ANCHO, ALTO, "retrato — blancarte", cuerpo)


def main():
    if len(sys.argv) > 1:
        img, comando, nombre = preparar_foto(sys.argv[1]), "cat retrato.txt", "retrato"
    else:
        img, comando, nombre = escena_luna(), "cat luna.txt", "luna"
    renglones = a_texto(img)
    print("\n".join(renglones))
    for t in TEMAS:
        guardar(f"ascii-{t}.svg", svg(t, renglones, comando))


if __name__ == "__main__":
    main()
