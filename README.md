# Estudo SEDUC/CE: Língua Portuguesa

Jogo de estudo em um único arquivo HTML, feito para quem vai prestar o concurso de Professor de Língua Portuguesa da SEDUC/CE (Edital nº 014/2026). Funciona no celular e no computador, sem instalar nada e sem internet.

**Abrir online:** https://lucasvpimentel.github.io/app-letras-seduc/

**Usar offline:** baixe [`jogo_seduc2018_portugues.html`](jogo_seduc2018_portugues.html) e abra no navegador.

## O que tem

- **Prova de 2018** (SEDUC/CE, Professor Nível A, Língua Portuguesa, caderno 3, banca FUNECE/CEV-UECE): 80 questões, com o gabarito definitivo depois dos recursos (Comunicado nº 129/2018). As questões anuladas (26, 30, 50, 53 e 57) não contam na pontuação.
- **Prova de 2023** (SEDUC/CE, Professor Indígena, caderno 1 de Linguagens, mesma banca): 17 questões, sendo 9 de Língua Portuguesa e 8 de Educação Brasileira, com o gabarito definitivo (Comunicado nº 215/2023).
- **Explicações** para cada questão com gabarito confirmado.
- **Modos:** Treino (explicação logo após cada resposta), Simulado (resultado só no fim) e Revisão de erros.
- **Áreas de foco:** escolha uma ou mais áreas e uma ou as duas provas. Ao fazer a prova completa de 2018, o resultado é comparado com as notas mínimas do edital de 2026.
- **Progresso salvo no navegador**, com opção de salvar em arquivo, abrir em outro aparelho e apagar.
- **Tema claro (padrão) e escuro**, layout para celular a partir de 320 px, uso pelo teclado, contraste conferido e respeito à preferência de menos movimento.

## Avisos importantes

- As **explicações foram geradas por inteligência artificial** e podem conter erros. Quando não foi possível confirmar uma norma ou um trecho, o texto diz isso.
- O **gabarito vem da banca**. Onde a análise da explicação discorda do gabarito oficial, o jogo mantém o oficial.
- A prova de 2018 antecede mudanças cobradas em 2026 (por exemplo, o novo PNE e a BNCC no lugar dos PCN). Há notas de atualização nas explicações.
- A distribuição de questões de 2018 difere da de 2026 (2018: 6 de Administração Pública e 8 de Dados e Indicadores; 2026: 8 e 6).
- Material de estudo **não oficial**.

## Como o projeto é organizado

| Pasta ou arquivo | Conteúdo |
| --- | --- |
| `index.html`, `jogo_seduc2018_portugues.html` | O jogo pronto (o mesmo arquivo, com dois nomes). |
| `work/template.html` | Interface (HTML, CSS e JavaScript), sem as questões. |
| `work/build.py` | Monta o jogo a partir do template e dos arquivos de dados. |
| `work/verify.py` | Confere que o jogo tem as questões, os gabaritos e as explicações esperados. |
| `work/data/` | Dados da prova de 2018 extraídos do PDF. |
| `work_indigena2023/` | Scripts e dados da prova de 2023. |
| `tasks/` | Planos de trabalho. |

Para regerar o jogo (Python 3 com `pymupdf` só é necessário para refazer a extração dos PDFs):

```bash
cd work
python build.py
python verify.py
```

Os PDFs originais das provas não estão no repositório. Eles estão no site da banca: https://www.cev.uece.br

## Limites conhecidos

- Não foi testado com leitor de tela, nem em aparelho físico, nem com zoom de 400%.
- Questões de outras provas só entram quando há caderno e gabarito definitivo oficiais que possam ser extraídos com fidelidade.

## Licença

O código está sob a [licença MIT](LICENSE). Os enunciados, textos de apoio e gabaritos das provas pertencem à banca organizadora (CEV/UECE) e aos autores dos textos citados; foram reproduzidos aqui apenas para estudo, sem alterações, e não são cobertos pela licença do código.
