# Monta data/questoes.json (+ recortes PNG) a partir de data/lines2.json. Nenhum texto e reescrito:
# apenas junta linhas, separa paragrafos e converte marcas (negrito/italico/sublinhado) em tags.
import json, re
import pymupdf as m
L = json.load(open('data/lines2.json', encoding='utf8'))
HEAD = {'EDUCAÇÃO BRASILEIRA: TEMAS', 'EDUCACIONAIS E PEDAGÓGICOS', 'ADMINISTRAÇÃO PÚBLICA', 'LÍNGUA PORTUGUESA',
        'LEITURA E INTERPRETAÇÃO DE', 'DADOS E INDICADORES', 'EDUCACIONAIS', 'CONHECIMENTOS ESPECÍFICOS'}
CROP = {2, 26, 29, 31, 35, 37, 38}          # questoes com quadro/grafico/tabela/colunas: ganham recorte PNG do enunciado
VERSE = {67, 75}                            # enunciados com poemas: preserva quebras de verso
# ---------- segmentacao em questoes ----------
qs, pre, cur, alt = {}, [], None, None
for ln in L:
    t = ln['t'].strip()
    mq = re.match(r'^(\d{2})\.\s', t)
    ma = re.match(r'^([A-D])\)(\s|$)', t)
    if mq and int(mq.group(1)) == (cur['id'] + 1 if cur else 1):
        cur = {'id': int(mq.group(1)), 'pg': ln['pg'], 'stem': [ln], 'alts': {}, 'pre': pre}
        qs[cur['id']] = cur; pre = []; alt = None
    elif ma and cur and ma.group(1) == 'ABCD'[len(cur['alts'])]:
        alt = ma.group(1); cur['alts'][alt] = [ln]
    elif cur is None:
        pre.append(ln)
    elif alt is None:
        cur['stem'].append(ln)
    elif len(cur['alts']) < 4:
        cur['alts'][alt].append(ln)
    else:
        last = cur['alts']['D'][-1]
        glued = ln['pg'] == last['pg'] and ln['col'] == last['col'] and ln['bbox'][1] - last['bbox'][3] < 4
        wrapped = last['bbox'][1] > 730 and ln['bbox'][1] < 80 and not re.search(r'[.?!)”"]\s*$', last['t'])
        (cur['alts']['D'] if glued or wrapped else pre).append(ln)
assert len(qs) == 80 and all(len(q['alts']) == 4 for q in qs.values())


def joinl(lines):
    """Junta linhas de um paragrafo: sem espaco apos hifen de fim de linha (todos sao hifens reais do original)."""
    out = ''
    prev = None
    for l in lines:
        # URL quebrada no meio da linha (sem espaco no original): cola sem espaco
        url_cut = (prev is not None and re.search(r'https?://\S*$', prev['t']) and not prev['t'].endswith('.')
                   and re.match(r'[a-z0-9_/.-]', l['t'].lstrip()))
        out = (out + l['h']) if (not out or out.endswith('-') or url_cut) else out + ' ' + l['h']
        prev = l
    return out.strip()


MARK = re.compile(r'^(?:[IVX]+\.|\(\s*\))$')


def paras(lines, verse=False):
    """Agrupa linhas em paragrafos por marcador (I., (  ), bullet, Fonte), recuo a direita ou folga vertical."""
    def ind(l):   # linha recuada a direita (autoria, fonte)
        return l['bbox'][0] - (50 if l['col'] == 'L' else 315) > 80 or len(l['t']) - len(l['t'].lstrip()) >= 8
    ps, prev = [], None
    for ln in lines:
        t = ln['t'].strip()
        if prev is None or MARK.match(t) or t.startswith('•') or t.startswith('Fonte'):
            new = True
        elif ind(ln) != ind(prev) and not ps[-1][0]['t'].strip().startswith('Fonte'):
            new = True
        elif prev['pg'] == ln['pg'] and prev['col'] == ln['col']:
            new = ln['bbox'][1] - prev['bbox'][3] > 3 and not MARK.match(prev['t'].strip())
        else:
            new = False                      # quebra de coluna/pagina: continua o paragrafo
        if new: ps.append([ln])
        else: ps[-1].append(ln)
        prev = ln
    res = []
    for p in ps:
        if verse and not MARK.match(p[0]['t'].strip()) and len(p) >= 3 and sum(1 for l in p[:-1] if l['bbox'][2] - l['bbox'][0] < 215) >= 0.7 * (len(p) - 1):
            res.append('<br>'.join(l['h'] for l in p))      # verso: preserva quebras
        else:
            res.append(joinl(p))
    return res


