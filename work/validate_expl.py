import json,re
g=json.load(open('data/gabarito.json'))['questoes']; E={}
for f in ('01','02','03','04'): E.update(json.load(open(f'data/expl_{f}.json',encoding='utf8')))
AREAS={'EB','AP','LP','DI','ENS','LIT','LAS'}
bad=[]
assert sorted(map(int,E))==list(range(1,81)),'faltam ids'
for i in range(1,81):
    e=E[str(i)]; s=g[str(i)]
    if e['area'] not in AREAS: bad.append((i,'area'))
    if s['situacao']!='confirmado':
        if not e.get('anulada'): bad.append((i,'anulada flag'))
        continue
    n=len(re.findall(r'[.!?](?:\s|$)',e['explicacao_correta']))
    if not 3<=n<=6: bad.append((i,'frases',n))
    want=set('ABCD')-{s['letra']}
    if set(e['por_que_erradas'])!=want: bad.append((i,'erradas',sorted(e['por_que_erradas'])))
    for k in ('fundamentacao','atualizacao','duvida','subtopico','item'):
        if k not in e: bad.append((i,'falta',k))
print('problemas:',bad)
from collections import Counter
print(Counter(e['area'] for e in E.values()))
json.dump(E,open('data/explicacoes.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
