import streamlit as st

from services import data_service as svc
from state import campo, definir, historia_por_id, ir_para, valor
from styles import avatar, cabecalho, chip, destacar, esc, md, topbar

try:  # st.dialog existe a partir da 1.37; antes era experimental
    _dialogo = st.dialog
except AttributeError:  # pragma: no cover
    _dialogo = st.experimental_dialog


def _chave(hid, aid, nome_campo):
    return f"c:{hid}:{aid}:{nome_campo}"


def _aprovar(hid, aid):
    ss = st.session_state
    ss.status_ativos[f"{hid}:{aid}"] = "aprovado"
    ss.toast = "Rascunho aprovado. Nenhum conteúdo foi publicado."


def _desfazer(hid, aid):
    ss = st.session_state
    ss.status_ativos[f"{hid}:{aid}"] = "rascunho"
    ss.motivos.pop(f"{hid}:{aid}", None)
    ss.toast = "Decisão desfeita. O ativo voltou para rascunho."


def _regenerar(hid, aid):
    ss = st.session_state
    h = historia_por_id(hid)
    n = ss.regen.get(f"{hid}:{aid}", 0) + 1
    ss.regen[f"{hid}:{aid}"] = n
    for nome_campo, texto in svc.regenerar(h, aid, n).items():
        definir(_chave(hid, aid, nome_campo), texto)
    ss.toast = "Novo rascunho gerado. Revise antes de aprovar."


def _alternar_copia():
    st.session_state.mostrar_copia = not st.session_state.mostrar_copia


@_dialogo("Rejeitar este rascunho?")
def _dialogo_rejeitar(hid, aid, nome_ativo, autor):
    ss = st.session_state
    st.write(f"O {nome_ativo.lower()} de {autor} será marcado como rejeitado e não ficará pronto para uso pelo time.")
    st.caption("A mensagem original e as evidências serão preservadas.")
    motivo = st.text_area("Motivo da rejeição (opcional)", placeholder="Conte por que este rascunho não deve ser usado.")
    c1, c2 = st.columns(2)
    if c1.button("Cancelar"):
        st.rerun()
    if c2.button("Confirmar rejeição", type="primary"):
        ss.status_ativos[f"{hid}:{aid}"] = "rejeitado"
        ss.motivos[f"{hid}:{aid}"] = motivo.strip()
        ss.toast = "Rascunho rejeitado."
        st.rerun()


def _preview_card(titulo, frase, autor):
    md(f'<div class="cl-cardativo"><div class="one">ONE<small>Oracle Next Education</small></div>'
       f'<div class="tit">{esc(titulo)}</div><div class="aut">{esc(autor)}</div>'
       f'<div style="margin-top:10px;">“{esc(frase)}”</div></div>')


def _coluna_rascunhos(h, ativo, status):
    hid, aid = h["id"], ativo["id"]
    editavel = status == "rascunho"
    if ativo["tipo"] == "texto":
        campo(st.text_area, "Texto do post" if "LinkedIn" in ativo["nome"] else "Texto",
              _chave(hid, aid, "texto"), ativo["campos"]["texto"], height=240, disabled=not editavel)
        texto_atual = valor(_chave(hid, aid, "texto"), "")
        st.caption(f"{len(texto_atual)} caracteres")
        copiavel = texto_atual
    else:
        titulo = valor(_chave(hid, aid, "titulo"), ativo["campos"]["titulo"])
        frase = valor(_chave(hid, aid, "frase"), ativo["campos"]["frase"])
        _preview_card(titulo, frase, h["autor"])
        campo(st.text_input, "Título", _chave(hid, aid, "titulo"), ativo["campos"]["titulo"], disabled=not editavel)
        campo(st.text_input, "Frase de destaque", _chave(hid, aid, "frase"), ativo["campos"]["frase"], disabled=not editavel)
        copiavel = f'{valor(_chave(hid, aid, "titulo"), "")}\n{valor(_chave(hid, aid, "frase"), "")}'
    md(chip("Rascunho gerado por IA", "purple"))
    return copiavel


