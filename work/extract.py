# Extracao fiel: PDF (2 colunas) -> data/lines.json (linhas na ordem de leitura) e data/seg.json (questoes).
# Remove somente cabecalho/rodape (faixas y<70 e y>778). Nada e reescrito.
import pymupdf as m, json, re
d = m.open('prova.pdf')
lines = []
for pn in range(2, len(d)):             # pag.1 capa, pag.2 instrucoes
    p = d[pn]
    bl = [b for b in p.get_text('dict')['blocks'] if b['type'] == 0 and b['bbox'][1] > 70 and b['bbox'][1] < 780]
    for c in 'LR':
        sel = [b for b in bl if (b['bbox'][0] < 290) == (c == 'L')]
        for b in sorted(sel, key=lambda b: b['bbox'][1]):
            for l in b['lines']:
                t = ''.join(s['text'] for s in l['spans']).rstrip()
                if t.strip():
                    lines.append({'pg': pn+1, 'col': c, 'bbox': [round(v) for v in l['bbox']], 't': t})
json.dump(lines, open('data/lines.json', 'w', encoding='utf8'), ensure_ascii=False)

qs, pre, cur, alt = {}, [], None, None
for ln in lines:
    t = ln['t'].strip()
    mq = re.match(r'^(\d{2})\.\s', t)
    ma = re.match(r'^([A-D])\)(\s|$)', t)
    if mq and int(mq.group(1)) == (cur['id'] + 1 if cur else 1):
        cur = {'id': int(mq.group(1)), 'pg': ln['pg'], 'stem': [ln], 'alts': {}, 'pre': pre}
        qs[cur['id']] = cur; pre = []; alt = None
    elif ma and cur and ma.group(1) not in cur['alts'] and ma.group(1) == 'ABCD'[len(cur['alts'])]:
        alt = ma.group(1); cur['alts'][alt] = [ln]
    elif cur is None:
        pre.append(ln)
    elif alt is None:
        cur['stem'].append(ln)
    elif len(cur['alts']) < 4:
        cur['alts'][alt].append(ln)
    else:
        # depois de D: continuacao de D (mesma coluna/pagina e colada) ou preludio da proxima
        last = cur['alts']['D'][-1]
        # continuacao: colada na mesma coluna, ou topo da coluna seguinte quando a ultima linha nao fecha frase
        glued = ln['pg'] == last['pg'] and ln['col'] == last['col'] and ln['bbox'][1] - last['bbox'][3] < 4
        wrapped = last['bbox'][1] > 730 and ln['bbox'][1] < 80 and not re.search(r'[.?!)”"]\s*$', last['t'])
        if glued or wrapped:
            cur['alts']['D'].append(ln)
        else:
            pre.append(ln)
json.dump(qs, open('data/seg.json', 'w', encoding='utf8'), ensure_ascii=False)
print(len(qs), 'questoes; sem 4 alts:', [i for i, q in qs.items() if len(q['alts']) != 4])
print('preludios:', {i: len(q['pre']) for i, q in qs.items() if q['pre']})
