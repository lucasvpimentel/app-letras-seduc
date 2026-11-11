# Plano: visualização responsiva para mobile

Escopo: `jogo_seduc2018_portugues.html`, gerado por `work/build.py` a partir de `work/template.html`. Só CSS/JS do template muda. Questões, gabarito e explicações não mudam.
Plano anterior arquivado em `tasks/arquivo/jogo-seduc-2018/`.

## Estado atual (lido em `work/template.html`)
- Já existe: viewport meta, layout fluido, `@media (max-width:420px)`, alvos >=48 px, sem rolagem horizontal em 360 px (testado antes).
- Lacunas para celular real (suposição a validar; ainda não medido em aparelho):
  1. `min-height:100vh` no `body`: barra de endereço do celular faz o rodapé "pular". Usar `dvh`.
  2. Sem `viewport-fit=cover` nem `env(safe-area-inset-*)`: em paisagem com notch, conteúdo encosta na borda.
  3. Tela de questão: bloco de 5 estatísticas + barra + cabeçalho empurra o enunciado para baixo da dobra em 360x640.
  4. Botões "Confirmar" e "Próxima" ficam no fim da página; com texto longo exigem rolar até o fim, longe do polegar.
  5. Recortes PNG (7 questões) encolhem para a largura da tela e ficam ilegíveis; sem toque para ampliar.
  6. Texto-base longo (poemas, crônicas) ocupa várias telas antes das alternativas.
  7. Sem `touch-action: manipulation` (atraso de toque/zoom duplo) e sem `-webkit-tap-highlight-color` definido.
  8. Cabeçalho com botões de tema/menu: conferir quebra em 320 px.
  9. Tabelas do Resultado: já ajustadas para 360 px; reconferir em 320 px.

## Decisões de design
- Mobile-first por breakpoints: base (<=480), tablet (>=768), desktop (>=1024, coluna de 880 px já existente).
- Barra de ações fixa no rodapé da tela de questão (só <=640 px): "Confirmar"/"Próxima" sempre à vista. Em telas largas continua no fluxo.
- Estatísticas compactas no mobile: uma linha rolável? Não (rolagem horizontal é falha). Usar grade 3x2 enxuta, ou resumo de uma linha "Acertos 5 · Erros 2 · 71%" com detalhes em `<details>`.
- Zoom de figura: toque abre a imagem em diálogo `<dialog>` com rolagem e botão Fechar (>=48 px); texto alternativo mantido.
- Não adicionar dependência, biblioteca nem PWA (offline já funciona por arquivo único).

## Grafo de dependência
```
T1 base (dvh, safe-area, touch) ─┬─ T2 tela Questão compacta ─┬─ T3 barra de ações fixa
                                 │                            └─ T4 zoom de figura
                                 ├─ T5 Início/Foco/Modo/Resultado em 320-480
                                 └─ T6 paisagem e tablet
T2..T6 ─► T7 verificação final (matriz de viewports + acessibilidade + regressão)
```
T2 e T5 podem ser feitas em qualquer ordem após T1. T3 depende de T2 (mesma tela).

## Tarefas (cada fatia é um caminho completo, não camada)

### T1 Base mobile
Mudar: `viewport-fit=cover`, `body min-height:100dvh` (fallback `100vh`), padding com `env(safe-area-inset-*)` em header, main, footer e barra fixa; `touch-action:manipulation` em botões; `-webkit-tap-highlight-color` suave.
Aceite: nenhum item some atrás de notch em paisagem (emulado); rodapé não pula ao rolar; build gera HTML sem erro.
Verificar: `python work/build.py`; `work/verify.py` "TUDO OK"; Playwright/painel a 667x375 conferindo `getBoundingClientRect` dentro de `innerWidth`.

### T2 Tela Questão compacta (360x640)
Mudar: estatísticas em formato compacto no <=480; cabeçalho da questão em 2 linhas; reduzir margens; fonte do enunciado 1rem; título "Questão N de 80" e barra de progresso no topo.
Aceite: em 360x640 o início do enunciado aparece sem rolar; nenhuma rolagem horizontal; alvos >=48 px; aproveitamento, pontos e sequência continuam acessíveis (texto, não só ícone).
Verificar: script mede `top` do `.exam` < 0.6 * innerHeight; varredura de alvos e `scrollWidth <= clientWidth` nas 80 questões.

