# Passo 1: converte o PDF em um fluxo linear de blocos (coluna esquerda, depois direita, por pagina).
import pymupdf as m, json
d = m.open('prova.pdf')
out = []
for pn in range(1, len(d)):            # pag. 1 = capa
    p = d[pn]
    bl = [b for b in p.get_text('blocks') if b[6] == 0 and 70 < b[1] and b[3] < 778]
    span = [b for b in bl if b[0] < 290 and b[2] > 310]
    left = sorted([b for b in bl if b[2] <= 310 and b not in span], key=lambda b: b[1])
    right = sorted([b for b in bl if b[0] >= 290 and b not in span], key=lambda b: b[1])
    for col, L in (('L', left), ('R', right)):
        for b in L:
            out.append({'pg': pn+1, 'col': col, 'x0': round(b[0]), 'y0': round(b[1]), 'y1': round(b[3]), 'text': b[4]})
    if span: print('SPAN on page', pn+1, [(round(b[0]),round(b[1]),b[4][:40]) for b in span])
json.dump(out, open('data/stream.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
print(len(out), 'blocos')