def strip_prefix(lines, pat):
    """Remove marcador estrutural (numero da questao / letra da alternativa) do inicio."""
    first = lines[0]
    if re.fullmatch(pat + r'\s*', first['t']): return lines[1:]
    f = dict(first)
    f['h'] = re.sub(r'^(?:<[biu]>)*' + pat + r'(?:\s|</[biu]>)*', '', first['h'], count=1)
    f['t'] = re.sub(r'^' + pat + r'\s*', '', first['t'], count=1)
    assert f['h'] != first['h'], first
    return [f] + lines[1:]


def balanced(h):
    return all(h.count(f'<{t}>') == h.count(f'</{t}>') for t in 'biu')


# ---------- textos compartilhados (linhas numeradas) ----------
def texto_numerado(pre, ids):
    pre = [l for l in pre if l['t'].strip() not in HEAD]
    gut = [l for l in pre if re.fullmatch(r'\d{2}', l['t'].strip())]
    body = [l for l in pre if l not in gut]

    def num(l):
        for g in gut:
            if g['pg'] == l['pg'] and g['col'] == l['col'] and abs(g['bbox'][1] - l['bbox'][1]) < 2: return int(g['t'])
    numd = [(num(l), l) for l in body]
    first = next(i for i, (n, _) in enumerate(numd) if n)
    last = max(i for i, (n, _) in enumerate(numd) if n)
    head = [l for _, l in numd[:first]]; foot = [l for _, l in numd[last + 1:]]
    rows = [{'n': n, 't': l['h']} for n, l in numd[first:last + 1] if n]
    miss = [l['t'] for n, l in numd[first:last + 1] if not n]
    return {'questoes': ids, 'cabecalho': paras(head), 'linhas': rows, 'rodape': paras(foot), 'sem_numero': miss}


textos = {'t15': texto_numerado(qs[15]['pre'], list(range(15, 23))), 't69': texto_numerado(qs[69]['pre'], list(range(69, 73)))}
tref = {i: 't15' for i in range(15, 23)}
tref.update({i: 't69' for i in range(69, 73)})
# ---------- recortes ----------
doc = m.open('prova.pdf')
COLX = {'L': (44, 300), 'R': (308, 566)}


def crops(q):
    out, groups = [], {}
    for l in q['stem']: groups.setdefault((l['pg'], l['col']), []).append(l)
    for k, ((pg, col), ls) in enumerate(groups.items()):
        y0 = min(l['bbox'][1] for l in ls) - 4
        y1 = max(l['bbox'][3] for l in ls) + 4
        r = m.Rect(COLX[col][0], y0, COLX[col][1], min(y1, 779))
        fn = f"img/q{q['id']:02d}_{k + 1}.png"
        doc[pg - 1].get_pixmap(dpi=200, clip=r).save('data/' + fn)
        out.append({'arquivo': fn, 'pg': pg, 'bbox': [round(v) for v in r]})
    return out


# ---------- questoes ----------
def sec(i):
    return ('Educação Brasileira' if i <= 8 else 'Administração Pública' if i <= 14 else 'Língua Portuguesa' if i <= 22
            else 'Leitura e Interpretação de Dados e Indicadores Educacionais' if i <= 30
            else 'Conhecimentos Específicos de Língua Portuguesa')


final, problems = [], []
for i in range(1, 81):
    q = qs[i]
    stem = strip_prefix(q['stem'], r'\d{2}\.')
    alts = {k: joinl(strip_prefix(v, k + r'\)')) for k, v in q['alts'].items()}
    pre = [l for l in q['pre'] if l['t'].strip() not in HEAD]
    if i not in (15, 69) and pre: problems.append(('pre', i, [l['t'] for l in pre]))
    enun = paras(stem, verse=i in VERSE)
    for h in enun + list(alts.values()):
        if not balanced(h): problems.append(('tags', i, h[:80]))
    final.append({'id': i, 'pg': q['pg'], 'secao': sec(i), 'enunciado': enun, 'alternativas': alts,
                  'texto_ref': tref.get(i), 'imagens': crops(q) if i in CROP else []})
json.dump({'questoes': final, 'textos': textos}, open('data/questoes.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('ok', len(final), 'problemas:', problems)
for k, t in textos.items():
    print(k, len(t['linhas']), 'sem_numero', t['sem_numero'], 'cab', len(t['cabecalho']), 'rod', len(t['rodape']))
