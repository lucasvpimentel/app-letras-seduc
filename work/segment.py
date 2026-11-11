# Segmenta o fluxo de blocos em questoes. Saida: data/seg.json (rascunho, ainda com linhas originais).
import json, re
els = json.load(open('data/els.json', encoding='utf8'))
qs, pre, cur, alt = {}, [], None, None
prelude_for = {}                       # id da questao -> blocos que vieram antes do numero dela
for e in els:
    first = e['lines'][0].strip() if e['lines'] else ''
    mq = re.match(r'^(\d{2})\.\s', e['lines'][0]) if e['lines'] else None
    ma = re.match(r'^([A-D])\)$', first) or re.match(r'^([A-D])\)\s', first)
    if mq and int(mq.group(1)) == (cur['id']+1 if cur else 1):
        cur = {'id': int(mq.group(1)), 'pg': e['pg'], 'stem': [e], 'alts': {}, 'pre': pre}
        qs[cur['id']] = cur; pre = []; alt = None
    elif ma and cur and ma.group(1) not in cur['alts']:
        alt = ma.group(1); cur['alts'][alt] = [e]
    elif cur and alt is None:
        cur['stem'].append(e)
    elif cur and alt is not None and len(cur['alts']) < 4:
        cur['alts'][alt].append(e)       # continuacao da alternativa
    else:
        pre.append(e)
json.dump(qs, open('data/seg.json', 'w', encoding='utf8'), ensure_ascii=False)
bad = [i for i, q in qs.items() if len(q['alts']) != 4]
print(len(qs), 'questoes; sem 4 alts:', bad)
print('com preludio:', [(i, len(q['pre'])) for i, q in qs.items() if q['pre']])
