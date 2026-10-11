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


PRINCIPALES = [
    ("JavaScript", "si-javascript"), ("Python", "si-python"), ("SQL", "db"), ("TypeScript", "si-typescript"),
    ("React", "si-react"), ("Next.js", "si-nextdotjs"), ("Node.js", "si-nodedotjs"), ("FastAPI", "si-fastapi"),
    ("PyTorch", "si-pytorch"), ("OpenCV", "si-opencv"), ("MySQL", "si-mysql"), ("Linux", "si-linux"),
    ("Nginx", "si-nginx"), ("Cloudflare", "si-cloudflare"), ("Git", "si-git"), ("Ableton", "Ab:#111111:#ffffff"),
    ("Pro Tools", "si-protools"), ("DaVinci", "si-davinciresolve"),
]


def svg(t):
    c = TEMAS[t]
    por_fila, tw, th, gap = 9, 84, 70, 8
    x0 = (ANCHO - (por_fila * tw + (por_fila - 1) * gap)) / 2
    out = []
    for k, (nombre, clave) in enumerate(PRINCIPALES):
        x = x0 + (k % por_fila) * (tw + gap)
        y = 22 + (k // por_fila) * (th + gap)
        fuerte = nombre in FUERTES
        out.append(
            f'<g class="a" style="animation-delay:{k * .03:.2f}s">'
            f'<rect x="{x:.1f}" y="{y}" width="{tw}" height="{th}" rx="12" fill="{c["barra"]}" '
            f'stroke="{c["acento"] if fuerte else c["borde"]}" stroke-width="{1.6 if fuerte else 1}"/>'
            f'{icono(t, clave, x + (tw - ICO) / 2, y + 11)}'
            f'<text x="{x + tw / 2:.1f}" y="{y + 57}" text-anchor="middle" font-family="{MONO}" font-size="10" '
            f'font-weight="{700 if fuerte else 400}" fill="{c["acento"] if fuerte else c["suave"]}">{esc(nombre)}</text></g>'
        )
    filas = (len(PRINCIPALES) + por_fila - 1) // por_fila
    alto = 22 + filas * (th + gap) + 14
    estilo = ".a{animation:ap .6s ease-out both}@keyframes ap{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}"
    return marco(t, ANCHO, alto, "Herramientas que uso", f'<g transform="translate(0,22)">{"".join(out)}</g>', estilo)


if __name__ == "__main__":
    for t in TEMAS:
        guardar(f"stack-{t}.svg", svg(t))