### T3 Barra de ações fixa (depende de T2)
Mudar: contêiner `.acoes` com `position:sticky; bottom:0` (<=640 px), fundo opaco, borda superior, safe-area; espaço no fim do conteúdo para não cobrir a última alternativa; foco não pode ficar escondido atrás da barra (WCAG 2.4.11) -> `scroll-padding-bottom`.
Aceite: Confirmar/Próxima visíveis sem rolar até o fim; Tab até a última alternativa a mostra por inteiro; foco vai para o feedback após confirmar e fica visível.
Verificar: teclado Tab/Enter no painel; medir sobreposição `elementFromPoint` no centro da última alternativa.

### T4 Ampliar figura (depende de T2)
Mudar: imagens `.exam img` viram botão "Ampliar figura" abrindo `<dialog>` com a imagem em largura natural e rolagem em dois eixos; Esc/Fechar retorna foco ao botão.
Aceite: as 7 figuras (Q2, 26, 29, 31, 35, 37, 38) abrem e fecham por toque e teclado; `alt` presente; leitor anuncia o diálogo (`aria-label`); sem rolagem horizontal da página atrás.
Verificar: abrir cada uma no painel; checar `document.activeElement` ao fechar. Leitor de tela real: não testável aqui, informar.

### T5 Telas Início, Foco, Modo, Resultado em 320-480
Mudar: ficha (`dl`) empilha em <=420; linhas de checkbox com contagem sem quebra feia; botões do Modo em largura total; tabelas do Resultado sem estouro a 320 px; botão de tema e menu cabem no cabeçalho.
Aceite: sem rolagem horizontal em 320, 360, 390, 412; alvos >=48 px; texto legível sem zoom (>=16 px em campos).
Verificar: varredura por script nas 5 telas em 320/360/390/412 px; captura de tela em 360.

### T6 Paisagem e tablet
Mudar: em paisagem baixa (<=500 px de altura) sem barra fixa alta nem cabeçalho grande; tablet 768 com duas colunas só onde ajuda (Foco: dois grupos lado a lado).
Aceite: 667x375, 768x1024 e 1024x768 sem corte nem rolagem horizontal; barra fixa não ocupa mais de ~25% da altura em paisagem.
Verificar: `resize_window` com tamanhos personalizados + medições.

### T7 Verificação final
- Matriz: 320x568, 360x640, 390x844, 412x915, 667x375, 768x1024, 1280x800; temas escuro e claro; `prefers-reduced-motion`.
- Regressão: `work/verify.py` "TUDO OK" (texto do HTML idêntico ao JSON); fluxo completo Treino/Simulado/Revisão; salvar/continuar; exportar/importar; contraste `work/contraste.py` 0 falhas.
- Console sem erros; zero requisições externas.
- Zoom 200%/400% (reflow) no painel; informar o que não foi testado (leitor de tela, aparelho físico, "Apagar tudo" por causa de `confirm()`).
- Rebuild, commit e push no repositório `lucasvpimentel/app-letras-seduc` (só após pedido).

## Checkpoints
- CP1 após T1+T2: tela Questão boa em 360x640; verify.py OK.
- CP2 após T3+T4: fluxo de uma questão completo só com polegar/teclado.
- CP3 após T5+T6: todas as telas na matriz.
- CP4 após T7: entrega.

## Riscos
- Barra fixa cobre conteúdo/foco -> `scroll-padding`, espaçador e teste de teclado.
- `dialog` em navegadores antigos de celular -> suporte amplo desde 2022; fallback: abrir imagem inline se `showModal` ausente.
- Mudança de CSS alterar texto da prova -> não tocar nos dados; `verify.py` pega.
- Sem aparelho real: medidas em emulação, dizer isso no relatório.

## Perguntas em aberto
1. Há aparelho/tamanho alvo específico (ex.: Android com 360 px)?
2. Barra fixa de ações aceitável, ou prefere botão no fim do conteúdo?
