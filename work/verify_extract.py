# Confere se o JSON preserva todos os caracteres do PDF (exceto cabecalho/rodape/marcadores estruturais).
import json, re, html, collections, pymupdf as m
J = json.load(open('data/questoes.json', encoding='utf8'))
def plain(h): return html.unescape(re.sub(r'<[^>]+>', '', h))
got = ''
for q in J['questoes']:
    got += f"{q['id']:02d}." + ''.join(plain(p) for p in q['enunciado'])
    got += ''.join(k + ')' + plain(v) for k, v in q['alternativas'].items())
for t in J['textos'].values():
    got += ''.join(plain(p) for p in t['cabecalho'] + t['rodape']) + ''.join(f"{r['n']:02d}" + plain(r['t']) for r in t['linhas'])
HEAD = ''.join(['EDUCAÇÃO BRASILEIRA: TEMAS EDUCACIONAIS E PEDAGÓGICOS', 'ADMINISTRAÇÃO PÚBLICA', 'LÍNGUA PORTUGUESA',
                'LEITURA E INTERPRETAÇÃO DE DADOS E INDICADORES EDUCACIONAIS', 'CONHECIMENTOS ESPECÍFICOS'])
d = m.open('prova.pdf'); raw = ''
for pn in range(2, len(d)):
    for b in d[pn].get_text('blocks'):
        if 70 < b[1] < 780: raw += b[4]
ws = lambda s: re.sub(r'\s+', '', s)
cg, cr = collections.Counter(ws(got + HEAD)), collections.Counter(ws(raw))
print('JSON chars', sum(cg.values()), 'PDF chars', sum(cr.values()))
print('faltam no JSON:', {k: v for k, v in (cr - cg).items()})
print('sobram no JSON:', {k: v for k, v in (cg - cr).items()})
