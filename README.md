# CommunityLab · Front-end (Streamlit)

Interface do CommunityLab, feita em Streamlit. Por enquanto ela funciona sozinha, com **dados fictícios**, para o time poder ver e validar o fluxo antes de o back ficar pronto.

> Todos os nomes, mensagens e depoimentos do front são inventados. Nada aqui representa pessoas reais.

## O que o front faz

O fluxo tem 4 etapas, na mesma ordem do menu lateral:

| Etapa | Tela | O que acontece |
|---|---|---|
| 1 | Ingestão | Upload de CSV/JSON ou JSON colado, com prévia das interações e filtro por canal |
| 2 | Processamento | Acompanha as etapas da análise (simulada) e mostra erro ao salvar no OCI com opção de tentar novamente |
| 3 | Histórias detectadas | Lista as histórias de sucesso com categoria, relevância e trecho original, com filtros |
| 3 | Curadoria | Revisa os rascunhos, mostra as evidências, exige confirmação de autorização e permite aprovar, rejeitar ou regenerar |
| 4 | Armazenamento OCI | Lista os pacotes salvos no bucket, com visualização do JSON e download |

**Princípio do produto:** a IA sugere, o time decide. Nada é publicado automaticamente, e cada ativo gerado aponta para a mensagem original.

## Como rodar

Pré-requisito: Python 3.10 ou superior.

```bash
pip install -r requirements-front.txt
streamlit run app/main.py
```

No Windows, se `streamlit` não for reconhecido:

```bash
python -m streamlit run app/main.py
```

O app abre em `http://localhost:8501`.

## Modo demonstração

Na barra lateral, em **Modo demonstração**, dá para:

- simular erro ao salvar no OCI (mostra a tela de falha e o botão "Tentar novamente");
- alternar a tela de Armazenamento OCI entre os estados normal, vazio, carregando e erro de conexão;
- reiniciar a demonstração.

Para acelerar ou desacelerar a simulação do Processamento, use a variável `COMMUNITYLAB_DELAY` (segundos por etapa).

## Estrutura de pastas

```
app/
  main.py                    entrada do app, menu lateral e roteamento
  state.py                   estado da sessão
  styles.py                  CSS e helpers de HTML
  telas/                     uma tela por arquivo
    ingestao.py
    processamento.py
    historias.py
    curadoria.py
    oci.py
  services/
    data_service.py          ÚNICO ponto de contato com os dados
  mocks/
    mock_data.py             dados fictícios
.streamlit/
  config.toml                tema (cores)
requirements-front.txt
```

## Como o back se conecta (importante)

As telas **não** importam o back diretamente. Elas só chamam funções do arquivo `app/services/data_service.py`. Hoje essas funções devolvem dados fictícios. Quando o back estiver pronto, basta trocar o corpo delas por chamadas reais, e as telas continuam iguais.

Procure por `TODO(back)` no arquivo para achar os pontos de integração:

| Função | O que o back precisa fazer |
|---|---|
| `analisar(interacoes)` | Receber as interações e devolver as histórias detectadas com os ativos gerados |
| `regenerar(historia, ativo_id, vez)` | Gerar um novo rascunho para um ativo |
| `listar_pacotes()` | Listar os objetos do bucket no OCI Object Storage |
| `salvar_no_oci(pacotes, lote_id)` | Gravar o pacote no OCI. **Precisa ser idempotente**: tentar de novo não pode duplicar resultados |
| `reenviar_pacote(pacote)` | Tentar gravar de novo um pacote que falhou |
| `conteudo_pacote(caminho)` | Ler o JSON de um objeto do bucket |

### Formato provisório dos dados

O formato abaixo é o que o front usa **hoje**. Ele é só um ponto de partida e **pode mudar**: quem define o contrato oficial é o back, e o time deve decidir em conjunto.

Interação (entrada):

```json
{ "autor": "Marina Costa", "canal": "#conquistas", "tipo": "mensagem", "texto": "..." }
```

História detectada (saída):

```json
{
  "id": "hist-001",
  "autor": "Marina Costa",
  "canal": "#conquistas",
  "categoria": "Conquista profissional",
  "sentimento": "Positivo",
  "relevancia": 96,
  "mensagem_original": "...",
  "destaques": ["trecho da mensagem usado no rascunho"],
  "fatos": ["Conquista: primeira vaga como dev júnior"],
  "ativos": [
    { "id": "post_linkedin", "nome": "Post para LinkedIn", "tipo": "texto", "campos": { "texto": "..." } },
    { "id": "card_conquista", "nome": "Card de conquista", "tipo": "card", "campos": { "titulo": "...", "frase": "..." } }
  ]
}
```

Pacote salvo no OCI (listagem):

```json
{ "caminho": "ativos/demo-001/pacote-distribuicao.json", "lote": "DEMO-001",
  "data": "15/10/2026 14:32", "tamanho": "2,4 KB", "status": "salvo" }
```

## Pontos para alinhar com o back

- Quais **tipos de ativo** o back vai gerar (hoje o front mostra Post para LinkedIn, Card de conquista, Resumo do projeto e Roteiro de história).
- Se o campo `tipo` da interação vai ser preenchido e com quais valores.
- O que o pacote salvo no OCI deve conter. Hoje o JSON de exemplo só tem o status dos ativos. O ideal é guardar também o texto gerado, as citações com a mensagem de origem e se a autorização foi confirmada.
- Se o status de aprovação ou rejeição feito na Curadoria deve ser atualizado no bucket e como.

## Limitações conhecidas do protótipo

- A análise sempre devolve as 3 histórias fictícias, mesmo que você envie outro arquivo (o arquivo é validado e aparece na prévia, mas não é analisado).
- Aprovar ou rejeitar só vale durante a sessão e não grava em lugar nenhum.
- "Copiar texto" mostra um bloco com ícone de copiar, porque o Streamlit não acessa a área de transferência.
- Testado no Streamlit 1.66. O `requirements-front.txt` pede `>=1.37`.

## Como contribuir no front

1. Para mudar um texto ou visual de uma tela, edite o arquivo dela em `app/telas/`.
2. Para mudar os dados de exemplo, edite `app/mocks/mock_data.py`.
3. Para conectar o back, edite só `app/services/data_service.py`.
4. Não misture os mocks do front com a pasta de dados de demonstração do back.

## Como executar no Windows

1. Abra o Prompt de Comando ou PowerShell.
2. Navegue até a pasta do projeto:
   ```bash
   cd "c:\Users\guilh\Documents\tissy\communitylab-front\communitylab-front"
   ```
3. Ative o ambiente virtual (se existir):
   ```bash
   .\.venv\Scripts\Activate
   ```
4. Instale as dependências:
   ```bash
   pip install -r requirements-front.txt
   ```
5. Execute o aplicativo:
   ```bash
   streamlit run app/main.py
   ```