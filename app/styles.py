"""CSS e pequenos helpers de HTML (chips, cards, topbar)."""
import html as _html

import streamlit as st

_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
.stApp {font-family:'Inter',sans-serif;}
#MainMenu, footer {visibility:hidden;}
header[data-testid="stHeader"] {background:transparent;}
.block-container {padding-top:1.4rem; max-width:1240px;}
section[data-testid="stSidebar"] {border-right:1px solid #E6E8EE;}
section[data-testid="stSidebar"] .stButton > button {width:100%; justify-content:flex-start; text-align:left;}
.cl-logo {font-size:20px; font-weight:600; margin-bottom:12px;}
.cl-ws {border:1px solid #E6E8EE; border-radius:10px; padding:12px; margin-bottom:14px; font-size:14px;}
.cl-ws small {color:#6B7280; font-size:12px;}
.cl-label {font-size:11px; letter-spacing:.05em; color:#6B7280; margin:10px 0 6px;}
.cl-humana {background:#F4F5F8; border-radius:10px; padding:12px; font-size:13px; color:#4B5262;}
.cl-humana b {color:#1F2430;}
.cl-topbar {display:flex; justify-content:space-between; align-items:center; padding-bottom:12px; border-bottom:1px solid #E6E8EE; margin-bottom:18px; color:#6B7280; font-size:14px;}
.cl-topbar b {color:#1F2430; font-weight:500;}
.cl-etapa {font-size:12px; letter-spacing:.05em; color:#6B7280; text-transform:uppercase; margin-top:6px;}
.cl-titulo {font-size:34px; font-weight:500; color:#1F2430; margin:2px 0 4px;}
.cl-sub {color:#6B7280; font-size:16px; margin-bottom:16px;}
.chip {display:inline-block; padding:3px 10px; border-radius:6px; font-size:12px; font-weight:500; margin-right:6px;}
.chip-gray {background:#EEF0F4; color:#4B5262;}
.chip-green {background:#E8F5EC; color:#1E7A46;}
.chip-yellow {background:#FFF3D6; color:#8A5A00;}
.chip-red {background:#FDEBEA; color:#B93A32;}
.chip-purple {background:#EEEAFE; color:#5B3DF5;}
.avatar {display:inline-flex; width:36px; height:36px; border-radius:50%; background:#ECEDF2; color:#4B5262; align-items:center; justify-content:center; font-size:12px; font-weight:600; margin-right:10px; vertical-align:middle;}
.cl-quote {background:#F4F5F8; border-radius:8px; padding:12px 14px; font-size:14px; color:#1F2430;}
.cl-quote small {display:block; font-size:10.5px; letter-spacing:.05em; color:#6B7280; text-transform:uppercase; margin-bottom:4px;}
mark {background:#E4DEFF; color:inherit; padding:1px 2px; border-radius:3px;}
.cl-muted {color:#6B7280; font-size:13px;}
.cl-big {font-size:26px; font-weight:600; color:#1F2430;}
.cl-kv {display:flex; justify-content:space-between; font-size:14px; padding:6px 0;}
.cl-kv span:first-child {color:#6B7280;}
.cl-table {width:100%; border-collapse:collapse; font-size:14px;}
.cl-table th {text-align:left; color:#6B7280; font-weight:500; font-size:12.5px; background:#F4F5F8; padding:10px 12px;}
.cl-table td {padding:14px 12px; border-top:1px solid #EEF0F4; vertical-align:top;}
.cl-table td.mut {color:#6B7280;}
.cl-progress {height:8px; background:#ECEDF2; border-radius:8px; overflow:hidden; margin:10px 0 8px;}
.cl-progress > div {height:100%; background:#5B3DF5;}
.cl-progress.erro > div {background:#B93A32;}
.cl-step {display:flex; align-items:center; gap:14px; padding:14px 0; border-top:1px solid #EEF0F4;}
.cl-step .ico {width:32px; height:32px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:14px; flex:none;}
.ico-ok {background:#E8F5EC; color:#1E7A46;}
.ico-run {background:#EEEAFE; color:#5B3DF5;}
.ico-pen {border:1px dashed #C6CAD4; color:#9AA0AE;}
.ico-err {background:#FDEBEA; color:#B93A32;}
.cl-step .txt {flex:1;}
.cl-step .t {font-weight:500; font-size:15px;}
.cl-step .d {font-size:13px; color:#6B7280;}
.cl-step .s {font-size:13px;}
.s-ok {color:#1E7A46;} .s-run {color:#5B3DF5;} .s-pen {color:#9AA0AE;} .s-err {color:#B93A32;}
.cl-box {border-radius:10px; padding:14px 16px; font-size:14px; margin:10px 0;}
.box-yellow {background:#FFF6E0; color:#8A5A00;}
.box-red {background:#FDEBEA; color:#8F2A24; border:1px solid #F5C6C2;}
.box-gray {background:#EEF0F4; color:#4B5262;}
.box-green {background:#E8F5EC; color:#1E7A46;}
.cl-cardativo {background:#EEEAFE; border-radius:10px; padding:24px; margin-bottom:12px;}
.cl-cardativo .one {font-size:22px; font-weight:700; color:#5B3DF5;}
.cl-cardativo .one small {font-size:11px; font-weight:400; margin-left:8px;}
.cl-cardativo .tit {font-size:24px; font-weight:600; margin:10px 0 6px;}
.cl-cardativo .aut {color:#5B3DF5; font-weight:600;}
.cl-skel {height:14px; border-radius:6px; background:linear-gradient(90deg,#ECEDF2 25%,#F6F7FA 37%,#ECEDF2 63%); background-size:400% 100%; animation:sk 1.4s ease infinite; margin:8px 0;}
@keyframes sk {0% {background-position:100% 50%;} 100% {background-position:0 50%;}}
"""


def compactar(s):
    """Junta as linhas do HTML para o Markdown não tratar recuo como bloco de código."""
    return "".join(linha.strip() for linha in s.splitlines())


def md(s):
    st.markdown(compactar(s), unsafe_allow_html=True)


def injetar_css():
    st.markdown("<style>" + compactar(_CSS) + "</style>", unsafe_allow_html=True)


def esc(texto):
    return _html.escape(str(texto))


def chip(texto, tom="gray"):
    return f'<span class="chip chip-{tom}">{esc(texto)}</span>'


def avatar(iniciais):
    return f'<span class="avatar">{esc(iniciais)}</span>'


def topbar():
    md(
        '<div class="cl-topbar"><span>Espaço de trabalho &nbsp;›&nbsp; <b>Programa ONE</b></span>'
        '<span class="chip chip-gray">Dados demonstrativos</span></div>'
    )


def cabecalho(etapa, titulo, subtitulo, extra=""):
    md(
        f'<div class="cl-etapa">{esc(etapa)}</div>'
        f'<div class="cl-titulo">{esc(titulo)} {extra}</div>'
        f'<div class="cl-sub">{esc(subtitulo)}</div>'
    )


def caixa(tom, conteudo_html):
    md(f'<div class="cl-box box-{tom}">{conteudo_html}</div>')


def destacar(texto, trechos):
    """Escapa o texto e marca os trechos usados nos rascunhos."""
    saida = esc(texto)
    for trecho in trechos:
        saida = saida.replace(esc(trecho), f"<mark>{esc(trecho)}</mark>")
    return saida
