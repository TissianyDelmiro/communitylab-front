"""Estado da aplicação (st.session_state) e helpers.

Obs.: o Streamlit apaga o estado de widgets que não aparecem numa execução
(por exemplo ao trocar de tela). Por isso os valores editáveis ficam em
st.session_state.dados e os widgets só os espelham (ver campo()).
"""
import copy

import streamlit as st

from mocks import mock_data as m
from services import data_service as svc

MENU = [
    ("ingestao", "📥  Ingestão"),
    ("historias", "💬  Histórias detectadas"),
    ("curadoria", "✅  Curadoria"),
    ("oci", "🗄️  Armazenamento OCI"),
]
CATEGORIA_TODAS = "Todas as categorias"
CANAL_TODOS = "Todos os canais"


def init_state():
    ss = st.session_state
    if ss.get("_iniciado"):
        return
    ss._iniciado = True
    ss.pagina = "ingestao"
    ss.dados = {}
    ss.interacoes = copy.deepcopy(m.INTERACOES)
    ss.arquivo = {"nome": m.ARQUIVO_DEMO, "tamanho": m.ARQUIVO_DEMO_TAMANHO, "origem": "Arquivo JSON"}
    ss.lote_id = m.LOTE_ID
    ss.ultimo_upload = None
    ss.historias = svc.analisar(ss.interacoes)
    ss.proc_status = "novo"  # novo | retry | erro | concluido
    ss.proc_etapas = ["pendente"] * 6
    ss.historia_atual = None
    ss.status_ativos = {}  # "hist:ativo" -> rascunho | aprovado | rejeitado
    ss.motivos = {}
    ss.regen = {}
    ss.pacotes_oci = svc.listar_pacotes()
    ss.toast = None
    ss.mostrar_copia = False
    for h in ss.historias:
        for a in h["ativos"]:
            ss.status_ativos[f"{h['id']}:{a['id']}"] = "rascunho"


def reiniciar():
    st.session_state.clear()


def ir_para(pagina):
    st.session_state.pagina = pagina


def campo(widget, label, chave, padrao, **kwargs):
    """Cria um widget cujo valor sobrevive à troca de tela."""
    ss = st.session_state
    wkey = f"w::{chave}"
    if chave not in ss.dados:
        ss.dados[chave] = padrao
    if wkey not in ss:
        ss[wkey] = ss.dados[chave]

    def _sincronizar():
        ss.dados[chave] = ss[wkey]

    return widget(label, key=wkey, on_change=_sincronizar, **kwargs)


def definir(chave, valor):
    """Altera um valor guardado e o widget que o espelha (use antes do widget ou em callbacks)."""
    ss = st.session_state
    ss.dados[chave] = valor
    ss[f"w::{chave}"] = valor


def valor(chave, padrao=None):
    return st.session_state.dados.get(chave, padrao)


def historia_por_id(hid):
    for h in st.session_state.historias:
        if h["id"] == hid:
            return h
    return None


def resumo_ativos():
    """Conta ativos por status em todas as histórias."""
    contagem = {"rascunho": 0, "aprovado": 0, "rejeitado": 0}
    for status in st.session_state.status_ativos.values():
        contagem[status] += 1
    return contagem
