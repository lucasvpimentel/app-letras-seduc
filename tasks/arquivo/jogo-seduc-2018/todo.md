# Todo: jogo SEDUC 2018 Portugues

Ver detalhes em `plan.md`.

## S0 Preparacao
- [x] Carregar skills de UI/UX disponiveis; anotar quais existem
- [ ] Tentar instalar jsdom/playwright (nao feito: testes rodaram no painel de navegador do app)

## S1 Extracao (parar se nao fechar 80 apos 2 tentativas)
- [x] extract.py prototipo em 2 paginas (colunas, cabecalho/rodape, hifen)
- [x] Estender as 23 paginas; secoes e faixas confirmadas
- [x] Textos de apoio compartilhados em campo proprio
- [x] Recortes PNG (200 dpi) + transcricao alt
- [x] verify (80 ids, 4 alternativas, sem artefatos) + conferencia visual
- [x] CHECKPOINT 1

## S2 Gabarito caderno 3 (parar se nao achar)
- [x] Pesquisar cev.uece.br, Comunicado 118/2018 e comunicados de recursos/definitivo
- [x] Gravar gabarito.json (letra, situacao, fonte url+data) para 80 questoes
- [x] CHECKPOINT 2

## S3 Classificacao
- [x] Ler Anexos II e III do edital 2026
- [x] area + subtopico + item Anexo III + duvidas; soma = 80
- [x] CHECKPOINT (contagens 8/6/8/8 e 50 especificas)

## S4 Explicacoes (so confirmadas)
- [x] Lote 1-20
- [x] Lote 21-40
- [x] Lote 41-60
- [x] Lote 61-80
- [x] Divergencias analise x oficial registradas no relatorio final (sem arquivo separado)
- [x] CHECKPOINT 3 (schema + amostra)

## S5 UI minima com fixture
- [x] Inicio -> Foco -> Modo -> Questao (Treino) -> Resultado navegavel por teclado
- [x] Estado + localStorage com tratamento de erro

## S6 Funcionalidades
- [x] Filtro por area (contagens, marcar tudo, limpar, prova completa, >=1)
- [x] Simulado e Revisao de erros
- [x] Anuladas/sem_gabarito fora da pontuacao
- [x] Resultado por materia/area + comparacao com minimos 2026 (prova completa)
- [x] Exportar/importar/apagar progresso
- [x] Temas, reduced-motion, 360px+, alvos 48px, foco, rodape de aviso
- [x] CHECKPOINT 4

## S7 Build
- [x] build.py gera jogo_seduc2018_portugues.html unico, offline, sem URLs externas

## S8 Verificacao e entrega
- [x] Criterios 1-4 e 6 por codigo
- [x] Criterio 5: offline, console limpo, zero requisicoes externas
- [x] Fluxo testado no navegador (Treino, Simulado, Revisao, filtro, persistencia, export/import). NAO testado: botao Apagar tudo (confirm bloqueado no painel)
- [x] Criterio 7: contraste calculado, alvos 48px, teclado A-D, nome acessivel. NAO testado: leitor de tela, zoom 400%
- [x] Comparacao visual HTML x PDF nas questoes com figura
- [x] SendUserFile + relatorio (<=15 linhas)
