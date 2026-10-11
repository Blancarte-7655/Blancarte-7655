"""Colores y marco de terminal compartidos, al estilo blancarte.lat."""
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(RAIZ, "assets")
DATA = os.path.join(RAIZ, "data")
USUARIO = os.environ.get("GH_USUARIO", "Blancarte-7655")

MONO = "'JetBrains Mono','SFMono-Regular',Consolas,'DejaVu Sans Mono',monospace"
SERIF = "Georgia,'Times New Roman',serif"

TEMAS = {
    # grafito + plata con un toque de azul (combina con el gris de GitHub)
    "oscuro": dict(
        fondo1="#161b22", fondo2="#0d1117", borde="#30363d", barra="#1c2128",
        tinta="#f0f3f6", suave="#b1bac4", tenue="#7d8590", acento="#bccbe4",
        linea="#56647c", prompt="#a9b6cc", ascii="#c9d1d9",
        # nivel 0 -> 5: de grafito a plata azulada
        calor=["#21262d", "#353c47", "#555f6f", "#7f8ca3", "#aebbd4", "#e3ebfa"],
        puntos=["#e06c75", "#e5c07b", "#98c379"],
    ),
    "claro": dict(
        fondo1="#f6f8fa", fondo2="#eef1f4", borde="#d0d7de", barra="#eaeef2",
        tinta="#1f2328", suave="#4b5563", tenue="#6e7781", acento="#3e4c66",
        linea="#8c96a8", prompt="#3e4c66", ascii="#2b3240",
        calor=["#ebedf0", "#d3d9e2", "#aab4c3", "#7c8799", "#4f5a6c", "#262d38"],
        puntos=["#d4646e", "#d6a84a", "#6fa35a"],
    ),
}


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def marco(t, ancho, alto, titulo, cuerpo, estilo=""):
    """Tarjeta lisa con esquinas redondeadas, como las de blancarte.lat (sin barra de ventana)."""
    c = TEMAS[t]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}" width="{ancho}" height="{alto}" role="img" aria-label="{esc(titulo)}">
<style>{estilo}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
<defs>
<linearGradient id="fd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c['fondo1']}"/><stop offset="1" stop-color="{c['fondo2']}"/></linearGradient>
<clipPath id="ventana"><rect x=".5" y=".5" width="{ancho - 1}" height="{alto - 1}" rx="14"/></clipPath>
</defs>
<g clip-path="url(#ventana)">
<rect width="{ancho}" height="{alto}" fill="url(#fd)"/>
<g transform="translate(0,-22)">
{cuerpo}
</g>
</g>
<rect x=".5" y=".5" width="{ancho - 1}" height="{alto - 1}" rx="14" fill="none" stroke="{c['borde']}"/>
</svg>'''


def guardar(nombre, svg):
    os.makedirs(ASSETS, exist_ok=True)
    ruta = os.path.join(ASSETS, nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(svg)
    print("escrito", os.path.relpath(ruta, RAIZ))
