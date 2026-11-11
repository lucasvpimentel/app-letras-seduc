# Plano: jogo de estudo SEDUC/CE 2018 (Português) -> `jogo_seduc2018_portugues.html`

## Estado do ambiente (verificado)
- Pasta de trabalho vazia, sem git, sem `tasks/` previo (nada a sobrescrever).
- Fontes locais achadas (anexos nao chegaram na pasta; estao em Downloads):
  - Prova: `C:\Users\user\Downloads\seduccod11gab3.pdf` (23 pag., Caderno 3, texto extraivel, 80 questoes; pag. 1 e 8 tem imagens, varias pag. com muitos tracos vetoriais = quadros/tabelas/graficos).
  - Edital 2026: `C:\Users\user\Downloads\do20260814p01.pdf` (17 pag.).
  - Gabarito: placeholder `{{GABARITO_ANEXO}}` nao preenchido -> tratar como "nenhum"; pesquisar na Fase 2.
- Ferramentas: Python 3.14 + PyMuPDF (ok), pdftotext (ok), Node 24 (ok). `jsdom` NAO instalado; Playwright Python nao confirmado. Plano: tentar `npm i jsdom` / `playwright` numa pasta de ferramentas fora do projeto. Se nada instalar, testar o JS com Node + DOM stub minimo e declarar a limitacao.
- Ferramentas de busca web ficam em ToolSearch (WebSearch/WebFetch, deferidas); shell sem internet. Condicao de parada (b) vale se o gabarito do caderno 3 nao for achado.

## Arquitetura (ponytail: o minimo que cumpre o pedido)
Um pipeline Python + um template HTML, tudo em `work/` ao lado do entregavel:
```
work/
  extract.py        PDF -> data/questoes.json + data/img/*.png (recortes)
  data/questoes.json
  data/gabarito.json      {id: {letra, situacao, fonte{url,data}}}
  data/explicacoes.json   {id: {...}}  (so confirmadas)
  data/classificacao.json area, subtopico, item Anexo III, duvida
  template.html     CSS + JS (sem dados)
  build.py          template + JSONs + PNG base64 -> ../jogo_seduc2018_portugues.html
  verify.py         checks 1-6 por codigo
  test_flow.*       fluxo do jogo (jsdom/Playwright)
```
Sem framework, sem libs externas: JS vanilla, CSS com variaveis (tema escuro padrao + claro), localStorage com try/catch.

## Grafo de dependencias
```
F1 extracao ──┬─> classificacao ──┐
              ├─> recortes PNG ───┤
F2 gabarito ──┴─> (situacao) ─────┼─> F3 explicacoes ─┐
                                  │                   ├─> F4 build ─> F5 verificacao/entrega
template UI (T-UI, independe do conteudo real, usa 3 questoes-fixture) ──┘
```
F1 e F2 sao independentes entre si (F2 so precisa dos ids 1-80). A UI pode ser construida em paralelo com fixture, mas o conteudo real so entra em F4.

## Fatias verticais
Cada fatia termina com algo que roda e se verifica.

### S0. Preparar ferramentas e ler fontes de design
- Carregar skills: frontend-design, design-elevation, interaction-design, ux-writing, accessibility-audit (as que existirem em `design-skills:*`/`design:*`; senao aplicar principios sem citar).
- Tentar instalar jsdom/playwright fora de `Letras/`.
- Aceite: lista do que esta disponivel para teste anotada em `work/NOTAS.md`.

### S1. Extracao fiel de ponta a ponta (1 pagina -> 80 questoes)
1. Prototipo em 2 paginas: extracao por blocos (`get_text("blocks")`/`words`) separando colunas pela coordenada x; remover cabecalho/rodape e hifenizacao de quebra de linha; separar questao por marcador de numero.
2. Estender para as 23 paginas; detectar secoes pelos titulos (confirmar faixas 1-8/9-14/15-22/23-30/31-80).
3. Textos de apoio compartilhados em campo proprio (`textos[]`, `questoes[].texto_ref`).
4. Recortes PNG >=150 dpi (usar 200) de figuras, graficos, tabelas, quadros, tirinhas, afirmativas em colunas, associacao de colunas; transcricao em texto mantida como `alt`.
5. Conferencia: renderizar paginas e comparar visualmente (todas as questoes com recorte + amostra das demais); `verify.py` checa 80 ids, 4 alternativas A-D nao vazias, sem sobra de cabecalho/rodape, sem hifen-quebra.
- Aceite: 80 questoes integras; 2 tentativas maximas, senao PARAR (condicao a).
- Checkpoint 1: revisar contagem por secao e lista de questoes com recorte.

### S2. Gabarito do caderno 3 (independente de S1)
1. Se a pessoa anexou PDF: verificar preliminar x definitivo e caderno. Aqui: "nenhum" -> pesquisar.
2. Busca: cev.uece.br, Comunicado 118/2018-CEV/UECE (preliminar), comunicados de recursos e gabarito definitivo (Edital 30/2018, Professor Lingua Portuguesa, cod. 11, gabarito 3).
3. Gravar por questao `{letra, situacao: confirmado|anulada|sem_gabarito, fonte:{url,data}}`. Nunca usar outro caderno; nunca deduzir pela propria analise.
4. Se o oficial for so de outro caderno com mapa de conversao: so usar se a fonte oficial trouxer o mapa; caso contrario tratar como nao encontrado.
- Aceite: 80 entradas com fonte; ou PARAR e pedir o PDF de www.cev.uece.br (condicao b).
- Checkpoint 2: resumir fonte, data, quantidade anulada.

