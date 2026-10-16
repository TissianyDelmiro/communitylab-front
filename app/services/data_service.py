"""Camada de dados do front.

Hoje: devolve dados fictícios (mocks).
Depois: cada função aqui vira uma chamada ao back (Python/n8n/OCI).
As telas só falam com este arquivo, então a troca não mexe nelas.

IMPORTANTE para combinar com o back: o formato dos dicionários abaixo é
PROVISÓRIO. Quem define o contrato oficial é o back.
"""
import copy
import csv
import io
import json

from mocks import mock_data as m

CAMPOS_OBRIGATORIOS = ("autor", "canal", "texto")


# ---------- Ingestão ----------
def _normalizar(itens):
    if not isinstance(itens, list) or not itens:
        raise ValueError("O arquivo precisa conter uma lista com pelo menos uma interação.")
    saida = []
    for i, item in enumerate(itens, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Interação {i}: formato inválido.")
        faltando = [c for c in CAMPOS_OBRIGATORIOS if not str(item.get(c, "")).strip()]
        if faltando:
            raise ValueError(f"Interação {i}: faltam os campos {', '.join(faltando)}.")
        saida.append({
            "autor": str(item["autor"]).strip(),
            "canal": str(item["canal"]).strip(),
            "tipo": str(item.get("tipo") or "mensagem").strip(),
            "texto": str(item["texto"]).strip(),
        })
    return saida


def interacoes_de_json(texto):
    """Aceita uma lista de interações ou um objeto com a chave 'interacoes'."""
    try:
        dados = json.loads(texto)
    except json.JSONDecodeError as erro:
        raise ValueError(f"JSON inválido: {erro.msg} (linha {erro.lineno}).")
    if isinstance(dados, dict) and "interacoes" in dados:
        dados = dados["interacoes"]
    return _normalizar(dados)


def parse_interacoes(nome_arquivo, conteudo):
    """Lê um arquivo CSV ou JSON enviado no upload."""
    nome = nome_arquivo.lower()
    try:
        texto = conteudo.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise ValueError("Não foi possível ler o arquivo. Salve-o em UTF-8.")
    if nome.endswith(".json"):
        return interacoes_de_json(texto)
    if nome.endswith(".csv"):
        return _normalizar(list(csv.DictReader(io.StringIO(texto))))
    raise ValueError("Formato não suportado. Envie um arquivo CSV ou JSON.")


# ---------- Análise ----------
def analisar(interacoes):
    """TODO(back): enviar as interações e receber histórias + ativos gerados."""
    return copy.deepcopy(m.HISTORIAS)


def regenerar(historia, ativo_id, vez):
    """TODO(back): pedir um novo rascunho. Aqui alterna entre variações fictícias."""
    for ativo in historia["ativos"]:
        if ativo["id"] == ativo_id:
            opcoes = [ativo["campos"]] + ativo["variacoes"]
            return dict(opcoes[vez % len(opcoes)])
    return {}


# ---------- OCI ----------
def listar_pacotes():
    """TODO(back): listar objetos do bucket no OCI Object Storage."""
    return copy.deepcopy(m.PACOTES_OCI)


def salvar_no_oci(pacotes, lote_id):
    """TODO(back): gravar o pacote no OCI. Deve ser idempotente (retry não duplica)."""
    return pacotes


def reenviar_pacote(pacote):
    """TODO(back): tentar gravar de novo um pacote que falhou."""
    novo = dict(pacote)
    novo.update({"status": "salvo", "data": "15/10/2026 14:40", "tamanho": "2,4 KB"})
    return novo


def conteudo_pacote(caminho):
    """TODO(back): ler o objeto do bucket. Formato provisório."""
    if caminho.endswith("evidencias.json"):
        return {
            "lote": "DEMO-001",
            "evidencias": [
                {"autor": h["autor"], "canal": h["canal"],
                 "mensagem_original": h["mensagem_original"], "citacoes": h["destaques"], "fatos": h["fatos"]}
                for h in m.HISTORIAS
            ],
        }
    return {
        "status": "sucesso",
        "lote": "DEMO-001",
        "gravado_em": "2026-10-15T14:32:00-03:00",
        "historias": [
            {"autor": h["autor"], "categoria": h["categoria"], "relevancia": h["relevancia"],
             "citacao": h["destaques"][0],
             "ativos": {a["id"]: {"status": "rascunho_aguardando_revisao"} for a in h["ativos"]}}
            for h in m.HISTORIAS
        ],
    }
