"""Tarjeta tipo `neofetch` con tus datos. Edita FILAS y vuelve a correrlo."""
from comun import MONO, TEMAS, esc, guardar, marco

ANCHO, ALTO = 490, 408

FILAS = [
    ("Estudio", "Ing. en Informática · UdeG"),
    ("De", "Guadalajara, Jalisco"),
    ("Hago", "apps web, IA y servidores"),
    ("Orgullo", "IA de señas · Gaceta UdeG"),
    ("Certificado", "Cisco Cybersecurity"),
    ("Música", "baterista y productor"),
]


def partes(t):
    c = TEMAS[t]
    y = 56
    out = [
        f'<text class="l" style="animation-delay:.1s" x="20" y="{y}" font-family="{MONO}" font-size="12.5" fill="{c["prompt"]}">osvaldo@blancarte <tspan fill="{c["tenue"]}">~ $</tspan> <tspan fill="{c["tinta"]}">neofetch</tspan></text>'
    ]
    y += 30
    out.append(
        f'<text class="l" style="animation-delay:.35s" x="20" y="{y}" font-family="{MONO}" font-size="13" font-weight="700" fill="{c["acento"]}">osvaldo<tspan fill="{c["tenue"]}">@</tspan>blancarte</text>'
    )
    y += 10
    out.append(f'<line class="l" style="animation-delay:.45s" x1="20" y1="{y}" x2="158" y2="{y}" stroke="{c["linea"]}" stroke-dasharray="4 3"/>')
    y += 20
    for i, (k, v) in enumerate(FILAS):
        out.append(
            f'<text class="l" style="animation-delay:{0.55 + i * 0.12:.2f}s" x="20" y="{y}" font-family="{MONO}" font-size="12">'
            f'<tspan fill="{c["acento"]}" font-weight="700">{esc(k)}</tspan><tspan x="130" fill="{c["tinta"]}">{esc(v)}</tspan></text>'
        )
        y += 26
    y += 6
    d = 0.55 + len(FILAS) * 0.12
    for k, col in enumerate(c["calor"] + [c["acento"], c["tinta"]]):
        out.append(f'<rect class="l" style="animation-delay:{d + k * 0.05:.2f}s" x="{20 + k * 24}" y="{y}" width="20" height="12" rx="2" fill="{col}"/>')
    y += 38
    out.append(
        f'<text class="l" style="animation-delay:{d + .35:.2f}s" x="20" y="{y - 6}" font-family="{MONO}" font-size="12" fill="{c["suave"]}">más info en <tspan fill="{c["acento"]}" font-weight="700" text-decoration="underline">blancarte.lat</tspan> ↗</text>'
    )
    y += 26
    out.append(
        f'<text class="l" style="animation-delay:{d + .5:.2f}s" x="20" y="{y}" font-family="{MONO}" font-size="12.5" fill="{c["prompt"]}">osvaldo@blancarte <tspan fill="{c["tenue"]}">~ $</tspan></text>'
    )
    out.append(f'<rect class="cur" x="194" y="{y - 11}" width="8" height="14" fill="{c["acento"]}"/>')
    estilo = (
        ".l{animation:ap .5s ease-out both}"
        "@keyframes ap{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:none}}"
        f".cur{{animation:bl 1.1s steps(1) {d + .7:.2f}s infinite}}@keyframes bl{{0%{{opacity:1}}50%{{opacity:0}}}}"
    )
    return "\n".join(out), estilo


def svg(t):
    cuerpo, estilo = partes(t)
    return marco(t, ANCHO, ALTO, "neofetch — blancarte", cuerpo, estilo)


if __name__ == "__main__":
    for t in TEMAS:
        guardar(f"info-{t}.svg", svg(t))