### S3. Classificacao por area e item do Anexo III
- Ler Anexos II e III do edital 2026 (extrair texto das paginas relevantes).
- Atribuir `area` (7 valores), `subtopico` e `item_anexo3`; registrar duvidas em `classificacao.json` (`duvida: true` + motivo).
- Aceite: contagens por area somam 80; areas base conferem com faixas das secoes (8/6/8/8 + 50).

### S4. Explicacoes (4 lotes de 20; so confirmadas)
- Formato do bloco `formato`: `explicacao_correta` 3-6 frases, `por_que_erradas` (3 linhas), `fundamentacao` (so com certeza, senao null), `atualizacao` (PNE 2026-2036, Lei 15.388/2026, BNCC etc. quando aplicavel).
- Cada explicacao parte da letra oficial; discordancia vai para `work/divergencias.md` (relatorio), nunca altera gabarito.
- Gravar arquivo por lote (`explicacoes_01-20.json` ...) e juntar.
- Aceite por lote: schema valido, 3 errôneas por questao, nada para anuladas.
- Checkpoint 3 (apos cada lote): validar JSON e amostrar 3 explicacoes.

### S5. UI vertical minima: Inicio -> Foco -> Modo -> Questao (Treino) -> Resultado, com fixture
- Template com 3 questoes ficticias para desenvolvimento (nunca vao ao entregavel).
- Estado unico em objeto + `render()`; localStorage com try/catch e aviso amigavel.
- Aceite: fluxo completo navegavel por teclado nas 3 questoes.

### S6. Camadas de funcionalidade (cada uma testada)
a. Filtro por area (checkboxes, contagens, marcar tudo/limpar/prova completa, >=1 area, trocar area sem perder progresso).
b. Modos Simulado e Revisao de erros (aparece quando ha erros).
c. Anuladas/sem_gabarito: aviso "nao conta na pontuacao", fora de acertos/erros/pontos/%.
d. Resultado: desempenho por materia e area, lista de erradas, Refazer, Escolher outra area; na prova completa comparar com minimos do edital 2026 (3/3/3 por materia P1, 2 em Dados, 12 P1, 20 P2, 40 total) e avisar que a distribuicao 2018 difere (AP 6 vs 8; Dados 8 vs 6). Cuidado: com anuladas, comparar sobre as validas e dizer isso.
e. Salvar: exportar/importar JSON de progresso, apagar tudo (confirmacao), validacao do arquivo importado.
f. Tema escuro/claro, prefers-reduced-motion, 360px+, alvos >=48px, foco visivel, rodape de aviso IA/banca.
- Checkpoint 4: demo manual via Playwright/Browser pane com fixture.

### S7. Build com dados reais
- `build.py` injeta JSON + PNG em base64; textos escapados (`</script>`), nenhum link para URLs de dentro das provas.
- Aceite: arquivo unico, sem `http(s)://` em atributos src/href/@import, tamanho razoavel (alvo < 8 MB).

### S8. Verificacao e entrega
- `verify.py` (criterios 1-4 e 6): 80 ids; 4 alternativas; texto do HTML == JSON (extrair dados embutidos e comparar); gabarito/fonte ou situacao; anuladas fora da pontuacao (teste de logica); contagens por area = 80.
- Criterio 5: abrir offline no navegador (Browser pane/Playwright com rede bloqueada), console sem erros, zero requisicoes externas.
- Fluxo automatizado: Treino, Simulado, Revisao, filtro, persistencia, export/import, apagar.
- Criterio 7: auditoria acessibilidade (contraste calculado por script nos dois temas, foco, teclado, alvos 48px, informacao nao so por cor) + skill accessibility-audit.
- Comparacao visual do HTML vs PNG da pagina nas questoes com figura.
- Entrega via SendUserFile + relatorio <= 15 linhas.
- Checkpoint final: nada marcado como testado sem execucao.

## Riscos e mitigacoes
| Risco | Mitigacao |
|---|---|
| Duas colunas misturadas / questao quebrando entre colunas ou paginas | Ordenar por (coluna, y); validar sequencia 1..80 e 4 alternativas; render lado a lado |
| Gabarito definitivo nao achado ou so de outro caderno | Parar (b) e pedir PDF; nao deduzir |
| Alternativas com formatacao rica (itens I, II, III, associacao) quebram em texto | Recorte PNG + transcricao |
| Fidelidade (nao "corrigir" texto da prova) | Verificacao automatica JSON x HTML; nenhum passo normaliza texto alem de hifenizacao/cabecalho |
| Explicacao errada ensina errado | Fundamentacao so com certeza; rodape de aviso; divergencias no relatorio |
| Sem jsdom/Playwright | Browser pane do app para fluxo; declarar no relatorio o que nao foi testado |
| Anuladas distorcem % | Contadores usam so `situacao == confirmado` |

## Decisoes para revisao humana
1. Aceitar usar os dois PDFs de `Downloads` (nomes acima) como os anexos? (Sao os unicos candidatos achados.)
2. Prova completa com questao anulada: pontos/percentual sobre as validas (como pedido); comparacao com minimos do edital feita proporcionalmente? Padrao proposto: comparar so a pontuacao bruta e avisar quando houver anuladas.
3. Pasta de trabalho: `Letras/work/` mantida ao lado do HTML final (ou apagada na entrega)?
