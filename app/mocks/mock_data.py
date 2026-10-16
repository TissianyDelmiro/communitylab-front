"""Dados FICTÍCIOS usados só pelo front enquanto o back não existe.

Nada aqui representa pessoas ou depoimentos reais.
Quando o back estiver pronto, o ideal é que o front deixe de importar
este arquivo e passe a usar apenas services/data_service.py.
"""

BUCKET = "communitylab-ativos-marketing"
LOTE_ID = "DEMO-001"
ARQUIVO_DEMO = "one_comunidade_demo.json"
ARQUIVO_DEMO_TAMANHO = "2,4 KB"

INTERACOES = [
    {"autor": "Marina Costa", "canal": "#conquistas", "tipo": "mensagem",
     "texto": "Consegui minha primeira vaga como dev júnior! O portfólio que construí no ONE fez a diferença."},
    {"autor": "Lucas Almeida", "canal": "#projetos", "tipo": "mensagem",
     "texto": "Nosso projeto de controle financeiro foi destaque no desafio. Fizemos tudo em equipe!"},
    {"autor": "Camila Santos", "canal": "#carreira", "tipo": "mensagem",
     "texto": "Depois de 10 anos no varejo, concluí a formação e comecei minha transição para tecnologia."},
    {"autor": "Rafael Lima", "canal": "#geral", "tipo": "mensagem",
     "texto": "Alguém sabe qual é o horário da próxima mentoria?"},
    {"autor": "Beatriz Nunes", "canal": "#geral", "tipo": "mensagem",
     "texto": "Bom dia, pessoal! Começando a semana com bastante energia."},
    {"autor": "Pedro Alves", "canal": "#projetos", "tipo": "mensagem",
     "texto": "Alguém tem um exemplo de como organizar as pastas do projeto?"},
]

# tipo do ativo: "texto" (um campo de texto) ou "card" (título + frase de destaque)
HISTORIAS = [
    {
        "id": "hist-001",
        "autor": "Marina Costa",
        "iniciais": "MC",
        "canal": "#conquistas",
        "origem": "Mensagem da comunidade",
        "categoria": "Conquista profissional",
        "sentimento": "Positivo",
        "relevancia": 96,
        "mensagem_original": "Consegui minha primeira vaga como dev júnior! O portfólio que construí no ONE fez a diferença.",
        "destaques": ["primeira vaga como dev júnior!", "O portfólio que construí no ONE fez a diferença."],
        "fatos": ["Conquista: primeira vaga como dev júnior", "Origem: portfólio construído no ONE"],
        "ativos": [
            {"id": "post_linkedin", "nome": "Post para LinkedIn", "tipo": "texto",
             "campos": {"texto": "Ver uma pessoa da comunidade conquistar a primeira vaga na área é o que dá sentido a tudo. "
                                 "A Marina Costa conseguiu a primeira vaga como dev júnior e contou que o portfólio construído "
                                 "no ONE fez a diferença. Parabéns, Marina! 👏 #ProgramaONE #CarreiraTech"},
             "variacoes": [{"texto": "Primeira vaga como dev júnior! A Marina Costa conseguiu e destacou que o portfólio "
                                     "construído no ONE fez a diferença. Parabéns, Marina! 🚀 #ProgramaONE #CarreiraTech"}]},
            {"id": "card_conquista", "nome": "Card de conquista", "tipo": "card",
             "campos": {"titulo": "Primeira vaga como dev júnior",
                        "frase": "O portfólio que construí no ONE fez a diferença."},
             "variacoes": [{"titulo": "Conquista: dev júnior", "frase": "O portfólio que construí no ONE fez a diferença."}]},
        ],
    },
    {
        "id": "hist-002",
        "autor": "Lucas Almeida",
        "iniciais": "LA",
        "canal": "#projetos",
        "origem": "Mensagem da comunidade",
        "categoria": "Projeto de destaque",
        "sentimento": "Positivo",
        "relevancia": 89,
        "mensagem_original": "Nosso projeto de controle financeiro foi destaque no desafio. Fizemos tudo em equipe!",
        "destaques": ["projeto de controle financeiro foi destaque no desafio.", "Fizemos tudo em equipe!"],
        "fatos": ["Projeto: controle financeiro", "Reconhecimento: destaque no desafio", "Trabalho em equipe"],
        "ativos": [
            {"id": "post_linkedin", "nome": "Post para LinkedIn", "tipo": "texto",
             "campos": {"texto": "Trabalho em equipe que dá resultado! O projeto de controle financeiro do Lucas Almeida e do "
                                 "time foi destaque no desafio. Parabéns a todos! 👏 #ProgramaONE #Projetos"},
             "variacoes": [{"texto": "Um projeto de controle financeiro, feito em equipe, e destaque no desafio. "
                                     "Parabéns, Lucas e time! 🚀 #ProgramaONE #Projetos"}]},
            {"id": "resumo_projeto", "nome": "Resumo do projeto", "tipo": "texto",
             "campos": {"texto": "Projeto: controle financeiro. Destaque no desafio. Desenvolvido em equipe."},
             "variacoes": [{"texto": "Controle financeiro: projeto em equipe reconhecido como destaque no desafio."}]},
        ],
    },
    {
        "id": "hist-003",
        "autor": "Camila Santos",
        "iniciais": "CS",
        "canal": "#carreira",
        "origem": "Mensagem da comunidade",
        "categoria": "Superação e transição de carreira",
        "sentimento": "Positivo",
        "relevancia": 84,
        "mensagem_original": "Depois de 10 anos no varejo, concluí a formação e comecei minha transição para tecnologia.",
        "destaques": ["Depois de 10 anos no varejo,", "concluí a formação", "comecei minha transição para tecnologia."],
        "fatos": ["Trajetória: 10 anos no varejo", "Marco: formação concluída", "Mudança: início da transição para tecnologia"],
        "ativos": [
            {"id": "post_linkedin", "nome": "Post para LinkedIn", "tipo": "texto",
             "campos": {"texto": "Depois de 10 anos no varejo, a Camila Santos concluiu a formação e começou a transição "
                                 "para tecnologia. Nunca é tarde para recomeçar. Parabéns, Camila! 💜 #ProgramaONE #MudançaDeCarreira"},
             "variacoes": [{"texto": "10 anos no varejo, uma formação concluída e uma nova carreira começando. "
                                     "A Camila Santos está em transição para tecnologia. Parabéns! 💜 #ProgramaONE"}]},
            {"id": "roteiro_historia", "nome": "Roteiro de história", "tipo": "texto",
             "campos": {"texto": "1) Dez anos no varejo. 2) A decisão de estudar. 3) Formação concluída. "
                                 "4) O começo da transição para tecnologia."},
             "variacoes": [{"texto": "Abertura: 10 anos no varejo. Virada: formação concluída. Fechamento: a transição para tecnologia começou."}]},
        ],
    },
]

PACOTES_OCI = [
    {"caminho": "ativos/demo-001/pacote-distribuicao.json", "lote": "DEMO-001",
     "data": "15/10/2026 14:32", "tamanho": "2,4 KB", "status": "salvo"},
    {"caminho": "ativos/demo-001/evidencias.json", "lote": "DEMO-001",
     "data": "15/10/2026 14:32", "tamanho": "1,1 KB", "status": "salvo"},
    {"caminho": "ativos/demo-002/pacote-distribuicao.json", "lote": "DEMO-002",
     "data": None, "tamanho": None, "status": "falhou"},
]
