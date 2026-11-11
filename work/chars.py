# Extrai linhas com marcacao inline (negrito/italico/sublinhado) a partir do PDF.
import pymupdf as m, json, re, html
d = m.open('prova.pdf')
UL_PAGES = {6, 7, 9, 11, 12}             # paginas onde ha sublinhado real no texto (conferir no relatorio)
def esc(s): return html.escape(s, quote=False)
def render(chars):
    """chars: [(c, b, i, u)] -> html com <b>,<i>,<u> agrupando marcas consecutivas."""
    out, cur = [], (False, False, False)
    def tags(st, opn):
        r = ''
        for on, t in zip(st, 'biu'):
            if on: r += f'<{t}>' if opn else f'</{t}>'
        return r
    for c, b, i, u in chars:
        st = (b, i, u)
        if st != cur:
            # fecha todas e reabre (simples e sempre bem formado); espacos nas bordas nao ganham marca
            out.append(tags(cur[::-1] if False else cur, False)); out.append(tags(st, True)); cur = st
        out.append(esc(c))
    out.append(tags(cur, False))
    return ''.join(out)
lines = []
for pn in range(2, len(d)):
    p = d[pn]
    ul = [x['rect'] for x in p.get_drawings() if x['rect'].height < 2.5 and 4 < x['rect'].width < 400 and x['rect'].height >= 0]
    bl = [b for b in p.get_text('rawdict')['blocks'] if b['type'] == 0 and b['bbox'][1] > 70 and b['bbox'][1] < 780]
    for c in 'LR':
        sel = [b for b in bl if (b['bbox'][0] < 290) == (c == 'L')]
        for b in sorted(sel, key=lambda b: b['bbox'][1]):
            for l in b['lines']:
                chs = []
                for s in l['spans']:
                    bold, ital = bool(s['flags'] & 16), bool(s['flags'] & 2)
                    for ch in s['chars']:
                        cc = ch['c']
                        if cc == '\uf0b7': cc = '\u2022'          # marcador de lista (fonte Symbol)
                        x0, y0, x1, y1 = ch['bbox']; cx = (x0 + x1) / 2
                        u = (pn + 1) in UL_PAGES and cc.strip() != '' and any(r.x0 - 1 <= cx <= r.x1 + 1 and y1 - 3.5 <= r.y0 <= y1 + 1.5 for r in ul)
                        chs.append((cc, bold, ital, u))
                while chs and chs[-1][0].isspace(): chs.pop()
                # espacos entre duas letras sublinhadas tambem recebem sublinhado
                for k in range(1, len(chs) - 1):
                    if chs[k][0].isspace() and chs[k-1][3] and chs[k+1][3]: chs[k] = (chs[k][0], chs[k][1], chs[k][2], True)
                if not chs: continue
                plain = ''.join(x[0] for x in chs)
                if re.search(r'Acesso|http|www', plain): chs = [(a, b, c, False) for a, b, c, _ in chs]   # links nao entram como sublinhado
                lines.append({'pg': pn + 1, 'col': c, 'bbox': [round(v, 1) for v in l['bbox']], 't': plain, 'h': render(chs),
                              'bold': all(x[1] for x in chs if not x[0].isspace())})
json.dump(lines, open('data/lines2.json', 'w', encoding='utf8'), ensure_ascii=False)
print(len(lines))
# relatorio de trechos sublinhados
for l in lines:
    if '<u>' in l['h']: print(l['pg'], re.findall(r'<u>(.*?)</u>', l['h']))
