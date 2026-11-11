# Confere: multiconjunto de caracteres do JSON == texto das páginas 3-6 do PDF (sem cabeçalho, rodapé e títulos de seção).
import json, re, html, collections, pymupdf as m
d = m.open('pdf/caderno1_linguagens.pdf')
pdf = ''
for pn in range(2, 6):
    for b in d[pn].get_text('blocks'):
        if 78.5 < b[1] < 778 and b[6] == 0:
            t = b[4]
            if t.strip() in ('LÍNGUA PORTUGUESA', 'EDUCAÇÃO BRASILEIRA'): continue
            pdf += t
J = json.load(open('data/questoes.json', encoding='utf8'))
strip = lambda h: html.unescape(re.sub(r'<[^>]+>', '', h))
out = ''
for q in J['questoes']:
    out += '%02d. ' % q['id'] + ' '.join(strip(p) for p in q['enunciado'])
    for k in 'ABCD': out += k + ') ' + strip(q['alternativas'][k])
for t in J['textos'].values():
    out += ' '.join(strip(c) for c in t['cabecalho']) + ' '.join(strip(r) for r in t['rodape'])
    for l in t.get('linhas', []): out += ('%02d' % l['n'] if l['n'] != '' else '') + strip(l['t'])
norm = lambda s: collections.Counter(re.sub(r'\s+', '', s).replace('\uf0b7', '•'))
a, b = norm(pdf), norm(out)
dif = {k: (a[k], b[k]) for k in set(a) | set(b) if a[k] != b[k]}
print('PDF', sum(a.values()), 'JSON', sum(b.values()), 'diferenças', dif)
print('FIEL' if not dif else 'DIVERGE')
