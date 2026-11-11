# Monta data/questoes.json (Q1-17) a partir de lines.json. Rode depois de extract_ind.py.
import json, re, html, os
L = json.load(open('lines.json', encoding='utf8'))
os.makedirs('data', exist_ok=True)
NUM = re.compile(r'^\d\d$')
SECOES = {range(1, 10): 'Língua Portuguesa', range(10, 18): 'Educação Brasileira'}
secao = lambda n: next(v for k, v in SECOES.items() if n in k)
HEAD = ('LÍNGUA PORTUGUESA', 'EDUCAÇÃO BRASILEIRA')
left = lambda l: 43 if l['col'] == 'L' else 323          # margem esquerda da coluna
def joinl(prev, cur):
    """junta linhas: sem espaço quando uma URL foi quebrada no meio do endereço."""
    last = prev.split(' ')[-1]
    if re.match(r'https?://|www\.', last) or ('/' in last and ' ' not in last and last.endswith(('-', '/', '.')) and 'http' in prev):
        return prev + cur
    return prev + ' ' + cur

# ---------- Texto 1 (poema) : página 3 ----------
p3 = [l for l in L if l['pg'] == 3 and l['t'].strip() not in HEAD]
iG = next(i for i, l in enumerate(p3) if l['t'].startswith('GRAÚNA'))
poem, post = p3[:iG], p3[iG:]
nums = [l for l in poem if NUM.match(l['t'].strip())]
txt = [l for l in poem if not NUM.match(l['t'].strip()) and l['t'].strip() not in ('TEXTO 1', 'Canção Peregrina')]
linhas = []
for t in txt:
    n = next((x for x in nums if x['col'] == t['col'] and abs(x['bbox'][1] - t['bbox'][1]) < 3), None)
    linhas.append({'n': int(n['t']) if n else '', 't': t['h']})
# rodapé do texto 1: linhas indentadas após o poema (até a primeira questão)
iQ = next(i for i, l in enumerate(post) if re.match(r'<b>0?1\. </b>', l['h']) or l['t'].startswith('01.'))
fonte1 = post[0]['h']
for l in post[1:iQ]: fonte1 = joinl(fonte1, l['h'])
stream = post[iQ:] + [l for l in L if l['pg'] >= 4 and l['t'].strip() not in HEAD]

# ---------- percorre o restante: questões e Texto 2 ----------
Q, cur, t2 = [], None, None
def novo_par(cur, h, src): cur['par'].append({'h': h, 'src': src}); cur['item'] = h.startswith('(')
i = 0
while i < len(stream):
    l = stream[i]; h, t = l['h'], l['t'].strip(); i += 1
    if t == 'TEXTO 2':                                   # cabeçalho do texto 2; imagem fica entre este e a "Fonte"
        t2 = {'cab': h, 'fonte': ''}; cur = None; continue
    m = re.match(r'^(\d\d)\. ', t)
    if not m and t2 is not None and cur is None:
        if t.startswith('Fonte') or t2['fonte']:
            t2['fonte'] = h if not t2['fonte'] else joinl(t2['fonte'], h); continue
    if m:                                                # começa uma questão
        cur = {'id': int(m.group(1)), 'pg': l['pg'], 'par': [], 'alts': {}, 'alt': None, 'item': False, 'ycol': None}
        Q.append(cur); t2done = True
        novo_par(cur, h, False); cur['last'] = l; continue
    if cur is None: continue
    ma = re.match(r'^([A-D])\) ', t)
    if ma:                                               # alternativa
        cur['alt'] = ma.group(1); cur['alts'][cur['alt']] = re.sub(r'^[A-D]\) ', '', h, count=1); cur['last'] = l; continue
    if cur['alt']:                                       # continuação de alternativa
        cur['alts'][cur['alt']] = joinl(cur['alts'][cur['alt']], h); cur['last'] = l; continue
    # estágio do enunciado
    if t == '(   )' or re.match(r'^\(\s+\)$', t):         # item V/F: marcador + texto na mesma altura
        nxt = stream[i]; i += 1
        novo_par(cur, '(   ) ' + nxt['h'], False); cur['item'] = True; cur['last'] = nxt; continue
    ind = l['bbox'][0] > left(l) + 3
    last = cur['last']; same_col = (last['pg'], last['col']) == (l['pg'], l['col'])
    dy = l['bbox'][1] - last['bbox'][1]
    if cur['item'] and ind and same_col and dy < 16:    # continuação do item V/F
        cur['par'][-1]['h'] = joinl(cur['par'][-1]['h'], h)
    else:
        prev = cur['par'][-1]
        quebra = (ind != prev['src']) or (same_col and dy > 16)
        if cur['item'] and not ind: cur['item'] = False
        if quebra: novo_par(cur, h, ind); cur['item'] = False if not h.startswith('(') else True
        else: prev['h'] = joinl(prev['h'], h)
    cur['last'] = l

ids = [q['id'] for q in Q]
assert ids == list(range(1, 18)), ids
questoes = []
for q in Q:
    n = q['id']
    enun = [p['h'].strip() for p in q['par']]
    enun[0] = re.sub(r'^<b>\d\d\. </b>', '', enun[0])                 # a numeração original fica no campo id
    questoes.append({'id': n, 'pg': q['pg'], 'secao': secao(n), 'enunciado': enun,
                     'alternativas': q['alts'], 'texto_ref': 't1' if n <= 5 else ('t2' if n <= 9 else None), 'imagens': []})
    assert sorted(q['alts']) == list('ABCD'), (n, sorted(q['alts']))
textos = {'t1': {'questoes': [1, 2, 3, 4, 5], 'cabecalho': ['<b>TEXTO 1</b>', '<b>Canção Peregrina</b>'], 'linhas': linhas, 'rodape': [fonte1]},
          't2': {'questoes': [6, 7, 8, 9], 'cabecalho': [t2['cab']], 'imagem': 'img/ind_t2_tirinha.png', 'rodape': [t2['fonte']]}}
json.dump({'questoes': questoes, 'textos': textos}, open('data/questoes.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('ok', len(questoes), 'questões')
