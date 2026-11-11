# Todo: visualização responsiva para mobile

Detalhes em `plan.md`. Plano antigo em `tasks/arquivo/jogo-seduc-2018/`.

## T1 Base mobile
- [x] viewport-fit=cover, 100dvh, safe-area, touch-action, tap-highlight
- [x] build + verify.py OK; teste 667x375

## T2 Tela Questão compacta
- [x] Estatísticas e cabeçalho compactos <=480
- [x] Enunciado visível sem rolar em 360x640 (topo em 291 px de 640)
- [x] CHECKPOINT 1

## T3 Barra de ações fixa
- [x] Confirmar/Próxima sticky <=640 e paisagem baixa, safe-area, scroll-padding
- [x] Varredura 80 questões: última alternativa nunca coberta; Próxima sempre visível
- (teste de Tab com teclado físico: só via foco programático)

## T4 Ampliar figura
- [x] Botão + dialog nas 7 figuras; Esc e Fechar; foco volta ao botão
- [x] CHECKPOINT 2

## T5 Início, Foco, Modo, Resultado
- [x] 320/360/412 sem rolagem horizontal, alvos >=48
- [x] Tabelas do Resultado a 320

## T6 Paisagem e tablet
- [x] 667x375 (barra 19% da altura), 768x1024 (grupos lado a lado)
- [x] CHECKPOINT 3

## T7 Verificação final
- [x] verify.py TUDO OK, contraste.py 0 falhas, console limpo, rede só localhost
- [ ] NÃO testado: leitor de tela, aparelho físico, zoom 400%, "Apagar tudo", 1024x768 e 1280x800

## Extra: tema claro como padrão
- [x] :root claro, [data-theme=dark] escuro; estado inicial claro; botão alterna e salva
- Nota: quem já salvou "escuro" no navegador continua escuro (não dá para distinguir de escolha).