def render():
    ss = st.session_state
    hid = ss.historia_atual or ss.historias[0]["id"]
    h = historia_por_id(hid)
    topbar()
    cabecalho("Etapa 3 de 4 · Revisar", "Curadoria", "Revise, edite e decida sobre cada rascunho antes de qualquer publicação.")
    st.button("← Voltar para histórias detectadas", on_click=ir_para, args=("historias",))

    with st.container(border=True):
        a, b, c = st.columns([3, 3, 1.5])
        a.markdown(compactar_avatar(h), unsafe_allow_html=True)
        b.markdown(chip(h["categoria"]) + chip(f'Sentimento {h["sentimento"].lower()}', "green"), unsafe_allow_html=True)
        c.markdown(f'<div style="text-align:right;"><span class="cl-muted">Relevância</span> '
                   f'<span style="font-size:22px;">{h["relevancia"]}</span> <span class="cl-muted">/ 100</span></div>',
                   unsafe_allow_html=True)

    esq, dir_ = st.columns([2, 1])
    nomes = [a_["nome"] for a_ in h["ativos"]]
    with esq:
        with st.container(border=True):
            md('<b style="font-size:20px;">Rascunhos gerados</b><br><span class="cl-muted">Confira o conteúdo e ajuste o texto antes de decidir.</span>')
            escolhido = campo(st.radio, "Tipo de ativo", f"aba:{hid}", nomes[0], options=nomes,
                              horizontal=True, label_visibility="collapsed")
            ativo = next(a_ for a_ in h["ativos"] if a_["nome"] == escolhido)
            aid = ativo["id"]
            status = ss.status_ativos[f"{hid}:{aid}"]
            copiavel = _coluna_rascunhos(h, ativo, status)
            st.divider()
            tom = {"rascunho": ("Rascunho", "yellow", "Aguardando revisão humana"),
                   "aprovado": ("Aprovado", "green", "Pronto para uso pelo time"),
                   "rejeitado": ("Rejeitado", "red", "Não ficará pronto para uso")}[status]
            md(f'<span class="cl-muted">Status do ativo</span> &nbsp;{chip(tom[0], tom[1])}'
               f'<span class="cl-muted" style="float:right;">{tom[2]}</span>')
            motivo = ss.motivos.get(f"{hid}:{aid}")
            if status == "rejeitado" and motivo:
                st.caption(f"Motivo: {motivo}")
    with dir_:
        with st.container(border=True):
            md('<b style="font-size:18px;">Evidências</b><br><b style="font-size:14px;">Mensagem original</b>'
               f'<div class="cl-quote" style="margin:8px 0;">“{destacar(h["mensagem_original"], h["destaques"])}”</div>'
               f'<div class="cl-kv"><span>Canal</span><span>{esc(h["canal"])}</span></div>'
               f'<div class="cl-kv"><span>Autor</span><span>{esc(h["autor"])}</span></div>'
               f'<div class="cl-kv"><span>Lote</span><span>{esc(ss.lote_id)}</span></div>'
               + chip("Mensagem fictícia"))
        with st.container(border=True):
            fatos = "".join(f'<div style="margin:8px 0;"><span style="color:#1E7A46;">✓</span> {esc(f)}<br>'
                            f'<span class="cl-muted" style="margin-left:18px;font-size:12px;">Vem da mensagem original</span></div>'
                            for f in h["fatos"])
            md(f'<b style="font-size:18px;">Fatos extraídos</b>{fatos}')
        with st.container(border=True):
            md('<b style="color:#8A5A00;">🛡️ Autorização de uso</b><br><span class="cl-muted">Este conteúdo identifica uma pessoa. '
               "Confirme a autorização da participante antes de aprovar.</span>")
            autorizado = campo(st.checkbox, "Autorização da participante confirmada", f"aut:{hid}", False,
                               disabled=status != "rascunho")

    st.divider()
    b1, b2, b3, b4, b5 = st.columns([1.1, 1.1, 1.3, 2.2, 2])
    if status == "rascunho":
        if b1.button("Rejeitar"):
            _dialogo_rejeitar(hid, aid, ativo["nome"], h["autor"])
        b2.button("↻ Regenerar", on_click=_regenerar, args=(hid, aid))
        b3.button("Copiar texto", on_click=_alternar_copia)
        if not autorizado:
            b4.markdown('<div class="cl-muted" style="text-align:right;padding-top:8px;">Confirme a autorização para aprovar</div>',
                        unsafe_allow_html=True)
        b5.button("✓ Aprovar rascunho", type="primary", disabled=not autorizado, on_click=_aprovar, args=(hid, aid))
    else:
        b1.button("Desfazer decisão", on_click=_desfazer, args=(hid, aid))
        b3.button("Copiar texto", on_click=_alternar_copia)
        if status == "aprovado":
            b5.button("→ Ir para Armazenamento OCI", type="primary", on_click=ir_para, args=("oci",))
        else:
            b5.button("→ Voltar às histórias", type="primary", on_click=ir_para, args=("historias",))
    st.caption("Aprovar não publica. O conteúdo só fica pronto para uso pelo seu time.")
    if ss.mostrar_copia:
        st.code(copiavel, language=None)
        st.caption("Use o ícone no canto do bloco para copiar.")


def compactar_avatar(h):
    return (f'{avatar(h["iniciais"])}<b>{esc(h["autor"])}</b><br>'
            f'<span class="cl-muted" style="margin-left:46px;">{esc(h["canal"])} · {esc(h["origem"])}</span>')
