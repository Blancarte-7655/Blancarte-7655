"""Todas las herramientas que manejo, agrupadas. Los "fuertes" van resaltados."""
from comun import MONO, TEMAS, esc, guardar, marco

FUERTES = {"JavaScript", "Python", "SQL"}

GRUPOS = [
    ("Lenguajes", ["JavaScript", "Python", "SQL", "TypeScript", "HTML", "CSS", "GLSL", "C"]),
    ("Frontend", ["React", "Next.js", "Vite", "Tailwind CSS"]),
    ("Backend", ["Node.js", "Express", "FastAPI", "WebAuthn"]),
    ("IA y visión", ["PyTorch", "MediaPipe", "OpenCV", "ONNX"]),
    ("Bases de datos", ["MySQL", "SQLite", "MySQL Workbench"]),
    ("Servidor", ["Linux", "Ubuntu", "Hetzner", "Nginx", "PM2", "Cloudflare"]),
    ("Flujo de trabajo", ["Git", "GitHub", "GitHub Actions", "VS Code", "Claude", "Anaconda", "Excel"]),
    ("Otros", ["Code::Blocks", "Octave"]),
    ("Audio y música", ["Ableton Live", "Pro Tools", "Waves", "Valhalla"]),
    ("Foto y video", ["Photoshop", "Lightroom", "Premiere Pro", "DaVinci Resolve"]),
]

ANCHO = 860
COL_X = 168          # donde empiezan los chips
CHIP_H, FS = 24, 11.5
CW = 6.95            # ancho aproximado por letra en monoespaciada a 11.5px


def svg(t):
    c = TEMAS[t]
    y = 36
    out = []
    for g, (titulo, items) in enumerate(GRUPOS):
        d = g * 0.08
        out.append(
            f'<text class="a" style="animation-delay:{d:.2f}s" x="28" y="{y + 16}" font-family="{MONO}" font-size="10.5" letter-spacing="1.6" fill="{c["tenue"]}">{esc(titulo.upper())}</text>'
        )
        x = COL_X
        for k, it in enumerate(items):
            w = len(it) * CW + 24
            if x + w > ANCHO - 24:
                x = COL_X
                y += CHIP_H + 8
            fuerte = it in FUERTES
            fondo = c["acento"] if fuerte else c["barra"]
            borde = c["acento"] if fuerte else c["borde"]
            tinta = c["fondo2"] if fuerte else c["tinta"]
            out.append(
                f'<g class="a" style="animation-delay:{d + .04 * k:.2f}s">'
                f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{CHIP_H}" rx="12" fill="{fondo}" stroke="{borde}"/>'
                f'<text x="{x + w / 2:.1f}" y="{y + 16}" text-anchor="middle" font-family="{MONO}" font-size="{FS}" font-weight="{700 if fuerte else 400}" fill="{tinta}">{esc(it)}</text></g>'
            )
            x += w + 8
        y += CHIP_H + 14
        if g < len(GRUPOS) - 1:
            out.append(f'<line x1="28" y1="{y - 7}" x2="{ANCHO - 28}" y2="{y - 7}" stroke="{c["borde"]}" stroke-opacity=".55"/>')
            y += 6
    y += 4
    out.append(
        f'<g class="a" style="animation-delay:.9s"><rect x="28" y="{y}" width="12" height="12" rx="6" fill="{c["acento"]}"/>'
        f'<text x="48" y="{y + 10}" font-family="{MONO}" font-size="10.5" fill="{c["tenue"]}">mis fuertes</text></g>'
    )
    alto = y + 32
    estilo = ".a{animation:ap .6s ease-out both}@keyframes ap{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}"
    # el marco recorre 22px hacia arriba (espacio de la vieja barra); compenso
    return marco(t, ANCHO, alto, "herramientas", f'<g transform="translate(0,22)">{"".join(out)}</g>', estilo)


if __name__ == "__main__":
    for t in TEMAS:
        guardar(f"stack-{t}.svg", svg(t))
