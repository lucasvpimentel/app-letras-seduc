# Verificações dos critérios de sucesso 1, 2, 3, 4(dados), 5(estático) e 6 sobre o HTML final.
import json, re, collections
H = open('../jogo_seduc2018_portugues.html', encoding='utf8').read()
m = re.search(r'<script id="dados" type="application/json">(.*?)</script>', H, re.S)
D = json.loads(m.group(1).replace('<\/', '</'))
J = json.load(open('data/questoes.json', encoding='utf8'))
G = json.load(open('data/gabarito.json', encoding='utf8'))
Q = D['questoes']; ok = True
def chk(nome, cond, extra=''):
    global ok; ok &= bool(cond); print(('OK   ' if cond else 'FALHA'), nome, extra)
chk('1. 80 questões, ids 1..80 sem duplicata', [q['id'] for q in Q] == list(range(1, 81)))
chk('1. cada questão com 4 alternativas A-D não vazias', all(sorted(q['alts']) == list('ABCD') and all(v.strip() for v in q['alts'].values()) for q in Q))
same = all(q['enunciado'] == j['enunciado'] and q['alts'] == j['alternativas'] for q, j in zip(Q, J['questoes']))
chk('2. enunciados e alternativas do HTML idênticos ao JSON extraído', same)
chk('2. textos compartilhados idênticos', D['textos'] == J['textos'])
chk('3. gabarito: letra confirmada com fonte, ou anulada', all((g['situacao'] == 'confirmado' and g['letra'] in 'ABCD') or g['situacao'] in ('anulada', 'sem_gabarito') for g in G['questoes'].values()) and G['fonte_definitivo']['url'] and G['fonte_definitivo']['data'])
chk('3. HTML traz a mesma situação/letra do gabarito', all(q['gab']['situacao'] == G['questoes'][str(q['id'])]['situacao'] and q['gab']['letra'] == G['questoes'][str(q['id'])]['letra'] for q in Q))
an = [q['id'] for q in Q if q['gab']['situacao'] != 'confirmado']
chk('4. anuladas sem letra e sem explicação (ficam fora da pontuação)', all(Q[i-1]['gab']['letra'] is None and Q[i-1]['exp'] is None for i in an), f'anuladas={an}')
c = collections.Counter(q['area'] for q in Q)
chk('6. contagens por área somam 80', sum(c.values()) == 80, dict(c))
chk('6. P1=30 (8/6/8/8) e P2=50', (c['EB'], c['AP'], c['LP'], c['DI']) == (8, 6, 8, 8) and c['ENS'] + c['LIT'] + c['LAS'] == 50)
chk('3. toda questão confirmada tem explicação com 3 erradas', all(len(q['exp']['por_que_erradas']) == 3 for q in Q if q['exp']))
semdados = H.replace(m.group(1), '')
ext = re.findall(r'(?:src|href|action)\s*=\s*["\']\s*(?:https?:)?//|@import|url\(\s*["\']?https?:', semdados)
chk('5. nenhuma referência externa (src/href/@import/url) fora dos dados', not ext, ext)
chk('5. imagens só em data: URI', all(i['src'].startswith('data:image/png;base64,') for q in Q for i in q['imgs']))
import struct
dpis = []
for q in J['questoes']:
    for im in q['imagens']:
        w = struct.unpack('>I', open('data/' + im['arquivo'], 'rb').read(24)[16:20])[0]; b = im['bbox']; dpis.append(w / (b[2] - b[0]) * 72)
chk('2. recortes PNG >= 150 dpi', dpis and min(dpis) >= 150, f'{len(dpis)} recortes, mín {min(dpis):.0f} dpi')
print('TUDO OK' if ok else 'HÁ FALHAS')
