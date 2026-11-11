# Extrai Q1-17 (Língua Portuguesa 1-9, Educação Brasileira 10-17) do caderno 1 de Linguagens
# do concurso Professor Indígena SEDUC/CE 2023 (CEV/UECE). Rode a partir da pasta work_indigena2023.
import pymupdf as m, json, re, html
d = m.open('pdf/caderno1_linguagens.pdf')
UL_PAGES = {4}                                   # sublinhado real só na página 4 (Q9, "que"); conferido visualmente
def esc(s): return html.escape(s, quote=False)
def render(chars):
    out, cur = [], (False, False, False)
    def tags(st, opn):
        ts = [t for on, t in zip(st, 'biu') if on]
        return ''.join(f'<{t}>' for t in ts) if opn else ''.join(f'</{t}>' for t in reversed(ts))
    for c, b, i, u in chars:
        st = (b, i, u)
        if st != cur: out.append(tags(cur, False)); out.append(tags(st, True)); cur = st
        out.append(esc(c))
    out.append(tags(cur, False)); return ''.join(out)
lines = []
for pn in range(2, 6):                            # páginas 3 a 6
    p = d[pn]
    ul = [x['rect'] for x in p.get_drawings() if x['rect'].height < 2.5 and 4 < x['rect'].width < 400]
    bl = [b for b in p.get_text('rawdict')['blocks'] if b['type'] == 0 and 78.5 < b['bbox'][1] < 778]
    for c in 'LR':
        sel = [b for b in bl if (b['bbox'][0] < 300) == (c == 'L')]
        for b in sorted(sel, key=lambda b: b['bbox'][1]):
            for l in b['lines']:
                chs = []
                for s in l['spans']:
                    bold, ital = bool(s['flags'] & 16), bool(s['flags'] & 2)
                    for ch in s['chars']:
                        cc = ch['c']
                        x0, y0, x1, y1 = ch['bbox']; cx = (x0 + x1) / 2
                        u = (pn + 1) in UL_PAGES and cc.strip() != '' and any(r.x0 - 1 <= cx <= r.x1 + 1 and y1 - 3.5 <= r.y0 <= y1 + 1.5 for r in ul)
                        chs.append((cc, bold, ital, u))
                while chs and chs[-1][0].isspace(): chs.pop()
                if not chs: continue
                plain = ''.join(x[0] for x in chs)
                if re.search(r'http|www|Disponível', plain): chs = [(a, b, c2, False) for a, b, c2, _ in chs]
                lines.append({'pg': pn + 1, 'col': c, 'bbox': [round(v, 1) for v in l['bbox']], 't': plain, 'h': render(chs)})
json.dump(lines, open('lines.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
print(len(lines), 'linhas')
for l in lines:
    if '<u>' in l['h']: print('sublinhado', l['pg'], re.findall(r'<u>(.*?)</u>', l['h']))
