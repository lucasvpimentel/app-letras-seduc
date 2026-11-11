# Monta ../jogo_seduc2018_portugues.html a partir dos JSONs (nunca digitando questoes a mao).
import json, re, html, base64, os
J = json.load(open('data/questoes.json', encoding='utf8'))
G = json.load(open('data/gabarito.json', encoding='utf8'))
E = json.load(open('data/explicacoes.json', encoding='utf8'))
plain = lambda h: html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<br>', ' ', h))).strip()
questoes = []
for q in J['questoes']:
    i = str(q['id']); g = G['questoes'][i]; e = E[i]
    imgs = []
    for im in q['imagens']:
        b64 = base64.b64encode(open('data/' + im['arquivo'], 'rb').read()).decode()
        alt = 'Questão %d como aparece na prova. Transcrição: ' % q['id'] + ' '.join(plain(p) for p in q['enunciado'])
        imgs.append({'src': 'data:image/png;base64,' + b64, 'alt': re.sub(r'\s+', ' ', alt)})
    exp = None
    if g['situacao'] == 'confirmado':
        exp = {k: e[k] for k in ('explicacao_correta', 'por_que_erradas', 'fundamentacao', 'atualizacao')}
    questoes.append({
        'id': q['id'], 'pg': q['pg'], 'secao': q['secao'], 'area': e['area'], 'subtopico': e['subtopico'], 'item': e['item'],
        'enunciado': q['enunciado'], 'alts': q['alternativas'], 'texto': q['texto_ref'], 'imgs': imgs,
        'gab': {'situacao': g['situacao'], 'letra': g['letra'], 'preliminar': g['preliminar'],
                'alterada': g['situacao'] == 'confirmado' and g['preliminar'] != g['letra']},
        'exp': exp})
D = {'prova': {'banca': 'FUNECE / CEV-UECE', 'concurso': 'Concurso Público SEDUC/CE, Edital nº 30/2018 – SEDUC/SEPLAG',
               'cargo': 'Professor Nível A, Língua Portuguesa (código 11)', 'ano': 2018, 'aplicacao': '21/10/2018', 'caderno': 3},
     'fonteGabarito': G['fonte_definitivo'], 'questoes': questoes, 'textos': J['textos']}
# ---- 2ª prova: Professor Indígena SEDUC/CE 2023 (caderno 1 de Linguagens, questões 1-17), dados em ../work_indigena2023/data
X = '../work_indigena2023/data/'
JI = json.load(open(X + 'questoes.json', encoding='utf8')); GI = json.load(open(X + 'gabarito.json', encoding='utf8')); EI = json.load(open(X + 'explicacoes.json', encoding='utf8'))
TREF = {'t1': 'i1', 't2': 'i2'}                       # chaves dos textos de apoio no jogo
extra_q = []
for q in JI['questoes']:
    n = q['id']; g = GI['questoes'][str(n)]; e = EI[str(n)]
    extra_q.append({'id': 100 + n, 'num': n, 'prova': '2023', 'pg': q['pg'], 'secao': q['secao'], 'area': e['area'], 'subtopico': e['subtopico'], 'item': e['item'],
                    'enunciado': q['enunciado'], 'alts': q['alternativas'], 'texto': TREF.get(q['texto_ref']), 'imgs': [],
                    'gab': {'situacao': g['situacao'], 'letra': g['letra'], 'preliminar': g['preliminar'], 'alterada': g['preliminar'] != g['letra']},
                    'exp': {k: e[k] for k in ('explicacao_correta', 'por_que_erradas', 'fundamentacao', 'atualizacao')}})
extra_t = {}
for k, t in JI['textos'].items():
    nt = {'questoes': [100 + x for x in t['questoes']], 'cabecalho': t['cabecalho'], 'rodape': t['rodape']}
    if 'linhas' in t: nt['linhas'] = t['linhas']
    if 'imagem' in t:
        nt['img'] = {'src': 'data:image/png;base64,' + base64.b64encode(open(X + t['imagem'], 'rb').read()).decode(), 'alt': t['alt']}
    extra_t[TREF[k]] = nt
D['extra'] = {'prova': {'nome': 'Concurso Professor Indígena SEDUC/CE 2023 (Edital 005/2023), caderno 1 de Linguagens', 'fonteGabarito': GI['fonte_definitivo']},
              'questoes': extra_q, 'textos': extra_t}
data = json.dumps(D, ensure_ascii=False).replace('</', '<\/')     # evita fechar a tag <script>
tpl = open('template.html', encoding='utf8').read()
out = tpl.replace('/*DADOS*/', data)
open('../jogo_seduc2018_portugues.html', 'w', encoding='utf8').write(out)
open('../index.html', 'w', encoding='utf8').write(out)   # cópia para o GitHub Pages
print('ok', len(out) // 1024, 'KB')
