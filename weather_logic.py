"""Funções pequenas para validar e formatar a resposta do bot de clima."""

from __future__ import annotations

import unicodedata
import math
from typing import Any


def normalizar_cidade(texto: str) -> str:
    """Remove espaços extras, acentos e diferenças de caixa do texto recebido."""
    texto = " ".join(texto.split())
    sem_acentos = "".join(
        caractere
        for caractere in unicodedata.normalize("NFD", texto)
        if unicodedata.category(caractere) != "Mn"
    )
    return sem_acentos.lower()


def montar_resposta(dados: Any, texto_original: str) -> dict[str, Any]:
    """Converte uma resposta OpenWeather em uma mensagem segura para o Telegram."""
    erro = "❌ Cidade não encontrada. Use o formato Cidade,UF,BR (ex.: São Paulo,SP,BR)."
    if not isinstance(dados, dict):
        return {"ok": False, "message": erro}

    try:
        codigo = int(dados.get("cod", 200))
        temperatura = float(dados["main"]["temp"])
        cidade = str(dados["name"]).strip()
    except (KeyError, TypeError, ValueError):
        return {"ok": False, "message": erro}

    if codigo != 200 or not cidade or not math.isfinite(temperatura):
        return {"ok": False, "message": erro}

    return {
        "ok": True,
        "message": f"🌤️ A temperatura em {cidade} é de {math.floor(temperatura + 0.5)}°C.",
        "consulta": normalizar_cidade(texto_original),
    }
