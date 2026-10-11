"""Colores y marco de terminal compartidos, al estilo blancarte.lat."""
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(RAIZ, "assets")
DATA = os.path.join(RAIZ, "data")
USUARIO = os.environ.get("GH_USUARIO", "Blancarte-7655")

MONO = "'JetBrains Mono','SFMono-Regular',Consolas,'DejaVu Sans Mono',monospace"
SERIF = "Georgia,'Times New Roman',serif"

TEMAS = {
    # azul noche como el mar de la página
    "oscuro": dict(
        fondo1="#0d1430", fondo2="#080d22", borde="#24305e", barra="#111a3a",
        tinta="#e6e9f2", suave="#aeb7cf", tenue="#6b7699", acento="#a8c4f0",
        linea="#2d5a8c", prompt="#7fa3e0", ascii="#cfd8f0",
        # nivel 0 -> 5: de agua profunda a espuma
        calor=["#141d3f", "#1d2f63", "#2d4a8c", "#4a72c0", "#7fa3e0", "#d4e2ff"],
        puntos=["#e06c75", "#e5c07b", "#98c379"],
    ),
    # blanco perla lavanda como el tema claro
    "claro": dict(
        fondo1="#f4f3f8", fondo2="#e9e7f1", borde="#c9c6da", barra="#e3e1ec",
        tinta="#171a2e", suave="#4a4f66", tenue="#8a87a3", acento="#2d5a8c",
        linea="#6f7fb0", prompt="#2d5a8c", ascii="#1d2547",
        calor=["#e2e0ec", "#c9d3ea", "#93a9d6", "#5a7fbf", "#2d5a8c", "#142a57"],
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
