"""Herramientas que manejo, con su icono. Los "fuertes" van resaltados.

Los iconos viven en scripts/iconos/ (Simple Icons y Devicon), así que no se
descarga nada al generar. Para agregar uno: pon su .svg ahí y súmalo a GRUPOS.
"""
import base64
import json
import os

from comun import MONO, TEMAS, esc, guardar, marco

AQUI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "iconos")
COLORES = json.load(open(os.path.join(AQUI, "colores.json"), encoding="utf-8"))

FUERTES = {"JavaScript", "Python", "SQL"}

# (nombre visible, icono)   icono: "si-slug" | "dv-nombre" | "db" | "XX:#fondo:#letra" (monograma)
GRUPOS = [
    ("Lenguajes", [("JavaScript", "si-javascript"), ("Python", "si-python"), ("SQL", "db"),
                   ("TypeScript", "si-typescript"), ("HTML", "si-html5"), ("CSS", "si-css"),
                   ("GLSL", "si-opengl"), ("C", "si-c")]),
    ("Frontend", [("React", "si-react"), ("Next.js", "si-nextdotjs"), ("Vite", "si-vite"), ("Tailwind", "si-tailwindcss")]),
    ("Backend", [("Node.js", "si-nodedotjs"), ("Express", "si-express"), ("FastAPI", "si-fastapi"), ("WebAuthn", "si-webauthn")]),
    ("IA y visión", [("PyTorch", "si-pytorch"), ("MediaPipe", "si-mediapipe"), ("OpenCV", "si-opencv"), ("ONNX", "si-onnx")]),
    ("Bases de datos", [("MySQL", "si-mysql"), ("SQLite", "si-sqlite"), ("Workbench", "si-mysql")]),
    ("Servidor", [("Linux", "si-linux"), ("Ubuntu", "si-ubuntu"), ("Hetzner", "si-hetzner"), ("Nginx", "si-nginx"),
                  ("PM2", "si-pm2"), ("Cloudflare", "si-cloudflare")]),
    ("Flujo de trabajo", [("Git", "si-git"), ("GitHub", "si-github"), ("Actions", "si-githubactions"),
                          ("VS Code", "dv-vscode"), ("Claude", "si-claude"), ("Anaconda", "si-anaconda"),
                          ("Excel", "X:#107C41:#ffffff"), ("CodeBlocks", "si-codeblocks"), ("Octave", "si-octave")]),
    ("Audio y música", [("Ableton", "Ab:#111111:#ffffff"), ("Pro Tools", "si-protools"),
                        ("Waves", "W:#0b3b6f:#ffffff"), ("Valhalla", "V:#3b2a5c:#e9dcff")]),
    ("Foto y video", [("Photoshop", "dv-photoshop"), ("Lightroom", "Lr:#001E36:#31A8FF"),
                      ("Premiere", "dv-premierepro"), ("DaVinci", "si-davinciresolve")]),
]

ANCHO = 860
COL_X = 178
TW, TH = 73, 66      # tamaño de cada mosaico
ICO = 26


def luz(hexa):
    h = hexa.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def data_uri(svg_txt):
    return "data:image/svg+xml;base64," + base64.b64encode(svg_txt.encode()).decode()


def icono(t, clave, x, y):
    c = TEMAS[t]
    if clave == "db":  # cilindro de base de datos
        col = c["acento"]
        return (f'<g fill="none" stroke="{col}" stroke-width="2"><ellipse cx="{x + 13}" cy="{y + 6}" rx="10" ry="4"/>'
                f'<path d="M{x + 3} {y + 6}v14c0 2.2 4.5 4 10 4s10-1.8 10-4V{y + 6}"/><path d="M{x + 3} {y + 13}c0 2.2 4.5 4 10 4s10-1.8 10-4"/></g>')
    if ":" in clave:  # monograma
        letras, fondo, tinta = clave.split(":")
        return (f'<rect x="{x}" y="{y}" width="{ICO}" height="{ICO}" rx="6" fill="{fondo}"/>'
                f'<text x="{x + ICO / 2}" y="{y + 17.5}" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" fill="{tinta}">{esc(letras)}</text>')
    txt = open(os.path.join(AQUI, clave + ".svg"), encoding="utf-8").read()
    if clave.startswith("si-"):
        col = "#" + COLORES[clave[3:]]
        # colores muy oscuros o muy claros se ajustan al tema para que se vean
        if t == "oscuro" and luz(col) < 0.22:
            col = c["tinta"]
        if t == "claro" and luz(col) > 0.62:  # en fondo claro, oscurecer los muy claros
            h = col.lstrip("#")
            col = "#" + "".join(f"{int(int(h[i:i + 2], 16) * .68):02x}" for i in (0, 2, 4))
        txt = txt.replace("<svg ", f'<svg fill="{col}" ', 1)
    return f'<image x="{x}" y="{y}" width="{ICO}" height="{ICO}" href="{data_uri(txt)}"/>'


def svg(t):
    c = TEMAS[t]
    y = 26
    out = []
    for g, (titulo, items) in enumerate(GRUPOS):
        d = g * 0.07
        x = COL_X
        fila_y = y
        out.append(f'<text class="a" style="animation-delay:{d:.2f}s" x="28" y="{y + 37}" font-family="{MONO}" font-size="10.5" letter-spacing="1.6" fill="{c["tenue"]}">{esc(titulo.upper())}</text>')
        for k, (nombre, clave) in enumerate(items):
            if x + TW > ANCHO - 20:
                x = COL_X
                fila_y += TH + 8
            fuerte = nombre in FUERTES
            out.append(
                f'<g class="a" style="animation-delay:{d + .03 * k:.2f}s">'
                f'<rect x="{x}" y="{fila_y}" width="{TW - 8}" height="{TH}" rx="12" fill="{c["barra"]}" '
                f'stroke="{c["acento"] if fuerte else c["borde"]}" stroke-width="{1.6 if fuerte else 1}"/>'
                f'{icono(t, clave, x + (TW - 8 - ICO) / 2, fila_y + 10)}'
                f'<text x="{x + (TW - 8) / 2}" y="{fila_y + 54}" text-anchor="middle" font-family="{MONO}" font-size="9.6" '
                f'font-weight="{700 if fuerte else 400}" fill="{c["acento"] if fuerte else c["suave"]}">{esc(nombre)}</text></g>'
            )
            x += TW
        y = fila_y + TH + 14
        if g < len(GRUPOS) - 1:
            out.append(f'<line x1="28" y1="{y - 7}" x2="{ANCHO - 28}" y2="{y - 7}" stroke="{c["borde"]}" stroke-opacity=".5"/>')
            y += 6
    out.append(
        f'<g class="a" style="animation-delay:.8s"><rect x="28" y="{y + 2}" width="14" height="14" rx="4" fill="none" stroke="{c["acento"]}" stroke-width="1.6"/>'
        f'<text x="50" y="{y + 13}" font-family="{MONO}" font-size="10.5" fill="{c["tenue"]}">mis fuertes</text></g>'
    )
    alto = y + 34
    estilo = ".a{animation:ap .6s ease-out both}@keyframes ap{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}"
    return marco(t, ANCHO, alto, "Herramientas que uso", f'<g transform="translate(0,22)">{"".join(out)}</g>', estilo)


if __name__ == "__main__":
    for t in TEMAS:
        guardar(f"stack-{t}.svg", svg(t))
