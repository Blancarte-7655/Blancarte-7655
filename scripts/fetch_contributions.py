"""Baja tu calendario de contribuciones público (sin token) y lo guarda en data/contributions.json.

GitHub sirve el calendario como HTML en https://github.com/users/<usuario>/contributions,
el mismo pedazo que usa tu perfil. Aquí se lee cada día y se calculan las rachas.
"""
import datetime as dt
import json
import os
import re

import requests
from bs4 import BeautifulSoup

from comun import DATA, USUARIO

MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def bajar(usuario):
    r = requests.get(
        f"https://github.com/users/{usuario}/contributions",
        headers={"User-Agent": "Mozilla/5.0 (perfil blancarte.lat)", "Accept": "text/html"},
        timeout=30,
    )
    r.raise_for_status()
    return r.text


def leer(html):
    soup = BeautifulSoup(html, "html.parser")
    # El número exacto viene en el tooltip de cada cuadrito
    tips = {}
    for tip in soup.find_all("tool-tip"):
        m = re.search(r"([\d,]+)\s+contribution", tip.get_text())
        tips[tip.get("for")] = int(m.group(1).replace(",", "")) if m else 0
    dias = []
    for td in soup.select("[data-date]"):
        nivel = int(td.get("data-level", 0) or 0)
        cuenta = tips.get(td.get("id"))
        if cuenta is None:  # formato viejo: data-count
            cuenta = int(td.get("data-count", 0) or 0)
        dias.append({"fecha": td["data-date"], "nivel": nivel, "cuenta": cuenta})
    dias.sort(key=lambda d: d["fecha"])
    return dias


def stats(dias):
    total = sum(d["cuenta"] for d in dias)
    larga = actual = corrida = 0
    for d in dias:
        corrida = corrida + 1 if d["cuenta"] > 0 else 0
        larga = max(larga, corrida)
    # la racha actual cuenta aunque hoy todavía no hayas hecho nada
    hoy = dias[-1] if dias else None
    lista = dias[:-1] if hoy and hoy["cuenta"] == 0 else dias
    for d in reversed(lista):
        if d["cuenta"] == 0:
            break
        actual += 1
    mejor = max(dias, key=lambda d: d["cuenta"]) if dias else None
    mejor_txt = ""
    if mejor and mejor["cuenta"]:
        f = dt.date.fromisoformat(mejor["fecha"])
        mejor_txt = f"{f.day} {MESES[f.month - 1]} ({mejor['cuenta']})"
    return {"total": total, "racha_actual": actual, "racha_larga": larga, "mejor_dia": mejor_txt}


def main():
    dias = leer(bajar(USUARIO))
    if not dias:
        raise SystemExit("No encontré días en el calendario; ¿cambió el HTML de GitHub?")
    os.makedirs(DATA, exist_ok=True)
    salida = {"usuario": USUARIO, "actualizado": dt.date.today().isoformat(), "stats": stats(dias), "dias": dias}
    with open(os.path.join(DATA, "contributions.json"), "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=1)
    print(f"{len(dias)} días · {salida['stats']}")


if __name__ == "__main__":
    main()
